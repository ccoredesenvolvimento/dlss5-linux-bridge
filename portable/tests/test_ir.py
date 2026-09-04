from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from dlssnr_portable.ir import (
    GraphIR,
    IRValidationError,
    ModelIR,
    Node,
    StorageRef,
    TensorSpec,
    load_model,
    save_model,
)


def weight(name: str, offset: int, values: int) -> TensorSpec:
    raw = b"\0" * (values * 2)
    return TensorSpec(
        name=name,
        shape=(values,),
        dtype="f16",
        role="weight",
        layout="C",
        storage=StorageRef(
            file="weights.bin",
            offset=offset,
            nbytes=len(raw),
            sha256=hashlib.sha256(raw).hexdigest(),
            alignment=64,
        ),
    )


def valid_model() -> ModelIR:
    graph = GraphIR(
        name="test-operator",
        scope="operator_family",
        tensors=(
            TensorSpec("input", ("tokens", 8), "f32", "input", "NC"),
            weight("scale", 0, 8),
            TensorSpec("output", ("tokens", 8), "f32", "output", "NC"),
        ),
        nodes=(Node("scale-node", "Mul", ("input", "scale"), ("output",)),),
        inputs=("input",),
        outputs=("output",),
    )
    return ModelIR(
        graph=graph,
        metadata={"source": "unit-test"},
        coverage={"complete": False, "implemented_blocks": 1, "total_blocks": 71},
    )


def test_round_trip(tmp_path: Path) -> None:
    model = valid_model()
    path = tmp_path / "model.json"
    save_model(model, path)
    restored = load_model(path)
    assert restored.to_dict() == model.to_dict()


def test_rejects_missing_input() -> None:
    model = valid_model()
    bad_graph = GraphIR(
        name=model.graph.name,
        scope=model.graph.scope,
        tensors=model.graph.tensors,
        nodes=(Node("bad", "Mul", ("missing", "scale"), ("output",)),),
        inputs=model.graph.inputs,
        outputs=model.graph.outputs,
    )
    with pytest.raises(IRValidationError, match="unknown input"):
        ModelIR(
            graph=bad_graph,
            metadata=model.metadata,
            coverage=model.coverage,
        ).validate()


def test_rejects_overlap() -> None:
    graph = GraphIR(
        name="overlap",
        scope="operator_family",
        tensors=(
            TensorSpec("input", (1,), "f32", "input", "C"),
            weight("a", 0, 64),
            weight("b", 64, 64),
            TensorSpec("output", (1,), "f32", "output", "C"),
        ),
        nodes=(Node("node", "Add", ("input", "a"), ("output",)),),
        inputs=("input",),
        outputs=("output",),
    )
    with pytest.raises(IRValidationError, match="overlapping storage"):
        ModelIR(
            graph=graph,
            metadata={},
            coverage={"complete": False},
        ).validate()


def test_complete_requires_full_temporal_scope() -> None:
    model = valid_model()
    with pytest.raises(IRValidationError, match="cannot be complete"):
        ModelIR(
            graph=model.graph,
            metadata=model.metadata,
            coverage={"complete": True, "implemented_blocks": 71, "total_blocks": 71},
        ).validate()
