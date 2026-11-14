---
name: safe-research-experiment
description: Design, implement, and benchmark new self-healing or chaos experiments in research/ with deterministic reproducibility and unit-test verification.
---

# Safe Research Experiment Skill

Use this skill when adding a new chaos scenario, ablation, or self-healing algorithm to `research/` or `agentic_plane/`.

## Workflow
1. **Define Hypothesis & Scenario:**
   - Add new deterministic scenarios to `research/chaos_scenarios.py` (following `ChaosScenario` dataclass).
   - Ensure `SafeRconAdapter(dry_run=True)` is used in automated benchmarks so live server worlds are never mutated unintentionally.
2. **Isolate Contracts:**
   - Add any new data contracts in `shared_interfaces/schemas.py` first so planes stay decoupled.
3. **Write Verification Tests:**
   - Add `unittest.TestCase` assertions in `tests/` covering normal behavior, boundary edge cases (e.g., `bool` vs `int`), and failure/rollback paths.
4. **Run & Verify:**
   - Execute `python -m unittest discover -s tests -v`
   - Execute `python -m research.run_benchmark`
   - Run `python scripts/generate_codegraph.py` to confirm 0 boundary violations.
