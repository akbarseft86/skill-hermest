---
name: mjo-reconciliation
description: >-
  SOP wajib untuk menarik & mencocokkan data iklan Meta Ads MJO dengan penjualan riil
  Scalev (SEFT Corp). Juga mencakup cron-based per-content decision dashboard dengan
  metrik CPR, IC, ATC Rate, Add to Cart Cost. Trigger setiap user minta: "tarik data
  MJO", "cocokin meta ke scalev", "reconcile MJO", "data iklan vs penjualan",
  "performa akun MJO", "cek cuan iklan", "berapa purchase riil", "scale/kill konten",
  "dashboard per konten", "per content MJO", atau membandingkan klaim Meta dengan
  order Scalev. Pakai tool meta_ads_self (get_insights) + scalev (get_order_statistics).
  Tujuan: tarik data TIDAK SALAH dan dashboard per konten siap-analisis.
version: 1.6.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [meta-ads, scalev, mjo, reconciliation, reporting, seft, content-dashboard]
    related_skills: [mjo-data-report]
---

# MJO Reconciliation (Meta Ads ↔ Scalev)

SOP untuk mencocokkan klaim iklan Meta dengan penjualan riil Scalev. Dibuat dari hasil
debug Juni 2026. **Faktor koreksi & angka acuan harus di-recompute tiap bulan.**

## 0. Prinsip inti
1. **Scalev = kebenaran (uang riil). Meta = klaim/sinyal (cenderung melebihkan).**
2. Pembanding benar = level **STORE ↔ pasangan AKUN**, bukan join per-campaign.
3. Patokan status Scalev = **`completed`**, BUKAN `payment_status=paid`.
4. Basis tanggal: Meta mencatat di **hari bayar** (conversion-time) → samakan Scalev pakai
   **`paid_time`**. Untuk samakan dengan list order di UI Scalev pakai `created_at`.
5. Data ≤7 hari terakhir masih **provisional** (konversi nyusul).

## 1. Pemetaan STORE ↔ AKUN META
| Store Scalev | store_id | Akun Meta | ad_account_id |
|---|---|---|---|
| **SEFT Corp** | `12993` | MJO DC-4592 | `act_1025434792768020` |
| | | KANTOR MJO-1054 | `act_1101865787490596` |
| **SEFT Corp - Jogja** | `30898` | MJO DC-4593 | `act_1217688183027696` |
| | | MJO DC-4594 | `act_1584139655637069` |

- Business: **SEFT CORP**, `business_unique_id = CAO0DOK1OPKQ5ZD3`.
- Store lain (Affiliate SEFT, FANPAGE) BUKAN MJO — jangan dicampur.
- Selalu **filter store**, lalu bandingkan ke pasangan akunnya. Jangan campur store/akun beda.

## 2. Tarik data SCALEV (tool: `get_order_statistics` dari server scalev)
Params wajib:
- `business_unique_id`: `CAO0DOK1OPKQ5ZD3`
- `status`: `completed`  ← patokan "result" (BUKAN `payment_status=paid`)
- `datetime_type`: `paid_time` (banding Meta) ATAU `created_at` (banding UI order)
- `breakdown_date`: `day`
- `query`: `{ "store_id": 12993 }` (SEFT Corp) atau `{ "store_id": 30898 }` (Jogja)

JEBAKAN (jangan ulang):
- `payment_status=paid` mengecualikan order "settled" → undercount. Pakai `status=completed`.
- Tanpa `store_id` → kehitung semua store → over. Wajib filter store.
- Filter `start_date`/`end_date` untuk 1 hari TIDAK berfungsi (API window default ±30 hari).
  Solusi: `breakdown_date=day` lalu **ambil baris tanggal yang dicari** dari `results`.
- **JANGAN** hitung total store via join `utm_campaign`/`utm_content` → undercount (order
  repeat/CS/ketik link langsung tak bawa tag). Terbukti: join=228 vs riil=351. Join UTM
  HANYA untuk analisa per-konten (§5).

## 3. Tarik data META (tool: `get_insights` dari server meta_ads_self)

Params:
- `object_id` (atau `account_id`): `act_...` sesuai §1
- `level`: `account` (total akun) / `campaign` / `ad`
- `time_range`: `{ "since":"YYYY-MM-DD", "until":"YYYY-MM-DD" }`
- (opsional) `breakdown`, `action_breakdowns`

Baca dari response:
- `spend`
- `actions[]` → cari `action_type`:
  - `omni_purchase` (preferred), atau `purchase`, `web_in_store_purchase` → **Result**
  - `initiate_checkout`, `omni_initiated_checkout` → **IC**
  - `add_to_cart`, `omni_add_to_cart` → **ATC**
  - `link_click` → denominator ATC rate
  - `view_content`, `omni_view_content` → VC
- `action_values[]` → cari purchase → **Revenue meta-claim** (bukan riil)

⚠️ JEBAKAN FATAL — JANGAN JUMLAHKAN action_type sinonim. Meta mengembalikan konversi yang
SAMA di banyak label (`omni_purchase`, `purchase`, `offsite_conversion.fb_pixel_purchase`,
`web_in_store_purchase`, ... semuanya bernilai SAMA). Kalau dijumlah = TRIPLE/× count
(mis. 539 jadi ~1600). Ambil SATU saja per metrik (prioritas `omni_*`, fallback ke yang
ada). Berlaku juga untuk IC, ATC, dan revenue. (Bug ini pernah terjadi di mjo_api.py.)

Keterbatasan tool:
- `get_insights` TIDAK punya `time_increment` → per-hari perlu loop.
- Atribusi = conversion-time → samakan Scalev pakai `paid_time`.
- List akun: tool `get_ad_accounts`.

## 4. RECONCILIATION level store (keputusan uang)
Per periode (window tertutup, disarankan bulanan):
1. Scalev: `status=completed`, `store_id` sesuai, total periode (§2).
2. Meta: jumlahkan `omni_purchase` **pasangan akun** store itu (§3).
3. `Selisih% = (Meta − Scalev) / Scalev`.

Angka acuan 1–13 Jun 2026 (sanity-check):
| Store | Meta | Scalev (completed) | Selisih |
|---|---|---|---|
| SEFT Corp | 384 (4592=301, 1054=83) | 351 (created) / 345 (paid) | +9% |
| Jogja | 376 (4593=74, 4594=302) | 386 (created) | −3% |
| **Gabungan** | **760** | **737** | **+3%** |

- **Faktor koreksi SEFT Corp: Meta × ~0,91 ≈ riil.** Recompute tiap bulan, per store.
- Selisih wajar = view-through + modeled conversion.

## 5. Analisa per KONTEN (naik/kill)

### 5a. CARA CEPAT (default) — jalankan script
Untuk report level konten + tampilan HTML siap-baca, JALANKAN:
```
python3 ~/.hermes/skills/mjo-reconciliation/generate_content_report.py <store_id> <since> <until>
```
Script otomatis: tarik Meta per-ad → join ke Scalev riil per `utm_content` → klasifikasi
→ tulis HTML ke `/var/www/html/mjo-konten-<store>.html`.

**Gotcha yang sudah di-handle:**
- Scalev API → wajib `User-Agent: Mozilla/5.0` (tanpa itu 403).
- Scoping periode per `utm_content` wajib `breakdown_date=day` lalu SUM tanggal target.
- Join key = `utm_content` ≈ nama ad/ID ad, **tapi cek dulu isi UTM per store**. SEFT Corp sering numeric (`utm_content`=ad_id); Jogja sering nama (`utm_content`=nama iklan) sementara ID numerik ada di `utm_id`/`utm_term` — dan `utm_id`/`utm_term` jangan dipakai sebagai filter karena bisa diabaikan Scalev.
- Coverage sering <100%. Meta-tinggi & Scalev-0 = vonis "CEK NAMA" (tag mismatch), JANGAN auto-KILL.
- URL intermediasi/redirect bisa memotong UTM. Temuan DC-4593 Jogja: creative mengarah ke `logosvillage.com/seft-lp-a`, Meta append UTM di sana, lalu redirect ke Scalev dapat membuat UTM hilang. Prefer destination URL langsung ke landing Scalev atau pastikan redirect preserve query string.
- **Rate-limit (HTTP 429 "Too many requests from CF):** banyak call Scalev beruntun kena
  blok Cloudflare → throttle ~0.35s antar-call + retry backoff. Jangan swallow error jadi 0
  (bikin angka salah diam-diam) — lebih baik gagal jelas lalu retry.
### Basis tanggal (datetime_type): `created_at` = COCOK dengan tampilan list order di UI
  Scalev (untuk spot-check owner). `paid_time` = sejajar Meta (conversion-time). **Default
  dashboard/API untuk banding Meta harus `paid_time`**, dengan opsi `created_at` tetap tersedia
  dan diberi warning UI. Beda angka created vs paid itu WAJAR (order dibuat hari lain,
  dibayar di hari lain), bukan bug.

### Decision framework: kapan pakai yang mana (owner preference, Jun 2026)

Owner confusion is **common** — the same data looks different on the two bases. Use this
simple framework when explaining or when designing dashboard toggles:

| Mode | Nama gampang | Basis | Jawab pertanyaan ini |
|---|---|---|---|
| **📅 Created** | **Order lahir / Nilai konten** | `datetime_type=created_at` | "Konten ini bikin orang *create order* berapa?" |
| **💰 Paid** | **Uang masuk / Cocok Meta** | `datetime_type=paid_time` | "Hari ini uang masuk berapa — cocok nggak sama Meta?" |

**⚠️ OWNER OVERRIDE (22 Jun 2026): default dashboard = `created_at`.** Owner (Akbar) memilih
**Result Konten / Created** sebagai default karena fokus utamanya **nilai konten & omset**, dan
basis Paid bikin dia bingung. `paid_time` TETAP tersedia sebagai toggle untuk banding Meta
(kolom Selisih/Match%). Jadi: jangan paksa balik ke paid_time default — itu keputusan owner.
(Catatan teknis lama: paid_time lebih sejajar Meta & menghindari false mismatch saat reconcile —
ini alasan kenapa toggle Paid tetap penting, bukan alasan menjadikannya default lagi.)

**Toggle ke `created_at`** saat user mengevaluasi konten/creative — karena `created_at` lebih
dekat ke momen iklan bekerja (order lahir karena konten), bukan kapan transfer bank masuk.

**Aturan pegangan sederhana (untuk diucapkan ke owner):**
> *"Created untuk **menilai konten**. Paid untuk **menilai uang masuk dan cocok Meta."*

**Explain lead with result, not funnel metrics:**
Ketika owner bertanya "kok beda?" atau brainstorming basis tanggal — mulai penjelasan dari
**result (purchase)**, bukan IC/ATC. Owner peduli result dulu, baru funnel.
Koreksi langsung dari owner (Jun 2026): *"bukan IC tapi result"*.

**Visual explainer reference:**
File HTML explainer sederhana dengan toggle interaktif:
`/var/www/html/result-created-vs-paid.html`
URL publik: `https://hermest.gerbangduid.my.id/result-created-vs-paid.html`
Ini bisa dishare ke owner kapan pun dia bingung soal beda created vs paid.

### 5b. Window-based operational decision rules (AUTO-LABEL system)

**CRITICAL — owner mandate (Jun 2026):** The dashboard MUST auto-label each ad with a
decision so the owner can execute without re-reading framework every day. The policy engine
at `/opt/mjo-api/policy/scalev_allocation.yaml` applies these rules automatically.
Labels appear in the "Vonis" column and a "Vonis Summary" bar at the top.

**Target CPR (default): Rp180.000 per result.** Adjustable by changing `target_cpr` in
policy engine caller (currently hardcoded in `/opt/mjo-api/mjo_api.py`).

**Implementation files:**
- Policy YAML: `/opt/mjo-api/policy/scalev_allocation.yaml`
- Policy engine: `/opt/mjo-api/policy_engine.py` — `apply_policy(rows, per_store, dt, days=0, target_cpr=180000)`
- API caller: `/opt/mjo-api/mjo_api.py` — computes `window_days` from `since`/`until` range
- Dashboard UI: `/var/www/html/mjo-dashboard.html` — renders Vonis column + Vonis Summary bar

#### Window-based rules

| Window | Label | Condition | Owner action |
|---|---|---|---|
| **1–2 hari** | **◌ OBSERVASI** | Data masih tipis / tidak memenuhi alarm | Pantau, jangan vonis |
| **1–2 hari** | **🔔 ALARM** | `spend >= target_cpr AND scalev == 0` | Waspada, cek besok lagi |
| **3+ hari** | **✕ KILL** | `spend >= 1.5×target_cpr AND scalev == 0` | Turun budget / pause |
| **3+ hari** | **✕ KILL** | `cpr_riil > 1.5×target_cpr` | Turun budget / pause |
| **5+ hari** | **▲ SCALE** | `scalev >= 5 AND cpr_riil <= target_cpr` | Naik budget 20–30% |
| **5+ hari** | **⬆ SCALE BESAR** | `scalev >= 8 AND cpr_riil <= 0.8×target_cpr` | Naik budget 30–50% |
| **Kapan saja** | **⚠ CEK NAMA** | `meta >= 8 AND scalev == 0` | Cek utm_content/nama ad mismatch |
| **Default** | **◌ OBSERVASI** | Tidak ada rule cocok | Pantau sampai window cukup |

Dengan target Rp180.000:
- 1.5× target = Rp270.000 → threshold KILL
- 0.8× target = Rp144.000 → threshold SCALE BESAR
- Spend Rp270.000+ selama 3 hari tanpa result → KILL

#### Monitoring window untuk konten yang sudah jalan

| Window | Fungsi |
|---|---|
| **2 hari rolling** | Alarm cepat — deteksi tanda fatigue. Jangan vonis final. |
| **3 hari rolling** | Keputusan — cukup data buat turun/kill atau lanjut. |
| **5–7 hari** | Evaluasi konten baru — jangan vonis sebelum ini. |

#### Formula pendek untuk owner

> **Target CPR = Rp180.000**
> **2 hari = Alarm** (waspada, jangan kill)
> **3 hari = Kill** (CPR > 1.5× target atau spend tanpa result)
> **5–7 hari = Scale** (CPR stabil di bawah target + result cukup)
>
> **Created = nilai konten. Paid = cocok Meta.**
> **Default dashboard: Created + 3 hari** (owner override 22 Jun 2026; Paid jadi toggle buat banding Meta).

#### Special cases
- **Allocated untagged rows** → always labeled **CEK** (never auto-KILL allocated rows
  because UTM may have been lost in redirect).
- **Duplicate ad names** → proportional allocation across duplicate rows, NOT full Scalev
  count on each row, and label as **CEK** with `duplicate_ad_name_allocated` note.

### 5c. Cara manual — per-content decision rules (LEGACY, use auto-label §5b instead)

For reference only. The auto-label system in §5b replaces this manual process.

**Scalev-based rules (pre-Juni 2026):**
| Condition | Decision |
|---|---|
| Meta result ≥ 8 AND Scalev result = 0 | **CEK NAMA** — likely `utm_content` / ad name mismatch; do not auto-kill |
| Scalev result ≥ 8 AND CPR Riil within target threshold | **SCALE** |
| Meta result ≥ 2 AND Scalev/Meta match < 40% | **KILL** unless tag mismatch suspected |
| Meta result = 1 AND Scalev result = 0 | **CEK / DATA TIPIS** — do not auto-kill single Meta purchase claims; may be attribution lag or untagged order |
| Meta and Scalev both low volume | **CEK / DATA TIPIS** |
| Otherwise | **CEK** |

**Meta-only fallback:**
| Condition | Decision |
|---|---|
| Result ≥ 3 AND CPR ≤ 130000 AND funnel sehat (ATC Rate ≥ 3% atau IC ≥ Result×1.2 atau ATC ≥ Result×1.5) | **SCALE** |
| Spend ≥ 100000 AND Result = 0 AND ATC/IC weak | **KILL** |
| Result ≥ 2 AND CPR > 180000 | **KILL** |
| Lainnya | **CEK** |

### 5d. Per-content Scalev join — allocation of untagged orders

## 6. Confidence per keputusan
| Keputusan | Sumber | Confidence |
|---|---|---|
| Total cuan / scaling budget akun | Scalev agregat (store) | Tinggi (~85%) |
| Kill konten phantom | Meta vs Scalev riil | Tinggi |
| Scale konten | Scalev riil + tren akun | Sedang–tinggi |
| ROAS/CPA absolut per konten dari Meta mentah | Meta saja | Rendah |
| **Per-content decision** (via JSON-first flow §9b) | Meta ad-level + derived metrics | Sedang |

## 7. CHECKLIST anti-salah (tiap pull)
- [ ] Store difilter benar? (SEFT Corp `12993` / Jogja `30898`)
- [ ] Akun Meta sesuai pasangan store-nya? (jangan campur)
- [ ] Status Scalev = `completed` (BUKAN `payment_status=paid`)?
- [ ] Basis tanggal sadar: `paid_time` (banding Meta) / `created_at` (banding UI)?
- [ ] Field Meta dibaca dari `actions[]` → omni_purchase / initiate_checkout / add_to_cart?
- [ ] Periode ≤7 hari terakhir ditandai provisional?
- [ ] Total store JANGAN via join utm (undercount)?
- [ ] Hasil dicocokkan ke angka acuan §4 sebagai sanity-check?
- [ ] Selisih arah sudah benar? (Meta−Scalev: positif = Meta overclaims → "+"; negatif = Meta underclaims → "−")
- [ ] Coverage note generik (tidak hardcode link satu store tertentu)?
- [ ] Jika per-content dashboard: JSON dump dulu sebelum overwrite HTML? (owner preference)
- [ ] Summary Scalev global mencerminkan **kedua store** (cek `summary.per_store['12993']` dan `'30898'`; `summary.scalev_store_result` harus total keduanya, bukan hanya store terakhir di-merge)?
- [ ] Summary card "Scalev Riil" menampilkan `scalev_tagged_result` (duit real per-konten), BUKAN `scalev_store_result`? Selisih = Meta − tagged?
- [ ] Row-scalev hanya diisi untuk store yang sesuai (`row.store_id == --store-id`)? Jangan sampai Scalev Jogja nempel ke row SEFT atau sebaliknya.

## 8. PITFALLS (from real sessions)

### CTR is already a percentage from Meta API
`get_insights` returns `ctr` as a percentage value, NOT a decimal. E.g. `3.587047` means **3.59%**, not 0.03587%.
**Correct formatter:** `v.toFixed(2) + '%'` — do NOT multiply by 100.
This was discovered Jun 2026 when the first dashboard showed CTR as 358% because the formatter did `(v*100).toFixed(2)`.

### No decorative/fake controls in dashboards
**Owner correction (Jun 2026):** Do NOT add checkbox columns, On/Off toggle switches, status badges, or any UI element that looks interactive but serves no real function. The owner explicitly said: "ad on off yang cuma hiasan ga usah di pake hapus aja" (the On/Off toggle that's just decoration — remove it).
- If a control doesn't trigger an actual state change, don't include it.
- Only ship functional UI: summary cards, account toggle buttons (working), sortable table headers, date picker (working).
- No Meta-style chrome: no sidebar, no header banner, no filter chips, no search box unless explicitly requested.

### Short date format must be prominent
The `period.short` field (e.g. `"01–19 Jun 2026"`) is not optional — the owner explicitly demanded it. Render it in the dashboard header as a visible date range indicator. Format helper (when same month/year):
```
s.day:02d–u.day:02d MONTH_ID[s.month-1] s.year
```
Cross-month: `"01 Jun – 19 Jul 2026"`.

### Summary cards must reflect the CURRENT filter, not the full dataset
When account toggles are active, KPI summary cards (total spend, result, CPR, etc.) must recalculate to show only the visible rows — NOT the full unfiltered dataset. Failing to do so makes toggle useless.

### Selisih sign direction (don't invert)
`Selisih = Meta − Scalev`. Di dashboard:
- Positif (mis. `+18`) = Meta mengeklaim 18 lebih banyak dari Scalev → Meta overclaims.
- Negatif (mis. `−18`) = Scalev mencatat 18 lebih banyak dari Meta → Meta underclaims.
- **Warna:** positif = merah/over (hlr), negatif = hijau/under (hl).
- **Jangan pernah terbalik:** bug ini pernah terjadi — formatter menampilkan positif sebagai `−X` dan negatif sebagai `+X`.

### Coverage link jangan hardcode satu store
Coverage note yang menautkan laporan detail jangan hardcode ke store ID tertentu (mis. link `/mjo-konten-12993.html` saja). Jika dashboard dipakai di beberapa store, link harus dinamis atau hapus.

### Total store perfect + per-content gap = NORMAL EXPECTED STATE

**Key insight from 18 Jun 2026 debug:** When the store-level total matches perfectly (Meta=57,
Scalev=57, diff=0), a per-content gap of 6 untagged (coverage ~89.5%) is NOT a bug. It's the
expected state of a healthy UTM-tracking system behind a redirect domain.

**Why:** Even with perfect total alignment, per-content matching has natural limits:
- Redirect domains (logosvillage.com) can strip or modify UTM parameters during forwarding.
- Some customers type the URL directly (no UTM).
- CS-assisted orders bypass the web funnel entirely.

**Don't chase 100% coverage.** The realistic healthy range is ~89–95%. Forcing allocation to
100% creates speculative row-level attribution that can mislead kill/scale decisions.

**18 Jun 2026 reference (concrete example):**
```
Total:     Meta=57, Scalev=57 ✅ diff=0
Tagged:    51 (89.5%)
Gap:        6 across 4 ads
  ┬ 3 from date boundary — orders paid on adjacent day (paid_time settlement vs Meta conversion)
  └ 3 truly untagged — no matching UTM recorded (redirect strip / direct traffic / CS orders)
```

When investigating a "small gap" after store totals are already confirmed matching:
1. First confirm store total IS already matched (many bugs are actually at store level).
2. If store total matches, the gap is normal and does not require a code fix.
3. Document the gap as `coverage: N%` and move on.
4. Only act if coverage drops below ~80% — that signals a systematic tracking failure.

### Date boundary mismatch: `created_at` vs `paid_time` AND `paid_time` settlement lag

**Two distinct date boundary effects:**

**A) `created_at` vs `paid_time` shift (the classic one):**
When a per-content dashboard shows low Scalev tagged rate (e.g. 7% for a store with 28 orders),
**the first thing to check is the date basis alignment**, NOT the UTM tag matching.

This was the root cause in the DC-4593 Jogja debug (Jun 2026). Meta recorded 4 conversions on
18 Jun. Scalev with `created_at` showed only 2 tagged orders. But Scalev with `paid_time` showed
4 total orders for the tagged ads—they just fell on 17 Jun for `paid_time` instead of 18 Jun.

**Why:** An order created at 23:55 WIB on 17 Jun (paid later) is recorded on `created_at=17 Jun`
but the Meta conversion happens on `18 Jun` (the ad click → purchase cycle). The sale is real,
it's just timestamped differently.

**B) `paid_time` settlement vs Meta conversion-time shift (adds ±1 day even with correct basis):**
Even when the dashboard correctly uses `paid_time`, a ±1 day shift can occur because:
- Scalev `paid_time` = the moment payment **settles** (e.g. COD courier transfer clears, credit
  card payment posts). For COD this can be 1–3 days after delivery.
- Meta conversion time = when the purchase **event fires** (user clicks Buy, payment is authorized
  but not yet settled).
- The two timestamps naturally differ by 1 day for COD-heavy stores.

**Concrete example from 18 Jun 2026:**
```
Rev-habibi anxiety:  Meta=4 (18 Jun)  Scalev paid_18=3  Scalev paid_17-18=8
ivana:              Meta=2 (18 Jun)  Scalev paid_18=1  Scalev paid_17-18=2
```
Both ads show Meta > Scalev on 18 Jun alone, but Scalev >= Meta when 17 Jun is included.
If the gap closes when expanding ±1 day, it is a date-boundary/settlement issue, not tracking failure.

**Diagnostic:**
When investigating a per-content gap, always check:
1. `get_order_statistics` with `dt=paid_time` for the single date → tagged count per content.
2. `get_order_statistics` with `dt=paid_time` for an expanded range (±1 day) → if the gap
   closes, the remaining orders fell on the adjacent day.
3. If gap closes on expanded range, it's a **date boundary shift** — no tracking fix needed.
4. If gap persists on expanded range, it's **truly untagged** — UTM strip / direct traffic.

**Correct approach per session:**
1. Always check the store-level total first on BOTH bases: `get_order_statistics` with `dt=paid_time`
   AND `dt=created_at`, comparing the row counts per day.
2. If totals differ, a date boundary shift is active. The dashboard **MUST use `paid_time`** as
   default when comparing with Meta.
3. Trace specific low-coverage ads: query per `utm_content` on BOTH `paid_time` and `created_at`
   to find which day the order actually falls on. If the order exists on a nearby date, it's a
   date boundary issue, NOT a tracking failure.
4. Only after confirming date alignment should you proceed to UTM/deep tracking debugging.

**Implementation rule (OWNER OVERRIDE 22 Jun 2026):** API server default `datetime_type` = `created_at`
(di `/opt/mjo-api/mjo_api.py` handler `/api/mjo-data`). Dashboard UI MUST provide a two-mode
`datetime_type` toggle and explain it in business language, not only technical labels:
- **Result Konten / Created — order lahir dari konten (default)** → `created_at`. Use for creative/content evaluation & omset: “konten ini bikin orang create order berapa?”
- **Result Paid / Meta — cocok Meta & uang masuk** → `paid_time`. Use for Meta reconciliation (Selisih/Match%) and paid/revenue truth.

Owner memilih `created_at` default karena fokus pada nilai konten & omset, dan basis Paid membingungkan.
`paid_time` tetap WAJIB tersedia sebagai toggle (jangan dihapus) untuk rekonsiliasi sejajar Meta.
The dashboard helper sentence: **“Default Created untuk nilai konten & omset. Ganti ke Paid kalau mau banding angka Meta.”**
When `paid_time` is selected, note it aligns with Meta conversion-time; when `created_at` (default),
note that the Selisih-vs-Meta column can drift because Meta counts on pay-day.

### `merge_scalev_into_mjo_data.py` and the API server (`/opt/mjo-api/mjo_api.py`) are independent code paths

The merge script (`scripts/merge_scalev_into_mjo_data.py`) and the live API server (`/opt/mjo-api/mjo_api.py`) both contain their own `enrich()` / Scalev-join logic. Patching one does NOT fix the other.

- **Merge script** is a batch tool: reads `mjo-data.json`, enriches Scalev per ad_name, writes back.
- **API server** (`mjo_api.py` on port 8787) pulls fresh data from Meta + Scalev on each request, caches to `/var/www/html/mjo-cache/`, and writes its result back to the same `mjo-data.json`.

When the user clicks **Apply** on the dashboard, they hit the API server, NOT the merge script. If a fix (untagged allocation, decision rules, bugfix) is only in the merge script, the API server's independent code will overwrite it on the next Apply click.

**Both code paths must be patched separately when adding new reconciliation logic.** The reference `references/mjo-api-server.md` documents the API server structure; any Scalev-join improvement added to the merge script should be read-translated into the API server's `enrich()` function.

**The durable fix is a shared policy engine.** Both code paths should call the same `policy_engine.apply_policy(rows, per_store, dt)` from `/opt/mjo-api/policy_engine.py`. The policy itself lives at `/opt/mjo-api/policy/scalev_allocation.yaml`. See `references/policy-engine-source-of-truth.md`.

### `enrich()` function ordering: store totals BEFORE allocation, NOT after
A bug found in Jun 2026: inline allocation code (allocating untagged orders) referenced `stores` and `per_store` variables that were computed LATER in the same function. This caused a `NameError` at runtime.

Correct ordering of `enrich()`:
1. **Step 1 — per-ad Scalev matching**: query Scalev API per `(store_id, ad_name)` pair, set `scalev_result`, `scalev_revenue`, `scalev_cpr`, `meta_scalev_diff`, `meta_scalev_match_rate` on each row.
2. **Step 2 — store-level totals**: compute `stores` from distinct `store_id` values in rows, then call `scalev_stats(store_id, ...)` without `utm_content` filter to get the true store total. Populate `per_store[store_id]`.
3. **Step 3 — apply policy**: call `policy_engine.apply_policy(rows, per_store, dt)` which does allocation + decision rules in one pass.
4. **Step 4 — recompute summary**: compute `tagged`, `tagged_rev`, `total_spend`, `total_meta`, `total_ic`, `total_atc` from the now-enriched rows. Build and return the summary dict.

Never put allocation logic before store totals are available. Never compute `tagged` from the per-ad cache before allocation is complete.
There is no way to see the raw `utm_content` value on individual orders via `mcp_scalev_list_orders`.
The response schema only contains customer info, product, pricing, status, and dates — no UTM fields.
However, `get_order_statistics` with a `utm_content=<value>` filter in the query parameters
DOES work for per-content aggregation.

This means:
- You cannot directly verify "what UTM value did order #12345 carry" through the API.
- To debug a specific ad name mismatch: use `get_order_statistics` with `utm_content=<ad_name>`
  and check if any orders appear. If yes, UTM tracking IS working for that ad.
- If `get_order_statistics` returns 0 for that ad but the store total clearly includes orders →
  the ad name in Meta doesn't match the `utm_content` recorded at order time.
- Workaround for full verification: check through Scalev dashboard UI, or inspect the landing
  page URL structure for UTM parameter passing.

### ad_id fallback via Scalev `utm_content=ad_id` does NOT work for untagged ads

When a Jogja ad has Meta=1 Scalev=0 and you attempt fallback by querying Scalev with `utm_content=<ad_id>` (numeric), coverage does NOT improve. This was tested on MUH FARID (HNP) and Budinda (both from DC-4593, creative without url_tags). The result was still zero.

**Root cause:** The ad's `url_tags` template (`utm_source={{site_source_name}}&utm_medium={{placement}}&utm_campaign={{campaign.name}}&utm_content={{ad.name}}`) uses `{{ad.name}}`, not `{{ad.id}}`. But even querying with the `ad.name` already returned 0 during the main join pass. The real problem is not ad_id vs ad_name — it's that the destination landing page (logosvillage.com/... ) strip or fail to forward UTM parameters during the redirect to Scalev's checkout. No fallback key will recover these orders on the content level.

**Don't chase ad_id fallback unless you confirm the creative's `url_tags` actually uses `{{ad.id}}`. First check the creative's `url_tags` field. If missing entirely, the issue is at the landing page / redirect level, not the join key.**

### Multi-store merge must filter rows by store_id and aggregate per-store summary

`merge_scalev_into_mjo_data.py` is often run sequentially for both stores (`12993` SEFT Corp and `30898` Jogja) against a single combined `mjo-data.json`. Two bugs are easy to introduce:

1. **Row overwrite bug:** if the merge loop iterates all `per_ad` rows while calling Scalev for only one `--store-id`, it will write that store's Scalev counts into ads from the other store. This makes “semua akun salah”. Always build `target_rows = [row for row in per_ad if str(row.store_id) == str(args.store_id)]` and only read/write those rows.
2. **Last-store summary bug:** if `summary.scalev_store_result`, `scalev_tagged_result`, and `scalev_coverage` are overwritten on every run, the final JSON only reflects the last merged store. Keep per-store buckets under `summary.per_store[store_id]` and recompute global totals from those buckets.
3. **Static file vs API/cache mismatch:** the dashboard may load `/var/www/html/mjo-data.json` on initial page load but call `/api/mjo-data` and `/var/www/html/mjo-cache/<since>_<until>_<dt>.json` after Apply. If a screenshot still shows stale numbers after fixing the static JSON, inspect/refresh the API cache and patch the live API source (for this deployment: `/opt/mjo-api/mjo_api.py`) as well. Do not claim fixed until the exact UI path the user screenshotted is verified.

Correct behavior after merging both stores for 18 Jun 2026 sanity-check:
- SEFT Corp (`12993`): Scalev total 28, tagged 27, coverage 96.4%.
- Jogja (`30898`): Scalev total 29, tagged 27, coverage 93.1%.
- Combined: Scalev total 57, tagged 54, coverage 94.7%; Meta total 57, `meta_scalev_diff_total = 0`.

Use `references/multi-store-merge-guardrails.md` before editing or trusting merge output.

### User screenshot triage: fix the visible wrong number first
When Akbar sends a dashboard screenshot and points to one wrong number (e.g. “Scalev masih 2 padahal 4”), do not broaden into a full report or long explanation. First reproduce the exact UI state: selected account pill(s), date range, basis (`paid_time`/`created_at`), force/cache status, and visible summary number. Then inspect only the rows behind that filtered view and patch the smallest source of mismatch. Reply with terse proof like `DC-4593 18 Jun paid_time: Meta=4, Scalev=4; changed MUH FARID and Budinda from 0→1 via allocated_untagged`.

### Duplicate ad names must not receive the full Scalev count on every row
When multiple Meta rows share the same `(store_id, ad_name)`, a naive per-content cache (`cache[(store_id, ad_name)] = Scalev count`) and then assigning that full count to each row will double/triple-count Scalev. This was found on 17 Jun 2026 where `New USP` appeared twice under KANTOR MJO-1054: the same Scalev=2 was attached to both rows, making one row show `Meta=1 Scalev=2` and inflating tagged totals.

Correct handling in the API/server `enrich()` path:
1. Group rows by `(store_id, ad_name)` after fetching the Scalev total for that key.
2. If a group has one row, assign normally.
3. If a group has multiple rows, allocate the single Scalev total across the group instead of duplicating it:
   - Prefer proportional allocation by Meta `result_purchase` among rows with Meta > 0.
   - If all Meta are 0, assign the Scalev total to one row and mark the others 0, or flag the group for manual review.
   - Recompute `scalev_revenue`, `scalev_cpr`, `meta_scalev_diff`, and `meta_scalev_match_rate` per allocated row.
4. Add an audit field such as `scalev_fallback='duplicate_ad_name_allocated'` or `scalev_allocation_note` so the dashboard/debugger can explain why row values differ from raw `utm_content` total.

Debug recipe when a screenshot shows `Scalev > Meta` or totals that do not add up:
```python
from collections import Counter
name_counts = Counter((r['store_id'], r['ad_name']) for r in rows)
for key, n in name_counts.items():
    if n > 1:
        print(key, n, [(r['account_name'], r['result_purchase'], r['scalev_result']) for r in rows if (r['store_id'], r['ad_name']) == key])
```
Always check duplicate ad names before assuming the issue is UTM stripping, attribution lag, or a policy allocation problem.

### `Scalev > Meta` is not a bug — never cap Scalev by Meta when matching Scalev UI
A unique ad can legitimately show Scalev orders above Meta claims when Scalev counts all completed orders carrying the UTM while Meta only attributes conversions inside its attribution/modeling window. Example found on 17 Jun 2026: `LP2 - Iklan DPR Hook_HowToo` showed Meta=13, Scalev=15; `Iklan Experience Level 2 Deep Hook` showed Meta=2, Scalev=3.

**Hard lesson from DC-4593 / 20 Jun 2026:** The API path had this bug:
```python
assign_total = min(sc_total, meta_total)
```
This undercounted Scalev whenever Meta under-attributed. A screenshot showed DC-4593 should be **4** in Scalev, but dashboard showed **2** because:
- `Masalah Hidup`: Meta=1, Scalev=2 → capped to 1
- `11/6/2026-ATIKA`: Meta=0, Scalev=1 → capped to 0
- `8 Grand Slam - ... Salin`: Meta=2, Scalev=1 → stayed 1

Correct API/server behavior:
```python
assign_total = sc_total  # Scalev is source-of-truth; preserve real completed orders
```
For duplicate `(store_id, ad_name)` groups, apportion the Scalev total across duplicates, but **do not bound each row by Meta count**. If all duplicate rows have Meta=0, keep the Scalev total visible on one row and mark for review.

Dashboard display rule:
- Preserve true Scalev count and label/explain rows where `scalev_result > result_purchase` as `Scalev > Meta / attribution window` or `scalev_over_meta`.
- Do **not** silently cap Scalev to Meta. Capping hides real Scalev orders and makes Akbar see mismatch against the Scalev UI.

Do not apply a blanket cap without checking duplicate ad names first; duplicate-counting is a data bug, while true `Scalev > Meta` can be a business signal.

### If the user challenges a quick allocation, find the source and encode it
Owner correction (Jun 2026): if Akbar says the fix is just “main alokasi” and asks for the **sumber**, stop treating the one-day JSON/cache as the solution. Find and patch the durable source path:
1. policy/source-of-truth rule (e.g. `/opt/mjo-api/policy/scalev_allocation.yaml`),
2. shared policy engine (e.g. `/opt/mjo-api/policy_engine.py`),
3. live API code path (`/opt/mjo-api/mjo_api.py`),
4. dashboard field logic (`/var/www/html/mjo-dashboard.html`),
5. force-refresh API/cache and verify the exact filtered view.

Do not answer with a long conceptual proposal when the user is angry. Give the exact source files, the rule, and the proof. See `references/policy-engine-source-of-truth.md`.

### Scalev Riil di summary card = `scalev_tagged_result`, BUKAN `scalev_store_result`

**Owner correction (Jun 2026):** Akbar explicitly corrected: *"51 itu duid masuk itu yg real gw itung oi, jangan halu"* — the real money per-content is the tagged Scalev count, not the store-level total.

**Consequences for dashboard (render() function):**

1. **Scalev Riil card** — MUST use `sum.scalev` (tagged per-content = `scalev_tagged_result`) as the primary "real money" number. NOT `storeResult` (`scalev_store_result`).
2. **Selisih** — MUST be `sum.meta - sum.scalev` (Meta claim minus tagged real). NOT `sum.meta - storeResult` (which produces false zero when store totals align perfectly).
3. **Store total** — SHOWN as a separate "Total Store" card with coverage note, as secondary context only. Never as the primary real-money metric.
4. **Coverage** — `sum.scalev / storeResult` = what % of store orders can be traced to content. Healthy range is 89–95%.

**Implementation fix (from 19 Jun 2026):** in `/var/www/html/mjo-dashboard.html`:
```javascript
// ✅ CORRECT
const selisih = sum.meta - sum.scalev;  // wait, I need to check: this should be sum.meta - sum.scalev
// Scalev Riil card uses sum.scalev (tagged per-content)
// Total Store card uses storeResult (store total)

// ❌ WRONG (pre-fix)
const selisih = sum.meta - storeResult;  // produces 0 when store aligns perfectly
// Scalev Riil card uses storeResult — falsely shows store total as real money
```

When all accounts in a store are selected:
- **Before:** Scalev Riil = 57, Selisih = 0 (false match)
- **After:** Scalev Riil = 51, Selisih = +6 (real gap), Total Store = 57 (context)

See the `§9b` summary card spec for the correct card layout. The store total must remain visible as context so the owner knows there ARE orders in the store, just not all attributable to content.
When using `listOrders`'s `stores_orders_count` as a sanity check (e.g. "28 orders for Jogja"),
remember this includes all order statuses: pending, confirmed, shipped, completed, cancelled, etc.
For reconciliation, `get_order_statistics` with `status=completed` is the authoritative count.
The raw count from `listOrders`/`stores_orders_count` will always be higher.

### Health endpoint sangat berguna
API server (Python stdlib http.server) butuh endpoint `/health` yang return `{"ok": true, "service": "mjo-api", "port": 8787}`. Ini memudahkan debugging cepat sebelum/sesudah restart.

### Cron toolsets menentukan apa yang bisa dilakukan
Cron yang perlu:
- **Write file HTML/JSON ke disk →** butuh `file` + `terminal` di `enabled_toolsets`
- **Cuma trigger API →** `web` saja cukup
- **Baca file konfigurasi →** butuh `file`

Periksa daftar toolsets yang diizinkan di `cronjob` action='create' untuk memastikan cron punya akses yang diperlukan.

## 9. Automated Dashboard (Cron-based, hourly refresh)

When the owner requests an always-live dashboard on `hermest.gerbangduid.my.id`:

### 9a. Store-level (aggregate summary) — LEGACY
1. Summary-level data → cron job using `cronjob` tool.
2. Self-contained prompt: list both Meta accounts, Scalev store.
3. Generate HTML: KPI cards, daily table, reconciliation summary.
4. Write to `/var/www/html/<name>.html`, set `deliver: local`.

Full reference: `references/hourly-static-dashboard.md`.

### 9b. Per-content dashboard (PREFERRED) — actionable per-ad creative

**CRITICAL — owner mandate:** Scalev riil data is THE MOST IMPORTANT metric. The per-content dashboard MUST include per-content Scalev result, Selisih (Meta - Scalev), and Match% columns. Never ship a dashboard with only Meta `result_purchase` as the primary result metric unless explicitly approved.

**AUTO-LABEL SYSTEM:** The dashboard must auto-label each ad row using the window-based
decision rules from §5b. Labels (ALARM, OBSERVASI, SCALE, KILL, CEK NAMA) appear in the
"Vonis" column with colored HTML tags. A **Vonis Summary bar** at the top shows aggregate
counts per label. The summary also shows the current **Target CPR** and **Window rules**
(e.g. "Target: Rp180K · 2H=alarm · 3H=kill · 5–7H=scale"). Implementation in the dashboard
HTML is at `/var/www/html/mjo-dashboard.html` — CSS classes `.tag-a` (orange), `.tag-o`
(blue), `.tag-g` (green), `.tag-r` (red), `.tag-p` (purple).

When user asks **per konten** with **CPR, IC, Result, ATC Rate, Add to Cart Cost**:

1. Pull `get_insights(level="ad")` from both SEFT Corp accounts for MTD.
2. Extract `actions[]`: omni_purchase (Result), initiate_checkout (IC), add_to_cart (ATC), link_click.
3. Calculate derived metrics per ad:
   - CPR = spend / result
   - Cost per IC = spend / IC
   - Add to Cart Cost = spend / ATC
   - ATC Rate = ATC / link_clicks (fallback clicks)
4. Apply decision rules (§5b) using Meta-only data for initial classification.
5. **Merge with Scalev per-content data (MANDATORY step):**
   - For each unique `ad_name`, query Scalev API `/v3/orders/statistics` with `utm_content=ad_name`, `status=completed`, `datetime_type=paid_time`, `breakdown_date=day`.
   - Aggregate daily results for the target date range.
   - Add to each ad: `scalev_result`, `scalev_revenue`, `meta_scalev_diff` (= result_purchase − scalev_result), `meta_scalev_match_rate` (= scalev_result / result_purchase), `scalev_cpr` (= spend / scalev_result).
   - Reclassify decisions based on Scalev data (see §5b rules).
   - Also pull total store count (without utm filter) and store revenue for the coverage banner.
6. **JSON shape** must include these additional fields:
   ```json
   {
     "summary": {
       "period": {"since":"YYYY-MM-DD", "until":"YYYY-MM-DD", "short":"01–19 Jun 2026", "timezone":"Asia/Jakarta"},
       "total_result_purchase": 549,
       "scalev_store_result": 496,
       "scalev_tagged_result": 205,
       "scalev_untagged_result": 291,
       "scalev_coverage": 0.41,
     "generated_at": "2026-06-19 12:00:00",
     "is_provisional": false
   },
   "per_ad": [
       {
         "scalev_result": 74,
         "scalev_revenue": 8950000,
         "meta_scalev_diff": 9,
         "meta_scalev_match_rate": 0.89,
         "scalev_cpr": 121696
       }
     ]
   }
   ```
7. **Dashboard HTML columns** — required set:
   - Ad, Spend, **Meta** (Meta claim), **Scalev** (riil, bold), **Selisih** (colored: red if overshoot, green if matched), **Match%**, **CPR Meta**, **CPR Riil** (may differ), IC, Cost IC, ATC, Cost ATC, ATC Rate, CTR, CPM, CPC, Vonis.
   - Summary cards at top MUST include: Total Spend, Meta Claim, **Scalev Riil** (highlighted, = `scalev_tagged_result` — real uang masuk per konten, BUKAN total store), **Total Store** (store total `scalev_store_result` sebagai konteks + coverage%), **Selisih Total** (Meta − Scalev Riil / tagged), Avg CPR, **CPR Riil**, CPM, CTR, IC, ATC.
8. **Short date indicator** — must appear prominently in the header (`<span class="period">01–19 Jun 2026</span>`), using the `period.short` field from the enriched JSON.
9. **Coverage warning** — if `scalev_coverage < 70%`, render an amber warning banner showing the untagged order count and linking to the full report (`mjo-konten-<store>.html`).
10. **CRITICAL — owner preference: JSON dump first (`mjo-data.json`), offer verification, then overwrite HTML only after approval.**
11. Write enriched JSON to `/var/www/html/mjo-data.json`, HTML to `/var/www/html/mjo-dashboard.html`.
12. Short stable redirect: `/var/www/html/mjo/index.html` → `/mjo-dashboard.html`.
13. Cron: `every 1h`, `deliver: local`.

See `references/per-content-json-dashboard.md` for detailed JSON shape, action parsing rules, and HTML rendering requirements. The reference file covers the Meta-only baseline; the Scalev enrichment steps above override/extend it.

PITFALL — generating `scalev_result` per ad takes one Scalev API call per unique `ad_name` (55+ calls, ~45s each max). Use the existing script `generate_content_report.py` as a reference or run it directly for the Scalev lookup, then merge the results into the existing `mjo-data.json`. The merge script pattern is:
```
python3 generate_content_report.py <store_id> <since> <until>  → produces HTML + raw data in memory
# Then merge scalev fields into mjo-data.json using ad_name as join key
```
A reusable merge script is available at `scripts/merge_scalev_into_mjo_data.py` in this skill's directory:
```
python3 ~/.hermes/skills/mjo-reconciliation/scripts/merge_scalev_into_mjo_data.py \
  --store-id 12993 \
  --input /var/www/html/mjo-data.json \
  --output /var/www/html/mjo-data.json
```
When `mjo-data.json` contains rows for **both stores** (SEFT Corp `12993` and Jogja `30898`), run the merge **for each store** in any order:
```
python3 ... --store-id 12993 ...
python3 ... --store-id 30898 ...
```
Each run only touches rows matching its `--store-id` and updates per-store accumulator in `summary.per_store`. The global summary fields (`scalev_store_result`, `scalev_tagged_result`, `scalev_coverage`, `meta_scalev_diff_total`) are recomputed from the per-store buckets on every run. See `§8 pitfalls — Multi-store merge` for the old bug and fix rationale.

**When owner says "terlalu general" / "mau per konten" → use 9b, not 9a.**

### 9c. Interactive date-range dashboard (server-side data pull via API)

> **STATUS: Aspirational / not yet implemented (Jun 2026).** The reference file `references/mjo-api-server.md` documents the desired architecture for an interactive API server. The current dashboard is purely static: cron-generated JSON file at `/var/www/html/mjo-data.json` read by the static HTML. To build this, create `/opt/mjo-api/mjo_api.py`, add nginx proxy, and configure systemd — see reference for the full plan.

**When owner asks for a date-range picker that triggers a server-side data pull** (not client-side filtering of cached data):

This is a fundamentally different architecture from §9a/§9b: instead of a cron-pushed static HTML, run a persistent HTTP server that pulls fresh data on demand.

#### Architecture

```
Browser date picker
  → Apply button → GET /api/mjo-data?since=YYYY-MM-DD&until=YYYY-MM-DD&force=1
  → Nginx proxy (location /api/ → 127.0.0.1:8787)
  → Python HTTP server (stdlib http.server)
    → Tarik Meta Ads ad-level (get_insights) for all SEFT Corp accounts
    → Tarik Scalev per-content (get_order_statistics) for each ad_name
    → Merge & enrich JSON
    → Return JSON response
  → Browser replaces dashboard table + summary with fresh data
```

#### API server setup

```python
# Minimal Python HTTP server at /opt/mjo-api/mjo_api.py
# Port 8787, stdlib only (no Flask dependency)
# Endpoints:
#   GET /api/mjo-data?since=YYYY-MM-DD&until=YYYY-MM-DD&force=1
#   GET /health

# Server lifecycle:
python3 /opt/mjo-api/mjo_api.py &   # background process
# Use process management:
# - process(action="poll") to check running
# - process(action="wait") on startup
# - Verify with: curl http://127.0.0.1:8787/health
```

#### Nginx proxy block

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:8787;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_read_timeout 300s;
    proxy_connect_timeout 10s;
    # CORS headers for static HTML to call API
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods "GET, OPTIONS";
    add_header Access-Control-Allow-Headers "*";
}
```

#### API endpoint behavior

- `since`/`until`: ISO dates in `YYYY-MM-DD` format
- `force=1`: skip cache, always pull fresh from Meta + Scalev APIs
- Response shape: same as `mjo-data.json` (§9b enriched JSON) but with the requested date range
- Scalev: calls `get_order_statistics` per unique `ad_name` — can take 30–60s for 55+ konten
- The API server should set a short timeout per upstream call (45s per unique content, ~60s total)

#### Dashboard frontend wiring (HTML + JS)

The `mjo-dashboard.html` must include a date-range picker overlay that:

1. Shows two monthly calendars (current + next month) with weekday headers Mo–Su
2. Left sidebar with shortcut buttons: Today, Yesterday, This Week, Last 1 Week, Last 2 Weeks, This Month
3. Click-to-select: first click = start date (blue circle), second click = end date (blue circle), in-range dates get light blue background
4. Apply button → `GET /api/mjo-data?since=<start>&until=<end>&force=1`
5. Loading spinner during API call
6. On success: update summary cards + table rows with fresh data
7. On error: show error message with retry button
8. Cancel/close button to dismiss the overlay

**Pitfall — full page reload vs dynamic update: owner must be asked which they prefer.** If full reload, navigate to `?since=X&until=Y` and let the page init load from the API on DOMContentLoaded. If dynamic, use fetch() and DOM replacement.

**Pitfall — API server persistence:** a background `python3` process dies on VPS reboot. To make it survive reboots, either:
- Systemd service unit (preferred for production)
- Cron `@reboot` entry (simpler, acceptable for dev)
- The Hermest cron `mjo-reconcile` could health-check the API and restart if down (advanced)
After re-creating the server (e.g. after config changes), kill the old PID and start fresh.

**Pitfall — Scalev per-content calls are slow:** 55+ API calls at ~45s each could take 40+ minutes sequentially. The `get_order_statistics` endpoint with `utm_content` filter is the bottleneck. Mitigation: reduce unique konten by batching or accepting partial Scalev data for the initial render (show Meta data immediately, enrich Scalev in background).

See `references/mjo-api-server.md` for the full server implementation pattern including: request routing, error handling, cache headers, and the Scalev per-content enrichment loop.

For dashboard repair/audit sessions (`audit penuh`, `benerin`, `ini udah bener belum`), use `references/mjo-dashboard-audit-playbook.md`. It captures the safe fix workflow, required checks (Scalev SOP, date-basis alignment `paid_time` vs `created_at`, low-coverage per-content debug, selisih sign, provisional flag, health endpoint), and final response template.

For multi-store merge verification after running `merge_scalev_into_mjo_data.py` for both stores, use `references/multi-store-merge-guardrails.md`. It includes a Python verification script, common failure modes with root causes, and correct reference numbers for 18 Jun 2026.

## 10. Glossary ID
- Business: `CAO0DOK1OPKQ5ZD3` (SEFT CORP, username `seft`)
- Store SEFT Corp: `12993` (uuid `store_3RNZ4FdHtIwuaHuOcKX16P7H`) · Pixel `2806190249528198`
- Store Jogja: `30898` (uuid `6046b55d-2c73-4607-bd2c-96b1b3466457`)
- Akun: 4592 `act_1025434792768020` · 1054 `act_1101865787490596` · 4593 `act_1217688183027696` · 4594 `act_1584139655637069`