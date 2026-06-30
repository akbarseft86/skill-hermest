# CLI + MCP Auth Setup Notes

Use when a vendor offers both a CLI, PromptScript/agent skills, and a remote MCP endpoint.

## Key distinction

Do not assume `npx skills add <repo>` installs a Hermes-native skill. The `skills` npm CLI often installs PromptScript/universal-agent skills into `~/.agents/skills/` and symlinks for tools like Claude Code, Codex, OpenCode, OpenClaw, and Hermes Agent. These may be useful as external prompt assets, but they are not the same as Hermes `~/.hermes/skills/` skills managed by `hermes skills install` or `skill_manage`.

## Recommended sequence

1. Load `hermes-agent` and `native-mcp` skills before changing Hermes MCP config.
2. Read the vendor docs/browser page for the Hermes-specific tab.
3. If the page says "CLI is better for Hermes", install the CLI first and test `vendor --help`.
4. If the page exposes a remote MCP URL, add it under `mcp_servers` with `url`, `timeout`, and `connect_timeout`.
5. Run `hermes mcp list` to verify the server is configured.
6. Run `hermes mcp test <server>` to verify transport/auth.
7. If the MCP test returns `401 Unauthorized`, do not call the server broken. Treat it as an OAuth/auth step. Look for either:
   - `hermes mcp login <server>` for Hermes OAuth MCP auth, or
   - vendor CLI login/device-code flow such as `<vendor> auth login`.
8. For device-code auth on a headless VPS, run the login command in a PTY/background process, capture the `https://.../device?code=...` URL, and give it to the user.
9. After the user approves login, test again, then use `/reload-mcp` or restart only with explicit approval if needed.

## Pitfalls

- Reading `config.yaml` through tools may redact secrets in output. Never patch a redacted secret (`Bearer ***`) back into the file. If that happens, restore the real value from a trusted source/config backup immediately and avoid exposing the secret in final replies.
- For live gateway profiles, avoid restart unless explicitly approved; prefer `/reload-mcp` when available.
- Treat CLI install success, skill install success, and MCP auth success as three separate statuses in the user-facing summary.

## Higgsfield example

Higgsfield setup page for Hermes currently shows:

```bash
npm install -g @higgsfield/cli
higgsfield auth login
npx skills add higgsfield-ai/skills
```

Their remote MCP endpoint is:

```yaml
mcp_servers:
  higgsfield:
    url: https://mcp.higgsfield.ai/mcp
    timeout: 300
    connect_timeout: 60
```

A plain `hermes mcp test higgsfield` can return `401 Unauthorized` until the account/device-code auth step is completed. The CLI login prints a URL like `https://higgsfield.ai/device?code=...` and waits for approval.

### Device code quirks

- **Code expires fast (~5 minutes).** Show the URL to the user immediately and ask them to approve before the process auto-terminates. Starting a new login flow creates a fresh code — do NOT reuse URLs from terminated sessions.
- **Multiple attempts may be needed.** If the first code expires before the user acts, rerun `higgsfield auth login` to get a fresh code and URL. In one case the third attempt succeeded.
- **CLI login ≠ MCP auth.** Even after successful CLI login (`higgsfield account status` returns plan/credits), `hermes mcp test higgsfield` may still return 401. The MCP endpoint may need a separate auth token or an OAuth handoff that is not yet wired. Check whether the vendor exposes a Bearer token via `higgsfield` CLI or web UI for the MCP headers.

### Vendor model discovery (CLI)

Higgsfield's CLI exposes model inventory without needing the MCP endpoint:

```bash
higgsfield model list                # all models with display names, types
higgsfield model get <job_set_type>  # params, defaults, required fields
```

Model IDs differ from display names. Examples discovered:
- `seedance_2_0` → Seedance 2.0 (res up to 4K, has `mode: std|fast`)
- `seedance_2_0_mini` → Seedance 2.0 Mini (capped at 720p, no mode param)
- `seedance1_5` → Seedance 1.5 Pro (legacy)

To estimate cost before generating:
```bash
higgsfield generate cost <job_set_type> prompt="test" [duration=N] [resolution=N]
```

### Web-only limitation (critical)

Higgsfield's pricing page notes: **"Unlimited models and free generations are accessible only via higgsfield.ai and are NOT accessible on MCP/CLI, Canvas, or Supercomputer."** This means models designated as "unlimited" on a plan (e.g., Nano Banana Pro, Kling 3.0, Seedream 4.5) may still consume credits when called via CLI or MCP.
