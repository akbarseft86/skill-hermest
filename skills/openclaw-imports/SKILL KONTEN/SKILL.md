---
name: meta-ads-algorithm-2025
description: >
  Panduan cara kerja algoritma Meta Ads 2025 (AI-based) berdasarkan materi Army Al Givari
  (kelaskonversi.com). Gunakan skill ini setiap kali user bertanya tentang: cara kerja algoritma
  Meta/Facebook Ads, kenapa iklan tidak terdeliver, perbedaan Advantage Sales Campaign vs campaign
  biasa, apa itu user factor, bagaimana Meta meranking iklan, kenapa budget besar malah boncos,
  learning phase Meta Ads, kapan harus pakai broad targeting vs detail targeting, apa pengaruh
  Pixel dan CAPI terhadap algoritma, atau kenapa iklan kadang bagus kadang jelek. Juga trigger
  saat user bingung kenapa performa iklan tidak konsisten, atau bertanya tentang strategi scaling
  budget. Bahkan jika user hanya bilang "kenapa iklan saya gak deliver" atau "apa bedanya ASC
  sama campaign biasa", skill ini harus di-trigger.
---

# Meta Ads Algorithm 2025 — Cara Meta Berpikir

## Konsep Fundamental

Meta Ads hari ini menggunakan **2 engine yang berbeda secara infrastruktur**:

1. **Engine Lama (Non-AI)** — Dipakai di campaign biasa (non-Advantage Sales Campaign). Hardware lama, algoritma heuristik.
2. **Engine Baru (AI-Based)** — Dipakai di **Advantage Sales Campaign (ASC)**. Hardware baru (Grace Hopper GPU), Deep Neural Network.

Ini bukan sekedar update fitur — ini **mesin yang berbeda**. Seperti mobil bensin vs mobil listrik. Keduanya bisa jalan, tapi cara kerjanya fundamental berbeda.

**Implikasi**: Kalau user bilang "cocok pakai yang lama" atau "nggak cocok pakai ASC", itu karena memang engine-nya berbeda. Bukan salah satu lebih baik — mereka bekerja dengan logika yang berbeda.

---

## Algoritma Lama vs Baru

Baca `references/algo-lama-vs-baru.md` untuk penjelasan detail.

### Quick Comparison

| Aspek | Algoritma Lama | Algoritma Baru (AI) |
|-------|---------------|---------------------|
| Cara berpikir | Heuristik (if-then, linear) | Deliberate Practice (feedback loop, learning) |
| Audience | Person (atribut statis) | **User Factor** (ribuan data points, real-time) |
| Ads | Kumpulan fitur terpisah | **Konten bermakna utuh** (semantik) |
| Scoring | True Value (Bid × Action Rate × Quality) | **Matching Value** (Intention × Content) |
| Targeting | Social Graph (siapa kamu) | **Interest/Intention Graph** (apa maumu sekarang) |
| Optimisasi | Logistic Regression + Multi-arm Bandit | Deep Neural Network (GEM + Andromeda + LETIS) |
| Data dependency | Sangat bergantung data sosial & atribut user | Real-time behavior + signal (Pixel/CAPI) |
| Scale | Sulit di-scale (data makin tipis di budget besar) | Lebih scalable (matching pool lebih besar) |

---

## Cara Menggunakan Skill Ini

### Skenario 1: User bertanya "kenapa iklan saya gak deliver / boncos?"
Cek dulu: pakai campaign apa? ASC atau biasa?
- Jika ASC → jelaskan dengan logika algoritma baru (matching, feedback loop, learning phase)
- Jika campaign biasa → jelaskan dengan logika heuristik (targeting, bidding, CTR)
- Referensikan juga skill Meta Ads Diagnostic untuk diagnosa metrics spesifik

### Skenario 2: User mau scaling budget
Jelaskan dinamika budget vs audience quality:
- Budget kecil → Meta deliver ke heavy buyers → mudah convert, CPL murah
- Budget besar → Meta mulai reach cold audience → butuh lebih banyak variasi konten & funnel
- Solusi scaling: perbanyak konten yang distinct + perluas CEP (referensikan CAVAC skill)

### Skenario 3: User bingung soal learning phase / performa tidak konsisten
Jelaskan konsep Feedback Loop:
- Boncos di awal = proses learning (bukan berarti gagal)
- Meta butuh data "salah" untuk menemukan yang "benar"
- Conversion window 7 hari penting
- Jangan kill terlalu cepat — beri waktu 3-7 hari untuk learning

### Skenario 4: User bertanya perbedaan ASC vs campaign biasa
Jelaskan bahwa ini beda mesin, bukan beda setting. Lalu jelaskan implikasinya terhadap cara bikin konten dan targeting.

---

## 3 Organ Utama AI Meta

Meta Ads AI punya 3 komponen utama yang bekerja bersama:

### 1. GEM (Generalized Embedding Model)
**Fungsi**: Mengkonversi semua data audience menjadi User Factor, dan semua data ads menjadi Ad Factor.
Seperti "penerjemah" yang mengubah data mentah menjadi unit yang bisa dicocokkan.

### 2. Andromeda
**Fungsi**: Mencocokkan (matching) User Factor dengan Ad Factor secara real-time dalam hitungan milidetik.
Meta membangun hardware custom sendiri untuk ini — tidak ada di TikTok atau Google.
Ini "tangan" yang melakukan shortlist: dari jutaan ads, mana yang cocok untuk user tertentu saat ini.

### 3. LETIS
**Fungsi**: Decision engine — menentukan ad mana yang akhirnya tayang di screen user.
Seperti "hakim" yang memutuskan dari shortlist Andromeda, mana yang benar-benar ditampilkan.

---

## Insight Kunci untuk Advertiser

### 1. Konten > Targeting
Di algoritma baru, **konten menentukan siapa yang melihat iklan**, bukan targeting manual. Meta membaca konten secara semantik dan mematch-kan dengan intention user. Kalau kontennya tentang "jerawat sebelum wedding", Meta akan cari user yang punya intention relevan — tanpa perlu kita set targeting manual.

### 2. Misleading = Bencana
Kalau konten visual tidak sesuai dengan pesan (misal: gambar suplemen tapi jualan fashion), algoritma Meta akan salah menilai konten → deliver ke audience yang salah → boncos. Relevansi harus dijaga untuk DUA audience: manusia yang melihat DAN algoritma Meta yang membaca.

### 3. Pixel & CAPI = Signal Terkuat
Walaupun bukan satu-satunya data source, Pixel dan Conversion API tetap **top signal** untuk Meta. Data purchase/conversion real dari CAPI memberi feedback loop yang sangat kuat untuk AI Meta menemukan audience yang tepat.

### 4. Budget Kecil = Diskon dari Meta
Advertiser dengan budget kecil mendapat "diskon" karena Meta deliver ke heavy buyers yang mudah convert. Budget besar kehilangan "diskon" ini — harus reach cold audience yang lebih mahal untuk di-convert.

### 5. Satu Orang = Banyak User
Dalam algoritma baru, satu manusia bisa menjadi beberapa "user factor" tergantung intention-nya. Pagi lagi cari kopi = user A, siang lagi cari baju = user B, malam self-reward = user C. Ini yang membuat impression di Meta bisa jadi sebenarnya "reach" ke intention yang berbeda.
