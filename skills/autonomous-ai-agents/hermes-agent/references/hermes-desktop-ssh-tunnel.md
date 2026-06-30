# Hermes Desktop — SSH Tunnel Connection

Community Electron app `fathah/hermes-desktop` lets users chat with a remote Hermes instance through an SSH tunnel — no exposed port, no API key sent over the network. The app is **unofficial** but actively maintained (v0.5.x as of late 2026). It is just a GUI client; the brain is still the remote `hermes` process.

Repo: https://github.com/fathah/hermes-desktop
Releases: https://github.com/fathah/hermes-desktop/releases/latest

## How it connects

The desktop app does three things on "Connect via SSH":

1. Opens an SSH tunnel from the local Mac/Win/Linux box to the remote VPS using the system `ssh` binary. Requires **passwordless SSH** — public key already installed in `~/.ssh/authorized_keys` on the remote.
2. On the remote, probes for the `hermes` CLI in two locations (PR #305): the venv binary (`/root/.hermes/hermes-agent/venv/bin/hermes`) and `~/.local/bin/hermes`. The symlink the official installer creates at `~/.local/bin/hermes → venv/bin/hermes` is the canonical happy path.
3. Talks to the remote Hermes via its **HTTP API server**, NOT through stdin/stdout. Default tunnel target port: **8642**. The API server token is resolved from `api_server.token` in `config.yaml` (PR #337, closes #333).

If you skip step 3 (no `api_server` block in `config.yaml`), the app fails with the generic "Could not connect via SSH or reach Hermes on the remote" error — the SSH tunnel works, but there is nothing listening on 8642 on the remote.

## Remote VPS setup checklist

Before telling the user to click Connect, confirm all of the following on the remote:

```bash
# 1. SSH listening, root login allowed
ss -tlnp | grep :22
grep -iE '^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication)' /etc/ssh/sshd_config

# 2. Port 22 reachable from outside
timeout 5 bash -c '</dev/tcp/<VPS_IP>/22 && echo OPEN || echo CLOSED'

# 3. hermes CLI discoverable at the path the app probes
which hermes
ls -la ~/.local/bin/hermes

# 4. api_server block exists in config.yaml
grep -A 5 "^api_server:" ~/.hermes/config.yaml

# 5. API server actually listening on 8642
ss -tlnp | grep 8642
```

If step 4 is empty, the user **must** enable the API server. **Do NOT add a top-level `api_server:` block in config.yaml** — that block is not read by the gateway. The API server is configured via **environment variables** in `~/.hermes/.env` (or the relevant profile's `.env`):

```bash
# Append to ~/.hermes/.env
API_SERVER_ENABLED=true
API_SERVER_PORT=8642
API_SERVER_HOST=127.0.0.1          # bind loopback only — tunneled via SSH
API_SERVER_KEY=<random-long-string> # token the Desktop app sends; do not leak
```

Source: `gateway/config.py` reads `os.getenv("API_SERVER_ENABLED")` etc., not config.yaml.

After editing `.env`, restart the gateway:

```bash
systemctl --user restart hermes-ceo-gateway.service   # adjust unit name as needed
ss -tlnp | grep 8642     # verify listener
```

## Mac client setup

```bash
# 1. Generate key (run ONE LINE AT A TIME — pasting two commands at once stuffs
#    the second command into the first command's filename prompt)
ssh-keygen -t ed25519        # press Enter 3x: default path, empty passphrase x2

# 2. Copy to VPS — will prompt for VPS password once
ssh-copy-id root@<VPS_IP>

# 3. Verify passwordless login works
ssh root@<VPS_IP>            # must drop you into the shell with no prompt
```

Then in the app:
- SSH Host: VPS public IP
- SSH Port: 22
- Username: `root` (or whatever owns the Hermes install)
- Private Key Path: `~/.ssh/id_ed25519` for ed25519 keys — the placeholder `~/.ssh/id_rsa` is wrong if you generated an ed25519 key
- Remote Hermes Port: 8642 (must match `api_server.port`)

## Pitfalls observed in the wild

- **Generic "Could not connect" error masks three different failures**: missing `api_server` block, wrong private key path, or SSH still password-prompting. Walk the checklist top-to-bottom; do not guess.
- **Private Key Path field defaults to `~/.ssh/id_rsa`** — must be edited explicitly to `~/.ssh/id_ed25519` when the user generated an ed25519 key.
- **Pasted multi-command instructions break `ssh-keygen`**: if the user pastes `ssh-keygen -t ed25519\nssh-copy-id …` into one line, the second command becomes the keyfile path and they end up stuck in a passphrase loop named after a command. Recovery: Ctrl+C, `rm ~/.ssh/id_ed25519*`, redo one line at a time.
- **App is NOT notarized by Apple** — first launch on macOS shows "cannot be opened, unidentified developer". Right-click → Open, or System Settings → Privacy & Security → Open Anyway.
- **App is community-built**, not from Nous Research. Do not promise official support; link to its repo issues for app-side bugs.
- **VPS hardening reminder**: a fresh install with `PermitRootLogin yes` + password auth is a soft target. After SSH-key login works, recommend disabling password auth (`PasswordAuthentication no`) and considering fail2ban / non-default port. Do not flip these toggles for the user without explicit consent — locking them out of their own VPS is a much worse failure than weak SSH config.

## When the user asks "can I install Hermes Desktop and connect to my VPS?"

Order of operations every time:
1. Confirm the OS and chip (arm64 vs x64 DMG for macOS).
2. Verify remote SSH reachability + `hermes` CLI path on the VPS (steps 1–3 above).
3. Verify `api_server` block + listener on 8642 (steps 4–5). If missing, add it before the user clicks Connect — that is the single most common cause of the "Could not connect" error.
4. Walk the user through passwordless SSH setup, one command per turn, asking for screenshots when they get stuck.
5. Only then point them at the Connect form with the exact field values.
