# Per-content JSON-first dashboard workflow

Use this when the owner asks for an MJO dashboard that is actionable per content/ad, especially with CPR, IC, Result, ATC Rate, and Add-to-Cart Cost.

## Owner preference captured
- Avoid overly general dashboard links/pages. Use a short stable link such as `/mjo/` that redirects to the canonical dashboard HTML.
- Before overwriting the dashboard HTML, offer or use a JSON dump first when the owner wants verification (`opsi 3`).
- Dashboard must be per-content/ad creative, not only daily/account aggregate.
- **CRITICAL — Scalev per-content data must be the primary result metric, not Meta claims.** The dashboard is useless without Scalev riil numbers. See §5b and §9b of the parent SKILL.md.

## Source data
Use Meta Ads `get_insights` at `level="ad"` for both SEFT Corp accounts:
- `act_1025434792768020` (MJO DC-4592)
- `act_1101865787490596` (KANTOR MJO-1054)

Use MTD period by default: first day of current month through today in Asia/Jakarta. For manual backfills, use explicit since/until.

## JSON dump shape
Write processed output to `/var/www/html/mjo-data.json` before rendering HTML when verification is requested.

### Summary block — enriched with Scalev
```json
{
  "summary": {
    "period": {
      "since": "YYYY-MM-DD",
      "until": "YYYY-MM-DD",
      "short": "01–19 Jun 2026",
      "timezone": "Asia/Jakarta"
    },
    "generated_at": "2026-06-19 12:34:56",
    "row_count": 62,
    "total_spend": 65290593,
    "total_result_purchase": 549,
    "scalev_store_result": 496,
    "scalev_store_revenue": 56619219,
    "scalev_tagged_result": 205,
    "scalev_tagged_revenue": 0,
    "scalev_untagged_result": 291,
    "scalev_coverage": 0.41,
    "avg_cpr": 118926,
    "total_ic": 4870,
    "total_atc": 14010,
    "avg_add_to_cart_cost": 4660,
    "decision_counts": {"SCALE":15, "KILL":0, "CEK":47}
  },
  "per_ad": [
    {
      "account_name":"MJO DC-4592",
      "ad_id":"...",
      "ad_name":"...",
      "spend": 13169031,
      "impressions": 163951,
      "clicks": 5881,
      "link_clicks": 3475,
      "ctr": 3.58,
      "cpm": 80322,
      "result_purchase": 108,
      "cpr": 121935,
      "ic": 760,
      "cost_per_ic": 17328,
      "atc": 2646,
      "add_to_cart_cost": 4977,
      "atc_rate_basis":"link_clicks",
      "atc_rate": 0.761,
      "view_content": 21350,
      "revenue_meta": 87192647,
      "roas_meta": 6.62,
      "scalev_result": 74,
      "scalev_revenue": 8950000,
      "scalev_cpr": 121696,
      "meta_scalev_diff": 9,
      "meta_scalev_match_rate": 0.89,
      "decision":"SCALE",
      "decision_reason":"Scalev riil cukup dan CPR riil masih masuk."
    }
  ]
}
```

### Required Scalev fields (per ad)
When Scalev per-content data has been merged, EVERY per_ad entry MUST include:
- `scalev_result` (number) — completed orders matched by `utm_content == ad_name`
- `scalev_revenue` (number) — gross revenue for those orders
- `scalev_cpr` (number|null) — `spend / scalev_result` or null if no result
- `meta_scalev_diff` (number) — `result_purchase - scalev_result` (positive = Meta overclaims)
- `meta_scalev_match_rate` (number|null) — `scalev_result / result_purchase` or null if Meta=0

### Scalev enrichment workflow
1. Run `generate_content_report.py 12993 <since> <until>` (or a custom merge script, see `/tmp/merge_scalev_mjo.py` pattern).
2. The script calls Scalev API once per unique `ad_name` with `utm_content=ad_name`.
3. Store results in a dict keyed by `ad_name`: `{scalev_result, scalev_revenue}`.
4. Merge into `mjo-data.json` per_ad entries by matching `ad_name`.
5. Calculate derived fields: `meta_scalev_diff`, `meta_scalev_match_rate`, `scalev_cpr`.
6. Reclassify decisions per §5b rules using Scalev data as primary signal.
7. Also get total store stats (no utm filter) and write to summary.
8. Write enriched JSON back to `/var/www/html/mjo-data.json`.

Known limitations:
- Coverage is never 100% because order repeat/CS/direct entry bypasses utm tags.
- Coverage `scalev_tagged_result / scalev_store_result` typically 30–50%.
- Always show the coverage warning in the dashboard when below 70%.
- For Jogja/DC-4593/DC-4594, do not overpromise server-side coverage fixes when Meta creatives lack `url_tags`/`utm_content`. If MUH FARID (HNP), Budinda, or similar creatives have no `utm_content`, the durable fix is updating Meta creative `url_tags`/tracking in Ads Manager or via a new creative. Offline fallback mapping can label/attribute known rows for reporting, but it cannot create missing Scalev order tags retroactively.

## Action parsing rules
From each `actions[]` row:
- Result/Purchase: prefer exact `omni_purchase`; fallback to purchase-ish action types only if `omni_purchase` absent. Avoid double-counting `omni_purchase` plus `web_in_store_purchase`.
- IC: `initiate_checkout` and/or `omni_initiated_checkout`.
- ATC: `add_to_cart` and/or `omni_add_to_cart`.
- Link clicks: `link_click`; fallback denominator to row `clicks`.
- View content: `view_content` and/or `omni_view_content`.

From `action_values[]`:
- Revenue: prefer purchase/omni_purchase action values, but label clearly as Meta-claim revenue, not Scalev-real revenue.

## Derived metrics
- `CPR = spend / result_purchase` (null if no result).
- `Cost per IC = spend / IC` (null if no IC).
- `Add-to-Cart Cost = spend / ATC` (null if no ATC).
- `ATC Rate = ATC / link_clicks` when link clicks exists, else `ATC / clicks`.
- Always show the ATC Rate basis in the dashboard so the analyst knows whether it used link clicks or total clicks.

## Decision rules (simple default)
- `SCALE`: result >= 3 AND CPR <= 130000 AND funnel exists (ATC Rate healthy, or IC strong, or ATC strong).
- `KILL`: spend >= 100000 AND result = 0 AND ATC/IC weak; OR result >= 2 AND CPR > 180000.
- `CEK`: not enough volume, spend too low, or funnel mismatch (ATC high but purchase low, IC high but purchase low, CTR low but funnel good, etc.).

Sort output: SCALE first, then KILL, then CEK; inside groups sort by spend or result descending.

## HTML rendering requirements
When owner approves HTML overwrite:
- Write canonical HTML to `/var/www/html/mjo-dashboard.html`.
- Keep short stable redirect at `/var/www/html/mjo/index.html` → `/mjo-dashboard.html`.
- Title: `MJO SEFT Corp — Dashboard Per Konten`.
- Must include Last Updated timestamp WIB.
- Table columns: Konten/Ad Name, Account, Spend, Result, CPR, IC, Cost per IC, ATC, Add-to-Cart Cost, ATC Rate, CTR, CPM, Clicks/Link Clicks, ROAS/Revenue if available, Decision, Reason.
- Keep token/API keys out of HTML.
- If ad-level data is empty/error, render an honest error panel with timestamp rather than a fake success dashboard.
