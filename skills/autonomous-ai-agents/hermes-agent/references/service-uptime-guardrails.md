# Service Uptime Guardrails for Live Hermes Instances

Use this when maintaining a Hermes install that the user depends on staying online, especially when they have limited ability to log back in and manually restart it.

## Durable preference captured
For this user class of setup, prefer `restart` over `stop`/`shutdown` during maintenance whenever possible.

## Practical pattern
1. Check whether the gateway runs as a user systemd service.
2. Ensure `loginctl show-user <user> -p Linger` is enabled so services survive logout.
3. For long-lived gateway services, prefer:
   - `Restart=always`
   - short `RestartSec` (for example 5s)
   - `TimeoutStopSec` comfortably larger than any configured drain timeout
4. If a secondary profile/service is critical (for example WhatsApp/CMO), harden it the same way instead of only fixing the main gateway.
5. Add a watchdog script under `~/.hermes/scripts/` that checks `systemctl --user is-active` for critical services and starts any that are not active.
6. Schedule the watchdog with a local cron job (`no_agent=true`) so the check continues even if the current conversation ends.
7. Verify both layers:
   - systemd service state
   - application-specific health endpoint when available (for WhatsApp bridge, `/health` should report `status: connected`)

## Example watchdog script shape
```bash
#!/usr/bin/env bash
set -euo pipefail
export XDG_RUNTIME_DIR="/run/user/$(id -u)"

services=(
  hermes-gateway.service
  hermes-cmo-gateway.service
)

for svc in "${services[@]}"; do
  state="$(systemctl --user is-active "$svc" 2>/dev/null || true)"
  if [[ "$state" != "active" ]]; then
    systemctl --user start "$svc"
  fi
done
```

## Pitfalls
- A service being `active (running)` is not sufficient proof that a bridge-backed platform is usable.
- `stop` can strand a user who cannot easily log back into the host; use `restart` unless you truly need a hard stop.
- If you adjust drain timeouts, keep `TimeoutStopSec` larger than the drain window or systemd may kill the process mid-shutdown.
- Protect secondary profile services too; otherwise the main gateway may look healthy while WhatsApp/CMO is down.
