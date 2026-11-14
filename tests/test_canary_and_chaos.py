"""Tests for Canary Verification Gate, Savepoints, and Chaos Suite."""

import tempfile
import unittest
from pathlib import Path

from agentic_plane.canary_gate import CanaryVerificationGate
from minecraft_plane.savepoint_manager import WorldSavepointManager
from research.run_benchmark import run_canonical_suite


class TestCanaryAndChaos(unittest.TestCase):
    def test_canary_promotes_healthy_and_rollbacks_lag(self) -> None:
        gate = CanaryVerificationGate()
        ok = gate.evaluate(savepoint_id="sp-1", mspt=20.0, error_log_rate=0.0)
        self.assertEqual(ok.status, "PROMOTED")
        self.assertGreaterEqual(ok.health_score, 0.98)

        bad = gate.evaluate(savepoint_id="sp-1", mspt=150.0, error_log_rate=0.05)
        self.assertEqual(bad.status, "ROLLBACK_TRIGGERED")

    def test_savepoint_create_and_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg = root / "server.properties"
            cfg.write_text("view-distance=10\n", encoding="utf-8")

            mgr = WorldSavepointManager(root / "backups")
            rec = mgr.create_savepoint("sp-test", [cfg])
            cfg.write_text("view-distance=2\n", encoding="utf-8")

            restored = mgr.rollback(rec, {"server.properties": cfg})
            self.assertEqual(restored, ["server.properties"])
            self.assertEqual(cfg.read_text(encoding="utf-8"), "view-distance=10\n")

    def test_canonical_chaos_suite_runs_end_to_end(self) -> None:
        results = run_canonical_suite()
        by_code = {r["code"]: r for r in results}
        self.assertTrue(by_code["MC_INC01"]["parried"])
        self.assertTrue(by_code["MC_INC02"]["suppressed"])
        self.assertTrue(by_code["MC_INC03"]["safety_blocked_poison"])
        self.assertEqual(by_code["MC_INC04"]["canary_status"], "PROMOTED")


if __name__ == "__main__":
    unittest.main()
