# MJO Schedule Tracking — API Reference

## DB Schema (upload_schedule)

Extended fields added to existing `upload_schedule` table:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `launch_status` | TEXT | `'scheduled'` | scheduled / drafted / launched / failed |
| `ad_id` | TEXT | NULL | Meta ad ID setelah launch |
| `campaign_id` | TEXT | NULL | Meta campaign ID |
| `adset_id` | TEXT | NULL | Meta ad set ID |
| `meta_account_id` | TEXT | NULL | act_XXXXXXXXX |
| `meta_status` | TEXT | NULL | ACTIVE / PAUSED / DELETED / ARCHIVED / ERROR |
| `meta_synced_at` | TEXT | NULL | Timestamp sync terakhir (%Y-%m-%d %H:%M:%S) |
| `meta_error` | TEXT | NULL | Error message dari sync |

## Endpoints

### POST /api/schedule/update-status

Digunakan oleh launch script untuk menulis balik ad IDs setelah iklan jadi di Meta.

**Request:**
```json
{
  "id": 14,
  "launch_status": "drafted",
  "ad_id": "123456789012345",
  "campaign_id": "123456789012345",
  "adset_id": "123456789012345",
  "meta_account_id": "act_1025434792768020"
}
```

**Response (success):**
```json
{"ok": true, "updated": 1}
```

**Response (already launched — HTTP 409):**
```json
{"ok": false, "error": "jadwal #14 udah di-launch (drafted)"}
```

Guard logic: backend ngecek `SELECT launch_status FROM upload_schedule WHERE id=`. Kalau sudah `drafted` atau `launched`, return 409. Launch script yang mau nulis balik harus handle error ini sebagai **skip / already done**, bukan retry.

### POST /api/schedule/sync-meta

Validasi status iklan langsung ke Meta Graph API, throttled. Tidak perlu Meta credentials di frontend.

**Request:**
```json
{"limit": 25, "gap": 2.0}
```
- `limit`: jumlah maksimal row yang diperiksa (1–100, default 25)
- `gap`: detik jeda antar request ke Meta (min 0.5, default 2.0)

**Response:**
```json
{
  "ok": true,
  "checked": 5,
  "gap_seconds": 2.0,
  "items": [
    {"schedule_id": 14, "ok": true, "ad_id": "123...", "meta_status": "ACTIVE"},
    {"schedule_id": 15, "ok": false, "error": "HTTP 400 - (#100) Unknown path"}
  ]
}
```

Sync cuma memproses row yang punya `ad_id` (pernah di-launch). Row tanpa `ad_id` dilewati.

## Frontend badge logic

```js
const badge = (i) => {
  if (i.meta_status == 'ACTIVE')         return '🟢 Live';
  if (i.meta_status == 'PAUSED' || i.meta_status == 'ADSET_PAUSED' || i.meta_status == 'CAMPAIGN_PAUSED') return '⚪ Paused';
  if (i.meta_status == 'DELETED' || 
      i.meta_status == 'ARCHIVED')       return '🔴 Hapus';
  if (i.meta_status == 'ERROR')          return '✖ Error';
  if (i.launch_status == 'drafted' || 
      i.launch_status == 'launched')     return '🔵 Draft';
  if (i.launch_status == 'failed')       return '✖ Gagal';
  return '🟡 Jadwal';  // default scheduled
};
```

Badge priority: Meta status > launch status. Kalau meta_status terisi, itu yang dipakai.

## Frontend filter tabs

Halaman jadwal (`mjo-jadwal.html`) punya filter tab di atas daftar jadwal:

| Tab | Fungsi |
|-----|--------|
| **🔜 Belum Launch** (default) | Hanya nampilin jadwal yang `launch_status=scheduled` dan `ad_id` null — item yang belum pernah di-launch sama sekali |
| **📋 Semua** | Nampilin semua jadwal tanpa filter |

Filter logic di JS:
```js
function isLaunched(i) {
  return ['drafted','launched'].includes(i.launch_status) || !!i.ad_id;
}
// Di loadList():
if (FILT=='pending') items = items.filter(i => !isLaunched(i));
```

Saat tab "Belum Launch" aktif dan semua jadwal udah pernah di-up, tampil pesan:
> Tidak ada yang belum launch. 5/5 jadwal sudah pernah di-up. Klik tab Semua untuk lihat arsip.

Baris informasi di atas daftar (Semua):
> Tampil 5/5 jadwal · sudah di-up 5

## GET /api/schedule response (fields)

Endpoint `GET /api/schedule` sekarang return kolom tambahan per item:

```
id, tanggal, jam, content_id, akun, budget, status,
judul, cep, produk, content_status,
launch_status, ad_id, campaign_id, adset_id, meta_account_id,
meta_status, meta_synced_at, meta_error
```

## Cron untuk auto-sync harian

```bash
# Via Hermest CLI:
cronjob action=create \
  name="mjo-daily-sync-meta" \
  schedule="0 9 * * *" \
  prompt="Panggil POST /api/schedule/sync-meta dengan limit=25 gap=2. Lapor: berapa dicek, berapa ok, berapa error. Kalau ada yang error/warning, sebutkan details." \
  skills=["mjo-launch-ads"] \
  enabled_toolsets=["web","terminal"]
```

## Frontend Picker Auto-Hide

Setelah konten di-launch, konten tersebut harus otomatis hilang dari daftar centang (content picker) di halaman jadwal — bukan cuma dari daftar schedule.

**Kode lengkap (dari `mjo-jadwal.html`):**

```html
<script>
// ─── Picker Filter ──────────────────────────────────────
// Built saat init: fetch schedule, kumpulin content_id + title yang udah di-launch
const LAUNCHED_IDS   = new Set();
const LAUNCHED_TITLES= new Set();

function normTitle(t) {
  return (t||'').toLowerCase().replace(/\s+/g,' ').trim();
}

function alreadyUp(item) {
  if (LAUNCHED_IDS.has(item.id))     return true;
  if (LAUNCHED_TITLES.has(normTitle(item.judul))) return true;
  return false;
}

// Panggil pas init, barengan fetch content:
fetch('/api/schedule').then(r=>r.json()).then(list=>{
  list.forEach(i => {
    if (i.launch_status=='drafted' || i.launch_status=='launched' || i.ad_id){
      LAUNCHED_IDS.add(i.content_id);
      if (i.judul) LAUNCHED_TITLES.add(normTitle(i.judul));
    }
  });
  // render picker setelah sets siap
  renderPicker();
});

// Di renderPicker(), filter pake alreadyUp:
function renderPicker() {
  let html = '';
  let hidden = 0;
  DATA.forEach(d => {
    if (alreadyUp(d)) { hidden++; return; }
    html += `<label><input type=checkbox value="${d.id}"> ${escHtml(d.judul)}</label>`;
  });
  if (hidden) html = `<div class=info>${hidden} konten disembunyikan (sudah di-up)</div>` + html;
  document.getElementById('picker').innerHTML = html || '<div class=info>Tidak ada konten.</div>';
}
</script>
```

**Kenapa perlu double filter (ID + Title):**
- `content_id` cocok → yang schedule-nya eksak merefer konten yang sama. Aman pasti dup.
- `title` cocok → catch content yang `status=BARU` tapi judulnya sama persis dengan item yang sudah di-launch via schedule sebelumnya (mis. konten duplikat atau re-upload dengan ID baru).

**Pitfall:**
- Jangan lupa normalisasi judul (`toLowerCase().trim()`) — data bisa beda casing.
- LAUNCHED_TITLES harus populated **sebelum** `renderPicker()` dipanggil pertama kali. Urutan: fetch schedule dulu → build sets → baru fetch content + render.
- Kalau user launch konten baru via tombol, setelah POST /api/schedule/update-status sukses → panggil renderPicker() ulang biar hide-nya instant tanpa reload halaman.

## Arsitektur keamanan

```
┌─────────────────────┐     ┌──────────────────────────┐
│  Browser / Frontend  │     │  Backend (VPS)           │
│  (no Meta creds)     │     │  mjo_api.py :8787        │
│                      │     │                          │
│  [🟡 Jadwal] badge ←───────│  GET /api/schedule       │ ← DB lokal
│  [↻ Sync Meta] btn ───────→│  POST /api/schedule/     │
│                      │     │        sync-meta         │──→ Meta Graph API
│                      │     │                          │    (2s throttle)
└─────────────────────┘     └──────────────────────────┘
```

Frontend TIDAK PERNAH:
- Membawa Meta access token
- Memanggil graph.facebook.com
- Menyimpan ad account credentials

Semua interaksi Meta lewat backend endpoint `sync-meta` yang throttled.