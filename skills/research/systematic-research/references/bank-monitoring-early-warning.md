# Bank Monitoring Early-Warning Notes

Use this reference when the user does not just want a one-off health check, but an ongoing early-warning radar for an Indonesian bank.

## Durable lessons from Krom monitoring work
- The user may explicitly reject a narrow search limited to only a handful of websites.
- For monitoring tasks, do a broad-source pass first, then rank evidence quality.
- The user's real goal may be **getting warned earlier**, not being told generic conservative advice like "avoid the bank" or "diversify away".
- A useful report can be short if it is structured: 1 page, clear verdict, and obvious escalation signals.

## Search posture
Do **not** frame the search as "4 websites is enough". Instead:
1. Search official bank disclosures and IR PDFs.
2. Search OJK, LPS, BI, IDX disclosures.
3. Search credible business media and mainstream financial press.
4. Search for operational-signal chatter only as weak evidence to be verified.
5. Synthesize across multiple queries; avoid over-weighting any single article.

## Leading vs lagging indicators
### Leading indicators (faster warning)
- App/login/withdrawal access complaints with unusual clustering
- Product/S&K changes that affect withdrawals, rates, or liquidity behavior
- Customer-service complaints suggesting blocked transactions or delayed funds
- News about operational incidents, sanctions, governance issues, fraud, or sudden policy reversals

### Lagging indicators (confirmation, but slower)
- Quarterly CAR/KPMM
- NPL gross/net
- LCR / NSFR / LDR
- Profitability trend
- Annual-report discussion of liquidity/funding mix

## Recommended concise report shape
1. Verdict line: Hijau / Kuning / Merah
2. What changed since last check
3. Leading indicators observed today
4. Official-metric snapshot (only the most relevant numbers)
5. LPS caveat if deposit rate exceeds guarantee cap
6. Bottom line: any evidence of Century-like public signals or not

## Two-layer delivery pattern for recurring monitoring
When the user wants both daily monitoring and a second-opinion workflow:

### Layer 1 — Analyst report
Use the richer report as the canonical source of truth. Include:
- verdict/status
- supporting metrics with concrete numbers
- source-rich evidence
- freshness notes / blind spots
- a Claude-ready block with these sections in order:
  1. `CONTEXT BLOCK`
  2. `RAW DATA SNAPSHOT`
  3. `SINYAL BARU 24 JAM TERAKHIR`
  4. `PATTERN DETECTION`
  5. `PRE-FILLED QUESTIONS UNTUK CLAUDE`
  6. `BLIND SPOT REPORT`

### Layer 2 — Messaging forwarder
For chat delivery, do **not** send the full analyst markdown. Send only one concise summary containing:
- tanggal
- status
- top 3 signals
- 1–2 action lines

Use **summary-content dedupe** (hash the rendered summary) rather than path-based dedupe. This prevents re-sending the same message when the source file name or formatting changes but the substance did not.

### Escalation pattern
A durable architecture for this task class is:
- daily dashboard/report on a fixed schedule
- higher-frequency hard-alert scan for ORANYE/MERAH conditions
- separate forwarder that only sends when alert-needed is true, with dedupe state

This keeps daily monitoring concise while still allowing urgent warnings outside the main report schedule.

## Tone guidance
- Practical, not preachy
- Early-warning oriented, not generic risk-avoidance advice
- Transparent about public-data limits
- Short enough to scan quickly every day
- For chat apps, prefer **1 ringkasan penting** and avoid duplicate sends
