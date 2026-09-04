from __future__ import annotations

import dataclasses
from typing import Any, Mapping, Sequence

import numpy as np


class CanonicalizationError(ValueError):
    pass


@dataclasses.dataclass(frozen=True, slots=True)
class OutputRecipe:
    name: str
    source: str
    source_dtype: str
    shape: tuple[int, ...]
    element_start: int | None = None
    element_count: int | None = None
    byte_start: int | None = None
    byte_count: int | None = None
    reinterpret_dtype: str | None = None
    transpose: tuple[int, ...] | None = None
    output_dtype: str | None = None
    layout: str = "row-major"

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "OutputRecipe":
        shape = tuple(int(item) for item in value["shape"])
        transpose_value = value.get("transpose")
        return cls(
            name=str(value["name"]),
            source=str(value["source"]),
            source_dtype=str(value["source_dtype"]),
            shape=shape,
            element_start=_optional_int(value.get("element_start")),
            element_count=_optional_int(value.get("element_count")),
            byte_start=_optional_int(value.get("byte_start")),
            byte_count=_optional_int(value.get("byte_count")),
            reinterpret_dtype=str(value["reinterpret_dtype"])
            if value.get("reinterpret_dtype") is not None
            else None,
            transpose=tuple(int(item) for item in transpose_value)
            if transpose_value is not None
            else None,
            output_dtype=str(value["output_dtype"])
            if value.get("output_dtype") is not None
            else None,
            layout=str(value.get("layout", "row-major")),
        )

    def validate(self) -> None:
        if not self.name or not self.source:
            raise CanonicalizationError("recipe name/source must not be empty")
        if not self.shape or any(item <= 0 for item in self.shape):
            raise CanonicalizationError(f"invalid shape for {self.name!r}: {self.shape}")
        uses_elements = self.element_start is not None or self.element_count is not None
        uses_bytes = self.byte_start is not None or self.byte_count is not None
        if uses_elements == uses_bytes:
            raise CanonicalizationError(
                f"{self.name!r} must use exactly one of element or byte slicing"
            )
        if uses_elements:
            if self.element_start is None or self.element_count is None:
                raise CanonicalizationError(
                    f"{self.name!r} requires element_start and element_count"
                )
        if uses_bytes:
            if self.byte_start is None or self.byte_count is None:
                raise CanonicalizationError(
                    f"{self.name!r} requires byte_start and byte_count"
                )
            if self.byte_count <= 0:
                raise CanonicalizationError(f"{self.name!r} byte_count must be positive")
        if self.transpose is not None:
            if tuple(sorted(self.transpose)) != tuple(range(len(self.shape))):
                raise CanonicalizationError(
                    f"{self.name!r} transpose is not a permutation: {self.transpose}"
                )


@dataclasses.dataclass(frozen=True, slots=True)
class CanonicalTensor:
    name: str
    array: np.ndarray
    layout: str


def apply_recipe(
    records: Mapping[str, bytes | bytearray | memoryview | np.ndarray],
    recipes: Sequence[OutputRecipe | Mapping[str, Any]],
) -> tuple[CanonicalTensor, ...]:
    outputs: list[CanonicalTensor] = []
    seen: set[str] = set()
    raw_cache: dict[str, bytes] = {}
    for supplied in recipes:
        recipe = (
            supplied
            if isinstance(supplied, OutputRecipe)
            else OutputRecipe.from_dict(supplied)
        )
        recipe.validate()
        if recipe.name in seen:
            raise CanonicalizationError(f"duplicate output tensor: {recipe.name!r}")
        seen.add(recipe.name)
        try:
            source = records[recipe.source]
        except KeyError as exc:
            raise CanonicalizationError(
                f"missing source record {recipe.source!r} for {recipe.name!r}"
            ) from exc
        raw = raw_cache.setdefault(recipe.source, _as_bytes(source, recipe.source_dtype))
        source_dtype = np.dtype(recipe.source_dtype)
        if recipe.element_start is not None:
            assert recipe.element_count is not None
            start = recipe.element_start * source_dtype.itemsize
            length = recipe.element_count * source_dtype.itemsize
        else:
            assert recipe.byte_start is not None and recipe.byte_count is not None
            start = recipe.byte_start
            length = recipe.byte_count
        if start < 0 or length <= 0 or start + length > len(raw):
            raise CanonicalizationError(
                f"slice for {recipe.name!r} is outside {recipe.source!r}: "
                f"{start}+{length} > {len(raw)}"
            )
        selected = memoryview(raw)[start : start + length]
        dtype = np.dtype(recipe.reinterpret_dtype or recipe.source_dtype)
        if len(selected) % dtype.itemsize:
            raise CanonicalizationError(
                f"{recipe.name!r} byte length {len(selected)} is not divisible by {dtype}"
            )
        array = np.frombuffer(selected, dtype=dtype)
        required = int(np.prod(recipe.shape, dtype=np.int64))
        if array.size != required:
            raise CanonicalizationError(
                f"{recipe.name!r}: recipe shape requires {required} values, "
                f"slice contains {array.size}"
            )
        array = array.reshape(recipe.shape)
        if recipe.transpose is not None:
            array = array.transpose(recipe.transpose)
        if recipe.output_dtype is not None:
            array = array.astype(np.dtype(recipe.output_dtype), copy=False)
        array = np.ascontiguousarray(array)
        if array.dtype.kind == "f" and not np.isfinite(array).all():
            raise CanonicalizationError(f"{recipe.name!r} contains non-finite values")
        outputs.append(CanonicalTensor(recipe.name, array, recipe.layout))
    return tuple(outputs)


def _as_bytes(value: bytes | bytearray | memoryview | np.ndarray, dtype: str) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    array = np.asarray(value)
    if array.dtype == np.uint8:
        return np.ascontiguousarray(array).tobytes(order="C")
    return np.ascontiguousarray(array, dtype=np.dtype(dtype)).tobytes(order="C")


def _optional_int(value: Any) -> int | None:
    return None if value is None else int(value)
