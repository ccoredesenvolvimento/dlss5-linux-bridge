from __future__ import annotations

import hashlib
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterable, Iterator, Mapping, Sequence

import numpy as np

from .ir import IRValidationError, StorageRef, TensorSpec

_NUMPY_DTYPES: dict[str, np.dtype] = {
    "f32": np.dtype("<f4"),
    "f16": np.dtype("<f2"),
    "i32": np.dtype("<i4"),
    "u32": np.dtype("<u4"),
    "u8": np.dtype("u1"),
    "bool": np.dtype("?"),
    "e4m3fn": np.dtype("u1"),
}


class WeightArchiveError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class StoredTensor:
    name: str
    shape: tuple[int, ...]
    dtype: str
    layout: str
    storage: StorageRef
    logical_dtype: str | None = None

    def to_spec(self) -> TensorSpec:
        return TensorSpec(
            name=self.name,
            shape=self.shape,
            dtype=self.dtype,  # type: ignore[arg-type]
            logical_dtype=self.logical_dtype,  # type: ignore[arg-type]
            role="weight",
            layout=self.layout,
            storage=self.storage,
        )


@dataclass(frozen=True, slots=True)
class TensorPayload:
    name: str
    array: np.ndarray
    storage_dtype: str
    layout: str
    logical_dtype: str | None = None


class WeightArchiveBuilder:
    def __init__(self, *, alignment: int = 64, filename: str = "weights.bin") -> None:
        if alignment <= 0 or alignment & (alignment - 1):
            raise ValueError("alignment must be a positive power of two")
        if not filename or Path(filename).is_absolute() or ".." in Path(filename).parts:
            raise ValueError("filename must be a safe relative path")
        self.alignment = alignment
        self.filename = filename

    def write(
        self,
        payloads: Sequence[TensorPayload],
        destination: str | Path,
    ) -> tuple[tuple[StoredTensor, ...], dict[str, object]]:
        output = Path(destination)
        output.parent.mkdir(parents=True, exist_ok=True)
        seen: set[str] = set()
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=output.name + ".", suffix=".tmp", dir=output.parent
        )
        stored: list[StoredTensor] = []
        whole_digest = hashlib.sha256()
        try:
            with os.fdopen(descriptor, "wb") as stream:
                for payload in payloads:
                    if payload.name in seen:
                        raise WeightArchiveError(f"duplicate tensor: {payload.name!r}")
                    seen.add(payload.name)
                    raw, shape = encode_array(payload.array, payload.storage_dtype)
                    offset = _align(stream.tell(), self.alignment)
                    padding = offset - stream.tell()
                    if padding:
                        zeros = b"\0" * padding
                        stream.write(zeros)
                        whole_digest.update(zeros)
                    digest = hashlib.sha256(raw).hexdigest()
                    stream.write(raw)
                    whole_digest.update(raw)
                    storage = StorageRef(
                        file=self.filename,
                        offset=offset,
                        nbytes=len(raw),
                        sha256=digest,
                        encoding="raw-little-endian",
                        alignment=self.alignment,
                    )
                    item = StoredTensor(
                        name=payload.name,
                        shape=shape,
                        dtype=payload.storage_dtype,
                        logical_dtype=payload.logical_dtype,
                        layout=payload.layout,
                        storage=storage,
                    )
                    item.to_spec().validate()
                    stored.append(item)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_name, output)
        except BaseException:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            raise
        manifest: dict[str, object] = {
            "schema": "dlssnr-portable-weights-v1",
            "file": self.filename,
            "size": output.stat().st_size,
            "sha256": sha256_file(output),
            "alignment": self.alignment,
            "tensor_count": len(stored),
            "tensors": [
                {
                    "name": item.name,
                    "shape": list(item.shape),
                    "dtype": item.dtype,
                    "logical_dtype": item.logical_dtype,
                    "layout": item.layout,
                    "offset": item.storage.offset,
                    "nbytes": item.storage.nbytes,
                    "sha256": item.storage.sha256,
                }
                for item in stored
            ],
        }
        return tuple(stored), manifest


class WeightArchiveReader:
    def __init__(
        self,
        root: str | Path,
        tensors: Iterable[TensorSpec],
        *,
        verify_file_hash: str | None = None,
    ) -> None:
        self.root = Path(root)
        self._tensors: dict[str, TensorSpec] = {}
        for tensor in tensors:
            if tensor.role not in {"weight", "constant"} or tensor.storage is None:
                continue
            tensor.validate()
            if tensor.name in self._tensors:
                raise WeightArchiveError(f"duplicate tensor spec: {tensor.name!r}")
            self._tensors[tensor.name] = tensor
        files = {tensor.storage.file for tensor in self._tensors.values() if tensor.storage}
        if len(files) > 1:
            raise WeightArchiveError("this reader currently requires one weight file")
        self.path = self.root / next(iter(files), "weights.bin")
        if not self.path.is_file():
            raise WeightArchiveError(f"weight file not found: {self.path}")
        self._size = self.path.stat().st_size
        if verify_file_hash is not None:
            actual = sha256_file(self.path)
            if actual != verify_file_hash.lower():
                raise WeightArchiveError(
                    f"weight-file SHA-256 mismatch: expected {verify_file_hash}, got {actual}"
                )
        self._validate_ranges()

    def names(self) -> tuple[str, ...]:
        return tuple(self._tensors)

    def spec(self, name: str) -> TensorSpec:
        try:
            return self._tensors[name]
        except KeyError as exc:
            raise WeightArchiveError(f"unknown tensor: {name!r}") from exc

    def read(
        self,
        name: str,
        *,
        logical: bool = True,
        verify: bool = True,
    ) -> np.ndarray:
        tensor = self.spec(name)
        assert tensor.storage is not None
        with self.path.open("rb") as stream:
            stream.seek(tensor.storage.offset)
            raw = _read_exact(stream, tensor.storage.nbytes, name)
        if verify:
            digest = hashlib.sha256(raw).hexdigest()
            if digest != tensor.storage.sha256:
                raise WeightArchiveError(
                    f"tensor {name!r} SHA-256 mismatch: expected "
                    f"{tensor.storage.sha256}, got {digest}"
                )
        static_shape = tuple(int(value) for value in tensor.shape)
        if tensor.dtype == "e4m3fn":
            encoded = np.frombuffer(raw, dtype=np.uint8).reshape(static_shape)
            if logical:
                target = tensor.logical_dtype or "f32"
                decoded = decode_e4m3fn(encoded)
                return decoded.astype(_numpy_dtype(target), copy=False)
            return encoded.copy()
        result = np.frombuffer(raw, dtype=_numpy_dtype(tensor.dtype)).reshape(static_shape)
        if logical and tensor.logical_dtype and tensor.logical_dtype != tensor.dtype:
            return result.astype(_numpy_dtype(tensor.logical_dtype), copy=True)
        return result.copy()

    def mmap(self, name: str) -> np.memmap:
        tensor = self.spec(name)
        assert tensor.storage is not None
        if tensor.dtype == "e4m3fn":
            dtype = np.uint8
        else:
            dtype = _numpy_dtype(tensor.dtype)
        return np.memmap(
            self.path,
            mode="r",
            dtype=dtype,
            offset=tensor.storage.offset,
            shape=tuple(int(value) for value in tensor.shape),
            order="C",
        )

    def _validate_ranges(self) -> None:
        ranges: list[tuple[int, int, str]] = []
        for tensor in self._tensors.values():
            assert tensor.storage is not None
            start = tensor.storage.offset
            end = start + tensor.storage.nbytes
            if end > self._size:
                raise WeightArchiveError(
                    f"tensor {tensor.name!r} ends at {end}, file size is {self._size}"
                )
            ranges.append((start, end, tensor.name))
        ranges.sort()
        previous_end = 0
        previous_name = ""
        for start, end, name in ranges:
            if start < previous_end:
                raise WeightArchiveError(
                    f"overlapping tensors: {previous_name!r} and {name!r}"
                )
            previous_end = end
            previous_name = name


def encode_array(array: np.ndarray, storage_dtype: str) -> tuple[bytes, tuple[int, ...]]:
    if storage_dtype not in _NUMPY_DTYPES:
        raise WeightArchiveError(f"unsupported storage dtype: {storage_dtype!r}")
    value = np.asarray(array)
    if value.ndim == 0:
        value = value.reshape(1)
    if not all(dimension > 0 for dimension in value.shape):
        raise WeightArchiveError("zero-sized tensor storage is not supported")
    if storage_dtype == "e4m3fn":
        if value.dtype == np.uint8:
            encoded = np.ascontiguousarray(value, dtype=np.uint8)
        else:
            encoded = encode_e4m3fn(np.asarray(value, dtype=np.float32))
        return encoded.tobytes(order="C"), tuple(int(item) for item in encoded.shape)
    encoded = np.ascontiguousarray(value, dtype=_numpy_dtype(storage_dtype))
    return encoded.tobytes(order="C"), tuple(int(item) for item in encoded.shape)


def decode_e4m3fn(encoded: np.ndarray) -> np.ndarray:
    """Decode ONNX/NVIDIA-style finite-only E4M3 bytes to float32."""
    value = np.asarray(encoded, dtype=np.uint8)
    sign = np.where(value & 0x80, -1.0, 1.0).astype(np.float32)
    exponent = ((value >> 3) & 0x0F).astype(np.int32)
    mantissa = (value & 0x07).astype(np.int32)
    normal = exponent != 0
    decoded = np.empty(value.shape, dtype=np.float32)
    decoded[~normal] = mantissa[~normal].astype(np.float32) * np.float32(2.0**-9)
    decoded[normal] = (
        1.0 + mantissa[normal].astype(np.float32) / 8.0
    ) * np.exp2(exponent[normal].astype(np.float32) - 7.0)
    decoded *= sign
    decoded[(exponent == 15) & (mantissa == 7)] = np.nan
    return decoded


def encode_e4m3fn(value: np.ndarray) -> np.ndarray:
    """Reference nearest-value E4M3FN encoder using an exhaustive 256-value table."""
    source = np.asarray(value, dtype=np.float32)
    table_bytes = np.arange(256, dtype=np.uint8)
    table_values = decode_e4m3fn(table_bytes)
    finite_mask = np.isfinite(table_values)
    finite_bytes = table_bytes[finite_mask]
    finite_values = table_values[finite_mask]
    flat = source.reshape(-1)
    output = np.empty(flat.shape, dtype=np.uint8)
    finite_input = np.isfinite(flat)
    if np.any(finite_input):
        # This is a conversion/reference path, not an inference kernel. Process
        # in chunks to bound temporary memory for large checkpoints.
        indices = np.flatnonzero(finite_input)
        for start in range(0, len(indices), 1 << 16):
            selected = indices[start : start + (1 << 16)]
            distances = np.abs(flat[selected, None] - finite_values[None, :])
            output[selected] = finite_bytes[np.argmin(distances, axis=1)]
    nan_code = np.uint8(0xFF)
    output[~finite_input] = nan_code
    return output.reshape(source.shape)


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _numpy_dtype(dtype: str) -> np.dtype:
    try:
        return _NUMPY_DTYPES[dtype]
    except KeyError as exc:
        raise WeightArchiveError(f"unsupported dtype: {dtype!r}") from exc


def _align(value: int, alignment: int) -> int:
    return (value + alignment - 1) & ~(alignment - 1)


def _read_exact(stream: BinaryIO, size: int, label: str) -> bytes:
    data = stream.read(size)
    if len(data) != size:
        raise WeightArchiveError(
            f"truncated tensor {label!r}: expected {size} bytes, got {len(data)}"
        )
    return data
