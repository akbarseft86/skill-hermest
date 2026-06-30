---
name: safe-hermes-self-update
description: Safely prepare a Hermes Agent instance for self-update when the local repo has uncommitted changes and active gateway services.
version: 1.0.0
author: Hermest
license: MIT
---

# Safe Hermes Self-Update

Use this when a user asks whether Hermes should be updated, or wants to update Hermes on a live VPS that may have local modifications, custom bridge code, or active gateway services.

## When to use
- `hermes --version` says an update is available
- `Project: ~/.hermes/hermes-agent`
- there are local git modifications or untracked files
- gateway services are running and must keep working after update

## Goal
Create a recovery point before updating, especially when the Hermes repo is dirty.

## Steps
1. **Load current Hermes state**
   Run:
   - `hermes --version`
   - `hermes status --all`
   - `hermes config path`
   - `hermes config env-path`

2. **Inspect repo state**
   In `~/.hermes/hermes-agent`, capture:
   - current branch
   - current commit SHA
   - `git status --short`
   - `git remote -v`

3. **Check live services before touching anything**
   Inspect:
   - `systemctl --user status hermes-gateway.service hermes-cmo-gateway.service`
   Note whether Telegram / WhatsApp bridge processes are active and whether logs already contain network errors.

4. **Write a pre-update checkpoint note**
   Save a dated markdown file in the workspace, e.g.:
   - `/root/.Hermes/workspace/hermest-preupdate-check-YYYY-MM-DD.md`
   Include version, update lag, config paths, auth status, service state, branch, commit, modified files, untracked files, and risk notes.

5. **Create a safety branch**
   From the repo root:
   - `git branch backup/pre-update-<timestamp>`

6. **Create file-level backups**
   Make a timestamped backup directory, e.g.:
   - `/root/.Hermes/workspace/hermes-backups/<timestamp>`

   Save:
   - `git diff > git-working-tree.diff`
   - `git diff --cached > git-staged.diff`
   - copies of each modified/untracked file using `cp --parents`
   - copies of repo-local config files if present

7. **Archive the backup**
   Create:
   - `/root/.Hermes/workspace/hermes-backups/<timestamp>.tar.gz`

8. **Verify backup actually exists**
   Confirm:
   - safety branch is listed
   - backup directory exists
   - tarball exists
   - expected files are inside the backup directory

9. **Only then consider update**
   Tell the user clearly whether the repo is clean or dirty and whether it is safe to proceed.

10. **Run update with conflict-safe monitoring**
   For live systems, prefer running the update in a tracked background process with completion notification or explicit polling. After it exits, verify:
   - `hermes --version`
   - `git status --short`
   - current branch/commit
   - whether update-created stash/autostash refs exist

11. **Handle post-update local-change conflicts explicitly**
   If update succeeds but restoring local changes fails:
   - do **not** force-apply or overwrite conflicted files
   - record the exact stash/ref and conflicted path(s)
   - preserve the stash until manual review is complete
   - tell the user update is installed, but local customization reconciliation remains pending

12. **Do not restart gateway automatically**
   Updating the codebase does not mean the running gateway process has loaded it. Ask for explicit permission before `systemctl restart`, `service restart`, `hermes gateway service install --replace`, or any stop/kill action. Until permission is granted, report the service as still running on the old process and list restart as pending.

13. **Check import/API compatibility after update**
   If post-update tool/provider refresh shows import errors, treat them as compatibility checks to investigate, not as a reason to rollback immediately. Capture the failing import/module names and verify whether they come from stale local custom code, plugin packages, or upstream refactors.

## Recommended wording to user
- If clean: update is straightforward, then verify services.
- If dirty: say update is possible, but local changes may conflict or be overwritten without backup.

## Recovery assets to preserve
At minimum keep:
- pre-update markdown note
- backup branch name
- backup directory
- tar.gz archive

## Pitfalls
- Do **not** say the system is safe to update before checking `git status --short`.
- Do **not** rely only on a branch name; also save file copies and diffs.
- Do **not** ignore active gateway services; they may need restart/verification after update.
- `hermes status --all` may not reflect profile-specific bridge details, so also inspect systemd services.
- `hermes update` auto-stashes dirty working tree before pulling — it does NOT force-push through conflicts. If local changes conflict with upstream, the stash (`stash@{0}`) is preserved and the working tree is reset clean. Always record the stash ref for later reconciliation.
- After update, `package-lock.json` (or equivalent lockfiles) may show as modified in `git status`. This is expected and not a conflict.
- The running gateway process does NOT pick up the new binary or code after update. Only the filesystem was updated. The user must explicitly restart the service — do not assume or auto-do this.
- Backend refresh warnings (import errors, missing symbols) after update are common when Python packages or internal Hermes module structures changed. They're non-fatal: the running gateway keeps using old cached imports. Treat as investigation items, not update failures.

## Verification checklist
Before finalizing, confirm:
- update availability was checked live
- repo dirtiness was confirmed live
- backup branch was created
- backup files and archive were created
- user received exact paths for recovery
