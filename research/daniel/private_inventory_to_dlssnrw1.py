#!/usr/bin/env python3
"""Convert a private tensor inventory into a validated ``DLSSNRW1`` container.

The converter is intentionally schema-tolerant because reconstruction packages
use different JSON/CSV field names. It preserves list/row order unless every
record provides an explicit ordinal. Tensor bytes may be individual files or
slices of a larger container. No private data is transmitted anywhere.
"""
from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Sequence

from dlssnrw1 import TensorSource, write_container

NAME_KEYS = ("name", "tensor_name", "tensor", "key")
PATH_KEYS = ("path", "file", "file_path", "filename", "source_path", "blob_path", "container_path")
OFFSET_KEYS = ("offset", "byte_offset", "start", "file_offset")
SIZE_KEYS = ("size", "nbytes", "byte_size", "length", "num_bytes")
ORDER_KEYS = ("ordinal", "index", "order", "tensor_index")
HASH_KEYS = ("sha256", "hash", "digest")
LIST_KEYS = ("tensors", "entries", "records", "items", "blobs", "weights")


@dataclasses.dataclass(frozen=True, slots=True)
class InventoryTensor:
    name: str
    source: Path
    offset: int
    size: int
    ordinal: int | None
    expected_sha256: str | None


@dataclasses.dataclass(frozen=True, slots=True)
class InventoryCandidate:
    path: Path
    tensors: tuple[InventoryTensor, ...]
    explicit_order: bool
    score: int


def _first(mapping: dict[str, Any], keys: Iterable[str]) -> Any:
    lowered = {str(key).lower(): value for key, value in mapping.items()}
    for key in keys:
        value = lowered.get(key)
        if value not in (None, ""):
            return value
    return None


def _integer(value: Any, field: str, *, default: int | None = None) -> int:
    if value in (None, "") and default is not None:
        return default
    if isinstance(value, bool):
        raise ValueError(f"{field} must be an integer")
    try:
        result = int(str(value), 0) if isinstance(value, str) else int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid {field}: {value!r}") from exc
    if result < 0:
        raise ValueError(f"{field} must be non-negative")
    return result


def _resolve_source(value: Any, inventory: Path, root: Path) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing source path")
    raw = Path(value)
    candidates = [raw] if raw.is_absolute() else [inventory.parent / raw, root / raw]
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.is_file():
            return resolved
    raise FileNotFoundError(f"tensor source not found: {value}")


def _extract_rows(document: Any) -> list[dict[str, Any]]:
    if isinstance(document, list):
        rows = document
    elif isinstance(document, dict):
        rows = None
        for key in LIST_KEYS:
            value = document.get(key)
            if isinstance(value, list):
                rows = value
                break
        if rows is None:
            # Also accept a mapping from tensor name to metadata/path.
            converted: list[dict[str, Any]] = []
            for key, value in document.items():
                if isinstance(value, dict):
                    converted.append({"name": key, **value})
                elif isinstance(value, str):
                    converted.append({"name": key, "path": value})
            rows = converted
    else:
        raise ValueError("inventory document must be a list or object")
    return [row for row in rows if isinstance(row, dict)]


def _read_rows(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".json":
        return _extract_rows(json.loads(path.read_text(encoding="utf-8")))
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            return [dict(row) for row in csv.DictReader(stream)]
    raise ValueError(f"unsupported inventory extension: {path.suffix}")


def parse_inventory(path: Path, root: Path, expected_count: int) -> InventoryCandidate:
    rows = _read_rows(path)
    tensors: list[InventoryTensor] = []
    seen: set[str] = set()
    explicit_ordinals = True
    for row_number, row in enumerate(rows, 1):
        name_value = _first(row, NAME_KEYS)
        source_value = _first(row, PATH_KEYS)
        if name_value in (None, "") or source_value in (None, ""):
            continue
        name = str(name_value)
        if name in seen:
            raise ValueError(f"duplicate name {name!r} in {path}")
        seen.add(name)
        source = _resolve_source(source_value, path, root)
        offset = _integer(_first(row, OFFSET_KEYS), "offset", default=0)
        listed_size = _first(row, SIZE_KEYS)
        available = source.stat().st_size - offset
        if available < 0:
            raise ValueError(f"offset exceeds source size for {name!r}")
        size = _integer(listed_size, "size", default=available)
        if size > available:
            raise ValueError(f"slice exceeds source size for {name!r}")
        ordinal_value = _first(row, ORDER_KEYS)
        ordinal = None if ordinal_value in (None, "") else _integer(ordinal_value, "ordinal")
        explicit_ordinals = explicit_ordinals and ordinal is not None
        digest = _first(row, HASH_KEYS)
        expected_digest = str(digest).lower().removeprefix("sha256:") if digest not in (None, "") else None
        if expected_digest is not None and (len(expected_digest) != 64 or any(c not in "0123456789abcdef" for c in expected_digest)):
            expected_digest = None  # Ignore non-SHA256 generic hash fields.
        tensors.append(InventoryTensor(name, source, offset, size, ordinal, expected_digest))

    if explicit_ordinals and tensors:
        ordinals = [tensor.ordinal for tensor in tensors]
        if len(set(ordinals)) != len(ordinals):
            raise ValueError(f"duplicate ordinals in {path}")
        tensors.sort(key=lambda tensor: int(tensor.ordinal))

    resolvable = len(tensors)
    score = resolvable * 10
    if resolvable == expected_count:
        score += 100_000
    if explicit_ordinals and tensors:
        score += 1_000
    if "tensor" in path.name.lower() or "inventory" in path.name.lower():
        score += 100
    return InventoryCandidate(path, tuple(tensors), explicit_ordinals and bool(tensors), score)


def discover_inventory(root: Path, expected_count: int) -> InventoryCandidate:
    candidates: list[InventoryCandidate] = []
    for path in sorted((*root.rglob("*.json"), *root.rglob("*.csv"))):
        try:
            candidate = parse_inventory(path, root, expected_count)
        except (OSError, ValueError, json.JSONDecodeError, UnicodeError):
            continue
        if candidate.tensors:
            candidates.append(candidate)
    if not candidates:
        raise ValueError("no usable JSON/CSV tensor inventory was found")
    candidates.sort(key=lambda candidate: (candidate.score, str(candidate.path)), reverse=True)
    best = candidates[0]
    tied = [candidate for candidate in candidates if candidate.score == best.score]
    if len(tied) > 1:
        names = "\n".join(f"  - {item.path}" for item in tied)
        raise ValueError(f"multiple equally plausible inventories; pass --inventory explicitly:\n{names}")
    return best


def _hash_slice(tensor: InventoryTensor) -> str:
    digest = hashlib.sha256()
    remaining = tensor.size
    with tensor.source.open("rb") as stream:
        stream.seek(tensor.offset)
        while remaining:
            chunk = stream.read(min(remaining, 8 * 1024 * 1024))
            if not chunk:
                raise EOFError(f"truncated source while reading {tensor.name!r}")
            digest.update(chunk)
            remaining -= len(chunk)
    return digest.hexdigest()


def _stage_sources(tensors: Sequence[InventoryTensor], staging: Path) -> list[TensorSource]:
    sources: list[TensorSource] = []
    for ordinal, tensor in enumerate(tensors):
        actual_digest = _hash_slice(tensor)
        if tensor.expected_sha256 and actual_digest != tensor.expected_sha256:
            raise ValueError(
                f"SHA-256 mismatch for {tensor.name!r}: expected {tensor.expected_sha256}, got {actual_digest}"
            )
        if tensor.offset == 0 and tensor.size == tensor.source.stat().st_size:
            path = tensor.source
        else:
            path = staging / f"{ordinal:03d}.bin"
            remaining = tensor.size
            with tensor.source.open("rb") as source, path.open("wb") as output:
                source.seek(tensor.offset)
                while remaining:
                    chunk = source.read(min(remaining, 8 * 1024 * 1024))
                    if not chunk:
                        raise EOFError(f"truncated source while staging {tensor.name!r}")
                    output.write(chunk)
                    remaining -= len(chunk)
        sources.append(TensorSource(tensor.name, path))
    return sources


def convert(
    root: Path,
    output: Path,
    *,
    inventory_path: Path | None,
    expected_count: int,
    basis: str,
    dry_run: bool,
) -> dict[str, Any]:
    root = root.resolve()
    inventory = (
        parse_inventory(inventory_path.resolve(), root, expected_count)
        if inventory_path is not None
        else discover_inventory(root, expected_count)
    )
    if len(inventory.tensors) != expected_count:
        raise ValueError(
            f"inventory {inventory.path} resolved {len(inventory.tensors)} tensors; expected {expected_count}"
        )
    total_bytes = sum(tensor.size for tensor in inventory.tensors)
    summary: dict[str, Any] = {
        "inventory": str(inventory.path),
        "count": len(inventory.tensors),
        "total_tensor_bytes": total_bytes,
        "explicit_order": inventory.explicit_order,
        "output": str(output),
        "dry_run": dry_run,
    }
    if dry_run:
        return summary

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dlssnrw1-stage-", dir=output.parent) as temporary:
        sources = _stage_sources(inventory.tensors, Path(temporary))
        index = write_container(
            sources,
            output,
            offset_basis=basis,  # type: ignore[arg-type]
            expected_count=expected_count,
        )
    digest = hashlib.sha256()
    with output.open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    summary.update(
        {
            "data_offset": index.data_offset,
            "file_size": index.file_size,
            "offset_basis": index.offset_basis,
            "sha256": digest.hexdigest(),
            "verified": True,
        }
    )
    return summary


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--expected-count", type=int, default=153)
    parser.add_argument("--basis", choices=("relative", "absolute"), default="relative")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = convert(
            args.private_root,
            args.output,
            inventory_path=args.inventory,
            expected_count=args.expected_count,
            basis=args.basis,
            dry_run=args.dry_run,
        )
    except (OSError, ValueError, EOFError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
