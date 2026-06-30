# Text Document → Public HTML Notes

Use when a user sends a long plain-text document and asks to “jadikan HTML”, “bikin HTML”, or similar.

## Parsing long one-line documents
- Many pasted/attached reports arrive as a single long line with table boundaries collapsed.
- Do not assume every `1. ` / `2. ` occurrence is a table/listing row; prose can contain phrases like “1 atau 2 kamar” that create false positives.
- For numbered datasets with an expected count (e.g. 1–50), prefer sequential parsing: find item `1.`, then the next item `2.`, then `3.` through N in order. Verify final count equals expected before publishing.
- If table columns are collapsed, preserve source honesty by creating cards from safe fields (number, name, type, price, confidence/status/source where detectable) and put the original row chunk behind `<details>` as “catatan mentah”.

## Publishing/verification gotcha
- Some `/var/www/html/<slug>/` paths may be protected by global Basic Auth even when other public share paths are open.
- Always verify the exact public URL, not just that the file exists.
- If the intended fresh slug returns `401`, do not edit nginx or restart services just to finish a quick HTML conversion. Prefer publishing under an already-public share prefix when available, then verify HTTP 200 there.
- Report the verified URL first; mention verification briefly.
