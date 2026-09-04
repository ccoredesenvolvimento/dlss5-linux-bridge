#!/usr/bin/env python3
"""Reduce static-analysis outputs to a compact implementation contract.

The full disassembly report is intentionally verbose. This tool keeps only
functions that cross-reference known DLSSNR contract strings and a bounded
instruction window around each reference, plus sanitized AMDGPU kernel ABIs.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ADDRESS_RE = re.compile(r"^0x([0-9a-fA-F]+):")
XREF_RE = re.compile(r"XREF -> (.+)$")
INTEREST = re.compile(
    r"DLSSNRW1|weights(?:\.bin|_index)|wrote %zu blobs|tensors? match|repackaged|"
    r"hipImportExternalMemory|hipExternalMemoryGetMappedBuffer|hipLaunchKernel|"
    r"DLSSNR_(?:STAGES|NO_REPACK|NOPOSTHIST|NOBLEND|SLOW_PREPOST|WBLOG)|"
    r"staging ready|k_(?:qkv|qkv_attn|expand2|contract2|conv_res2|repack|swin)",
    re.IGNORECASE,
)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def classify(values: list[str]) -> str:
    text = "\n".join(values)
    if re.search(r"DLSSNRW1|wrote %zu blobs|weights_index|weights\.bin", text, re.I):
        return "weight_container"
    if re.search(r"tensors? match|repackaged|checking its tensors", text, re.I):
        return "weight_recognition"
    if re.search(r"hipImportExternalMemory|hipExternalMemoryGetMappedBuffer", text, re.I):
        return "d3d12_hip_interop"
    if re.search(r"hipLaunchKernel|k_(?:qkv|expand|contract|swin|conv|repack)", text, re.I):
        return "hip_dispatch"
    if re.search(r"STAGES|NO_REPACK|NOPOSTHIST|NOBLEND|SLOW_PREPOST|WBLOG", text, re.I):
        return "runtime_debug_controls"
    if re.search(r"staging ready", text, re.I):
        return "frame_staging"
    return "other"


def xref_windows(function: dict[str, Any], radius: int) -> list[dict[str, Any]]:
    disassembly = function.get("disassembly", [])
    if not isinstance(disassembly, list):
        return []
    xref_indices = [index for index, line in enumerate(disassembly) if isinstance(line, str) and "XREF ->" in line]
    windows: list[dict[str, Any]] = []
    occupied: list[tuple[int, int]] = []
    for index in xref_indices:
        start = max(0, index - radius)
        end = min(len(disassembly), index + radius + 1)
        if occupied and start <= occupied[-1][1] + 2:
            old_start, old_end = occupied.pop()
            start, end = old_start, max(old_end, end)
            if windows:
                windows.pop()
        occupied.append((start, end))
        lines = [str(line) for line in disassembly[start:end]]
        markers: list[str] = []
        for line in lines:
            match = XREF_RE.search(line)
            if match:
                markers.extend(part.strip() for part in match.group(1).split(" | "))
        windows.append(
            {
                "start_instruction": start,
                "end_instruction": end,
                "markers": list(dict.fromkeys(markers)),
                "lines": lines,
            }
        )
    return windows


def compact_xrefs(report: dict[str, Any], radius: int) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for pe_index, image in enumerate(report.get("pe_images", [])):
        for function in image.get("function_reports", []):
            values: list[str] = []
            for xref in function.get("xrefs", []):
                for target in xref.get("targets", []):
                    value = str(target.get("value", ""))
                    if value and value not in values:
                        values.append(value)
            selected = [value for value in values if INTEREST.search(value)]
            if not selected:
                continue
            compact.append(
                {
                    "pe_index": pe_index,
                    "pe_offset": image.get("absolute_offset"),
                    "pe_kind": image.get("kind"),
                    "function_begin_rva": function.get("begin_rva"),
                    "function_end_rva": function.get("end_rva"),
                    "function_size": function.get("size"),
                    "category": classify(selected),
                    "targets": selected,
                    "windows": xref_windows(function, radius),
                }
            )
    return compact


def compact_abi(report: dict[str, Any]) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for index, obj in enumerate(report.get("code_objects", [])):
        kernels = []
        for kernel in obj.get("kernels", []):
            kernels.append(
                {
                    "name": kernel.get("name"),
                    "symbol": kernel.get("symbol"),
                    "kernarg_segment_size": kernel.get("kernarg_segment_size"),
                    "kernarg_segment_align": kernel.get("kernarg_segment_align"),
                    "group_segment_fixed_size": kernel.get("group_segment_fixed_size"),
                    "private_segment_fixed_size": kernel.get("private_segment_fixed_size"),
                    "sgpr_count": kernel.get("sgpr_count"),
                    "vgpr_count": kernel.get("vgpr_count"),
                    "max_flat_workgroup_size": kernel.get("max_flat_workgroup_size"),
                    "wavefront_size": kernel.get("wavefront_size"),
                    "args": kernel.get("args", []),
                }
            )
        objects.append(
            {
                "index": index,
                "offset": obj.get("absolute_offset"),
                "size": obj.get("intrinsic_size"),
                "sha256": obj.get("intrinsic_sha256"),
                "targets": obj.get("targets", []),
                "metadata_versions": obj.get("metadata_versions", []),
                "kernels": kernels,
            }
        )
    return objects


def make_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# DLSSNR Daniel-route implementation contract",
        "",
        "> Compact, metadata-only output from static analysis. No installer, DLL, code object or model weight is included.",
        "",
        "## Proven architecture",
        "",
        f"- Installer SHA-256 validated: `{result['installer_sha256']}`",
        f"- Embedded PE images: `{result['pe_image_count']}`",
        f"- Embedded AMDGPU code objects: `{len(result['amdgpu_code_objects'])}`",
        f"- Contract-bearing x64 functions: `{len(result['contract_functions'])}`",
        f"- Relevant AMDGPU kernel records: `{sum(len(x['kernels']) for x in result['amdgpu_code_objects'])}`",
        "- Primary runtime path: converted weight container + custom HIP kernels + D3D12/HIP interop.",
        "- ONNX/DirectML is not evidenced as the in-game backend and remains a secondary export target.",
        "",
        "## Contract functions",
        "",
    ]
    for function in result["contract_functions"]:
        lines.extend(
            [
                f"### `{function['category']}` — PE {function['pe_index']} RVA `0x{int(function['function_begin_rva']):x}`–`0x{int(function['function_end_rva']):x}`",
                "",
            ]
        )
        for target in function["targets"]:
            lines.append(f"- References: `{target}`")
        for window in function["windows"]:
            lines.extend(["", "```asm", *window["lines"], "```"])
        lines.append("")

    lines.extend(["## AMDGPU kernel ABI", ""])
    for obj in result["amdgpu_code_objects"]:
        lines.extend(
            [
                f"### Code object {obj['index']} at `0x{int(obj['offset']):x}`",
                "",
                f"- Size/hash: `{obj['size']}` / `{obj['sha256']}`",
                f"- Target metadata: `{json.dumps(obj['targets'], ensure_ascii=False)}`",
                f"- Relevant kernels: `{len(obj['kernels'])}`",
                "",
            ]
        )
        for kernel in obj["kernels"]:
            name = kernel.get("name") or kernel.get("symbol")
            lines.append(f"#### `{name}`")
            lines.append("")
            lines.append(
                f"- Kernarg `{kernel.get('kernarg_segment_size')}` bytes; LDS `{kernel.get('group_segment_fixed_size')}`; "
                f"SGPR/VGPR `{kernel.get('sgpr_count')}/{kernel.get('vgpr_count')}`; wave `{kernel.get('wavefront_size')}`."
            )
            args = kernel.get("args") or []
            if args:
                lines.extend(["", "| Offset | Size | Name | Type | Kind |", "|---:|---:|---|---|---|"])
                for arg in args:
                    lines.append(
                        f"| {arg.get('offset')} | {arg.get('size')} | `{arg.get('name')}` | "
                        f"`{arg.get('type_name') or arg.get('value_type')}` | `{arg.get('value_kind')}` |"
                    )
            lines.append("")

    lines.extend(
        [
            "## Success gates",
            "",
            "1. Decode and round-trip the `DLSSNRW1` header/index without using captured activations.",
            "2. Map independent private tensors into the same logical blob order and verify hashes/shapes locally.",
            "3. Reproduce fixed-contract `expand2 -> activation/FP8 -> contract2` and QKV/Swin blocks numerically.",
            "4. Complete pre/repack, convolutional encoder/decoder, history/blend and post stages.",
            "5. Validate one full frame through the reference graph, then the HIP backend.",
            "6. Export ONNX only from the already validated reference graph and require end-to-end PNG equivalence.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--radius", type=int, default=24)
    args = parser.parse_args()

    xrefs = read_json(args.input / "pe-xrefs.json")
    abi = read_json(args.input / "amdgpu-abi.json")
    payloads = read_json(args.input / "payload-map.json")
    report = read_json(args.input / "report.json")

    digests = {
        str(xrefs.get("installer_sha256")),
        str(abi.get("installer_sha256")),
        str(payloads.get("installer_sha256")),
        str(report.get("installer", {}).get("sha256")),
    }
    if len(digests) != 1:
        raise SystemExit(f"analysis inputs refer to different installers: {sorted(digests)}")

    result = {
        "schema_version": 1,
        "analysis_mode": "static_only_never_executed",
        "installer_sha256": next(iter(digests)),
        "pe_image_count": len(xrefs.get("pe_images", [])),
        "contract_functions": compact_xrefs(xrefs, max(4, min(args.radius, 80))),
        "amdgpu_code_objects": compact_abi(abi),
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "contract-summary.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    (args.output / "contract-summary.md").write_text(make_markdown(result), encoding="utf-8")
    print(json.dumps({
        "status": "ok",
        "functions": len(result["contract_functions"]),
        "code_objects": len(result["amdgpu_code_objects"]),
        "kernels": sum(len(x["kernels"]) for x in result["amdgpu_code_objects"]),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
