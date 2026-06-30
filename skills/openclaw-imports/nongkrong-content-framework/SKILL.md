---
name: nongkrong-content-framework
description: Framework induk Nongkrong + CAVAC untuk strategi dan produksi konten iklan: domain, CEP, advertised value, Product POV, angle, hook, kemasan, HABOC, AeP mass production, dan Excel final.
version: 1.1.0
author: Akbar + Hermest
license: Proprietary
---

# Nongkrong Content Framework — Induk CAVAC

Gunakan skill ini saat user ingin menyusun strategi dan produksi konten iklan dari nol sampai siap jadi script/ad copy/Excel.

Skill ini adalah **induk** untuk CAVAC content strategy. Jangan load `cavac-content-strategy` lagi; gunakan skill ini. Untuk membedah iklan existing, pakai `cavac-ads-analyzer`.

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
- Fokus pada **situasi/CEP**, bukan funnel cold/warm/BOFU.
- CAVAC = `CEP × Advertised Value × Angle = Konten`.
- CEP dan value dikerjakan **iteratif**, bukan linear.
- Brand baru entry market wajib pakai **Product POV + Concrete Value**.
- OFFER dan CTA ditetapkan sekali lalu konsisten di variasi.
- Untuk produksi massal, ubah Hook + Story; Offer + CTA tetap.

---

## Prinsip CAVAC yang Wajib Dijaga

### Product POV vs Audience POV

**Product POV**:
- Subjek = produk.
- Ceritakan elemen produk → fungsi → dampak.
- Contoh: kandungan, bahan, fitur teknis, jahitan, proses, packaging, durabilitas.
- Wajib untuk brand baru.

**Audience POV**:
- Subjek = konsumen.
- Bicara emosi, status, aspirasi, identitas.
- Boleh untuk brand established, tapi concrete value tetap jalan.

Aturan:
- Baru entry market → **Product POV + Concrete Value**.
- Established → boleh mix aspirational, tapi jangan mengganti concrete value.
- Jangan bikin Vanity Value: narasi keren tanpa fondasi produk kuat.

### Kenapa Product POV dulu?
1. Sosmed sudah penuh insecurity; ngomongin produk memberi jarak sehat.
2. Brand baru belum punya konteks; audience perlu tahu produknya apa.
3. Concrete value menciptakan light buyers pertama.

Case study ringkas:
- Audience POV aspirational: ATC tinggi, IC rendah, purchase rendah, CPP ±Rp3,3 juta.
- Product POV concrete: IC naik, purchase naik, CPP turun ±Rp64 ribu.
- Pelajaran: ganti landing page tanpa ganti value/angle tidak cukup.

---

## CEP Framework

### 6 tipe CEP
1. **Problem-Solution** — urgent, terbesar, keputusan cepat.
2. **Routine** — habitual, luas, butuh frekuensi.
3. **Opportunistic** — trigger eksternal: promo, rekomendasi, tren.
4. **Commitment** — habit high-involvement: gym, diet, skincare routine.
5. **Aspirational** — wish/ideal, kecil untuk entry awal.
6. **Emotional** — mood-driven, paling kecil; hindari sebagai entry pertama.

Prioritas entry:
```text
Problem-Solution → Routine → Opportunistic → Commitment → Aspirational → Emotional
```

### W's Framework untuk memperdalam CEP
Gunakan untuk membuat CEP lebih spesifik:
- When — kapan terjadi?
- Where — di mana?
- With Whom — bersama siapa?
- How Feeling — perasaan apa?
- While — sedang apa?
- With What — menggunakan/bersama apa?

### Dual CEP
Gunakan dua level:
- **General CEP**: umbrella situasi luas.
- **Specific CEP**: turunan tajam dari W's Framework.

Contoh:
- General: saat jerawat muncul mendadak.
- Specific: saat jerawat muncul sebelum acara penting.

---

## Advertised Value Framework

### 3 level value

#### 1. Concrete Value — fondasi wajib
Value yang menempel langsung pada produk:
- kandungan/bahan aktif
- fitur teknis
- hasil terukur
- build quality
- packaging
- material
- proses pembuatan
- kenyamanan/durabilitas

Cara menyampaikan:
```text
Elemen produk → fungsi elemen → dampak bagi situasi CEP
```

#### 2. Aspirational Value — setelah established
Value emosi/status/identitas. Hanya boleh jika concrete value sudah kuat dan tetap berjalan.

#### 3. Uncharted Value — advanced
Brand menjadi gerakan/filosofi lebih besar dari produk. Jangan dipakai untuk entry awal.

### Vanity Value Warning
Jika brand langsung bicara lifestyle/status tanpa concrete value:
- terlihat keren di awal
- tapi runtuh saat review/pengalaman produk tidak mendukung
- customer sadar produk biasa saja

---

## 12 Angle CAVAC
1. Ilmiah / Factual
2. Emosional / Motivasional
3. Relatable / Humor
4. Eksklusivitas / Status
5. FOMO / Scarcity
6. Sosial / Community
7. Testimoni / Proof
8. Zero to Hero / Storytelling
9. Ekspektasi vs Realita / Before-After
10. Reverse Psychology
11. Challenge / Eksperimen
12. Edukasi

Untuk brand baru, prioritaskan:
```text
Ilmiah, Edukasi, Testimoni, Before-After, Reverse Psychology
```

Hindari dulu:
```text
Emosional standalone, Status standalone, Aspirational heavy
```

---

## Depth Before Breadth

Jangan maruk banyak CEP di awal.

Urutan benar:
1. Pilih 1 CEP besar.
2. Pilih 1 advertised value kuat.
3. Garap 4–7 angle dalam CEP itu.
4. Buat beberapa konten per angle.
5. Baru tambah CEP/value setelah yang pertama mature.

Analogi: lebih baik satu sumur digali dalam sampai keluar air daripada 10 sumur dangkal.

---

# Alur Kerja

## Langkah awal — minta input produk
Selalu mulai dengan:

> Deskripsikan produkmu secara spesifik — apa produknya, untuk siapa, dan apa yang ditawarkan?

Simpan sebagai **[DESKRIPSI PRODUK]**.

---

## PART 1 — RISET & ANALISA

### Langkah 1 — Riset domain produk
Tujuan: memetakan domain tempat produk bisa bertarung.

Prompt:
```text
Saya menjual [DESKRIPSI PRODUK].

Jangan berpikir seperti marketer konvensional yang mencari siapa target market dari produk ini. Berpikirlah: produk ini potensial dan relevan bertarung di domain mana saja?

Petakan kemungkinan produk saya bisa bermain di domain berikut:
1. Kesehatan  2. Parenting  3. Finansial  4. Relationship
5. Pendidikan  6. Karir  7. Spiritualitas  8. Kecantikan

Untuk setiap domain tentukan:
- Relevan / opsional / tidak relevan
- Peran produk: alternatif, pelengkap, atau substitusi
- Problem besar yang bisa disentuh

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

Wajib arahkan comment mining:
- cari iklan kompetitor di Meta Ads Library/feed/Reels
- baca komentar panjang/emosional
- catat situasi spesifik yang disebutkan
- catat bahasa natural pasar
- jika komentar banyak dan konsisten, anggap itu sinyal CEP valid

### Langkah 3 — Petakan situasi / CEP
Tujuan: mencari kondisi massal dan berulang yang memicu pembelian.

Prompt:
```text
Dari domain dan problem yang sudah kita petakan, sekarang petakan situasi-situasi spesifik yang membuat seseorang mulai merasakan masalah itu secara aktif.

Pakai 6 tipe CEP:
1. Problem-Solution
2. Routine
3. Opportunistic
4. Commitment
5. Aspirational
6. Emotional

Untuk tiap situasi, perdalam dengan W's Framework:
When, Where, With Whom, How Feeling, While, With What.

Yang dicari bukan momen satu kali, tapi situasi yang:
- Massal: dialami banyak orang
- Frequent: terjadi berulang
- Urgent: cukup mendesak untuk memicu aksi

Jangan gunakan funnel cold/warm/BOFU atau segmentasi psikografis.

Buat tabel:
1. CEP type
2. General CEP
3. Specific CEP
4. Frekuensi
5. Skala
6. Urgensi
7. Bahasa natural IG
8. Catatan validasi comment mining
```

Lalu minta user validasi dan pilih 1 CEP paling kuat.

### Langkah 4 — Definisikan advertised value
Prompt:
```text
Dari tabel situasi tadi, saya memilih CEP ini:
[TEMPEL CEP YANG DIPILIH]

Bantu saya merumuskan advertised value yang tepat.

Advertised value harus:
- Menjawab langsung kondisi yang dialami di CEP tersebut
- Berbasis concrete value / elemen produk
- Disampaikan dari Product POV jika brand baru entry market
- Spesifik dan masuk akal, bukan klaim berlebihan

Gali semua elemen tangible produk:
- bahan/kandungan
- fitur teknis
- packaging
- proses pembuatan
- durabilitas
- kenyamanan
- hasil terukur

Berikan 3 opsi advertised value, lalu rekomendasikan yang terkuat.
Format: elemen produk → fungsi → dampak pada CEP.
```

Tunggu konfirmasi user sebelum lanjut.

### Langkah 5 — Buat angle & inti pesan
Gunakan 12 angle CAVAC dan hasilkan tabel:
```text
No | Angle | Product POV/Audience POV | Inti Pesan | Format yang cocok
```

Aturan:
- Untuk brand baru, mayoritas harus Product POV.
- Mulai dengan 4–7 angle, bukan semua sekaligus.
- Rekomendasikan 1–3 angle terkuat untuk batch awal.

Setelah Part 1 selesai, minta user membawa konteks:
- domain
- CEP terpilih
- advertised value
- angle + inti pesan
- bahasa natural dari comment mining

---

## PART 2 — PRODUKSI KONTEN

### Langkah 6 — Pilih hook
Gunakan 12 formula hook resmi framework. Pilih 5 paling relevan dan tulis hook maksimal 10 kata.

Hook harus mengkomunikasikan:
```text
CEP + advertised value + angle
```

### Langkah 6.5 — Tentukan kemasan
Tanya user:
- format video: talking head / text motion / before-after / UGC / carousel
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
- untuk brand baru: script tetap Product POV dominan

Tunggu user memilih atau revisi.

### Langkah 8 — Produksi final ke Excel
Jika user setuju, buat file `.xlsx` dengan kolom:
```text
No | CEP | Value | Angle | Inti Pesan | Hook | Agitate | Bridge | Offer | CTA | Primary Text | Headline | Format | Durasi | Distribusi
```

Isi berdasarkan variasi yang disetujui dan kemasan batch 1.

---

## MODE CEPAT — AeP 5-Fase Workflow

Gunakan saat user bilang: “bikin iklan massal”, “workflow cepat”, “AeP”, “langsung produksi”, “butuh banyak konten sekarang”.

Filosofi AeP:
> Winning di Meta Ads bukan soal setting iklan atau produk sempurna, tapi menemukan PESAN yang resonan, lalu mengeksploitasi pesan itu lewat variasi konten.

### Fase 1 — Market Territory Mapping
1. Tentukan domain.
2. Petakan kategori masalah.
3. Identifikasi CEP.
4. Pilih CEP frequent + massal + urgent.

### Fase 2 — Message Design
1. Tentukan advertised value.
2. Petakan angle dan inti pesan.
3. Buat struktur Hook → Story → Offer → CTA.
4. Yang berubah di variasi: Hook + Story. Offer + CTA tetap.

### Fase 3 — Hook Engineering
1. Kumpulkan hook winning dari market.
2. Ekstrak formula/pattern.
3. Generate 10–12 variasi hook berbasis formula, bukan hook AI generik.

### Fase 4 — Mass Production Planning
1. Rencanakan footage/B-roll/sound/template.
2. Buat 1 template master.
3. Ganti hook + footage per variasi.
4. Target format utama: Reels.

### Fase 5 — Testing & Scale
1. Jalankan variasi budget rendah.
2. Evaluasi CPM masuk + view naik = market besar.
3. Scale dengan eksploitasi pesan winning, bukan cuma naik budget.
4. Jika CEP mentok, pindah CEP/domain baru.
5. Jaga AOV > CPA.

---

## Aturan eksekusi
- Jangan lompat langkah.
- Jangan pakai CTR/ROAS/funnel saat menjalankan framework ini, kecuali user khusus minta diagnosa performa.
- Jika user belum memilih output langkah sebelumnya, berhenti dan minta keputusan.
- Jika user ingin analisa iklan existing, arahkan ke `cavac-ads-analyzer`.
- Jangan load `cavac-content-strategy`; skill itu sudah di-merge ke sini.

## Support Files
- `cavac-content-strategy` lama sudah digabung ke skill ini.
- Jika butuh hook bank/script winning, cek apakah ada file `references/winning-script-framework.md` di repo skill.

## Referensi teori
- Byron Sharp — Category Entry Points, Mental Availability.
- Jenni Romaniuk — W's Framework.
- Brand Repertoire — setiap CEP memanggil repertoire brand berbeda.
- MECE Principle — 6 tipe CEP.
- Meta Advertising Best Practices — untuk brand baru, angkat produk dulu.
- Army / Nongkrong — CAVAC Model, 12 Angles, AeP workflow.
