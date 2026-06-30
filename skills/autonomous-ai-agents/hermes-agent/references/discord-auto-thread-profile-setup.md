# Discord auto-thread for profile gateways

Use this when the user asks why a Hermes/secondary profile does not automatically create Discord threads, or asks to make one profile behave like another.

## What to verify first

1. Check whether the target profile actually has Discord enabled. A profile with only another platform (for example WhatsApp) cannot auto-thread in Discord regardless of gateway code.
2. Check the main/default profile separately from secondary profiles. Do not infer CMO/profile behavior from the CEO/default config.
3. Confirm existing Hermes Discord code supports auto-thread before proposing a custom bot or code patch.

## Known implementation points

In the Hermes Discord adapter, auto-thread is implemented by the platform code, not by a separate bot:

- `_auto_create_thread(self, message)` builds a title from message content, strips Discord mentions, caps it around 80 chars, and falls back to `Hermes`.
- Primary path: `message.create_thread(name=thread_name, auto_archive_duration=1440)`.
- Fallback path: send a seed message like `🧵 Thread created by Hermes: **...**`, then create a thread from that seed message.
- Config mapping exists for `discord.auto_thread` → `DISCORD_AUTO_THREAD`, plus related keys like `discord.free_response_channels`, `discord.allowed_channels`, and `discord.no_thread_channels`.

## Minimal config shape

Add Discord to the target profile config using an env var placeholder for the token. Never paste or persist the real token in notes, summaries, or skills.

```yaml
platforms:
  discord:
    enabled: true
    token: ${DISCORD_BOT_TOKEN_CMO}
    extra:
      slash_commands: true

# Top-level discord behavior config
discord:
  require_mention: false
  auto_thread: true
  thread_require_mention: false
  free_response_channels: ''
  no_thread_channels: ''
```

Adapt the env var name to the profile, but keep the value in `.env`/service environment only.

## Safe workflow

1. Read the profile config and gateway logs first; avoid guessing from memory.
2. If the source profile already auto-threads, point out that no code patch is needed.
3. If the target profile lacks Discord, add the minimal platform config and token env only after user approval.
4. Do not restart/start/reload a live gateway without explicit approval. If restart is needed, explain why and the risk, then wait.
5. After applying, verify with logs and an actual Discord message: inbound text channel message should result in a thread context/flush rather than a plain group response.

## Common pitfall

A process environment may show `DISCORD_AUTO_THREAD` unset while config has `discord.auto_thread: true`; Hermes can map config to env at startup. Treat config + adapter behavior + logs together instead of relying on env alone.
