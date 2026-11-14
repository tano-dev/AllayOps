---
description: Agent productivity workflow, repo-map usage, and verification discipline
trigger: always_on
---

# Agent Workflow & Productivity Standards

1. **Read the Repo Map First:** Before running broad directory scans, inspect `docs/architecture/repo_map.json` to locate modules, scripts, workflows, and docs in one read.
2. **Surgical & Verifiable Edits:** Make minimal, targeted edits. After editing any script, config, or workflow, validate syntax (JSON/YAML/Python/PowerShell) before reporting completion.
3. **Conventional Commits:** Whenever preparing or suggesting commits, strictly follow `<type>(<scope>): <subject>` as defined in `.github/.gitmessage` and `CONTRIBUTING.md`.
4. **Zero-Secret Discipline:** Never echo, copy, or commit values from `server.properties` (`management-server-secret`, `rcon.password`) or `.env`.
5. **Auto-Synced Repo Map:** `.githooks/pre-commit` automatically runs `python scripts/generate_repo_map.py` when available, keeping `docs/architecture/repo_map.json` up to date for future agent sessions.
