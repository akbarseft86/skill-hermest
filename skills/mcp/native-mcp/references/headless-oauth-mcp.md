# Headless OAuth for Remote MCP Servers

Use this note when connecting a remote HTTP MCP server that returns `401 invalid_token` / `WWW-Authenticate: Bearer` and requires browser-based OAuth from a VPS or other headless host.

## Key Lessons

- A `401 invalid_token` response with `WWW-Authenticate: Bearer ... resource_metadata=... scope=...` means the MCP endpoint is reachable but needs OAuth/token authorization. Configure the server with `auth: oauth`, not a static header unless the user has an explicit bearer token.
- Each `hermes mcp login <server>` run creates a fresh OAuth flow: new callback port, state, PKCE verifier, and authorization code challenge. Authorization codes are single-use and only valid for the still-running flow that generated them.
- Do not kill or timeout the login process while the user is approving. If the process exits, any callback URL/code from that flow is stale and cannot be exchanged.
- Avoid running several OAuth flows simultaneously. The user will see multiple URLs and may approve the wrong one. Keep one active flow, quote its port/state, and tell the user to ignore older process notifications.
- On headless hosts, the callback URL is `http://127.0.0.1:<port>/callback` on the Hermes host, not on the user's laptop/phone. Opening the URL from another device usually cannot reach that localhost callback automatically.

## Recommended Workflow

1. Add the MCP server explicitly with OAuth:

```bash
hermes mcp add <name> --url "https://example.com/mcp" --auth oauth
```

If the interactive `add` flow prompts for a token or times out, add the config manually:

```yaml
mcp_servers:
  <name>:
    url: https://example.com/mcp
    auth: oauth
    oauth:
      redirect_port: 0   # or a fixed port if tunneling
      client_name: Hermes Agent
    connect_timeout: 60
    timeout: 180
```

2. Start exactly one login process and keep it alive long enough for the user:

```bash
PYTHONUNBUFFERED=1 timeout 180 hermes mcp login <name> 2>&1
```

Use a tracked background process if operating from chat, but do not kill it until it completes or the user gives up.

3. Send the user only the currently active authorization URL. Include the callback port and state so they can distinguish it from stale URLs.

4. If the user's browser cannot reach the localhost callback, ask for the complete callback URL from the browser address bar. It should match the active port/state exactly:

```text
http://127.0.0.1:<active-port>/callback?code=...&state=<active-state>
```

If the state/port does not match, do not try to exchange it. Start a new single flow and be explicit that older codes are invalid.

5. After successful login, verify before claiming success:

```bash
hermes mcp list
hermes mcp test <name>
```

Then restart/reload MCP only if required and approved by the user in live-gateway environments.

## Better Headless Patterns

- If possible, use a fixed `oauth.redirect_port` and tunnel that port from the user's browser machine to the VPS (SSH reverse/forward tunnel) so the callback lands on the running Hermes process.
- If the provider supports a bearer token or device flow, prefer that over repeated localhost callbacks on a pure headless server.
- When the provider issues very short-lived authorization codes, increase the process timeout and reduce round trips in chat.

## User-Facing Messaging Pattern

Be concise and operational:

- "Only use this latest URL; ignore old process notifications. Active callback: port X, state Y."
- "If the callback page fails, copy the full URL from the address bar. It must include port X and state Y."
- "Older codes cannot be reused because the PKCE verifier lived in the process that has already exited."
