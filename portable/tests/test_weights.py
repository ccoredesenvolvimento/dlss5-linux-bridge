from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from dlssnr_portable.weights import (
    TensorPayload,
    WeightArchiveBuilder,
    WeightArchiveError,
    WeightArchiveReader,
    decode_e4m3fn,
    encode_e4m3fn,
)


def test_archive_round_trip_and_alignment(tmp_path: Path) -> None:
    payloads = (
        TensorPayload("a", np.arange(15, dtype=np.float32).reshape(3, 5), "f16", "RC"),
        TensorPayload("b", np.linspace(-1, 1, 12, dtype=np.float32), "f32", "C"),
    )
    path = tmp_path / "weights.bin"
    stored, manifest = WeightArchiveBuilder(alignment=64).write(payloads, path)
    specs = tuple(item.to_spec() for item in stored)
    assert all(item.storage.offset % 64 == 0 for item in stored)
    assert manifest["tensor_count"] == 2

    reader = WeightArchiveReader(tmp_path, specs, verify_file_hash=manifest["sha256"])
    np.testing.assert_allclose(reader.read("a"), payloads[0].array, atol=5e-3, rtol=5e-3)
    np.testing.assert_array_equal(reader.read("b"), payloads[1].array)
    assert reader.mmap("a").shape == (3, 5)


def test_hash_mismatch_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "weights.bin"
    stored, _ = WeightArchiveBuilder().write(
        (TensorPayload("a", np.arange(8, dtype=np.float32), "f32", "C"),),
        path,
    )
    raw = bytearray(path.read_bytes())
    raw[-1] ^= 0x01
    path.write_bytes(raw)
    reader = WeightArchiveReader(tmp_path, (stored[0].to_spec(),))
    with pytest.raises(WeightArchiveError, match="SHA-256 mismatch"):
        reader.read("a")


def test_e4m3fn_reference_conversion() -> None:
    values = np.array(
        [-448.0, -2.0, -0.0, 0.0, 2.0**-9, 1.0, 1.5, 448.0],
        dtype=np.float32,
    )
    encoded = encode_e4m3fn(values)
    decoded = decode_e4m3fn(encoded)
    np.testing.assert_allclose(decoded, values, atol=2e-3, rtol=0.08)


def test_e4m3fn_nan_code() -> None:
    decoded = decode_e4m3fn(np.array([0x7F, 0xFF], dtype=np.uint8))
    assert np.isnan(decoded).all()
