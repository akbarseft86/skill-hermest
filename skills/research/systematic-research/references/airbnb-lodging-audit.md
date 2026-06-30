# Airbnb / Lodging Audit HTML Notes

Use when a user asks for many accommodation options from Airbnb/OTA/direct websites and wants a manual-check HTML dashboard.

## Durable workflow
1. Treat scraped Airbnb/OTA results as **candidates**, not final recommendations. Prices, availability, map pins, fees, and taxes can change or be hidden until click-through.
2. Prefer a dashboard/table with: area, listing name, visible price, rough IDR conversion, rating/review count, beach/location note, and direct link.
3. Label unverifiable facts explicitly: `CEK ULANG harga`, `CEK ULANG jarak`, `cek map`, `cek total final`.
4. For beach-trip lodging, separate areas by suitability:
   - Sanur: usually primary for calmer swimming-friendly beach.
   - Jimbaran/Nusa Dua/Tanjung Benoa: potentially good, but verify exact beach access.
   - South Kuta/Ungasan/Uluwatu/Pecatu/Balangan: often surf/cliff/transport-dependent; keep as cadangan unless user wants that vibe.
5. Do not delete earlier candidates when adding new sources. Append a new section/tab and preserve provenance.
6. If the user is overwhelmed by many listings, add a quick-jump anchor/filter and concise warnings above the table.

## Practical extraction pattern
- Airbnb search pages often expose visible cards via browser DOM. Use page scrolling, then extract card text containing price/rating plus the nearest `/rooms/` link.
- Some server HTML contains structured search result JSON with `structuredDisplayPrice`, `avgRatingLocalized`, badges, and listing IDs. Parse this as a candidate source, but verify suspicious area leakage in the browser.
- Airbnb search can broaden results outside the typed neighborhood; mark those rows clearly as `South Kuta/Ungasan/Uluwatu` or `cek lokasi`, not as the requested beach area.

## Reporting pattern
- Say exactly what changed: previous total + added source count + final row count.
- Mention the public HTML URL/anchor.
- Include verification evidence: row count in file and expected auth/HTTP status if relevant.
- Keep caveat short: “harga Airbnb/availability wajib cek ulang di link.”
