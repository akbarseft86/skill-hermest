---
name: meta-ads-diagnostic
description: >
  Framework diagnostik untuk Meta Ads (Facebook/Instagram Ads) berdasarkan "Focus on Ads" dari
  Agan Khalid (kelaskonversi.com). Gunakan skill ini setiap kali user menyebut: iklan boncos,
  CPL mahal, ads tidak perform, cara baca metrics Meta Ads, diagnosa iklan Facebook, kenapa
  iklan saya rugi, CTR jelek, landing page tidak convert, ATC rendah, cost per lead naik,
  cara optimize Meta Ads, atau kapan harus kill iklan. Juga trigger saat user share screenshot
  dashboard FB Ads dan minta analisis, atau saat user bertanya "apa yang harus saya perbaiki"
  terkait iklan yang sedang berjalan. Bahkan jika user hanya bilang "iklan saya boncos" atau
  "tolong analisis ads saya", skill ini harus di-trigger.
---

# Meta Ads Diagnostic — Focus on Ads Framework

## Konsep Utama

Framework ini mengajarkan cara mendiagnosa iklan Meta Ads secara **berurutan** — seperti dokter yang memeriksa pasien dari gejala paling dasar dulu sebelum masuk ke pemeriksaan lanjutan.

**Prinsip kunci**: Jangan loncat-loncat. Kalau Bagan 1 belum beres, jangan perbaiki hal di Bagan 3. Setiap bagan harus "lulus" dulu sebelum lanjut ke bagan berikutnya.

Analogi: CTR Link Click itu seperti ranking anak SD — kalau dari kecilnya sudah bagus, kemungkinan besar masa depannya (profit) juga bagus. Bukan jaminan, tapi secara statistik mayoritas iklan yang profit punya CTR Link Click di atas 1%.

---

## Alur Diagnostik: 5 Bagan Berurutan

Baca `references/diagnostic-flow.md` untuk detail lengkap setiap bagan beserta parameter dan cara hitungnya.

### Quick Reference

| Bagan | Apa yang Dicek | Parameter Kunci | Jika Gagal, Perbaiki |
|-------|---------------|-----------------|----------------------|
| 1 | Iklan (CTR) | CTR Link Click ≥ 1% | Ad Image → Ad Copy |
| 2 | Speed Website | OC vs LP ≥ 65% | Speed/Loading Website |
| 3 | Copywriting Website | LP vs ATC ≥ 10% | Copywriting & Navigasi |
| 4 | Conversion to Lead | Cost per ATC ≤ Rp5.000 | Website + Form/WA flow |
| 5 | Closing | CR CS ≥ 50% | CS Performance |

---

## Cara Menggunakan Skill Ini

### Skenario 1: User bilang "iklan saya boncos"
Tanyakan data metrics secara berurutan mulai dari Bagan 1. Jangan langsung tanya semua sekaligus — diagnosis step by step.

Pertanyaan pertama: "Berapa CTR Link Click iklan Anda?"
- Jika < 1% → STOP. Masalahnya di iklan. Perbaiki Ad Image dulu, lalu Ad Copy. Belum perlu lihat yang lain.
- Jika ≥ 1% → Lanjut ke Bagan 2.

### Skenario 2: User share screenshot dashboard
Baca semua metrics yang terlihat, lalu diagnosa dari Bagan 1 ke bawah. Identifikasi di bagan mana "penyakit"-nya berada.

### Skenario 3: User tanya "apa yang harus saya perbaiki?"
Jalankan diagnostic flow dari awal. Jangan langsung suggest perbaikan random — ikuti urutan bagan.

---

## Quadrant Level (dari Agan Khalid)

| Level | Singkatan | Artinya |
|-------|-----------|---------|
| **BIBAT** | Bingung Hebatnya di Mana | Sudah profit tapi tidak tahu kenapa → tidak bisa mengulang keberhasilan |
| **BIGO** | Bingung Gobloknya di Mana | Boncos tapi tidak tahu kenapa → tidak tahu apa yang harus diperbaiki |
| **TAGO** | Tahu Gobloknya di Mana | Sudah tahu letak masalah → tinggal diperbaiki (ini target dari diagnostic) |
| **TABAT** | Tahu Hebatnya di Mana | Tahu kenapa berhasil → bisa mengulang & mendelegasikan |

**Goal dari skill ini**: Membawa user dari BIBAT/BIGO → TAGO → TABAT.

---

## Insight Penting dari Framework

1. **Urutan perbaikan itu krusial** — Jangan benerin CS kalau iklannya aja belum bagus. Jangan benerin copywriting website kalau speed-nya masih lambat.

2. **Iklan dengan CTR jelek di depan bisa tetap profit** — Tapi ini pengecualian, bukan aturan. Secara data, mayoritas iklan profit punya CTR Link Click ≥ 1%.

3. **Iklan dengan CTR bagus bisa tetap boncos** — Karena masalahnya bisa ada di speed website, copywriting, atau CS. Makanya harus cek semua bagan.

4. **Metrics yang saling mempengaruhi** — CTR rendah di depan akan membuat semua metrics di belakang makin mahal. Seperti efek domino.

5. **Sudah profit tapi metrics jelek = peluang** — Kalau sudah profit dengan speed jelek (< 60%), berarti kalau speed diperbaiki, profit akan semakin tebal.

6. **Jangan kill iklan yang "boncos" tanpa diagnosa** — Mungkin yang boncos itu bukan iklannya, tapi speed website atau copywriting-nya.

---

## Format Output Diagnostik

Saat memberikan hasil diagnosa ke user, gunakan format ini:

```
📊 HASIL DIAGNOSA META ADS
========================

Bagan 1 — Iklan (CTR)
├─ CTR All: [nilai]% → [✅/⚠️/❌] (parameter: ≥ 2%)
├─ CTR Link Click: [nilai]% → [✅/⚠️/❌] (parameter: ≥ 1%)
└─ Status: [LULUS/PERLU PERBAIKAN]
   └─ Action: [jika perlu perbaikan]

Bagan 2 — Speed Website
├─ Outbound Clicks: [nilai]
├─ Landing Page Views: [nilai]
├─ Rasio: [nilai]% → [✅/⚠️/❌] (parameter: ≥ 65%)
└─ Status: [LULUS/PERLU PERBAIKAN]
   └─ Action: [jika perlu perbaikan]

... (lanjut per bagan)

🎯 DIAGNOSA UTAMA
Masalah terletak di: [Bagan X - ...]
Yang harus diperbaiki: [...]
Prioritas: [...]
```
