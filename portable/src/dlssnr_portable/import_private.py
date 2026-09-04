from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

from .window_family import WINDOW_FAMILIES, build_window_family_model

_BLOCK_PATTERN = re.compile(r"block[^0-9]*(\d+).*?layer[^0-9]*([0-3])", re.IGNORECASE)


class ImportError(ValueError):
    pass


def import_private_archive(
    archive_path: Path,
    output_directory: Path,
    *,
    recipe_path: Path,
    record_map_path: Path | None = None,
    expected_archive_sha256: str | None = None,
) -> dict[str, object]:
    archive_path = archive_path.resolve()
    if not archive_path.is_file():
        raise ImportError(f"private archive not found: {archive_path}")
    archive_digest = _sha256_file(archive_path)
    if expected_archive_sha256 is not None:
        expected = expected_archive_sha256.lower().removeprefix("sha256:")
        if archive_digest != expected:
            raise ImportError(
                f"private archive SHA-256 mismatch: expected {expected}, got {archive_digest}"
            )
    recipe = json.loads(recipe_path.read_text(encoding="utf-8"))
    source_specs = recipe.get("source_records")
    if not isinstance(source_specs, Mapping):
        raise ImportError("recipe has no source_records object")
    required_sizes = {
        str(name): int(spec["nbytes"])
        for name, spec in source_specs.items()
        if isinstance(spec, Mapping)
    }
    if set(required_sizes) != {"layer0", "layer1", "layer2", "layer3"}:
        raise ImportError("this importer requires layer0..layer3 source records")

    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            corrupt = archive.testzip()
            if corrupt is not None:
                raise ImportError(f"ZIP CRC failure in member {corrupt!r}")
            block_records = (
                _read_mapped_records(archive, record_map_path, required_sizes)
                if record_map_path is not None
                else _discover_direct_records(archive, required_sizes)
            )
    except zipfile.BadZipFile as exc:
        raise ImportError(f"invalid private ZIP: {exc}") from exc

    model = build_window_family_model(block_records, recipe, output_directory)
    report: dict[str, object] = {
        "schema": "dlssnr-private-import-v1",
        "private_archive": str(archive_path),
        "private_archive_sha256": archive_digest,
        "recipe": str(recipe_path.resolve()),
        "record_map": str(record_map_path.resolve()) if record_map_path else None,
        "blocks_imported": [block for family in WINDOW_FAMILIES for block in family],
        "canonical_tensor_count": sum(
            1 for tensor in model.graph.tensors if tensor.role == "weight"
        ),
        "coverage": dict(model.coverage),
        "output_directory": str(output_directory.resolve()),
        "verified": True,
    }
    (output_directory / "import-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report


def _discover_direct_records(
    archive: zipfile.ZipFile,
    required_sizes: Mapping[str, int],
) -> dict[int, dict[str, bytes]]:
    expected_blocks = {block for family in WINDOW_FAMILIES for block in family}
    candidates: dict[tuple[int, str], list[zipfile.ZipInfo]] = {}
    for info in archive.infolist():
        if info.is_dir():
            continue
        match = _BLOCK_PATTERN.search(PurePosixPath(info.filename).name)
        if match is None:
            continue
        block = int(match.group(1))
        layer = f"layer{int(match.group(2))}"
        if block not in expected_blocks or info.file_size != required_sizes[layer]:
            continue
        candidates.setdefault((block, layer), []).append(info)

    output: dict[int, dict[str, bytes]] = {}
    failures: list[str] = []
    for block in sorted(expected_blocks):
        output[block] = {}
        for layer, size in required_sizes.items():
            matches = candidates.get((block, layer), [])
            if not matches:
                failures.append(f"missing block{block}.{layer} ({size} bytes)")
                continue
            payloads = [(info, archive.read(info)) for info in matches]
            digests = {hashlib.sha256(data).hexdigest() for _, data in payloads}
            if len(digests) != 1:
                failures.append(
                    f"ambiguous non-identical block{block}.{layer}: "
                    + ", ".join(info.filename for info, _ in payloads[:8])
                )
                continue
            output[block][layer] = payloads[0][1]
    if failures:
        raise ImportError(
            "direct-record discovery did not close the 16-block contract:\n  - "
            + "\n  - ".join(failures[:50])
        )
    return output


def _read_mapped_records(
    archive: zipfile.ZipFile,
    record_map_path: Path,
    required_sizes: Mapping[str, int],
) -> dict[int, dict[str, bytes]]:
    document = json.loads(record_map_path.read_text(encoding="utf-8"))
    blocks = document.get("blocks") if isinstance(document, Mapping) else None
    if not isinstance(blocks, Mapping):
        raise ImportError("record map must contain a blocks object")
    members = {info.filename: info for info in archive.infolist() if not info.is_dir()}
    expected_blocks = {block for family in WINDOW_FAMILIES for block in family}
    output: dict[int, dict[str, bytes]] = {}
    for block in sorted(expected_blocks):
        value = blocks.get(str(block), blocks.get(block))
        if not isinstance(value, Mapping):
            raise ImportError(f"record map is missing block {block}")
        output[block] = {}
        for layer, expected_size in required_sizes.items():
            descriptor = value.get(layer)
            if not isinstance(descriptor, Mapping):
                raise ImportError(f"record map is missing block{block}.{layer}")
            member = str(descriptor.get("member", descriptor.get("path", "")))
            info = members.get(member)
            if info is None:
                raise ImportError(f"ZIP member not found: {member!r}")
            offset = int(descriptor.get("offset", 0))
            nbytes = int(descriptor.get("nbytes", expected_size))
            if nbytes != expected_size or offset < 0 or offset + nbytes > info.file_size:
                raise ImportError(f"invalid range for block{block}.{layer}")
            data = archive.read(info)[offset : offset + nbytes]
            expected_digest = descriptor.get("sha256")
            if expected_digest is not None:
                actual = hashlib.sha256(data).hexdigest()
                if actual != str(expected_digest).lower().removeprefix("sha256:"):
                    raise ImportError(f"SHA-256 mismatch for block{block}.{layer}")
            output[block][layer] = data
    return output


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--recipe",
        type=Path,
        default=Path(__file__).parents[2] / "recipes" / "window-transformer-512-v1.json",
    )
    parser.add_argument("--record-map", type=Path)
    parser.add_argument("--expected-archive-sha256")
    args = parser.parse_args(argv)
    try:
        report = import_private_archive(
            args.archive,
            args.output,
            recipe_path=args.recipe,
            record_map_path=args.record_map,
            expected_archive_sha256=args.expected_archive_sha256,
        )
    except (OSError, ImportError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
