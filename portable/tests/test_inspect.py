from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

from dlssnr_portable.inspect import inspect_model
from dlssnr_portable.ir import GraphIR, ModelIR, Node, StorageRef, TensorSpec, save_model
from dlssnr_portable.weights import TensorPayload, WeightArchiveBuilder


def test_inspection_verifies_weights_and_reports_partial(tmp_path: Path) -> None:
    stored, archive = WeightArchiveBuilder().write(
        (TensorPayload("scale", np.ones((8,), dtype=np.float32), "f32", "C"),),
        tmp_path / "weights.bin",
    )
    model = ModelIR(
        graph=GraphIR(
            name="inspect-test",
            scope="operator_family",
            tensors=(
                TensorSpec("input", ("tokens", 8), "f32", "input", "NC"),
                stored[0].to_spec(),
                TensorSpec("output", ("tokens", 8), "f32", "output", "NC"),
            ),
            nodes=(Node("node", "Mul", ("input", "scale"), ("output",)),),
            inputs=("input",),
            outputs=("output",),
        ),
        metadata={"weight_archive": archive},
        coverage={"complete": False, "implemented_blocks": 1, "total_blocks": 71},
    )
    save_model(model, tmp_path / "model.json")
    report = inspect_model(tmp_path / "model.json")
    assert report["weights"]["verified"] is True
    assert report["portable_complete"] is False
    assert report["operators"] == {"Mul": 1}
