---
name: image-gen-9router
description: "Use when user asks to generate, create, render, bikin, atau buat image/gambar/picture. Route via 9Router (cx/gpt-5.5-image), never FAL/Pollinations/DALL-E."
version: 1.0.0
author: Hermest CMO
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [image-generation, 9router, hermest, gpt-image, routing]
    related_skills: [hermes-agent, hermes-custom-provider]
---

# Image Generation via 9Router (Hermest)

## Overview

Bos (user) routes ALL image generation through **9Router** running on his MacBook. Model: `cx/gpt-5.5-image`. This skill exists because agents keep defaulting to FAL/Pollinations/DALL-E and getting stuck on `FAL_KEY` errors when the actual configured provider is 9Router.

**Never suggest FAL, fal.ai, Pollinations, or direct DALL-E.** They are not Bos's setup.

## When to Use

Trigger on ANY of these:
- "bikin image / gambar / picture"
- "generate image / picture / gambar"
- "buat ilustrasi / poster / visual"
- "render <visual thing>"
- Tool `image_generate` returns error mentioning `FAL_KEY`
- User screenshots an image gen failure

**Don't use for:**
- HTML/CSS screenshot workflows (different tool, IG text posts)
- Video generation (separate skill)
- Image *analysis* (vision tool, not generation)

## Routing Decision

Determine environment FIRST. Do NOT guess.

| Environment | Base URL | Notes |
|-------------|----------|-------|
| MacBook (Hermest desktop app) | `http://127.0.0.1:20128/v1` | 9Router localhost, fastest |
| VPS Hermest CMO | `http://100.119.69.80:20128/v1` | Tailscale to MacBook |
| Anywhere else | STOP, ask Bos | Don't fallback to FAL |

Model is always: `cx/gpt-5.5-image`
Auth header always: `Authorization: Bearer <9ROUTER_API_KEY>`

API key source: `http://127.0.0.1:20128/dashboard` (open on MacBook). Key is per-9Router-instance, not OpenAI/Anthropic.

## Configuration (Hermes Agent)

Set image_gen provider to OpenAI-compatible pointing at 9Router:

```bash
hermes config set image_gen.provider openai
hermes config set image_gen.openai.base_url http://127.0.0.1:20128/v1
hermes config set image_gen.openai.model cx/gpt-5.5-image
hermes config set image_gen.openai.api_key "<9ROUTER_KEY>"
hermes tools enable image_gen
```

For VPS, replace `127.0.0.1` with `100.119.69.80`.

After config change: `/reset` in chat OR `hermes gateway restart` if running as service.

## Direct API Call (if tool unavailable)

```bash
curl -s http://127.0.0.1:20128/v1/images/generations \
  -H "Authorization: Bearer $NINE_ROUTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "cx/gpt-5.5-image",
    "prompt": "A red apple on white background, square, studio lighting",
    "size": "1024x1024"
  }' | jq -r '.data[0].url' | xargs -I{} curl -s -o /tmp/out.png {}
```

Then deliver: `MEDIA:/tmp/out.png`

## Prompt Quality

Bos prefers concise, visual prompts. Format:
- Subject + descriptor
- Style (realistic / illustration / 3D / minimal / cinematic)
- Lighting + mood
- Composition + aspect ratio

Example:
- ❌ "monkey"
- ✅ "Funny realistic monkey portrait, expressive face, detailed fur, jungle background bokeh, wildlife photography, vibrant colors, sharp focus, square 1:1"

## Aspect Ratios

Map user intent → size param:
- square / IG square → `1024x1024`
- IG feed portrait 4:5 → `1024x1280`
- story / reels 9:16 → `1024x1792`
- landscape 16:9 → `1792x1024`

## Common Pitfalls

0. **Hermes `image_generate` tool is broken for custom base_url (as of 2026-05).** Even with `image_gen.provider=openai` + `image_gen.openai.base_url` set to 9Router, the tool still hits OpenAI hardcoded endpoint with hardcoded model `gpt-image-2-medium`. Returns 401 invalid_api_key. WORKAROUND: skip `image_generate` tool, use direct curl recipe below. Save b64_json to /root/.hermes/workspace/<name>.png.

1. **Defaulting to FAL_KEY error path.** Tool's default error message mentions fal.ai. IGNORE it. Switch to 9Router config or direct curl. Don't relay "daftar fal.ai" to user.

2. **Wrong environment check.** Claude Code shell ≠ Hermes profile. Check `hermes config path` and `hermes status --all` to confirm which Hermes instance you're configuring.

3. **Treating 9Router key as OpenAI key.** It's instance-local. MacBook 9Router key works only when endpoint is reachable to MacBook (localhost on Mac, Tailscale from VPS).

4. **Cloudflare tunnel.** `r6jkibc.abc-tunnel.us` is dead/unstable. Don't use it. Tailscale `100.119.69.80` is the reliable route from VPS.

5. **Forgetting `/reset` after config change.** Toolset/provider changes don't take effect mid-session. Always restart session or gateway.

6. **Suggesting HTML/CSS screenshot as fallback.** Only do this if Bos explicitly asks for IG-text-post style content. For "bikin gambar X" requests, the answer is 9Router image.

## Verification Checklist

- [ ] Identified environment (MacBook vs VPS vs other)
- [ ] Base URL set correctly (`127.0.0.1` on Mac, Tailscale IP from VPS)
- [ ] Model = `cx/gpt-5.5-image`
- [ ] 9Router API key in place (from dashboard `http://127.0.0.1:20128/dashboard`)
- [ ] Test request returns image URL or binary
- [ ] Delivered to user via `MEDIA:<path>` or markdown image
- [ ] Did NOT mention FAL / Pollinations / DALL-E

## One-Shot Recipes

**User just says "bikin gambar X" on MacBook Hermest:**
1. Run config block above (one time setup)
2. `/reset`
3. Call `image_generate` tool with detailed prompt
4. Deliver result

**User says "bikin gambar X" from VPS Hermest CMO:**
1. Verify Tailscale reachable: `curl -s http://100.119.69.80:20128/v1/models -H "Authorization: Bearer $KEY"`
2. If 200 → use direct curl recipe above
3. If fail → tell Bos Tailscale/9Router needs fixing, paste raw error
