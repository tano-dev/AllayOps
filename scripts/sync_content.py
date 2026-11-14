"""Synchronize external Mods & Datapacks repository into AllayOps runtime folders.

Keeps AllayOps focused purely on the Agentic Self-Healing System while syncing
mods/ and world/datapacks/ from a separate GitHub repository (e.g., AllayOps-Content).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from minecraft_plane.savepoint_manager import WorldSavepointManager

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "content-manifest.json"


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict:
    """Load and validate content-manifest.json."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if "content_repo" not in data or "mappings" not in data:
        raise ValueError("Invalid content-manifest.json: missing 'content_repo' or 'mappings'.")
    return data


def _sync_tree(src_dir: Path, dst_dir: Path, dry_run: bool) -> list[str]:
    """Copy files/directories from src_dir to dst_dir and return synced relative paths."""
    if not src_dir.is_dir():
        return []
    synced: list[str] = []
    if not dry_run:
        dst_dir.mkdir(parents=True, exist_ok=True)
    for item in sorted(src_dir.iterdir()):
        if item.name.startswith("."):
            continue
        target = dst_dir / item.name
        synced.append(item.name)
        if dry_run:
            continue
        if item.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)
    return synced


def sync_from_local_source(
    source_root: Path,
    manifest: dict,
    workspace_root: Path = ROOT,
    dry_run: bool = False,
) -> dict[str, list[str]]:
    """Sync `mods/` and `datapacks/` from a local checked-out content repository."""
    mappings = manifest["mappings"]
    mods_dst = workspace_root / mappings["mods_dir"]
    datapacks_dst = workspace_root / mappings["datapacks_dir"]

    if not dry_run and manifest.get("safety", {}).get("create_savepoint_before_sync", True):
        savepoint_mgr = WorldSavepointManager(workspace_root / ".content-savepoints")
        existing_files = [p for p in mods_dst.glob("*.jar")] if mods_dst.is_dir() else []
        if existing_files:
            savepoint_mgr.create_savepoint("pre-content-sync", existing_files)

    mods_synced = (
        _sync_tree(source_root / "mods", mods_dst, dry_run=dry_run)
        if manifest.get("safety", {}).get("allow_jar_sync", True)
        else []
    )
    datapacks_synced = _sync_tree(source_root / "datapacks", datapacks_dst, dry_run=dry_run)

    return {"mods": mods_synced, "datapacks": datapacks_synced}


def fetch_content_repo(manifest: dict, workspace_root: Path = ROOT) -> Path:
    """Clone or update the external content repository into cache_dir."""
    repo_cfg = manifest["content_repo"]
    url = repo_cfg["url"]
    ref = repo_cfg.get("ref", "main")
    cache_dir = workspace_root / repo_cfg.get("cache_dir", ".content-cache")

    if (cache_dir / ".git").is_dir():
        subprocess.run(["git", "-C", str(cache_dir), "fetch", "--all", "--tags"], check=True)
        subprocess.run(["git", "-C", str(cache_dir), "checkout", ref], check=True)
        subprocess.run(["git", "-C", str(cache_dir), "pull", "--ff-only"], check=False)
    else:
        subprocess.run(
            ["git", "clone", "--branch", ref, "--depth", "1", url, str(cache_dir)],
            check=True,
        )
    return cache_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync AllayOps-Content mods and datapacks.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--local-source", type=Path, default=None, help="Sync from local folder")
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying files")
    args = parser.parse_args()

    manifest = load_manifest(args.manifest)
    source = args.local_source if args.local_source else fetch_content_repo(manifest)
    summary = sync_from_local_source(source, manifest, dry_run=args.dry_run)
    print(json.dumps({"dry_run": args.dry_run, "synced": summary}, indent=2))


if __name__ == "__main__":
    main()
