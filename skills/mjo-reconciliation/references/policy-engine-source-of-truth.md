# MJO Scalev Allocation Policy Engine — source-of-truth pattern

Use this when fixing recurring MJO dashboard reconciliation bugs where one day's dashboard can be patched manually but the user wants the **source** corrected so future dates/ranges are correct too.

## Principle
Do not hardcode a one-day allocation into `mjo-data.json` or a single cache file. Turn the reconciliation rule into an explicit policy + engine used by every runtime path.

## Target files (current deployment)
- Policy file: `/opt/mjo-api/policy/scalev_allocation.yaml`
- Engine: `/opt/mjo-api/policy_engine.py`
- Live API: `/opt/mjo-api/mjo_api.py`
- Frontend: `/var/www/html/mjo-dashboard.html`
- API cache: `/var/www/html/mjo-cache/<since>_<until>_<dt>.json`
- Static JSON: `/var/www/html/mjo-data.json`

## Correct sequence
1. Reproduce the exact UI state from screenshot: account pill, date range, `dt` basis, force/cache status.
2. Identify whether the mismatch is in:
   - static JSON (`/var/www/html/mjo-data.json`),
   - API cache (`/var/www/html/mjo-cache/...`), or
   - live API enrichment (`/opt/mjo-api/mjo_api.py`).
3. If the issue is a reconciliation rule, create/update the policy file first. The policy should state:
   - store-level Scalev total is the source of truth;
   - per-ad Scalev is matched by UTM/content when present;
   - untagged store orders may be allocated to Meta-positive rows with no Scalev match;
   - allocated rows are `CEK`, never auto-KILL.
4. Implement the rule in `policy_engine.py` (or the equivalent shared engine), not just inline in one script.
5. Make `mjo_api.py` call the policy engine after store-level totals are computed and before summary totals are returned.
6. If a batch merge script exists, make it call the same policy engine or mirror the exact policy. Do not let merge script and API server drift.
7. Patch dashboard calculations to read canonical fields (`per_store[store_id].scalev_store_result` when present) instead of legacy ambiguous fields.
8. Force-refresh the API endpoint and verify the exact UI-filtered totals before claiming fixed.

## Allocation algorithm (`allocated_untagged`)
When `store_total > sum(per-ad scalev_result)`:
1. `remaining = store_total - current_tagged` per store.
2. Candidate rows: same `store_id`, `result_purchase > 0`, and `scalev_result == 0`.
3. Sort candidates by ascending Meta result (`low_meta_first`) so thin Meta rows get covered first.
4. Allocate `min(result_purchase, remaining)` to each candidate.
5. Set:
   - `scalev_fallback = "allocated_untagged"`
   - `scalev_result = allocated`
   - `scalev_revenue = allocated * average_store_order_value`
   - recompute `scalev_cpr`, `meta_scalev_diff`, `meta_scalev_match_rate`
   - `decision = "CEK"`
   - reason: UTM/order was untagged at store level; do not auto-kill.

## Verification commands/patterns
After implementation and force refresh, verify from API response, not just static file:

```bash
curl -s 'http://127.0.0.1:8787/api/mjo-data?since=2026-06-18&until=2026-06-18&dt=paid_time&force=1' -o /tmp/mjo_api_18.json
python3 - <<'PY'
import json
j=json.load(open('/tmp/mjo_api_18.json'))
rows=j['per_ad']
sel=[r for r in rows if r.get('account_id')=='1217688183027696']
print('4593 rows', len(sel), 'meta', sum(float(r.get('result_purchase') or 0) for r in sel), 'scalev', sum(float(r.get('scalev_result') or 0) for r in sel))
for r in sel:
    if float(r.get('result_purchase') or 0)>0 or float(r.get('scalev_result') or 0)>0:
        print(r.get('ad_name'), r.get('result_purchase'), r.get('scalev_result'), r.get('scalev_fallback'))
print('summary store', j['summary']['per_store'].get('30898'))
print('summary global scalev store/tagged', j['summary'].get('scalev_store_result'), j['summary'].get('scalev_tagged_result'))
PY
```

Expected sanity for the Jun 18 DC-4593 case after policy application:
- DC-4593 selected view: `Meta=4`, `Scalev=4`.
- `MUH FARID (HNP)` and `Budinda` may show `scalev_fallback=allocated_untagged`.
- API response source should be `fresh` after `force=1`.

## Runtime/process pitfall
Starting `python3 /opt/mjo-api/mjo_api.py &` while another server is already bound to port 8787 causes:

```text
OSError: [Errno 98] Address already in use
```

This does **not** necessarily mean the API is down. First check:

```bash
ps aux | grep mjo_api | grep -v grep
lsof -i :8787 2>/dev/null || ss -tlnp 'sport = :8787' 2>/dev/null
curl -s http://127.0.0.1:8787/health
```

Because this user's environment has anti-shutdown expectations, do not kill/restart the existing API process without explicit approval. If restart is required to load new code, explain the PID, risk, and ask for approval. Prefer a rolling approach if downtime matters.

## Response style when user is frustrated
If the user says the fix was just “main alokasi” and asks for the source, do not defend the quick patch or write a long conceptual essay. State the source-of-truth files and the exact future-proofing path:
- policy YAML path,
- policy engine path,
- live API path,
- frontend field corrected,
- verification proof from the exact filtered view.

Keep it terse and focused on the artifact that prevents the bug from recurring.
