---
name: hermes-sumopod-provider
description: Configure a Hermes profile to use the Sumopod OpenAI-compatible endpoint, validate the real model IDs, and safely switch defaults without getting tripped up by stale model names or misleading restart symptoms.
version: 1.0.0
author: Hermest
license: MIT
---

# Hermes Sumopod Provider Setup

Use this when:
- A Hermes instance/profile should use Sumopod at `https://ai.sumopod.com/v1`
- The user gives a Sumopod API key and wants a bot/profile switched over
- You need to diagnose why Sumopod works in theory but the configured model fails

## Why this needs a specific workflow

Two practical gotchas showed up:

1. **Configured model names may not match Sumopod's actual `/v1/models` IDs**
   - Example: `qwen/qwen3.6-plus` looked plausible but Sumopod rejected it.
   - The real model ID returned by the endpoint was `qwen3.6-plus`.

2. **A gateway restart can look like a provider failure when the real issue is another adapter**
   - In a multi-platform Hermes profile, restarting the gateway can briefly fail because a WhatsApp bridge exits during shutdown/restart.
   - Verify the service state after restart before blaming the Sumopod config.

## Working procedure

### 1. Add the API key to the profile `.env`
For a profile at `HERMES_HOME=/root/.hermes-cmo`:

```bash
# Add or replace
SUMOPOD_API_KEY=***
```

Do not rely on `OPENAI_API_KEY` for Sumopod if you want the setup to stay explicit and predictable.

### 2. Define a named provider in `config.yaml`
Use the profile config, not the main Hermes config if this is a separate bot/profile.

```yaml
model:
  provider: sumopod
  default: qwen3.6-plus

providers:
  sumopod:
    name: sumopod
    base_url: https://ai.sumopod.com/v1
    api_mode: openai
    key_env: SUMOPOD_API_KEY
    models:
      qwen3.6-plus:
        context_length: 131072
      qwen3.6-flash:
        context_length: 131072
      kimi-k2-5-260127:
        context_length: 128000

delegation:
  provider: sumopod
  model: qwen3.6-plus
```

Important:
- Use `api_mode: openai`
- Use `key_env: SUMOPOD_API_KEY`
- Put the **real model IDs** returned by Sumopod under `models:`

### 3. Validate the endpoint before trusting the config
Always query `/v1/models` first.

```bash
python - <<'PY'
import json, urllib.request
req = urllib.request.Request(
    'https://ai.sumopod.com/v1/models',
    headers={'Authorization': 'Bearer ' + 'YOUR_SUMOPOD_KEY'}
)
with urllib.request.urlopen(req, timeout=20) as r:
    data = json.loads(r.read().decode())
for item in data.get('data', []):
    print(item.get('id'))
PY
```

Use the exact IDs returned there.

### 4. If switching to Kimi 2.5 promo, use the exact Sumopod model ID
Observed valid promo model:

```text
kimi-k2-5-260127
```

To make it the default:

```yaml
model:
  provider: sumopod
  default: kimi-k2-5-260127

delegation:
  provider: sumopod
  model: kimi-k2-5-260127
```

### 5. Prove the model actually works with a direct completion test
Do not stop at `/v1/models`.

```bash
python - <<'PY'
import json, urllib.request
req = urllib.request.Request(
    'https://ai.sumopod.com/v1/chat/completions',
    data=json.dumps({
        'model': 'kimi-k2-5-260127',
        'messages': [{'role': 'user', 'content': 'Reply with exactly: OK_SUMOPOD'}],
        'temperature': 0,
    }).encode(),
    headers={
        'Authorization': 'Bearer ' + 'YOUR_SUMOPOD_KEY',
        'Content-Type': 'application/json',
    },
)
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read().decode())
print(data['choices'][0]['message']['content'])
PY
```

Expected:
- Exact success text back
- No 400 invalid-model error

## Failure signatures and fixes

### Failure: invalid model name
Example:

```text
Invalid model name passed in model=qwen/qwen3.6-plus
```

Fix:
- Query `/v1/models`
- Replace guessed/legacy model name with the exact ID from Sumopod
- Example correction:
  - wrong: `qwen/qwen3.6-plus`
  - right: `qwen3.6-plus`

### Failure: service restart looks broken
Example symptoms:
- `systemctl --user restart ...` appears to hang or times out
- service briefly shows `deactivating`
- logs mention WhatsApp bridge exit during shutdown

Fix:
- Check actual state after the restart:

```bash
systemctl --user show hermes-cmo-gateway.service -p ActiveState -p SubState -p MainPID
journalctl --user -u hermes-cmo-gateway.service -n 50 --no-pager
```

Interpretation:
- If logs show the old process died and systemd started a new one, the restart likely succeeded
- Do not misdiagnose this as a Sumopod/provider issue unless the new process also fails model calls

### Failure: config says Sumopod but runtime still behaves like old provider
Fix:
- Verify the correct profile config was edited
- Verify the service has the correct `HERMES_HOME`
- Restart the profile's gateway service
- Re-check the live unit file and process:

```bash
systemctl --user status hermes-cmo-gateway.service --no-pager
readlink /proc/$(systemctl --user show hermes-cmo-gateway.service -p MainPID --value)/cwd
```

## Verification checklist

- [ ] `SUMOPOD_API_KEY` exists in the target profile `.env`
- [ ] `providers.sumopod.base_url` is `https://ai.sumopod.com/v1`
- [ ] `providers.sumopod.api_mode` is `openai`
- [ ] `providers.sumopod.key_env` points to `SUMOPOD_API_KEY`
- [ ] `model.default` uses a real `/v1/models` ID
- [ ] `delegation.model` uses a real `/v1/models` ID
- [ ] Direct `/chat/completions` test succeeds
- [ ] Gateway service is active after restart

## Notes
- Sumopod is OpenAI-compatible, but **do not assume OpenRouter-style vendor/model slugs will work**.
- Always trust the endpoint's live `/v1/models` output over prior assumptions or copied config.
- In multi-platform profiles, a noisy restart can be caused by sidecar/bridge processes rather than the model provider itself.
