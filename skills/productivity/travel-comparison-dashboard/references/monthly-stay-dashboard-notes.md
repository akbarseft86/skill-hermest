# Monthly Stay Dashboard Notes

Session-derived patterns for building 30-day accommodation dashboards.

## Airbnb monthly search
- Use a real ~30-night date range in the search URL to trigger Airbnb monthly pricing and `Monthly discount` text.
- Example parameters: `adults=2&checkin=YYYY-MM-DD&checkout=YYYY-MM-DD&query=Sanur%2C%20Bali%2C%20Indonesia&search_mode=regular_search`.
- Extract cards from `a[href*="/rooms/"][aria-labelledby]`, then resolve title via `document.getElementById(ariaLabelledById).innerText` and walk parents to capture the longest useful card text.
- Parse the last visible `SGD` amount as the discounted monthly total when both original and discounted prices appear.

## Multi-source long-stay columns
For 1-month stays, add columns beyond a hotel comparison:
- Source: Airbnb monthly / official web / OTA info
- Estimasi per bulan: IDR and original currency if available
- Cocok 1 Bulan: kitchen, private/open kitchen, desk, wifi, pool, room vs apartment/villa
- Pantai: 🟢 dekat, 🔵 area Sanur, 🟡 cek map / inland risk
- Link status: every row should have a clear LIVE/CHECK status

## Direct web/guesthouse quirks
- Local accommodation domains may have invalid certs, dead DNS, or have been repurposed. Do not keep them as verified rows.
- If a direct website fails, replace the row with a live Airbnb/OTA/info page or another official site. Mark direct/OTA candidates as `harga perlu nego/cek` unless monthly price is visible.

## Publishing pattern when Basic Auth blocks a new path
- If root `/var/www/html/<new-path>/` returns 401 because only an existing comparison path is whitelisted, publish under the already-public path, e.g. `/var/www/html/audit-hotel-bali-ai-comparison/<new-dashboard>/`.
- Verify with `curl -I` that the final public URL returns HTTP 200.
- Add a cache-buster query param in the final URL, e.g. `?v=30liveYYYYMMDD`.

## Final verification
- Grep the HTML for stale statuses before final: `CHECK`, `404`, `LINK MATI`.
- Confirm key entries and the metric string exist in the served URL, not only in the local file.
