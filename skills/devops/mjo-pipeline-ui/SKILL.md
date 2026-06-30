---
name: mjo-pipeline-ui
description: Maintain and extend the MJO pipeline web UI — content form, antrian queue, upload jadwal. Covers architecture, adding new fields, deployment.
---

# MJO Pipeline Web UI

The MJO pipeline has a **3-layer architecture**:

```
HTML/CSS/JS (frontend)    →   /var/www/html/*.html
       ↓
mjo_api.py (HTTP server)  →   /opt/mjo-api/mjo_api.py   (LIVE)
                                 /root/mjo-pipeline/backend/mjo_api.py   (DEV)
       ↓
pipeline_db.py (SQLite)   →   /opt/mjo-api/pipeline_db.py   (LIVE)
                                 /root/mjo-pipeline/backend/pipeline_db.py   (DEV)
```

## Pages

| Page | URL | Purpose |
|------|-----|---------|
| Content Form | `/content-form.html` | Daftar konten baru + AI generate copy/headline |
| Antrian Queue | `/content-queue.html` | Edit status, LP, ad copy, headline per kartu |
| Jadwal | `/mjo-jadwal.html` | Schedule konten ke tanggal + jam + akun |
| Dashboard | `/mjo-dashboard.html` | Overview performance |

## Adding a new field to a feature (e.g. schedule jam)

Always touch all 3 layers:

### 1. DB (pipeline_db.py)

- Add column to `CREATE TABLE IF NOT EXISTS` for new installs
- Add migration guard for existing databases: check `PRAGMA table_info(table_name)`, `ALTER TABLE ADD COLUMN IF NOT EXISTS`
- Update model functions: add parameter to `add_schedule()`, include column in `list_schedule()` SELECT + ORDER BY

```python
# Migration guard pattern
cols = {r['name'] for r in c.execute('PRAGMA table_info(upload_schedule)').fetchall()}
if 'jam' not in cols:
    c.execute('ALTER TABLE upload_schedule ADD COLUMN jam TEXT')
```

### 2. API (mjo_api.py)

- Extract the new field from request body: `b.get('jam') or ''`
- Pass it to the DB function
- The GET handler returns items from `list_schedule()` — no change needed if `list_schedule()` already returns the column

### 3. Frontend (HTML)

- Add input in the form: `<input type="time" id="jam" value="09:00">`
- Include value in POST body: `jam:$('jam').value`
- Display in the saved list: `i.jam?'🕐 '+esc(i.jam):''`
- The row template uses `i.jam` from the API response

## Dev vs Deploy

- **DEV files**: `/root/mjo-pipeline/backend/` — edit these
- **LIVE files**: `/opt/mjo-api/` — running process reads from here
- **Sync step**: After editing dev, `cp` both `.py` files to `/opt/mjo-api/`
- **Restart**: The API runs as a long-lived process (`ps aux | grep mjo_api`). Restart requires explicit user approval per Hermes anti-shutdown rules.

Check the active process path first with `ps aux | grep mjo_api | grep -v grep`. It may be a different copy than expected.

## API Endpoints (relevant)

| Method | Path | Body | Returns |
|--------|------|------|---------|
| GET | `/api/schedule` | — | `{ok, items: [{id, tanggal, jam, content_id, judul, cep, akun, budget, status}]}` |
| POST | `/api/schedule` | `{tanggal, jam, content_ids: [id], akun, budget}` | `{ok, added: count}` |
| POST | `/api/schedule/delete` | `{id}` | `{ok, deleted: count}` |
| GET | `/api/content?live=1` | — | Content queue with live status |
| POST | `/api/content/update` | `{id, landing_page, ad_copy, headline, ...}` | Update content fields |

## Auto-open after scheduling

After adding a schedule item (POST `/api/schedule`), the frontend:
- Calls `SEL.clear()`, `updSel()`, `renderPicker()`, `loadList()` to refresh the UI
- No further navigation needed

## Debugging slow page loads

The most common cause of slowness is the **`?live=1` path** on the content queue. When `content-queue.html` loads with `?live=1`, the API calls `meta_ads_index()` which pulls live ad status from Meta Graph API for every MJO account — can take 5+ seconds.

### Quick diagnosis

```bash
# Time the first request
curl -s -o /dev/null -w 'first  %{time_total}s\n' 'http://127.0.0.1:8787/api/content?live=1'
# Compare with a second request after cache warms
curl -s -o /dev/null -w 'second %{time_total}s\n' 'http://127.0.0.1:8787/api/content?live=1'
```

If first is 4–6s and second is <1s → the bottleneck is the Meta API calls and a TTL cache is the fix.

### Root cause

The request path: `GET /api/content?live=1` → `_match_live()` → `meta_ads_index()` → calls Meta Ads MCP `get_ads` for each MJO account, then maps to creative fields for status lookup. This happens on **every** page load with no caching, because ad/live status was assumed to change frequently.

### Fix: short TTL cache around meta_ads_index()

```python
_INDEX_CACHE = {"ts": 0, "data": None}
_INDEX_CACHE_TTL = 120  # seconds

def meta_ads_index():
    now = time.time()
    if _INDEX_CACHE["data"] is not None and now - _INDEX_CACHE["ts"] < _INDEX_CACHE_TTL:
        return _INDEX_CACHE["data"]

    # ... existing Meta loop ...

    _INDEX_CACHE["ts"] = now
    _INDEX_CACHE["data"] = idx
    return idx
```

See `references/content-queue-live-status-cache.md` for full details, verification, and pitfalls.

## Pitfalls

- **PRAGMA migration only works on columns that don't exist yet** — subsequent ALTER TABLE fails silently on some SQLite versions. Always guard with `IF NOT EXISTS` style check.
- **Restart kills existing connections** — the API is single-process. Restart briefly interrupts service. Always ask user before restarting.
- **frontend HTML reads `i.jam` from API response** — if `jam` column is NULL (existing rows before migration), JS handles it gracefully with empty string, but the display check `i.jam?'...':''` must account for empty/null.
- **TTL cache is per-process memory** — restart clears it. First request after restart always warms fresh. Keep TTL short (120s) so status is operationally current.
- **Patch both DEV and LIVE copies** — the cache fix must go in both `/root/mjo-pipeline/backend/mjo_api.py` and `/opt/mjo-api/mjo_api.py`. Then sync and restart only with user approval.
- **Do not cache the full content list** — only the Meta ads index. The content list (with user edits) should always be read fresh from DB. Caching wrong data here leads to stale UI bugs.
