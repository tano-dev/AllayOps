# Security Policy

## Supported Versions

Currently, the `main` branch of **AllayOps** is actively supported with security updates.

| Version | Supported |
| :--- | :---: |
| `main` | :white_check_mark: |

---

## Reporting a Vulnerability

1. **Do NOT open a public GitHub issue.**
2. Use GitHub's **Private Vulnerability Reporting** (`Security -> Advisories -> Report a vulnerability`) or contact the repository maintainers directly.
3. Include reproducible steps, affected files, and potential impact.

---

## Minecraft Server & Agentic Research Threat Model

Because **AllayOps** combines a live Minecraft Fabric server with autonomous/agentic research techniques, the following vectors are classified as **Critical Severity**:

- **Credential & Secret Leakage:** Committing `server.properties` (which contains `management-server-secret` or `rcon.password`), `.env`, API keys, or private keys to Git.
- **RCON / Management Server Exposure:** Exposing RCON (`25575`) or the Minecraft management server port without TLS, strong secrets, or network isolation.
- **Prompt Injection / Unbounded Tool Execution:** Inputs (e.g., in-game chat, logs, or external payloads) attempting to trick an AI agent into executing destructive server commands (`/stop`, `/op`, `rm -rf`, world deletion).
- **Supply Chain / Untrusted Mods:** Introducing unverified `.jar` mods or third-party dependencies without checksum/source verification.
