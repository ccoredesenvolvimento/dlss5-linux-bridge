from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Sequence

import numpy as np

from .ir import load_model
from .torch_backend import build_window_family_module, require_torch


def export_window_family_onnx(
    model_directory: Path,
    output: Path,
    *,
    tokens: int,
    opset: int = 18,
    validate_runtime: bool = True,
) -> dict[str, object]:
    if tokens <= 0 or tokens % 64:
        raise ValueError("tokens must be a positive multiple of 64")
    model = load_model(model_directory / "model.json")
    if model.graph.name != "dlssnr-window-transformer-families":
        raise ValueError(f"unsupported graph for this exporter: {model.graph.name}")
    if model.coverage.get("complete") is True:
        raise ValueError("operator-family exporter received a graph marked complete")

    torch, _ = require_torch()
    module = build_window_family_module(model, str(model_directory))
    generator = torch.Generator(device="cpu").manual_seed(0)
    sample_inputs = tuple(
        torch.randn((tokens, 512), generator=generator, dtype=torch.float32)
        for _ in model.graph.inputs
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    torch.onnx.export(
        module,
        sample_inputs,
        str(output),
        input_names=list(model.graph.inputs),
        output_names=list(model.graph.outputs),
        opset_version=opset,
        do_constant_folding=True,
        export_params=True,
        dynamic_axes=None,
    )

    try:
        import onnx
    except ImportError as exc:
        raise RuntimeError("install dlssnr-portable[onnx] to validate ONNX") from exc
    graph = onnx.load(str(output), load_external_data=True)
    onnx.checker.check_model(graph, full_check=True)

    with torch.no_grad():
        torch_outputs = module(*sample_inputs)
    if not isinstance(torch_outputs, tuple):
        torch_outputs = (torch_outputs,)

    report: dict[str, object] = {
        "schema": "dlssnr-portable-onnx-validation-v1",
        "graph": model.graph.name,
        "coverage_complete": model.coverage.get("complete"),
        "tokens": tokens,
        "opset": opset,
        "onnx_path": str(output),
        "onnx_size": output.stat().st_size,
        "onnx_checker": True,
        "runtime_validated": False,
        "outputs": [],
    }
    if validate_runtime:
        try:
            import onnxruntime as ort
        except ImportError as exc:
            raise RuntimeError("onnxruntime is required for numerical validation") from exc
        session = ort.InferenceSession(str(output), providers=["CPUExecutionProvider"])
        feeds = {
            name: tensor.detach().cpu().numpy()
            for name, tensor in zip(model.graph.inputs, sample_inputs, strict=True)
        }
        ort_outputs = session.run(list(model.graph.outputs), feeds)
        metrics: list[dict[str, object]] = []
        for name, expected_tensor, actual in zip(
            model.graph.outputs, torch_outputs, ort_outputs, strict=True
        ):
            expected = expected_tensor.detach().cpu().numpy().astype(np.float32)
            actual_array = np.asarray(actual, dtype=np.float32)
            difference = actual_array - expected
            expected_flat = expected.reshape(-1).astype(np.float64)
            actual_flat = actual_array.reshape(-1).astype(np.float64)
            denominator = float(np.linalg.norm(expected_flat) * np.linalg.norm(actual_flat))
            cosine = (
                float(np.dot(expected_flat, actual_flat) / denominator)
                if denominator > 0.0
                else 1.0
            )
            metrics.append(
                {
                    "name": name,
                    "shape": list(actual_array.shape),
                    "finite": bool(np.isfinite(actual_array).all()),
                    "max_abs": float(np.max(np.abs(difference))),
                    "rmse": float(math.sqrt(float(np.mean(np.square(difference, dtype=np.float64))))),
                    "cosine": cosine,
                }
            )
        report["outputs"] = metrics
        report["runtime_validated"] = True
        report["passed"] = all(
            item["finite"]
            and float(item["max_abs"]) <= 2e-4
            and float(item["cosine"]) >= 0.99999
            for item in metrics
        )
        if not report["passed"]:
            raise RuntimeError(f"ONNX numerical gate failed: {metrics}")
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model_directory", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--tokens", type=int, required=True)
    parser.add_argument("--opset", type=int, default=18)
    parser.add_argument("--skip-runtime-validation", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    try:
        report = export_window_family_onnx(
            args.model_directory,
            args.output,
            tokens=args.tokens,
            opset=args.opset,
            validate_runtime=not args.skip_runtime_validation,
        )
    except (OSError, ValueError, RuntimeError, ImportError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
