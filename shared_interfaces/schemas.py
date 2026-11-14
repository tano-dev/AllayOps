"""Immutable contracts shared across AllayOps planes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


def utc_now_iso() -> str:
    """Return an ISO-8601 UTC timestamp."""
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class TickTelemetry:
    """Point-in-time Minecraft server tick and entity telemetry."""

    mspt: float
    tps: float
    player_count: int
    entity_count: int
    tnt_count: int = 0
    chunks_loaded: int = 0
    error_log_rate: float = 0.0
    timestamp: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True)
class IncidentContext:
    """Normalized anomaly context passed from Observability to Agentic Plane."""

    incident_id: str
    scenario_code: str
    summary: str
    severity: str
    mspt_series: tuple[float, ...] = ()
    error_rate_series: tuple[float, ...] = ()
    log_templates: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now_iso)


@dataclass(frozen=True)
class ActionProposal:
    """Untrusted remediation action proposed by an LLM or heuristic planner."""

    action_type: str
    parameters: dict[str, Any] = field(default_factory=dict)
    rationale: str = ""
    confidence: float = 0.0


@dataclass(frozen=True)
class SafetyVerdict:
    """Deterministic result from PolicyValidator."""

    allowed: bool
    reason: str
    violated_rule: str | None = None


@dataclass(frozen=True)
class ParryResult:
    """Outcome of a sub-50ms System-1 In-Flight Active Parry evaluation."""

    parried: bool
    action: str
    latency_ms: float
    target_signature: str
    vaccine_generated: bool = False


@dataclass(frozen=True)
class CanaryResult:
    """Outcome of Closed-Loop Canary Verification."""

    status: str  # "PROMOTED" | "ROLLBACK_TRIGGERED"
    health_score: float
    savepoint_id: str
    reason: str


@dataclass(frozen=True)
class ThoughtHypothesis:
    """Single reasoning branch in Tree of Thoughts (ToT) diagnosis."""

    branch: str  # "world_entity" | "jvm_io" | "mod_config"
    hypothesis: str
    confidence: float
    recommended_action: ActionProposal
    pruned: bool = False


@dataclass(frozen=True)
class DPOPreferencePair:
    """Preference triplet (x, y_w, y_l) for Direct Preference Optimization."""

    incident_id: str
    prompt: str
    chosen: dict[str, Any]
    rejected: dict[str, Any]
    source: str
    timestamp: str = field(default_factory=utc_now_iso)
