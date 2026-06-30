---
name: paperclip-root-vps-install
description: Install and run Paperclip on a VPS where you are operating as root and Docker is unavailable. Covers embedded-postgres pitfalls, filesystem placement, and startup verification.
version: 1.0.1
author: Hermest
license: MIT
---

# Paperclip install on a root-operated VPS

## Docker on OpenCloudOS (non-standard distro)

When later deciding to install Docker on OpenCloudOS, do **not** rely on Docker's generic install script. It can fail with:

```bash
ERROR: Unsupported distribution 'opencloudos'
```

Use the distro packages instead:

```bash
dnf install -y docker docker-buildx docker-compose
systemctl enable --now docker
docker --version
```

OpenCloudOS is RHEL/CentOS-compatible; `dnf`/`yum` is the reliable path.

Use this when:
- You need to install `paperclipai/paperclip` on a Linux VPS
- You are operating as `root`
- Docker is unavailable or not desired
- Paperclip uses embedded PostgreSQL

## Why this needs a special workflow

Paperclip's embedded PostgreSQL flow does not work cleanly when the repo/runtime live under `/root/...`.

Observed failure modes:
- `You are running this script as root. Postgres does not support running as root...`
- embedded-postgres tries to run `initdb`/`postgres` as system user `postgres`
- if repo or runtime are under `/root`, the spawned process cannot access paths because `/root` is commonly restricted
- startup can also fail if the data-dir parent is owned by `root:root` and not writable by `postgres`

## Working approach

### 1. Clone repo normally for inspection
```bash
git clone --depth 1 https://github.com/paperclipai/paperclip.git /root/.Hermes/workspace/paperclip
cd /root/.Hermes/workspace/paperclip
```

### 2. Install pnpm via corepack if needed
```bash
pnpm --version || corepack enable && pnpm --version
pnpm install
```

### 3. Ensure a system `postgres` user exists
Paperclip's embedded-postgres package expects this when run as root.
```bash
getent group postgres >/dev/null || groupadd -r postgres
getent passwd postgres >/dev/null || useradd -r -g postgres -d /var/lib/postgres -s /sbin/nologin -M postgres
```

### 4. Copy runtime to an accessible path outside `/root`
Do not run from `/root/...`.
Use `/srv` instead.
```bash
mkdir -p /srv
cp -a /root/.Hermes/workspace/paperclip /srv/paperclip
mkdir -p /srv/paperclip-home/instances/default
```

If `/srv/paperclip` already exists, move it aside first or delete it only after confirming it is safe to replace.

### 5. Make the Paperclip home writable by `postgres`
This is required because embedded-postgres initializes the cluster as `postgres`.
```bash
chown -R postgres:postgres /srv/paperclip-home
chmod 755 /srv /srv/paperclip /srv/paperclip-home
```

### 6. Start Paperclip with an explicit runtime home and Node path
If Node/pnpm are installed under root's nvm, export that path first.
```bash
export PAPERCLIP_HOME=/srv/paperclip-home
export PATH=/root/.nvm/versions/node/v22.22.1/bin:$PATH
cd /srv/paperclip
pnpm dev:once
```

## Verification

Wait for logs like:
- `Embedded PostgreSQL ready`
- `Server listening on 127.0.0.1:3100`

Then verify:
```bash
python - <<'PY'
import urllib.request
for url in ['http://127.0.0.1:3100/api/health','http://127.0.0.1:3100/api/companies']:
    with urllib.request.urlopen(url, timeout=10) as r:
        print(url, r.status)
        print(r.read().decode()[:500])
PY
```

Expected:
- `/api/health` returns `200` with `{"status":"ok"...}`
- `/api/companies` returns `200` (often `[]` on first run)

## Common traps

### Trap 1: Starting from `/root/...`
Symptoms:
- root warning from embedded-postgres
- `EACCES` or initdb failure

Fix:
- relocate repo/runtime to `/srv/...`
- keep `PAPERCLIP_HOME` outside `/root`

### Trap 2: `postgres` user missing
Symptoms:
- `You are running this script as root... configure embedded-postgres to create a Postgres user...`

Fix:
- create the system `postgres` user/group manually

### Trap 3: data dir parent owned by root
Symptoms:
- `Failed to initialize embedded PostgreSQL cluster ... creating directory ...`
- startup fails even after moving to `/srv`

Fix:
- `chown -R postgres:postgres /srv/paperclip-home`

### Trap 4: trying to run as another user with Node only installed in `/root/.nvm`
Symptoms:
- `pnpm: command not found`
- `corepack: command not found`
- permission denied executing binaries from `/root/.nvm`

Fix:
- simplest path is to keep the main process under root but place repo/runtime in paths accessible to `postgres`
- or install Node globally for the target non-root user before retrying

## Notes
- If Docker is available, Paperclip's Docker path may be simpler; this skill is for no-Docker environments.
- `pnpm dev:once` is sufficient to bring up a working local instance.
- For persistence, create a systemd service later using the same `PAPERCLIP_HOME` and PATH assumptions.
