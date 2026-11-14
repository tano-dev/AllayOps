"""Closed-Loop Canary Verification Gate for AllayOps."""

from __future__ import annotations

from shared_interfaces.schemas import CanaryResult


class CanaryVerificationGate:
    """Evaluates post-remediation Minecraft health and triggers rollback if degraded."""

    def __init__(self, min_health_score: float = 0.98) -> None:
        self.min_health_score = min_health_score

    @staticmethod
    def compute_health_score(
        mspt: float,
        error_log_rate: float,
        adwin_malignant: bool = False,
    ) -> float:
        """Compute bounded HealthScore in [0.0, 1.0].

        Target steady-state Minecraft tick budget is <= 50.0 mspt (20 TPS).
        """
        mspt_excess = max(0.0, mspt - 50.0)
        penalty = (
            10.0 * max(0.0, error_log_rate)
            + min(mspt_excess, 200.0) / 1000.0
            + (0.35 if adwin_malignant else 0.0)
        )
        return max(0.0, min(1.0, 1.0 - penalty))

    def evaluate(
        self,
        savepoint_id: str,
        mspt: float,
        error_log_rate: float,
        adwin_malignant: bool = False,
    ) -> CanaryResult:
        """Promote if HealthScore >= 0.98 and no malignant drift; otherwise rollback."""
        score = self.compute_health_score(mspt, error_log_rate, adwin_malignant)
        if not adwin_malignant and score >= self.min_health_score:
            return CanaryResult(
                status="PROMOTED",
                health_score=round(score, 4),
                savepoint_id=savepoint_id,
                reason="Canary health invariants satisfied.",
            )
        return CanaryResult(
            status="ROLLBACK_TRIGGERED",
            health_score=round(score, 4),
            savepoint_id=savepoint_id,
            reason=f"HealthScore {score:.4f} < {self.min_health_score} or malignant drift active.",
        )
