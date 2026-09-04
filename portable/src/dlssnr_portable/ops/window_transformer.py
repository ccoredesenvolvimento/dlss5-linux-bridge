from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class WindowTransformerWeights:
    gate: np.ndarray
    value: np.ndarray
    ffn_projection: np.ndarray
    ffn_residual_scale: np.ndarray
    qkv: np.ndarray
    relative_bias: np.ndarray
    logit_scale: np.ndarray
    output_projection: np.ndarray
    attention_residual_scale: np.ndarray


def polynomial_activation(x: np.ndarray, coefficients: tuple[float, float, float]) -> np.ndarray:
    a, b, c = coefficients
    value = np.clip(np.asarray(x, dtype=np.float32), -4.0, 4.0)
    return value * (np.float32(a) + value * (np.float32(b) - np.float32(c) * np.abs(value)))


def stable_softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    value = np.asarray(x, dtype=np.float32)
    shifted = value - np.max(value, axis=axis, keepdims=True)
    numerator = np.exp(shifted).astype(np.float32)
    return numerator / np.sum(numerator, axis=axis, keepdims=True, dtype=np.float32)


def run_window_transformer(
    feature: np.ndarray,
    weights: WindowTransformerWeights,
    *,
    window_tokens: int,
    head_count: int,
    head_width: int,
    activation_coefficients: tuple[float, float, float],
    epsilon: float = 1e-12,
) -> np.ndarray:
    value = np.asarray(feature, dtype=np.float32)
    if value.ndim != 2:
        raise ValueError("feature must be a two-dimensional [tokens, channels] tensor")
    tokens, channels = value.shape
    if tokens == 0 or tokens % window_tokens:
        raise ValueError("token count must be a positive multiple of window_tokens")
    projected_width = head_count * head_width

    expected = {
        "gate": (weights.gate.shape[0], channels),
        "value": (weights.gate.shape[0], channels),
        "ffn_projection": (channels, weights.gate.shape[0]),
        "ffn_residual_scale": (channels,),
        "qkv": (3, channels, projected_width),
        "relative_bias": (head_count, window_tokens, window_tokens),
        "logit_scale": (head_count,),
        "output_projection": (channels, projected_width),
        "attention_residual_scale": (channels,),
    }
    for name, shape in expected.items():
        array = np.asarray(getattr(weights, name))
        if array.shape != shape:
            raise ValueError(f"{name}: expected {shape}, got {array.shape}")
        if not np.isfinite(array).all():
            raise ValueError(f"{name} contains non-finite values")

    hidden = polynomial_activation(
        value @ np.asarray(weights.gate, dtype=np.float32).T,
        activation_coefficients,
    )
    hidden *= value @ np.asarray(weights.value, dtype=np.float32).T
    residual = hidden @ np.asarray(weights.ffn_projection, dtype=np.float32).T
    residual += value * np.asarray(weights.ffn_residual_scale, dtype=np.float32)

    qkv = np.einsum(
        "nc,kcd->knd",
        residual,
        np.asarray(weights.qkv, dtype=np.float32),
        optimize=True,
    )
    windows = tokens // window_tokens
    q, k, v = (
        tensor.reshape(windows, window_tokens, head_count, head_width).transpose(0, 2, 1, 3)
        for tensor in qkv
    )
    q /= np.maximum(np.linalg.norm(q, axis=-1, keepdims=True), epsilon)
    k /= np.maximum(np.linalg.norm(k, axis=-1, keepdims=True), epsilon)
    logits = np.einsum("whqd,whkd->whqk", q, k, optimize=True)
    logits *= np.asarray(weights.logit_scale, dtype=np.float32).reshape(1, head_count, 1, 1)
    logits += np.asarray(weights.relative_bias, dtype=np.float32).reshape(
        1, head_count, window_tokens, window_tokens
    )
    attention = stable_softmax(logits)
    attended = np.einsum("whqk,whkd->wqhd", attention, v, optimize=True).reshape(
        tokens, projected_width
    )
    output = attended @ np.asarray(weights.output_projection, dtype=np.float32).T
    output += residual * np.asarray(weights.attention_residual_scale, dtype=np.float32)
    if not np.isfinite(output).all():
        raise FloatingPointError("operator produced non-finite output")
    return np.ascontiguousarray(output, dtype=np.float32)
