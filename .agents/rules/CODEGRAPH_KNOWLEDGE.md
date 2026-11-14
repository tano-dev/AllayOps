---
description: AST CodeGraph architecture, 4-plane dependency rules, and auto-sync workflow
trigger: always_on
---

# CodeGraph AST & 4-Plane Dependency Rules

AllayOps maintains a live AST dependency graph at `docs/architecture/codegraph.json` (plus file/symbol index `docs/architecture/repo_map.json`).

## 1. Automated Synchronization
- **Generator:** `python scripts/generate_codegraph.py`
- **Pre-commit Hook:** `.githooks/pre-commit` automatically regenerates both `codegraph.json` and `repo_map.json`, stages them, and **blocks commits** if any architectural boundary violation is detected.

## 2. Strict 4-Plane Dependency Direction
- `shared_interfaces/` is the **leaf contract layer** — it MUST NOT import from `minecraft_plane/`, `observability_plane/`, `agentic_plane/`, or `research/`.
- `minecraft_plane/`, `observability_plane/`, and `agentic_plane/` communicate via `shared_interfaces/` contracts and `EventDrivenControlBus`.
- `research/` and `tests/` orchestrate across planes for chaos experiments and verification.

## 3. Agent Best Practice
- Read `docs/architecture/codegraph.json` first to trace upstream/downstream blast radius in one read instead of grepping the entire repository.
