#!/usr/bin/env python3
"""Static-only analyzer for the public DLSS-NR-on-AMD installer.

The program downloads a release asset, verifies its expected digest and inspects
its container/PE structure without executing any untrusted Windows code.  Only
metadata and narrowly selected strings are written to the output directory;
installer and extracted binaries are deliberately excluded from artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

try:
    import pefile  # type: ignore
except ImportError as exc:  # pragma: no cover - workflow installs it
    raise SystemExit("pefile is required: python -m pip install pefile") from exc


INTEREST_RE = re.compile(
    r"(?:"
    r"dlssnr|dlss[_ -]?nr|neural[_ -]?render|"
    r"weights?\.bin|version\.dll|nvngx_dlssnr|"
    r"\bk_(?:qkv|qkv_attn|expand|contract|conv|swin)[A-Za-z0-9_<>:,.-]*|"
    r"qkv|swin|expand2|contract2|conv_res2|"
    r"gfx12(?:00|01)|rdna4|amdhip|hip(?:Import|External|Launch|Module|Stream)|"
    r"d3d12|dxgi|zero[-_ ]copy|external[_ -]memory|external[_ -]semaphore|"
    r"DLSSNR_[A-Z0-9_]+|repack|posthist|noblend|slow_prepost|"
    r"e4m3|fp8|mfma|wmma|onnx|directml|onnxruntime|zstd|lz4|zlib|"
    r"nsis|inno setup|pyinstaller|upx"
    r")",
    re.IGNORECASE,
)

ASCII_RE = re.compile(rb"[\x20-\x7e]{4,}")
UTF16_RE = re.compile(rb"(?:[\x20-\x7e]\x00){4,}")
MAGICS = {
    "pe_mz": b"MZ",
    "zip": b"PK\x03\x04",
    "zip_eocd": b"PK\x05\x06",
    "seven_zip": b"7z\xbc\xaf\x27\x1c",
    "cab": b"MSCF",
    "gzip": b"\x1f\x8b\x08",
    "zstd": b"\x28\xb5\x2f\xfd",
    "xz": b"\xfd7zXZ\x00",
    "elf": b"\x7fELF",
}


def sha256_file(path: Path, chunk_size: int = 8 * 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())


def run_command(argv: list[str], *, cwd: Path | None = None, timeout: int = 180) -> dict[str, Any]:
    record: dict[str, Any] = {"argv": argv, "cwd": str(cwd) if cwd else None}
    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd) if cwd else None,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            env={**os.environ, "LC_ALL": "C", "LANG": "C"},
        )
        record.update(returncode=proc.returncode, output=proc.stdout[-2_000_000:])
    except FileNotFoundError:
        record.update(returncode=None, output="command not installed")
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        record.update(returncode=124, output=(output + "\nTIMEOUT")[-2_000_000:])
    except Exception as exc:  # defensive diagnostic path
        record.update(returncode=-1, output=f"{type(exc).__name__}: {exc}")
    return record


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ccore-dlssnr-static-research/1.0",
            "Accept": "application/octet-stream",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output, length=8 * 1024 * 1024)


def iter_strings(data: bytes) -> Iterable[tuple[str, int, str]]:
    for match in ASCII_RE.finditer(data):
        yield (match.group().decode("ascii", "replace"), match.start(), "ascii")
    for match in UTF16_RE.finditer(data):
        yield (match.group().decode("utf-16le", "replace"), match.start(), "utf16le")


def selected_strings(path: Path, max_hits: int = 20_000) -> list[dict[str, Any]]:
    try:
        data = path.read_bytes()
    except (OSError, MemoryError):
        return []
    hits: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for value, offset, encoding in iter_strings(data):
        if not INTEREST_RE.search(value):
            continue
        # Keep context useful but avoid dumping large embedded source/resources.
        value = value.strip().replace("\r", "\\r").replace("\n", "\\n")
        if len(value) > 500:
            value = value[:500] + "…"
        key = (encoding, value)
        if key in seen:
            continue
        seen.add(key)
        hits.append({"offset": offset, "encoding": encoding, "value": value})
        if len(hits) >= max_hits:
            break
    return hits


def find_magic_offsets(path: Path, max_per_magic: int = 256) -> dict[str, list[int]]:
    data = path.read_bytes()
    result: dict[str, list[int]] = {}
    for name, magic in MAGICS.items():
        offsets: list[int] = []
        start = 0
        while len(offsets) < max_per_magic:
            pos = data.find(magic, start)
            if pos < 0:
                break
            offsets.append(pos)
            start = pos + 1
        result[name] = offsets
    return result


def pe_metadata(path: Path) -> dict[str, Any] | None:
    try:
        pe = pefile.PE(str(path), fast_load=False)
    except Exception:
        return None

    sections = []
    for section in pe.sections:
        name = section.Name.rstrip(b"\0").decode("ascii", "replace")
        raw = section.get_data()
        sections.append(
            {
                "name": name,
                "virtual_address": int(section.VirtualAddress),
                "virtual_size": int(section.Misc_VirtualSize),
                "raw_offset": int(section.PointerToRawData),
                "raw_size": int(section.SizeOfRawData),
                "characteristics": int(section.Characteristics),
                "entropy": round(entropy(raw), 5),
            }
        )

    imports: list[dict[str, Any]] = []
    for entry in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []) or []:
        dll = entry.dll.decode("ascii", "replace") if entry.dll else ""
        symbols = []
        for item in entry.imports:
            name = item.name.decode("ascii", "replace") if item.name else None
            symbols.append({"name": name, "ordinal": item.ordinal, "address": int(item.address)})
        imports.append({"dll": dll, "symbols": symbols})

    exports: list[dict[str, Any]] = []
    export_dir = getattr(pe, "DIRECTORY_ENTRY_EXPORT", None)
    if export_dir:
        for symbol in export_dir.symbols:
            exports.append(
                {
                    "name": symbol.name.decode("ascii", "replace") if symbol.name else None,
                    "ordinal": int(symbol.ordinal),
                    "address": int(symbol.address),
                }
            )

    overlay_offset = pe.get_overlay_data_start_offset()
    overlay_size = path.stat().st_size - overlay_offset if overlay_offset is not None else 0
    optional = pe.OPTIONAL_HEADER
    result = {
        "machine": int(pe.FILE_HEADER.Machine),
        "timestamp": int(pe.FILE_HEADER.TimeDateStamp),
        "characteristics": int(pe.FILE_HEADER.Characteristics),
        "image_base": int(optional.ImageBase),
        "entry_point_rva": int(optional.AddressOfEntryPoint),
        "subsystem": int(optional.Subsystem),
        "dll_characteristics": int(optional.DllCharacteristics),
        "sections": sections,
        "imports": imports,
        "exports": exports,
        "overlay_offset": overlay_offset,
        "overlay_size": overlay_size,
    }
    try:
        result["imphash"] = pe.get_imphash()
    except Exception:
        result["imphash"] = None
    pe.close()
    return result


def identify_file(path: Path) -> str:
    command = run_command(["file", "-b", str(path)], timeout=30)
    return command.get("output", "").strip()


def analyze_file(path: Path, root: Path, *, collect_strings: bool = True) -> dict[str, Any]:
    rel = str(path.relative_to(root)) if path != root else path.name
    record: dict[str, Any] = {
        "path": rel,
        "size": path.stat().st_size,
        "sha256": sha256_file(path),
        "file_type": identify_file(path),
    }
    pe = pe_metadata(path)
    if pe is not None:
        record["pe"] = pe
    if collect_strings and path.stat().st_size <= 256 * 1024 * 1024:
        record["interesting_strings"] = selected_strings(path)
    return record


def attempt_extraction(installer: Path, extraction_root: Path) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    seven_dir = extraction_root / "seven_zip"
    seven_dir.mkdir(parents=True, exist_ok=True)
    attempts.append(run_command(["7z", "x", "-y", f"-o{seven_dir}", str(installer)], timeout=300))

    inno_dir = extraction_root / "inno"
    inno_dir.mkdir(parents=True, exist_ok=True)
    attempts.append(run_command(["innoextract", "--silent", "--output-dir", str(inno_dir), str(installer)], timeout=300))

    cab_dir = extraction_root / "cab"
    cab_dir.mkdir(parents=True, exist_ok=True)
    attempts.append(run_command(["cabextract", "-q", "-d", str(cab_dir), str(installer)], timeout=300))
    return attempts


def write_markdown(report: dict[str, Any], destination: Path) -> None:
    installer = report["installer"]
    lines = [
        "# Daniel DLSS-NR-on-AMD installer — static analysis",
        "",
        "> Static inspection only. The Windows executable was never launched.",
        "",
        "## Integrity",
        "",
        f"- URL: `{report['source_url']}`",
        f"- Size: `{installer['size']}` bytes",
        f"- SHA-256: `{installer['sha256']}`",
        f"- Expected SHA-256 matched: `{report['expected_sha256_matched']}`",
        f"- File type: `{installer['file_type']}`",
        "",
        "## Container and extraction",
        "",
    ]
    for attempt in report["extraction_attempts"]:
        lines.append(f"- `{' '.join(attempt['argv'])}` → `{attempt.get('returncode')}`")
    lines.extend(["", "## Extracted-file manifest", ""])
    for item in report["extracted_files"]:
        lines.append(f"- `{item['path']}` — {item['size']} bytes — `{item['sha256']}` — {item['file_type']}")
    lines.extend(["", "## Relevant implementation evidence", ""])
    evidence = report.get("evidence_summary", {})
    for key, values in evidence.items():
        lines.append(f"### {key}")
        lines.append("")
        if values:
            for value in values:
                lines.append(f"- `{value}`")
        else:
            lines.append("- No matching static string found.")
        lines.append("")
    lines.extend(
        [
            "## Interpretation guardrail",
            "",
            "A string/import hit proves that a name or dependency is present in the binary; it does not, by itself, prove runtime control flow. The next gate is cross-referencing these hits with code and validating the generated weight file against independently captured tensors.",
            "",
        ]
    )
    destination.write_text("\n".join(lines), encoding="utf-8")


def summarize_evidence(files: list[dict[str, Any]]) -> dict[str, list[str]]:
    groups: dict[str, tuple[re.Pattern[str], list[str]]] = {
        "weight_artifacts": (re.compile(r"weights?\.bin|weight conversion|nvngx_dlssnr", re.I), []),
        "kernel_families": (re.compile(r"\bk_(?:qkv|qkv_attn|expand|contract|conv|swin)[A-Za-z0-9_<>:,.-]*", re.I), []),
        "hip_rdna4": (re.compile(r"gfx12(?:00|01)|rdna4|amdhip|hip(?:Import|External|Launch|Module|Stream)", re.I), []),
        "interop": (re.compile(r"d3d12|dxgi|zero[-_ ]copy|external[_ -](?:memory|semaphore)", re.I), []),
        "debug_controls": (re.compile(r"DLSSNR_[A-Z0-9_]+|repack|posthist|noblend|slow_prepost", re.I), []),
        "model_ops": (re.compile(r"qkv|swin|expand2|contract2|conv_res2|e4m3|fp8|mfma|wmma", re.I), []),
        "alternative_runtimes": (re.compile(r"onnx|directml|onnxruntime", re.I), []),
        "packers_compression": (re.compile(r"nsis|inno setup|pyinstaller|upx|zstd|lz4|zlib", re.I), []),
    }
    for item in files:
        for hit in item.get("interesting_strings", []):
            value = hit["value"]
            for _, (pattern, values) in groups.items():
                for match in pattern.findall(value):
                    text = match if isinstance(match, str) else "".join(match)
                    text = text.strip()
                    if text and text not in values:
                        values.append(text[:300])
    return {name: values[:200] for name, (_, values) in groups.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="dlssnr-daniel-static-") as temp_name:
        temp = Path(temp_name)
        installer = temp / "dlssnr_on_amd_setup.exe"
        extraction_root = temp / "extracted"
        extraction_root.mkdir()

        download(args.url, installer)
        actual_digest = sha256_file(installer)
        expected = args.expected_sha256.lower().strip()
        if actual_digest != expected:
            raise SystemExit(f"SHA-256 mismatch: expected {expected}, got {actual_digest}")

        list_result = run_command(["7z", "l", "-slt", str(installer)], timeout=180)
        (output / "7z-list.txt").write_text(list_result.get("output", ""), encoding="utf-8")
        extraction_attempts = attempt_extraction(installer, extraction_root)

        installer_record = analyze_file(installer, temp)
        installer_record["magic_offsets"] = find_magic_offsets(installer)
        extracted_records: list[dict[str, Any]] = []
        for path in sorted(extraction_root.rglob("*")):
            if not path.is_file():
                continue
            try:
                extracted_records.append(analyze_file(path, extraction_root))
            except Exception as exc:
                extracted_records.append(
                    {
                        "path": str(path.relative_to(extraction_root)),
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )

        all_records = [installer_record, *extracted_records]
        report = {
            "schema_version": 1,
            "analysis_mode": "static_only_never_executed",
            "source_url": args.url,
            "expected_sha256": expected,
            "expected_sha256_matched": actual_digest == expected,
            "installer": installer_record,
            "container_listing": {
                "returncode": list_result.get("returncode"),
                "artifact": "7z-list.txt",
            },
            "extraction_attempts": extraction_attempts,
            "extracted_files": extracted_records,
            "evidence_summary": summarize_evidence(all_records),
        }

        (output / "report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        write_markdown(report, output / "report.md")

        # Explicitly assert that no downloaded/extracted executable is under output.
        forbidden = [p for p in output.rglob("*") if p.is_file() and p.suffix.lower() in {".exe", ".dll", ".bin", ".so", ".cubin", ".hsaco"}]
        if forbidden:
            raise SystemExit("forbidden binary leaked into report output: " + ", ".join(map(str, forbidden)))

    print(json.dumps({"status": "ok", "report": str(output / "report.json")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
