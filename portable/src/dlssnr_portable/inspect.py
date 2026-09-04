from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Sequence

from .ir import IRValidationError, load_model
from .weights import WeightArchiveError, WeightArchiveReader


def inspect_model(model_path: Path, *, verify_weights: bool = True) -> dict[str, object]:
    model = load_model(model_path)
    graph = model.graph
    roles = Counter(tensor.role for tensor in graph.tensors)
    operators = Counter(node.op for node in graph.nodes)
    stored = [
        tensor for tensor in graph.tensors
        if tensor.role in {"weight", "constant"} and tensor.storage is not None
    ]

    archive_metadata = model.metadata.get("weight_archive")
    expected_file_hash = None
    if isinstance(archive_metadata, dict):
        value = archive_metadata.get("sha256")
        if isinstance(value, str):
            expected_file_hash = value

    weight_summary: dict[str, object] = {
        "declared_tensor_count": len(stored),
        "verified": False,
    }
    if stored and verify_weights:
        reader = WeightArchiveReader(
            model_path.parent,
            graph.tensors,
            verify_file_hash=expected_file_hash,
        )
        for name in reader.names():
            reader.read(name, logical=False, verify=True)
        weight_summary.update(
            {
                "verified": True,
                "file": str(reader.path),
                "file_size": reader.path.stat().st_size,
                "tensor_count": len(reader.names()),
            }
        )

    report: dict[str, object] = {
        "schema": model.schema,
        "graph": graph.name,
        "scope": graph.scope,
        "inputs": list(graph.inputs),
        "outputs": list(graph.outputs),
        "states": [
            {
                "name": state.name,
                "input": state.input_tensor,
                "output": state.output_tensor,
                "initial": state.initial,
                "reset_on": list(state.reset_on),
            }
            for state in graph.states
        ],
        "tensor_count": len(graph.tensors),
        "tensor_roles": dict(sorted(roles.items())),
        "node_count": len(graph.nodes),
        "operators": dict(sorted(operators.items())),
        "coverage": dict(model.coverage),
        "weights": weight_summary,
        "portable_complete": bool(
            model.coverage.get("complete")
            and graph.scope == "full_temporal_renderer"
            and bool(graph.states)
        ),
    }
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("--skip-weight-verification", action="store_true")
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv)
    try:
        report = inspect_model(
            args.model,
            verify_weights=not args.skip_weight_verification,
        )
        if args.require_complete and not report["portable_complete"]:
            raise ValueError("model is structurally valid but not a complete temporal renderer")
    except (
        OSError,
        ValueError,
        IRValidationError,
        WeightArchiveError,
        json.JSONDecodeError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        coverage = report["coverage"]
        implemented = coverage.get("implemented_blocks", "?") if isinstance(coverage, dict) else "?"
        total = coverage.get("total_blocks", "?") if isinstance(coverage, dict) else "?"
        print(f"graph: {report['graph']}")
        print(f"scope: {report['scope']}")
        print(f"nodes: {report['node_count']}")
        print(f"coverage: {implemented}/{total}")
        print(f"weights verified: {report['weights']['verified']}")
        print(f"portable complete: {report['portable_complete']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
