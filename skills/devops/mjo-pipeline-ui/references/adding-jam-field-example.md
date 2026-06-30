# Adding "jam" field to schedule — concrete example

This reference documents the exact implementation of adding a waktu/jam field
to the MJO upload schedule feature. Use it as a template for future field additions.

## Problem

Form jadwal only had `tanggal`, `akun`, `budget`. User wanted to also set **jam**
(waktu upload iklan) per jadwal item.

## Files changed

| File | Change |
|------|--------|
| `pipeline_db.py` | Schema: add `jam TEXT` column. Functions: `add_schedule()` gets `jam` param, `list_schedule()` returns `jam`, ORDER BY now uses `COALESCE(s.jam,'')` |
| `mjo_api.py` | POST handler extracts `b.get('jam')` and passes to `add_schedule()` |
| `mjo-jadwal.html` | Form: `<input type="time" id="jam" value="09:00">`. JS POST body: includes `jam`. Display: shows `🕐 ${i.jam}` |

## Schema migration

```sql
-- For new tables (CREATE):
jam TEXT,  -- added between tanggal and content_id

-- For existing databases:
cols = PRAGMA table_info(upload_schedule)
if 'jam' not in cols:
    ALTER TABLE upload_schedule ADD COLUMN jam TEXT
```

## Database function changes

```python
def add_schedule(tanggal, content_ids, akun='', budget=0, jam=''):
    jam = (jam or '').strip()
    c.execute('''INSERT INTO upload_schedule(tanggal,jam,content_id,akun,budget,status,created_at)
        VALUES(?,?,?,?,?,'PLANNED',?)''', (tanggal, jam, int(cid), akun, int(budget or 0), iso))

def list_schedule():
    rows = c.execute('''SELECT s.id,s.tanggal,s.jam,s.content_id,s.akun,s.budget,s.status, ...
        ORDER BY s.tanggal, COALESCE(s.jam,''), s.id''')
```

## API change

```python
n = pipeline_db.add_schedule(tanggal, ids, akun, budget, 
    (b.get('jam') or '').strip())
```

## Frontend

```html
<!-- Form input -->
<div><label>Jam</label><input type="time" id="jam" value="09:00"></div>

<!-- POST body -->
{..., jam:$('jam').value}

<!-- Display in saved list -->
${i.jam?'🕐 '+esc(i.jam):''} · ${esc(i.akun||'')} · ${rupiah(i.budget)}
```

## Deploy

1. Edit `/root/mjo-pipeline/backend/` files
2. `cp` to `/opt/mjo-api/`
3. Restart API process (ask user)
