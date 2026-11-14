"""Tests for external Mods & Datapacks content sync."""

import tempfile
import unittest
from pathlib import Path

from scripts.sync_content import sync_from_local_source


class TestContentSync(unittest.TestCase):
    def test_sync_from_local_source_copies_mods_and_datapacks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "AllayOps-Content"
            (src / "mods").mkdir(parents=True)
            (src / "datapacks" / "allay_pack").mkdir(parents=True)
            (src / "mods" / "example-mod.jar").write_bytes(b"fake-jar")
            (src / "datapacks" / "allay_pack" / "pack.mcmeta").write_text("{}", encoding="utf-8")

            ws = root / "AllayOps"
            ws.mkdir()
            manifest = {
                "content_repo": {"url": "https://example.com/repo.git", "ref": "main"},
                "mappings": {"mods_dir": "mods", "datapacks_dir": "world/datapacks"},
                "safety": {"create_savepoint_before_sync": True, "allow_jar_sync": True},
            }

            res = sync_from_local_source(src, manifest, workspace_root=ws, dry_run=False)
            self.assertEqual(res["mods"], ["example-mod.jar"])
            self.assertEqual(res["datapacks"], ["allay_pack"])
            self.assertTrue((ws / "mods" / "example-mod.jar").is_file())
            self.assertTrue((ws / "world" / "datapacks" / "allay_pack" / "pack.mcmeta").is_file())


if __name__ == "__main__":
    unittest.main()
