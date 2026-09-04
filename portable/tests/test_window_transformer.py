from __future__ import annotations

import numpy as np
import pytest

from dlssnr_portable.ops.window_transformer import (
    WindowTransformerWeights,
    run_window_transformer,
    stable_softmax,
)


def weights(seed: int = 7) -> WindowTransformerWeights:
    rng = np.random.default_rng(seed)
    channels = 8
    hidden = 4
    heads = 2
    width = 2
    window = 4

    def random(shape: tuple[int, ...], scale: float = 0.05) -> np.ndarray:
        return (rng.standard_normal(shape) * scale).astype(np.float32)

    return WindowTransformerWeights(
        gate=random((hidden, channels)),
        value=random((hidden, channels)),
        ffn_projection=random((channels, hidden)),
        ffn_residual_scale=np.ones((channels,), dtype=np.float32),
        qkv=random((3, channels, heads * width)),
        relative_bias=random((heads, window, window), 0.01),
        logit_scale=np.ones((heads,), dtype=np.float32),
        output_projection=random((channels, heads * width)),
        attention_residual_scale=np.ones((channels,), dtype=np.float32),
    )


def test_softmax_is_normalized() -> None:
    rng = np.random.default_rng(1)
    value = rng.standard_normal((3, 5, 7)).astype(np.float32) * 20
    output = stable_softmax(value)
    np.testing.assert_allclose(output.sum(axis=-1), 1.0, atol=1e-6)
    assert np.isfinite(output).all()


def test_operator_is_deterministic_and_input_sensitive() -> None:
    rng = np.random.default_rng(2)
    feature = rng.standard_normal((8, 8)).astype(np.float32)
    model_weights = weights()
    first = run_window_transformer(
        feature,
        model_weights,
        window_tokens=4,
        head_count=2,
        head_width=2,
        activation_coefficients=(0.89453125, 0.447265625, 0.055908203125),
    )
    second = run_window_transformer(
        feature.copy(),
        model_weights,
        window_tokens=4,
        head_count=2,
        head_width=2,
        activation_coefficients=(0.89453125, 0.447265625, 0.055908203125),
    )
    np.testing.assert_array_equal(first, second)
    assert first.shape == feature.shape
    changed = feature.copy()
    changed[0, 0] += 0.5
    third = run_window_transformer(
        changed,
        model_weights,
        window_tokens=4,
        head_count=2,
        head_width=2,
        activation_coefficients=(0.89453125, 0.447265625, 0.055908203125),
    )
    assert not np.array_equal(first, third)


def test_rejects_non_window_aligned_tokens() -> None:
    with pytest.raises(ValueError, match="multiple"):
        run_window_transformer(
            np.zeros((7, 8), dtype=np.float32),
            weights(),
            window_tokens=4,
            head_count=2,
            head_width=2,
            activation_coefficients=(1.0, 0.0, 0.0),
        )
