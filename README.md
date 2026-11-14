# AllayOps: Autonomous Low-Latency Agentic Ops for Self-Healing Minecraft Servers

> **Enterprise-Grade Minecraft Fabric Server & Safe Agentic Research Platform**

AllayOps combines a reproducible **Fabric Minecraft Server (MC 26.3 / Loader 0.20.1)** with an enterprise software engineering, CI/CD, and **AI Agentic Productivity** foundation for applying and benchmarking research techniques directly on a live server environment.

### Research Lineage
AllayOps is the domain-applied sister project of [**Safe-Agentic-DataOps for Self-Healing Real-Time E-Commerce Data Pipelines**](https://github.com/tano-dev/Safe-Agentic-DataOps-for-Self-Healing-Real-Time-E-Commerce-Data-Pipelines), adapting its core self-healing mechanisms (`ADWIN` drift detection, `Drain` log compression, `<50ms` In-Flight Active Parry, `Constitutional Safety Gate`, `Tree of Thoughts`, `Closed-Loop Canary Gate`, and `DPO` preference logging) to real-time Minecraft server operations.

---

## Architecture & Repository Layout

```text
AllayOps/
├── .github/                  # Enterprise CI/CD, security scans, Dependabot, PR/Issue templates, CODEOWNERS
├── .githooks/                # Version-controlled Git hooks (secret & binary guardrails)
├── .agents/                  # Agentic rules, knowledge base, and repo-map automation
├── AGENTS.md                 # Root system prompt & safety guardrails for AI coding agents
├── docs/
│   ├── architecture/         # Architecture Decision Records (ADRs)
│   └── guides/               # Onboarding, GitHub Enterprise setup, and operational runbooks
├── scripts/                  # Automation scripts (repo setup, repo-map generator, server helpers)
├── server.properties.example # Safe server configuration template (no secrets)
├── .env.example              # Safe environment variable template
├── start.bat                 # JVM ZGC startup script (JDK 25, 6G-8G heap)
├── CONTRIBUTING.md           # Git workflow, Conventional Commits, and PR standards
├── SECURITY.md               # Vulnerability disclosure & Agentic/Minecraft threat model
└── CODE_OF_CONDUCT.md        # Contributor Covenant v2.1
```

> **Note:** Runtime Minecraft state (`world/`, `logs/`, `crash-reports/`, `libraries/`, `versions/`, `.fabric/`, `*.jar`, `server.properties`, `eula.txt`, `ops.json`) is intentionally excluded from Git via `.gitignore` to keep the repository clean, fast, and secret-free.

---

## Quickstart

### 1. Local Git & Hook Setup (First-time Clone)
```powershell
git config core.hooksPath .githooks
git config commit.template .github/.gitmessage
```

### 2. Server Configuration
1. Copy `server.properties.example` to `server.properties` and set a strong `management-server-secret` / `rcon.password`.
2. Copy `.env.example` to `.env` and populate your local secrets.
3. Ensure `eula.txt` has `eula=true` and JDK 25 is installed.
4. Launch the server with `start.bat`.

### 3. Sync External Mods & Datapacks (Optional)
`AllayOps` focuses strictly on the **Agentic Self-Healing System**. Mods (`mods/`) and world datapacks (`world/datapacks/`) are maintained in a separate repository (`AllayOps-Content`) and pinned via [`content-manifest.json`](content-manifest.json):
```powershell
python scripts/sync_content.py --dry-run   # preview
python scripts/sync_content.py             # sync with pre-update savepoint
```

---

## Governance & Agentic Standards

- **AI Agent Instructions:** Read [AGENTS.md](AGENTS.md) before making any changes.
- **Contributing & Branching:** See [CONTRIBUTING.md](CONTRIBUTING.md).
- **Security Policy:** See [SECURITY.md](SECURITY.md).
- **GitHub Enterprise Setup Guide:** See [docs/guides/GITHUB_ENTERPRISE_SETUP.md](docs/guides/GITHUB_ENTERPRISE_SETUP.md).
