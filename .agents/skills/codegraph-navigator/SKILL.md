---
name: codegraph-navigator
description: Navigate AllayOps modules, classes, functions, and cross-plane dependencies in one read using the AST CodeGraph (docs/architecture/codegraph.json) and Repo Map before scanning files.
---

# CodeGraph Navigator Skill

Use this skill whenever you need to understand how modules connect, trace the blast radius of a change, or locate where a class/function is defined.

## Workflow
1. **Read the CodeGraph first:** Open `docs/architecture/codegraph.json` (and `docs/architecture/repo_map.json` for non-Python files).
2. **Trace Blast Radius:**
   - Look up the target module in `nodes` to inspect its `plane`, `classes`, `functions`, and `loc`.
   - Filter `edges` where `target == <module>` to find all downstream callers that could break if you change a public signature.
3. **Verify Layer Boundaries:**
   - Confirm `summary.boundary_violations` is empty (`[]`).
   - Never introduce an import from `shared_interfaces` to `minecraft_plane`, `observability_plane`, `agentic_plane`, or `research`.
4. **Refresh After Structural Edits:**
   - Run `python scripts/generate_codegraph.py` after adding, renaming, or refactoring Python modules.
