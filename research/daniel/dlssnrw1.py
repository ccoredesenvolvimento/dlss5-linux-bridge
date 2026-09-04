#!/usr/bin/env python3
"""Read, validate, unpack and create Daniel-compatible ``DLSSNRW1`` containers.

The file format was recovered independently from the public v0.2.9 installer:

    0x00  char[8]   magic = ``DLSSNRW1``
    0x08  uint32le  tensor/blob count
    0x0c  uint32le  data-section file offset
    0x10  repeated index records:
                     uint8 name_length
                     char[name_length] UTF-8 name
                     uint64le offset
                     uint64le byte_size
    data_offset      concatenated tensor bytes

Observed binaries can represent record offsets either relative to the data
section or as absolute file offsets. The reader detects both forms and the
writer supports both explicitly; ``relative`` is the canonical default.

This module contains no model data and never imports NVIDIA or Daniel binaries.
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import struct
import sys
import tempfile
from pathlib import Path
from typing import BinaryIO, Iterable, Iterator, Literal, Sequence

MAGIC = b"DLSSNRW1"
HEADER = struct.Struct("<8sII")
U64 = struct.Struct("<Q")
OffsetBasis = Literal["relative", "absolute"]


class FormatError(ValueError):
    """Raised when a container violates its structural contract."""


@dataclasses.dataclass(frozen=True, slots=True)
class TensorEntry:
    name: str
    stored_offset: int
    size: int
    file_offset: int

    @property
    def end_file_offset(self) -> int:
        return self.file_offset + self.size


@dataclasses.dataclass(frozen=True, slots=True)
class ContainerIndex:
    count: int
    data_offset: int
    file_size: int
    offset_basis: OffsetBasis
    entries: tuple[TensorEntry, ...]

    def by_name(self) -> dict[str, TensorEntry]:
        return {entry.name: entry for entry in self.entries}


@dataclasses.dataclass(frozen=True, slots=True)
class TensorSource:
    name: str
    path: Path


@dataclasses.dataclass(frozen=True, slots=True)
class _RawRecord:
    name: str
    offset: int
    size: int


def _read_exact(stream: BinaryIO, size: int, what: str) -> bytes:
    data = stream.read(size)
    if len(data) != size:
        raise FormatError(f"truncated {what}: expected {size} bytes, got {len(data)}")
    return data


def _validate_name(name: str) -> bytes:
    if not name:
        raise ValueError("tensor name must not be empty")
    encoded = name.encode("utf-8")
    if len(encoded) > 255:
        raise ValueError(f"tensor name exceeds 255 UTF-8 bytes: {name!r}")
    if "\x00" in name:
        raise ValueError(f"tensor name contains NUL: {name!r}")
    return encoded


def _parse_records(stream: BinaryIO, count: int, data_offset: int) -> tuple[_RawRecord, ...]:
    records: list[_RawRecord] = []
    seen: set[str] = set()
    for index in range(count):
        if stream.tell() >= data_offset:
            raise FormatError(f"index ended before record {index}/{count}")
        name_size = _read_exact(stream, 1, f"record {index} name length")[0]
        if name_size == 0:
            raise FormatError(f"record {index} has an empty name")
        name_bytes = _read_exact(stream, name_size, f"record {index} name")
        try:
            name = name_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise FormatError(f"record {index} name is not UTF-8") from exc
        if name in seen:
            raise FormatError(f"duplicate tensor name: {name!r}")
        seen.add(name)
        offset, size = struct.unpack("<QQ", _read_exact(stream, 16, f"record {index} offset/size"))
        records.append(_RawRecord(name=name, offset=offset, size=size))

    if stream.tell() != data_offset:
        raise FormatError(
            f"header data_offset={data_offset}, but {count} index records end at {stream.tell()}"
        )
    return tuple(records)


def _candidate_entries(
    records: Sequence[_RawRecord], data_offset: int, file_size: int, basis: OffsetBasis
) -> tuple[TensorEntry, ...] | None:
    entries: list[TensorEntry] = []
    for record in records:
        file_offset = record.offset + data_offset if basis == "relative" else record.offset
        if file_offset < data_offset or file_offset > file_size:
            return None
        if record.size > file_size - file_offset:
            return None
        entries.append(
            TensorEntry(
                name=record.name,
                stored_offset=record.offset,
                size=record.size,
                file_offset=file_offset,
            )
        )
    return tuple(entries)


def _is_dense(entries: Sequence[TensorEntry], data_offset: int, file_size: int) -> bool:
    cursor = data_offset
    for entry in entries:
        if entry.file_offset != cursor:
            return False
        cursor += entry.size
    return cursor == file_size


def read_index(path: os.PathLike[str] | str, *, require_dense: bool = True) -> ContainerIndex:
    """Parse and structurally validate a ``DLSSNRW1`` file.

    ``require_dense=True`` enforces the layout produced by the public installer:
    records are ordered, non-overlapping, gapless and cover the data section.
    """
    source = Path(path)
    file_size = source.stat().st_size
    if file_size < HEADER.size:
        raise FormatError(f"file is smaller than the {HEADER.size}-byte header")

    with source.open("rb") as stream:
        magic, count, data_offset = HEADER.unpack(_read_exact(stream, HEADER.size, "header"))
        if magic != MAGIC:
            raise FormatError(f"bad magic: expected {MAGIC!r}, got {magic!r}")
        if data_offset < HEADER.size or data_offset > file_size:
            raise FormatError(f"invalid data offset {data_offset} for {file_size}-byte file")
        # Every record consumes at least 18 bytes: one-byte name length, one name
        # byte and two uint64 fields. This catches absurd counts before looping.
        if count > (data_offset - HEADER.size) // 18:
            raise FormatError(f"count {count} cannot fit before data offset {data_offset}")
        records = _parse_records(stream, count, data_offset)

    candidates: list[tuple[OffsetBasis, tuple[TensorEntry, ...]]] = []
    for basis in ("relative", "absolute"):
        entries = _candidate_entries(records, data_offset, file_size, basis)
        if entries is None:
            continue
        if require_dense and not _is_dense(entries, data_offset, file_size):
            continue
        candidates.append((basis, entries))

    if not candidates:
        raise FormatError("record offsets do not describe a valid data section")
    if len(candidates) > 1:
        # An empty payload or a specially constructed file can be ambiguous.
        # Prefer relative because it is relocatable and is the writer default.
        candidates.sort(key=lambda item: item[0] != "relative")
    basis, entries = candidates[0]
    return ContainerIndex(
        count=count,
        data_offset=data_offset,
        file_size=file_size,
        offset_basis=basis,
        entries=entries,
    )


def iter_tensor_bytes(
    path: os.PathLike[str] | str, index: ContainerIndex | None = None
) -> Iterator[tuple[TensorEntry, bytes]]:
    source = Path(path)
    parsed = index or read_index(source)
    with source.open("rb") as stream:
        for entry in parsed.entries:
            stream.seek(entry.file_offset)
            yield entry, _read_exact(stream, entry.size, f"tensor {entry.name!r}")


def _build_index(names_and_sizes: Sequence[tuple[str, int]]) -> tuple[bytes, tuple[int, ...]]:
    index = bytearray()
    relative_offsets: list[int] = []
    cursor = 0
    for name, size in names_and_sizes:
        encoded = _validate_name(name)
        if size < 0 or size > 0xFFFFFFFFFFFFFFFF:
            raise ValueError(f"invalid byte size for {name!r}: {size}")
        relative_offsets.append(cursor)
        index.extend(struct.pack("<B", len(encoded)))
        index.extend(encoded)
        # Offset is patched after data_offset is known when absolute mode is used.
        index.extend(struct.pack("<QQ", cursor, size))
        cursor += size
        if cursor > 0xFFFFFFFFFFFFFFFF:
            raise ValueError("aggregate tensor payload exceeds uint64")
    return bytes(index), tuple(relative_offsets)


def _encode_index(
    names_and_sizes: Sequence[tuple[str, int]], data_offset: int, basis: OffsetBasis
) -> bytes:
    output = bytearray()
    cursor = 0
    for name, size in names_and_sizes:
        encoded = _validate_name(name)
        stored_offset = cursor if basis == "relative" else data_offset + cursor
        output.extend(struct.pack("<B", len(encoded)))
        output.extend(encoded)
        output.extend(struct.pack("<QQ", stored_offset, size))
        cursor += size
    return bytes(output)


def write_container(
    sources: Sequence[TensorSource],
    output: os.PathLike[str] | str,
    *,
    offset_basis: OffsetBasis = "relative",
    expected_count: int | None = None,
) -> ContainerIndex:
    """Create a deterministic container from tensor files, then re-parse it."""
    if offset_basis not in ("relative", "absolute"):
        raise ValueError(f"unsupported offset basis: {offset_basis}")
    if expected_count is not None and len(sources) != expected_count:
        raise ValueError(f"expected {expected_count} tensors, received {len(sources)}")
    if len(sources) > 0xFFFFFFFF:
        raise ValueError("tensor count exceeds uint32")

    seen: set[str] = set()
    names_and_sizes: list[tuple[str, int]] = []
    normalized: list[TensorSource] = []
    for source in sources:
        if source.name in seen:
            raise ValueError(f"duplicate tensor name: {source.name!r}")
        seen.add(source.name)
        path = source.path.resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        _validate_name(source.name)
        names_and_sizes.append((source.name, path.stat().st_size))
        normalized.append(TensorSource(source.name, path))

    provisional, _ = _build_index(names_and_sizes)
    data_offset = HEADER.size + len(provisional)
    if data_offset > 0xFFFFFFFF:
        raise ValueError("index/data offset exceeds uint32")
    encoded_index = _encode_index(names_and_sizes, data_offset, offset_basis)
    if len(encoded_index) != len(provisional):
        raise AssertionError("index size changed while patching offsets")

    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_fd, temp_name = tempfile.mkstemp(prefix=destination.name + ".", suffix=".tmp", dir=destination.parent)
    try:
        with os.fdopen(temp_fd, "wb") as stream:
            stream.write(HEADER.pack(MAGIC, len(normalized), data_offset))
            stream.write(encoded_index)
            for source in normalized:
                with source.path.open("rb") as tensor:
                    while chunk := tensor.read(8 * 1024 * 1024):
                        stream.write(chunk)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, destination)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise

    parsed = read_index(destination, require_dense=True)
    if parsed.count != len(normalized) or parsed.offset_basis != offset_basis:
        raise AssertionError("writer round-trip validation failed")
    return parsed


def unpack_container(
    source: os.PathLike[str] | str,
    destination: os.PathLike[str] | str,
    *,
    overwrite: bool = False,
) -> dict[str, object]:
    input_path = Path(source)
    output_root = Path(destination)
    output_root.mkdir(parents=True, exist_ok=True)
    index = read_index(input_path)
    manifest: list[dict[str, object]] = []
    used_paths: set[Path] = set()

    with input_path.open("rb") as stream:
        for ordinal, entry in enumerate(index.entries):
            # Tensor names may contain path syntax; never trust them as paths.
            safe = "".join(char if char.isalnum() or char in "._-" else "_" for char in entry.name)
            safe = safe.strip(".") or f"tensor_{ordinal:03d}"
            candidate = output_root / f"{ordinal:03d}_{safe}.bin"
            suffix = 1
            while candidate in used_paths:
                candidate = output_root / f"{ordinal:03d}_{safe}_{suffix}.bin"
                suffix += 1
            used_paths.add(candidate)
            if candidate.exists() and not overwrite:
                raise FileExistsError(candidate)
            stream.seek(entry.file_offset)
            digest = hashlib.sha256()
            with candidate.open("wb") as tensor:
                remaining = entry.size
                while remaining:
                    chunk = _read_exact(stream, min(remaining, 8 * 1024 * 1024), entry.name)
                    tensor.write(chunk)
                    digest.update(chunk)
                    remaining -= len(chunk)
            manifest.append(
                {
                    "ordinal": ordinal,
                    "name": entry.name,
                    "path": candidate.name,
                    "stored_offset": entry.stored_offset,
                    "file_offset": entry.file_offset,
                    "size": entry.size,
                    "sha256": digest.hexdigest(),
                }
            )

    result: dict[str, object] = {
        "format": MAGIC.decode("ascii"),
        "offset_basis": index.offset_basis,
        "count": index.count,
        "data_offset": index.data_offset,
        "file_size": index.file_size,
        "tensors": manifest,
    }
    (output_root / "manifest.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


def _load_manifest(path: Path) -> list[TensorSource]:
    document = json.loads(path.read_text(encoding="utf-8"))
    items = document.get("tensors") if isinstance(document, dict) else document
    if not isinstance(items, list):
        raise ValueError("manifest must be a list or an object with a 'tensors' list")
    root = path.parent
    sources: list[TensorSource] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"manifest tensor {index} is not an object")
        name = item.get("name")
        source_path = item.get("path")
        if not isinstance(name, str) or not isinstance(source_path, str):
            raise ValueError(f"manifest tensor {index} requires string name/path")
        sources.append(TensorSource(name=name, path=(root / source_path)))
    return sources


def _summary(path: Path, index: ContainerIndex) -> dict[str, object]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    return {
        "path": str(path),
        "format": MAGIC.decode("ascii"),
        "count": index.count,
        "data_offset": index.data_offset,
        "file_size": index.file_size,
        "payload_size": index.file_size - index.data_offset,
        "offset_basis": index.offset_basis,
        "sha256": digest.hexdigest(),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_parser = sub.add_parser("inspect", help="validate and summarize a container")
    inspect_parser.add_argument("container", type=Path)
    inspect_parser.add_argument("--list", action="store_true", dest="list_entries")

    unpack_parser = sub.add_parser("unpack", help="extract tensors and a JSON manifest")
    unpack_parser.add_argument("container", type=Path)
    unpack_parser.add_argument("destination", type=Path)
    unpack_parser.add_argument("--overwrite", action="store_true")

    pack_parser = sub.add_parser("pack", help="pack a manifest into DLSSNRW1")
    pack_parser.add_argument("manifest", type=Path)
    pack_parser.add_argument("output", type=Path)
    pack_parser.add_argument("--basis", choices=("relative", "absolute"), default="relative")
    pack_parser.add_argument("--expected-count", type=int, default=None)

    args = parser.parse_args(argv)
    if args.command == "inspect":
        index = read_index(args.container)
        result = _summary(args.container, index)
        if args.list_entries:
            result["tensors"] = [dataclasses.asdict(entry) for entry in index.entries]
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if args.command == "unpack":
        result = unpack_container(args.container, args.destination, overwrite=args.overwrite)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if args.command == "pack":
        sources = _load_manifest(args.manifest)
        index = write_container(
            sources,
            args.output,
            offset_basis=args.basis,
            expected_count=args.expected_count,
        )
        print(json.dumps(_summary(args.output, index), indent=2, ensure_ascii=False))
        return 0
    parser.error("unreachable")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FormatError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
