"""Tests for ADWIN concept drift classification and Drain log compression."""

import unittest

from observability_plane.adwin_detector import MinecraftDriftClassifier
from observability_plane.drain_parser import DrainLogParser


class TestADWINAndDrain(unittest.TestCase):
    def test_benign_player_surge_is_suppressed(self) -> None:
        classifier = MinecraftDriftClassifier()
        mspt = [10.0, 10.5, 11.0, 10.2, 10.8, 22.0, 23.0, 24.0, 23.5, 22.5]
        result = classifier.evaluate_mspt_stream(mspt, has_watchdog_warning=False)
        self.assertTrue(result.drift_detected)
        self.assertEqual(result.drift_type, "BENIGN_PLAYER_SURGE")
        self.assertTrue(result.suppress_alert)

    def test_tnt_watchdog_lag_triggers_malignant_anomaly(self) -> None:
        classifier = MinecraftDriftClassifier()
        mspt = [12.0, 13.0, 12.5, 12.8, 13.2, 85.0, 160.0, 320.0, 640.0, 950.0]
        result = classifier.evaluate_mspt_stream(mspt, has_watchdog_warning=True)
        self.assertTrue(result.drift_detected)
        self.assertEqual(result.drift_type, "MALIGNANT_LAG_ANOMALY")
        self.assertFalse(result.suppress_alert)

    def test_drain_compresses_repetitive_logs(self) -> None:
        parser = DrainLogParser()
        lines = [
            "[12:00:01] [Server/WARN]: PrimedTnt.explode took 120ms at 10, 64, 20",
            "[12:00:02] [Server/WARN]: PrimedTnt.explode took 340ms at 12, 64, 22",
            "[12:00:03] [Server/WARN]: PrimedTnt.explode took 560ms at 14, 64, 24",
        ]
        summary = parser.summarize_for_llm(lines)
        self.assertEqual(len(summary), 1)
        self.assertTrue(summary[0].startswith("[x3]"))


if __name__ == "__main__":
    unittest.main()
