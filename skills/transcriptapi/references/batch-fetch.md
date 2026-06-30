# Batch Transcript Fetching Pattern

Use when user provides a list of 20+ YouTube videos and wants transcripts for all of them.

## 1. Parse video IDs

Extract video IDs from URLs, spreadsheets, or raw text. Common formats:
- `https://youtu.be/VIDEO_ID` → split on `/`, take last segment
- `https://youtube.com/watch?v=VIDEO_ID` → split on `v=`, take first param
- `youtube.com/shorts/VIDEO_ID` → split on `/shorts/`
- Bare 11-char IDs → use directly

Tip: When data comes from CSV/TSV, parse row-by-row. Title usually sits one row above the link.

## 2. Validate API key first

```python
# Single test call to validate key before spending credits on batch
url = f"{BASE_URL}?video_url={first_video_id}&format=json&send_metadata=true"
```

If 401 → key is invalid. Ask user to check transcriptapi.com dashboard and regenerate.

## 3. Parallel fetch with ThreadPoolExecutor

```python
import concurrent.futures, urllib.request, json, time

BASE_URL = "https://transcriptapi.com/api/v2/youtube/transcript"
API_KEY = os.environ['TRANSCRIPT_API_KEY']

def fetch_transcript(video_id):
    url = f"{BASE_URL}?video_url={video_id}&format=json&send_metadata=true"
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {API_KEY}',
        'User-Agent': 'HermesAgent/1.0'
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        d = json.loads(resp.read())
    transcript = '\n'.join(seg['text'] for seg in d.get('transcript', []))
    return {
        'video_id': video_id,
        'language': d.get('language', ''),
        'video_title': d.get('metadata', {}).get('title', ''),
        'author': d.get('metadata', {}).get('author_name', ''),
        'transcript': transcript,
        'segments': d.get('transcript', []),
    }

# 10 workers — stays under 300 req/min (free tier limit)
results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    futures = {ex.submit(fetch_transcript, vid): vid for vid in video_ids}
    done = 0
    for f in concurrent.futures.as_completed(futures):
        vid = futures[f]
        done += 1
        try:
            r = f.result()
            results.append(r)
            print(f"[{done}/{total}] ok {vid}")
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            results.append({'video_id': vid, 'error': err, 'status': 'error'})
            print(f"[{done}/{total}] err {vid}: {e.code}")
        except Exception as e:
            results.append({'video_id': vid, 'error': str(e), 'status': 'error'})
            print(f"[{done}/{total}] err {vid}: {e}")
```

## 4. Retry 408 errors

```python
# After first pass, retry 408 errors with exponential backoff
retry_ids = {r['video_id'] for r in results if '408' in r.get('error', '')}
for vid in retry_ids:
    for attempt in range(3):
        try:
            r = fetch_transcript(vid)
            # merge result
            break
        except urllib.error.HTTPError as e:
            if e.code in (408, 429):
                time.sleep(2 * (attempt + 1))
            else:
                break
```

## 5. Save to JSON

Save intermediate results immediately — don't lose work if something fails mid-batch.

```python
json.dump(results, open('transcripts.json', 'w'), indent=2, ensure_ascii=False)
```

## 5a. Verify the saved JSON

Do not assume all saved entries are valid transcripts:

```python
ok = sum(1 for r in results if r.get('transcript') and not r.get('error'))
err = sum(1 for r in results if r.get('error') or not r.get('transcript'))
print(f"OK: {ok}, Errors: {err}")
for r in results:
    if r.get('error'):
        print(f"  ❌ {r['video_id']}: {r['error'][:80]}")
```

A saved JSON may contain error messages (bot detection, timeouts, 404s) where transcripts should be. This happens when `yt-dlp` is used as a fallback and YouTube blocks it. The actual transcript data may exist only in the HTML artifact generated from the batch results, not in the raw JSON. Always verify file contents before treating them as the data source for analysis or downstream work.

## 6. Export to CSV

For Google Sheets import — export the same data as CSV.

```python
import csv
with open('transcripts.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Year', 'Title', 'Video ID', 'Link', 'Status', 'YouTube Title', 'Author', 'Language', 'Transcript'])
    for r in results:
        writer.writerow([r['year'], r['title'], r['video_id'], r['link'], r.get('status','ok'), r.get('video_title',''), r.get('author',''), r.get('language',''), r.get('transcript','')])
```

## 7. Generate HTML with copy-per-item

For the HTML generation, see the transcriptapi session `doc_572d99fcc76e_message.txt` (June 2026) for the full working pattern including:
- Dark-themed collapsible sections grouped by category/year
- Copy button per item (copies title + link + full transcript to clipboard)
- Copy-all per section and copy-all-everything buttons
- Search box that filters entries by title or transcript content
- Download CSV link alongside copy buttons

Key HTML decisions:
- White-space: pre-wrap for transcripts (preserves line breaks)
- Max-height 600px with overflow-y auto on transcript boxes
- Collapsible sections default open (user wants to see content immediately)
- Toast notification on copy ("Tersalin!")
- File sizes: 51 transcripts ≈ 3.3MB HTML, 3.3MB CSV

## Errors seen in production

| Error | Cause | Resolution |
|-------|-------|------------|
| 401 | Invalid API key | Ask user to regenerate at transcriptapi.com/dashboard |
| 404 | Video has no captions | Cannot fix — mark as unavailable, skip in output |
| 408 | Transient timeout | Retry 1-3 times, 2s exponential backoff |
| 429 | Rate limited | Respect Retry-After header, or reduce workers |
| 1010 | Cloudflare block | Missing or bad User-Agent header |
