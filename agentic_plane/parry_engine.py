"""System-1 (< 50ms) In-Flight Active Parry Engine for Minecraft Server."""

from __future__ import annotations

import time

from shared_interfaces.schemas import ParryResult, TickTelemetry


class AllayOpsParryEngine:
    """Deflects runaway tick hazards (e.g. TNT chains, poison chat) in < 50ms."""

    def __init__(self, tnt_threshold: int = 50, entity_threshold: int = 1500) -> None:
        self.tnt_threshold = tnt_threshold
        self.entity_threshold = entity_threshold
        self.immunized_signatures: set[str] = set()

    def evaluate_tick(self, telemetry: TickTelemetry, signature: str = "") -> ParryResult:
        """Evaluate tick telemetry and emit an immediate System-1 parry if needed."""
        start = time.perf_counter()

        if signature and signature in self.immunized_signatures:
            elapsed = (time.perf_counter() - start) * 1000.0
            return ParryResult(
                parried=True,
                action="STAGGER_LOCKOUT",
                latency_ms=elapsed,
                target_signature=signature,
                vaccine_generated=False,
            )

        if telemetry.tnt_count >= self.tnt_threshold:
            sig = signature or "MC_TNT_CHAIN_SPIKE"
            self.immunized_signatures.add(sig)
            elapsed = (time.perf_counter() - start) * 1000.0
            return ParryResult(
                parried=True,
                action="clear_tnt_bounded",
                latency_ms=elapsed,
                target_signature=sig,
                vaccine_generated=True,
            )

        if telemetry.entity_count >= self.entity_threshold and telemetry.mspt >= 45.0:
            sig = signature or "MC_ENTITY_OVERLOAD"
            self.immunized_signatures.add(sig)
            elapsed = (time.perf_counter() - start) * 1000.0
            return ParryResult(
                parried=True,
                action="tick_freeze",
                latency_ms=elapsed,
                target_signature=sig,
                vaccine_generated=True,
            )

        elapsed = (time.perf_counter() - start) * 1000.0
        return ParryResult(
            parried=False,
            action="NONE",
            latency_ms=elapsed,
            target_signature=signature or "HEALTHY",
            vaccine_generated=False,
        )
