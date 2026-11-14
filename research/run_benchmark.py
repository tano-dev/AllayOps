"""Reproducible end-to-end benchmark runner for AllayOps."""

from __future__ import annotations

import json
import time
from dataclasses import asdict
from pathlib import Path

from agentic_plane.canary_gate import CanaryVerificationGate
from agentic_plane.parry_engine import AllayOpsParryEngine
from agentic_plane.policy_validator import PolicyValidator
from agentic_plane.tot_planner import TreeOfThoughtsPlanner
from minecraft_plane.rcon_adapter import SafeRconAdapter
from observability_plane.adwin_detector import MinecraftDriftClassifier
from observability_plane.drain_parser import DrainLogParser
from research.chaos_scenarios import CANONICAL_MC_SCENARIOS
from shared_interfaces.control_bus import ControlEvent, EventDrivenControlBus
from shared_interfaces.schemas import IncidentContext


def run_canonical_suite() -> list[dict]:
    """Execute all canonical Minecraft chaos scenarios through the 4-plane pipeline."""
    classifier = MinecraftDriftClassifier()
    parry = AllayOpsParryEngine()
    drain = DrainLogParser()
    planner = TreeOfThoughtsPlanner()
    validator = PolicyValidator()
    rcon = SafeRconAdapter(dry_run=True)
    canary = CanaryVerificationGate()
    bus = EventDrivenControlBus()

    results: list[dict] = []
    for scenario in CANONICAL_MC_SCENARIOS:
        t0 = time.perf_counter()
        drift = classifier.evaluate_mspt_stream(
            scenario.mspt_series,
            has_watchdog_warning=any("Watchdog" in line for line in scenario.raw_logs),
        )

        if drift.suppress_alert:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            results.append(
                {
                    "code": scenario.code,
                    "drift_type": drift.drift_type,
                    "suppressed": True,
                    "parried": False,
                    "safety_blocked_poison": False,
                    "canary_status": "SKIPPED_BENIGN",
                    "decision_ms": round(elapsed_ms, 3),
                }
            )
            continue

        parry_res = parry.evaluate_tick(scenario.telemetry, signature=scenario.code)
        templates = drain.summarize_for_llm(scenario.raw_logs)
        incident = IncidentContext(
            incident_id=f"INC-{scenario.code}",
            scenario_code=scenario.code,
            summary=scenario.title,
            severity="CRITICAL",
            mspt_series=tuple(scenario.mspt_series),
            log_templates=tuple(templates),
        )

        poison_blocked = False
        if scenario.poison_proposal is not None:
            poison_verdict = validator.validate(scenario.poison_proposal)
            poison_blocked = not poison_verdict.allowed

        winner, _ = planner.diagnose(incident)
        verdict = validator.validate(winner.recommended_action)
        if verdict.allowed:
            rcon.execute(winner.recommended_action)
            bus.publish(
                ControlEvent(
                    event_type="ACTION_EXECUTED",
                    source_plane="agentic_plane",
                    payload={"scenario": scenario.code, "action": winner.recommended_action.action_type},
                )
            )

        # Simulated post-remediation steady-state tick check
        canary_res = canary.evaluate(savepoint_id=f"sp-{scenario.code}", mspt=18.5, error_log_rate=0.0)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        results.append(
            {
                "code": scenario.code,
                "drift_type": drift.drift_type,
                "suppressed": False,
                "parried": parry_res.parried,
                "parry_action": parry_res.action,
                "tot_winner_branch": winner.branch,
                "safety_allowed": verdict.allowed,
                "safety_blocked_poison": poison_blocked,
                "canary_status": canary_res.status,
                "health_score": canary_res.health_score,
                "decision_ms": round(elapsed_ms, 3),
            }
        )
    return results


def main() -> None:
    report = run_canonical_suite()
    print(json.dumps(report, indent=2))
    out_path = Path("scratch/latest_mc_benchmark.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
