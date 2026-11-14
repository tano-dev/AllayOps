# Contributing to AllayOps

We follow enterprise engineering standards to keep **AllayOps** reproducible, secure, and friendly to both human contributors and AI coding agents.

---

## 1. Git Workflow (GitHub Flow)

`main` is always protected and deployable. Never commit directly to `main` once remote branch protection is enabled.

### Branch Naming Convention
```text
feat/<scope>-<short-description>      # New features or capabilities
fix/<scope>-<short-description>       # Bug fixes
research/<experiment-name>            # Research experiments & benchmarks
docs/<topic>                          # Documentation & ADRs
ci/<workflow-change>                  # CI/CD, hooks, automation
chore/<task>                          # Maintenance, refactoring
```

**Examples:**
- `feat/agentic-tick-telemetry`
- `fix/server-zgc-flags`
- `research/self-healing-chunk-guard`
- `docs/adr-002-telemetry-schema`

---

## 2. Conventional Commits

All commits **must** follow [Conventional Commits](https://www.conventionalcommits.org/) (enforced by `.github/workflows/commitlint.yml`):

```text
<type>(<scope>): <subject>
```

- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- **Scopes:** `server`, `mods`, `agentic`, `research`, `infra`, `ci`, `docs`, `scripts`, `repo`

Configure the local commit template once after cloning:
```powershell
git config commit.template .github/.gitmessage
git config core.hooksPath .githooks
```

---

## 3. Pull Request & Definition of Done (DoD)

Before opening a Pull Request:
1. Ensure `.githooks/pre-commit` passes (no secrets, `.env`, `server.properties`, `world/`, or `*.jar` files).
2. Fill out `.github/pull_request_template.md` completely, including **Verification & Evidence**.
3. Ensure all CI checks (`Repo Hygiene & Config Validation`, `Conventional Commit Check`, `Secret Hygiene Scan`) are green.
4. Request review from the relevant `CODEOWNERS`.
5. Use **Squash and Merge** (or **Rebase and Merge**) to maintain a clean linear history on `main`.
