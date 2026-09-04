#!/usr/bin/env python3
"""Prepare a verified Daniel-compatible game directory in one command.

This orchestration performs the shortest working route demonstrated publicly:

1. validate and stream the exact private tensor contract into
   ``dlssnr_on_amd_weights.bin``;
2. download/read the official Daniel v0.2.9 installer, verify its SHA-256 and
   statically carve the embedded ``version.dll`` without executing it;
3. stage both files, verify their hashes/contracts, then install them atomically;
4. optionally copy an existing upstream ``dlssnr_on_amd.ini`` unchanged.

No proprietary artifact is committed or uploaded. The generated directory is
for local interoperability/testing under the terms of the upstream projects.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence

from dlssnrw1 import read_index
from extract_official_runtime import (
    DEFAULT_INSTALLER_SHA256,
    DEFAULT_RUNTIME_SHA256,
    DEFAULT_URL,
    ExtractionError,
    execute as extract_runtime,
)
from pack_private_zip_by_contract import (
    MappingError,
    execute as pack_private_zip,
    load_contract,
)

RUNTIME_NAME = "version.dll"
WEIGHTS_NAME = "dlssnr_on_amd_weights.bin"
CONFIG_NAME = "dlssnr_on_amd.ini"
REPORT_NAME = "dlssnr_install_report.json"
COPY_CHUNK = 8 * 1024 * 1024


class PreparationError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(COPY_CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def copy_atomic(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=destination.name + ".", suffix=".tmp", dir=destination.parent
    )
    try:
        with source.open("rb") as input_stream, os.fdopen(descriptor, "wb") as output_stream:
            while chunk := input_stream.read(COPY_CHUNK):
                output_stream.write(chunk)
            output_stream.flush()
            os.fsync(output_stream.fileno())
        os.replace(temporary_name, destination)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _destination_policy(
    destination: Path,
    expected_sha256: str,
    *,
    overwrite: bool,
    backup_existing: bool,
) -> dict[str, Any]:
    if not destination.exists():
        return {"action": "create", "existing_sha256": None, "backup": None}
    if not destination.is_file():
        raise PreparationError(f"destination exists but is not a regular file: {destination}")
    existing = sha256_file(destination)
    if existing == expected_sha256:
        return {"action": "already-current", "existing_sha256": existing, "backup": None}
    if not overwrite and not backup_existing:
        raise PreparationError(
            f"refusing to replace existing {destination.name} ({existing}); "
            "use --backup-existing or --overwrite"
        )
    backup: Path | None = None
    if backup_existing:
        backup = destination.with_name(destination.name + ".pre-dlssnr.bak")
        if backup.exists():
            backup_digest = sha256_file(backup) if backup.is_file() else None
            if backup_digest != existing:
                raise PreparationError(
                    f"backup path already exists with different content: {backup}"
                )
        else:
            copy_atomic(destination, backup)
            if sha256_file(backup) != existing:
                raise PreparationError(f"backup verification failed: {backup}")
    return {
        "action": "replace",
        "existing_sha256": existing,
        "backup": str(backup) if backup else None,
    }


def _verify_weight_contract(weights: Path, contract_path: Path) -> dict[str, Any]:
    contract = load_contract(contract_path)
    parsed = read_index(weights, require_dense=True)
    expected = [(item.name, item.byte_size) for item in contract]
    actual = [(item.name, item.size) for item in parsed.entries]
    if actual != expected:
        raise PreparationError("generated weights do not match the exact tensor contract")
    return {
        "count": parsed.count,
        "data_offset": parsed.data_offset,
        "file_size": parsed.file_size,
        "payload_size": parsed.file_size - parsed.data_offset,
        "offset_basis": parsed.offset_basis,
        "sha256": sha256_file(weights),
    }


def prepare(
    private_zip: Path,
    game_directory: Path,
    *,
    contract_path: Path,
    installer: Path | None,
    installer_url: str,
    expected_installer_sha256: str,
    expected_runtime_sha256: str,
    expected_private_sha256: str | None,
    config: Path | None,
    overwrite: bool,
    backup_existing: bool,
    dry_run: bool,
) -> dict[str, Any]:
    private_zip = private_zip.resolve()
    game_directory = game_directory.resolve()
    contract_path = contract_path.resolve()
    if not private_zip.is_file():
        raise PreparationError(f"private ZIP not found: {private_zip}")
    if not contract_path.is_file():
        raise PreparationError(f"tensor contract not found: {contract_path}")
    if config is not None:
        config = config.resolve()
        if not config.is_file():
            raise PreparationError(f"configuration file not found: {config}")
    if game_directory.exists() and not game_directory.is_dir():
        raise PreparationError(f"game destination is not a directory: {game_directory}")
    if not game_directory.exists() and not dry_run:
        game_directory.mkdir(parents=True, exist_ok=True)

    # Staging next to the destination makes final os.replace/copies stay on the
    # same filesystem while keeping incomplete results out of the game folder.
    staging_parent = game_directory.parent if game_directory.parent.exists() else Path.cwd()
    with tempfile.TemporaryDirectory(prefix="dlssnr-daniel-stage-", dir=staging_parent) as temp_name:
        staging = Path(temp_name)
        staged_runtime = staging / RUNTIME_NAME
        staged_weights = staging / WEIGHTS_NAME
        runtime_report_path = staging / "runtime-report.json"
        weight_report_path = staging / "weight-report.json"

        runtime_report = extract_runtime(
            staged_runtime,
            installer=installer,
            url=installer_url,
            expected_installer_sha256=expected_installer_sha256,
            expected_runtime_sha256=expected_runtime_sha256,
            inspect_only=False,
            report_path=runtime_report_path,
        )
        weight_report = pack_private_zip(
            private_zip,
            contract_path,
            staged_weights,
            offset_basis="relative",
            forced_inventory=None,
            expected_private_sha256=expected_private_sha256,
            dry_run=False,
            report_path=weight_report_path,
        )
        if sha256_file(staged_runtime) != expected_runtime_sha256.lower():
            raise PreparationError("staged runtime hash validation failed")
        weight_summary = _verify_weight_contract(staged_weights, contract_path)
        if weight_summary["sha256"] != weight_report.get("container_sha256"):
            raise PreparationError("weight packer and independent verifier disagree on SHA-256")

        destinations = {
            RUNTIME_NAME: game_directory / RUNTIME_NAME,
            WEIGHTS_NAME: game_directory / WEIGHTS_NAME,
        }
        policies = {
            RUNTIME_NAME: _destination_policy(
                destinations[RUNTIME_NAME],
                runtime_report["runtime_sha256"],
                overwrite=overwrite,
                backup_existing=backup_existing,
            ),
            WEIGHTS_NAME: _destination_policy(
                destinations[WEIGHTS_NAME],
                weight_summary["sha256"],
                overwrite=overwrite,
                backup_existing=backup_existing,
            ),
        }
        if config is not None:
            config_digest = sha256_file(config)
            destinations[CONFIG_NAME] = game_directory / CONFIG_NAME
            policies[CONFIG_NAME] = _destination_policy(
                destinations[CONFIG_NAME],
                config_digest,
                overwrite=overwrite,
                backup_existing=backup_existing,
            )
        else:
            config_digest = None

        report: dict[str, Any] = {
            "schema_version": 1,
            "route": "daniel-v0.2.9-custom-hip",
            "status": "VERIFIED_STAGED" if dry_run else "INSTALLED",
            "private_zip": str(private_zip),
            "private_zip_sha256": weight_report["private_zip_sha256"],
            "contract": str(contract_path),
            "game_directory": str(game_directory),
            "runtime": {
                "source": runtime_report["source"],
                "installer_sha256": runtime_report["installer_sha256"],
                "sha256": runtime_report["runtime_sha256"],
                "size": runtime_report["runtime_size"],
            },
            "weights": weight_summary,
            "config": {
                "source": str(config) if config is not None else None,
                "sha256": config_digest,
                "note": (
                    "No INI was generated; the runtime uses its compiled defaults. "
                    "An upstream-generated INI can be supplied with --config."
                    if config is None
                    else "Copied unchanged from the supplied upstream configuration."
                ),
            },
            "destination_policy": policies,
            "installed_files": [],
            "success_gate": {
                "static_and_weight_contract": True,
                "runtime_execution_on_supported_gpu": False,
                "note": "A supported Windows 11 + Radeon RX 9000 machine must perform the final in-game frame gate.",
            },
        }

        if not dry_run:
            for name, source in ((RUNTIME_NAME, staged_runtime), (WEIGHTS_NAME, staged_weights)):
                policy = policies[name]
                if policy["action"] != "already-current":
                    copy_atomic(source, destinations[name])
                actual = sha256_file(destinations[name])
                expected = runtime_report["runtime_sha256"] if name == RUNTIME_NAME else weight_summary["sha256"]
                if actual != expected:
                    raise PreparationError(f"installed {name} failed SHA-256 verification")
                report["installed_files"].append(
                    {"name": name, "path": str(destinations[name]), "sha256": actual}
                )
            if config is not None:
                policy = policies[CONFIG_NAME]
                if policy["action"] != "already-current":
                    copy_atomic(config, destinations[CONFIG_NAME])
                actual = sha256_file(destinations[CONFIG_NAME])
                if actual != config_digest:
                    raise PreparationError("installed INI failed SHA-256 verification")
                report["installed_files"].append(
                    {"name": CONFIG_NAME, "path": str(destinations[CONFIG_NAME]), "sha256": actual}
                )
            report_path = game_directory / REPORT_NAME
            report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
            report["report_path"] = str(report_path)
        return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_zip", type=Path)
    parser.add_argument("game_directory", type=Path)
    parser.add_argument(
        "--contract",
        type=Path,
        default=Path(__file__).with_name("results") / "tensor-contract.json",
    )
    parser.add_argument("--installer", type=Path)
    parser.add_argument("--installer-url", default=DEFAULT_URL)
    parser.add_argument("--expected-installer-sha256", default=DEFAULT_INSTALLER_SHA256)
    parser.add_argument("--expected-runtime-sha256", default=DEFAULT_RUNTIME_SHA256)
    parser.add_argument("--expected-private-sha256")
    parser.add_argument("--config", type=Path)
    replacement = parser.add_mutually_exclusive_group()
    replacement.add_argument("--overwrite", action="store_true")
    replacement.add_argument("--backup-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = prepare(
            args.private_zip,
            args.game_directory,
            contract_path=args.contract,
            installer=args.installer,
            installer_url=args.installer_url,
            expected_installer_sha256=args.expected_installer_sha256,
            expected_runtime_sha256=args.expected_runtime_sha256,
            expected_private_sha256=args.expected_private_sha256,
            config=args.config,
            overwrite=args.overwrite,
            backup_existing=args.backup_existing,
            dry_run=args.dry_run,
        )
    except (
        OSError,
        PreparationError,
        MappingError,
        ExtractionError,
        json.JSONDecodeError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
