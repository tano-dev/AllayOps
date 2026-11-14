---
description: Core context for AllayOps Minecraft Fabric Server and repository boundaries
trigger: always_on
---

# AllayOps Project Context

## 1. Runtime Environment
- **Minecraft Server:** Fabric (`fabric-server-mc.26.3-loader.0.20.1-launcher.1.1.2.jar`)
- **Java Runtime:** Eclipse Adoptium JDK 25 (`-Xms6G -Xmx8G -XX:+UseZGC -XX:+AlwaysPreTouch`)
- **Server Port:** `2026` (configured in `server.properties`)

## 2. Version-Controlled vs. Runtime-Only Boundary
- **Tracked in Git:** `.github/`, `.githooks/`, `.agents/`, `AGENTS.md`, `docs/`, `scripts/`, `start.bat`, `server.properties.example`, `.env.example`, and future `research/` / `agentic/` / `mods-src/` code.
- **Excluded from Git (`.gitignore`):** `world/`, `logs/`, `crash-reports/`, `.fabric/`, `libraries/`, `versions/`, `*.jar`, `server.properties` (contains `management-server-secret`), `ops.json`, `usercache.json`, `eula.txt`, `.env`.
- **Rule for Agents:** When modifying server configuration defaults, update `server.properties.example` (never commit `server.properties`), and instruct the user if they need to sync local `server.properties`.
