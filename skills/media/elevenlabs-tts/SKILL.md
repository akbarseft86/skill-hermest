---
name: elevenlabs-tts
description: Generate ElevenLabs voice-over via three paths — Hermes built-in tool, MCP server, or direct REST curl. Pick voice, lock config, avoid common gotchas.
when_to_use: User wants AI voice-over (ads, reels, narration, demo). Especially when comparing voices, multilingual (Indonesian/Bahasa), or producing batch versions for A/B testing.
---

# ElevenLabs TTS — Three Paths

Three valid ways to drive ElevenLabs from Hermes. Pick by use case:

| Path | Tool | Best for | Output |
|---|---|---|---|
| **A. MCP** | `mcp_elevenlabs_*` | Ad-hoc, voice library search, voice cloning | `.mp3` to `$HOME/Desktop` or custom dir |
| **B. REST curl** | `terminal` + curl | Full control, batch loops, custom params per call | `.mp3` raw |
| **C. Built-in** | `text_to_speech` tool | Auto-delivery to Telegram (voice bubble), default voice locked | `.mp3` (elevenlabs) or `.ogg` (edge fallback) |

## Setup (one-time)

### Path A — MCP
1. Append to `/root/.hermes/config.yaml`:
   ```yaml
   mcp_servers:
     elevenlabs:
       command: uvx
       args: ["--from", "elevenlabs-mcp", "elevenlabs-mcp"]
       env:
         ELEVENLABS_API_KEY: sk_xxx
   ```
2. Prefetch: `uvx --from elevenlabs-mcp elevenlabs-mcp --help` (warm cache, avoid timeout on first call).
3. Restart gateway: `systemctl restart hermes-ceo-gateway` — gateway down ~10–30s. Warn user first if always-on matters.
4. Verify: call `mcp_elevenlabs_search_voices` — should return list.

### Path B — REST
Just need API key in env or inline. No restart.
```bash
curl -s -X POST "https://api.elevenlabs.io/v1/text-to-speech/$VOICE_ID" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"...","model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.5,"similarity_boost":0.8,"style":0.3,"use_speaker_boost":true,"speed":1.0}}' \
  --output out.mp3
```

### Path C — Built-in `text_to_speech`
1. `/root/.hermes/config.yaml` `tts:` block — set `provider: elevenlabs` and `tts.elevenlabs.voice_id: <id>`.
2. API key goes to `/root/.hermes/.env` as `ELEVENLABS_API_KEY=sk_xxx`. **`.env` is protected** — write via shell redirect: `echo "ELEVENLABS_API_KEY=sk_xxx" >> /root/.hermes/.env` (ask user first).
3. Restart gateway. Call `text_to_speech(text="...")` — output auto-delivered as Telegram voice bubble.

## Pitfalls (learned the hard way)

- **MCP param conflict**: `voice_id` and `voice_name` cannot both be set on `mcp_elevenlabs_text_to_speech`. Pick one. Voice ID always wins for reproducibility.
- **Circuit breaker**: 3 consecutive MCP failures → ~41s cooldown. If you hit it, wait it out, don't retry-spam.
- **Voice selection for ads**: filter by `use_case: advertisement` in voice library. Narrative-story voices sound great but wrong cadence for ad copy. Maya (`U3dExJoUNcmTY5H6GMuG`) = warm/calm/soft advertisement. Citra (`RbNgJzKAV7jpYJNtCBpj`) = narrative_story.
- **Indonesian language**: always use `model_id: eleven_multilingual_v2`. Default `eleven_turbo_v2` is English-only and butchers pronunciation.
- **Built-in fallback**: if `provider: edge` (default), output is `.ogg` English voice regardless of voice_id config. Must patch provider to `elevenlabs` explicitly.
- **Gateway restart cost**: every config change touching MCP or TTS needs gateway restart. User may have a no-downtime preference — check before bouncing.

## Voice settings cheat sheet (ads/narration in Bahasa)

- `stability`: 0.45–0.55 (lower = more emotion, higher = monotone)
- `similarity_boost`: 0.75–0.85
- `style`: 0.2–0.4 (higher exaggerates voice traits — costs latency)
- `speed`: 0.95–1.05 (ads slightly slower, hooks slightly faster)
- `use_speaker_boost`: `true`

## A/B testing voice for production

When user is picking a voice for production, generate the **same script** across:
- 2–3 candidate voices (always include 1 advertisement-tagged voice)
- Same voice across 2–3 setting profiles (low/mid/high stability)
- Across all 3 paths if they want to compare setup overhead

Deliver MP3s with descriptive filenames: `<voice>_<path>_<version>.mp3`. Never deliver one sample and ask "good?" — user can't compare against nothing.

## References
- `references/voice-library-bahasa.md` — known good Indonesian voices and which use case they fit
- `references/comparison-mcp-vs-rest-vs-builtin.md` — when to pick which path, setup cost, latency, key handling, reproducibility
