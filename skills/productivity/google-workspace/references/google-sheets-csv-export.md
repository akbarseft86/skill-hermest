# Google Sheets CSV Export (No-Auth)

Public ("anyone with link") Google Sheets can be exported as CSV via a direct
download URL — no OAuth, no API key, no `gws` CLI needed. This is the fastest
way to scrape structured data from a shared spreadsheet when you just need
to read cells.

## Export URL Pattern

```
https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv
```

Where `{SPREADSHEET_ID}` is the long alphanumeric string in the sheet URL:

- Full URL: `https://docs.google.com/spreadsheets/d/1L9b9dhLtf3Ien9KVkdfv3Bd7eprYm3GmHSHOaL0Rw8w/edit?usp=sharing`
- ID: `1L9b9dhLtf3Ien9KVkdfv3Bd7eprYm3GmHSHOaL0Rw8w`

## Download via curl

```bash
curl -sL -o /tmp/sheet.csv \
  "https://docs.google.com/spreadsheets/d/{ID}/export?format=csv"
```

Flags:
- `-s` — silent (no progress meter)
- `-L` — follow redirects (Google may redirect)
- `-o` — output file

## Read directly to stdout

```bash
curl -sL "https://docs.google.com/spreadsheets/d/{ID}/export?format=csv"
```

## Parse with Python

Once the CSV is downloaded, use Python stdlib `csv` module:

```python
import csv, io

resp = __import__('urllib.request').request.urlopen(
    'https://docs.google.com/spreadsheets/d/{ID}/export?format=csv'
)
reader = csv.reader(io.StringIO(resp.read().decode('utf-8')))
for row in reader:
    print(row)
```

Or from a local file:

```python
import csv
with open('/tmp/sheet.csv') as f:
    reader = csv.reader(f)
    rows = list(reader)  # all rows as list of lists
```

## Notes

- **Public sheets only** — this export URL does NOT authenticate. Only works
  for sheets shared with "Anyone with the link → Viewer/Editor".
- **First sheet only** — the export?format=csv endpoint returns only the first
  tab. For other tabs, you'd need the Sheets API (requires OAuth).
- **Single sheet** — merged cells appear with the value only in the first cell.
- **No formatting** — CSV is raw data with no styling, formulas, or images.
  Formulas are exported as their *computed values*, not the formula text.
- **Rate limit** — Google may temporarily block rapid repeated exports from the
  same IP. Space requests at least a few seconds apart.
- **Large sheets** — Google sheets have a 10M cell limit; CSV export works
  up to that limit. Very large files may take several seconds to download.