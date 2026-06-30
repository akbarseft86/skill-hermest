# Cron-to-WhatsApp forwarding via local bridge

Use this pattern when a Hermes instance can generate scheduled reports, but the active profile does not expose `send_message(target='whatsapp')` as a configured messaging target.

## When to use
- A secondary Hermes profile (for example a CMO / WhatsApp profile) already runs a local WhatsApp bridge.
- `send_message(action='list')` on the current profile does not show WhatsApp, or `send_message(target='whatsapp', ...)` fails with "Platform 'whatsapp' is not configured".
- You still need scheduled reports delivered to a specific WhatsApp number.

## Working pattern
1. Keep the analysis/report cron job separate from transport.
   - Example: a weekly BBSI monitor cron writes its normal output under `~/.hermes/cron/output/<job_id>/...`.
2. Add a second `no_agent=True` cron job a few minutes later.
3. That forwarding script should:
   - check `http://127.0.0.1:3013/health`
   - require `status == connected`
   - find the latest report file in the source job's cron output directory
   - keep a small state file with the last forwarded path to avoid duplicate sends
   - POST the full report body to `http://127.0.0.1:3013/send`
4. Send to the E.164-style WhatsApp JID, e.g. `6285285616667@s.whatsapp.net`.

## Minimal forwarding script shape
```python
health = GET('http://127.0.0.1:3013/health')
assert health['status'] == 'connected'
latest = newest_file('~/.hermes/cron/output/<source_job_id>/*.md')
if latest != last_sent_state:
    POST('http://127.0.0.1:3013/send', {
        'chatId': '6285...@s.whatsapp.net',
        'message': latest_file_text,
    })
    save_state(latest)
```

## Why this is useful
- Decouples report generation from channel delivery.
- Lets the main Hermes profile keep delivering to `origin` while WhatsApp delivery is handled by the bridge that is actually authenticated.
- Preserves the full report body, not just a status color or summary.

## Validation checklist
- Bridge health endpoint returns `status: connected`.
- `GET /chat/<jid>` resolves the recipient chat.
- `POST /send` returns `success: true` and a `messageId`.
- The forwarding cron runs after the source cron, not before.

## Pitfalls
- Do not assume `send_message` availability and bridge health are equivalent. They are separate paths.
- Do not send only a green/yellow/red label for monitoring jobs when the user wants to audit the research. Forward the complete report text with sources and validation notes.
- Add a dedupe state file; otherwise manual runs plus scheduled runs can resend the same report repeatedly.
