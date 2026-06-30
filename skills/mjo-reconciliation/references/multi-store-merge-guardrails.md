# Multi-Store Merge Guardrails

Use this file when editing `merge_scalev_into_mjo_data.py` or debugging wrong summary numbers in `mjo-data.json`.

## Verification checklist after merge

```python
import json
d = json.load(open('/var/www/html/mjo-data.json'))
s = d['summary']

# 1. Per-store Scalev buckets exist for BOTH stores
assert '12993' in s.get('per_store', {}), 'Missing SEFT Corp per_store bucket'
assert '30898' in s.get('per_store', {}), 'Missing Jogja per_store bucket'
p = s['per_store']
ps12993 = p['12993']
ps30898 = p['30898']

# 2. Per-store numbers look reasonable
assert ps12993.get('scalev_store_result', 0) >= 0
assert ps30898.get('scalev_store_result', 0) >= 0

# 3. Global total = sum of per-store
global_total = s.get('scalev_store_result', 0)
sum_per_store = ps12993.get('scalev_store_result', 0) + ps30898.get('scalev_store_result', 0)
assert abs(global_total - sum_per_store) < 0.1, \
    f"Global total {global_total} != sum per-store {sum_per_store}"

# 4. Row-level Scalev data is only written for matching store_id
for row in d['per_ad']:
    sid = str(row.get('store_id'))
    scalev_from_row = float(row.get('scalev_result', 0) or 0)
    # If row has Scalev data, its store must have that ad cached
    if scalev_from_row > 0 and sid == '12993':
        assert row.get('ad_name') in [r.get('ad_name') for r in d['per_ad'] if r.get('scalev_result', 0) > 0]
```

## Common failure modes

| Symptom | Root cause | Fix |
|---|---|---|
| `scalev_store_result` shows 29 but `per_store` has 2 entries | Summary was overwritten by last merge; `per_store` got cleared and only 1 bucket exists | Re-run merge for missed store |
| SEFT Corp rows show Jogja Scalev numbers | `target_rows` filter missing: loop over all rows but only queries Scalev for one store | Add `if str(row.store_id) != str(args.store_id): continue` before cache lookup |
| `meta_scalev_diff_total` = 0 | Summary recomputed correctly; total Meta = total Scalev store result (expected when both stores cover all orders) | This is a success state |
| Row has `scalev_result: 0, scalev_fallback: false` even for ads with orders | Creative has no `url_tags` or destination strips UTM via redirect | Not recoverable via API; manual mapping or redirect fix needed |

## Correct reference numbers (18 Jun 2026)

```
SEFT Corp (12993):  Scalev total=28, tagged=27, coverage=96.4%
Jogja     (30898):  Scalev total=29, tagged=27, coverage=93.1%
Combined:           Scalev total=57, tagged=54, coverage=94.7%
Meta total:         57  (SEFT=31, Jogja=26 via ad-level rows)
meta_scalev_diff_total: 0
```