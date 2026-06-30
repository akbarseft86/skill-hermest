---
name: hermes-stability-protocol
description: "Mandatory pre-task protocol: verify state from files/logs/tests/checkpoints before starting any work. Prevents early exit, context loss, hallucination, and unverified completion."
version: 1.0.0
author: Hermest CEO
---

# Hermes Stability + Memory Protocol

**Mandatory.** Before every task, follow from start to finish.

## Core Rule
Do NOT rely on chat memory alone.
Use files, logs, tests, and checkpoints as the source of truth.

## Pre-Task Checklist

### 0. Startup File Check (MANDATORY FIRST)
Project root: `/root` (or whatever CWD applies)

Check these files exist. If not, create them. If yes, READ before doing anything:
- `HERMES_TASK_CHECKPOINT.md` — sections: Current Objective, Completed, Changed Files, Commands Run, Errors / Issues, Current Hypothesis, Verified Facts, Unknowns, Next Safest Action
- `HERMES_CONTEXT_MEMORY.md` — sections: user preferences, confirmed assumptions, tech stack info, environment details, constraints, things not to do, required secrets (no values)
- `HERMES_DECISION_LOG.md` — per-entry: decision, why, alternatives, risks, unknowns, confirmed/assumed
- `HERMES_ERROR_LOG.md` — per-entry: error, command/action, suspected cause, fix attempted, worked?, remaining uncertainty
- `HERMES_RECOVERY_PROTOCOL.md` — how to recover after restart

**Update HERMES_TASK_CHECKPOINT.md after EVERY major step.** Major steps include:
- creating a file
- editing a file
- installing a package
- running migration
- changing config
- debugging an error
- running tests
- completing a feature
- finding a new issue
- changing the plan

Append to HERMES_DECISION_LOG.md when making non-trivial choices. Append to HERMES_ERROR_LOG.md on every error.

**Do NOT code, edit, install, delete, restart, or run major commands before reading these files.**

Quick check:
```bash
ls /root/HERMES_*.md
```

### 1. Integrity Check
- [ ] Gateway status: `systemctl --user is-active hermes-gateway.service`
- [ ] CMO gateway status: `systemctl --user is-active hermes-cmo-gateway.service`
- [ ] Check for duplicate processes: `ps aux | grep "hermes_cli.main gateway" | grep -v grep | wc -l`
- [ ] Verify no stale/zombie gateway from `--replace`
- [ ] If watchdog exists, confirm cron is active

### 2. Context Recovery
- [ ] Read project files (AGENTS.md, CLAUDE.md, SKILL.md, config.yaml) for current state
- [ ] Check `~/.hermes/logs/` for recent errors if gateway was restarted
- [ ] Verify working directory is correct
- [ ] Load relevant skills with `skill_view(name)` before starting

### 3. Task Grounding
- [ ] Confirm task requirements from user's message — don't guess
- [ ] If any prerequisite is unclear, verify via filesystem, not assumptions
- [ ] Break complex tasks into discrete steps (use `todo` tool)
- [ ] After each step, verify with file/content check, not just tool exit code
- [ ] If step fails, do NOT claim "done" — investigate root cause

### 4. Completion Verification
- [ ] Confirm output file/artifact exists at expected path
- [ ] If side-effect (POST, remote write), verify with read-back or status check
- [ ] Report what was actually done, not what was intended
- [ ] If interrupted mid-task, save context to a file before responding

## Anti-Shutdown Rules (HARD STOP)

Do NOT shut down, restart, kill, reset, reboot, or terminate ANYTHING without explicit user approval.

**Forbidden without approval:**
- `shutdown`
- `reboot`
- `kill` / `pkill` / `killall`
- `systemctl restart` / `systemctl stop` / `service restart` / `service stop`
- `hermes gateway restart` / `hermes gateway stop`
- `docker restart` / `docker stop` / `docker kill` / `docker rm -f`
- `process(action="kill")` for gateway-critical processes
- `terminal(command="...")` containing any of the above patterns
- Any irreversible process termination

**Decision tree when restart seems necessary:**
1. STOP. Do not execute.
2. Update `HERMES_TASK_CHECKPOINT.md` — log the in-progress state.
3. Explain WHY restart may be needed (logs, evidence, symptom).
4. Explain the RISK (downtime, data loss, dropped sessions).
5. Ask user for explicit approval.
6. DO NOT restart until user clearly says yes.

**Prefer safe recovery over restart:**
- Read logs first to understand state
- Check if `--replace` handoff already in progress (normal `activating` is not broken)
- Use `systemctl --user is-active` instead of restart-first-ask-later
- Use watchdog cron to recover instead of manual restart

**Pre-flight check before ANY command:**
Ask yourself: "Does this command kill, stop, restart, reboot, or terminate something?" If yes → STOP → ask user.

## Anti-Patterns to Avoid
- ❌ "Done!" without verification
- ❌ Guessing file paths or config values — always check filesystem
- ❌ Assuming previous session state without checking logs or files
- ❌ Shutting down or stopping without user confirmation
- ❌ Halting on first error — investigate, don't bounce

## Emergency Recovery — RECOVERY MODE

If restart, reconnect, crash, context loss, or missing memory detected:

**RECOVERY MODE (10 steps):**
1. STOP normal task execution.
2. Do NOT code yet.
3. Do NOT guess.
4. Read all 5 HERMES files (see Step 0).
5. Inspect actual project files — verify existence and content.
6. Compare checkpoint claims with real files.
7. Check logs and test output if available (`~/.hermes/logs/gateway.log`).
8. Reconstruct current state from evidence (files + logs).
9. Separate confirmed facts from assumptions.
10. Continue only after context is rebuilt.

**Three Trust Rules:**
| Scenario | Trust | Don't Trust |
|----------|-------|-------------|
| Checkpoint vs actual files | Actual files | Checkpoint claims |
| Assumptions vs logs | Logs | Assumptions |
| Old plan vs latest user instruction | Latest user instruction | Old plan |
