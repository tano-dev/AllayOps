# ADR-002: Decoupling Mods & World Datapacks into a Separate Repository

> **Project:** AllayOps: Autonomous Low-Latency Agentic Ops for Self-Healing Minecraft Servers  
> **Status:** Accepted  
> **Date:** 2026-11-14

## Context
`AllayOps` is focused on the **autonomous agentic self-healing control plane, observability, and research benchmarks**. Mixing Minecraft content assets (`mods/*.jar`, `world/datapacks/`) directly into `AllayOps` pollutes Git history with binary JARs and couples gameplay content updates to agentic code releases.

## Decision
1. Remove `mods_src/` from `AllayOps` so this repository remains 100% focused on the Agentic Ops & Research platform.
2. Maintain all Minecraft modding and world content in a separate repository (`https://github.com/tano-dev/AllayOps-Content.git`) with three folders:
   - `mods_src/` (Fabric mod source code)
   - `mods/` (Curated/built `.jar` mods)
   - `datapacks/` (Server world datapacks)
3. Keep `D:\AllayOps\mods` and `D:\AllayOps\world\datapacks` as **gitignored runtime sync targets** populated by `scripts/sync_content.py` (`make sync-content`), which automatically creates a SHA-256 savepoint via `WorldSavepointManager` before updating.

## Consequences
- **Positive:** `AllayOps` stays 100% focused on Agentic Ops & Research; content updates are versioned independently and safely reversible.
- **Negative:** Contributors must run `make sync-content` after cloning if they want the latest mods and datapacks.
