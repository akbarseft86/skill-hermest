# Airbnb Link Patterns & Location Audit Notes

Session-derived notes from building a Bali July 2026 accommodation audit dashboard.

## Link Pattern Observation

When scraping Airbnb search cards, multiple `a[href*="/rooms/"]` anchors can point to non-listing IDs. In the Bali session:

- Short IDs such as `2655482324`, `2601249124`, `1639891132` opened as Airbnb `404 Page Not Found`.
- Long IDs such as `1647450330369792562`, `1466410668106177464`, `1549062736752599468` opened as real listing pages.

Do not infer validity from seeing `/rooms/<id>` alone. Always open or HTTP-test the final link.

## Verification Snippet

```python
import requests, re
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
}
r = requests.get(url, headers=headers, timeout=12, allow_redirects=True)
# Airbnb sometimes serves 404 via redirect, not HTTP 404
title = re.search(r'<title[^>]*>(.*?)</title>', r.text, re.S|re.I)
is_404 = (r.status_code == 404) \
    or ("404 page not found" in (title.group(1) if title else '').lower()) \
    or ("can't seem to find the page" in r.text.lower()) \
    or ("error code: 404" in r.text.lower())
```

If a page returns HTTP 200 but the title/body says `404 Page Not Found - Airbnb`, treat it as dead.

## When 30-50% links are dead: Replace, Don't Label

Session experience: 26/51 links were dead (long room IDs from earlier scrape). Rather than marking them all dead:
1. Do a **fresh live search** via browser (same check-in/out dates, target areas)
2. Scroll-extract 40-60 new cards from DOM using `a[href*="/rooms/"][aria-labelledby]`
3. Resolve listing names via `document.getElementById(ariaLabelledBy.split(' ')[0]).innerText`
4. Prices come from parent card innerText crawl
5. Batch test all fresh links before building the new HTML section
6. Replace the entire old Airbnb section in HTML (vs patching individual rows)
7. Add a prominent green banner: "X Airbnb BARU — SEMUA LINK VERIFIED LIVE"

This avoids fragmenting the table with half-dead half-live rows.

## DOM Extraction Note

Airbnb search cards don't put listing names inside the anchor's text. The anchor has `aria-labelledby="title_<rid>"`. To get the name:
```js
const titleId = a.getAttribute('aria-labelledby').split(' ')[0];
const name = document.getElementById(titleId).innerText;
```
For price/rating, walk up 6-8 parents and track the longest innerText snippet.

## Location Audit Pitfall

Airbnb search labels are broad. A result found under `Nusa Dua` or `Jimbaran` can actually be:

- Banjar Mumbul / inland South Kuta
- Ungasan / GWK hill area
- Uluwatu / Pecatu / Balangan / Dreamland surf-cliff area

For beach-family travel, classify conservatively:

- `Sanur`: generally safe area, still check walkability.
- `Tanjung Benoa`: beach-oriented but some listings can be inland; check map.
- `Ungasan`, `Uluwatu`, `Pecatu`, `GWK`, `Balangan`, `Dreamland`, `Banjar Mumbul`: mark as far/not quiet-beach priority unless user explicitly wants villa/cliff/surf.

## UI Lesson

When patching a published HTML page used by the owner in browser:

- Add a very visible version/update banner if the user says “where is it?”
- Provide a cache-busted link: `?v=<short-version>`
- If the user reports link failures, mark the row in-place with a visible `❌ LINK MATI / 404` badge rather than just explaining in chat.
- BUT if >50% links are dead, replace the entire section with fresh data rather than patching individual rows.

