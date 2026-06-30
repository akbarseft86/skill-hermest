---
name: openclaw-to-hermes-migration-audit
description: Audit a mixed OpenClaw/Hermes server during migration, identify what is already running, map Telegram bot identities to services, and determine what is still missing before cutover.
version: 1.0.1
author: Hermes Agent
license: MIT
---

# OpenClaw to Hermes Migration Audit

Use this skill when a user says they already migrated from OpenClaw to Hermes, wants to know whether migration is complete, or plans to repurpose old OpenClaw bots as Hermes bots (for example CEO/CMO split).

## When to use
- User asks whether everything is already running on Hermes
- User has both `hermes-gateway.service` and `openclaw-gateway.service`
- User wants to turn the legacy OpenClaw bot into a Hermes bot without changing the Telegram username/token
- User needs a grounded status report: what is already migrated vs what is still legacy

## Key findings from real migrations
- `hermes status --all` alone is not enough; it can show Telegram configured and gateway running while migration is still incomplete.
- A server can be in a mixed state: one Hermes gateway plus one legacy OpenClaw gateway.
- `hermes profile list` may show only `default`, and `~/.hermes/profiles/` may not even exist yet. That means the planned multi-profile setup (e.g. `ceo` / `cmo`) has not actually been created.
- Hermes can already own one Telegram bot while the legacy OpenClaw service still owns a second bot.
- The fastest way to map real bot identity is to inspect the active Hermes/OpenClaw config sources and validate each configured Telegram bot via the Telegram API, without exposing secrets in outputs or notes.
- Migration artifacts under `~/.hermes/migration/openclaw/<timestamp>/` are strong evidence that migration was run before; use `summary.md`, `MIGRATION_NOTES.md`, and archived workspace files to see what did and did not come over.
- Identity drift is common after migration: the Hermes bot display name may already be updated, while config still contains legacy mention patterns or persona remnants (for example `raden`). Call this out explicitly.
- Do not recommend deleting OpenClaw if the replacement Hermes instances do not yet exist. A mixed state is not the same as a finished migration.

## Audit procedure

### 1. Check live service state
Run:
```bash
hermes status --all
hermes gateway status
systemctl --user list-units --type=service --all | grep -Ei 'hermes|openclaw|claw' || true
```

What to extract:
- Is Hermes gateway running?
- Is OpenClaw gateway still running?
- What model/provider is Hermes currently using?
- Is Telegram configured in Hermes?

### 2. Check whether planned Hermes profiles actually exist
Run:
```bash
hermes profile list
```
Optionally also inspect whether `~/.hermes/profiles/` exists.

Interpretation:
- Only `default` present -> multi-bot/profile migration is not built yet
- Missing `ceo` / `cmo` -> target architecture still not implemented

### 3. Locate the active Hermes config and env
Run:
```bash
hermes config path
hermes config env-path
```
Then inspect the active `config.yaml` and env file.

Look for:
- current Hermes model/provider
- Telegram mention patterns
- presence of Telegram credential/allowlist variables
- whether config still contains legacy identity cues

### 4. Read the legacy OpenClaw config
Inspect:
```bash
/root/.openclaw/openclaw.json
```

Extract:
- Telegram enabled?
- WhatsApp enabled?
- group policy / allowlist
- any group IDs or allow-from values
- whether the file still defines a live Telegram bot

### 5. Validate both Telegram bot identities directly
Validate the Hermes-configured bot and the OpenClaw-configured bot with Telegram `getMe`, but never print or store raw secrets.

Return and compare only:
- bot id
- username
- first_name
- can_join_groups

This distinguishes the real case:
- two different bots can coexist safely
- conflict only happens if two services poll the same token

### 6. Check migration artifacts
Search under:
```bash
~/.hermes/migration/openclaw/
```
Read at minimum:
- `summary.md`
- `MIGRATION_NOTES.md`
- archived `workspace/IDENTITY.md`

Use these to answer:
- Was migration actually run?
- How many items migrated vs archived vs conflicted?
- Which pieces still require manual recreation?
- What persona/identity was preserved only in the archive?

### 7. Identify migration completeness
Call out separately:

**Already migrated**
- Hermes gateway running
- Telegram configured in Hermes
- one bot identity already owned by Hermes
- migration archive exists

**Not yet migrated**
- missing target profiles (`ceo`, `cmo`)
- legacy OpenClaw service still active
- archived identity/workspace material not yet mapped
- legacy mention patterns/persona remnants still present
- WhatsApp still only present in OpenClaw, not Hermes

## How to present results to the user
Use a blunt state summary:
- “Run? yes/no”
- “Full Hermest migration? yes/no”
- “Still mixed with legacy? yes/no”
- “2 target Hermes roles/profiles already exist? yes/no”

Then provide:
1. current-state mapping (which bot is owned by which engine)
2. target-state mapping (e.g. Hermes CEO vs Hermes CMO)
3. blockers preventing OpenClaw retirement
4. safest next step

## Important reasoning rules
- Do not equate “gateway running” with “migration complete”.
- Do not recommend deleting OpenClaw merely because a migration archive exists.
- If the user wants the old OpenClaw Telegram bot to become a Hermes bot, recommend reusing the same Telegram identity under a dedicated Hermes instance/profile.
- For two Telegram bots with separate identities, prefer separate Hermes homes or clearly isolated profiles to avoid config/env confusion.
- If WhatsApp exists only in OpenClaw config, say plainly that WhatsApp has not yet been migrated to Hermes.

## 8. If a dedicated Hermes home exists (for example `/root/.hermes-cmo`), audit whether the old bot's journey/context actually came over
This is a common failure mode: the legacy migration was run into `/root/.hermes`, but the repurposed bot now runs from a different `HERMES_HOME` such as `/root/.hermes-cmo`.

### Verify the real home used by the bot service
Inspect the unit file and process environment. Look for:
- `Environment="HERMES_HOME=..."` in the systemd user service
- `HOME`, `HERMES_HOME`, and PID environment for the running gateway

### Compare old workspace context vs the dedicated Hermes home
Check whether the dedicated Hermes home actually contains the old context-bearing files.

Priority files/directories to compare:
- workspace instruction/bootstrap files
- `HEARTBEAT.md`
- `IDENTITY.md`
- `MEMORY.md`
- `SOUL.md`
- `TOOLS.md`
- `USER.md`
- `memory/`
- `hooks/`
- `vault/`
- `rag_storage/`
- `inputs/`
- `state/`

Interpretation:
- If only `IDENTITY.md`, `SOUL.md`, and `skills/` exist in the dedicated Hermes home, the persona shell exists but the old journey/context was not fully cloned.
- If `memories/` is empty or `MEMORY.md` is missing, the bot likely does not know the old long-term context.
- If `sessions/` only starts from the new cutover date, conversation history was not migrated into that new home.
- If `SOUL.md` is still generic/default, identity migration is incomplete even if the bot is already live.

### Check archive + old workspace together
Do not only inspect the migration archive. Also compare against the still-present legacy workspace under `/root/.openclaw/workspace`.
- Some important files may still exist only in the live legacy workspace.
- Some others may exist only in `~/.hermes/migration/openclaw/<timestamp>/archive/workspace/`.

### Report this explicitly to the user
Add a dedicated section:
- `Old files cloned into dedicated CMO/CEO home? yes/no`
- `Does the new bot know the old journey/history? yes/no/partial`
- `Where the missing context still lives` (legacy workspace vs migration archive)
- `Safe first merge set` (`MEMORY.md`, `USER.md`, `TOOLS.md`, `memory/`) before broader operational folders

## 9. Safe curated knowledge migration into the dedicated Hermes home
When the user says some variant of "terserah gimana caranya, kamu atur aja yang aman" or otherwise clearly delegates the method, treat that as permission to proceed with a **safe curated migration** rather than waiting for more clarification.

### Goal
Carry over **knowledge and journey/history** from OpenClaw into the dedicated Hermes home, without importing legacy runtime state that can break or confuse the new bot.

### Import directly or rewrite
Safe to import or rewrite into the dedicated Hermes home:
- old `workspace/USER.md` -> rewrite into `~/.hermes-cmo/memories/USER.md`
- old `workspace/MEMORY.md` -> rewrite or summarize into `~/.hermes-cmo/memories/MEMORY.md`
- selected `workspace/memory/*.md` files -> copy into `~/.hermes-cmo/memories/imported-openclaw/`
- add an audit note like `~/.hermes-cmo/memories/OPENCLAW_KNOWLEDGE_MIGRATION.md`

The rewrite matters. Do not keep stale identity references (for example `Raden`) if the new bot should now be `Hermest CMO`.

### Reference-only materials
Useful, but should be selectively mined instead of copied verbatim:
- legacy workspace instruction files
- environment notes files
- legacy soul/identity/bootstrap/heartbeat notes
- old hooks (for example Titi/WhatsApp routers)
- `vault/`
- old workspace `skills/` when they may already be synced or use stale formats

### Never import into the new Hermes home
Do NOT copy these:
- `openclaw.json`
- `credentials/`, `identity/`, `devices/`
- old session stores and auth state
- Telegram polling offsets
- `.env`
- `.git/`, `node_modules/`
- RAG indexes/caches/browser profiles/logs/sqlite runtime files

### Required post-import cleanup
After the knowledge files are in place:
1. rewrite `IDENTITY.md` so the dedicated bot's role is explicit (for example `Hermest CMO`, not OpenClaw/Raden)
2. rewrite `SOUL.md` so it matches the new role and does not inherit the old persona by accident
3. add a small group-response rules note if the user expects the bot to notice their messages and not appear unresponsive
4. restart the dedicated gateway service
5. verify the service is active after restart

### Practical verification checklist
- list files created under `~/.hermes-cmo/memories/`
- read back `USER.md`, `MEMORY.md`, `IDENTITY.md`, and `SOUL.md`
- confirm the old active identity no longer appears where it should not
- confirm the new role mapping is explicit (CEO vs CMO)
- confirm the gateway service is still running after restart
