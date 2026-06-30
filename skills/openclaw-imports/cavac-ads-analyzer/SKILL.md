---
name: cavac-ads-analyzer
description: Analisa iklan dengan framework CAVAC dari handout Nongkrong — fokus pada domain, situasi/CEP, advertised value, angle, hook, kemasan, HABOC, dan struktur ad copy.
version: 1.0.0
author: Akbar + Hermest
license: Proprietary
---

# CAVAC Ads Analyzer

Gunakan skill ini saat user ingin membedah iklan kompetitor atau iklan sendiri memakai framework CAVAC saja.

## Input yang diterima
1. **Teks**: script video, ad copy, caption, headline.
2. **Screenshot/gambar**: baca teks yang terlihat + deskripsi visualnya.
3. **Input parsial**: tetap analisa sejauh data tersedia, dan tandai bagian yang tidak bisa dianalisa.

## Larangan
- Jangan analisa CTR, ROAS, CPM, algoritma, atau metrik platform.
- Jangan kasih opini kreatif yang tidak grounded pada input.
- Jangan mengarang elemen yang tidak ada.

## Kerangka analisa CAVAC
Analisa selalu memakai urutan berikut.

### 1. Domain
Identifikasi domain kehidupan yang disasar:
- Kesehatan
- Parenting
- Finansial
- Relationship
- Pendidikan
- Karir
- Spiritualitas
- Kecantikan

### 2. Situasi / CEP
Identifikasi situasi spesifik sebagai titik masuk iklan.
Jika tidak spesifik, catat:
> Situasi tidak spesifik — iklan bermain di level masalah generik.

### 3. Advertised Value
Identifikasi janji transformasi, bukan fitur.
Format ideal:
> Dengan [produk], [hasil spesifik] tanpa [hambatan yang ditakuti].

Jika masih fitur, catat:
> Advertised value belum terkomunikasikan — iklan baru sampai di level fitur.

### 4. Angle & Inti Pesan
Identifikasi angle dari 12 pilihan Nongkrong, lalu ekstrak inti pesan.
Wajib evaluasi:
- apakah situasi disebut eksplisit?
- apakah advertised value disebut eksplisit?

### 5. Formula Hook
Identifikasi formula hook dari 12 formula hook resmi.
Kutip hook asli jika ada.
Nilai apakah efektif untuk 3 detik pertama.

### 6. Kemasan
Bedah 5 elemen:
- Teks
- Ilustrasi
- Warna
- Format
- Distribusi

Lalu nilai:
- apakah kemasan mendukung atau melemahkan pesan?
- apakah kemasan distinct?
- apa 1 variasi kemasan dari pesan yang sama?

### 7. Struktur Script HABOC
Breakdown menjadi:
- HOOK
- AGITATE
- BRIDGE
- OFFER
- CTA

Kalau tidak ada, tulis `Tidak ditemukan`.

### 8. Struktur Ad Copy
Jika ada primary text/headline, breakdown dengan alur:
- situasi
- realita
- insight
- solusi

## Format output wajib
Gunakan struktur ini:

```text
## ANALISA IKLAN — [nama produk / judul iklan jika ada]

━━━ TIGA KOMPONEN UTAMA ━━━

### 1. SITUASI / CEP
...
→ Kualitas: Spesifik / Generik / Tidak ada

### 2. ADVERTISED VALUE
...
→ Format ideal: "Dengan [produk], [hasil spesifik] tanpa [hambatan]"
→ Kualitas: Transformasi jelas / Masih di level fitur / Tidak ada

### 3. INTI PESAN
...
→ Apakah situasi disebut eksplisit? Ya / Tidak
→ Apakah advertised value disebut eksplisit? Ya / Tidak

━━━ EKSEKUSI KONTEN ━━━

### 4. Domain
...

### 5. Angle
...

### 6. Formula Hook
Hook: "..."
Formula: ...
→ Efektif di 3 detik pertama: Ya / Tidak — [alasan]

### 7. Kemasan
| Elemen     | Yang Digunakan |
|------------|-----------------|
| Teks       | ...             |
| Ilustrasi  | ...             |
| Warna      | ...             |
| Format     | ...             |
| Distribusi | ...             |

→ Kemasan distinct? Ya / Tidak
→ Variasi kemasan yang bisa dicoba: ...

### 8. Struktur Script HABOC
| Bagian   | Isi dari iklan ini |
|----------|---------------------|
| HOOK     | ...                 |
| AGITATE  | ...                 |
| BRIDGE   | ...                 |
| OFFER    | ...                 |
| CTA      | ...                 |

### 9. Ad Copy
Primary Text: ...
Headline: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━

### KESIMPULAN CAVAC
...
```

## Aturan kualitas
- Kesimpulan harus fokus pada: situasi, value, pesan, dan kemasan.
- Jika input screenshot, deskripsikan visual seperlunya sebelum masuk ke analisa.
- Jika hanya ada hook/headline tanpa body, analisa bagian yang ada dan tandai sisanya tidak tersedia.
- Jika user minta membuat konten baru setelah analisa, arahkan ke `nongkrong-content-framework`.
