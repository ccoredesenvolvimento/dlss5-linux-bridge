#!/usr/bin/env python3
"""Extract Daniel's official ``version.dll`` from a verified release installer.

The public v0.2.9 installer embeds the game runtime as a complete PE DLL. This
utility downloads or reads that installer, verifies its SHA-256, locates the
embedded runtime by structural markers, verifies the runtime SHA-256 and writes
it atomically. It never executes the installer or DLL.

The extracted binary remains Daniel's work. Use it only under the upstream
project's terms and do not commit or redistribute it from this repository.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import sys
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

import pefile  # type: ignore

DEFAULT_URL = (
    "https://github.com/danielblnc/DLSS-NR-on-AMD/releases/download/"
    "v0.2.9/dlssnr_on_amd_setup.exe"
)
DEFAULT_INSTALLER_SHA256 = "b4b31e19e1d9028b3d63b7ac5074d7f71ede736d6185c11d25863f6415c6ece9"
DEFAULT_RUNTIME_SHA256 = "69d06ea9fc78abc22d403a3108c38f897d76be52d409209ef08ed4743ab8ded2"
EXPECTED_EXPORTS = {
    "DirectInput8Create",
    "DllCanUnloadNow",
    "DllGetClassObject",
    "DllRegisterServer",
    "DllUnregisterServer",
}
EXPECTED_IMPORT_DLL = "amdhip64_7.dll"


class ExtractionError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class PeCandidate:
    offset: int
    intrinsic_size: int
    sha256: str
    machine: int
    is_dll: bool
    imports: tuple[str, ...]
    exports: tuple[str, ...]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ccore-dlssnr-interoperability/1.0",
            "Accept": "application/octet-stream",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def scan(data: bytes, needle: bytes) -> Iterable[int]:
    start = 0
    while True:
        position = data.find(needle, start)
        if position < 0:
            return
        yield position
        start = position + 1


def intrinsic_size(pe: pefile.PE, available: int) -> int:
    end = int(pe.OPTIONAL_HEADER.SizeOfHeaders)
    for section in pe.sections:
        raw_offset = int(section.PointerToRawData)
        raw_size = int(section.SizeOfRawData)
        if raw_offset < 0 or raw_size < 0 or raw_offset + raw_size > available:
            raise ExtractionError("embedded PE section lies outside the installer")
        end = max(end, raw_offset + raw_size)
    security = pe.OPTIONAL_HEADER.DATA_DIRECTORY[
        pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
    ]
    if security.VirtualAddress and security.Size:
        certificate_end = int(security.VirtualAddress) + int(security.Size)
        if certificate_end > available:
            raise ExtractionError("embedded PE certificate lies outside the installer")
        end = max(end, certificate_end)
    if end <= 0 or end > available:
        raise ExtractionError("invalid embedded PE intrinsic size")
    return end


def parse_candidate(data: bytes, offset: int) -> PeCandidate | None:
    suffix = data[offset:]
    if len(suffix) < 0x100 or suffix[:2] != b"MZ":
        return None
    try:
        e_lfanew = struct.unpack_from("<I", suffix, 0x3C)[0]
    except struct.error:
        return None
    if e_lfanew < 0x40 or e_lfanew > 0x1000:
        return None
    if e_lfanew + 4 > len(suffix) or suffix[e_lfanew : e_lfanew + 4] != b"PE\0\0":
        return None
    try:
        pe = pefile.PE(data=suffix, fast_load=False)
    except Exception:
        return None
    try:
        count = int(pe.FILE_HEADER.NumberOfSections)
        if not (1 <= count <= 96):
            return None
        size = intrinsic_size(pe, len(suffix))
        imports: list[str] = []
        for entry in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []) or []:
            if entry.dll:
                imports.append(entry.dll.decode("ascii", "replace"))
        exports: list[str] = []
        export_directory = getattr(pe, "DIRECTORY_ENTRY_EXPORT", None)
        if export_directory is not None:
            for symbol in export_directory.symbols:
                if symbol.name:
                    exports.append(symbol.name.decode("ascii", "replace"))
        image = suffix[:size]
        return PeCandidate(
            offset=offset,
            intrinsic_size=size,
            sha256=sha256_bytes(image),
            machine=int(pe.FILE_HEADER.Machine),
            is_dll=bool(int(pe.FILE_HEADER.Characteristics) & 0x2000),
            imports=tuple(sorted(set(imports), key=str.lower)),
            exports=tuple(sorted(set(exports))),
        )
    finally:
        pe.close()


def locate_runtime(data: bytes, expected_runtime_sha256: str) -> tuple[PeCandidate, bytes]:
    candidates = [
        candidate
        for offset in scan(data, b"MZ")
        if (candidate := parse_candidate(data, offset)) is not None
    ]
    exact = [candidate for candidate in candidates if candidate.sha256 == expected_runtime_sha256]
    if len(exact) == 1:
        candidate = exact[0]
    elif len(exact) > 1:
        raise ExtractionError("installer contains duplicate runtime images with the expected hash")
    else:
        structural = [
            candidate
            for candidate in candidates
            if candidate.machine == 0x8664
            and candidate.is_dll
            and EXPECTED_IMPORT_DLL.lower() in {name.lower() for name in candidate.imports}
            and EXPECTED_EXPORTS.issubset(set(candidate.exports))
        ]
        if len(structural) != 1:
            summary = [
                {
                    "offset": item.offset,
                    "size": item.intrinsic_size,
                    "sha256": item.sha256,
                    "is_dll": item.is_dll,
                    "imports": item.imports,
                    "exports": item.exports,
                }
                for item in candidates
            ]
            raise ExtractionError(
                "could not identify exactly one Daniel runtime DLL; candidates="
                + json.dumps(summary, ensure_ascii=False)
            )
        candidate = structural[0]
        if candidate.sha256 != expected_runtime_sha256:
            raise ExtractionError(
                "runtime structure matched, but its SHA-256 differs from the pinned release: "
                f"expected {expected_runtime_sha256}, got {candidate.sha256}"
            )
    start = candidate.offset
    end = start + candidate.intrinsic_size
    return candidate, data[start:end]


def write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def execute(
    output: Path,
    *,
    installer: Path | None,
    url: str,
    expected_installer_sha256: str,
    expected_runtime_sha256: str,
    inspect_only: bool,
    report_path: Path | None,
) -> dict[str, Any]:
    if installer is None:
        data = download(url)
        source = url
    else:
        installer = installer.resolve()
        if not installer.is_file():
            raise ExtractionError(f"installer not found: {installer}")
        data = installer.read_bytes()
        source = str(installer)
    installer_digest = sha256_bytes(data)
    expected_installer = expected_installer_sha256.lower().strip().removeprefix("sha256:")
    expected_runtime = expected_runtime_sha256.lower().strip().removeprefix("sha256:")
    if installer_digest != expected_installer:
        raise ExtractionError(
            f"installer SHA-256 mismatch: expected {expected_installer}, got {installer_digest}"
        )
    candidate, runtime = locate_runtime(data, expected_runtime)
    if sha256_bytes(runtime) != expected_runtime:
        raise AssertionError("runtime digest changed after carving")
    report: dict[str, Any] = {
        "schema_version": 1,
        "analysis_mode": "static_extract_never_executed",
        "source": source,
        "installer_sha256": installer_digest,
        "runtime_offset": candidate.offset,
        "runtime_size": candidate.intrinsic_size,
        "runtime_sha256": candidate.sha256,
        "machine": f"0x{candidate.machine:04x}",
        "imports": list(candidate.imports),
        "exports": list(candidate.exports),
        "output": str(output.resolve()),
        "inspect_only": inspect_only,
        "verified": True,
    }
    if not inspect_only:
        write_atomic(output.resolve(), runtime)
        if output.stat().st_size != candidate.intrinsic_size or sha256_file(output) != expected_runtime:
            try:
                output.unlink()
            except OSError:
                pass
            raise ExtractionError("written runtime failed size/hash verification")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, nargs="?", default=Path("version.dll"))
    parser.add_argument("--installer", type=Path)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--expected-installer-sha256", default=DEFAULT_INSTALLER_SHA256)
    parser.add_argument("--expected-runtime-sha256", default=DEFAULT_RUNTIME_SHA256)
    parser.add_argument("--inspect-only", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    try:
        report = execute(
            args.output,
            installer=args.installer,
            url=args.url,
            expected_installer_sha256=args.expected_installer_sha256,
            expected_runtime_sha256=args.expected_runtime_sha256,
            inspect_only=args.inspect_only,
            report_path=args.report,
        )
    except (OSError, ExtractionError, urllib.error.URLError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
