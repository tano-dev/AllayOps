# AGENTS.md (System Prompt)

> **Context:** This is **AllayOps** (*Autonomous Low-Latency Agentic Ops for Self-Healing Minecraft Servers*) — an enterprise-grade Minecraft Fabric Server (MC 26.3 / Loader 0.20.1, JDK 25 with ZGC) integrated with a Safe Agentic & Research platform, derived from [Safe-Agentic-DataOps](https://github.com/tano-dev/Safe-Agentic-DataOps-for-Self-Healing-Real-Time-E-Commerce-Data-Pipelines).

## 1. Coding Principles (Karpathy's Rules)
- **Think Before Coding:** Explicitly state assumptions before implementing. If multiple approaches exist, expose tradeoffs and ask the user.
- **Simplicity First:** Minimum code to solve the problem. No speculative features or over-engineering.
- **Surgical Changes:** Touch ONLY what is necessary. Do not reformat adjacent code or rewrite unrelated comments.
- **Goal-Driven Execution:** Transform tasks into verifiable goals (e.g., "fix config" -> "validate schema/syntax and verify server boot").

## 2. NEVER DO
- **NEVER** commit `server.properties`, `.env`, `ops.json`, `usercache.json`, `eula.txt`, `world/`, `logs/`, or `*.jar` binaries.
- **NEVER** hardcode secrets (`management-server-secret`, `rcon.password`, API keys) in tracked files or documentation.
- **NEVER** run destructive server/git commands (`rm -rf world`, `git push --force`, `git reset --hard`) without explicit user consent.
- **NEVER** bypass `.githooks/pre-commit` (`--no-verify`) or CI validation checks.
- **NEVER** invent or fake server telemetry, TPS/MSPT metrics, or test results.

## 3. Centralized Commands & Workflow
- **AST CodeGraph & Repo Map (Fast Context):** Read `docs/architecture/codegraph.json` and `docs/architecture/repo_map.json` before scanning the whole repository.
- **Regenerate Maps:** `python scripts/generate_codegraph.py` & `python scripts/generate_repo_map.py` (also run automatically in `.githooks/pre-commit`).
- **Workspace Skills:** Check `.agents/skills/` (`codegraph-navigator`, `mc-incident-triage`, `safe-research-experiment`, `config-and-release-hygiene`).
- **Start Minecraft Server:** `.\start.bat` (uses JDK 25, ZGC, 6G–8G heap).
- **Validate Repo Hygiene:** Check `git status` and ensure no forbidden runtime/secret files are staged.

## 4. Safety & Permissions
- **Allowed without asking:** Read/list files, run `git status`/`git diff`, run `python scripts/generate_repo_map.py`, run unit tests or single-file linters.
- **MUST ask first:** `git push` to remote, modifying `server.properties` live secrets, deleting `world/` data, installing new external dependencies or mods.

## 5. Progressive Disclosure (Where to Find Things)
Do not guess the architecture. Read these references when you need deeper context:
- **Onboarding & Local Setup:** `docs/guides/ONBOARDING.md`
- **GitHub Enterprise Setup (Branch Protection, Rulesets, Secrets):** `docs/guides/GITHUB_ENTERPRISE_SETUP.md`
- **Architecture Decision Records:** `docs/architecture/ADR-001-repo-structure.md`
- **Security & Threat Model:** `SECURITY.md`
- **Git & PR Standards:** `CONTRIBUTING.md`

## 6. When Stuck
- If an issue takes more than **3 attempts** to resolve, **STOP**. Summarize what you observed, expose the blockers/tradeoffs, and ask the user before proceeding.
