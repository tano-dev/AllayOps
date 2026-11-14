# GitHub Enterprise Setup Guide (A to Z)

This guide walks through connecting **AllayOps** to GitHub and enabling enterprise-grade repository governance, branch protection, and security controls.

---

## Step 1: Create the Remote Repository on GitHub

1. Create a new repository named **`AllayOps`** on GitHub (Private or Public).
2. **Do NOT** initialize it with a README, `.gitignore`, or License (we already created enterprise versions locally).
3. Connect and push your local `main` branch:
   ```powershell
   git remote add origin https://github.com/<YOUR_USERNAME>/AllayOps.git
   git push -u origin main
   ```

---

## Step 2: General Repository Settings

Go to **Settings -> General**:
- **Default branch:** `main`
- **Pull Requests:**
  - Enable **Allow squash merging** (recommended: *Pull request title* as default commit message so Conventional Commits stay clean on `main`).
  - Disable **Allow merge commits** (keeps history linear).
  - Enable **Automatically delete head branches** after merge.

---

## Step 3: Branch Ruleset on `main` (Enterprise Standard)

Go to **Settings -> Rules -> Rulesets -> New branch ruleset**:
- **Ruleset Name:** `Protect main`
- **Enforcement status:** `Active`
- **Target branches:** `Include default branch` (`main`)
- **Rules to enable:**
  1. **Restrict deletions** (prevent deleting `main`)
  2. **Block force pushes**
  3. **Require a pull request before merging**:
     - Required approvals: `1` (set `0` if solo developer, `1+` for team)
     - Dismiss stale pull request approvals when new commits are pushed: `Enabled`
     - Require review from Code Owners (`.github/CODEOWNERS`): `Enabled`
     - Require conversation resolution before merging: `Enabled`
  4. **Require status checks to pass**:
     - Require branches to be up to date before merging: `Enabled`
     - Add required checks:
       - `Repo Hygiene & Config Validation`
       - `Conventional Commit Check`
       - `Secret Hygiene Scan`
  5. **Require linear history**: `Enabled`

---

## Step 4: Security & Analysis

Go to **Settings -> Code security and analysis**:
- **Private vulnerability reporting:** `Enable`
- **Dependency graph:** `Enable`
- **Dependabot alerts:** `Enable`
- **Dependabot security updates:** `Enable`
- **Secret scanning:** `Enable` (and **Push protection**: `Enable`)

---

## Step 5: Update Placeholders

1. In `.github/CODEOWNERS`, replace `@tanokido85` with your exact GitHub handle or `@org/team`.
2. In `.github/ISSUE_TEMPLATE/config.yml`, replace `OWNER` with your GitHub username/organization.
