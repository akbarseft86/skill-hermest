# AI Video Generation Stack untuk Ads (Akbar)

Capture dari sesi 2026-05-23. Akbar minta workflow AI buat eksekusi script video ads jadi footage. Konteks: produk workbook pernikahan, Meta Ads + IG Reels + TikTok Ads.

## Akses User (penting — jangan lupa)

- **ChatGPT Plus:** Sora 2 versi lite (kalau region account US/CA/JP/KR). Akun region Indonesia biasanya belum dapat menu Sora — perlu VPN US + invite code untuk akses awal.
- **Veo 3:** user punya banyak akun via Google family group → akses aman dari Indonesia via `gemini.google.com` atau `flow.google.com`. Ini stack utama.
- **ElevenLabs:** untuk VO Indonesia natural.

## Pilihan Tool (per use case, 2026)

| Use case | Primary | Backup | Catatan |
|---|---|---|---|
| Cinematic scene + audio native | Veo 3 (Flow) | Sora 2 (kalau ada) | Veo 3 native audio + dialog |
| Wajah Asia/Indo close-up | Kling 2.0 | Hailuo 02 | Kling paling natural untuk wajah Asia |
| Image-to-video continuity | Runway Gen-4 | Kling | Kasih foto referensi, generate video |
| Talking-head avatar (Personal Reveal) | HeyGen (avatar user) | Arcads | Cocok angle "Personal Reveal" |
| UGC ad style | Arcads | Captions/AI Studio | 300+ template aktor |
| Budget tight test | Hailuo 02 | Kling free tier | 80% Sora dengan 25% harga |
| Stock b-roll | Pexels/Envato | — | Lebih authentic dari AI buat scene biasa |

## Hybrid Workflow (Rekomendasi Default Akbar)

Paling efisien karena Akbar sudah punya Veo + ChatGPT Plus:

1. **B-roll umum** → cari di Pexels/Envato (pasangan, ritual, golden hour)
2. **Scene spesifik** (lab Gottman 70s, micro-expression spesifik) → generate di **Veo 3**
3. **Wajah pasangan Indo close-up** → generate di **Kling** (lebih natural dari Veo untuk Asian face)
4. **VO Indonesia** → ElevenLabs atau record sendiri
5. **Edit + subtitle** → CapCut Pro

Stack cost ~$40-60/bulan kalau di luar Veo (Veo sudah covered via family group).

## Setting Veo 3 Default untuk Reels/TikTok/Meta Ads

- Aspect ratio: **9:16** (vertical)
- Duration per clip: **5-8 detik** per prompt (kalau >8 detik, split jadi 2 prompt)
- Quality: **Highest**
- Generate 2-3 variasi per scene → pilih terbaik
- Style hybrid yg sering dipakai: **archival/documentary 0-10s + cinematic warm 10-30s** (kombo D+A) untuk angle riset/peneliti

## Prompt Engineering Pattern (Veo 3)

Struktur prompt yg konsisten menghasilkan output bagus:

```
[Camera setup] of [subject], [age/ethnicity if needed], 
[action / micro-expression], [lighting], [time of day], 
[lens/DOF], [film stock or digital look], [duration], 
[audio note or "no dialogue"].
```

Tambahan kalau wajah kurang natural:
> hyper-realistic, photographic, natural skin texture, no AI artifacts

## Urutan Generate (Hemat Credit + Cepat Pivot)

1. Scene paling susah dulu (micro-expression, dialog continuity)
2. Scene multi-cut (3 cuts dalam 1 prompt)
3. Scene mudah/archival
4. Scene continuity (butuh 2 shots connected)

## Compliance Note (Meta Ads — pernikahan/relationship/health)

- Boleh sebut "peneliti pernikahan terkemuka" / "puluhan tahun riset" / "ribuan pasangan"
- Jangan klaim angka spesifik sebagai keunggulan produk ("94% akurasi", "3000 pasangan")
- Jangan klaim produk menyelamatkan pernikahan
- Jangan visual konflik keras (KDRT, teriakan) — pakai micro-expression
- Soft phrasing untuk angka: ganti "94%" → "tingkat akurasi tinggi" / hapus, ganti "3000 pasangan" → "ribuan pasangan"

## Bila User Minta Prompt Veo dari Script

Pattern delivery yg dia suka:
- 1 prompt per scene (sesuai overlay timing 3-4 detik)
- Setiap prompt sudah include: kamera, subject, ekspresi, lighting, durasi, audio note
- Tutup dengan "Tips Eksekusi di Veo 3" (aspect ratio, durasi, urutan generate, fallback ke Kling)
- Akhiri dengan offer: VO prompt (ElevenLabs), CapCut edit guide, atau versi lain

## Open Issues / To Verify Next Time

- Sora 2 di region Indonesia: masih perlu VPN + invite per akhir 2025 — verify ulang tiap quarter
- Veo 3 native audio dialog Indonesia: cek kualitas lip-sync untuk Bahasa Indonesia (kadang kurang akurat)
- HeyGen avatar dari foto Akbar: belum dicoba, kandidat utama untuk Versi 3 "Personal Reveal"
