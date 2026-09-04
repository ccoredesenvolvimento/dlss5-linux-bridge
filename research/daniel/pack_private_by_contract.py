#!/usr/bin/env python3
"""Build ``dlssnr_on_amd_weights.bin`` from extracted private tensor files.

The tool uses the statically recovered 153-entry Daniel contract as the source
of truth. It locates each tensor by exact logical name/basename, requires the
exact byte size, resolves byte-identical duplicates deterministically, and
refuses ambiguous or incomplete inputs. No inference capture is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from dlssnrw1 import TensorSource, read_index, write_container

SKIP_SUFFIXES = {
    ".zip", ".7z", ".rar", ".tar", ".gz", ".xz", ".bz2",
    ".json", ".csv", ".md", ".txt", ".log", ".py", ".pyc",
    ".exe", ".dll", ".so", ".cubin", ".hsaco", ".onnx", ".png", ".jpg", ".jpeg",
}


class MappingError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class ContractTensor:
    ordinal: int
    name: str
    byte_size: int


@dataclass(frozen=True, slots=True)
class Resolution:
    tensor: ContractTensor
    path: Path
    duplicate_count: int
    sha256: str | None = None


def load_contract(path: Path) -> tuple[ContractTensor, ...]:
    document = json.loads(path.read_text(encoding="utf-8"))
    rows = document.get("tensors") if isinstance(document, dict) else None
    if not isinstance(rows, list):
        raise MappingError("contract must contain a 'tensors' list")
    tensors: list[ContractTensor] = []
    names: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise MappingError(f"contract entry {index} is not an object")
        try:
            ordinal = int(row["ordinal"])
            name = str(row["name"])
            byte_size = int(row["byte_size"])
        except (KeyError, TypeError, ValueError) as exc:
            raise MappingError(f"contract entry {index} is incomplete") from exc
        if ordinal != index:
            raise MappingError(f"contract ordinal {ordinal} is out of sequence at row {index}")
        if not name or name in names:
            raise MappingError(f"empty or duplicate contract name: {name!r}")
        if byte_size <= 0:
            raise MappingError(f"invalid byte size for {name!r}: {byte_size}")
        names.add(name)
        tensors.append(ContractTensor(ordinal, name, byte_size))
    declared_count = document.get("count") if isinstance(document, dict) else None
    if declared_count is not None and int(declared_count) != len(tensors):
        raise MappingError("contract count does not match its tensor list")
    return tuple(tensors)


def name_keys(path: Path) -> set[str]:
    name = path.name
    keys = {name}
    lowered = name.lower()
    for suffix in (".bin", ".dat", ".raw", ".blob", ".weights"):
        if lowered.endswith(suffix):
            keys.add(name[: -len(suffix)])
    return keys


def discover_files(root: Path, excluded: Iterable[Path] = ()) -> dict[str, list[Path]]:
    excluded_resolved = {path.resolve() for path in excluded}
    index: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved in excluded_resolved or path.suffix.lower() in SKIP_SUFFIXES:
            continue
        for key in name_keys(path):
            index.setdefault(key, []).append(resolved)
    for paths in index.values():
        paths.sort(key=lambda path: (len(path.parts), str(path)))
    return index


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_tensor(tensor: ContractTensor, file_index: dict[str, list[Path]]) -> Resolution:
    candidates: list[Path] = []
    seen: set[Path] = set()
    for key in (tensor.name, tensor.name + ".bin", tensor.name + ".dat", tensor.name + ".raw"):
        for path in file_index.get(key, []):
            if path in seen:
                continue
            seen.add(path)
            try:
                if path.stat().st_size == tensor.byte_size:
                    candidates.append(path)
            except OSError:
                continue
    if not candidates:
        available = []
        for key in (tensor.name, tensor.name + ".bin", tensor.name + ".dat", tensor.name + ".raw"):
            for path in file_index.get(key, []):
                try:
                    available.append({"path": str(path), "size": path.stat().st_size})
                except OSError:
                    pass
        detail = f"; same-name candidates={available}" if available else ""
        raise MappingError(
            f"missing {tensor.name!r} with exact size {tensor.byte_size}{detail}"
        )
    if len(candidates) == 1:
        return Resolution(tensor, candidates[0], 1)

    digests = [(path, hash_file(path)) for path in candidates]
    unique = {digest for _, digest in digests}
    if len(unique) != 1:
        detail = ", ".join(f"{path}={digest}" for path, digest in digests)
        raise MappingError(f"ambiguous non-identical copies of {tensor.name!r}: {detail}")
    chosen = min((path for path, _ in digests), key=lambda path: (len(path.parts), str(path)))
    return Resolution(tensor, chosen, len(candidates), digests[0][1])


def map_contract(
    private_root: Path,
    contract_path: Path,
    *,
    output_path: Path | None = None,
) -> tuple[tuple[ContractTensor, ...], tuple[Resolution, ...], dict[str, Any]]:
    contract = load_contract(contract_path)
    exclusions = [contract_path]
    if output_path is not None:
        exclusions.append(output_path)
    file_index = discover_files(private_root, exclusions)
    resolutions: list[Resolution] = []
    failures: list[str] = []
    for tensor in contract:
        try:
            resolutions.append(resolve_tensor(tensor, file_index))
        except MappingError as exc:
            failures.append(str(exc))

    report: dict[str, Any] = {
        "contract": str(contract_path.resolve()),
        "private_root": str(private_root.resolve()),
        "required_count": len(contract),
        "resolved_count": len(resolutions),
        "missing_or_ambiguous_count": len(failures),
        "required_payload_bytes": sum(item.byte_size for item in contract),
        "resolved_payload_bytes": sum(item.tensor.byte_size for item in resolutions),
        "failures": failures,
        "resolved": [
            {
                "ordinal": item.tensor.ordinal,
                "name": item.tensor.name,
                "byte_size": item.tensor.byte_size,
                "path": str(item.path),
                "duplicate_count": item.duplicate_count,
                "sha256": item.sha256,
            }
            for item in resolutions
        ],
    }
    return contract, tuple(resolutions), report


def execute(
    private_root: Path,
    contract_path: Path,
    output_path: Path,
    *,
    dry_run: bool,
    report_path: Path | None,
    basis: str,
) -> dict[str, Any]:
    private_root = private_root.resolve()
    contract_path = contract_path.resolve()
    output_path = output_path.resolve()
    if not private_root.is_dir():
        raise MappingError(f"private root is not a directory: {private_root}")
    if not contract_path.is_file():
        raise MappingError(f"contract does not exist: {contract_path}")

    contract, resolutions, report = map_contract(
        private_root, contract_path, output_path=output_path
    )
    report.update({"output": str(output_path), "dry_run": dry_run, "offset_basis": basis})
    if report["missing_or_ambiguous_count"]:
        if report_path is not None:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        raise MappingError(
            f"resolved {len(resolutions)}/{len(contract)} tensors; inspect failures in "
            f"{report_path or 'stderr/report'}"
        )
    if dry_run:
        report["verified"] = True
    else:
        sources = [TensorSource(item.tensor.name, item.path) for item in resolutions]
        index = write_container(
            sources,
            output_path,
            offset_basis=basis,  # type: ignore[arg-type]
            expected_count=len(contract),
        )
        parsed = read_index(output_path)
        expected_pairs = [(item.name, item.byte_size) for item in contract]
        actual_pairs = [(item.name, item.size) for item in parsed.entries]
        if actual_pairs != expected_pairs:
            try:
                output_path.unlink()
            except OSError:
                pass
            raise MappingError("post-write container contract mismatch")
        report.update(
            {
                "verified": True,
                "container_count": parsed.count,
                "container_data_offset": parsed.data_offset,
                "container_file_size": parsed.file_size,
                "container_sha256": hash_file(output_path),
            }
        )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path(__file__).with_name("results") / "tensor-contract.json",
    )
    parser.add_argument("--report", type=Path)
    parser.add_argument("--basis", choices=("relative", "absolute"), default="relative")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = execute(
            args.private_root,
            args.contract,
            args.output,
            dry_run=args.dry_run,
            report_path=args.report,
            basis=args.basis,
        )
    except (OSError, MappingError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    compact = {key: value for key, value in report.items() if key != "resolved"}
    print(json.dumps(compact, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
