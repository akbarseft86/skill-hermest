#!/usr/bin/env python3
"""
Merge Scalev per-content results into an existing MJO Meta per-ad JSON dump.

Usage:
  python3 ~/.hermes/skills/mjo-reconciliation/scripts/merge_scalev_into_mjo_data.py \
    --store-id 12993 \
    --input /var/www/html/mjo-data.json \
    --output /var/www/html/mjo-data.json

Requirements:
- /root/.hermes/config.yaml contains mcp_servers.scalev.headers.Authorization
- JSON input has summary.period.since/until and per_ad[].ad_name/spend/result_purchase
- Scalev join key is utm_content == ad_name
"""
import argparse, datetime, json, urllib.parse, urllib.request, yaml

BUID = "CAO0DOK1OPKQ5ZD3"

MONTHS_ID = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

def short_date(since, until):
    s = datetime.date.fromisoformat(since)
    u = datetime.date.fromisoformat(until)
    if s.year == u.year and s.month == u.month:
        return f"{s.day:02d}–{u.day:02d} {MONTHS_ID[s.month-1]} {s.year}"
    return f"{s.day:02d} {MONTHS_ID[s.month-1]} {s.year} – {u.day:02d} {MONTHS_ID[u.month-1]} {u.year}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store-id", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--business-unique-id", default=BUID)
    args = ap.parse_args()

    data = json.load(open(args.input))
    period = data["summary"]["period"]
    since, until = period["since"], period["until"]
    period["short"] = period.get("short") or short_date(since, until)

    auth = yaml.safe_load(open("/root/.hermes/config.yaml"))["mcp_servers"]["scalev"]["headers"]["Authorization"]
    headers = {"Authorization": auth, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    def gget(url, timeout=60):
        return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout))

    def scalev(utm=None):
        params = {
            "b_uid": args.business_unique_id,
            "store_id": args.store_id,
            "breakdown_date": "day",
            "datetime_type": "paid_time",
            "status": "completed",
        }
        if utm:
            params["utm_content"] = utm
        url = "https://api.scalev.com/v3/orders/statistics?" + urllib.parse.urlencode(params)
        res = gget(url, 45).get("results") or []
        count = sum(float(r.get("count") or 0) for r in res if since <= r.get("day", "") <= until)
        revenue = sum(float(r.get("gross_revenue") or 0) for r in res if since <= r.get("day", "") <= until)
        return count, revenue

    target_rows = [row for row in data.get("per_ad", []) if str(row.get("store_id")) == str(args.store_id)]
    if not target_rows:
        raise SystemExit(f"No rows found for store_id={args.store_id}")

    cache_name = {}
    cache_id = {}
    rows_need_id_fallback = []
    for row in target_rows:
        name = row.get("ad_name") or ""
        if name and name not in cache_name:
            cache_name[name] = scalev(name)
        # Track rows for ad_id fallback (after we know name-matches)
        if name:
            rows_need_id_fallback.append(row)

    store_count, store_revenue = scalev()

    # ad_id fallback: for Jogja ads where ad_name doesn't match UTM content
    # but utm_content might be set to {{ad.id}} (numeric)
    for row in rows_need_id_fallback:
        name_count, _ = cache_name.get(row.get("ad_name") or "", (0, 0))
        meta_result = float(row.get("result_purchase") or 0)
        if name_count == 0 and meta_result > 0:
            aid = str(row.get("ad_id") or "")
            if aid and aid not in cache_id:
                cache_id[aid] = scalev(aid)

    # Summary coverage: only count rows belonging to this store
    tagged_count = 0.0
    tagged_revenue = 0.0
    for row in data.get("per_ad", []):
        if str(row.get("store_id")) != str(args.store_id):
            continue
        name_count, name_revenue = cache_name.get(row.get("ad_name") or "", (0, 0))
        if name_count:
            tagged_count += name_count
            tagged_revenue += name_revenue
            continue
        aid_count, aid_revenue = cache_id.get(str(row.get("ad_id") or ""), (0, 0))
        tagged_count += aid_count
        tagged_revenue += aid_revenue

    for row in data.get("per_ad", []):
        if str(row.get("store_id")) != str(args.store_id):
            continue
        scalev_result, scalev_revenue = cache_name.get(
            row.get("ad_name") or "", (0, 0)
        )
        scalev_fallback = False
        # If name match is 0 but ad_id match > 0, use ad_id as fallback
        if scalev_result == 0:
            aid_match = cache_id.get(str(row.get("ad_id") or ""), (0, 0))
            if aid_match[0] > 0:
                scalev_result, scalev_revenue = aid_match
                scalev_fallback = True

        meta_result = float(row.get("result_purchase") or 0)
        spend = float(row.get("spend") or 0)
        row["scalev_result"] = scalev_result
        row["scalev_revenue"] = scalev_revenue
        row["scalev_fallback"] = scalev_fallback
        row["scalev_cpr"] = (spend / scalev_result) if scalev_result else None
        row["meta_scalev_diff"] = meta_result - scalev_result
        row["meta_scalev_match_rate"] = (scalev_result / meta_result) if meta_result else None

    # Allocate untagged Scalev store orders to Meta-positive rows that still have Scalev=0.
    # This fixes account-filter summaries where store-level total is right, but 1-2 orders
    # lost their utm_content and therefore don't attach to the specific ad rows.
    current_tagged = sum(float(r.get("scalev_result") or 0) for r in target_rows)
    remaining_untagged = max(0.0, store_count - current_tagged)
    if remaining_untagged > 0:
        candidates = [
            r for r in target_rows
            if float(r.get("result_purchase") or 0) > 0 and float(r.get("scalev_result") or 0) == 0
        ]
        # Prefer low-volume Meta rows first; they usually represent the exact missing untagged orders.
        candidates.sort(key=lambda r: float(r.get("result_purchase") or 0))
        avg_order_value = (store_revenue / store_count) if store_count else 0
        for r in candidates:
            if remaining_untagged <= 0:
                break
            alloc = min(float(r.get("result_purchase") or 0), remaining_untagged)
            if alloc <= 0:
                continue
            spend = float(r.get("spend") or 0)
            r["scalev_result"] = alloc
            r["scalev_revenue"] = alloc * avg_order_value
            r["scalev_fallback"] = "allocated_untagged"
            r["scalev_cpr"] = (spend / alloc) if alloc else None
            r["meta_scalev_diff"] = float(r.get("result_purchase") or 0) - alloc
            r["meta_scalev_match_rate"] = alloc / float(r.get("result_purchase") or 0)
            r["decision"] = "CEK"
            r["decision_reason"] = "Dialokasikan dari order Scalev untagged store-level; UTM hilang, jangan auto-kill."
            remaining_untagged -= alloc

    for row in target_rows:
        meta_result = float(row.get("result_purchase") or 0)
        scalev_result = float(row.get("scalev_result") or 0)
        spend = float(row.get("spend") or 0)
        if scalev_result:
            row["scalev_cpr"] = spend / scalev_result
            row["meta_scalev_diff"] = meta_result - scalev_result
            row["meta_scalev_match_rate"] = (scalev_result / meta_result) if meta_result else None

        if meta_result >= 8 and scalev_result == 0:
            row["decision"] = "CEK NAMA"
            row["decision_reason"] = "Meta tinggi tapi Scalev 0: kemungkinan utm_content/nama ad tidak cocok; cek manual sebelum kill."
        elif scalev_result >= 8 and row["scalev_cpr"] is not None and row["scalev_cpr"] <= 180000:
            row["decision"] = "SCALE"
            row["decision_reason"] = "Scalev riil cukup dan CPR riil masih masuk."
        elif meta_result >= 2 and scalev_result / meta_result < 0.4:
            row["decision"] = "KILL"
            row["decision_reason"] = "Scalev riil jauh di bawah klaim Meta."
        elif meta_result == 1 and scalev_result == 0:
            row["decision"] = "CEK"
            row["decision_reason"] = "Meta baru 1 result tapi Scalev 0; data tipis / bisa untagged, jangan auto-kill."
        else:
            row["decision"] = row.get("decision") or "CEK"
            row["decision_reason"] = row.get("decision_reason") or "Perlu cek tag/CPR/funnel sebelum scale."

    summary = data["summary"]

    # Keep per-store Scalev summary instead of overwriting global numbers with the last merge.
    per_store = summary.setdefault("per_store", {})
    store_bucket = per_store.setdefault(str(args.store_id), {})
    store_bucket["scalev_store_result"] = store_count
    store_bucket["scalev_store_revenue"] = store_revenue
    store_bucket["scalev_tagged_result"] = tagged_count
    store_bucket["scalev_tagged_revenue"] = tagged_revenue
    store_bucket["scalev_untagged_result"] = store_count - tagged_count
    store_bucket["scalev_coverage"] = tagged_count / store_count if store_count else None

    # Recompute global Scalev totals from per_store buckets.
    scalev_store_total = sum(float(v.get("scalev_store_result") or 0) for v in per_store.values())
    scalev_revenue_total = sum(float(v.get("scalev_store_revenue") or 0) for v in per_store.values())
    scalev_tagged_total = sum(float(v.get("scalev_tagged_result") or 0) for v in per_store.values())
    scalev_tagged_revenue_total = sum(float(v.get("scalev_tagged_revenue") or 0) for v in per_store.values())
    summary["scalev_store_result"] = scalev_store_total
    summary["scalev_store_revenue"] = scalev_revenue_total
    summary["scalev_tagged_result"] = scalev_tagged_total
    summary["scalev_tagged_revenue"] = scalev_tagged_revenue_total
    summary["scalev_untagged_result"] = scalev_store_total - scalev_tagged_total
    summary["scalev_coverage"] = scalev_tagged_total / scalev_store_total if scalev_store_total else None
    summary["meta_scalev_diff_total"] = float(summary.get("total_result_purchase") or 0) - scalev_store_total
    summary["generated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    json.dump(data, open(args.output, "w"), ensure_ascii=False, indent=2)
    print(f"OK merged Scalev into {args.output}: rows={len(data.get('per_ad', []))}, store={store_count}, tagged={tagged_count}, coverage={summary['scalev_coverage']}")

if __name__ == "__main__":
    main()
