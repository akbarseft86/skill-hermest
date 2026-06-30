---
name: mjo-launch-ads
description: >
  Launch konten MJO dari antrian pipeline jadi iklan Meta berstatus DRAFT/PAUSED (ada gerbang
  review manusia). Trigger: "launch konten", "naikin iklan MJO", "bikin draft iklan dari antrian",
  "formasi 1 campaign 1 adset N konten". Baca antrian VPS → download video Drive → upload ke Meta →
  bikin campaign/adset/creative/ad (SEMUA PAUSED) niru template akun tujuan. Dua mode: PER-KONTEN
  (1:1:1) atau FORMASI (1 campaign : 1 adset : N ad — N ditentukan user, mis. 1:1:2, 1:1:3, 1:1:6).
  TIDAK PERNAH menyalakan — user review sendiri.
---

# MJO Auto-Launch (Draft) — SOP

Skill ini dijalankan di **Claude/Cowork** (yang terhubung **MCP Meta Ads resmi**). Bukan di VPS Hermest.

## Prasyarat
- MCP Meta Ads resmi aktif (punya tool `ads_create_campaign`, `ads_create_ad_set`, `ads_create_creative`, `ads_create_ad`, `ads_get_ad_accounts`).
- Akun tujuan sudah **advertiser-verified**. Kalau dapat error `code 31 "authenticate your account"` → akun belum verif: arahkan user ke Ads Manager → Account Overview → **Start verification**, lalu retry.
- API pipeline VPS: **pakai `http://127.0.0.1:8787/api/`** (jalan di VPS via Bash → bypass login). URL publik `https://hermest.gerbangduid.my.id/api/` ada di belakang **nginx Basic Auth** (Jun 2026, return 401 tanpa kredensial), jadi JANGAN dipakai buat call otomatis — selalu localhost.
- Token Meta VPS (buat upload video): `/root/.hermes/.meta-ads-token` (akses via SSH/Bash ke VPS).

## ATURAN KESELAMATAN (WAJIB, jangan dilanggar)
1. **SEMUA objek dibuat `status=PAUSED`. JANGAN PERNAH `ads_activate_entity` / menyalakan.**
2. Setelah draft jadi → **BERHENTI**, lapor link. **User yang review & nyalain.**
3. Budget default: PER-KONTEN **Rp50.000/hari**. FORMASI **skala ikut N** (saran ±Rp20–30rb/creative; mis. N=3→Rp75rb, N=5→Rp125rb) — selalu konfirmasi angka total ke user. `campaign_daily_budget`, IDR 1:1.
4. **Akun tujuan ditentukan USER** (bukan dari store). Konfirmasi dulu sebelum mulai.
5. **REM ANTI RATE-LIMIT (WAJIB — biar akun nggak kena "action blocked"/code 368):**
   - **Jeda ~20–30 detik antar pembuatan objek** (campaign → adset → creative → ad, dan antar konten). Jangan burst.
   - **Batas aman: ±1 formasi / ~5 ad per akun per sesi.** Mau lebih dari itu → **pecah ke beberapa sesi/hari** (selaras jadwal nyicil), atau sebar ke akun berbeda.
   - **Kalau kena error rate-limit** (code 368, subcode 1390008, atau "You can't use this feature right now") → **STOP TOTAL, jangan retry.** Lapor ke user, tunggu beberapa jam. Retry malah manjangin blok.
   - Sebelum mulai batch besar: ingatkan user upload manual di Ads Manager juga dihitung — jangan barengan klak-klik banyak.

## Pilih MODE dulu
- **PER-KONTEN (1:1:1):** tiap konten → campaign+adset+ad sendiri. Buat launch lepasan / 1-2 konten.
- **FORMASI (1 campaign : 1 adset : N ad):** semua creative numpuk di 1 adset, CBO bagi budget ke N ad → learning lebih cepat & murah buat testing creative. **N ditentukan user saat itu** (1:1:2, 1:1:3, 1:1:6, … tidak dipatok). **Ini mode default kalau user minta "formasi" / banyak konten sekaligus.** Saran Meta: ≤6 ad aktif per adset biar learning sehat & tiap creative kebaca — kalau user minta lebih, kerjain tapi ingatkan sekali. Bukan Dynamic Creative.

## Input dari user
- `ad_account_id` tujuan (mis. `1025434792768020` = 4592; bisa juga 1054/4593/4594).
- Mode (PER-KONTEN / FORMASI). Default FORMASI kalau ≥3 konten atau user sebut "formasi".
- FORMASI: **N** = jumlah ad dalam 1 adset (ditentukan user; bisa 2/3/4/6/…). Kalau user nyebut "formasi 1-1-3" → N=3.
- Konten mana: judul spesifik, daftar N konten (formasi), atau "semua BARU".
- FORMASI: **label batch** buat nama campaign+adset (default `MJO - <ACC> - <DDMon>-M<minggu>`).
- (opsional) budget override.

## Langkah eksekusi — MODE PER-KONTEN (1:1:1)

**1. Ambil antrian:** `GET http://127.0.0.1:8787/api/content?status=BARU`
   Tiap item: `judul, ad_copy, headline, drive_link, landing_page, store, creator, angle, id`.
   - `landing_page` kosong → STOP, minta user (iklan wajib punya tujuan).
   - `ad_copy`/`headline` kosong → minta user atau pakai ringkas dari `angle`.

**2. Ambil template dari akun tujuan** (1 iklan ACTIVE buat dicontek):
   `GET graph.facebook.com/v21.0/act_<ACC>/ads?effective_status=["ACTIVE"]&limit=1&fields=adset{promoted_object,optimization_goal,billing_event,targeting},creative{object_story_spec}`
   Catat: `page_id`, `pixel_id`, `optimization_goal` (biasanya OFFSITE_CONVERSIONS), `billing_event` (IMPRESSIONS), `targeting` (geo+age). CTA: LEARN_MORE.

**3. Per konten:**
   a. **Download video Drive** (ekstrak FILEID dari `drive_link` pola `/d/<FILEID>/`). Handle file besar:
      ```python
      import urllib.request, urllib.parse, http.cookiejar, re
      cj=http.cookiejar.CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
      op.addheaders=[('User-Agent','Mozilla/5.0')]
      data=op.open(f'https://drive.usercontent.google.com/download?id={FILEID}&export=download&confirm=t',timeout=120).read()
      if b'<html' in data[:200].lower():
          p=dict(re.findall(r'name="([^"]+)"\s+value="([^"]*)"', data.decode('utf-8','ignore')))
          data=op.open('https://drive.usercontent.google.com/download?'+urllib.parse.urlencode(p),timeout=180).read()
      open('/tmp/v.mp4','wb').write(data)
      ```
   b. **Upload ke Meta:** `POST graph-video.facebook.com/v21.0/act_<ACC>/advideos` (`-F source=@/tmp/v.mp4 -F access_token=<VPS_TOKEN>`) → `video_id`. Tunggu ready: `GET <video_id>?fields=status` sampai `video_status=ready`.
      (Video upload pakai **token VPS** via Bash — MCP resmi belum punya tool upload video.)
   c. **Thumbnail:** `GET <video_id>/thumbnails` → ambil uri `is_preferred`.
   d. **Campaign** (MCP resmi): `ads_create_campaign(ad_account_id=ACC, campaign_name="[DRAFT] <judul>", objective="OUTCOME_SALES", buying_type="AUCTION", special_ad_categories="[]", campaign_daily_budget=<budget>)`
   e. **Ad Set** (MCP): `ads_create_ad_set(ad_account_id=ACC, campaign_id, ad_set_name="[DRAFT] <judul> - adset", billing_event="IMPRESSIONS", optimization_goal="OFFSITE_CONVERSIONS", conversion_locations="WEBSITE", promoted_object='{"pixel_id":"<pixel>","custom_event_type":"PURCHASE"}', targeting='{"geo_locations":{"countries":["ID"]},"age_min":25,"age_max":65}')`
   f. **Creative** (MCP): `ads_create_creative(ad_account_id=ACC, page_id="<page>", video_id, image_url="<thumbnail>", message="<ad_copy>", headline="<headline>", call_to_action_type="LEARN_MORE", link_url="<landing_page>", name="[DRAFT] <judul> - creative")`
   g. **Ad** (MCP): `ads_create_ad(ad_account_id=ACC, ad_set_id, ad_name="<judul>", creative='{"creative_id":"<id>"}')` → PAUSED otomatis. **Nama ad = judul (kunci join dashboard).**
   h. **Tulis balik ke VPS:** `POST /api/content/update {"id":<id>,"status":"DITES","note":"draft <ad_id> @ <ACC>"}`

**4. Lapor & BERHENTI:** tabel per konten (judul · ad_id · link Ads Manager). Tegaskan: **semua PAUSED, nol spend — user review lalu nyalakan sendiri.** Jangan menyalakan.

## Langkah eksekusi — MODE FORMASI (1 campaign : 1 adset : N ad)

Struktur: **1 campaign (CBO) → 1 adset → N ad** dalam adset yang sama (N ditentukan user — 2/3/4/6/…, tidak dipatok). Tiap ad = 1 konten (nama ad = judul → kunci join dashboard tetap per-ad). Campaign+adset cuma wadah bersama, dinamai pakai label batch.

**1. Tentukan N + ambil N konten:** N dari user (mis. "formasi 1-1-3" → N=3). Konten dari daftar judul yang user sebut, atau N BARU teratas:
   `GET http://127.0.0.1:8787/api/content?status=BARU`
   Validasi TIAP konten: `drive_link`, `landing_page`, `ad_copy`, `headline` wajib ada.
   - `landing_page` kosong → STOP, minta user. `ad_copy`/`headline` kosong → minta user atau ringkas dari `angle`.
   - Konten tersedia < N → kerjain yang ada + lapor kurangnya. N besar (>6) → kerjain tapi ingatkan saran Meta sekali.

**2. Ambil template akun** — sama persis Langkah 2 mode per-konten (`page_id`, `pixel_id`, `optimization_goal`, `targeting`).

**3. Bikin WADAH sekali aja** (sebelum loop konten):
   a. **Campaign** (MCP): `ads_create_campaign(ad_account_id=ACC, campaign_name="<label_batch>", objective="OUTCOME_SALES", buying_type="AUCTION", special_ad_categories="[]", campaign_daily_budget=<budget, default 100000>)` → simpan `campaign_id`. CBO aktif (budget di campaign).
   b. **Ad Set** (MCP): `ads_create_ad_set(ad_account_id=ACC, campaign_id, ad_set_name="<label_batch> - adset", billing_event="IMPRESSIONS", optimization_goal="OFFSITE_CONVERSIONS", conversion_locations="WEBSITE", destination_type="WEBSITE", promoted_object='{"pixel_id":"<pixel>","custom_event_type":"PURCHASE"}', targeting='{"geo_locations":{"countries":["ID"]},"age_min":25,"age_max":65}')` → simpan `adset_id`. **JANGAN set budget di adset** (campaign udah CBO).

**4. Loop tiap konten (N kali)** — semua masuk `adset_id` yang SAMA:
   a. Download video Drive (kode sama Langkah 3a per-konten) → `/tmp/v<N>.mp4`.
   b. Upload ke Meta (`act_<ACC>/advideos`, token VPS) → `video_id`, tunggu `video_status=ready`.
   c. Thumbnail: `GET <video_id>/thumbnails` → uri `is_preferred`.
   d. **Creative** (MCP): `ads_create_creative(ad_account_id=ACC, page_id, video_id, image_url=<thumb>, message=<ad_copy>, headline=<headline>, call_to_action_type="LEARN_MORE", link_url=<landing_page>, name="[DRAFT] <judul> - creative")`.
   e. **Ad** (MCP): `ads_create_ad(ad_account_id=ACC, ad_set_id=<adset_id sama>, ad_name="<judul>", creative='{"creative_id":"<id>"}')` → PAUSED.
   f. **Tulis balik:** `POST /api/content/update {"id":<id>,"status":"DITES","note":"formasi <campaign_id>/<adset_id> · ad <ad_id> @ <ACC>"}`.

**5. Lapor & BERHENTI:** 1 campaign + 1 adset + tabel N ad (judul · ad_id). Link Ads Manager ke campaign. **Semua PAUSED, nol spend — user review & nyalakan sendiri.**

⚠️ **Budget formasi:** N creative berbagi 1 kolam CBO. Skala budget ikut N (saran ±Rp20–30rb/creative) & selalu konfirmasi total ke user. Kalau optimization PURCHASE dan budget tipis → nilai awal dari hook rate/CTR, jangan nunggu purchase. Saran Meta ≤6 ad aktif/adset; lebih dari itu boleh tapi ingatkan sekali.

## Catatan
- Kalau pakai token VPS langsung buat bikin creative → gagal "development mode" (app VPS belum Live). Maka **creative + ad WAJIB lewat MCP resmi**. Campaign/adset/video-upload boleh token VPS.
- Template per akun beda → selalu tarik ulang template dari akun tujuan di Langkah 2.
- **Start time dari jadwal:** kalau konten dijadwalin (tanggal+jam), set `start_time` ad set ke jadwal itu (ISO 8601 +07:00) PAS bikin ad set — biar user bisa Publish/nyalain langsung & Meta auto-mulai pas waktunya. **start_time TIDAK bisa diedit setelah ad set lewat waktu mulai** (error 1487057) → kalau telanjur, bikin ad set baru (reuse creative_id) + hapus yang lama.
- Referensi bukti & detail: memori [[mjo-content-pipeline]].
