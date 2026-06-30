---
name: nongkrong-content-framework
description: Framework 8 langkah dari riset domain sampai script/Excel untuk produksi konten iklan berbasis situasi, advertised value, angle, hook, kemasan, dan HABOC.
version: 1.0.0
author: Akbar + Hermest
license: Proprietary
---

# Nongkrong Content Framework

Gunakan skill ini saat user ingin menyusun strategi dan produksi konten iklan dari nol sampai siap jadi script/ad copy/Excel.

## Tujuan
Mengubah deskripsi produk menjadi:
- domain yang tepat
- situasi/CEP yang valid
- advertised value
- angle & inti pesan
- hook
- kemasan
- script HABOC
- ad copy
- file Excel final

## Prinsip utama
- Jalankan **berurutan**.
- **Tunggu keputusan user** di setiap titik keputusan sebelum lanjut.
- Fokus pada **situasi**, bukan segmentasi funnel/cold-warm audience.
- Lakukan **validasi CEP** sebelum produksi konten.
- Gunakan **comment mining** sebagai sumber bahasa natural dan situasi nyata.
- OFFER dan CTA ditetapkan sekali lalu dipakai konsisten di variasi.
- Part 1 dan Part 2 dijalankan terpisah bila perlu.

## Alur kerja

### Langkah awal — minta input produk
Selalu mulai dengan pertanyaan ini:

> Deskripsikan produkmu secara spesifik — apa produknya, untuk siapa, dan apa yang ditawarkan?

Simpan sebagai **[DESKRIPSI PRODUK]**.

---

## PART 1 — RISET & ANALISA

### Langkah 1 — Riset domain produk
Tujuan: memetakan domain tempat produk bisa bertarung.

Prompt:

```text
Saya menjual [DESKRIPSI PRODUK].

Jangan berpikir seperti marketer konvensional yang mencari siapa
target market dari produk ini. Tapi berpikirlah: produk ini potensial
dan relevan bertarung di domain mana saja?

Petakan kemungkinan produk saya bisa bermain di domain berikut:
1. Kesehatan  2. Parenting  3. Finansial  4. Relationship
5. Pendidikan  6. Karir  7. Spiritualitas  8. Kecantikan

Untuk setiap domain tentukan:
- Relevan / opsional / tidak relevan
- Peran produk: alternatif, pelengkap, atau substitusi

Buat output dalam bentuk tabel.
```

Setelah keluar, tanya:
> Domain mana yang mau difokuskan untuk langkah berikutnya?

### Langkah 2 — Riset brand, produk, influencer, dan comment mining
Tujuan: memahami lanskap pesaing dan celah diferensiasi.

Prompt:

```text
Dari hasil riset domain tadi, saya memilih domain [DOMAIN YANG DIPILIH].

Sekarang risetkan siapa saja yang sudah bermain di domain tersebut.

Cakup dua kategori:
1. Brand atau produk yang aktif berjualan di domain ini
2. Influencer atau kreator konten yang bermain di kategori ini

Untuk setiap nama, analisa:
- Problem spesifik apa yang mereka sasar
- Value atau pesan utama yang mereka tawarkan
- Catatan singkat: apa yang bisa jadi diferensiasi untuk produk saya

Buat output dalam bentuk tabel.
```

Lalu wajib arahkan user melakukan comment mining:
- cari iklan kompetitor di Meta Ads Library/feed/Reels
- baca komentar panjang/emosional
- catat situasi spesifik yang disebutkan
- catat bahasa natural pasar
- jika komentar banyak dan konsisten, anggap itu CEP valid

### Langkah 3 — Petakan situasi / CEP
Tujuan: mencari kondisi massal dan berulang yang memicu pembelian.

Prompt:

```text
Dari domain dan problem yang sudah kita petakan, sekarang petakan
situasi-situasi spesifik yang membuat seseorang mulai merasakan
masalah itu secara aktif.

Yang saya cari bukan momen satu kali — tapi situasi yang:
- Massal: dialami banyak orang
- Frequent: terjadi berulang, bukan sekali seumur hidup

Jangan gunakan konsep funnel, cold/warm audience, atau segmentasi
psikografis dalam analisa ini.

Buat dalam bentuk tabel dengan kolom:
1. Situasi — deskripsi singkat kondisinya
2. Frekuensi — harian / mingguan / bulanan
3. Skala — perkiraan seberapa banyak orang yang mengalami
4. Bahasa natural IG — 2-3 frasa yang dipakai orang biasa
   saat ngomongin situasi ini di konten atau caption IG.
   Bukan hashtag — tapi cara mereka ngomong secara natural.
```

Lalu minta user validasi di Meta Ads Library dan pilih 1 situasi paling kuat.

### Langkah 4 — Definisikan advertised value
Prompt:

```text
Dari tabel situasi tadi, saya memilih situasi ini:
[TEMPEL SITUASI YANG DIPILIH]

Bantu saya merumuskan advertised value yang tepat.

Advertised value harus:
- Menjawab langsung kondisi yang dialami di situasi tersebut
- Berbentuk janji transformasi, bukan sekadar fitur produk
- Spesifik dan masuk akal — bukan klaim berlebihan

Berikan 3 opsi advertised value, lalu rekomendasikan yang terkuat
beserta alasannya.
```

Tunggu konfirmasi user sebelum lanjut.

### Langkah 5 — Buat angle & inti pesan
Gunakan 12 angle resmi framework dan hasilkan tabel `No | Angle | Inti Pesan`, lalu rekomendasikan 1 angle terkuat. Tunggu persetujuan user.

Sudut pandang yang dipakai:
1. Ilmiah / Factual
2. Emosional / Motivasional
3. Relatable / Humor
4. Eksklusivitas / Status
5. FOMO / Scarcity
6. Sosial
7. Testimoni / Proof
8. Eksperimen & Challenge
9. Zero to Hero
10. Ekspektasi vs Realita
11. Sustainability / Green
12. Reverse Psychology

Setelah Part 1 selesai, minta user membuka sesi baru atau lanjut dengan membawa konteks:
- situasi yang dipilih
- advertised value
- angle + inti pesan
- catatan bahasa natural dari comment mining

---

## PART 2 — PRODUKSI KONTEN

### Langkah 6 — Pilih hook
Gunakan 12 formula hook resmi framework. Pilih 5 paling relevan dan tulis hook sesuai rumus, maksimal 10 kata, dengan fungsi mengkomunikasikan inti pesan.

### Langkah 6.5 — Tentukan kemasan
Tanya user:
- format video: talking head / text motion / before-after
- durasi target: testing 15–20 detik atau reach <15 detik
- distribusi utama: Reels / Feed / Story

Simpan sebagai **[KEMASAN BATCH 1]**.

### Langkah 7 — Script & ad copy
Buat 3 paket konten dengan struktur:
- SCRIPT: HOOK / AGITATE / BRIDGE / OFFER / CTA
- AD COPY: Primary Text + Headline

Aturan:
- total script maks 60 kata
- hook dirancang untuk 3 detik pertama
- OFFER dan CTA konsisten di semua variasi
- primary text maksimal 70 kata
- headline 5–7 kata, solutif

Tunggu user memilih atau revisi.

### Langkah 8 — Produksi final ke Excel
Jika user setuju, buat file `.xlsx` dengan kolom:
`No | Angle | Inti Pesan | Hook | Agitate | Bridge | Offer | CTA | Primary Text | Headline | Format | Durasi | Distribusi`

Isi berdasarkan variasi yang disetujui dan kemasan batch 1.

## Aturan eksekusi
- Jangan lompat langkah.
- Jangan pakai CTR/ROAS/funnel saat menjalankan framework ini.
- Jika user belum memilih output langkah sebelumnya, berhenti dan minta keputusan.
- Jika user ingin analisa iklan, arahkan ke skill `cavac-ads-analyzer`.
