# Dual CLI + MCP Auth Setup

Some vendors (Higgsfield, Scalev, etc.) provide **two separate auth paths**:

| Auth Path | Tool | Authenticates | Lifespan |
|-----------|------|---------------|----------|
| **CLI auth** | `higgsfield auth login` (device code) | CLI tool, local credential store | Per-session (~10-15 min) |
| **MCP endpoint auth** | Static Bearer token, OAuth, or `hermes mcp login` | Hermes MCP client ↔ MCP server | Persistent (config) |

## Critical: These are separate

Running `higgsfield auth login` **does NOT** authenticate the MCP endpoint `https://mcp.higgsfield.ai/mcp`. The CLI login stores a token in `~/.config/higgsfield/` (or similar). The MCP endpoint at `https://mcp.higgsfield.ai/mcp` accepts a Bearer token or OAuth — the CLI's token is not directly compatible.

## Higgsfield case study

1. Install CLI: `npm install -g @higgsfield/cli`
2. Add MCP server to `~/.hermes/config.yaml`:
   ```yaml
   mcp_servers:
     higgsfield:
       url: "https://mcp.higgsfield.ai/mcp"
       timeout: 300
       connect_timeout: 60
   ```
3. Auth required for MCP endpoint:
   - `hermes mcp test higgsfield` returns **401 Unauthorized** until auth resolved
   - The MCP endpoint may need a Bearer token or OAuth (needs investigation per vendor)
   - CLI device-code login (`higgsfield auth login`) does NOT solve this — it only authenticates the CLI

## Workflow: find the right auth

```yaml
mcp_servers:
  vendor_name:
    url: "https://mcp.vendor.com/mcp"
    # Option A: Static token (preferred for headless/VPS)
    headers:
      Authorization: "Bearer <api_key_from_vendor>"
    
    # Option B: OAuth (if vendor supports it)
    auth: oauth
    oauth:
      redirect_port: 0
      client_name: "Hermes Agent"
    # Then: hermes mcp login vendor_name
```

To determine which auth the MCP endpoint needs:
1. Check vendor docs for MCP endpoint auth
2. Try `hermes mcp test <server>` — if 401, check if they document OAuth or Bearer
3. Don't assume CLI auth will carry over to MCP

## Pitfalls

- **Device code expires fast (~2-3 min)**: On a VPS, by the time user opens the link on their phone, the code is often invalid. Regenerating forces restarting the login process.
- **"Invalid or expired code"**: Screenshot shows this when user waits too long. Kill the process and start a fresh `auth login`.
- **CLI auth doesn't fix MCP 401**: Even after successful `higgsfield auth login` (CLI stores a token), the MCP endpoint at `mcp.higgsfield.ai/mcp` still returns 401 because it needs its own auth.
- **Skills install (PromptScript) != MCP tools**: `npx skills add vendor/skills --yes` installs Hermes skills (SKILL.md files), not MCP server config. You need BOTH the MCP server config AND the skill for full integration.

## See Also

- `references/headless-oauth-mcp.md` — for OAuth-based MCP servers on headless setups
- `references/scalev-headless-oauth-and-bearer.md` — Bearer-first approach for Scalev
