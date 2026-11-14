# AllayOps

> **Enterprise-Grade Minecraft Fabric Server & Agentic Research Platform**

AllayOps combines a reproducible **Fabric Minecraft Server (MC 26.3 / Loader 0.20.1)** with an enterprise software engineering, CI/CD, and **AI Agentic Productivity** foundation for applying and benchmarking research techniques directly on a live server environment.

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

---

## Governance & Agentic Standards

- **AI Agent Instructions:** Read [AGENTS.md](AGENTS.md) before making any changes.
- **Contributing & Branching:** See [CONTRIBUTING.md](CONTRIBUTING.md).
- **Security Policy:** See [SECURITY.md](SECURITY.md).
- **GitHub Enterprise Setup Guide:** See [docs/guides/GITHUB_ENTERPRISE_SETUP.md](docs/guides/GITHUB_ENTERPRISE_SETUP.md).
