#!/usr/bin/env python3
"""
MJO content-level reconciliation report (Meta per-ad x Scalev real per utm_content).
Usage:  python3 generate_content_report.py <store_id> <since YYYY-MM-DD> <until YYYY-MM-DD>
Example: python3 generate_content_report.py 12993 2026-06-01 2026-06-18
Writes HTML to /var/www/html/mjo-konten-<store>.html → https://hermest.gerbangduid.my.id/mjo-konten-<store>.html

Gotchas baked in (jangan diubah tanpa alasan):
- Scalev API di belakang Cloudflare → WAJIB User-Agent browser (tanpa itu 403/1010).
- Period scoping per utm_content WAJIB breakdown_date=day lalu sum tanggal target
  (aggregate + start/end_date TIDAK reliable — terkontaminasi window draft_time).
- Join key = utm_content == NAMA ad di Meta. Banyak order tak ter-tag (rename/repeat/CS) →
  coverage sering <100%. Meta-tinggi & Scalev-0 = "CEK NAMA" (tag mismatch), JANGAN auto-KILL.
"""
import json, sys, urllib.parse, urllib.request, yaml, datetime, html

META_TOKEN = open('/root/.hermes/.meta-ads-token').read().strip()
SK = yaml.safe_load(open('/root/.hermes/config.yaml'))['mcp_servers']['scalev']['headers']['Authorization']
BUID = "CAO0DOK1OPKQ5ZD3"

STORE_ACCOUNTS = {  # §1 pemetaan store -> akun Meta
    "12993": {"label": "SEFT Corp", "accounts": {"1025434792768020": "DC-4592", "1101865787490596": "MJO-1054"}},
    "30898": {"label": "Jogja",     "accounts": {"1217688183027696": "DC-4593", "1584139655637069": "DC-4594"}},
}

STORE = sys.argv[1] if len(sys.argv) > 1 else "12993"
SINCE = sys.argv[2] if len(sys.argv) > 2 else "2026-06-01"
UNTIL = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().isoformat()
CFG = STORE_ACCOUNTS[STORE]; ACCOUNTS = CFG["accounts"]; LABEL = CFG["label"]
UA = {"Authorization": SK, "User-Agent": "Mozilla/5.0", "Accept": "application/json"}

def gget(url, headers=None, timeout=60):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=headers or {}), timeout=timeout))

# 1) Meta per-ad aggregated by ad name
meta = {}
for acc, lbl in ACCOUNTS.items():
    tr = urllib.parse.quote(json.dumps({"since": SINCE, "until": UNTIL}))
    url = (f"https://graph.facebook.com/v21.0/act_{acc}/insights?level=ad"
           f"&fields=ad_name,spend,actions&time_range={tr}&limit=300&access_token={META_TOKEN}")
    for r in gget(url).get("data", []):
        sp = float(r.get("spend", 0))
        if sp <= 0: continue
        pur = next((int(float(a["value"])) for a in r.get("actions", []) if a.get("action_type") == "omni_purchase"), 0)
        m = meta.setdefault(r.get("ad_name", "?"), {"spend": 0.0, "pur": 0, "acc": set()})
        m["spend"] += sp; m["pur"] += pur; m["acc"].add(lbl)

# 2) Scalev real per utm_content (sum daily over period)
def scalev(utm=None):
    p = {"b_uid": BUID, "store_id": STORE, "breakdown_date": "day", "datetime_type": "paid_time", "status": "completed"}
    if utm: p["utm_content"] = utm
    try:
        res = gget(f"https://api.scalev.com/v3/orders/statistics?{urllib.parse.urlencode(p)}", UA, 40).get("results") or []
    except Exception:
        return 0, 0
    c = sum(r["count"] for r in res if SINCE <= r.get("day", "") <= UNTIL)
    rev = sum(r["gross_revenue"] for r in res if SINCE <= r.get("day", "") <= UNTIL)
    return c, rev

rows = []
for name, m in meta.items():
    sc, srev = scalev(name)
    rows.append({"name": name, "acc": ",".join(sorted(m["acc"])), "spend": m["spend"],
                 "pur": m["pur"], "sc": sc, "srev": srev})

def verdict(r):
    if r["pur"] >= 8 and r["sc"] == 0: return ("CEK NAMA", "Meta tinggi, Scalev 0 — utm_content beda dgn nama ad? cek manual")
    if r["pur"] == 0 and r["sc"] == 0: return ("KILL", "Spend tanpa hasil (Meta & Scalev 0)")
    if r["pur"] < 8 and r["sc"] < 8: return ("DATA TIPIS", "Volume kecil — tunda vonis")
    match = (r["sc"] / r["pur"] * 100) if r["pur"] else (999 if r["sc"] else 0)
    if match >= 80: return ("SCALE", f"Match {match:.0f}% — jualan riil terkonfirmasi")
    if match >= 40: return ("CEK", f"Match {match:.0f}% — sebagian view-through/tag bocor")
    return ("KILL", f"Match {match:.0f}% — riil jauh di bawah klaim")

for r in rows:
    r["match"] = (r["sc"] / r["pur"] * 100) if r["pur"] else None
    r["roas"] = (r["srev"] / r["spend"]) if r["spend"] else 0
    r["cpa"] = (r["spend"] / r["sc"]) if r["sc"] else None
    r["verdict"], r["why"] = verdict(r)
rows.sort(key=lambda x: -x["spend"])

T = {k: sum(r[k] for r in rows) for k in ["spend", "pur", "sc", "srev"]}
roas_t = T["srev"] / T["spend"] if T["spend"] else 0
profit = T["srev"] - T["spend"]
BASE_C, BASE_REV = scalev()           # total store tanpa filter utm
COV = (T["sc"] / BASE_C * 100) if BASE_C else 0

def rp(n): return "Rp " + f"{int(round(n)):,}".replace(",", ".")
BADGE = {"SCALE": "#16a34a", "CEK": "#d97706", "KILL": "#dc2626", "DATA TIPIS": "#64748b", "CEK NAMA": "#7c3aed"}
gen = datetime.datetime.now().strftime("%d %b %Y %H:%M")
trs = ""
for r in rows:
    match = f'{r["match"]:.0f}%' if r["match"] is not None else "–"
    cpa = rp(r["cpa"]) if r["cpa"] else "–"
    trs += (f'<tr><td class=n><span class=name>{html.escape(r["name"])}</span><span class=acc>{r["acc"]}</span></td>'
            f'<td class=num>{rp(r["spend"])}</td><td class=num>{r["pur"]}</td><td class=num><b>{r["sc"]}</b></td>'
            f'<td class=num>{match}</td><td class=num>{cpa}</td><td class=num>{r["roas"]:.2f}x</td>'
            f'<td><span class=badge style="background:{BADGE[r["verdict"]]}">{r["verdict"]}</span>'
            f'<div class=why>{html.escape(r["why"])}</div></td></tr>')

doc = f"""<!DOCTYPE html><html lang=id><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>MJO Konten — {LABEL} {SINCE}…{UNTIL}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#0f172a;color:#e2e8f0;font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-size:14px}}
.wrap{{max-width:1100px;margin:0 auto;padding:24px}}h1{{font-size:20px;margin:0 0 4px}}.sub{{color:#94a3b8;font-size:13px;margin-bottom:16px}}
.warn{{background:#422006;border:1px solid #a16207;color:#fde68a;border-radius:10px;padding:12px 14px;margin-bottom:18px;font-size:12.5px;line-height:1.6}}.warn code{{background:#1e293b;padding:1px 5px;border-radius:4px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:22px}}
.card{{background:#1e293b;border-radius:12px;padding:14px 16px}}.card .l{{color:#94a3b8;font-size:12px}}.card .v{{font-size:18px;font-weight:700;margin-top:4px}}
table{{width:100%;border-collapse:collapse;background:#1e293b;border-radius:12px;overflow:hidden}}
th,td{{padding:10px 12px;text-align:left;border-bottom:1px solid #334155}}th{{background:#0b1220;color:#94a3b8;font-size:12px;text-transform:uppercase;letter-spacing:.04em}}
td.num,th.num{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}.name{{display:block;font-weight:600}}.acc{{color:#64748b;font-size:11px}}
.badge{{display:inline-block;color:#fff;font-weight:700;font-size:11px;padding:3px 9px;border-radius:999px}}.why{{color:#94a3b8;font-size:11px;margin-top:3px}}
tr:hover td{{background:#243049}}.legend{{margin-top:16px;color:#94a3b8;font-size:12px;line-height:1.8}}.dot{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}}
.loss{{color:#f87171}}.win{{color:#4ade80}}</style></head><body><div class=wrap>
<h1>📊 MJO Konten — {LABEL}</h1>
<div class=sub>Periode {SINCE} … {UNTIL} (paid_time) · store {STORE} · {' + '.join(ACCOUNTS.values())} · dibuat {gen}<br>
Purchase = <b>RIIL Scalev (completed)</b>, bukan klaim Meta. Match% = Scalev ÷ Meta.</div>
<div class=warn>⚠️ <b>Coverage tag: {T['sc']} dari {BASE_C} order riil ter-tag ke konten ({COV:.0f}%).</b>
Sisanya {BASE_C-T['sc']} order ({100-COV:.0f}%) tanpa <code>utm_content</code> cocok (ad di-rename/repeat/CS/direct).
<b>SCALE</b>=winner terkonfirmasi (percaya). <b>CEK NAMA</b>=Meta tinggi tapi tag 0 → kemungkinan nama ad ≠ utm_content, JANGAN langsung kill. Per-konten = directional, bukan P&L final.</div>
<div class=cards>
<div class=card><div class=l>Total Spend</div><div class=v>{rp(T['spend'])}</div></div>
<div class=card><div class=l>Meta Claim</div><div class=v>{T['pur']}</div></div>
<div class=card><div class=l>Scalev Riil (tagged)</div><div class=v>{T['sc']}</div></div>
<div class=card><div class=l>Order Riil Store</div><div class=v>{BASE_C}</div></div>
<div class=card><div class=l>ROAS Riil Store</div><div class=v>{(BASE_REV/T['spend'] if T['spend'] else 0):.2f}x</div></div>
<div class=card><div class=l>Profit/Rugi Store</div><div class="v {'win' if (BASE_REV-T['spend'])>=0 else 'loss'}">{rp(BASE_REV-T['spend'])}</div></div>
</div>
<table><thead><tr><th>Konten</th><th class=num>Spend</th><th class=num>Meta</th><th class=num>Scalev</th>
<th class=num>Match</th><th class=num>CPA Riil</th><th class=num>ROAS</th><th>Vonis</th></tr></thead><tbody>{trs}</tbody></table>
<div class=legend>
<span class=dot style="background:#16a34a"></span><b>SCALE</b> Match ≥80% — naikkan budget &nbsp;
<span class=dot style="background:#d97706"></span><b>CEK</b> 40–79% — sebagian view-through &nbsp;
<span class=dot style="background:#dc2626"></span><b>KILL</b> &lt;40% / spend tanpa hasil &nbsp;
<span class=dot style="background:#64748b"></span><b>DATA TIPIS</b> volume &lt;8 &nbsp;
<span class=dot style="background:#7c3aed"></span><b>CEK NAMA</b> tag mismatch — cek manual</div></div></body></html>"""

out = f"/var/www/html/mjo-konten-{STORE}.html"
open(out, "w").write(doc)
print(f"OK {LABEL} {SINCE}..{UNTIL} | rows={len(rows)} | tagged {T['sc']}/{BASE_C} ({COV:.0f}%) | spend {rp(T['spend'])} | store rev {rp(BASE_REV)} | profit {rp(BASE_REV-T['spend'])}")
print(f"URL: https://hermest.gerbangduid.my.id/mjo-konten-{STORE}.html")
