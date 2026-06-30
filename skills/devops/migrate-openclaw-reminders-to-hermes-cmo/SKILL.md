---
name: migrate-openclaw-reminders-to-hermes-cmo
description: Migrate legacy OpenClaw/Titi-Teliti reminder cron jobs into the Hermest CMO profile so reminders are delivered via the CMO bot's WhatsApp account, then remove the duplicate legacy cron entry.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [openclaw, hermes-cmo, cron, whatsapp, migration, reminders]
---

# Migrate OpenClaw Reminders to Hermest CMO

Use when:
- legacy reminders still live in root crontab or `titi-teliti`
- the user wants reminder delivery moved from old OpenClaw flows to the CMO bot
- WhatsApp delivery should happen from `/root/.hermes-cmo`

## What this workflow solved
In this environment, the old reminder system was split across:
- root `crontab`
- `/root/titi-teliti/send_reminder.sh`
- `/root/titi-teliti/run_due_custom_reminders.py`
- `/root/titi_teliti.db` and `/root/titi-teliti/reminders.db`

The desired migration path was:
1. inspect the legacy reminder source of truth
2. extract the real reminder meaning/details
3. create a new Hermes cron job in the CMO profile with WhatsApp delivery
4. remove the old one-off cron entry to avoid duplicate sends

## Prerequisites
- CMO profile exists at `/root/.hermes-cmo`
- Hermes CLI exists at `/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main`
- CMO WhatsApp platform is configured and connected
- You know the target WhatsApp delivery ID (for this setup: inspect `/root/.hermes-cmo/channel_directory.json`)

## Proven discovery steps

### 1. Inspect legacy crontab
```bash
crontab -l 2>/dev/null
```

Look for lines calling:
- `/root/titi-teliti/send_reminder.sh`
- `/root/titi-teliti/run_due_custom_reminders.py`

### 2. Read reminder scripts and custom files
```bash
sed -n '1,200p' /root/titi-teliti/send_reminder.sh
sed -n '1,220p' /root/titi-teliti/run_due_custom_reminders.py
sed -n '1,240p' /root/titi-teliti/reminder.py
find /root/titi-teliti/custom-reminders -maxdepth 1 -type f -name '*.txt'
```

### 3. Inspect reminder databases directly
```bash
python3 - <<'PY'
import sqlite3
conn=sqlite3.connect('/root/titi-teliti/reminders.db')
for row in conn.execute("SELECT id,title,message_file,remind_at,status,sent_at FROM custom_reminders ORDER BY remind_at,id"):
    print(row)
conn.close()
PY
```

```bash
python3 - <<'PY'
import sqlite3
conn=sqlite3.connect('/root/titi_teliti.db')
conn.row_factory=sqlite3.Row
for row in conn.execute("SELECT t.id,t.title,t.details,t.due_date,t.priority,t.status,p.name as project_name FROM tasks t LEFT JOIN projects p ON p.id=t.project_id ORDER BY t.due_date,t.id"):
    print(dict(row))
conn.close()
PY
```

This matters because the cron line alone may not say what the reminder is actually for. In this environment, the important reminder text lived in task `details`, not just the title.

## Proven migration flow

### 4. Verify CMO WhatsApp delivery target
Read:
```bash
sed -n '1,200p' /root/.hermes-cmo/channel_directory.json
```

For this setup, the user DM target was:
```text
whatsapp:186749590483065@lid
```

### 5. Verify Hermes CMO cron subsystem is available
```bash
HERMES_HOME=/root/.hermes-cmo /root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron status
HERMES_HOME=/root/.hermes-cmo /root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list --all
```

### 6. Create the replacement reminder in the CMO profile
Use a self-contained prompt so the future cron run needs no chat context.

Pattern:
```bash
HERMES_HOME=/root/.hermes-cmo /root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron create '0 22 24 6 *' 'Kirim pesan WhatsApp ini persis apa adanya ke user dan jangan tambah komentar lain:
⏰ Reminder pembayaran Jogjamerapi (One Google)
Hari ini cek subscription dan batalkan sebelum kena charge.
Upcoming charges yang tercatat:
- Rp3.000 mulai 29 Apr 2026
- Rp309.000 mulai 29 Jun 2026
Target: cancel subscriber sebelum charge 29 Jun 2026.' --name 'reminder-jogjamerapi-one-google' --deliver 'whatsapp:186749590483065@lid'
```

### 7. Remove the duplicate legacy cron entry
Only remove the exact matching one-off line, not the whole Titi-Teliti system.

Pattern used successfully:
```bash
python3 - <<'PY'
import subprocess
old = subprocess.run(['crontab','-l'], capture_output=True, text=True)
lines = old.stdout.splitlines()
needle = "0 22 24 6 * . /root/titi-teliti/titi.env 2>/dev/null; /usr/bin/bash /root/titi-teliti/send_reminder.sh 2026-06-25 >> /root/titi-teliti/titi.log 2>&1"
new_lines = [line for line in lines if line.strip() != needle.strip()]
content = '\n'.join(new_lines) + ('\n' if new_lines else '')
subprocess.run(['crontab','-'], input=content, text=True, check=True)
print('removed' if len(new_lines) != len(lines) else 'not_found')
print(content)
PY
```

### 8. Verify final state
```bash
HERMES_HOME=/root/.hermes-cmo /root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main cron list --all
crontab -l
```

## Important experiential findings
- The real reminder meaning may be stored in `/root/titi_teliti.db` task details, not in the raw cron line.
- `channel_directory.json` is the fastest reliable way to get the CMO WhatsApp DM target.
- Hermes CLI cron jobs created from the CLI can default to repeating forever with a cron expression. If the user wants a one-time reminder, explicitly convert to a one-shot schedule or tell them the cron will recur yearly.
- Remove only the specific legacy one-off cron line; do not blindly delete all `titi-teliti` jobs because daily reminders/custom reminder runners may still be wanted.

## Pitfalls
- Do not assume the reminder title tells the full story; always inspect `details`.
- Do not create the new CMO cron before confirming WhatsApp is actually configured in `/root/.hermes-cmo`.
- Do not leave both legacy and new reminder active unless the user explicitly wants duplicate sends.
- Do not forget to warn the user if the new cron expression repeats indefinitely.

## Success criteria
- Legacy reminder intent identified from DB/scripts
- Replacement cron exists under `/root/.hermes-cmo`
- Delivery target is the user’s WhatsApp DM
- Duplicate old one-off cron entry removed
- User is told whether the new reminder is recurring or one-time
