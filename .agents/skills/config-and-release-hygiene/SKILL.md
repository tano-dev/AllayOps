---
name: config-and-release-hygiene
description: Safely update Minecraft server configs, JVM flags, and prepare Conventional Commits or PRs without leaking secrets or committing runtime artifacts.
---

# Config & Release Hygiene Skill

Use this skill when modifying `server.properties.example`, `.env.example`, `start.bat`, `.github/`, or preparing a Git commit.

## Workflow
1. **Secret & Runtime Boundary Check:**
   - **NEVER** stage or commit `server.properties`, `.env`, `ops.json`, `usercache.json`, `eula.txt`, `world/`, `logs/`, `crash-reports/`, or `*.jar`.
   - Always edit `server.properties.example` or `.env.example` first, then instruct or safely sync non-secret keys to local runtime files.
2. **Validate Before Commit:**
   - Verify JSON/YAML syntax and run `python -m unittest discover -s tests -v`.
   - Check `git status --short` to confirm no forbidden files are tracked.
3. **Conventional Commits:**
   - Format commit messages strictly as `<type>(<scope>): <subject>` (e.g., `perf(server): tune ZGC flags`, `feat(agentic): add parry rule`).
   - Never bypass `.githooks/pre-commit` (`--no-verify`).
