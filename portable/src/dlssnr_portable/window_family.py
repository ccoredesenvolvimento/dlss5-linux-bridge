from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from .canonicalize import apply_recipe
from .ir import GraphIR, ModelIR, Node, TensorSpec, save_model
from .ops.window_transformer import WindowTransformerWeights, run_window_transformer
from .weights import TensorPayload, WeightArchiveBuilder, WeightArchiveReader

WINDOW_FAMILIES: tuple[tuple[int, ...], ...] = (
    tuple(range(23, 31)),
    tuple(range(40, 48)),
)
WEIGHT_NAMES = (
    "gate",
    "value",
    "ffn_projection",
    "ffn_residual_scale",
    "qkv",
    "relative_bias",
    "logit_scale",
    "output_projection",
    "attention_residual_scale",
)


class WindowFamilyError(ValueError):
    pass


def build_window_family_model(
    block_records: Mapping[int, Mapping[str, bytes | np.ndarray]],
    recipe: Mapping[str, Any],
    output_directory: str | Path,
    *,
    weight_storage_dtype: str = "f16",
) -> ModelIR:
    expected_blocks = {block for family in WINDOW_FAMILIES for block in family}
    actual_blocks = set(block_records)
    if actual_blocks != expected_blocks:
        missing = sorted(expected_blocks - actual_blocks)
        extra = sorted(actual_blocks - expected_blocks)
        raise WindowFamilyError(f"block set mismatch; missing={missing}, extra={extra}")
    if weight_storage_dtype not in {"f16", "f32"}:
        raise WindowFamilyError("weight_storage_dtype must be f16 or f32")

    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    recipes = recipe.get("outputs")
    operator = recipe.get("operator")
    if not isinstance(recipes, Sequence) or not isinstance(operator, Mapping):
        raise WindowFamilyError("recipe must contain outputs and operator")

    payloads: list[TensorPayload] = []
    for block in sorted(expected_blocks):
        canonical = apply_recipe(block_records[block], recipes)
        names = {item.name for item in canonical}
        if names != set(WEIGHT_NAMES):
            raise WindowFamilyError(
                f"block {block} canonical tensors mismatch: {sorted(names)}"
            )
        for item in canonical:
            storage_dtype = "f32" if item.name == "logit_scale" else weight_storage_dtype
            payloads.append(
                TensorPayload(
                    name=f"block{block}.{item.name}",
                    array=item.array,
                    storage_dtype=storage_dtype,
                    logical_dtype="f32",
                    layout=item.layout,
                )
            )

    stored, hashes = WeightArchiveBuilder(filename="weights.bin").write(
        payloads, output / "weights.bin"
    )
    tensors: list[TensorSpec] = [item.to_spec() for item in stored]
    nodes: list[Node] = []
    graph_inputs: list[str] = []
    graph_outputs: list[str] = []

    for family in WINDOW_FAMILIES:
        family_name = f"blocks{family[0]}_{family[-1]}"
        input_name = f"{family_name}.input"
        graph_inputs.append(input_name)
        tensors.append(TensorSpec(input_name, ("tokens", 512), "f32", "input", "NC"))
        current = input_name
        for index, block in enumerate(family):
            output_name = f"block{block}.output"
            final = index == len(family) - 1
            tensors.append(
                TensorSpec(
                    output_name,
                    ("tokens", 512),
                    "f32",
                    "output" if final else "activation",
                    "NC",
                )
            )
            weight_inputs = tuple(f"block{block}.{name}" for name in WEIGHT_NAMES)
            nodes.append(
                Node(
                    id=f"block{block}",
                    op="GatedWindowTransformer",
                    inputs=(current, *weight_inputs),
                    outputs=(output_name,),
                    attrs={
                        "channels": int(operator["channels"]),
                        "window_tokens": int(operator["window_tokens"]),
                        "head_count": int(operator["head_count"]),
                        "head_width": int(operator["head_width"]),
                        "activation_coefficients": list(
                            operator["activation"]["coefficients"]
                        ),
                    },
                    evidence={
                        "block": block,
                        "status": "canonical-record-shape-closed",
                    },
                )
            )
            current = output_name
        graph_outputs.append(current)

    model = ModelIR(
        graph=GraphIR(
            name="dlssnr-window-transformer-families",
            scope="operator_family",
            tensors=tuple(tensors),
            nodes=tuple(nodes),
            inputs=tuple(graph_inputs),
            outputs=tuple(graph_outputs),
        ),
        metadata={
            "source": "user-supplied-private-evidence",
            "weight_archive": hashes,
            "inference_dependencies": ["model.json", "weights.bin"],
            "forbidden_runtime_dependencies": [
                "captured-activations",
                "vendor-runtime-dll",
                "cubin",
                "sass",
                "hip-code-object",
            ],
        },
        coverage={
            "complete": False,
            "implemented_blocks": len(expected_blocks),
            "total_blocks": 71,
            "blocks": sorted(expected_blocks),
            "missing_blocks": [
                block for block in range(71) if block not in expected_blocks
            ],
            "png_to_png": False,
            "temporal_state": False,
        },
    )
    save_model(model, output / "model.json")
    (output / "hashes.json").write_text(
        json.dumps(hashes, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return model


def run_window_family_model(
    model: ModelIR,
    model_directory: str | Path,
    inputs: Mapping[str, np.ndarray],
) -> dict[str, np.ndarray]:
    model.validate()
    if model.graph.name != "dlssnr-window-transformer-families":
        raise WindowFamilyError(f"unsupported graph {model.graph.name!r}")
    reader = WeightArchiveReader(
        model_directory,
        model.graph.tensors,
        verify_file_hash=_weight_file_hash(model),
    )
    values: dict[str, np.ndarray] = {
        name: np.asarray(value, dtype=np.float32) for name, value in inputs.items()
    }
    missing_inputs = [name for name in model.graph.inputs if name not in values]
    if missing_inputs:
        raise WindowFamilyError(f"missing graph inputs: {missing_inputs}")

    for node in model.graph.nodes:
        if node.op != "GatedWindowTransformer":
            raise WindowFamilyError(f"unsupported operator {node.op!r}")
        feature = values[node.inputs[0]]
        prefix = node.id + "."
        arrays = {name: reader.read(prefix + name) for name in WEIGHT_NAMES}
        weights = WindowTransformerWeights(**arrays)
        coefficients = tuple(float(item) for item in node.attrs["activation_coefficients"])
        result = run_window_transformer(
            feature,
            weights,
            window_tokens=int(node.attrs["window_tokens"]),
            head_count=int(node.attrs["head_count"]),
            head_width=int(node.attrs["head_width"]),
            activation_coefficients=coefficients,  # type: ignore[arg-type]
        )
        values[node.outputs[0]] = result
    return {name: values[name] for name in model.graph.outputs}


def _weight_file_hash(model: ModelIR) -> str | None:
    archive = model.metadata.get("weight_archive")
    if isinstance(archive, Mapping):
        value = archive.get("sha256")
        if isinstance(value, str):
            return value
    return None
