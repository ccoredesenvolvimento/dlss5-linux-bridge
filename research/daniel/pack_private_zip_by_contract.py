#!/usr/bin/env python3
"""Create a Daniel-compatible ``DLSSNRW1`` file directly from a private ZIP.

The command never extracts the archive to disk. It resolves the exact, publicly
recovered 153-name/size contract from either:

* individual archive members whose basenames match tensor names; or
* JSON/CSV inventories that describe slices of larger archive members.

Every tensor is required, ordered by the contract, size-checked, streamed into
the output and hashed. Ambiguous non-identical candidates are rejected. The
private ZIP and generated weight container must remain local and are never
suitable for committing to the public repository.
"""
from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import io
import json
import os
import posixpath
import struct
import sys
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, BinaryIO, Iterable, Iterator, Literal, Sequence

from dlssnrw1 import HEADER, MAGIC, FormatError, read_index

OffsetBasis = Literal["relative", "absolute"]
NAME_KEYS = ("name", "tensor_name", "tensor", "key", "logical_name")
PATH_KEYS = (
    "path",
    "file",
    "file_path",
    "filename",
    "source_path",
    "blob_path",
    "container_path",
    "member",
    "archive_member",
)
OFFSET_KEYS = ("offset", "byte_offset", "start", "file_offset")
SIZE_KEYS = ("size", "nbytes", "byte_size", "length", "num_bytes")
ORDER_KEYS = ("ordinal", "index", "order", "tensor_index")
HASH_KEYS = ("sha256", "hash", "digest")
LIST_KEYS = ("tensors", "entries", "records", "items", "blobs", "weights")
COMMON_SUFFIXES = (".bin", ".dat", ".raw", ".blob", ".weights", ".tensor")
MAX_INVENTORY_BYTES = 32 * 1024 * 1024
COPY_CHUNK = 8 * 1024 * 1024


class MappingError(ValueError):
    """Raised when the archive cannot satisfy the exact tensor contract."""


@dataclasses.dataclass(frozen=True, slots=True)
class ContractTensor:
    ordinal: int
    name: str
    byte_size: int


@dataclasses.dataclass(frozen=True, slots=True)
class ArchiveSlice:
    member: str
    offset: int
    size: int
    expected_sha256: str | None
    origin: str

    def identity(self) -> tuple[str, int, int]:
        return (self.member, self.offset, self.size)


@dataclasses.dataclass(frozen=True, slots=True)
class Resolution:
    tensor: ContractTensor
    source: ArchiveSlice
    sha256: str
    candidate_count: int


@dataclasses.dataclass(frozen=True, slots=True)
class InventoryCandidate:
    member: str
    records: dict[str, tuple[ArchiveSlice, ...]]
    exact_contract_matches: int
    extraneous_records: int


class SliceReader:
    """Bounded sequential reader over a member slice."""

    def __init__(self, stream: BinaryIO, remaining: int) -> None:
        self._stream = stream
        self._remaining = remaining

    @property
    def remaining(self) -> int:
        return self._remaining

    def read(self, size: int = -1) -> bytes:
        if self._remaining == 0:
            return b""
        if size < 0 or size > self._remaining:
            size = self._remaining
        data = self._stream.read(size)
        if len(data) != size:
            raise MappingError(
                f"truncated archive member: expected {size} bytes, received {len(data)}"
            )
        self._remaining -= len(data)
        return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(COPY_CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def _first(mapping: dict[str, Any], keys: Iterable[str]) -> Any:
    lowered = {str(key).lower(): value for key, value in mapping.items()}
    for key in keys:
        value = lowered.get(key)
        if value not in (None, ""):
            return value
    return None


def _integer(value: Any, field: str, *, default: int | None = None) -> int:
    if value in (None, ""):
        if default is not None:
            return default
        raise MappingError(f"missing {field}")
    if isinstance(value, bool):
        raise MappingError(f"{field} must be an integer")
    try:
        result = int(value, 0) if isinstance(value, str) else int(value)
    except (TypeError, ValueError) as exc:
        raise MappingError(f"invalid {field}: {value!r}") from exc
    if result < 0:
        raise MappingError(f"{field} must be non-negative")
    return result


def _sha256_value(value: Any) -> str | None:
    if value in (None, ""):
        return None
    text = str(value).strip().lower().removeprefix("sha256:")
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        return None
    return text


def load_contract(path: Path) -> tuple[ContractTensor, ...]:
    document = json.loads(path.read_text(encoding="utf-8"))
    rows = document.get("tensors") if isinstance(document, dict) else None
    if not isinstance(rows, list):
        raise MappingError("contract must contain a 'tensors' list")
    tensors: list[ContractTensor] = []
    names: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise MappingError(f"contract row {index} is not an object")
        try:
            ordinal = int(row["ordinal"])
            name = str(row["name"])
            byte_size = int(row["byte_size"])
        except (KeyError, TypeError, ValueError) as exc:
            raise MappingError(f"contract row {index} is incomplete") from exc
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


def _safe_member_name(name: str) -> str:
    # zipfile already normalizes separators for normal archives, but treat member
    # paths as POSIX and reject NUL/absolute/traversal syntax anyway.
    if not name or "\x00" in name:
        raise MappingError("archive contains an empty/NUL member name")
    normalized = posixpath.normpath(name.replace("\\", "/"))
    if normalized.startswith("/") or normalized == ".." or normalized.startswith("../"):
        raise MappingError(f"unsafe archive member path: {name!r}")
    return normalized


def _member_keys(member: str) -> set[str]:
    basename = PurePosixPath(member).name
    keys = {basename}
    lowered = basename.lower()
    for suffix in COMMON_SUFFIXES:
        if lowered.endswith(suffix):
            keys.add(basename[: -len(suffix)])
    return keys


def _archive_members(archive: zipfile.ZipFile) -> tuple[dict[str, zipfile.ZipInfo], dict[str, list[str]], dict[str, list[str]]]:
    exact: dict[str, zipfile.ZipInfo] = {}
    by_key: dict[str, list[str]] = defaultdict(list)
    by_basename: dict[str, list[str]] = defaultdict(list)
    for info in archive.infolist():
        if info.is_dir():
            continue
        name = _safe_member_name(info.filename)
        if name in exact:
            raise MappingError(f"duplicate archive member path: {name!r}")
        exact[name] = info
        by_basename[PurePosixPath(name).name].append(name)
        for key in _member_keys(name):
            by_key[key].append(name)
    for mapping in (by_key, by_basename):
        for values in mapping.values():
            values.sort()
    return exact, dict(by_key), dict(by_basename)


def _extract_rows(document: Any) -> list[dict[str, Any]]:
    if isinstance(document, list):
        rows = document
    elif isinstance(document, dict):
        rows: Any = None
        for key in LIST_KEYS:
            candidate = document.get(key)
            if isinstance(candidate, list):
                rows = candidate
                break
        if rows is None:
            converted: list[dict[str, Any]] = []
            for key, value in document.items():
                if isinstance(value, dict):
                    converted.append({"name": key, **value})
                elif isinstance(value, str):
                    converted.append({"name": key, "path": value})
            rows = converted
    else:
        return []
    return [row for row in rows if isinstance(row, dict)]


def _read_inventory_rows(archive: zipfile.ZipFile, info: zipfile.ZipInfo) -> list[dict[str, Any]]:
    if info.file_size > MAX_INVENTORY_BYTES:
        return []
    raw = archive.read(info)
    suffix = PurePosixPath(info.filename).suffix.lower()
    if suffix == ".json":
        return _extract_rows(json.loads(raw.decode("utf-8-sig")))
    if suffix == ".csv":
        text = raw.decode("utf-8-sig")
        return [dict(row) for row in csv.DictReader(io.StringIO(text))]
    return []


def _resolve_member_reference(
    value: Any,
    inventory_member: str,
    exact: dict[str, zipfile.ZipInfo],
    by_basename: dict[str, list[str]],
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MappingError("inventory record has no source member")
    supplied = _safe_member_name(value.strip())
    parent = str(PurePosixPath(inventory_member).parent)
    relative = _safe_member_name(posixpath.join(parent, supplied)) if parent != "." else supplied
    for candidate in (supplied, relative):
        if candidate in exact:
            return candidate
    basename_matches = by_basename.get(PurePosixPath(supplied).name, [])
    if len(basename_matches) == 1:
        return basename_matches[0]
    if len(basename_matches) > 1:
        raise MappingError(
            f"inventory reference {value!r} is ambiguous: {basename_matches[:8]}"
        )
    raise MappingError(f"inventory reference does not exist in ZIP: {value!r}")


def _parse_inventory(
    archive: zipfile.ZipFile,
    info: zipfile.ZipInfo,
    exact: dict[str, zipfile.ZipInfo],
    by_basename: dict[str, list[str]],
    contract_by_name: dict[str, ContractTensor],
) -> InventoryCandidate | None:
    try:
        rows = _read_inventory_rows(archive, info)
    except (UnicodeError, json.JSONDecodeError, csv.Error, MappingError, KeyError):
        return None
    records: dict[str, list[ArchiveSlice]] = defaultdict(list)
    extraneous = 0
    for row in rows:
        name_value = _first(row, NAME_KEYS)
        path_value = _first(row, PATH_KEYS)
        if name_value in (None, "") or path_value in (None, ""):
            continue
        name = str(name_value)
        contract_tensor = contract_by_name.get(name)
        if contract_tensor is None:
            extraneous += 1
            continue
        try:
            member = _resolve_member_reference(path_value, info.filename, exact, by_basename)
            member_size = exact[member].file_size
            offset = _integer(_first(row, OFFSET_KEYS), "offset", default=0)
            available = member_size - offset
            if available < 0:
                raise MappingError("slice offset exceeds member size")
            size = _integer(_first(row, SIZE_KEYS), "size", default=available)
            if size > available:
                raise MappingError("slice exceeds member size")
            if size != contract_tensor.byte_size:
                continue
            records[name].append(
                ArchiveSlice(
                    member=member,
                    offset=offset,
                    size=size,
                    expected_sha256=_sha256_value(_first(row, HASH_KEYS)),
                    origin=f"inventory:{info.filename}",
                )
            )
        except MappingError:
            continue
    if not records:
        return None
    frozen = {name: tuple(values) for name, values in records.items()}
    return InventoryCandidate(
        member=info.filename,
        records=frozen,
        exact_contract_matches=len(frozen),
        extraneous_records=extraneous,
    )


def discover_inventories(
    archive: zipfile.ZipFile,
    exact: dict[str, zipfile.ZipInfo],
    by_basename: dict[str, list[str]],
    contract: Sequence[ContractTensor],
    forced_member: str | None,
) -> tuple[InventoryCandidate, ...]:
    contract_by_name = {tensor.name: tensor for tensor in contract}
    candidates: list[InventoryCandidate] = []
    infos: Iterable[zipfile.ZipInfo]
    if forced_member is not None:
        normalized = _safe_member_name(forced_member)
        info = exact.get(normalized)
        if info is None:
            raise MappingError(f"forced inventory member not found: {forced_member!r}")
        infos = (info,)
    else:
        infos = (
            info
            for info in exact.values()
            if PurePosixPath(info.filename).suffix.lower() in {".json", ".csv"}
        )
    for info in infos:
        candidate = _parse_inventory(archive, info, exact, by_basename, contract_by_name)
        if candidate is not None:
            candidates.append(candidate)
    candidates.sort(
        key=lambda item: (
            -item.exact_contract_matches,
            item.extraneous_records,
            item.member,
        )
    )
    return tuple(candidates)


def _direct_candidates(
    tensor: ContractTensor,
    exact: dict[str, zipfile.ZipInfo],
    by_key: dict[str, list[str]],
) -> list[ArchiveSlice]:
    members: set[str] = set()
    for key in (tensor.name, *(tensor.name + suffix for suffix in COMMON_SUFFIXES)):
        members.update(by_key.get(key, ()))
    result = []
    for member in sorted(members):
        info = exact[member]
        if info.file_size == tensor.byte_size:
            result.append(
                ArchiveSlice(
                    member=member,
                    offset=0,
                    size=info.file_size,
                    expected_sha256=None,
                    origin="direct-member",
                )
            )
    return result


def _open_slice(archive: zipfile.ZipFile, source: ArchiveSlice) -> tuple[BinaryIO, SliceReader]:
    stream = archive.open(source.member, "r")
    remaining_skip = source.offset
    while remaining_skip:
        chunk = stream.read(min(remaining_skip, COPY_CHUNK))
        if not chunk:
            stream.close()
            raise MappingError(
                f"truncated member {source.member!r} while skipping to offset {source.offset}"
            )
        remaining_skip -= len(chunk)
    return stream, SliceReader(stream, source.size)


def hash_slice(archive: zipfile.ZipFile, source: ArchiveSlice) -> str:
    digest = hashlib.sha256()
    stream, bounded = _open_slice(archive, source)
    try:
        while chunk := bounded.read(COPY_CHUNK):
            digest.update(chunk)
    finally:
        stream.close()
    if bounded.remaining:
        raise MappingError(f"short read while hashing {source.member!r}")
    actual = digest.hexdigest()
    if source.expected_sha256 is not None and actual != source.expected_sha256:
        raise MappingError(
            f"SHA-256 mismatch for {source.member!r}: expected "
            f"{source.expected_sha256}, got {actual}"
        )
    return actual


def resolve_contract(
    archive: zipfile.ZipFile,
    contract: Sequence[ContractTensor],
    exact: dict[str, zipfile.ZipInfo],
    by_key: dict[str, list[str]],
    inventories: Sequence[InventoryCandidate],
) -> tuple[Resolution, ...]:
    resolutions: list[Resolution] = []
    failures: list[str] = []
    for tensor in contract:
        candidates: dict[tuple[str, int, int], ArchiveSlice] = {}
        for inventory in inventories:
            for source in inventory.records.get(tensor.name, ()):
                candidates.setdefault(source.identity(), source)
        for source in _direct_candidates(tensor, exact, by_key):
            candidates.setdefault(source.identity(), source)
        if not candidates:
            failures.append(f"missing {tensor.name!r} ({tensor.byte_size} bytes)")
            continue

        hashed: list[tuple[ArchiveSlice, str]] = []
        for source in candidates.values():
            try:
                hashed.append((source, hash_slice(archive, source)))
            except MappingError as exc:
                failures.append(f"{tensor.name!r}: {exc}")
        if not hashed:
            continue
        distinct = {digest for _, digest in hashed}
        if len(distinct) != 1:
            details = ", ".join(
                f"{source.member}@{source.offset}+{source.size}={digest}"
                for source, digest in hashed[:12]
            )
            failures.append(f"ambiguous non-identical candidates for {tensor.name!r}: {details}")
            continue
        chosen, digest = min(
            hashed,
            key=lambda item: (
                item[0].origin != "direct-member",
                len(PurePosixPath(item[0].member).parts),
                item[0].member,
                item[0].offset,
            ),
        )
        resolutions.append(
            Resolution(
                tensor=tensor,
                source=chosen,
                sha256=digest,
                candidate_count=len(hashed),
            )
        )

    if failures:
        preview = "\n".join(f"  - {failure}" for failure in failures[:40])
        suffix = "" if len(failures) <= 40 else f"\n  ... and {len(failures) - 40} more"
        raise MappingError(
            f"resolved {len(resolutions)}/{len(contract)} tensors; failures:\n{preview}{suffix}"
        )
    if len(resolutions) != len(contract):
        raise MappingError("internal resolution-count mismatch")
    return tuple(resolutions)


def _encode_index(contract: Sequence[ContractTensor], data_offset: int, basis: OffsetBasis) -> bytes:
    output = bytearray()
    cursor = 0
    for tensor in contract:
        encoded = tensor.name.encode("utf-8")
        if not encoded or len(encoded) > 255:
            raise MappingError(f"name cannot be encoded in DLSSNRW1: {tensor.name!r}")
        stored_offset = cursor if basis == "relative" else data_offset + cursor
        output.extend(struct.pack("<B", len(encoded)))
        output.extend(encoded)
        output.extend(struct.pack("<QQ", stored_offset, tensor.byte_size))
        cursor += tensor.byte_size
    return bytes(output)


def write_container_from_archive(
    archive: zipfile.ZipFile,
    resolutions: Sequence[Resolution],
    output: Path,
    *,
    offset_basis: OffsetBasis,
) -> tuple[str, int, int]:
    contract = [resolution.tensor for resolution in resolutions]
    provisional_index_size = sum(1 + len(item.name.encode("utf-8")) + 16 for item in contract)
    data_offset = HEADER.size + provisional_index_size
    if data_offset > 0xFFFFFFFF:
        raise MappingError("DLSSNRW1 data offset exceeds uint32")
    index = _encode_index(contract, data_offset, offset_basis)
    if len(index) != provisional_index_size:
        raise AssertionError("index-size calculation mismatch")

    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=output.name + ".", suffix=".tmp", dir=output.parent
    )
    container_digest = hashlib.sha256()
    try:
        with os.fdopen(fd, "wb") as destination:
            header = HEADER.pack(MAGIC, len(resolutions), data_offset)
            destination.write(header)
            destination.write(index)
            container_digest.update(header)
            container_digest.update(index)
            for resolution in resolutions:
                tensor_digest = hashlib.sha256()
                stream, bounded = _open_slice(archive, resolution.source)
                try:
                    while chunk := bounded.read(COPY_CHUNK):
                        destination.write(chunk)
                        container_digest.update(chunk)
                        tensor_digest.update(chunk)
                finally:
                    stream.close()
                if bounded.remaining:
                    raise MappingError(f"short copy for {resolution.tensor.name!r}")
                actual = tensor_digest.hexdigest()
                if actual != resolution.sha256:
                    raise MappingError(
                        f"source changed while copying {resolution.tensor.name!r}: "
                        f"expected {resolution.sha256}, got {actual}"
                    )
            destination.flush()
            os.fsync(destination.fileno())
        os.replace(temporary_name, output)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise

    parsed = read_index(output, require_dense=True)
    expected = [(item.name, item.byte_size) for item in contract]
    actual = [(item.name, item.size) for item in parsed.entries]
    if actual != expected or parsed.offset_basis != offset_basis:
        try:
            output.unlink()
        except OSError:
            pass
        raise MappingError("post-write DLSSNRW1 validation failed")
    return container_digest.hexdigest(), parsed.data_offset, parsed.file_size


def execute(
    private_zip: Path,
    contract_path: Path,
    output: Path,
    *,
    offset_basis: OffsetBasis,
    forced_inventory: str | None,
    expected_private_sha256: str | None,
    dry_run: bool,
    report_path: Path | None,
) -> dict[str, Any]:
    private_zip = private_zip.resolve()
    contract_path = contract_path.resolve()
    output = output.resolve()
    if not private_zip.is_file():
        raise MappingError(f"private ZIP not found: {private_zip}")
    if not contract_path.is_file():
        raise MappingError(f"tensor contract not found: {contract_path}")
    if private_zip == output:
        raise MappingError("input ZIP and output container must be different files")

    archive_sha256 = sha256_file(private_zip)
    if expected_private_sha256 is not None:
        expected = expected_private_sha256.strip().lower().removeprefix("sha256:")
        if archive_sha256 != expected:
            raise MappingError(
                f"private ZIP SHA-256 mismatch: expected {expected}, got {archive_sha256}"
            )

    contract = load_contract(contract_path)
    try:
        with zipfile.ZipFile(private_zip, "r") as archive:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise MappingError(f"ZIP CRC failure in member: {bad_member}")
            exact, by_key, by_basename = _archive_members(archive)
            inventories = discover_inventories(
                archive,
                exact,
                by_basename,
                contract,
                forced_inventory,
            )
            resolutions = resolve_contract(
                archive,
                contract,
                exact,
                by_key,
                inventories,
            )
            report: dict[str, Any] = {
                "schema_version": 1,
                "private_zip": str(private_zip),
                "private_zip_sha256": archive_sha256,
                "contract": str(contract_path),
                "required_count": len(contract),
                "resolved_count": len(resolutions),
                "required_payload_bytes": sum(item.byte_size for item in contract),
                "resolved_payload_bytes": sum(item.tensor.byte_size for item in resolutions),
                "archive_member_count": len(exact),
                "inventory_candidates": [
                    {
                        "member": item.member,
                        "exact_contract_matches": item.exact_contract_matches,
                        "extraneous_records": item.extraneous_records,
                    }
                    for item in inventories
                ],
                "offset_basis": offset_basis,
                "output": str(output),
                "dry_run": dry_run,
                "tensors": [
                    {
                        "ordinal": item.tensor.ordinal,
                        "name": item.tensor.name,
                        "byte_size": item.tensor.byte_size,
                        "source_member": item.source.member,
                        "source_offset": item.source.offset,
                        "source_kind": item.source.origin,
                        "candidate_count": item.candidate_count,
                        "sha256": item.sha256,
                    }
                    for item in resolutions
                ],
            }
            if not dry_run:
                container_sha256, data_offset, file_size = write_container_from_archive(
                    archive,
                    resolutions,
                    output,
                    offset_basis=offset_basis,
                )
                report.update(
                    {
                        "container_sha256": container_sha256,
                        "container_data_offset": data_offset,
                        "container_file_size": file_size,
                    }
                )
            report["verified"] = True
    except zipfile.BadZipFile as exc:
        raise MappingError(f"invalid private ZIP: {exc}") from exc

    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_zip", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path(__file__).with_name("results") / "tensor-contract.json",
    )
    parser.add_argument("--inventory", help="force one JSON/CSV member inside the ZIP")
    parser.add_argument("--basis", choices=("relative", "absolute"), default="relative")
    parser.add_argument("--expected-private-sha256")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = execute(
            args.private_zip,
            args.contract,
            args.output,
            offset_basis=args.basis,
            forced_inventory=args.inventory,
            expected_private_sha256=args.expected_private_sha256,
            dry_run=args.dry_run,
            report_path=args.report,
        )
    except (OSError, MappingError, FormatError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    compact = {key: value for key, value in report.items() if key != "tensors"}
    print(json.dumps(compact, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
