# Dual-profile gateway diagnostics (HERMES_HOME conflict, crash loops)

When two Hermes gateway services run on the same host — main (`hermes-gateway.service`) plus a secondary profile like CMO (`hermes-cmo-gateway.service`) — they MUST point at different `HERMES_HOME` directories. If both load the same profile they fight over the Telegram bot token and WhatsApp bridge port/session, and one (or both) ends up in a restart loop.

## Symptoms

- One service stuck in `activating (auto-restart)` for a long time, often with `restart counter is at <large>` in journal.
- Journal shows the gateway starting, printing the banner, then immediately receiving `signal=SIGTERM under_systemd=yes` 5-15 seconds later, repeated forever.
- Telegram errors: `Telegram bot token already in use (PID …)`. Telegram polling conflicts (`Conflict: terminated by other getUpdates request`).
- WhatsApp errors on the duplicate profile: `Bridge ready (status: connected)` quickly followed by `Poll error: Cannot connect to host 127.0.0.1:3013` and `Disconnected`. Or: `WhatsApp session already in use (PID …). Stop the other gateway first.`
- Watchdog cron jobs (`hermes-gateway-watchdog`) timeout or report `error` status because `systemctl --user start` blocks waiting on the broken service.

## Diagnostic commands

```bash
# 1. Confirm which env each unit actually has loaded.
systemctl --user show hermes-gateway.service -p ExecStart,Environment,Restart,RestartSec
systemctl --user show hermes-cmo-gateway.service -p ExecStart,Environment,Restart,RestartSec

# 2. Inspect static unit files AND drop-ins.
cat /root/.config/systemd/user/hermes-gateway.service
ls /root/.config/systemd/user/hermes-gateway.service.d/
cat /root/.config/systemd/user/hermes-gateway.service.d/override.conf 2>/dev/null
cat /root/.config/systemd/user/hermes-cmo-gateway.service
ls /root/.config/systemd/user/hermes-cmo-gateway.service.d/
cat /root/.config/systemd/user/hermes-cmo-gateway.service.d/override.conf 2>/dev/null

# 3. Confirm crash pattern in journal.
journalctl --user -u hermes-gateway.service -n 60 --no-pager

# 4. Verify config.yaml in each profile actually matches the intended profile.
grep -n 'whatsapp\|bridge_port\|session_path\|platforms:' /root/.hermes/config.yaml
grep -n 'whatsapp\|bridge_port\|session_path\|platforms:' /root/.hermes-cmo/config.yaml
```

## Root cause to look for

The static unit body of `hermes-gateway.service` may carry the wrong `HERMES_HOME`. Real-world example caught in the wild:

```
[Service]
Environment="HERMES_HOME=/root/.hermes-cmo"   # WRONG for main service
```

This was a copy-paste leftover from when the CMO profile was installed via `hermes claw migrate` / dual-bot setup. Result: both services run the CMO profile, both try to claim the same Telegram bot, both try to claim port 3013, both die.

## Fix

1. Patch the unit so the main service uses the main profile:
   - For `hermes-gateway.service`: `Environment="HERMES_HOME=/root/.hermes"`
   - For `hermes-cmo-gateway.service`: `Environment="HERMES_HOME=/root/.hermes-cmo"`
2. `systemctl --user daemon-reload`
3. `systemctl --user reset-failed hermes-gateway.service`
4. `systemctl --user restart hermes-gateway.service`
5. Watch journal for one clean startup with no SIGTERM and `Telegram` + (if enabled) `WhatsApp` connecting successfully.

## Pitfalls

- `config.yaml` alone being correct is NOT proof — `Environment=HERMES_HOME=…` in the unit overrides which profile gets loaded.
- Don't just edit the drop-in `override.conf`. If the static unit body also sets `HERMES_HOME`, the last assignment wins and you'll go in circles. Edit whichever one is authoritative and remove duplicates.
- After fixing, also re-verify `bridge_port` and `session_path` in each profile's `config.yaml` so the two profiles don't accidentally collide on port 3013.
- Restarting the main gateway will briefly disconnect any active CEO bot chat session. If the operator depends on that bot to recover access, warn them before restarting and prefer `restart` over `stop`.
- Pair this fix with a hardened watchdog: treat `activating` as non-error, and use `systemctl --user start --no-block` so cron-driven watchdog runs do not hang while a gateway is draining or auto-restarting.
