from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import pytest

from dlssnrw1 import iter_tensor_bytes, read_index
from pack_private_zip_by_contract import MappingError, execute


def _contract(path: Path) -> Path:
    tensors = [
        {"ordinal": 0, "name": "block0.layer0.layer", "byte_size": 3},
        {"ordinal": 1, "name": "block1.layer0.layer", "byte_size": 5},
        {"ordinal": 2, "name": "block70.layer0.blend_scale", "byte_size": 2},
    ]
    path.write_text(json.dumps({"count": 3, "tensors": tensors}), encoding="utf-8")
    return path


def _payloads() -> dict[str, bytes]:
    return {
        "block0.layer0.layer": b"abc",
        "block1.layer0.layer": b"12345",
        "block70.layer0.blend_scale": b"xy",
    }


def _contents(container: Path) -> dict[str, bytes]:
    return {entry.name: data for entry, data in iter_tensor_bytes(container)}


def test_direct_members_are_ordered_by_contract(tmp_path: Path) -> None:
    contract = _contract(tmp_path / "contract.json")
    archive_path = tmp_path / "private.zip"
    payloads = _payloads()
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        # Deliberately write in a different order and at different depths.
        archive.writestr("private/tensors/block70.layer0.blend_scale.bin", payloads["block70.layer0.blend_scale"])
        archive.writestr("root/block1.layer0.layer.raw", payloads["block1.layer0.layer"])
        archive.writestr("root/deeper/block0.layer0.layer", payloads["block0.layer0.layer"])
        archive.writestr("notes/readme.md", "not a tensor")

    output = tmp_path / "dlssnr_on_amd_weights.bin"
    report_path = tmp_path / "report.json"
    report = execute(
        archive_path,
        contract,
        output,
        offset_basis="relative",
        forced_inventory=None,
        expected_private_sha256=hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        dry_run=False,
        report_path=report_path,
    )

    assert report["verified"] is True
    assert report["resolved_count"] == 3
    assert report["container_file_size"] == output.stat().st_size
    assert _contents(output) == payloads
    assert [(entry.name, entry.size) for entry in read_index(output).entries] == [
        ("block0.layer0.layer", 3),
        ("block1.layer0.layer", 5),
        ("block70.layer0.blend_scale", 2),
    ]
    assert json.loads(report_path.read_text(encoding="utf-8"))["container_sha256"] == report["container_sha256"]


def test_json_inventory_can_reference_slices(tmp_path: Path) -> None:
    contract = _contract(tmp_path / "contract.json")
    archive_path = tmp_path / "private.zip"
    payloads = _payloads()
    combined = b"PREFIX" + payloads["block1.layer0.layer"] + payloads["block0.layer0.layer"] + b"GAP" + payloads["block70.layer0.blend_scale"] + b"SUFFIX"
    inventory = {
        "tensors": [
            {
                "ordinal": 2,
                "name": "block70.layer0.blend_scale",
                "container_path": "../containers/all.blob",
                "byte_offset": 17,
                "byte_size": 2,
            },
            {
                "ordinal": 0,
                "name": "block0.layer0.layer",
                "container_path": "../containers/all.blob",
                "byte_offset": 11,
                "byte_size": 3,
                "sha256": hashlib.sha256(payloads["block0.layer0.layer"]).hexdigest(),
            },
            {
                "ordinal": 1,
                "name": "block1.layer0.layer",
                "container_path": "../containers/all.blob",
                "byte_offset": 6,
                "byte_size": 5,
            },
        ]
    }
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("private/containers/all.blob", combined)
        archive.writestr("private/metadata/tensor_inventory.json", json.dumps(inventory))

    output = tmp_path / "weights.bin"
    report = execute(
        archive_path,
        contract,
        output,
        offset_basis="absolute",
        forced_inventory="private/metadata/tensor_inventory.json",
        expected_private_sha256=None,
        dry_run=False,
        report_path=None,
    )
    assert report["verified"] is True
    assert report["inventory_candidates"][0]["exact_contract_matches"] == 3
    assert read_index(output).offset_basis == "absolute"
    assert _contents(output) == payloads


def test_csv_inventory_is_discovered(tmp_path: Path) -> None:
    contract = _contract(tmp_path / "contract.json")
    archive_path = tmp_path / "private.zip"
    payloads = _payloads()
    with zipfile.ZipFile(archive_path, "w") as archive:
        for name, data in payloads.items():
            archive.writestr(f"data/{name}.bin", data)
        archive.writestr(
            "metadata/inventory.csv",
            "tensor_name,file_path,byte_size\n"
            "block0.layer0.layer,../data/block0.layer0.layer.bin,3\n"
            "block1.layer0.layer,../data/block1.layer0.layer.bin,5\n"
            "block70.layer0.blend_scale,../data/block70.layer0.blend_scale.bin,2\n",
        )
    report = execute(
        archive_path,
        contract,
        tmp_path / "unused.bin",
        offset_basis="relative",
        forced_inventory=None,
        expected_private_sha256=None,
        dry_run=True,
        report_path=None,
    )
    assert report["verified"] is True
    assert report["dry_run"] is True
    assert report["resolved_count"] == 3
    assert not (tmp_path / "unused.bin").exists()


def test_nonidentical_duplicate_members_are_rejected(tmp_path: Path) -> None:
    contract = _contract(tmp_path / "contract.json")
    archive_path = tmp_path / "private.zip"
    payloads = _payloads()
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("a/block0.layer0.layer.bin", b"abc")
        archive.writestr("b/block0.layer0.layer.bin", b"xyz")
        archive.writestr("block1.layer0.layer.bin", payloads["block1.layer0.layer"])
        archive.writestr("block70.layer0.blend_scale.bin", payloads["block70.layer0.blend_scale"])
    with pytest.raises(MappingError, match="ambiguous non-identical"):
        execute(
            archive_path,
            contract,
            tmp_path / "weights.bin",
            offset_basis="relative",
            forced_inventory=None,
            expected_private_sha256=None,
            dry_run=False,
            report_path=None,
        )


def test_wrong_size_is_rejected(tmp_path: Path) -> None:
    contract = _contract(tmp_path / "contract.json")
    archive_path = tmp_path / "private.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("block0.layer0.layer.bin", b"wrong")
        archive.writestr("block1.layer0.layer.bin", b"12345")
        archive.writestr("block70.layer0.blend_scale.bin", b"xy")
    with pytest.raises(MappingError, match="resolved 2/3"):
        execute(
            archive_path,
            contract,
            tmp_path / "weights.bin",
            offset_basis="relative",
            forced_inventory=None,
            expected_private_sha256=None,
            dry_run=True,
            report_path=None,
        )


def test_private_zip_hash_gate(tmp_path: Path) -> None:
    contract = _contract(tmp_path / "contract.json")
    archive_path = tmp_path / "private.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for name, data in _payloads().items():
            archive.writestr(name, data)
    with pytest.raises(MappingError, match="SHA-256 mismatch"):
        execute(
            archive_path,
            contract,
            tmp_path / "weights.bin",
            offset_basis="relative",
            forced_inventory=None,
            expected_private_sha256="0" * 64,
            dry_run=True,
            report_path=None,
        )
