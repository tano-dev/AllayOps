# ADR-002: Decoupling Mods & World Datapacks into a Separate Repository

> **Project:** AllayOps: Autonomous Low-Latency Agentic Ops for Self-Healing Minecraft Servers  
> **Status:** Accepted  
> **Date:** 2026-11-14

## Context
`AllayOps` is focused on the **autonomous agentic self-healing control plane, observability, and research benchmarks**. Mixing Minecraft content assets (`mods/*.jar`, `world/datapacks/`) directly into `AllayOps` pollutes Git history with binary JARs and couples gameplay content updates to agentic code releases.

## Decision
1. Maintain Minecraft mods and world datapacks in a separate repository (default: `https://github.com/tano-dev/AllayOps-Content.git`) with two top-level folders:
   - `mods/` (Fabric mods / release assets)
   - `datapacks/` (Server datapacks)
2. Pin the remote repository and target branch/tag in [`content-manifest.json`](../../content-manifest.json).
3. Sync content into local runtime directories (`mods/`, `world/datapacks/`) via `scripts/sync_content.py` (`make sync-content`), which automatically creates a SHA-256 savepoint via `WorldSavepointManager` before updating.

## Consequences
- **Positive:** `AllayOps` stays 100% focused on Agentic Ops & Research; content updates are versioned independently and safely reversible.
- **Negative:** Contributors must run `make sync-content` after cloning if they want the latest mods and datapacks.
