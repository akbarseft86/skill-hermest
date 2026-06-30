# Content Queue live-status cache

Use this reference when `/content-queue.html` or `/api/content?live=1` feels slow.

## Symptom

The Antrian Queue page loads slowly even though the HTML itself is static and small. A direct request to:

```bash
curl -w '\n%{time_total}\n' 'http://127.0.0.1:8787/api/content?live=1'
```

takes multiple seconds (observed ~5.6s) on the first request.

## Root cause pattern

`/api/content?live=1` enriches content cards with live Meta Ads status. In `mjo_api.py`, the request path calls `_match_live()` which calls `meta_ads_index()`. If `meta_ads_index()` rebuilds the index on every request, it can call Meta Graph/API for all MJO accounts and hundreds of ads on each page load.

This is expensive and unnecessary because ad/live-status index data does not need to change every second.

## Fix pattern: short in-memory TTL cache

Add a small module-level cache around `meta_ads_index()` in the live API source (`/opt/mjo-api/mjo_api.py`) and the dev source (`/root/mjo-pipeline/backend/mjo_api.py`).

```python
import time

_INDEX_CACHE = {"ts": 0, "data": None}
_INDEX_CACHE_TTL = 120  # seconds

def meta_ads_index():
    now = time.time()
    if _INDEX_CACHE["data"] is not None and now - _INDEX_CACHE["ts"] < _INDEX_CACHE_TTL:
        return _INDEX_CACHE["data"]

    # existing expensive Meta account/ad loop here
    idx = {}
    ...

    _INDEX_CACHE["ts"] = now
    _INDEX_CACHE["data"] = idx
    return idx
```

## Verification

Run two back-to-back requests:

```bash
curl -s -o /dev/null -w 'first %{time_total}\n' 'http://127.0.0.1:8787/api/content?live=1'
curl -s -o /dev/null -w 'second %{time_total}\n' 'http://127.0.0.1:8787/api/content?live=1'
```

Expected:
- First request may still take several seconds because it warms the cache.
- Second request should be near-instant (observed ~0.016s).

## Pitfalls

- This is per-process memory. Restarting the API clears the cache; first request after restart warms again.
- Keep TTL short (e.g. 120s) so status is fresh enough for operational use.
- Patch both DEV and LIVE copies, then sync/restart only with user approval per anti-shutdown rules.
- Do not cache the whole content list unless the user explicitly accepts staleness. The safer cache is the Meta ads index only.
