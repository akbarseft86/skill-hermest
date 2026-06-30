# Algoritma Lama vs Algoritma Baru Meta Ads

## Algoritma Lama: Heuristik (Social Graph)

### Cara Kerja
Berpikir linear: Jika A maka B. If-then rules.

**True Value Formula:**
```
True Value = Bid Value × Estimated Action Rate × Ad Quality
```

- **Bid Value**: Ditentukan sistem berdasarkan budget (discounted bid)
- **Estimated Action Rate**: CTR, Purchase Rate, ATC Rate, dll
- **Ad Quality**: Seberapa bagus engagement iklan

Iklan dengan True Value tertinggi yang menang dan ditayangkan.

### Audience = Person (Atribut Statis)
- Jenis kelamin, umur, lokasi, bahasa, device
- Interest (dari grup, page like, aktivitas)
- Behavior (purchase history, device usage)
- Dibangun dari **Social Graph** — struktur sosial user

**Problem:**
- Orang malas share data pribadi ke sosmed (beda dengan era 2016-2017)
- Data statis: join grup 3 tahun lalu tapi sudah tidak relevan
- Privacy concerns → Apple vs Facebook (iOS 14.5)
- Sulit scale — makin besar budget, makin susah cari audience yang tepat

### Ads = Kumpulan Fitur Terpisah
- Headline, gambar, text, deskripsi → dibaca terpisah
- Meta hanya melakukan scoring per fitur, bukan memahami makna keseluruhan
- "Kalau ada kata X + gambar Y → tayangkan ke segment Z" (heuristik)

### Optimisasi: Multi-arm Bandit
- Algoritma "judi" — coba beberapa iklan, lihat mana yang menang, fokuskan ke situ
- Iklan winning akan terus winning sampai fatigue
- Kalau sudah winning, deliver terus ke audience yang sama

### Kapan Masih Relevan
- Campaign non-ASC (non-Advantage Sales Campaign)
- Budget kecil (< Rp100rb/hari) dengan targeting spesifik
- Retargeting campaign (Custom Audience)
- Advertiser yang belum setup CAPI

---

## Algoritma Baru: AI Model (Interest/Intention Graph)

### Cara Kerja
Deliberate Practice: Ada feedback loop. Meta belajar dari kesalahan.

**Matching Value Formula:**
```
Matching Value = Semantic Intention × Semantic Content
```

Bukan lagi scoring tertinggi yang menang, tapi **yang paling match** yang menang.

### Audience = User Factor (Dinamis, Real-time)
Satu manusia bisa menjadi beberapa "user" tergantung intention saat itu:

```
Army Al Givari (1 orang) bisa jadi:
├── User_124: Pagi → lagi cari gamis/sorban → intention: fashion muslim
├── User_130: Siang → lagi lapar → intention: cari makanan
├── User_145: Sore → lagi stress → intention: self-reward
└── User_160: Malam → scrolling → intention: hiburan
```

**Data points per user: RIBUAN**
- Berapa lama scrolling
- Sedang searching apa di Tokopedia/Shopee
- Jam berapa biasa transaksi
- Device apa
- Pola behavior real-time
- Micro-behavior (scroll speed, pause duration, tap pattern)

**Implikasi**: Impression ≈ Reach ke intention yang berbeda. Satu orang dilihat 8x sehari bisa berarti 8 "user factor" yang berbeda.

### Ads = Konten Bermakna Utuh (Semantik)
- Headline + gambar + text + deskripsi → dibaca sebagai SATU KESATUAN makna
- Meta memahami iklan seperti manusia memahami iklan
- Variasi headline/deskripsi = Meta punya lebih banyak "ad factor" untuk di-match-kan
- Konten yang punya makna unik → lebih mudah di-match dengan intention yang tepat

**Kaitannya dengan CAVAC Model:**
- Satu produk bisa punya beberapa "semantic content" yang berbeda
- Setiap CEP × Angle = 1 semantic content yang unik
- Semakin banyak variasi semantic content → semakin banyak intention yang bisa di-match

### 3 Organ Utama AI Meta

1. **GEM (Generalized Embedding Model)**
   - Mengkonversi data audience → User Factor
   - Mengkonversi data ad → Ad Factor
   - "Penerjemah" data mentah ke unit yang bisa dicocokkan

2. **Andromeda**
   - Hardware custom Meta (bukan GPU standar)
   - Matching User Factor ↔ Ad Factor secara real-time (milidetik)
   - Tidak ada di TikTok atau Google — unique Meta technology
   - "Tangan" yang melakukan shortlist

3. **LETIS**
   - Decision engine final
   - Dari shortlist Andromeda → tentukan ad mana yang tayang
   - "Hakim" yang memutuskan

### Feedback Loop (Deliberate Practice)

```
Iklan deliver → User nggak suka → Meta catat "salah"
                                        ↓
            → Cari user lain yang mirip tapi beda → Deliver lagi
                                        ↓
            → User suka → Meta catat "benar" → Reinforcement
                                        ↓
            → Cari lebih banyak user seperti ini → Scale
```

**Implikasi penting:**
- Boncos di hari 1-3 = NORMAL (learning phase)
- Jangan kill terlalu cepat — beri waktu 3-7 hari (conversion window 7 hari)
- Semakin banyak data "salah" di awal → semakin akurat matching di depan
- Tapi kalau setelah 7 hari masih boncos terus → mungkin produk/konten yang perlu diperbaiki

### Kapan Dipakai
- Advantage Sales Campaign (ASC) / Advantage Shopping Campaign
- Budget yang mau di-scale
- Produk dengan multiple CEP dan banyak variasi konten
- Sudah setup Pixel + CAPI (signal terkuat)

---

## Transisi & Adaptasi

Algoritma lama TIDAK dihilangkan — dikembangkan dan diadaptasi. Prinsip-prinsip lama (True Value, Multi-arm Bandit) masih dipakai sebagai "thought experiment" dan cara berpikir kita saat mendesain konten.

Yang berubah:
- True Value → **Matching Value** (dari scoring ke matching)
- Social Graph → **Interest/Intention Graph** (dari siapa kamu ke apa maumu)
- Static targeting → **Dynamic matching** (real-time, per-intention)
- Data-dependent → **Signal-enhanced** (Pixel/CAPI sebagai top signal, bukan satu-satunya)

---

## Dampak Terhadap Budget & Scaling

| Budget | Audience yang Dijangkau | Karakteristik | Implikasi |
|--------|------------------------|---------------|-----------|
| Kecil (< 1jt/hari) | Heavy buyers, followers, warm audience | Mudah convert, CPL murah | "Diskon" dari Meta, slow growth tapi profitable |
| Sedang (1-10jt/hari) | Heavy + medium buyers | Campuran, CPL mulai naik | Butuh variasi konten lebih banyak |
| Besar (> 10jt/hari) | Semua termasuk cold/light buyers | Sulit convert, CPL mahal | Butuh funnel lengkap, banyak CEP, konten massive |

**Prinsip**: Budget kecil bukan kelemahan — justru mendapat "harga diskon" dari Meta. Slow creation, slow growth lebih sustainable untuk pemula.
