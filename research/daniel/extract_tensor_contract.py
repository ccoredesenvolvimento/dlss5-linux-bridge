#!/usr/bin/env python3
"""Recover the public installer's 153-entry DLSSNR tensor contract.

The v0.2.9 setup binary contains a static table used to validate extracted
weights. Each 16-byte record is ``{const char* name, uint64_t byte_size}``.
This tool verifies the release SHA-256, parses that table as PE metadata and
writes names/sizes only. It never executes the installer and never emits model
bytes or executable payloads.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import urllib.request
from pathlib import Path
from typing import Any, Sequence

import pefile  # type: ignore

DEFAULT_TABLE_RVA = 0x26860
DEFAULT_COUNT = 153
MAX_NAME_BYTES = 255


class ContractError(ValueError):
    pass


def download(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ccore-dlssnr-static-research/1.0",
            "Accept": "application/octet-stream",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_integer(value: str) -> int:
    return int(value, 0)


def rva_to_offset(pe: pefile.PE, rva: int, image_size: int) -> int:
    if rva < int(pe.OPTIONAL_HEADER.SizeOfHeaders):
        if rva >= image_size:
            raise ContractError(f"RVA 0x{rva:x} lies outside the image")
        return rva
    for section in pe.sections:
        start = int(section.VirtualAddress)
        raw_size = int(section.SizeOfRawData)
        virtual_size = int(section.Misc_VirtualSize)
        span = max(raw_size, virtual_size)
        if start <= rva < start + span:
            delta = rva - start
            if delta >= raw_size:
                raise ContractError(f"RVA 0x{rva:x} is in a zero-filled section tail")
            offset = int(section.PointerToRawData) + delta
            if offset >= image_size:
                raise ContractError(f"RVA 0x{rva:x} maps outside the file")
            return offset
    raise ContractError(f"RVA 0x{rva:x} is not mapped by any PE section")


def read_c_string(image: bytes, offset: int) -> str:
    if offset < 0 or offset >= len(image):
        raise ContractError(f"string offset 0x{offset:x} is outside the image")
    end = image.find(b"\0", offset, min(len(image), offset + MAX_NAME_BYTES + 1))
    if end < 0:
        raise ContractError(f"unterminated tensor name at file offset 0x{offset:x}")
    raw = image[offset:end]
    if not raw:
        raise ContractError(f"empty tensor name at file offset 0x{offset:x}")
    try:
        name = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContractError(f"tensor name at 0x{offset:x} is not UTF-8") from exc
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in name):
        raise ContractError(f"tensor name contains a control character: {name!r}")
    return name


def extract_contract(image: bytes, table_rva: int, count: int) -> dict[str, Any]:
    try:
        pe = pefile.PE(data=image, fast_load=False)
    except Exception as exc:
        raise ContractError(f"installer is not a parseable PE image: {exc}") from exc
    try:
        if int(pe.FILE_HEADER.Machine) != 0x8664:
            raise ContractError(f"expected x86-64 PE, machine=0x{int(pe.FILE_HEADER.Machine):x}")
        image_base = int(pe.OPTIONAL_HEADER.ImageBase)
        table_offset = rva_to_offset(pe, table_rva, len(image))
        table_size = count * 16
        if table_offset + table_size > len(image):
            raise ContractError("tensor contract table is truncated")

        tensors: list[dict[str, Any]] = []
        seen: set[str] = set()
        relative_payload_offset = 0
        index_size = 0
        for ordinal in range(count):
            record_offset = table_offset + ordinal * 16
            name_va, byte_size = struct.unpack_from("<QQ", image, record_offset)
            if name_va < image_base:
                raise ContractError(
                    f"record {ordinal}: name VA 0x{name_va:x} precedes image base 0x{image_base:x}"
                )
            name_rva = name_va - image_base
            name_offset = rva_to_offset(pe, name_rva, len(image))
            name = read_c_string(image, name_offset)
            if name in seen:
                raise ContractError(f"record {ordinal}: duplicate tensor name {name!r}")
            seen.add(name)
            if byte_size == 0:
                raise ContractError(f"record {ordinal}: tensor {name!r} has zero byte size")
            if byte_size > (1 << 40):
                raise ContractError(
                    f"record {ordinal}: implausible tensor size {byte_size} for {name!r}"
                )
            encoded_name = name.encode("utf-8")
            if len(encoded_name) > 255:
                raise ContractError(f"record {ordinal}: name exceeds DLSSNRW1 u8 length")
            tensors.append(
                {
                    "ordinal": ordinal,
                    "name": name,
                    "byte_size": byte_size,
                    "relative_payload_offset": relative_payload_offset,
                    "table_record_rva": table_rva + ordinal * 16,
                    "name_rva": name_rva,
                }
            )
            relative_payload_offset += byte_size
            index_size += 1 + len(encoded_name) + 16

        data_offset = 16 + index_size
        return {
            "schema_version": 1,
            "source_kind": "static_public_installer_contract",
            "table_layout": "char_pointer_u64_size",
            "table_rva": table_rva,
            "count": count,
            "image_base": image_base,
            "dlssnrw1": {
                "magic": "DLSSNRW1",
                "header_size": 16,
                "index_record": "u8_name_length + utf8_name + u64_offset + u64_size",
                "index_size": index_size,
                "data_offset": data_offset,
                "payload_size": relative_payload_offset,
                "predicted_file_size": data_offset + relative_payload_offset,
            },
            "tensors": tensors,
        }
    finally:
        pe.close()


def markdown(contract: dict[str, Any]) -> str:
    layout = contract["dlssnrw1"]
    lines = [
        "# DLSSNR v0.2.9 tensor contract",
        "",
        "> Static names/sizes only. No executable code or model bytes are included.",
        "",
        f"- Installer SHA-256: `{contract['installer_sha256']}`",
        f"- Contract table RVA: `0x{contract['table_rva']:x}`",
        f"- Tensor count: `{contract['count']}`",
        f"- Aggregate tensor bytes: `{layout['payload_size']}`",
        f"- Predicted `DLSSNRW1` data offset: `{layout['data_offset']}`",
        f"- Predicted complete container size: `{layout['predicted_file_size']}`",
        "",
        "| # | Tensor name | Bytes | Relative payload offset |",
        "|---:|---|---:|---:|",
    ]
    for tensor in contract["tensors"]:
        escaped = str(tensor["name"]).replace("|", "\\|")
        lines.append(
            f"| {tensor['ordinal']} | `{escaped}` | {tensor['byte_size']} | "
            f"{tensor['relative_payload_offset']} |"
        )
    lines.extend(
        [
            "",
            "## Validation rule",
            "",
            "A candidate private inventory is compatible only when it contains exactly the same 153 names in this order and every tensor has the declared byte size. Matching the count alone is insufficient.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--table-rva", type=parse_integer, default=DEFAULT_TABLE_RVA)
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    try:
        image = download(args.url)
        actual_digest = sha256(image)
        expected_digest = args.expected_sha256.lower().strip()
        if actual_digest != expected_digest:
            raise ContractError(
                f"SHA-256 mismatch: expected {expected_digest}, got {actual_digest}"
            )
        contract = extract_contract(image, args.table_rva, args.count)
        contract["installer_sha256"] = actual_digest
        args.output.mkdir(parents=True, exist_ok=True)
        (args.output / "tensor-contract.json").write_text(
            json.dumps(contract, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (args.output / "tensor-contract.md").write_text(markdown(contract), encoding="utf-8")
        print(
            json.dumps(
                {
                    "status": "ok",
                    "count": contract["count"],
                    "payload_size": contract["dlssnrw1"]["payload_size"],
                    "data_offset": contract["dlssnrw1"]["data_offset"],
                },
                indent=2,
            )
        )
        return 0
    except (OSError, ContractError, ValueError, struct.error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
