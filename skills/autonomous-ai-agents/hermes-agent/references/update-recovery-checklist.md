# Hermes update recovery checklist for dirty repos and gateway profiles

Use when `hermes update` is run on a live multi-profile install with local modifications.

## Pre-update capture
- Record `hermes --version`
- Record `hermes status --all`
- Record repo state:
  - `git rev-parse --abbrev-ref HEAD`
  - `git rev-parse HEAD`
  - `git status --short`
- Save a manual backup even though Hermes autostashes:
  - make a safety branch
  - save `git diff`
  - copy modified/untracked files to an external backup dir

## What Hermes update does on a dirty repo
- `hermes update` auto-stashes modified + untracked files before pulling.
- If stash restore conflicts with updated upstream files, Hermes may:
  - report the conflicting files
  - preserve the stash ref
  - reset the working tree to clean `HEAD`
- Afterward, check `git stash list` and keep the stash ref in your notes before any cleanup.

## Post-update verification
1. `hermes --version`
2. `hermes status --all`
3. `systemctl --user --no-pager --full status hermes-gateway.service hermes-cmo-gateway.service`
4. For WhatsApp-backed profiles, verify the bridge directly:
   - `http://127.0.0.1:3013/health` should report `status: connected`

## If the main gateway is up but the CMO/WhatsApp profile is down
- Start only the failed service first:
  - `systemctl --user start hermes-cmo-gateway.service`
- Re-check status and then the bridge health endpoint.
- If the unit warns that `TimeoutStopSec` is too short for `agent.restart_drain_timeout`, regenerate the unit or patch the timeout so it is at least 90s when drain timeout is 60s.

## Useful facts observed in this workflow
- A failed blanket restart can leave the main gateway healthy while the CMO/WhatsApp service is inactive.
- WhatsApp service health is not proven by systemd alone; confirm both:
  - service status = `active (running)`
  - bridge health endpoint = `connected`
- Keep the autostash until the user explicitly decides whether to reapply local changes.
