from __future__ import annotations

import hashlib
import json
from pathlib import Path

from dlssnrw1 import read_index
from private_inventory_to_dlssnrw1 import convert, discover_inventory


def test_json_inventory_with_file_slices(tmp_path: Path) -> None:
    packed = tmp_path / "container.bin"
    packed.write_bytes(b"prefix" + b"AAAA" + b"BBBBB" + b"suffix")
    direct = tmp_path / "tail.bin"
    direct.write_bytes(b"CCC")
    inventory = tmp_path / "tensor_inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "tensors": [
                    {
                        "name": "first",
                        "container_path": packed.name,
                        "byte_offset": 6,
                        "byte_size": 4,
                        "ordinal": 0,
                        "sha256": hashlib.sha256(b"AAAA").hexdigest(),
                    },
                    {
                        "name": "second",
                        "container_path": packed.name,
                        "byte_offset": 10,
                        "byte_size": 5,
                        "ordinal": 1,
                    },
                    {"name": "third", "path": direct.name, "ordinal": 2},
                ]
            }
        ),
        encoding="utf-8",
    )

    discovered = discover_inventory(tmp_path, expected_count=3)
    assert discovered.path == inventory
    output = tmp_path / "dlssnr_on_amd_weights.bin"
    result = convert(
        tmp_path,
        output,
        inventory_path=None,
        expected_count=3,
        basis="relative",
        dry_run=False,
    )
    assert result["verified"] is True
    index = read_index(output)
    assert [entry.name for entry in index.entries] == ["first", "second", "third"]
    assert [entry.size for entry in index.entries] == [4, 5, 3]


def test_csv_inventory_preserves_row_order(tmp_path: Path) -> None:
    (tmp_path / "a.bin").write_bytes(b"a")
    (tmp_path / "b.bin").write_bytes(b"bb")
    inventory = tmp_path / "inventory.csv"
    inventory.write_text("tensor_name,file_path\nb,b.bin\na,a.bin\n", encoding="utf-8")
    candidate = discover_inventory(tmp_path, expected_count=2)
    assert [tensor.name for tensor in candidate.tensors] == ["b", "a"]


def test_dry_run_does_not_create_output(tmp_path: Path) -> None:
    (tmp_path / "x.bin").write_bytes(b"x")
    inventory = tmp_path / "tensors.json"
    inventory.write_text(json.dumps([{"name": "x", "path": "x.bin"}]), encoding="utf-8")
    output = tmp_path / "out.bin"
    result = convert(
        tmp_path,
        output,
        inventory_path=inventory,
        expected_count=1,
        basis="relative",
        dry_run=True,
    )
    assert result["dry_run"] is True
    assert not output.exists()
