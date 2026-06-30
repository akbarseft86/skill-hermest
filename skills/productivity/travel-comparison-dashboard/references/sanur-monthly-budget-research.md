# Sanur Monthly Stay Budget Research Notes

Session-derived notes for long-stay accommodation dashboards around Sanur/Denpasar Selatan.

## When budget cap changes
- If the user says “mentok harga X juta”, immediately rerun/reshape the dashboard around that cap rather than continuing the old cap.
- For Airbnb Singapore-domain searches, a practical conversion used in this session was `1 SGD ≈ Rp11.500`.
- Rp15jt/month roughly maps to `price_max=1305` SGD on Airbnb search.

## Airbnb URL pattern used
Example search URL for monthly Sanur stay:

```text
https://www.airbnb.com.sg/s/Sanur--Bali--Indonesia/homes?adults=2&checkin=2026-07-01&checkout=2026-07-31&price_max=1305&query=Sanur%2C%20Bali%2C%20Indonesia&search_mode=regular_search
```

If Sanur core is sparse, try Denpasar Selatan as a second Airbnb query, but label area expansion conservatively.

## Status taxonomy for mixed certainty
Use clear row statuses and summary metrics:

- `PRICE-LIVE`: monthly price is visible in source UI and within cap.
- `LEAD-CHECK`: live target/direct/OTA candidate, but monthly price is not confirmed online; user must contact/nego.
- `FAR-FALLBACK`: optional label/badge when the result is budget-valid but geographically outside the requested core area.

Do not advertise “50 verified under budget” if only a subset has visible monthly price. Say e.g. “50 candidates: 27 price-live + 23 lead-check”.

## Location labelling
For Sanur-specific dashboards:
- 🟢 near beach / Sanur Harbour / Mertasari / explicit walking distance.
- 🔵 Sanur or Denpasar Selatan area, reasonable but map still worth checking.
- 🟡 likely inland / needs map confirmation.
- 🔴 Denpasar Barat, Kerobokan, Kuta, Kuta Utara, or other areas far from Sanur — only fallback.

## Presentation
- Put the public HTML under `/var/www/html/audit-hotel-bali-ai-comparison/<slug>/` to reuse the public-whitelisted path.
- Add `?v=` cachebuster in the final link.
- The dashboard top cards should expose count by certainty/status, price range, and any honest limitation.
