from __future__ import annotations

import json
from pathlib import Path

import pytest

from dlssnrw1 import read_index
from pack_private_by_contract import MappingError, execute


def write_contract(path: Path) -> Path:
    rows = [
        {"ordinal": 0, "name": "block0.layer0.layer", "byte_size": 3},
        {"ordinal": 1, "name": "block1.layer0.layer", "byte_size": 5},
        {"ordinal": 2, "name": "block70.layer0.blend_scale", "byte_size": 2},
    ]
    path.write_text(json.dumps({"count": len(rows), "tensors": rows}), encoding="utf-8")
    return path


def test_contract_driven_pack_and_order(tmp_path: Path) -> None:
    contract = write_contract(tmp_path / "contract.json")
    private = tmp_path / "private"
    (private / "nested").mkdir(parents=True)
    (private / "block1.layer0.layer.bin").write_bytes(b"12345")
    (private / "nested" / "block0.layer0.layer.bin").write_bytes(b"abc")
    (private / "block70.layer0.blend_scale").write_bytes(b"xy")
    output = tmp_path / "dlssnr_on_amd_weights.bin"
    report_path = tmp_path / "report.json"

    report = execute(
        private,
        contract,
        output,
        dry_run=False,
        report_path=report_path,
        basis="relative",
    )
    assert report["verified"] is True
    assert report["resolved_count"] == 3
    assert output.stat().st_size == report["container_file_size"]
    index = read_index(output)
    assert [(entry.name, entry.size) for entry in index.entries] == [
        ("block0.layer0.layer", 3),
        ("block1.layer0.layer", 5),
        ("block70.layer0.blend_scale", 2),
    ]
    persisted = json.loads(report_path.read_text(encoding="utf-8"))
    assert persisted["container_sha256"] == report["container_sha256"]


def test_identical_duplicate_is_resolved_deterministically(tmp_path: Path) -> None:
    contract = write_contract(tmp_path / "contract.json")
    private = tmp_path / "private"
    (private / "a").mkdir(parents=True)
    (private / "b" / "deeper").mkdir(parents=True)
    for directory in (private / "a", private / "b" / "deeper"):
        (directory / "block0.layer0.layer.bin").write_bytes(b"abc")
    (private / "block1.layer0.layer.bin").write_bytes(b"12345")
    (private / "block70.layer0.blend_scale.bin").write_bytes(b"xy")

    report = execute(
        private,
        contract,
        tmp_path / "out.bin",
        dry_run=True,
        report_path=None,
        basis="relative",
    )
    item = next(row for row in report["resolved"] if row["name"] == "block0.layer0.layer")
    assert item["duplicate_count"] == 2
    assert item["path"].endswith("a/block0.layer0.layer.bin")
    assert item["sha256"] is not None


def test_nonidentical_duplicate_is_rejected(tmp_path: Path) -> None:
    contract = write_contract(tmp_path / "contract.json")
    private = tmp_path / "private"
    (private / "a").mkdir(parents=True)
    (private / "b").mkdir(parents=True)
    (private / "a" / "block0.layer0.layer.bin").write_bytes(b"abc")
    (private / "b" / "block0.layer0.layer.bin").write_bytes(b"xyz")
    (private / "block1.layer0.layer.bin").write_bytes(b"12345")
    (private / "block70.layer0.blend_scale.bin").write_bytes(b"xy")
    report = tmp_path / "mapping-report.json"

    with pytest.raises(MappingError, match="resolved 2/3"):
        execute(
            private,
            contract,
            tmp_path / "out.bin",
            dry_run=False,
            report_path=report,
            basis="relative",
        )
    document = json.loads(report.read_text(encoding="utf-8"))
    assert document["missing_or_ambiguous_count"] == 1
    assert "ambiguous non-identical" in document["failures"][0]
    assert not (tmp_path / "out.bin").exists()


def test_wrong_size_is_reported(tmp_path: Path) -> None:
    contract = write_contract(tmp_path / "contract.json")
    private = tmp_path / "private"
    private.mkdir()
    (private / "block0.layer0.layer.bin").write_bytes(b"wrong")
    (private / "block1.layer0.layer.bin").write_bytes(b"12345")
    (private / "block70.layer0.blend_scale.bin").write_bytes(b"xy")
    report = tmp_path / "mapping-report.json"

    with pytest.raises(MappingError):
        execute(
            private,
            contract,
            tmp_path / "out.bin",
            dry_run=True,
            report_path=report,
            basis="relative",
        )
    document = json.loads(report.read_text(encoding="utf-8"))
    assert document["resolved_count"] == 2
    assert "exact size 3" in document["failures"][0]
