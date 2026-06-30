# OAuth for Remote HTTP MCP Servers

Session-derived troubleshooting notes for remote MCP servers that require OAuth (example: `https://mcp.facebook.com/ads`).

## Config shape

Remote HTTP MCP servers can use Hermes' browser-based OAuth 2.1 / PKCE support by adding `auth: oauth` and an optional `oauth:` block:

```yaml
mcp_servers:
  meta_ads:
    url: https://mcp.facebook.com/ads
    auth: oauth
    oauth:
      redirect_port: 0          # 0 = auto-pick localhost callback port
      client_name: Hermes Agent # optional display name
      # client_id: ...          # required if provider disallows dynamic registration
      # client_secret: ...      # if confidential client is required
      # scope: ...              # if provider requires explicit scopes
    connect_timeout: 60
    timeout: 180
```

Initial login is forced with:

```bash
hermes mcp login <server_name>
```

Tokens are profile-scoped and stored under:

```text
$HERMES_HOME/mcp-tokens/
```

## Headless/VPS pitfall

The OAuth callback URI is localhost on the machine running Hermes, e.g. `http://127.0.0.1:<port>/callback`. On a VPS or gateway session, a browser opened on the user's laptop may not be able to hit that callback unless you use a browser on the same host or set up port forwarding/tunnel. Prefer running the login from an interactive TTY and be ready to tunnel the fixed `redirect_port` if callback cannot complete.

### Discovery-first `mcp add` can time out before saving config

`hermes mcp add <name> --url <url> --auth oauth` is discovery-first: it starts the OAuth flow and waits for callback before persisting the server. In a headless/gateway session this can time out while waiting for the user's browser approval; if that happens, `hermes mcp list` and `hermes mcp test <name>` will still say the server is not found.

Recovery pattern:

1. Add the server entry manually to `$HERMES_HOME/config.yaml` under `mcp_servers`:

```yaml
mcp_servers:
  scalev:
    url: https://mcp.scalev.com/mcp
    auth: oauth
    oauth:
      redirect_port: 0
      client_name: Hermes Scalev MCP
    connect_timeout: 60
    timeout: 180
```

2. Run OAuth explicitly from a PTY/interactive shell so the authorization URL is printed promptly:

```bash
PYTHONUNBUFFERED=1 hermes mcp login scalev
```

3. After approval, verify in order:

```bash
hermes mcp list
hermes mcp test scalev
```

If the approval was done against an old timed-out OAuth URL, it will not complete the new login process because the state/port/code_challenge changed. Generate a fresh URL with `hermes mcp login <name>` and have the user approve that exact URL.

## Dynamic registration failure pattern

If `hermes mcp login <server>` fails with:

```text
Registration failed: 400 {"error":"invalid_client_metadata","error_description":"Dynamic registration is not available for this client."}
```

interpret it as: the MCP server does not allow Hermes to dynamically register an OAuth client. The next action is **not** retrying blindly or restarting the gateway. Obtain/provider-configure a pre-registered OAuth client:

- `oauth.client_id`
- `oauth.client_secret` if required
- accepted `redirect_uri` (possibly fixed port)
- required `scope`

Then rerun `hermes mcp login <server_name>`.

## Restart rule

Adding OAuth config changes `config.yaml`; gateway/tool discovery may need a fresh agent process later, but do not restart live gateway services without explicit user approval. First complete login and verify token files exist; only then ask for approval if restart is necessary for discovery.