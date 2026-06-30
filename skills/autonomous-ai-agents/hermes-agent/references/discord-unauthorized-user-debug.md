# Discord silent / "bengong" due to unauthorized user

Use this when Discord messages are visible in logs but the bot does not answer.

## Symptom
- User says Hermest is silent in Discord threads/channels.
- Gateway is running and Discord is connected.
- Logs show inbound Discord messages with content, followed by:
  - `Unauthorized user: <discord_user_id> (<name>) on discord`

This means Message Content Intent is working; the blocker is authorization, not Discord connectivity.

## Safe diagnostic path
1. Read gateway logs for Discord inbound + auth rejection:
   - `tail -n 250 ~/.hermes/logs/gateway.log | grep -iE 'discord|Unauthorized user|<message text>|<username>'`
2. Confirm active service read-only; do not restart first:
   - `systemctl --user is-active hermes-ceo-gateway.service hermes-gateway.service 2>&1 || true`
3. Check pairing/allowlist state:
   - `hermes pairing list`
   - Inspect env vars only if needed: `DISCORD_ALLOWED_USERS`, `DISCORD_ALLOW_ALL_USERS`, `GATEWAY_ALLOWED_USERS`.

## Fix options
Prefer the least broad fix:

1. **Approve/pair the exact Discord user ID** if this is a trusted owner/user:
   - The runtime checks `PairingStore.is_approved(platform, user_id)` on each incoming message, so adding to the approved file usually takes effect on the next message without gateway restart.
   - CLI approval normally requires a DM pairing code. If the code flow is not available because the user is posting in a group/thread, manually add the ID to the pairing store.

2. **Allowlist env var** (`DISCORD_ALLOWED_USERS=<id1>,<id2>`) if the deployment intentionally uses static allowlists.

3. **Allow all** (`DISCORD_ALLOW_ALL_USERS=true`) only for low-risk/private Discord servers.

## Pairing store path pitfall
Depending on Hermes version/profile compatibility, the active pairing path may be one of:
- `~/.hermes/pairing/discord-approved.json`
- `~/.hermes/platforms/pairing/discord-approved.json`

Verify with Python if needed:
```bash
python3 - <<'PY'
from hermes_constants import get_hermes_home, get_hermes_dir
print('home', get_hermes_home())
print('pairing', get_hermes_dir('platforms/pairing', 'pairing'))
PY
```

If uncertain and you need a fast repair, write the same approved entry to both paths, then run `hermes pairing list` to verify the CLI-visible path.

Example JSON entry:
```json
{
  "1510466085680451685": {
    "user_name": "Akbar / akbarn86",
    "approved_at": 1781335622.656996
  }
}
```

Use current epoch seconds for `approved_at`.

## Verification
- `hermes pairing list` shows the user under Approved Users.
- Ask the user to send a fresh Discord message. If logs no longer show `Unauthorized user`, continue debugging the next error if any.

## Do not
- Do not restart/stop/kill the gateway before checking logs and auth state.
- Do not misdiagnose this as Message Content Intent if the log already includes the message content.
