---
name: travel-comparison-dashboard
description: "Build multi-source accommodation comparison dashboards: collecting data from AI, PDFs, direct websites, and marketplaces (Airbnb), verifying all links, classifying locations by beach proximity, and publishing as a filterable HTML table."
version: 1.0.0
author: Hermest CEO
trigger: user asks to compare hotels, Airbnb, villas, or accommodation options in Bali or any travel destination, especially wanting a table/HTML/dashboard summary.
---

# Travel Comparison Dashboard

Workflow untuk membangun halaman perbandingan akomodasi travel dari berbagai sumber (AI, PDF, website resmi, Airbnb) dalam satu tabel HTML interaktif.

## Workflow

### 1. Collect Data from All Sources
- AI research: scraping dari web_search, web_extract
- PDF: load skill `ocr-and-documents` untuk ekstraksi PDF
- Direct website: browser_navigate untuk harga/fasilitas
- Marketplace (Airbnb): search via browser, extract listing cards

### 2. Airbnb Data — Critical Verification Steps
- **VERIFY ALL LINKS** sebelum masuk tabel — jangan percaya room ID hasil scrape mentah.
- Untuk **monthly stay / long stay**, pakai rentang tanggal ±30 malam di URL pencarian (mis. `checkin=2026-07-01&checkout=2026-07-31`) agar Airbnb menampilkan harga `monthly` dan `Monthly discount`. Jangan pakai daily-rate search lalu mengalikan manual kecuali tidak ada alternatif.
- Prefer fresh search result domain-region URLs (contoh `airbnb.com.sg` untuk session SG) daripada memaksa `.com` jika hasil live redirect/search memakai regional domain.
- Short room IDs (e.g. `2655482324`, 10 digit) biasanya **stale/photo IDs** → return 404
- Long room IDs (e.g. `783163874925518631`, 18-19 digit) cenderung **live listing actual**
- Saat DOM card text kosong/visual blank, extract dari anchors `a[href*="/rooms/"][aria-labelledby]`, lalu resolve nama card via `document.getElementById(ariaLabelledById).innerText`; cari parent yang `innerText` terpanjang untuk harga/rating.
- Jika search backend (`web_search`) gagal/down, fallback langsung ke `browser_navigate` pada Airbnb/search-result pages dan kumpulkan data via `browser_console` DOM extraction. Jangan berhenti menunggu search engine.
- Batch test dengan Python requests + header User-Agent real browser:
  ```python
  r = requests.get(url, headers={'User-Agent': '...'}, timeout=12, allow_redirects=True)
  title = re.search(r'<title[^>]*>(.*?)</title>', r.text, re.S|re.I)
  is_404 = (r.status_code == 404) or ("404 page not found" in (title or '').lower()) or ("can't seem to find the page" in r.text.lower()) or ("error code: 404" in r.text.lower())
  ```
- Beri delay 0.25–0.5s antar request untuk hindari rate limit.
- Kalau banyak link lama mati, jangan sekadar label dead: cari ulang fresh 50 dari search live, pilih 50 final, lalu update HTML dengan banner jelas `50/50 LIVE`.
- Jika user meminta jumlah besar dengan batas budget ketat (mis. “50 list max Rp8jt/bln” atau “mentok Rp15jt/bln”), **jangan memaksakan/fake jumlah**. Kumpulkan listing verified yang benar-benar memenuhi filter terlebih dulu, lalu jika jumlah kurang: (1) laporkan count sementara, (2) perluas sumber/area hanya dengan label jelas (`Sanur inti`, `Denpasar Selatan dekat Sanur`, `melebar/perlu cek map`, `lead perlu nego`), dan (3) bedakan `listing verified` vs `lead/search candidate` di HTML.
- Untuk long-stay dashboards dengan campuran tingkat kepastian, gunakan taxonomy status eksplisit, bukan satu klaim “verified”: `PRICE-LIVE` = harga monthly tampil dan masuk budget; `LEAD-CHECK` = link direct/OTA/target hidup tapi harga bulanan harus dinego/konfirmasi; optional `FAR-FALLBACK` atau badge lokasi merah = masih valid sebagai fallback budget, tapi di luar area inti. Summary cards wajib memecah jumlah per status (contoh “27 price-live, 23 lead-check”), jangan mengesankan semua 50 sama-sama memenuhi harga+lokasi dengan kepastian sama.

### 3. Location Classification — Jangan Percaya Search Label
- Airbnb search area name (`"Nusa Dua"`) **tidak menjamin** listing di pantai.
- Contoh: listing "Casa Nakoa 2BR Private Pool" muncul di search Nusa Dua tapi map-nya Banjar Mumbul (inland, bukan beachfront).
- Cara klasifikasi konservatif:
  - Keywords bahaya: `ungasan`, `uluwatu`, `pecatu`, `gwk`, `balangan`, `dreamland`, `banjar mumbul`, `south kuta`
  - Keywords baik: `beachside`, `near beach`, `oceanfront`, `on the water`, `private beach`, `waterfront`
  - Sanur: umumnya aman untuk pantai tenang, tapi tetap cek walkability
- Tambah kolom **"Jarak Pantai"** dengan badge warna: 🟢 DEKAT / 🔵 AMAN AREA / 🟡 PERLU CEK MAP / 🔴 JAUH

### 4. HTML Dashboard Structure
- Tabel dengan kolom: Area, Listing, Harga, Est. IDR, Rating, **Jarak Pantai** (wajib), Catatan, Link
- Untuk **monthly/long-stay dashboard**, tambah kolom: `Sumber`, `Estimasi/Bulan`, `Cocok 1 Bulan?` (kitchen/wifi/desk/pool/akses dapur), dan filter budget bulanan praktis (mis. ≤Rp5jt, ≤Rp8jt, ≤Rp12jt, ≤Rp15jt, ≤Rp25jt).
- Filterable/sortable via JavaScript (tambah data-attribute pada `<tr>`, terutama `data-price`, `data-source`, `data-status`)
- Cache-buster: perlu parameter `?v=<version>` biar user lihat update terbaru
- Section terpisah: Hotel (verified) vs Airbnb (manual-check)
- Ringkasan metrik (jumlah per status) di atas tabel; untuk link verified pakai format tegas seperti `30/30 LIVE` setelah dead/blocked links diganti, bukan dibiarkan sebagai catatan kecil.

### 5. Publish & Cache Buster
- HTML bisa di-publish di `/var/www/html/<subfolder>/`
- Basic Auth bisa dinonaktifkan per path dengan:
  ```
  location ^~ /audit-hotel-bali-ai-comparison/ {
      auth_basic off;
      try_files $uri $uri/ =404;
  }
  ```
- Jika path baru kena `401` dan tidak perlu mengubah/reload nginx saat itu, publish sebagai subfolder di bawah path yang sudah public-whitelisted (contoh `/var/www/html/audit-hotel-bali-ai-comparison/<new-dashboard>/`) lalu verifikasi URL public HTTP 200.
- Beri user link dengan `?v=` parameter untuk cache-busting jika kolom baru tidak muncul

## Pitfalls
- ❌ Jangan publish link Airbnb tanpa test 404 — banyak room ID stale dari scraping.
- ❌ Jangan klaim klasifikasi lokasi dari search area — listing bisa melebar ke inland/cliff area.
- ❌ Jangan lupa cache-buster — user browser bisa nampilin versi lama.
- ❌ Jangan hapus Basic Auth global — hanya disable per path yang perlu publik; kalau tidak mau reload nginx, taruh dashboard di subfolder path yang sudah public.
- ❌ Jangan panggil Airbnb dengan automated browser tanpa residential proxy — bot detection sangat agresif.
- ❌ Jangan percaya domain hotel/guesthouse lama hanya karena terlihat seperti official; beberapa domain akomodasi lokal bisa expired, DNS mati, cert invalid, atau berubah jadi spam/blog. Jika direct link gagal, ganti kandidat atau pakai halaman OTA/info yang live, dan tulis `harga perlu nego/cek`.
- ❌ Jangan klaim `30/30 live` kalau masih ada `CHECK`/dead rows di HTML. Grep final HTML untuk `CHECK`, `404`, atau dead label sebelum final.

## Verification
- [ ] Semua link Airbnb di-test: count `is_404 == True` vs `False`
- [ ] Column "Jarak Pantai" ada di thead
- [ ] Deadline/mati link punya label visual (❌ LINK MATI / 404)
- [ ] Setiap baris punya `data-link-status="live|dead"` attribute
- [ ] Public URL return HTTP 200 bukan 401
- [ ] Bukti screenshot dari user bahwa kolom baru terlihat (minta hard refresh jika perlu)

## References
- `references/airbnb-link-patterns.md` — pola room ID vs photo ID
- `references/monthly-stay-dashboard-notes.md` — pola dashboard long-stay 30 hari, kolom khusus monthly, fallback publish saat Basic Auth, dan verifikasi final
- `references/sanur-monthly-budget-research.md` — notes khusus Sanur/Denpasar Selatan monthly stay: cap Rp15jt ≈ price_max 1305 SGD, taxonomy `PRICE-LIVE` vs `LEAD-CHECK`, dan label area melebar
