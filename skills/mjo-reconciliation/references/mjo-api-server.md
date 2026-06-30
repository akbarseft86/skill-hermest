# MJO Interactive API Server Pattern

Use this reference when an MJO dashboard needs a date-range picker that triggers a fresh server-side pull from Meta Ads + Scalev, instead of only reading a static JSON file.

## Trigger phrases
- "bisa milih tanggal"
- "kalau dipilih tanggal baru narik data"
- "date range picker"
- "data trigger dari tanggal yang saya pilih"
- "jangan filter dari data lama, tarik data baru"

## Architecture

Static HTML stays public and credential-free. Data pulling happens behind nginx via a local Python HTTP server.

```
/var/www/html/mjo-dashboard.html
  fetch('/api/mjo-data?since=YYYY-MM-DD&until=YYYY-MM-DD&force=1')

/etc/nginx/conf.d/website.conf
  location /api/ { proxy_pass http://127.0.0.1:8787; }

/opt/mjo-api/mjo_api.py
  stdlib http.server on 127.0.0.1:8787
  pulls Meta Ads + Scalev using server-side config/tool credentials
  writes /var/www/html/mjo-data.json and /var/www/html/mjo-data-reconciled.json
  returns enriched JSON to browser
```

## Endpoint contract

`GET /api/mjo-data?since=YYYY-MM-DD&until=YYYY-MM-DD&force=1`

Required behavior:
- Validate date format and range.
- Pull Meta Ads at `level=ad` for the account pair mapped to the store.
- Pull Scalev store totals using `status=completed`, `datetime_type=paid_time`, `breakdown_date=day`, `store_id`.
- Pull Scalev per-content with `utm_content == ad_name` when possible.
- Merge per-content fields into every row: `scalev_result`, `scalev_revenue`, `scalev_cpr`, `meta_scalev_diff`, `meta_scalev_match_rate`.
- Return the same JSON shape expected by the dashboard.
- Never expose Meta/Scalev tokens in response or frontend.

## Minimal nginx proxy block

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8787;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 300s;
    proxy_connect_timeout 10s;
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods "GET, OPTIONS";
    add_header Access-Control-Allow-Headers "*";
}
```

After editing nginx:

```bash
nginx -t
nginx -s reload
```

## Frontend date picker requirements

Match owner screenshot style:
- Floating panel under date button.
- Left shortcut column: Today, Yesterday, This week, Last 1 week, Last 2 weeks, This month.
- Two calendars side-by-side.
- Month navigation arrows.
- Week starts Monday (`Mo Tu We Th Fr Sa Su`).
- Start/end dates use blue filled circles.
- In-range dates use light blue background.
- Out-of-month dates muted gray.
- Apply triggers API call.
- Cancel closes overlay.

## Dashboard refresh modes

Ask owner if uncertain:
1. **Dynamic update** (recommended): `fetch()` JSON and re-render summary/table without reload.
2. **Full reload**: update query string `?since=...&until=...`, then reload; page init calls the API.

Default to dynamic update when the owner emphasizes a dashboard-like interactive feel.

## Loading and failure handling

During API call:
- Disable Apply button.
- Show status like `Menarik data Meta + Scalev... bisa 30–60 detik`.
- Preserve current table until new data succeeds.

On failure:
- Show visible error panel with timestamp and HTTP status/message.
- Do not clear old data.
- Add a retry action using the same date range.

## Important implementation notes

### CTR formatting
Meta Ads `ctr` already arrives as a percent value (`3.58` = `3.58%`). Do not multiply by 100.

### Scalev per-content speed
Per-content Scalev enrichment is expensive because it may call one API request per unique `ad_name`. If it becomes too slow:
- Load Meta ad-level data first.
- Return `scalev_result: null` rows with `scalev_status: 'pending'`.
- Enrich in a second background request or cron.

### Server persistence
A raw background process will not survive reboot. For a durable deployment, create a systemd unit:

```ini
[Unit]
Description=MJO Dashboard API
After=network.target

[Service]
WorkingDirectory=/opt/mjo-api
ExecStart=/usr/bin/python3 /opt/mjo-api/mjo_api.py
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
```

Then:

```bash
systemctl daemon-reload
systemctl enable --now mjo-api.service
systemctl status mjo-api.service
```

Only restart/stop services with explicit owner approval if Hermes anti-shutdown protocol is active.

## Verification checklist

- [ ] `curl http://127.0.0.1:8787/health` returns OK.
- [ ] `curl 'http://127.0.0.1:8787/api/mjo-data?since=2026-06-01&until=2026-06-19&force=0'` returns JSON.
- [ ] `nginx -t` passes.
- [ ] Public endpoint works: `https://hermest.gerbangduid.my.id/api/mjo-data?...`.
- [ ] Browser console has no JS errors.
- [ ] Selecting a date range changes `summary.period.short` and table rows.
- [ ] No API keys/tokens appear in HTML or JSON.
