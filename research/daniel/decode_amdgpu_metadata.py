#!/usr/bin/env python3
"""Decode AMDGPU code-object metadata embedded in Daniel's public installer.

Only architecture, kernel names and ABI/resource metadata are retained. Code
bytes, constants and executable payloads never leave the temporary directory.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import struct
import urllib.request
from pathlib import Path
from typing import Any, Iterable

import msgpack  # type: ignore
from elftools.elf.elffile import ELFFile  # type: ignore


KERNEL_RE = re.compile(
    r"(?:k_(?:swin|pre|post|qkv|conv|expand|contract|repack)|swin_layer|g_e4m3_lut)",
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


def scan(data: bytes, needle: bytes) -> Iterable[int]:
    start = 0
    while True:
        pos = data.find(needle, start)
        if pos < 0:
            return
        yield pos
        start = pos + 1


def normalize(value: Any) -> Any:
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except UnicodeDecodeError:
            return {"bytes_size": len(value), "sha256": sha256(value), "hex_prefix": value[:32].hex()}
    if isinstance(value, dict):
        return {str(normalize(key)): normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def intrinsic_elf_size(elf: ELFFile, available: int) -> int | None:
    end = max(
        int(elf.header["e_ehsize"]),
        int(elf.header["e_phoff"]) + int(elf.header["e_phentsize"]) * int(elf.header["e_phnum"]),
        int(elf.header["e_shoff"]) + int(elf.header["e_shentsize"]) * int(elf.header["e_shnum"]),
    )
    for section in elf.iter_sections():
        if str(section["sh_type"]) != "SHT_NOBITS":
            end = max(end, int(section["sh_offset"]) + int(section["sh_size"]))
    for segment in elf.iter_segments():
        end = max(end, int(segment["p_offset"]) + int(segment["p_filesz"]))
    return end if 0 < end <= available else None


def decode_note(desc: Any) -> Any | None:
    if not isinstance(desc, (bytes, bytearray)):
        return None
    raw = bytes(desc)
    try:
        return normalize(msgpack.unpackb(raw, raw=False, strict_map_key=False))
    except Exception:
        return None


def find_key(value: Any, names: set[str]) -> Any | None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized_key = str(key).lstrip(".")
            if normalized_key in names:
                return item
        for item in value.values():
            found = find_key(item, names)
            if found is not None:
                return found
    elif isinstance(value, list):
        for item in value:
            found = find_key(item, names)
            if found is not None:
                return found
    return None


def get_field(mapping: dict[str, Any], *names: str) -> Any:
    wanted = {name.lstrip(".") for name in names}
    for key, value in mapping.items():
        if str(key).lstrip(".") in wanted:
            return value
    return None


def sanitize_kernel(kernel: dict[str, Any]) -> dict[str, Any]:
    name = get_field(kernel, "name")
    symbol = get_field(kernel, "symbol")
    args = get_field(kernel, "args") or []
    sanitized_args: list[dict[str, Any]] = []
    if isinstance(args, list):
        for arg in args:
            if not isinstance(arg, dict):
                continue
            sanitized_args.append(
                {
                    "name": get_field(arg, "name"),
                    "type_name": get_field(arg, "type_name"),
                    "size": get_field(arg, "size"),
                    "offset": get_field(arg, "offset"),
                    "value_kind": get_field(arg, "value_kind"),
                    "value_type": get_field(arg, "value_type"),
                    "address_space": get_field(arg, "address_space"),
                    "access": get_field(arg, "actual_access", "access"),
                }
            )
    fields = {
        "name": name,
        "symbol": symbol,
        "language": get_field(kernel, "language"),
        "language_version": get_field(kernel, "language_version"),
        "kernarg_segment_size": get_field(kernel, "kernarg_segment_size"),
        "kernarg_segment_align": get_field(kernel, "kernarg_segment_align"),
        "group_segment_fixed_size": get_field(kernel, "group_segment_fixed_size"),
        "private_segment_fixed_size": get_field(kernel, "private_segment_fixed_size"),
        "sgpr_count": get_field(kernel, "sgpr_count"),
        "vgpr_count": get_field(kernel, "vgpr_count"),
        "sgpr_spill_count": get_field(kernel, "sgpr_spill_count"),
        "vgpr_spill_count": get_field(kernel, "vgpr_spill_count"),
        "max_flat_workgroup_size": get_field(kernel, "max_flat_workgroup_size"),
        "reqd_workgroup_size": get_field(kernel, "reqd_workgroup_size"),
        "wavefront_size": get_field(kernel, "wavefront_size"),
        "uniform_work_group_size": get_field(kernel, "uniform_work_group_size"),
        "args": sanitized_args,
    }
    return {key: value for key, value in fields.items() if value is not None}


def analyze_elf(blob: bytes, absolute_offset: int) -> dict[str, Any] | None:
    try:
        elf = ELFFile(io.BytesIO(blob))
    except Exception:
        return None
    size = intrinsic_elf_size(elf, len(blob))
    if size is None or str(elf.header["e_machine"]) != "EM_AMDGPU":
        return None

    decoded_notes: list[dict[str, Any]] = []
    kernels: list[dict[str, Any]] = []
    metadata_versions: list[Any] = []
    targets: list[str] = []

    for section in elf.iter_sections():
        if not hasattr(section, "iter_notes"):
            continue
        try:
            notes = section.iter_notes()
        except Exception:
            continue
        for note in notes:
            desc = note.get("n_desc")
            decoded = decode_note(desc)
            note_record: dict[str, Any] = {
                "section": section.name,
                "name": str(note.get("n_name")),
                "type": str(note.get("n_type")),
                "desc_size": len(desc) if isinstance(desc, (bytes, bytearray)) else None,
                "desc_sha256": sha256(bytes(desc)) if isinstance(desc, (bytes, bytearray)) else None,
                "decoded": decoded is not None,
            }
            if decoded is not None:
                version = find_key(decoded, {"amdhsa.version", "version"})
                if version is not None and version not in metadata_versions:
                    metadata_versions.append(version)
                kernel_list = find_key(decoded, {"amdhsa.kernels", "kernels"})
                if isinstance(kernel_list, list):
                    for item in kernel_list:
                        if not isinstance(item, dict):
                            continue
                        sanitized = sanitize_kernel(item)
                        display_name = str(sanitized.get("name") or sanitized.get("symbol") or "")
                        if KERNEL_RE.search(display_name):
                            kernels.append(sanitized)
                target = find_key(decoded, {"amdhsa.target", "target"})
                if target is not None and str(target) not in targets:
                    targets.append(str(target))
            decoded_notes.append(note_record)

    # De-duplicate metadata repeated in multiple note sections.
    unique: dict[tuple[str, str], dict[str, Any]] = {}
    for kernel in kernels:
        key = (str(kernel.get("name", "")), str(kernel.get("symbol", "")))
        unique[key] = kernel

    return {
        "absolute_offset": absolute_offset,
        "intrinsic_size": size,
        "intrinsic_sha256": sha256(blob[:size]),
        "elf_class": int(elf.elfclass),
        "little_endian": bool(elf.little_endian),
        "machine": str(elf.header["e_machine"]),
        "flags": int(elf.header["e_flags"]),
        "metadata_versions": metadata_versions,
        "targets": targets,
        "notes": decoded_notes,
        "kernels": list(unique.values()),
    }


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Sanitized AMDGPU kernel ABI",
        "",
        "> Derived by static MessagePack decoding of embedded AMDGPU notes. No code bytes or weights are included.",
        "",
        f"- Installer SHA-256: `{report['installer_sha256']}`",
        f"- AMDGPU code objects: `{len(report['code_objects'])}`",
        "",
    ]
    for index, obj in enumerate(report["code_objects"]):
        lines.extend(
            [
                f"## Code object {index}",
                "",
                f"- File offset: `0x{obj['absolute_offset']:x}`",
                f"- Intrinsic size: `{obj['intrinsic_size']}`",
                f"- SHA-256: `{obj['intrinsic_sha256']}`",
                f"- Targets: `{', '.join(obj['targets']) or 'not exposed in decoded note'}`",
                f"- Metadata versions: `{json.dumps(obj['metadata_versions'], ensure_ascii=False)}`",
                f"- Relevant kernels: `{len(obj['kernels'])}`",
                "",
            ]
        )
        for kernel in obj["kernels"]:
            lines.append(f"### `{kernel.get('name') or kernel.get('symbol')}`")
            lines.append("")
            lines.append(f"- Symbol: `{kernel.get('symbol')}`")
            lines.append(f"- Kernarg bytes/alignment: `{kernel.get('kernarg_segment_size')}` / `{kernel.get('kernarg_segment_align')}`")
            lines.append(f"- LDS/private bytes: `{kernel.get('group_segment_fixed_size')}` / `{kernel.get('private_segment_fixed_size')}`")
            lines.append(f"- SGPR/VGPR: `{kernel.get('sgpr_count')}` / `{kernel.get('vgpr_count')}`")
            lines.append(f"- Wave/workgroup: `{kernel.get('wavefront_size')}` / `{kernel.get('max_flat_workgroup_size')}`")
            args = kernel.get("args", [])
            if args:
                lines.extend(["", "| Offset | Size | Name | Type | Kind | Address space |", "|---:|---:|---|---|---|---|"])
                for arg in args:
                    lines.append(
                        "| {offset} | {size} | `{name}` | `{type}` | `{kind}` | `{space}` |".format(
                            offset=arg.get("offset"),
                            size=arg.get("size"),
                            name=arg.get("name"),
                            type=arg.get("type_name") or arg.get("value_type"),
                            kind=arg.get("value_kind"),
                            space=arg.get("address_space"),
                        )
                    )
            lines.append("")
    return "\n".join(lines)


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

    code_objects: list[dict[str, Any]] = []
    for offset in scan(data, b"\x7fELF"):
        analyzed = analyze_elf(data[offset:], offset)
        if analyzed is not None:
            code_objects.append(analyzed)

    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": 1,
        "analysis_mode": "static_only_never_executed",
        "installer_sha256": actual,
        "code_objects": code_objects,
    }
    (args.output / "amdgpu-abi.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.output / "amdgpu-abi.md").write_text(markdown(report), encoding="utf-8")

    forbidden = {".exe", ".dll", ".bin", ".so", ".cubin", ".hsaco", ".elf"}
    leaked = [str(p) for p in args.output.rglob("*") if p.is_file() and p.suffix.lower() in forbidden]
    if leaked:
        raise SystemExit("binary payload leaked into output: " + ", ".join(leaked))

    print(json.dumps({"status": "ok", "code_objects": len(code_objects), "kernels": sum(len(x['kernels']) for x in code_objects)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
