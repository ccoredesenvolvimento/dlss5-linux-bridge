#!/usr/bin/env python3
"""Locate PE code references to the DLSSNR weight/runtime contract strings.

The analyzer uses the x64 exception table as a function-boundary oracle and
Capstone for RIP-relative reference recovery. It emits disassembly text only;
no executable payload is retained.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import struct
import tempfile
import urllib.request
from pathlib import Path
from typing import Any, Iterable

import capstone  # type: ignore
import pefile  # type: ignore
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP  # type: ignore


TARGET_RE = re.compile(
    rb"(?:"
    rb"DLSSNRW1|"
    rb"dlssnr_on_amd_weights\.bin|dlssnr_weights_index\.txt|"
    rb"wrote %zu blobs|cannot write dlssnr_on_amd_weights\.bin|"
    rb"all %zu tensors match|%zu of %zu tensors do not match|"
    rb"checking its tensors instead|different build, not a repackaged|"
    rb"weights build from nvngx_dlssnr\.dll|"
    rb"staging ready: colour|"
    rb"hipImportExternalMemory|hipExternalMemoryGetMappedBuffer|hipLaunchKernel|"
    rb"DLSSNR_(?:STAGES|NO_REPACK|NOPOSTHIST|NOBLEND|SLOW_PREPOST|WBLOG)|"
    rb"_Z(?:9k_expand2|11k_contract2|5k_qkv|10k_qkv_attn|11k_conv_res2|8k_repack|10k_swin_var)"
    rb")[\x20-\x7e]{0,220}"
)


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "ccore-dlssnr-static-research/1.0"})
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scan(data: bytes, needle: bytes) -> Iterable[int]:
    pos = 0
    while True:
        pos = data.find(needle, pos)
        if pos < 0:
            return
        yield pos
        pos += 1


def valid_pe(data: bytes, offset: int) -> tuple[pefile.PE, int] | None:
    suffix = data[offset:]
    if len(suffix) < 0x100 or suffix[:2] != b"MZ":
        return None
    try:
        e_lfanew = struct.unpack_from("<I", suffix, 0x3C)[0]
    except struct.error:
        return None
    if e_lfanew < 0x40 or e_lfanew > 0x1000 or suffix[e_lfanew:e_lfanew + 4] != b"PE\0\0":
        return None
    try:
        pe = pefile.PE(data=suffix, fast_load=False)
    except Exception:
        return None
    if int(pe.FILE_HEADER.Machine) != 0x8664 or not (1 <= int(pe.FILE_HEADER.NumberOfSections) <= 96):
        pe.close()
        return None
    end = int(pe.OPTIONAL_HEADER.SizeOfHeaders)
    for section in pe.sections:
        raw_offset = int(section.PointerToRawData)
        raw_size = int(section.SizeOfRawData)
        if raw_offset + raw_size > len(suffix):
            pe.close()
            return None
        end = max(end, raw_offset + raw_size)
    return pe, end


def offset_to_rva(pe: pefile.PE, file_offset: int) -> int | None:
    if file_offset < int(pe.OPTIONAL_HEADER.SizeOfHeaders):
        return file_offset
    for section in pe.sections:
        start = int(section.PointerToRawData)
        end = start + int(section.SizeOfRawData)
        if start <= file_offset < end:
            return int(section.VirtualAddress) + (file_offset - start)
    return None


def rva_to_file_offset(pe: pefile.PE, rva: int) -> int | None:
    if rva < int(pe.OPTIONAL_HEADER.SizeOfHeaders):
        return rva
    for section in pe.sections:
        start = int(section.VirtualAddress)
        span = max(int(section.Misc_VirtualSize), int(section.SizeOfRawData))
        if start <= rva < start + span:
            delta = rva - start
            if delta >= int(section.SizeOfRawData):
                return None
            return int(section.PointerToRawData) + delta
    return None


def find_targets(image: bytes, pe: pefile.PE) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    seen: set[tuple[int, str]] = set()
    for match in TARGET_RE.finditer(image):
        value = match.group().decode("ascii", "replace").strip()
        rva = offset_to_rva(pe, match.start())
        if rva is None:
            continue
        key = (rva, value)
        if key in seen:
            continue
        seen.add(key)
        targets.append({"file_offset": match.start(), "rva": rva, "value": value})

    # Important names also occur as UTF-16 in installer UI/error paths.
    for text in (
        "dlssnr_on_amd_weights.bin",
        "dlssnr_weights_index.txt",
        "nvngx_dlssnr.dll",
        "version.dll",
    ):
        needle = text.encode("utf-16le")
        for pos in scan(image, needle):
            rva = offset_to_rva(pe, pos)
            if rva is None:
                continue
            key = (rva, text)
            if key in seen:
                continue
            seen.add(key)
            targets.append({"file_offset": pos, "rva": rva, "value": text, "encoding": "utf16le"})
    return sorted(targets, key=lambda x: x["rva"])


def function_ranges(pe: pefile.PE) -> list[tuple[int, int]]:
    ranges: set[tuple[int, int]] = set()
    for entry in getattr(pe, "DIRECTORY_ENTRY_EXCEPTION", []) or []:
        begin = int(entry.struct.BeginAddress)
        end = int(entry.struct.EndAddress)
        if 0 < begin < end:
            ranges.add((begin, end))
    return sorted(ranges)


def containing_function(ranges: list[tuple[int, int]], rva: int) -> tuple[int, int] | None:
    # The x64 runtime-function table is sorted; linear traversal is fine for a
    # small research binary and avoids another dependency.
    for begin, end in ranges:
        if begin <= rva < end:
            return (begin, end)
        if begin > rva:
            break
    return None


def disassemble_text(image: bytes, pe: pefile.PE) -> tuple[list[Any], dict[int, Any]]:
    text = next((s for s in pe.sections if s.Name.rstrip(b"\0") == b".text"), None)
    if text is None:
        return [], {}
    raw_offset = int(text.PointerToRawData)
    raw_size = int(text.SizeOfRawData)
    rva = int(text.VirtualAddress)
    code = image[raw_offset:raw_offset + raw_size]
    base = int(pe.OPTIONAL_HEADER.ImageBase) + rva
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    md.skipdata = True
    instructions = list(md.disasm(code, base))
    return instructions, {int(ins.address): ins for ins in instructions}


def instruction_targets(ins: Any) -> set[int]:
    result: set[int] = set()
    try:
        operands = ins.operands
    except capstone.CsError:
        return result
    for operand in operands:
        if operand.type == X86_OP_MEM and operand.mem.base == X86_REG_RIP:
            result.add(int(ins.address + ins.size + operand.mem.disp))
        elif operand.type == X86_OP_IMM:
            result.add(int(operand.imm) & 0xFFFFFFFFFFFFFFFF)
    return result


def format_instruction(ins: Any, markers: list[str] | None = None) -> str:
    raw = bytes(ins.bytes).hex()
    suffix = ""
    if markers:
        suffix = "    ; XREF -> " + " | ".join(markers)
    return f"0x{ins.address:016x}: {raw:<30} {ins.mnemonic:<10} {ins.op_str}{suffix}".rstrip()


def analyze_pe(data: bytes, absolute_offset: int, pe: pefile.PE, intrinsic_size: int) -> dict[str, Any]:
    image = data[absolute_offset:absolute_offset + intrinsic_size]
    targets = find_targets(image, pe)
    base = int(pe.OPTIONAL_HEADER.ImageBase)
    target_by_va: dict[int, list[dict[str, Any]]] = {}
    for target in targets:
        target_by_va.setdefault(base + int(target["rva"]), []).append(target)

    instructions, _ = disassemble_text(image, pe)
    ranges = function_ranges(pe)
    xrefs: list[dict[str, Any]] = []
    xrefs_by_function: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for ins in instructions:
        matched: list[dict[str, Any]] = []
        for address in instruction_targets(ins):
            matched.extend(target_by_va.get(address, []))
        if not matched:
            continue
        ins_rva = int(ins.address) - base
        fn = containing_function(ranges, ins_rva)
        record = {
            "instruction_va": int(ins.address),
            "instruction_rva": ins_rva,
            "mnemonic": ins.mnemonic,
            "operands": ins.op_str,
            "targets": matched,
            "function": {"begin_rva": fn[0], "end_rva": fn[1]} if fn else None,
        }
        xrefs.append(record)
        if fn:
            xrefs_by_function.setdefault(fn, []).append(record)

    function_reports: list[dict[str, Any]] = []
    for (begin, end), records in sorted(xrefs_by_function.items()):
        begin_va, end_va = base + begin, base + end
        relevant = [ins for ins in instructions if begin_va <= int(ins.address) < end_va]
        markers_by_va: dict[int, list[str]] = {}
        for record in records:
            markers_by_va.setdefault(record["instruction_va"], []).extend(t["value"] for t in record["targets"])
        function_reports.append(
            {
                "begin_rva": begin,
                "end_rva": end,
                "size": end - begin,
                "xrefs": records,
                "instruction_count": len(relevant),
                "disassembly": [format_instruction(ins, markers_by_va.get(int(ins.address))) for ins in relevant[:12_000]],
                "truncated": len(relevant) > 12_000,
            }
        )

    return {
        "absolute_offset": absolute_offset,
        "kind": "dll" if int(pe.FILE_HEADER.Characteristics) & 0x2000 else "exe",
        "image_base": base,
        "intrinsic_size": intrinsic_size,
        "sha256": sha256(image),
        "targets": targets,
        "xrefs": xrefs,
        "function_reports": function_reports,
        "function_range_count": len(ranges),
    }


def write_text(report: dict[str, Any], destination: Path) -> None:
    lines = [
        "# PE string cross-reference report",
        "",
        "> Static disassembly only. No executable payload is included.",
        "",
    ]
    for pe_index, item in enumerate(report["pe_images"]):
        lines.extend(
            [
                f"## PE {pe_index} at file offset `0x{item['absolute_offset']:x}`",
                "",
                f"- Kind: `{item['kind']}`",
                f"- Intrinsic SHA-256: `{item['sha256']}`",
                f"- Target strings: `{len(item['targets'])}`",
                f"- Recovered xrefs: `{len(item['xrefs'])}`",
                f"- Functions containing xrefs: `{len(item['function_reports'])}`",
                "",
            ]
        )
        for fn in item["function_reports"]:
            values = []
            for xref in fn["xrefs"]:
                for target in xref["targets"]:
                    if target["value"] not in values:
                        values.append(target["value"])
            lines.extend(
                [
                    f"### Function RVA `0x{fn['begin_rva']:x}`–`0x{fn['end_rva']:x}`",
                    "",
                    "References:",
                    "",
                ]
            )
            for value in values:
                lines.append(f"- `{value}`")
            lines.extend(["", "```asm", *fn["disassembly"], "```", ""])
    destination.write_text("\n".join(lines), encoding="utf-8")


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

    images: list[dict[str, Any]] = []
    for offset in scan(data, b"MZ"):
        parsed = valid_pe(data, offset)
        if parsed is None:
            continue
        pe, intrinsic_size = parsed
        try:
            images.append(analyze_pe(data, offset, pe, intrinsic_size))
        finally:
            pe.close()

    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": 1,
        "analysis_mode": "static_only_never_executed",
        "installer_sha256": actual,
        "pe_images": images,
    }
    (args.output / "pe-xrefs.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_text(report, args.output / "pe-xrefs.md")

    forbidden = {".exe", ".dll", ".bin", ".so", ".cubin", ".hsaco", ".elf"}
    leaked = [str(p) for p in args.output.rglob("*") if p.is_file() and p.suffix.lower() in forbidden]
    if leaked:
        raise SystemExit("binary payload leaked into output: " + ", ".join(leaked))

    print(json.dumps({"status": "ok", "pe_images": len(images), "xrefs": sum(len(x["xrefs"]) for x in images)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
