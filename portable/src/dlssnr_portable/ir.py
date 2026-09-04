from __future__ import annotations

import dataclasses
import json
import re
from pathlib import Path
from typing import Any, Iterable, Literal, Mapping, Sequence, TypeAlias

Dim: TypeAlias = int | str
DType = Literal["f32", "f16", "e4m3fn", "i32", "u32", "u8", "bool"]
TensorRole = Literal["input", "output", "state", "weight", "constant", "activation"]
Scope = Literal["operator_family", "full_temporal_renderer"]

SCHEMA = "dlssnr-portable-ir-v1"
_IDENTIFIER = re.compile(r"^[A-Za-z0-9_.:/-]+$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_DTYPE_BYTES: dict[str, int] = {
    "f32": 4,
    "f16": 2,
    "e4m3fn": 1,
    "i32": 4,
    "u32": 4,
    "u8": 1,
    "bool": 1,
}


class IRValidationError(ValueError):
    pass


@dataclasses.dataclass(frozen=True, slots=True)
class StorageRef:
    file: str
    offset: int
    nbytes: int
    sha256: str
    encoding: str = "raw-little-endian"
    alignment: int = 64

    def validate(self) -> None:
        if not self.file or Path(self.file).is_absolute() or ".." in Path(self.file).parts:
            raise IRValidationError(f"unsafe storage file: {self.file!r}")
        if self.offset < 0 or self.nbytes < 0:
            raise IRValidationError("storage offset/nbytes must be non-negative")
        if self.alignment <= 0 or self.alignment & (self.alignment - 1):
            raise IRValidationError("storage alignment must be a positive power of two")
        if self.offset % self.alignment:
            raise IRValidationError(
                f"storage offset {self.offset} is not aligned to {self.alignment}"
            )
        if not _SHA256.fullmatch(self.sha256):
            raise IRValidationError(f"invalid SHA-256: {self.sha256!r}")
        if not self.encoding:
            raise IRValidationError("storage encoding must not be empty")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "StorageRef":
        return cls(
            file=str(value["file"]),
            offset=int(value["offset"]),
            nbytes=int(value["nbytes"]),
            sha256=str(value["sha256"]).lower(),
            encoding=str(value.get("encoding", "raw-little-endian")),
            alignment=int(value.get("alignment", 64)),
        )


@dataclasses.dataclass(frozen=True, slots=True)
class TensorSpec:
    name: str
    shape: tuple[Dim, ...]
    dtype: DType
    role: TensorRole
    layout: str
    storage: StorageRef | None = None
    logical_dtype: DType | None = None
    description: str | None = None

    def validate(self) -> None:
        _validate_name(self.name, "tensor")
        if not self.shape:
            raise IRValidationError(f"tensor {self.name!r} has no dimensions")
        for dimension in self.shape:
            if isinstance(dimension, bool):
                raise IRValidationError(f"invalid boolean dimension in {self.name!r}")
            if isinstance(dimension, int):
                if dimension <= 0:
                    raise IRValidationError(
                        f"tensor {self.name!r} has non-positive dimension {dimension}"
                    )
            elif isinstance(dimension, str):
                _validate_name(dimension, "symbolic dimension")
            else:
                raise IRValidationError(
                    f"tensor {self.name!r} has unsupported dimension {dimension!r}"
                )
        if self.dtype not in _DTYPE_BYTES:
            raise IRValidationError(f"unsupported dtype {self.dtype!r}")
        if self.logical_dtype is not None and self.logical_dtype not in _DTYPE_BYTES:
            raise IRValidationError(f"unsupported logical dtype {self.logical_dtype!r}")
        if self.role in {"weight", "constant"} and self.storage is None:
            raise IRValidationError(f"stored tensor {self.name!r} has no storage reference")
        if self.role not in {"weight", "constant"} and self.storage is not None:
            raise IRValidationError(
                f"non-stored tensor {self.name!r} unexpectedly references weights.bin"
            )
        if not self.layout:
            raise IRValidationError(f"tensor {self.name!r} has no layout")
        if self.storage is not None:
            self.storage.validate()
            element_count = _static_element_count(self.shape)
            if element_count is not None:
                required = element_count * _DTYPE_BYTES[self.dtype]
                if self.storage.nbytes != required:
                    raise IRValidationError(
                        f"tensor {self.name!r} requires {required} bytes for "
                        f"{self.dtype}{self.shape}, storage declares {self.storage.nbytes}"
                    )

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "TensorSpec":
        storage_value = value.get("storage")
        return cls(
            name=str(value["name"]),
            shape=tuple(value["shape"]),
            dtype=str(value["dtype"]),  # type: ignore[arg-type]
            role=str(value["role"]),  # type: ignore[arg-type]
            layout=str(value["layout"]),
            storage=StorageRef.from_dict(storage_value)
            if isinstance(storage_value, Mapping)
            else None,
            logical_dtype=str(value["logical_dtype"])  # type: ignore[arg-type]
            if value.get("logical_dtype") is not None
            else None,
            description=str(value["description"])
            if value.get("description") is not None
            else None,
        )


@dataclasses.dataclass(frozen=True, slots=True)
class Node:
    id: str
    op: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    attrs: Mapping[str, Any] = dataclasses.field(default_factory=dict)
    evidence: Mapping[str, Any] = dataclasses.field(default_factory=dict)

    def validate(self) -> None:
        _validate_name(self.id, "node")
        _validate_name(self.op, "operator")
        if not self.inputs:
            raise IRValidationError(f"node {self.id!r} has no inputs")
        if not self.outputs:
            raise IRValidationError(f"node {self.id!r} has no outputs")
        for value in (*self.inputs, *self.outputs):
            _validate_name(value, "tensor reference")
        if len(set(self.outputs)) != len(self.outputs):
            raise IRValidationError(f"node {self.id!r} repeats an output")
        _validate_json_value(self.attrs, f"node {self.id} attrs")
        _validate_json_value(self.evidence, f"node {self.id} evidence")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Node":
        attrs = value.get("attrs", {})
        evidence = value.get("evidence", {})
        if not isinstance(attrs, Mapping) or not isinstance(evidence, Mapping):
            raise IRValidationError("node attrs/evidence must be objects")
        return cls(
            id=str(value["id"]),
            op=str(value["op"]),
            inputs=tuple(str(item) for item in value["inputs"]),
            outputs=tuple(str(item) for item in value["outputs"]),
            attrs=dict(attrs),
            evidence=dict(evidence),
        )


@dataclasses.dataclass(frozen=True, slots=True)
class StateEdge:
    name: str
    input_tensor: str
    output_tensor: str
    initial: Literal["zeros", "external", "first-frame"]
    reset_on: tuple[str, ...] = ()

    def validate(self) -> None:
        _validate_name(self.name, "state")
        _validate_name(self.input_tensor, "state input")
        _validate_name(self.output_tensor, "state output")
        if self.input_tensor == self.output_tensor:
            raise IRValidationError(f"state {self.name!r} aliases input and output")
        for condition in self.reset_on:
            if not condition:
                raise IRValidationError(f"state {self.name!r} has an empty reset condition")

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "StateEdge":
        return cls(
            name=str(value["name"]),
            input_tensor=str(value["input_tensor"]),
            output_tensor=str(value["output_tensor"]),
            initial=str(value["initial"]),  # type: ignore[arg-type]
            reset_on=tuple(str(item) for item in value.get("reset_on", ())),
        )


@dataclasses.dataclass(frozen=True, slots=True)
class GraphIR:
    name: str
    scope: Scope
    tensors: tuple[TensorSpec, ...]
    nodes: tuple[Node, ...]
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    states: tuple[StateEdge, ...] = ()

    def validate(self) -> None:
        _validate_name(self.name, "graph")
        if self.scope not in {"operator_family", "full_temporal_renderer"}:
            raise IRValidationError(f"unsupported graph scope: {self.scope}")
        if not self.tensors:
            raise IRValidationError("graph contains no tensors")
        tensor_by_name: dict[str, TensorSpec] = {}
        for tensor in self.tensors:
            tensor.validate()
            if tensor.name in tensor_by_name:
                raise IRValidationError(f"duplicate tensor: {tensor.name!r}")
            tensor_by_name[tensor.name] = tensor
        node_ids: set[str] = set()
        produced: set[str] = set()
        available = {
            tensor.name
            for tensor in self.tensors
            if tensor.role in {"input", "state", "weight", "constant"}
        }
        for node in self.nodes:
            node.validate()
            if node.id in node_ids:
                raise IRValidationError(f"duplicate node id: {node.id!r}")
            node_ids.add(node.id)
            for input_name in node.inputs:
                if input_name not in tensor_by_name:
                    raise IRValidationError(
                        f"node {node.id!r} references unknown input {input_name!r}"
                    )
                if input_name not in available:
                    raise IRValidationError(
                        f"node {node.id!r} consumes {input_name!r} before it is produced"
                    )
            for output_name in node.outputs:
                if output_name not in tensor_by_name:
                    raise IRValidationError(
                        f"node {node.id!r} references unknown output {output_name!r}"
                    )
                if output_name in produced or output_name in available:
                    raise IRValidationError(
                        f"tensor {output_name!r} has more than one producer"
                    )
                produced.add(output_name)
                available.add(output_name)
        for name in self.inputs:
            tensor = tensor_by_name.get(name)
            if tensor is None or tensor.role != "input":
                raise IRValidationError(f"graph input {name!r} is missing or not role=input")
        for name in self.outputs:
            tensor = tensor_by_name.get(name)
            if tensor is None or tensor.role != "output":
                raise IRValidationError(f"graph output {name!r} is missing or not role=output")
            if name not in available:
                raise IRValidationError(f"graph output {name!r} is never produced")
        state_names: set[str] = set()
        for state in self.states:
            state.validate()
            if state.name in state_names:
                raise IRValidationError(f"duplicate state edge: {state.name!r}")
            state_names.add(state.name)
            input_tensor = tensor_by_name.get(state.input_tensor)
            output_tensor = tensor_by_name.get(state.output_tensor)
            if input_tensor is None or input_tensor.role != "state":
                raise IRValidationError(
                    f"state input {state.input_tensor!r} is missing or not role=state"
                )
            if output_tensor is None or output_tensor.role not in {"state", "output"}:
                raise IRValidationError(
                    f"state output {state.output_tensor!r} is missing or has invalid role"
                )
            if state.output_tensor not in available:
                raise IRValidationError(
                    f"state output {state.output_tensor!r} is never produced"
                )
        if self.scope == "full_temporal_renderer" and not self.states:
            raise IRValidationError("full temporal renderer must declare explicit state edges")
        _validate_storage_ranges(self.tensors)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "GraphIR":
        return cls(
            name=str(value["name"]),
            scope=str(value["scope"]),  # type: ignore[arg-type]
            tensors=tuple(TensorSpec.from_dict(item) for item in value["tensors"]),
            nodes=tuple(Node.from_dict(item) for item in value["nodes"]),
            inputs=tuple(str(item) for item in value["inputs"]),
            outputs=tuple(str(item) for item in value["outputs"]),
            states=tuple(StateEdge.from_dict(item) for item in value.get("states", ())),
        )


@dataclasses.dataclass(frozen=True, slots=True)
class ModelIR:
    graph: GraphIR
    metadata: Mapping[str, Any]
    coverage: Mapping[str, Any]
    schema: str = SCHEMA

    def validate(self) -> None:
        if self.schema != SCHEMA:
            raise IRValidationError(
                f"unsupported schema {self.schema!r}; expected {SCHEMA!r}"
            )
        self.graph.validate()
        _validate_json_value(self.metadata, "metadata")
        _validate_json_value(self.coverage, "coverage")
        complete = self.coverage.get("complete")
        if not isinstance(complete, bool):
            raise IRValidationError("coverage.complete must be boolean")
        implemented = self.coverage.get("implemented_blocks")
        total = self.coverage.get("total_blocks")
        if implemented is not None or total is not None:
            if not isinstance(implemented, int) or not isinstance(total, int):
                raise IRValidationError(
                    "coverage implemented_blocks/total_blocks must both be integers"
                )
            if implemented < 0 or total <= 0 or implemented > total:
                raise IRValidationError("invalid block coverage")
        if complete and self.graph.scope != "full_temporal_renderer":
            raise IRValidationError(
                "coverage cannot be complete for an operator-family graph"
            )

    def to_dict(self) -> dict[str, Any]:
        return _to_jsonable(self)

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ModelIR":
        metadata = value.get("metadata", {})
        coverage = value.get("coverage", {})
        if not isinstance(metadata, Mapping) or not isinstance(coverage, Mapping):
            raise IRValidationError("metadata/coverage must be objects")
        model = cls(
            schema=str(value.get("schema", "")),
            graph=GraphIR.from_dict(value["graph"]),
            metadata=dict(metadata),
            coverage=dict(coverage),
        )
        model.validate()
        return model


def save_model(model: ModelIR, path: str | Path) -> None:
    model.validate()
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(
        json.dumps(model.to_dict(), indent=2, ensure_ascii=False, sort_keys=False)
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(destination)


def load_model(path: str | Path) -> ModelIR:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise IRValidationError("model root must be a JSON object")
    return ModelIR.from_dict(value)


def _validate_name(value: str, label: str) -> None:
    if not value or not _IDENTIFIER.fullmatch(value):
        raise IRValidationError(f"invalid {label} identifier: {value!r}")


def _static_element_count(shape: Sequence[Dim]) -> int | None:
    count = 1
    for dimension in shape:
        if not isinstance(dimension, int):
            return None
        count *= dimension
    return count


def _validate_storage_ranges(tensors: Iterable[TensorSpec]) -> None:
    by_file: dict[str, list[tuple[int, int, str]]] = {}
    for tensor in tensors:
        if tensor.storage is None:
            continue
        start = tensor.storage.offset
        end = start + tensor.storage.nbytes
        by_file.setdefault(tensor.storage.file, []).append((start, end, tensor.name))
    for file, ranges in by_file.items():
        ranges.sort()
        previous_end = -1
        previous_name = ""
        for start, end, name in ranges:
            if start < previous_end:
                raise IRValidationError(
                    f"overlapping storage in {file!r}: {previous_name!r} and {name!r}"
                )
            previous_end = end
            previous_name = name


def _validate_json_value(value: Any, label: str) -> None:
    try:
        json.dumps(value, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise IRValidationError(f"{label} is not strict JSON: {exc}") from exc


def _to_jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            field.name: _to_jsonable(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, Mapping):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_to_jsonable(item) for item in value]
    return value
