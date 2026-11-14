---
name: mc-incident-triage
description: Triage Minecraft Fabric server crashes, Watchdog freezes, and TPS/MSPT lag spikes using DrainLogParser, ADWINDetector, AllayOpsParryEngine, and PolicyValidator.
---

# Minecraft Incident Triage Skill

Use this skill when investigating a server crash (`crash-reports/*.txt`), tick lag (`logs/latest.log`), or Watchdog termination.

## Workflow
1. **Inspect Evidence (Read-Only):**
   - Read the latest `crash-reports/crash-*.txt` header (`Description:`, `Thread:`, top stack frames) and tail of `logs/latest.log`.
   - Never fabricate TPS/MSPT numbers or stack traces.
2. **Compress & Classify:**
   - Use `observability_plane.drain_parser.DrainLogParser` to collapse repetitive log lines into templates.
   - Use `observability_plane.adwin_detector.MinecraftDriftClassifier` to separate `BENIGN_PLAYER_SURGE` from `MALIGNANT_LAG_ANOMALY`.
3. **Select Remediation Tier:**
   - **Tier 1 (< 50ms):** If TNT/entity spike threatens `max-tick-time=60000`, route through `AllayOpsParryEngine.evaluate_tick`.
   - **Tier 2 (Root Cause):** Use `TreeOfThoughtsPlanner.diagnose` across `world_entity`, `jvm_io`, and `mod_config`.
4. **Enforce Safety & Verification:**
   - Validate every proposed action through `PolicyValidator.validate` before touching `SafeRconAdapter`.
   - Create a savepoint via `WorldSavepointManager` before config/world changes and verify with `CanaryVerificationGate`.
