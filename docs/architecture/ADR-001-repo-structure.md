# ADR-001: Separation of Runtime Minecraft State from Version-Controlled Repository

> **Project:** AllayOps: Autonomous Low-Latency Agentic Ops for Self-Healing Minecraft Servers  
> **Status:** Accepted  
> **Date:** 2026-11-14

## Context
A live Fabric Minecraft server generates large binary files (`*.jar`, `libraries/`, `versions/`, `world/*.mca`), rotating logs (`logs/`, `crash-reports/`), and runtime secrets (`server.properties` containing `management-server-secret` and `rcon.password`). Committing these directly to Git bloats repository history, causes merge conflicts, and leaks credentials.

## Decision
1. Exclude all Minecraft runtime state, binaries, worlds, and live secret files via `.gitignore`.
2. Track safe templates (`server.properties.example`, `.env.example`) and startup scripts (`start.bat`) in Git.
3. Enforce this boundary at two layers:
   - **Local:** `.githooks/pre-commit` blocks staging runtime/secret files and scans diffs for API keys.
   - **CI:** `.github/workflows/ci.yml` and `.github/workflows/security.yml` fail builds if forbidden files or secrets enter the tree.

## Consequences
- **Positive:** Fast clones, clean diffs, zero secret leakage, reproducible server configuration.
- **Negative:** New contributors must copy `server.properties.example` -> `server.properties` and supply their own Fabric server JAR/runtime on first boot.
