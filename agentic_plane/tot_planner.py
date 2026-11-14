"""System-2 3-Branch Tree of Thoughts (ToT) Root-Cause Planner."""

from __future__ import annotations

from shared_interfaces.schemas import ActionProposal, IncidentContext, ThoughtHypothesis


class TreeOfThoughtsPlanner:
    """Evaluates 3 parallel Minecraft failure branches and prunes weak hypotheses."""

    def __init__(self, prune_threshold: float = 0.60) -> None:
        self.prune_threshold = prune_threshold

    def diagnose(self, incident: IncidentContext) -> tuple[ThoughtHypothesis, list[ThoughtHypothesis]]:
        """Generate H1 (World/Entity), H2 (JVM/IO), H3 (Mod/Config) and pick winner."""
        text = (incident.summary + " " + " ".join(incident.log_templates)).lower()

        h1_score = 0.90 if any(k in text for k in ("tnt", "explosion", "entity", "watchdog")) else 0.35
        h2_score = 0.88 if any(k in text for k in ("heap", "zgc", "outofmemory", "disk")) else 0.30
        h3_score = 0.85 if any(k in text for k in ("mod", "fabric", "mixin", "properties")) else 0.25

        candidates = [
            ThoughtHypothesis(
                branch="world_entity",
                hypothesis="Runaway entity or PrimedTnt explosion chain blocking main server tick.",
                confidence=h1_score,
                recommended_action=ActionProposal(
                    action_type="clear_tnt_bounded",
                    parameters={"radius": 32},
                    rationale="Defuse active TNT entities in bounded radius without touching world saves.",
                    confidence=h1_score,
                ),
                pruned=h1_score < self.prune_threshold,
            ),
            ThoughtHypothesis(
                branch="jvm_io",
                hypothesis="JVM heap pressure or world save I/O bottleneck stalling tick loop.",
                confidence=h2_score,
                recommended_action=ActionProposal(
                    action_type="save_all",
                    parameters={},
                    rationale="Flush chunks safely before adjusting view-distance or restarting.",
                    confidence=h2_score,
                ),
                pruned=h2_score < self.prune_threshold,
            ),
            ThoughtHypothesis(
                branch="mod_config",
                hypothesis="Fabric mod mixin conflict or misconfigured server.properties.",
                confidence=h3_score,
                recommended_action=ActionProposal(
                    action_type="say_alert",
                    parameters={"message": "Mod/config anomaly detected; preparing safe rollback."},
                    rationale="Notify operators and prepare config savepoint rollback.",
                    confidence=h3_score,
                ),
                pruned=h3_score < self.prune_threshold,
            ),
        ]

        winner = max(candidates, key=lambda h: h.confidence)
        return winner, candidates
