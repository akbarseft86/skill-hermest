# ElevenLabs TTS Path Comparison

## A. MCP (`mcp_elevenlabs_*`)

**Best for**
- Voice discovery
- Voice cloning/design
- Ad-hoc generation from chat
- Agent workflows that need ElevenLabs-specific tools

**Pros**
- Rich tool surface: voices, conversations, agents, music, SFX
- No manual curl JSON
- Good for exploratory work

**Cons**
- Needs `mcp_servers` config + gateway restart
- Param validation stricter than REST
- Circuit breaker after repeated failures
- File path/output handling less predictable than direct curl

**Gotcha**
- `voice_id` xor `voice_name`. Passing both fails.

## B. Direct REST curl

**Best for**
- Batch rendering many scripts
- Exact output names
- Full control over `voice_settings`
- Debugging raw ElevenLabs API behavior

**Pros**
- No Hermes restart
- Most reproducible
- Easy to loop in Python/bash
- Exact HTTP status + response body available

**Cons**
- Must handcraft JSON safely
- Must handle keys securely
- Not auto-delivered unless you attach file path in final response

## C. Hermes built-in `text_to_speech`

**Best for**
- Fast user-facing voice notes in Telegram
- Production default once voice is picked
- Workflows where assistant should directly return `MEDIA:/path`

**Pros**
- Cleanest UX
- Provider abstraction
- Easy: one tool call with `text`

**Cons**
- Less per-call control unless config supports it
- Requires config + `.env` + gateway restart
- If provider still `edge`, voice ID ignored and output may be English `.ogg`

## Decision rule

- Need voice search / ElevenLabs extras → **MCP**
- Need batch + exact controls → **REST**
- Need routine Telegram delivery → **built-in**

## Secure key handling

Preferred order:
1. Env var in `/root/.hermes/.env` for built-in provider
2. `mcp_servers.<name>.env` for MCP
3. Shell env var for one-off curl
4. Inline key in chat or command — avoid unless user explicitly approves
