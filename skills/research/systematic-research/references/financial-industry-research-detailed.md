# Domain C: Financial/Industry Deep Research — Detailed Methodology

Absorbed from: `indonesia-banking-risk-research` (archived)

## Trigger Conditions

Use this when the user:
- Asks whether an Indonesian bank is healthy, safe, or showing danger signs
- Asks about deposit safety, LPS coverage, NPL/CAR/LCR/NSFR, or bank failure risk
- Wants a comparison between a current bank and a historical bank failure case
- Asks for wider web research rather than a narrow answer based on few sites

## Core Principles

1. **Search broadly, not narrowly.** Do multiple queries across official disclosures, OJK/LPS/BI sources, exchange filings, credible financial media, and broader web. Do not rely on only a few sites.
2. **Do not cap research to a tiny fixed website set.** A narrow 3–4-site sweep is insufficient for monitoring-oriented risk work.
3. **Lead with the direct answer.** Answer plainly first, then explain the evidence.
4. **Prefer official metrics before commentary.** Priority: official bank IR PDFs > OJK/LPS/BI/IDX > annual reports > credible media > user complaints (weak signals only).
5. **Be transparent about limits.** Don't overclaim that a bank is "safe" in an absolute sense.
6. **Separate bank-health risk from depositor-protection risk.** A healthy bank can still exceed LPS guarantee limits.

## Minimum Research Checklist

For a current bank-health question, gather as many as available:
- Capital: CAR / KPMM / total capital ratio
- Asset quality: NPL gross, NPL net, and trend
- Liquidity: LCR, NSFR, LDR
- Profitability: latest quarterly/annual profit trend
- Funding mix / liquidity strategy
- Regulatory/public stress signals: sanctions, special supervision, bailout support, kliring issues, withdrawal problems
- LPS coverage caveat: compare offered deposit rates with the current LPS guaranteed-rate cap

## Heuristic Interpretation

| Metric | Strong | Okay | Watchlist | Red Flag |
|--------|--------|------|-----------|----------|
| NPL gross | <2% | 2%–3% | 3%–5% | >5% |
| LCR/NSFR | >>100% | ≥100% | Approaching 100% | <100% |
| CAR/KPMM | High & rising | Stable | Deteriorating | Near minimum |

Sharp deterioration over successive quarters matters more than any single number.

## Historical-Failure Comparison Workflow

When comparing a current bank to a historical failure case (e.g., Bank Century):

1. Pull the **historical red flags** from reliable summaries or official references.
2. Convert them into a **checklist**: CAR collapse, severe liquidity stress, payment failure, emergency support, mass confidence shock.
3. Compare each item against the current bank using public data.
4. End with a plain-language verdict: "not showing [case]-like public signals" or "some overlapping warning signs exist."
5. Add depositor-protection caveat separately if rates exceed LPS guarantee limits.

### Century Red-Flag Pattern (from session)
- CAR per 31 Oct 2008: ~ -3.53%
- Serious liquidity stress in late Oct / early Nov 2008
- Kalah kliring in mid-Nov 2008
- BI emergency liquidity support / FPJP: ~Rp689.4 miliar
- Bailout burden: ~Rp6.7 triliun

Working comparison logic: Century = capital breakdown + liquidity failure + payment failure + emergency support. If a current bank lacks those public signals, say "not currently showing a Century-like public pattern."

### Krom Public-Signal Snapshot (from session, Q1 2026)
- NPL gross: ~3.11%
- NPL net: ~0.16%
- KPMM: ~39.78%
- LCR: ~1,078%
- NSFR: ~181%
- Profitability: positive

Interpretation: not a Century-like pattern from public data. Main caveat: LPS coverage risk if deposit rates exceed guaranteed cap.

### Practical Phrasing
- "Dari data publik terbaru, belum terlihat tanda-tanda seperti Century."
- "Sehat ≠ tanpa risiko."
- "Risiko yang lebih relevan untuk nasabah retail di sini adalah bunga di atas batas penjaminan LPS."

## Leading vs Lagging Indicators

### Leading Indicators (faster warning)
- App/login/withdrawal access complaints with unusual clustering
- Product/S&K changes affecting withdrawals, rates, or liquidity behavior
- Customer-service complaints suggesting blocked transactions or delayed funds
- News about operational incidents, sanctions, governance issues, fraud

### Lagging Indicators (confirmation, slower)
- Quarterly CAR/KPMM, NPL, LCR/NSFR, profitability trend
- Annual-report discussion of liquidity/funding mix

## Two-Layer Delivery for Recurring Monitoring

### Layer 1 — Analyst Report
Richer, source-heavy report. Include Claude-ready block with sections:
1. `CONTEXT BLOCK`
2. `RAW DATA SNAPSHOT`
3. `SINYAL BARU 24 JAM TERAKHIR`
4. `PATTERN DETECTION`
5. `PRE-FILLED QUESTIONS UNTUK CLAUDE`
6. `BLIND SPOT REPORT`

### Layer 2 — Messaging Forwarder
For chat delivery (WA/Telegram), send only:
- tanggal
- status
- top 3 signals
- 1–2 action lines

**Do NOT dump the full markdown report into chat.**

Use **summary-content dedupe** (hash the rendered summary, not the file path) to prevent re-sending same substance under different filenames.

### Escalation Pattern
- Daily dashboard/report on fixed schedule
- Higher-frequency hard-alert scan for ORANYE/MERAH conditions
- Separate forwarder that only sends when alert-needed is true, with dedupe state

## Recommended Concise Report Shape
1. Verdict: Hijau / Kuning / Merah
2. What changed since last check
3. Leading indicators observed today
4. Official-metric snapshot (most relevant numbers)
5. LPS caveat if deposit rate exceeds guarantee cap
6. Bottom line: any evidence of Century-like public signals or not

## Output Style
- Use Bahasa Indonesia unless asked otherwise.
- Plain opening verdict, then bullets and checklist.
- For monitoring: concise 1-page early-warning report with Hijau/Kuning/Merah.
- Emphasize leading indicators first (the user wants to avoid being late).
- Avoid false certainty: "dari data publik terbaru", "belum terlihat", "ini bukan jaminan tanpa risiko".
- Narrow follow-ups: answer in 1–3 lines first, then compact explanation.

## Pitfalls
- Don't say safe just because OJK-regulated.
- Don't confuse high interest with higher guaranteed safety.
- Don't treat scattered complaints as proof of collapse; look for systemic signals.
- Don't compare to Century using vibes; anchor in capital, liquidity, payment ability, emergency support.
- Don't over-rely on one publication period. Trend matters.
