from __future__ import annotations

from typing import Mapping, Sequence

from .ir import ModelIR
from .weights import WeightArchiveReader
from .window_family import WEIGHT_NAMES, WINDOW_FAMILIES


def require_torch():
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError(
            "the Torch backend is optional; install dlssnr-portable[torch]"
        ) from exc
    return torch, nn


def build_window_family_module(
    model: ModelIR,
    model_directory: str,
):
    torch, nn = require_torch()
    model.validate()
    reader = WeightArchiveReader(
        model_directory,
        model.graph.tensors,
        verify_file_hash=_weight_file_hash(model),
    )

    class WindowBlock(nn.Module):
        def __init__(self, prefix: str, attrs: Mapping[str, object]) -> None:
            super().__init__()
            for name in WEIGHT_NAMES:
                array = reader.read(prefix + name)
                self.register_buffer(name, torch.from_numpy(array.astype("float32")))
            self.window_tokens = int(attrs["window_tokens"])
            self.head_count = int(attrs["head_count"])
            self.head_width = int(attrs["head_width"])
            coefficients = attrs["activation_coefficients"]
            if not isinstance(coefficients, Sequence) or len(coefficients) != 3:
                raise ValueError("activation_coefficients must contain three values")
            self.activation_a = float(coefficients[0])
            self.activation_b = float(coefficients[1])
            self.activation_c = float(coefficients[2])

        def forward(self, feature):
            clipped = torch.clamp(feature @ self.gate.transpose(0, 1), -4.0, 4.0)
            activated = clipped * (
                self.activation_a
                + clipped * (self.activation_b - self.activation_c * torch.abs(clipped))
            )
            hidden = activated * (feature @ self.value.transpose(0, 1))
            residual = hidden @ self.ffn_projection.transpose(0, 1)
            residual = residual + feature * self.ffn_residual_scale

            channels = self.qkv.shape[1]
            projected = self.qkv.shape[2]
            qkv_matrix = self.qkv.permute(1, 0, 2).reshape(channels, 3 * projected)
            qkv = (residual @ qkv_matrix).reshape(feature.shape[0], 3, projected)
            qkv = qkv.permute(1, 0, 2)
            windows = feature.shape[0] // self.window_tokens
            q = qkv[0].reshape(
                windows, self.window_tokens, self.head_count, self.head_width
            ).permute(0, 2, 1, 3)
            k = qkv[1].reshape(
                windows, self.window_tokens, self.head_count, self.head_width
            ).permute(0, 2, 1, 3)
            v = qkv[2].reshape(
                windows, self.window_tokens, self.head_count, self.head_width
            ).permute(0, 2, 1, 3)
            q = q / torch.clamp(torch.linalg.vector_norm(q, dim=-1, keepdim=True), min=1e-12)
            k = k / torch.clamp(torch.linalg.vector_norm(k, dim=-1, keepdim=True), min=1e-12)
            logits = torch.matmul(q, k.transpose(-2, -1))
            logits = logits * self.logit_scale.reshape(1, self.head_count, 1, 1)
            logits = logits + self.relative_bias.reshape(
                1, self.head_count, self.window_tokens, self.window_tokens
            )
            attention = torch.softmax(logits, dim=-1)
            attended = torch.matmul(attention, v).permute(0, 2, 1, 3)
            attended = attended.reshape(feature.shape[0], projected)
            output = attended @ self.output_projection.transpose(0, 1)
            return output + residual * self.attention_residual_scale

    class WindowFamilyModel(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            attrs = {node.id: node.attrs for node in model.graph.nodes}
            self.family_a = nn.ModuleList(
                [WindowBlock(f"block{block}.", attrs[f"block{block}"]) for block in WINDOW_FAMILIES[0]]
            )
            self.family_b = nn.ModuleList(
                [WindowBlock(f"block{block}.", attrs[f"block{block}"]) for block in WINDOW_FAMILIES[1]]
            )

        def forward(self, blocks23_30_input, blocks40_47_input):
            first = blocks23_30_input
            for block in self.family_a:
                first = block(first)
            second = blocks40_47_input
            for block in self.family_b:
                second = block(second)
            return first, second

    return WindowFamilyModel().eval()


def _weight_file_hash(model: ModelIR) -> str | None:
    archive = model.metadata.get("weight_archive")
    if isinstance(archive, Mapping):
        value = archive.get("sha256")
        if isinstance(value, str):
            return value
    return None
