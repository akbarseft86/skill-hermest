# Diagnostic Flow — Detail Setiap Bagan

Framework Focus on Ads dari Agan Khalid (kelaskonversi.com). Diagnosis dilakukan BERURUTAN dari Bagan 1 sampai 5. Jangan loncat.

---

## BAGAN 1: Cek Iklan — CTR All & CTR Link Click

**Apa yang dicek**: Apakah iklan cukup menarik sehingga orang mau klik?

### Metrics

**CTR All (Click-Through Rate All)**
- Definisi: Persentase orang yang melakukan engagement apapun terhadap iklan (like, comment, share, zoom, klik link, dll)
- Fungsi: "Lampu kuning" — indikator awal sebelum lihat CTR Link Click
- Parameter: **≥ 2%**

**CTR Link Click (Click-Through Rate Link Click)**
- Definisi: Persentase orang yang mengklik link di iklan dan keluar dari Facebook menuju website
- Fungsi: **METRIC PALING PENTING di Bagan 1** — ini yang utama
- Parameter: **≥ 1%**
- Contoh: CTR Link Click 1% = dari 1000 orang yang melihat iklan, 10 orang mengklik ke website

### Hubungan CTR All dan CTR Link Click
- CTR All itu satu step sebelum CTR Link Click
- Kalau CTR All saja tidak 2%, kemungkinan besar CTR Link Click juga tidak akan 1%
- Tapi yang PALING PENTING tetap CTR Link Click
- Ada pengecualian: CTR All < 2% tapi CTR Link Click > 1% → masih bisa dibiarin

### Parameter & Scoring

| Metric | Great 🟢 | Normal 🟡 | Jelek 🔴 |
|--------|----------|-----------|----------|
| CTR All | > 3% | ≥ 2% | < 2% |
| CTR Link Click | > 1.5% | ≥ 1% | < 1% |

### Jika GAGAL (CTR Link Click < 1%)

**STOP.** Jangan lanjut ke bagan lain. Yang harus diperbaiki:

1. **Ad Image (prioritas pertama)** — foto atau video iklan
   - Apakah visual menarik perhatian di newsfeed?
   - Apakah thumbnail video cukup eye-catching?
   - Apakah ada elemen yang membuat orang berhenti scroll?

2. **Ad Copy (prioritas kedua)** — teks/tulisan iklan
   - Apakah hook di baris pertama cukup kuat?
   - Apakah penawaran jelas?
   - Apakah ada CTA yang jelas?

Urutan: **Benerin Ad Image DULU, baru Ad Copy.** Ad Image punya porsi pengaruh lebih besar terhadap CTR.

### Catatan Penting
- 13 dari 18 iklan top performer Agan Khalid punya CTR Link Click ≥ 1%
- Ada 5 yang < 1% tapi tetap profit → pengecualian, bukan aturan
- Ada juga iklan CTR > 1% tapi tetap boncos → karena masalahnya di bagan lain
- Intinya: CTR bagus = fondasi kuat, tapi bukan jaminan profit sendirian

---

## BAGAN 2: Cek Speed Website — Outbound Clicks vs Landing Page Views

**Apa yang dicek**: Dari orang yang klik iklan, berapa yang benar-benar sampai melihat website (setelah loading selesai)?

### Metrics

**Outbound Clicks (OC)**
- Definisi: Jumlah real orang yang mengklik link keluar dari Facebook menuju website
- Ini JUMLAH orang, bukan persentase

**Landing Page Views (LP / LPV)**
- Definisi: Jumlah orang yang "merelakan hidupnya" untuk menunggu loading website selesai
- Selalu lebih kecil dari Outbound Clicks karena pasti ada yang "gugur di medan perang loading"

**Cost per Landing Page View (CPLPV)**
- Definisi: Biaya per orang yang sampai melihat website
- Ini metric cepat untuk mengecek tanpa hitung manual
- Parameter: **≤ Rp2.000**

### Cara Hitung Rasio
```
Rasio = Landing Page Views ÷ Outbound Clicks × 100%
```

Contoh: LP 16.771, OC 24.732 → 16.771 / 24.732 = 67.8%

### Parameter & Scoring

| Metric | Great 🟢 | Bagus 🟡 | Normal ⚪ | Jelek 🔴 |
|--------|----------|---------|----------|----------|
| Rasio OC vs LP | ≥ 70% | 65-69% | 60-64% | < 60% |
| Cost per LPV | < Rp500 | < Rp1.000 | Rp1.000-2.000 | > Rp2.000 |

Toleransi gugur yang bisa diterima: **30-35%** (artinya 65-70% yang selamat)

### Jika GAGAL (Rasio < 60% atau CPLPV > Rp2.000)

Yang harus diperbaiki: **SPEED WEBSITE**

Bukan copywriting. Bukan harga. Bukan CS. Murni speed/loading.

Yang termasuk dalam "speed":
- Loading time halaman
- Ukuran gambar/media yang terlalu besar
- Server response time
- Mobile responsiveness
- Redirect chains

**Insight**: Kalau sudah profit tapi rasio < 60%, berarti kalau speed diperbaiki, profit akan semakin tebal. Karena lebih banyak orang yang "selamat" sampai website.

---

## BAGAN 3: Cek Copywriting Website — Landing Page Views vs Add to Cart (ATC)

**Apa yang dicek**: Dari orang yang sampai di website, berapa yang tertarik untuk mengambil action (klik button beli/WA/form)?

### Metrics

**Landing Page Views (LP)**
- Jumlah orang yang sampai melihat website (dari Bagan 2)

**Website Add to Cart (ATC)**
- Definisi: Jumlah orang yang mengklik button action di website (beli, WhatsApp, mulai isi form, dll)
- "Add to Cart" di sini bukan hanya keranjang belanja — ini mewakili semua button CTA utama

### Cara Hitung
```
Rasio = ATC ÷ Landing Page Views × 100%
```

### Parameter & Scoring

| Metric | Bagus 🟢 | Normal 🟡 | Jelek 🔴 |
|--------|---------|----------|----------|
| LP vs ATC | > 15% | ≥ 10% | < 10% |

**10% adalah standar industri global** (parameter e-commerce dunia).

### Jika GAGAL (Rasio < 10%)

Yang harus diperbaiki (2 hal):

1. **Copywriting Sales Page (prioritas utama)**
   - Headline yang tidak compelling
   - Penjabaran manfaat kurang kuat
   - Tidak ada/kurang testimoni
   - Tidak ada urgency/scarcity
   - Penawaran tidak jelas
   - Kurang social proof

2. **Navigasi / User Interface**
   - Button tidak kelihatan atau warna kurang mencolok
   - Layout membingungkan
   - Terlalu banyak distraksi
   - User tidak tahu harus klik apa
   - Form terlalu panjang/ribet

**Catatan**: Di Bagan 3 ini BARU mulai bicara soal konten website. Di Bagan 1 & 2, masalahnya murni iklan dan teknis speed.

---

## BAGAN 4: Cek Conversion to Lead/Prospect

Bagan 4 ada **2 jalur** tergantung flow bisnis:

### Jalur A: WhatsApp / Direct Contact

Untuk bisnis yang button CTA-nya langsung ke WhatsApp/telepon/SMS.

**Metrics yang dicek**: Cost per ATC (Add to Cart)

| Metric | Great 🟢 | Normal 🟡 | Batas 🔴 |
|--------|----------|----------|----------|
| Cost per ATC | < Rp2.000 | Rp2.000-2.500 | > Rp5.000 |

Setelah ATC → langsung bandingkan jumlah WhatsApp masuk vs Closing (lanjut ke Bagan 5).

### Jalur B: Form / Add Payment Info (API)

Untuk bisnis yang menggunakan form (lead form, checkout form, registration).

**Metrics yang dicek**:
1. Cost per ATC
2. Cost per Add Payment Info (API) / Cost per Lead / Cost per Form Submit

| Metric | Great 🟢 | Normal 🟡 | Batas 🔴 |
|--------|----------|----------|----------|
| Cost per ATC | < Rp2.000 | Rp2.000-2.500 | > Rp5.000 |
| Cost per API/Lead | < Rp10.000-15.000 | Rp15.000-20.000 | > Rp25.000 |

### Jika Cost per ATC GAGAL (> Rp5.000)
Yang harus diperbaiki: Kembali ke website — copywriting, navigasi, dan keseluruhan user experience.

### Jika Cost per API GAGAL (> Rp25.000)
Yang harus diperbaiki: **Form + Navigasi**
- Form terlalu panjang?
- Field terlalu banyak?
- Proses checkout membingungkan?
- Ada friction yang tidak perlu?

---

## BAGAN 5: Cek Closing — Lead vs Sale

**Apa yang dicek**: Dari prospek yang masuk (WhatsApp/form), berapa yang akhirnya closing/beli?

### Parameter Conversion Rate CS

| CR CS | Rating |
|-------|--------|
| 75%+ | 🟢 Great / Awesome |
| 50% | 🟡 Normal / Bagus |
| 35% | ⚪ Batas minimal |
| < 35% | 🔴 Jelek — CS perlu diperbaiki |

### Jika GAGAL (CR < 35%)

Yang harus diperbaiki: **CS Performance**
- Kecepatan response
- Script follow-up
- Teknik closing
- Handling objection
- Follow-up timing

### Catatan
- Kalau semua Bagan 1-4 sudah lulus tapi masih boncos, kemungkinan besar masalahnya di sini — CS
- Kalau jumlah lead banyak tapi closing rendah, itu bukan masalah iklan — itu masalah CS
- Parameter 50% = 10 lead masuk, 5 closing. Ini angka yang realistis dan sustainable

---

## Ringkasan Alur Lengkap

```
IKLAN → [Bagan 1: CTR] → KLIK → [Bagan 2: Speed] → LOADING → [Bagan 3: Copywriting] → ATC
                                                                                          │
                                                                    ┌─────────────────────┤
                                                                    │                     │
                                                              [Jalur WA]           [Jalur Form]
                                                                    │                     │
                                                              [Bagan 5]          [Bagan 4: API]
                                                              Closing                     │
                                                                                    [Bagan 5]
                                                                                    Closing
```

**Yang diperbaiki per bagan:**
1. CTR jelek → **Ad Image & Ad Copy**
2. Speed jelek → **Loading/Speed Website**
3. ATC rendah → **Copywriting & Navigasi Website**
4. API/Lead mahal → **Form & Checkout Flow**
5. Closing rendah → **CS Performance & Follow-up**
