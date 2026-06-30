# MJO Dashboard Audit & Fix Playbook

Use this when the owner says variants of: `audit penuh`, `benerin`, `ini udah bener belum`, `dashboard salah`, or asks to verify the MJO per-content dashboard.

## Operating mode
- Treat `benerin` as permission to audit and fix safe code/config/UI issues in the dashboard/API path. Do not stop at diagnosis.
- Keep the final response short and evidence-based: what was fixed, what was verified, what remains. Avoid long strategic option menus unless a destructive/credential step is required.
- Do not claim completion unless verified from files/endpoints/browser/API output.
- **When user says "debug dengan teliti"/"bertindak sebagai [expert]" → deep debug mode:**
  - Do NOT start by re-reading code or re-writing HTML. Go straight to raw API data sources.
  - Trace data lineage: call Scalev API directly (get_order_statistics, listOrders) and Meta API directly (get_insights) to compare raw numbers.
  - Isolate variables one by one: test `paid_time` vs `created_at`, test per ad_name vs per utm_content, test per store.
  - Report findings as specific numbers with sources, not generic "low coverage" statements.
  - Only after identifying root cause from data, proceed to code/HTML patches.

## Files/endpoints to inspect
- Dashboard HTML: `/var/www/html/mjo-dashboard.html`
- API server: `/opt/mjo-api/mjo_api.py`
- Snapshot JSON: `/var/www/html/mjo-data.json`
- Public dashboard: `https://hermest.gerbangduid.my.id/mjo-dashboard.html`
- Local API: `http://127.0.0.1:8787/api/mjo-data?since=YYYY-MM-DD&until=YYYY-MM-DD&dt=created_at`
- Health endpoint should exist: `http://127.0.0.1:8787/health`

## Two-dashboard comparison diagnostic (Scalev UI vs MJO Dashboard)

When the owner sends **screenshots** of both the **Scalev Orders page** and the **MJO Dashboard** asking "kok beda?":

1. **Identify the date basis of each screenshot.**
   - Scalev Orders page orders table uses **Created At** by default. The right sidebar filter card says "Created At" at the top. Orders counted as "Completed" in the sidebar use `created_at` basis.
   - MJO Dashboard has a "Mode Result" toggle: **Created** (owner-default for content/omset) or **Paid** (for Meta/money-in reconciliation). Check which is selected in the screenshot.
   - **Action:** Pull Scalev statistics in BOTH modes: `datetime_type=created_at` and `datetime_type=paid_time`, with `status=completed`. Compare totals against both screenshots.

2. **Identify account/store filter state.**
   - Scalev Orders page: check the store selector (top-left, e.g. "SEFT CORP").
   - MJO Dashboard: check which account pills are highlighted blue (`active`). Match against the ACCOUNT_STORE mapping:
     - DC-4592 + MJO-1054 → SEFT Corp (store 12993)
     - DC-4593 + DC-4594 → Jogja (store 30898)
     - All 4 active → Gabungan (both stores)
   - **Action:** Reproduce exact filter: call `get_order_statistics` with the matching `store_id`. Compare the number of konten rows — if the screenshot shows 61 konten ("Hasil dari 61 konten") and only SEFT accounts are active, that's correct (SEFT has 61 ad rows).

3. **Check cache staleness.**
   - The MJO Dashboard shows "diperbarui <timestamp>" — that's when the *current data was generated*, NOT when the screenshot was taken.
   - Static `mjo-data.json` is loaded on page init. If it was last regenerated at a different time than the API cache, the initial page view can show stale data.
   - **Action:** Run `ls -la /var/www/html/mjo-cache/*<since>*<until>*` to find cache files. Compare their modification times with `mjo-data.json` timestamp and the screenshot's "diperbarui" timestamp.
   - If timestamps differ significantly, the cached snapshot is stale — click **Apply** or call the API with `force=1` to refresh.

4. **Compare status filter (Scalev Orders page nuance).**
   - Scalev Orders sidebar shows:
     - "151 order(s)" = orders with ALL statuses (Pending + Confirmed + Shipped + Completed + ...)
     - "86 Completed Orders" = subset with status=Completed
   - MJO Dashboard `scalev_store_result` = **completed only** (`status=completed`).
   - **Action:** If comparing Scalev's "151" against MJO's "80", the mismatch is just the Pending/other statuses. If comparing "86" against "80", it's the `paid_time` vs `created_at` difference (step 1).

5. **Final number cross-check:**
   After isolating variables, confirm with a direct Scalev API call:
   ```bash
   curl -s 'https://api.scalev.com/v3/orders/statistics?b_uid=CAO0DOK1OPKQ5ZD3&store_id=STOREID&breakdown_date=day&datetime_type=MODE&status=completed' \
     -H 'Authorization: Bearer TOKEN' -H 'User-Agent: Mozilla/5.0' | python3 -c "
   import json,sys; d=json.load(sys.stdin)
   rows=[r for r in d.get('results',[]) if 'SINCE' <= r.get('day','') <= 'UNTIL']
   for r in rows: print(r.get('day'), r.get('count'))
   print('TOTAL:', sum(float(r.get('count') or 0) for r in rows))"
   ```
   This is the authoritative number. If MJO dashboard matches this, the dashboard is correct.

## Audit checks
1. Scalev SOP compliance:
   - `status=completed`, never `payment_status=paid`.
   - `store_id` required for store totals.
   - `breakdown_date=day` used; then aggregate selected dates.
   - Do not filter by `utm_id` or `utm_term`.
2. **CRITICAL — date basis alignment check (root cause #1 for screenshot mismatches):**
   - Compare Meta conversion dates vs Scalev `paid_time` vs Scalev `created_at`.
   - **Owner override (22 Jun 2026): dashboard default = `created_at` / “Result Konten”** because the owner primarily evaluates content value/omset. `paid_time` remains available as toggle for Meta reconciliation and money-in checks.
   - Scalev Orders page UI usually filters by **Created At** and may show **ALL statuses** count plus a separate Completed count. MJO dashboard uses `status=completed` only. Therefore a screenshot of Scalev Orders can legitimately differ from MJO default if the status/date basis differs.
   - `paid_time` answers “uang masuk / cocok Meta”; `created_at` answers “order lahir dari konten”. Do not call either wrong until the source basis is identified.
   - **To debug date/status mismatch:**
     a. Pull Scalev `get_order_statistics` for the store with `dt=created_at`, `status=completed`, `breakdown_date=day`.
     b. Pull the same with `dt=paid_time`, `status=completed`.
     c. If comparing against Scalev Orders page, also note the UI’s All Orders count (ALL statuses) vs Completed Orders count; do not compare All Orders to completed-only dashboard.
     d. Compare per-day totals for the exact screenshot range and selected store/accounts.
     e. Then trace specific ad names with low coverage: query per `utm_content` on both `paid_time` and `created_at` to see which day the order falls on.
   - Dashboard should explain the selected basis in business language: “Created untuk nilai konten & omset. Paid untuk banding angka Meta/uang masuk.”
3. **Per-content debug procedure when coverage is low (<70%):**
   - Step 1: Check ad names in Meta (get_insights level=ad) → list all `ad_name` values.
   - Step 2: For each ad_name, query Scalev `get_order_statistics` with `utm_content=ad_name`, `status=completed`, `store_id`, `breakdown_date=day`, `dt=paid_time` and `dt=created_at`.
   - Step 3: If a Scalev order exists but on a different day than Meta → date boundary mismatch (patch: ensure dashboard uses `paid_time`).
   - Step 4: If order exists at store level but UTM doesn't match → UTM tracking issue (permanent low coverage; add to fallback mapping).
   - Step 5: Check the actual order list via `listOrders` with `search=<partial_phrase>` to inspect raw UTM fields if available. **Known limitation:** `listOrders` does NOT return `utm_content`/`utm_*` fields at the top level — only `get_order_statistics` with `utm_content` filter works. So you can't easily "see" the raw UTM value per order through the API. Workaround: check via Scalev dashboard UI or ask business owner for expected tracking values.
   - Step 6: For any ad with Meta claim ≥2 and Scalev tagged = 0 → diagnose as "CEK NAMA" (tag mismatch), NOT auto-kill.
   - Step 7: Check landing page redirect chain — logosvillage.com is Scalev's own storefront domain. URL params appended by Meta may be stripped during Scalev's own redirect. Solution: use destination URL directly to Scalev checkout, or ensure redirect chain preserves query params.
2. Per-content join:
   - Confirm join key behavior per store (`utm_content` can be ad_id numeric or ad name depending store/tracking).
   - If coverage is low, mark estimates; do not overclaim per-content P&L finality.
3. Dashboard fields:
   - Required columns: Meta, Scalev, Selisih, Match%, CPR Meta, CPR Riil, IC, ATC, CTR, CPM, CPC, Vonis.
   - Summary cards recalc with active account filters.
   - CTR from Meta is already percent; do not multiply by 100.
   - `Selisih = Meta - Scalev`; show sign consistently (`+` means Meta over Scalev, negative means Scalev higher).
4. Date/API behavior:
   - Date picker must trigger server-side pull (`/api/mjo-data?...`) rather than client-side filtering only.
   - Include `is_provisional` warning for recent ranges (≤7 days) because conversions can lag.
5. API service:
   - Add/verify `/health` for quick checks.
   - Use tracked background process or systemd for servers; avoid untracked `nohup ... &` in Hermes terminal.
   - If restart is needed, follow the anti-shutdown protocol and explain why.

### "Total store perfect but per-content gap" debug pattern

When the user reports "still has a small gap" but store totals are already matched:

1. **Confirm store total is actually matched** — pull the API summary and check `meta_claim_total` vs `scalev_store_result`. If these differ, fix store-level reconciliation first (scalev SOP, store_id filter, status=completed).

2. **If matched, quantify the gap:**
   ```
   diff = scalev_store_result - scalev_tagged_result  # = 6 in 18 Jun case
   coverage = scalev_tagged_result / scalev_store_result  # = 89.5%
   ```
   A healthy range is ~89–95%. Do not chase 100%.

3. **Date-boundary check — expand ±1 day** — For the four mismatch ads, pull `scalev_stats` on `dt=paid_time` for range `[date-1date, date]`:
   - If total expands and matches or exceeds Meta → the missing orders are on the adjacent day (date boundary shift, not UTM failure).
   - If total still below Meta → those orders are truly untagged (redirect strip, direct traffic, CS bypass).

4. **If truly untagged (3 of 6 in 18 Jun case):** Add to coverage documentation, do not force 100%. Only escalate if coverage drops below ~80%.

**Rules of thumb for healthy systems (18 Jun 2026 baseline):**
- Store total match: 100% (Meta=57, Scalev=57)
- Coverage normal: 89–95%
- Untagged breakdown: ~50% date boundary, ~50% truly untagged

## Verification examples
- Health:
  `curl -sS http://127.0.0.1:8787/health`
- Cached API smoke test:
  `curl -sS 'http://127.0.0.1:8787/api/mjo-data?since=2026-06-18&until=2026-06-18&dt=created_at' | python3 -c 'import sys,json; j=json.load(sys.stdin); s=j["summary"]; print(j.get("ok"), j.get("source"), s.get("row_count"), s.get("scalev_store_result"), s.get("scalev_tagged_result"), s.get("scalev_coverage"))'`

## Final response template
```
Sudah saya audit + betulin.

Fixed:
- ...

Verified:
- /health ok
- API smoke: rows X, Scalev store Y, tagged Z, coverage N%
- Dashboard file updated: /var/www/html/mjo-dashboard.html

Sisa risiko:
- ... (only if any)
```
