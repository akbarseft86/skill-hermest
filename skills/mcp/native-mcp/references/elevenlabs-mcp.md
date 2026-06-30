# ElevenLabs MCP setup notes

Use when wiring ElevenLabs as a native MCP server in Hermes.

## Server

Official/community-visible package tested in session:

```bash
uvx --from elevenlabs-mcp elevenlabs-mcp
```

The server exits immediately unless `ELEVENLABS_API_KEY` is present in the server environment:

```text
ValueError: ELEVENLABS_API_KEY environment variable is required
```

## Hermes config pattern

Add under `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  elevenlabs:
    command: "uvx"
    args: ["--from", "elevenlabs-mcp", "elevenlabs-mcp"]
    env:
      ELEVENLABS_API_KEY: "..."
    timeout: 180
    connect_timeout: 60
```

Then restart/reload MCP:

- Gateway: `/restart` or `hermes gateway restart`
- CLI: `/reload-mcp` if available, otherwise restart session/process

## Pitfalls

- Do not put API keys in normal chat transcripts if avoidable; prefer `.env`, profile config, or a secret manager. If a key was pasted into chat, advise user to revoke/rotate unless they explicitly accept the risk.
- Native MCP tools only appear after MCP discovery runs. If the server was added to config but no `mcp_elevenlabs_*` tools appear, restart/reload MCP and inspect startup logs.
- `uvx --from elevenlabs-mcp elevenlabs-mcp --help` may still import the server and fail for missing `ELEVENLABS_API_KEY`; this validates that the package is installed but not that the key works.
- For comparing MCP vs direct API vs built-in Hermes TTS, keep the same script text, voice ID, model, and output format across all three paths; otherwise voice quality comparison is polluted by changed parameters.
