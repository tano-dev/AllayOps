"""Savepoint & config snapshot manager with SHA-256 integrity verification."""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

from shared_interfaces.schemas import utc_now_iso


@dataclass(frozen=True)
class SavepointRecord:
    """Metadata for a verified server configuration/world savepoint."""

    savepoint_id: str
    created_at: str
    snapshot_dir: str
    checksums: dict[str, str]


class WorldSavepointManager:
    """Creates SHA-256 verified config/world snapshots and supports rollback."""

    def __init__(self, backup_root: Path) -> None:
        self.backup_root = backup_root
        self.lineage_file = self.backup_root / "savepoint_lineage.jsonl"

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def create_savepoint(self, savepoint_id: str, files_to_snapshot: list[Path]) -> SavepointRecord:
        """Copy target files into a savepoint directory and record SHA-256 checksums."""
        snap_dir = self.backup_root / savepoint_id
        snap_dir.mkdir(parents=True, exist_ok=True)
        checksums: dict[str, str] = {}

        for src in files_to_snapshot:
            if src.is_file():
                dst = snap_dir / src.name
                shutil.copy2(src, dst)
                checksums[src.name] = self._sha256(dst)

        record = SavepointRecord(
            savepoint_id=savepoint_id,
            created_at=utc_now_iso(),
            snapshot_dir=str(snap_dir),
            checksums=checksums,
        )
        self.lineage_file.parent.mkdir(parents=True, exist_ok=True)
        with self.lineage_file.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(record)) + "\n")
        return record

    def rollback(self, record: SavepointRecord, restore_targets: dict[str, Path]) -> list[str]:
        """Restore tracked files from a verified savepoint after checking SHA-256."""
        snap_dir = Path(record.snapshot_dir)
        restored: list[str] = []
        for filename, expected_hash in record.checksums.items():
            src = snap_dir / filename
            if not src.is_file():
                raise FileNotFoundError(f"Missing savepoint artifact: {src}")
            if self._sha256(src) != expected_hash:
                raise ValueError(f"Checksum mismatch for savepoint artifact: {src}")
            if filename in restore_targets:
                shutil.copy2(src, restore_targets[filename])
                restored.append(filename)
        return restored
