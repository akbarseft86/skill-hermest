# Travel Listing Location Audits

Use this reference when building or updating public HTML dashboards that compare hotels, Airbnb, villas, or other lodging listings where distance-to-beach/attraction matters.

## Durable lesson

Do **not** trust the search area or listing bucket as the location truth. Airbnb/OTA search results for `Nusa Dua`, `Jimbaran`, or similar can include inland/adjacent zones such as South Kuta, Banjar Mumbul, Ungasan, Uluwatu, Pecatu, GWK, Balangan, or Dreamland. These may be attractive villas but are not equivalent to beachfront or calm-swim beach access.

## Required dashboard pattern

When the user's decision depends on proximity:

1. Add an explicit column such as `Jarak Pantai`, `Jarak Venue`, or `Location Risk`.
2. Use conservative labels:
   - `DEKAT / KANDIDAT` — title/map/source indicates near beach/venue, still verify final map.
   - `AMAN AREA, CEK JARAK` — area is generally appropriate (e.g. Sanur for calm beach) but walkability is unverified.
   - `PERLU CEK MAP` — search bucket is plausible but location precision is unknown.
   - `JAUH DARI PANTAI` or `BUKAN PANTAI TENANG` — inland/surf/cliff/adjacent-area signals.
3. Keep the original source note in a separate column so the user can see both the raw reason and the derived risk label.
4. Add summary counts above the table (e.g. near / safe area / check map / far) so the user can shortlist quickly.
5. If a user provides a screenshot/map correction, update that row explicitly and cite the evidence in-row (e.g. `From Airbnb map: Banjar Mumbul/inland, not Nusa Dua beachfront`).

## Conservative Bali heuristics from the session

For Bali calm-beach family lodging audits:

- `Sanur` is generally safer as an area, but still mark `cek walkable` unless exact distance is verified.
- `Tanjung Benoa` can be appropriate for calm water, but listings may still be inland/gang-side; mark `PERLU CEK MAP` unless waterfront/private beach/oceanfront is supported.
- `Nusa Dua` search results can include Sawangan, Banjar Mumbul, Ungasan, and other inland/adjacent zones. Treat as `PERLU CEK MAP` unless beachfront/near-beach is supported.
- `Ungasan`, `Uluwatu`, `Pecatu`, `GWK`, `Balangan`, and `Dreamland` should usually be flagged as `JAUH / BUKAN PANTAI TENANG` for a calm-swimming beach brief: cliff/surf/inland access, requires transport.
- If Airbnb/OTA automated pages block or return dynamic errors, do not claim exact coordinates. Say verification was limited and classify conservatively from available title/area/map screenshot/source text.

## Final response style for corrections

When the user points out a wrong listing location, acknowledge directly and fix the exact row first. Report the updated public link and the changed classification. Keep caveats short and avoid turning the reply into a long generic methodology unless asked.
