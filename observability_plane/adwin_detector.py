"""Hoeffding-Bernstein ADWIN Concept Drift Detector for Minecraft Tick Telemetry.

Adapted from Bifet & Gavalda (SIAM SDM 2007) and Safe-Agentic-DataOps.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ADWINDriftResult:
    """Output of ADWIN drift detection and Minecraft surge classification."""

    drift_detected: bool
    drift_type: str  # "STABLE" | "BENIGN_PLAYER_SURGE" | "MALIGNANT_LAG_ANOMALY"
    epsilon_cut: float
    suppress_alert: bool
    mean_before: float
    mean_after: float


class ADWINDetector:
    """Normalized Hoeffding-Bernstein Adaptive Windowing detector."""

    def __init__(self, delta: float = 0.002, max_window: int = 200, min_subwindow: int = 4) -> None:
        self.delta = delta
        self.max_window = max_window
        self.min_subwindow = min_subwindow
        self.window: list[float] = []

    def update(self, value: float) -> tuple[bool, float, float, float]:
        """Insert a new metric sample and test for a statistically significant cut."""
        self.window.append(float(value))
        if len(self.window) > self.max_window:
            self.window.pop(0)

        n = len(self.window)
        if n < 2 * self.min_subwindow:
            return False, 0.0, 0.0, 0.0

        min_v = min(self.window)
        max_v = max(self.window)
        scale = max(max_v - min_v, 1e-6)
        w_norm = [(x - min_v) / scale for x in self.window]

        mean_all = sum(w_norm) / n
        var_norm = sum((x - mean_all) ** 2 for x in w_norm) / n
        delta_prime = self.delta / max(math.log(n), 1.0)
        l_term = math.log(4.0 * n / max(delta_prime, 1e-12))

        for i in range(self.min_subwindow, n - self.min_subwindow + 1):
            w0_norm = w_norm[:i]
            w1_norm = w_norm[i:]
            m = 1.0 / ((1.0 / len(w0_norm)) + (1.0 / len(w1_norm)))
            eps_norm = min(
                0.38,
                math.sqrt((2.0 / m) * var_norm * l_term) + (2.0 / (3.0 * m)) * l_term,
            )
            diff_norm = abs((sum(w0_norm) / len(w0_norm)) - (sum(w1_norm) / len(w1_norm)))
            w0_raw = self.window[:i]
            w1_raw = self.window[i:]
            mu0 = sum(w0_raw) / len(w0_raw)
            mu1 = sum(w1_raw) / len(w1_raw)

            if diff_norm >= eps_norm and abs(mu0 - mu1) > 1e-3:
                eps_cut = eps_norm * scale
                self.window = self.window[i:]
                return True, eps_cut, mu0, mu1

        return False, 0.0, 0.0, 0.0


class MinecraftDriftClassifier:
    """Separates benign player/chunk surges from malignant MSPT/Watchdog anomalies."""

    def __init__(self, delta: float = 0.002) -> None:
        self.detector = ADWINDetector(delta=delta)

    def evaluate_mspt_stream(
        self,
        mspt_series: list[float],
        error_rates: list[float] | None = None,
        has_watchdog_warning: bool = False,
    ) -> ADWINDriftResult:
        """Evaluate an MSPT time-series and classify benign surges vs real lag."""
        detector = ADWINDetector(delta=self.detector.delta)
        drift = False
        eps_cut = 0.0
        mu0 = 0.0
        mu1 = 0.0

        for sample in mspt_series:
            d, e, m0, m1 = detector.update(sample)
            if d:
                drift, eps_cut, mu0, mu1 = d, e, m0, m1

        err_tail = error_rates[-5:] if error_rates else [0.0]
        avg_err = sum(err_tail) / len(err_tail)
        latest_mspt = mspt_series[-1] if mspt_series else 0.0

        # Benign surge: moderate MSPT rise (e.g. players joining) without hitting 50ms tick budget
        if drift and mu1 > mu0 and latest_mspt < 45.0 and avg_err < 0.03 and not has_watchdog_warning:
            return ADWINDriftResult(
                drift_detected=True,
                drift_type="BENIGN_PLAYER_SURGE",
                epsilon_cut=eps_cut,
                suppress_alert=True,
                mean_before=mu0,
                mean_after=mu1,
            )

        if (drift and latest_mspt >= 45.0) or latest_mspt >= 50.0 or avg_err >= 0.05 or has_watchdog_warning:
            return ADWINDriftResult(
                drift_detected=drift or latest_mspt >= 50.0,
                drift_type="MALIGNANT_LAG_ANOMALY",
                epsilon_cut=eps_cut,
                suppress_alert=False,
                mean_before=mu0,
                mean_after=mu1 or latest_mspt,
            )

        return ADWINDriftResult(
            drift_detected=False,
            drift_type="STABLE",
            epsilon_cut=eps_cut,
            suppress_alert=True,
            mean_before=mu0,
            mean_after=mu1,
        )
