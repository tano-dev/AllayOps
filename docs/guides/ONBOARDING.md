# Onboarding Guide — AllayOps

> **AllayOps: Autonomous Low-Latency Agentic Ops for Self-Healing Minecraft Servers**

Welcome to **AllayOps**! This guide helps both human engineers and AI coding agents get productive immediately.

## 1. Local Git Setup
Run once after cloning:
```powershell
git config core.hooksPath .githooks
git config commit.template .github/.gitmessage
```

## 2. Minecraft Server Setup
1. Ensure **Eclipse Adoptium JDK 25** is installed (`C:\Program Files\Eclipse Adoptium\jdk-25*`).
2. Copy `server.properties.example` to `server.properties` (if not already present) and configure your local secrets.
3. Copy `.env.example` to `.env` for local research/agentic keys.
4. Start the server:
   ```powershell
   .\start.bat
   ```

## 3. Research & Development Workflow
1. Always branch off `main`: `git checkout -b research/<experiment-name>` or `feat/<scope>-<name>`.
2. Keep `AGENTS.md` and `docs/architecture/repo_map.json` updated as new modules are added.
3. Open a Pull Request using `.github/pull_request_template.md` and wait for CI checks to pass.
