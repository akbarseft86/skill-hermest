---
name: output-style-clarify
description: Use when user requests format-sensitive output (script, copy, ads, caption, email, brief, hook, headline). Ask 3 quick clarifying questions before executing to ensure output matches intent. Skip if user already specified tone/audience/channel in prompt.
version: 1.0.0
author: Hermest
license: MIT
metadata:
  hermes:
    tags: [copywriting, clarify, output-style, ads, script, content]
    related_skills: [hormozi-indo-writing-style, research-to-relief, cavac-content-strategy]
---

# Output Style Clarify

## Overview

Sebelum mengeksekusi tugas yang outputnya format-sensitive, tanya 3 hal singkat ke user. Tujuan: output langsung tepat sasaran tanpa revisi bolak-balik.

## Trigger Words

Aktif kalau user menyebut salah satu kata ini:

- `script`, `skrip`
- `copy`, `copywriting`
- `caption`, `caption iklan`
- `ads`, `iklan`
- `email`, `newsletter`
- `brief`, `briefing`
- `hook`, `headline`, `judul`
- `carousel`, `thread`
- `post`, `konten`
- `video ads`, `reels`, `tiktok`

## Skip Kondisi

Langsung eksekusi tanpa tanya kalau user sudah menyebut **format + channel** di prompt.

Contoh skip: *"bikin script video ads 30s"* → format (script) + channel (video ads 30s) sudah jelas, langsung eksekusi pakai rekomendasi tone + audience.

## Yang Ditanya ke User (HANYA 2 hal)

Sebelum eksekusi, tanya dalam satu blok:

```
Sebelum mulai, 2 hal cepat:

1. **Format:** script / copy / caption / carousel / email / brief / hook / headline?
2. **Channel:** video ads 30s / 60s / reels / tiktok / IG feed / WA broadcast / email / landing page?
```

## Yang TIDAK Ditanya — Saya Rekomendasikan + Tulis Referensinya

User minta saya yang putuskan + tulis referensi dulu sebelum eksekusi. Jadi sebelum produce output, **tampilkan dulu rekomendasi tone + audience dalam blok ringkas**, baru lanjut eksekusi di pesan yang sama.

Template rekomendasi:

```
**Rekomendasi saya:**

- **Audience:** [cold / warm / internal] — alasan: [1 kalimat]
- **Tone:** [caveman lite / tengah / normal panjang] — alasan: [1 kalimat]

Lanjut eksekusi dengan setup di atas. Kalau mau ganti, bilang aja.
```

Baru di bawah itu output script/copy nya.

## Decision Rules (cara saya pilih audience + tone)

### Audience — pilih berdasarkan channel + sinyal produk

| Channel | Default audience |
|---|---|
| Video ads (FB/IG/TikTok ads) | **Cold** — belum kenal produk |
| Organic reels / TikTok | **Cold** — discovery feed |
| IG feed / carousel organik | **Warm** — follower existing |
| Email blast | **Warm** — sudah ada di list |
| Email nurture sequence | **Warm** |
| WA broadcast | **Warm** — sudah opt-in |
| Landing page | **Cold** — datang dari ads |
| Sales page | **Warm** — datang dari email/nurture |
| Internal brief / SOP | **Internal** |

### Tone — pilih berdasarkan channel + durasi/panjang

| Channel | Default tone |
|---|---|
| Video ads ≤30s | **Caveman lite** — detik berharga |
| Video ads 60s | **Tengah** — masih perlu padat tapi ada nafas |
| Reels/TikTok organik | **Tengah** — natural conversational |
| Hook / headline / push notif | **Caveman lite** — punchy |
| Caption IG | **Tengah** |
| Carousel slide | **Caveman lite** untuk judul, **tengah** untuk body |
| Email subject line | **Caveman lite** |
| Email body | **Normal panjang** — orang siap baca |
| Landing page hero | **Caveman lite** |
| Landing page body | **Tengah** |
| Sales page | **Normal panjang** |
| Brief internal | **Tengah** |

### Override Triggers

Tetap pakai rule di atas, kecuali user kasih sinyal:

- Sebut **"hangat"**, **"empati"**, **"storytelling"** → naikkan ke tone yang lebih panjang/natural
- Sebut **"punchy"**, **"to the point"**, **"hard sell"** → turunkan ke caveman lite
- Sebut nama follower/customer existing → audience jadi warm
- Sebut "buat yang belum kenal" → audience jadi cold

## Flow Eksekusi

1. Deteksi trigger word di prompt user
2. Cek skip kondisi — kalau format + channel sudah jelas, langsung ke step 4
3. Kalau belum jelas, tanya 2 hal (format + channel) dalam 1 blok
4. Tulis rekomendasi **audience + tone + alasan singkat** di atas output
5. Langsung eksekusi output di bawah rekomendasi — satu pesan, tidak perlu tunggu konfirmasi
6. Tutup dengan: *"Kalau mau ganti tone/audience, bilang aja."*

## Tone Reference

### Caveman Lite
- Potong filler, artikel, pleasantries
- Kalimat pendek, jeda jelas
- Bahasa tetap natural Indo
- Cocok: hook reels, headline, bullet benefit, push notif

### Tengah (Default)
- Natural bahasa sehari-hari ("nggak", "bareng", "yuk")
- Kalimat sedang ~8-12 kata
- Ada jeda emosional
- Cocok: video ads 30s, caption, carousel

### Normal Panjang
- Full grammar, kalimat lengkap
- Tone hangat dan conversational
- Cocok: email, landing page, sales page, blog

## Produk Konteks (Akbar — Workbook Pernikahan)

Kalau konteks produk adalah workbook/program pernikahan milik user:

- Angle utama 1: Authority Discovery (riset India 1% perceraian → 9 kebiasaan → ritual batin → workbook)
- Angle utama 2: Gottman/Love Lab (Dr. Gottman → puluhan tahun riset/ribuan pasangan → pola halus/micro-expression → luka tersimpan → workbook/Ho'oponopono)
- Tone: hangat, tidak menggurui, relatable pasangan Indonesia
- Pain point: luka lama, jarak emosional, kecewa yg menumpuk, maaf yg cuma menyentuh permukaan
- CTA default: "Link di bawah" atau "DM kata INDIA"
- Jangan: hard sell, klaim produk menyelamatkan pernikahan, bahasa klinis/terapi
- Meta Ads compliance: boleh menyebut riset/peneliti, tapi hindari framing angka spesifik sebagai klaim produk. Untuk aman, ganti "94% akurasi / 3000 pasangan" menjadi "puluhan tahun riset / ribuan pasangan".

## Preferred Video Ads Output Shape

Kalau user meminta script video ads/reels 30 detik, format output mengikuti bentuk ini (Telegram-friendly, tanpa tabel pipe):

```
Script Video Ads 30 Detik — [Tone/Angle]

---

VO SCRIPT

> Baris VO pendek.
>
> Baris VO berikutnya.
>
> Jeda pakai blockquote kosong.

---

Text Overlay Per Scene

0–3s

• Detik: 0–3s
• Overlay: [teks pendek]
• Footage: [footage konkret]

3–6s

• Detik: 3–6s
• Overlay: [teks pendek]
• Footage: [footage konkret]

---

Catatan eksekusi:

- VO pace: [lambat/sedang/punchy]
- Tone musik: [referensi]
- Hook visual: [wajib]
- CTA terakhir: [urgency lembut]
```

User prefers this structure over dense tables for execution-ready ads scripts. If asked for multiple versions, repeat the same structure per version rather than compressing into comparison tables.

## Common Pitfalls

### Cardinality & Scope Pitfall for Headlines/Judul

When the user asks for `N judul per X`, `5 judul per transkrip`, `per konten`, `per produk`, `per ad`, or similar, do **not** collapse the task into a small global shortlist. First compute and state the expected output count: e.g. `46 transkrip × 5 judul = 230 judul`. Generate and present output grouped by each source item, then verify the count before claiming done. If also useful, a separate global summary/cluster may be added, but label it clearly as a global summary so it is not mistaken for the requested per-item output.

1. **Jangan tanya satu per satu** — tanya semua yg perlu (format + channel) sekaligus dalam 1 blok
2. **Jangan skip kalau trigger ada tapi context ambigu** — lebih baik tanya 10 detik daripada salah eksekusi
3. **Jangan override default diam-diam** — selalu tulis rekomendasi audience + tone + alasan di atas output
4. **Jangan tanya tone atau audience** — user prefer Hermest yg memutuskan. Hanya format + channel yg ditanya.
5. **Jangan padatkan multi-versi script ke tabel komparasi** — repeat full structure per versi (VO + overlay + catatan eksekusi). User suka format paralel, bukan dense compare.
6. **Hindari tabel pipe di Telegram untuk script ads** — pakai bullet `• Detik: …` style. Pipe table auto-rewrite jadi bullet, tapi langsung pakai bullet lebih clean.
7. **Compliance Meta Ads** — angka spesifik (94%, 3000 pasangan) di-soften jadi "puluhan tahun riset / ribuan pasangan" untuk hindari flag.
8. **Tone tengah ≠ tone normal panjang** — tengah masih punchy + kalimat pendek, cuma tambah sapaan/konjungsi natural. Normal panjang = full grammar, overflow durasi.

## Linked References

- `references/ai-video-generation-stack.md` — tool & workflow buat eksekusi script jadi footage (Veo/Sora/Kling/HeyGen) + akses user + compliance Meta Ads

## Verification Checklist

- [ ] Trigger word terdeteksi
- [ ] Skip kondisi dicek
- [ ] 3 pertanyaan ditanya dalam 1 blok
- [ ] Default diterapkan untuk field kosong
- [ ] Konfirmasi singkat sebelum eksekusi
- [ ] Output sesuai tone + audience + channel yang disepakati
