#!/usr/bin/env python3
"""Identify embedded PE and AMDGPU ELF payloads in Daniel's public installer.

This is a metadata-only, static analysis tool. Payload bytes are carved only into
an ephemeral directory so standard parsers can inspect them; no PE/ELF payload
is copied into the report artifact.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import struct
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

import pefile  # type: ignore
from elftools.elf.elffile import ELFFile  # type: ignore


PRINTABLE = re.compile(rb"[\x20-\x7e]{4,}")
KERNEL_HINT = re.compile(
    r"(?:^|_)(?:k_(?:swin|pre|post|qkv|conv|expand|contract|repack)|swin_layer|g_e4m3_lut)",
    re.IGNORECASE,
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def download(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "ccore-dlssnr-static-research/1.0", "Accept": "application/octet-stream"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def scan_all(data: bytes, needle: bytes) -> list[int]:
    offsets: list[int] = []
    start = 0
    while True:
        pos = data.find(needle, start)
        if pos < 0:
            return offsets
        offsets.append(pos)
        start = pos + 1


def pe_candidate(data: bytes, offset: int) -> dict[str, Any] | None:
    suffix = data[offset:]
    if len(suffix) < 0x100 or suffix[:2] != b"MZ":
        return None
    e_lfanew = struct.unpack_from("<I", suffix, 0x3C)[0]
    if e_lfanew < 0x40 or e_lfanew > 0x1000 or e_lfanew + 0x108 > len(suffix):
        return None
    if suffix[e_lfanew : e_lfanew + 4] != b"PE\0\0":
        return None
    try:
        pe = pefile.PE(data=suffix, fast_load=False)
    except Exception:
        return None
    try:
        machine = int(pe.FILE_HEADER.Machine)
        section_count = int(pe.FILE_HEADER.NumberOfSections)
        if machine not in {0x14C, 0x8664, 0xAA64} or not (1 <= section_count <= 96):
            return None
        sections: list[dict[str, Any]] = []
        intrinsic_end = int(pe.OPTIONAL_HEADER.SizeOfHeaders)
        for section in pe.sections:
            name = section.Name.rstrip(b"\0").decode("ascii", "replace")
            raw_offset = int(section.PointerToRawData)
            raw_size = int(section.SizeOfRawData)
            virtual_size = int(section.Misc_VirtualSize)
            if raw_offset < 0 or raw_size < 0 or raw_offset + raw_size > len(suffix):
                return None
            intrinsic_end = max(intrinsic_end, raw_offset + raw_size)
            sections.append(
                {
                    "name": name,
                    "virtual_address": int(section.VirtualAddress),
                    "virtual_size": virtual_size,
                    "raw_offset": raw_offset,
                    "raw_size": raw_size,
                    "characteristics": int(section.Characteristics),
                }
            )

        # Authenticode uses a file offset rather than an RVA.
        security = pe.OPTIONAL_HEADER.DATA_DIRECTORY[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]]
        if security.VirtualAddress and security.Size:
            intrinsic_end = max(intrinsic_end, int(security.VirtualAddress + security.Size))
        intrinsic_end = min(intrinsic_end, len(suffix))

        imports: list[dict[str, Any]] = []
        for entry in getattr(pe, "DIRECTORY_ENTRY_IMPORT", []) or []:
            dll = entry.dll.decode("ascii", "replace") if entry.dll else ""
            names = []
            for symbol in entry.imports:
                names.append(symbol.name.decode("ascii", "replace") if symbol.name else f"ordinal:{symbol.ordinal}")
            imports.append({"dll": dll, "symbols": names})

        exports: list[dict[str, Any]] = []
        export_dir = getattr(pe, "DIRECTORY_ENTRY_EXPORT", None)
        if export_dir:
            for symbol in export_dir.symbols:
                exports.append(
                    {
                        "name": symbol.name.decode("ascii", "replace") if symbol.name else None,
                        "ordinal": int(symbol.ordinal),
                        "rva": int(symbol.address),
                    }
                )

        resources: list[dict[str, Any]] = []
        resource_dir = getattr(pe, "DIRECTORY_ENTRY_RESOURCE", None)
        if resource_dir:
            for type_entry in resource_dir.entries:
                type_name = str(type_entry.name) if type_entry.name else int(type_entry.struct.Id)
                directory = getattr(type_entry, "directory", None)
                if directory is None:
                    continue
                for name_entry in directory.entries:
                    name = str(name_entry.name) if name_entry.name else int(name_entry.struct.Id)
                    lang_dir = getattr(name_entry, "directory", None)
                    if lang_dir is None:
                        continue
                    for lang_entry in lang_dir.entries:
                        data_entry = getattr(lang_entry, "data", None)
                        if data_entry is None:
                            continue
                        resources.append(
                            {
                                "type": type_name,
                                "name": name,
                                "lang": int(lang_entry.struct.Id),
                                "rva": int(data_entry.struct.OffsetToData),
                                "size": int(data_entry.struct.Size),
                            }
                        )

        file_kind = "dll" if int(pe.FILE_HEADER.Characteristics) & 0x2000 else "exe"
        return {
            "offset": offset,
            "kind": file_kind,
            "machine": machine,
            "section_count": section_count,
            "timestamp": int(pe.FILE_HEADER.TimeDateStamp),
            "image_base": int(pe.OPTIONAL_HEADER.ImageBase),
            "entry_point_rva": int(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
            "size_of_image": int(pe.OPTIONAL_HEADER.SizeOfImage),
            "intrinsic_size": intrinsic_end,
            "intrinsic_sha256": sha256(suffix[:intrinsic_end]),
            "sections": sections,
            "imports": imports,
            "exports": exports,
            "resources": resources,
        }
    finally:
        pe.close()


def elf_candidate(data: bytes, offset: int) -> dict[str, Any] | None:
    suffix = data[offset:]
    if not suffix.startswith(b"\x7fELF"):
        return None
    try:
        elf = ELFFile(io.BytesIO(suffix))
    except Exception:
        return None

    intrinsic_end = 0
    sections: list[dict[str, Any]] = []
    for section in elf.iter_sections():
        sh_offset = int(section["sh_offset"])
        sh_size = int(section["sh_size"])
        sh_type = str(section["sh_type"])
        # SHT_NOBITS occupies no bytes in the file.
        if sh_type != "SHT_NOBITS":
            intrinsic_end = max(intrinsic_end, sh_offset + sh_size)
        sections.append(
            {
                "name": section.name,
                "type": sh_type,
                "offset": sh_offset,
                "size": sh_size,
                "address": int(section["sh_addr"]),
                "flags": int(section["sh_flags"]),
            }
        )

    for segment in elf.iter_segments():
        intrinsic_end = max(intrinsic_end, int(segment["p_offset"]) + int(segment["p_filesz"]))
    intrinsic_end = max(
        intrinsic_end,
        int(elf.header["e_ehsize"]),
        int(elf.header["e_phoff"]) + int(elf.header["e_phentsize"]) * int(elf.header["e_phnum"]),
        int(elf.header["e_shoff"]) + int(elf.header["e_shentsize"]) * int(elf.header["e_shnum"]),
    )
    if intrinsic_end <= 0 or intrinsic_end > len(suffix):
        return None

    symbols: list[dict[str, Any]] = []
    for section in elf.iter_sections():
        if not hasattr(section, "iter_symbols"):
            continue
        try:
            iterator = section.iter_symbols()
        except Exception:
            continue
        for symbol in iterator:
            name = symbol.name
            if not name:
                continue
            if KERNEL_HINT.search(name) or name.endswith(".kd"):
                symbols.append(
                    {
                        "name": name,
                        "value": int(symbol["st_value"]),
                        "size": int(symbol["st_size"]),
                        "bind": str(symbol["st_info"]["bind"]),
                        "type": str(symbol["st_info"]["type"]),
                        "section_index": str(symbol["st_shndx"]),
                    }
                )

    notes: list[dict[str, Any]] = []
    for section in elf.iter_sections():
        if not hasattr(section, "iter_notes"):
            continue
        try:
            iterator = section.iter_notes()
        except Exception:
            continue
        for note in iterator:
            desc = note.get("n_desc")
            if isinstance(desc, bytes):
                printable = [m.group().decode("ascii", "replace") for m in PRINTABLE.finditer(desc)]
                desc_summary: Any = {
                    "size": len(desc),
                    "sha256": sha256(desc),
                    "printable": printable[:100],
                    "hex_prefix": desc[:64].hex(),
                }
            else:
                text = str(desc)
                desc_summary = text[:10_000]
            notes.append(
                {
                    "section": section.name,
                    "name": str(note.get("n_name")),
                    "type": str(note.get("n_type")),
                    "desc": desc_summary,
                }
            )

    return {
        "offset": offset,
        "class": int(elf.elfclass),
        "little_endian": bool(elf.little_endian),
        "machine": str(elf.header["e_machine"]),
        "type": str(elf.header["e_type"]),
        "flags": int(elf.header["e_flags"]),
        "entry": int(elf.header["e_entry"]),
        "intrinsic_size": intrinsic_end,
        "intrinsic_sha256": sha256(suffix[:intrinsic_end]),
        "sections": sections,
        "kernel_symbols": symbols,
        "notes": notes,
    }


def run_text(argv: list[str], timeout: int = 120) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            argv,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
        return {"argv": argv, "returncode": proc.returncode, "output": proc.stdout[-4_000_000:]}
    except FileNotFoundError:
        return {"argv": argv, "returncode": None, "output": "command not installed"}
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout.decode("utf-8", "replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        return {"argv": argv, "returncode": 124, "output": output[-4_000_000:] + "\nTIMEOUT"}


def write_markdown(report: dict[str, Any], output: Path) -> None:
    lines = [
        "# Embedded payload map",
        "",
        "> Metadata-only static analysis; no embedded executable or code object is included.",
        "",
        f"- Installer SHA-256: `{report['installer_sha256']}`",
        f"- Valid PE candidates: `{len(report['pe_candidates'])}`",
        f"- Valid ELF candidates: `{len(report['elf_candidates'])}`",
        "",
        "## PE candidates",
        "",
    ]
    for candidate in report["pe_candidates"]:
        lines.extend(
            [
                f"### PE at `0x{candidate['offset']:x}`",
                "",
                f"- Kind: `{candidate['kind']}`",
                f"- Machine: `0x{candidate['machine']:x}`",
                f"- Sections: `{candidate['section_count']}`",
                f"- Intrinsic size: `{candidate['intrinsic_size']}`",
                f"- SHA-256 of intrinsic image: `{candidate['intrinsic_sha256']}`",
                f"- Imported DLLs: `{', '.join(x['dll'] for x in candidate['imports'])}`",
                f"- Export count: `{len(candidate['exports'])}`",
                f"- Resource count: `{len(candidate['resources'])}`",
                "",
            ]
        )
    lines.extend(["## AMDGPU ELF candidates", ""])
    for index, candidate in enumerate(report["elf_candidates"]):
        names = [x["name"] for x in candidate["kernel_symbols"]]
        lines.extend(
            [
                f"### ELF {index} at `0x{candidate['offset']:x}`",
                "",
                f"- Machine: `{candidate['machine']}`",
                f"- Intrinsic size: `{candidate['intrinsic_size']}`",
                f"- SHA-256: `{candidate['intrinsic_sha256']}`",
                f"- Sections: `{len(candidate['sections'])}`",
                f"- Notes: `{len(candidate['notes'])}`",
                f"- Kernel-related symbols: `{len(names)}`",
                "",
            ]
        )
        for name in names:
            lines.append(f"  - `{name}`")
        lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    data = download(args.url)
    actual = sha256(data)
    expected = args.expected_sha256.lower().strip()
    if actual != expected:
        raise SystemExit(f"SHA-256 mismatch: expected {expected}, got {actual}")

    pe_candidates = [x for offset in scan_all(data, b"MZ") if (x := pe_candidate(data, offset)) is not None]
    elf_candidates = [x for offset in scan_all(data, b"\x7fELF") if (x := elf_candidate(data, offset)) is not None]

    args.output.mkdir(parents=True, exist_ok=True)
    tool_reports: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="dlssnr-payloads-") as temp_name:
        temp = Path(temp_name)
        for index, candidate in enumerate(elf_candidates):
            start = candidate["offset"]
            end = start + candidate["intrinsic_size"]
            path = temp / f"payload-{index}.elf"
            path.write_bytes(data[start:end])
            invocations = []
            for argv in (
                ["llvm-readelf", "--file-header", "--sections", "--symbols", "--notes", str(path)],
                ["llvm-readobj", "--file-headers", "--sections", "--symbols", "--notes", str(path)],
                ["readelf", "-h", "-S", "-s", "-n", str(path)],
            ):
                result = run_text(argv)
                invocations.append(result)
                if result["returncode"] == 0:
                    break
            tool_report = invocations[-1]
            for result in invocations:
                if result["returncode"] == 0:
                    tool_report = result
                    break
            report_name = f"elf-{index}-tool-report.txt"
            (args.output / report_name).write_text(tool_report["output"], encoding="utf-8")
            tool_reports.append(
                {
                    "elf_index": index,
                    "artifact": report_name,
                    "argv": tool_report["argv"],
                    "returncode": tool_report["returncode"],
                }
            )

    report = {
        "schema_version": 1,
        "analysis_mode": "static_only_never_executed",
        "installer_size": len(data),
        "installer_sha256": actual,
        "valid_pe_offsets": [x["offset"] for x in pe_candidates],
        "valid_elf_offsets": [x["offset"] for x in elf_candidates],
        "pe_candidates": pe_candidates,
        "elf_candidates": elf_candidates,
        "tool_reports": tool_reports,
    }
    (args.output / "payload-map.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_markdown(report, args.output / "payload-map.md")

    forbidden = {".exe", ".dll", ".bin", ".so", ".cubin", ".hsaco", ".elf"}
    leaked = [str(p) for p in args.output.rglob("*") if p.is_file() and p.suffix.lower() in forbidden]
    if leaked:
        raise SystemExit("binary payload leaked into output: " + ", ".join(leaked))

    print(json.dumps({"status": "ok", "pe": len(pe_candidates), "elf": len(elf_candidates)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
