---
name: hermes-telegram-gateway-setup
description: Configure, validate, and start Hermes Agent on Telegram, including gateway startup, persistent service installation, and end-to-end bot verification.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Hermes Telegram Gateway Setup

Use this skill when a user wants Hermes to work through Telegram and you need to confirm the bot is actually usable, not merely partially configured.

## When to use
- User says they already provided a Telegram bot token and asks whether it is installed
- User wants Telegram gateway enabled end-to-end
- `hermes status --all` shows Telegram configured but gateway stopped
- Need to verify the bot can really send messages

## Important findings
- `read_file` may show secrets in redacted form; do not assume that redacted text is the literal file content.
- `patch` may be denied on protected credential files such as `.env`; if credentials must be changed, use an approved shell/Python edit path instead.
- Hermes may use a user-level env file for Telegram credentials instead of a project-local `.env`; use `hermes config env-path` to locate the active env file before diagnosing token/allowlist issues.
- `hermes status --all` is the fastest way to confirm both Telegram configuration and gateway service state.
- `hermes gateway install` is the right path for persistence; it installs a user systemd service and can confirm linger status.
- In Telegram groups with `require_mention: true`, the bot still responds when directly `@mentioned`, replied to, invoked via command, or matched by configured `mention_patterns`; a plain group message without one of those triggers is expected to be ignored.
- Before blaming a legacy gateway/service for Telegram polling conflicts, compare the actual bot tokens/identities. Two different Telegram bots can coexist in the same group and on the same VPS without conflict; the real conflict case is multiple pollers using the same bot token.
- Legacy OpenClaw installs may keep their Telegram bot token in `~/.openclaw/openclaw.json` under `channels.telegram.botToken`, while Hermes uses the env file returned by `hermes config env-path`.
- When migrating a legacy Telegram bot from OpenClaw to Hermes, the cleanest cutover is often a separate Hermes home (for example `/root/.hermes-cmo`) plus a dedicated user service (for example `hermes-cmo-gateway.service`) with `HERMES_HOME` set explicitly. This avoids config/session/memory collisions with the main Hermes bot.
- For a cutover of the SAME bot token, do not run OpenClaw and Hermes simultaneously. Prepare the Hermes home first, then stop/disable the OpenClaw gateway service, start the Hermes service, and only then verify the bot.
- In newer Hermes builds, `hermes login` may be removed. For OpenAI Codex OAuth on a specific Hermes instance/home, use `HERMES_HOME=/path/to/home hermes auth add openai-codex --type oauth --label <label> --no-browser`, then complete the device-code flow. This stores credentials in that instance's `auth.json` instead of the main Hermes home.
- End-to-end verification should include both bot identity validation and an actual message delivery test.

## Procedure

1. Check status first.
- Run `hermes status --all`
- Run `hermes gateway status`
- Confirm Telegram shows as configured.
- Confirm whether the gateway is stopped or running.

2. Confirm required Telegram environment settings exist.
- Verify that the Hermes `.env` contains `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS`.
- If the token must be changed, update `.env` via an approved shell/Python edit flow rather than relying on `patch`.

3. Validate the bot token.
- Query Telegram `getMe` for the configured token.
- Confirm `ok: true` and capture the bot username and id.

4. Start the gateway.
- Try `hermes gateway run` if you need a quick manual foreground check.
- For normal production use, install the persistent service with `hermes gateway install`.
- Start it with `hermes gateway start`.
- Re-check with `hermes gateway status`.

5. Verify persistence and logs.
- Confirm the gateway service reports `active (running)`.
- If needed, inspect `journalctl --user -u hermes-gateway` for startup problems.

6. Verify end-to-end delivery.
- Send a real Telegram test message from the bot to the allowed user/chat.
- Treat the setup as complete only when Telegram API delivery succeeds and the user receives the test message.

## Success criteria
- Telegram is configured in `hermes status --all`
- `hermes gateway status` reports running
- The service is installed and persistent
- Bot identity is confirmed
- A real test message is delivered successfully

## What to tell the user after success
- Token is installed and valid
- Gateway is running
- The service is persistent
- The bot username to open in Telegram
- Ask the user to open the bot, press Start if needed, and send a test message

## Failure modes
- Gateway not running: install/start the service
- Token validation fails: wrong or revoked token
- Bot can send messages but user gets no reply: user may need to open the bot and press Start first
- Protected credential file write denied: use approved shell/Python editing for `.env`
- Repeated `getUpdates` conflict warnings in `journalctl`: another process/service is polling the same Telegram token. Check `systemctl --user list-units --type=service --all | grep -i openclaw` and process list for legacy runners such as `openclaw-gateway.service`, then stop/disable the duplicate before re-testing.
- `send_message(target='telegram')` fails with no home channel: send directly to `telegram:<chat_id>` for verification or configure `TELEGRAM_HOME_CHANNEL` first.
