# Hourly Static Dashboard Pattern for MJO Reconciliation

Use when the owner wants an always-available dashboard on `hermest.gerbangduid.my.id` without exposing Meta/Scalev tokens in browser JavaScript.

## Recommended architecture

```
Hermes cronjob every 1h
  -> pull Meta Ads via meta_ads_self tools
  -> pull Scalev via scalev tools
  -> compute reconciliation metrics
  -> generate static HTML + optional JSON snapshot
  -> write to /var/www/html/<dashboard>.html
  -> serve at https://hermest.gerbangduid.my.id/<dashboard>.html
```

This is preferred over frontend API calls because Meta/Scalev credentials stay server-side.

## Dashboard UX shape

Top-down order should be:
1. Header: store, period, last updated timestamp, refresh cadence.
2. KPI cards: Spend Meta, Meta Purchase, Scalev Completed, Match Rate, Revenue Riil, ROAS Riil.
3. Secondary metrics: CPA Riil, Faktor Koreksi, Meta-vs-Scalev selisih, Profit/Loss status.
4. Daily table for current month.
5. Reconciliation summary table: Meta vs Scalev purchase/revenue/ROAS/CPA.
6. Per-account Meta breakdown.
7. Notes: data source, `status=completed`, `datetime_type=paid_time`, provisional warning for recent data.

For per-content reports, keep SCALE/KILL/CEK/CEK NAMA filters separate from the store-level money dashboard. Low UTM coverage (e.g. ~40%) means content rows are directional; store-level Scalev aggregate remains the money truth.

## Cronjob settings

- Use `deliver: local` for hourly dashboards so the origin chat is not spammed every hour.
- Run once immediately after creation to verify the file is produced, then verify with file existence/size and HTML tags.
- Prefer dynamic period: month-to-date (`since = first day of current month`, `until = today WIB`) instead of hardcoding dates. Hardcoded date ranges are acceptable only for one-off backfills.

## Public paths

- Main dashboard example: `/var/www/html/mjo-dashboard.html` -> `https://hermest.gerbangduid.my.id/mjo-dashboard.html`
- Content report example: `/var/www/html/mjo-konten-seft.html` -> `https://hermest.gerbangduid.my.id/mjo-konten-seft.html`

## Implementation note

A cron prompt can generate HTML directly, but for reliability prefer moving repeated logic into a script later. The prompt should explicitly list the two SEFT Corp Meta accounts (`act_1025434792768020`, `act_1101865787490596`) and Scalev store (`12993`) and should request verification after writing.
