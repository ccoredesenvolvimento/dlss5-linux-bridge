from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

import pytest

from dlssnrw1 import (
    FormatError,
    HEADER,
    MAGIC,
    TensorSource,
    read_index,
    unpack_container,
    write_container,
)


def _sources(root: Path, count: int = 4) -> tuple[list[TensorSource], dict[str, bytes]]:
    sources: list[TensorSource] = []
    expected: dict[str, bytes] = {}
    for index in range(count):
        name = ["front.weight", "block24.layer0", "átenção.bias", "tail/out"][index]
        data = bytes(((position * 17 + index * 31) & 0xFF) for position in range(index * 37 + 1))
        path = root / f"source-{index}.bin"
        path.write_bytes(data)
        sources.append(TensorSource(name, path))
        expected[name] = data
    return sources, expected


@pytest.mark.parametrize("basis", ["relative", "absolute"])
def test_round_trip_and_unpack(tmp_path: Path, basis: str) -> None:
    sources, expected = _sources(tmp_path)
    container = tmp_path / f"weights-{basis}.bin"
    index = write_container(sources, container, offset_basis=basis, expected_count=4)  # type: ignore[arg-type]

    assert index.count == 4
    assert index.offset_basis == basis
    assert container.read_bytes()[:8] == MAGIC
    assert [entry.name for entry in index.entries] == [source.name for source in sources]
    assert [entry.size for entry in index.entries] == [len(expected[source.name]) for source in sources]

    out = tmp_path / f"unpacked-{basis}"
    manifest = unpack_container(container, out)
    assert manifest["count"] == 4
    for item in manifest["tensors"]:  # type: ignore[index]
        name = item["name"]  # type: ignore[index]
        data = (out / item["path"]).read_bytes()  # type: ignore[index]
        assert data == expected[name]
        assert item["sha256"] == hashlib.sha256(data).hexdigest()  # type: ignore[index]


def test_header_and_index_contract(tmp_path: Path) -> None:
    sources, expected = _sources(tmp_path)
    container = tmp_path / "weights.bin"
    index = write_container(sources, container)
    raw = container.read_bytes()

    magic, count, data_offset = HEADER.unpack_from(raw)
    assert magic == MAGIC
    assert count == len(sources)
    assert data_offset == index.data_offset

    cursor = HEADER.size
    payload_cursor = 0
    for source in sources:
        name_size = raw[cursor]
        cursor += 1
        name = raw[cursor : cursor + name_size].decode("utf-8")
        cursor += name_size
        offset, size = struct.unpack_from("<QQ", raw, cursor)
        cursor += 16
        assert name == source.name
        assert offset == payload_cursor
        assert size == len(expected[name])
        payload_cursor += size
    assert cursor == data_offset
    assert payload_cursor == len(raw) - data_offset


def test_rejects_bad_magic(tmp_path: Path) -> None:
    path = tmp_path / "bad.bin"
    path.write_bytes(b"NOTNRW1!" + struct.pack("<II", 0, 16))
    with pytest.raises(FormatError, match="bad magic"):
        read_index(path)


def test_rejects_bad_data_offset(tmp_path: Path) -> None:
    path = tmp_path / "bad.bin"
    path.write_bytes(HEADER.pack(MAGIC, 0, 4096))
    with pytest.raises(FormatError, match="invalid data offset"):
        read_index(path)


def test_rejects_duplicate_names(tmp_path: Path) -> None:
    first = tmp_path / "a.bin"
    second = tmp_path / "b.bin"
    first.write_bytes(b"a")
    second.write_bytes(b"b")
    with pytest.raises(ValueError, match="duplicate tensor name"):
        write_container([TensorSource("same", first), TensorSource("same", second)], tmp_path / "out.bin")


def test_rejects_non_dense_payload(tmp_path: Path) -> None:
    source = tmp_path / "source.bin"
    source.write_bytes(b"payload")
    container = tmp_path / "weights.bin"
    write_container([TensorSource("x", source)], container)
    raw = bytearray(container.read_bytes())
    name_size = raw[HEADER.size]
    offset_position = HEADER.size + 1 + name_size
    struct.pack_into("<Q", raw, offset_position, 1)
    container.write_bytes(raw)
    with pytest.raises(FormatError, match="valid data section"):
        read_index(container)


def test_expected_count_gate(tmp_path: Path) -> None:
    sources, _ = _sources(tmp_path)
    with pytest.raises(ValueError, match="expected 153 tensors"):
        write_container(sources, tmp_path / "weights.bin", expected_count=153)


def test_manifest_is_json_serializable(tmp_path: Path) -> None:
    sources, _ = _sources(tmp_path)
    container = tmp_path / "weights.bin"
    write_container(sources, container)
    manifest = unpack_container(container, tmp_path / "out")
    json.dumps(manifest, ensure_ascii=False)
