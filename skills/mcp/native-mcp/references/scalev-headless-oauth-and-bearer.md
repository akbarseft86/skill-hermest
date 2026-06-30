# Scalev MCP on headless Hermes hosts

Session-derived notes for connecting `https://mcp.scalev.com/mcp` from a VPS/headless Hermes instance.

## What worked

Use HTTP Bearer header auth when the user can provide a Scalev API key:

```yaml
mcp_servers:
  scalev:
    url: https://mcp.scalev.com/mcp
    headers:
      Authorization: "Bearer <SCALEV_API_KEY>"
    timeout: 180
    connect_timeout: 30
```

Verify with:

```bash
hermes mcp test scalev
```

A successful test reports HTTP transport, redacted Authorization header, connection latency, and discovered tools. In the observed session Scalev exposed 25 tools including identity/docs/search, generic API operations, landing page operations, and order operations.

## Headless OAuth pitfall

`hermes mcp add scalev --url https://mcp.scalev.com/mcp --auth oauth` can generate a valid Scalev OAuth URL, but on a headless VPS the redirect URI is a loopback URL such as:

```text
http://127.0.0.1:<port>/callback?code=...&state=...
```

If the user opens the authorization URL on their own phone/laptop, `127.0.0.1` points to the user's device, not the VPS where Hermes is listening. The Hermes callback server never receives the code, and the OAuth process times out.

For PKCE flows, a copied `code` is only useful while the originating process is still alive and holding the matching `code_verifier`. Once the process times out or is killed, do not keep retrying old callback URLs; start a fresh flow or switch auth method.

## Recommended sequence

1. First test the endpoint with a minimal HEAD/initialize request to confirm whether it requires auth. Scalev returns `401 invalid_token` with a `www-authenticate` header when unauthenticated.
2. Add config with `--auth oauth` only if a usable browser/callback path exists on the Hermes host or a tunnel/forwarding setup is ready.
3. On headless VPS, prefer a Scalev API key/Bearer token if the user has one.
4. After editing `~/.hermes/config.yaml`, verify with `hermes mcp test scalev` before claiming success.
5. Do not restart the gateway automatically just to reload MCP tools. Explain that native tools load at startup and ask for explicit approval before restart, especially on always-on bot setups.

## User-facing wording

Be precise: say “configured and `hermes mcp test scalev` passed” only after the test succeeds. If OAuth was attempted but callback failed, say the config exists but authentication is not complete.
