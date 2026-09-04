from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from dlssnr_portable.canonicalize import (
    CanonicalizationError,
    OutputRecipe,
    apply_recipe,
)


def test_element_slice_reshape_and_transpose() -> None:
    source = np.arange(24, dtype="<f2")
    outputs = apply_recipe(
        {"record": source},
        (
            OutputRecipe(
                name="matrix",
                source="record",
                source_dtype="<f2",
                element_start=0,
                element_count=24,
                shape=(2, 3, 4),
                transpose=(0, 2, 1),
                output_dtype="<f4",
                layout="A_C_B",
            ),
        ),
    )
    assert outputs[0].array.shape == (2, 4, 3)
    assert outputs[0].array.dtype == np.dtype("<f4")
    np.testing.assert_array_equal(outputs[0].array, source.reshape(2, 3, 4).transpose(0, 2, 1))


def test_byte_reinterpretation() -> None:
    scales = np.array([0.5, 1.0, 2.0, 4.0], dtype="<f4")
    record = b"prefix00" + scales.tobytes() + b"suffix"
    outputs = apply_recipe(
        {"record": record},
        (
            OutputRecipe(
                name="scales",
                source="record",
                source_dtype="<f2",
                byte_start=8,
                byte_count=16,
                reinterpret_dtype="<f4",
                shape=(4,),
                layout="C",
            ),
        ),
    )
    np.testing.assert_array_equal(outputs[0].array, scales)


def test_production_recipe_closes_expected_shapes() -> None:
    recipe_path = Path(__file__).parents[1] / "recipes" / "window-transformer-512-v1.json"
    recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
    records = {
        name: bytes(spec["nbytes"])
        for name, spec in recipe["source_records"].items()
    }
    outputs = apply_recipe(records, recipe["outputs"])
    actual = {item.name: item.array.shape for item in outputs}
    assert actual == {
        "gate": (256, 512),
        "value": (256, 512),
        "ffn_projection": (512, 256),
        "ffn_residual_scale": (512,),
        "qkv": (3, 512, 256),
        "relative_bias": (16, 64, 64),
        "logit_scale": (16,),
        "output_projection": (512, 256),
        "attention_residual_scale": (512,),
    }


def test_out_of_range_slice_is_rejected() -> None:
    with pytest.raises(CanonicalizationError, match="outside"):
        apply_recipe(
            {"record": bytes(8)},
            (
                OutputRecipe(
                    name="bad",
                    source="record",
                    source_dtype="<f2",
                    byte_start=4,
                    byte_count=16,
                    shape=(8,),
                ),
            ),
        )
