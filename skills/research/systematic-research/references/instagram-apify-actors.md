# Instagram Apify Actor Notes

Use this reference when direct Instagram/browser scraping is blocked and the user needs competitor post classification.

## Repository Pattern

A repo like `social-media-scraping-apis` may only be a **catalog** of Apify actors, not executable scraper code. Check for:
- `package.json` — if absent, not a runnable Node project
- scripts / actor code — if absent, catalog only
- `APIFY_TOKEN` env var — required to call actors
- `apify` CLI — optional; REST API works too

Do not call a catalog repo "working" until an actor has actually run and returned dataset items.

## Candidate Actors for Instagram Competitor Audit

### Apify Store lookup first — avoid stale actor slugs
Actor slugs/names change and `/acts/<username>~<actor>/runs` can return `page-not-found` even when a similar actor exists. Before running, search the Apify Store and use the returned **actor id**:

```bash
curl -sS "https://api.apify.com/v2/store?search=instagram-scraper&limit=5" \
| python3 -c 'import sys,json; d=json.load(sys.stdin); [print(it.get("id"), it.get("username"), it.get("title")) for it in d.get("data",{}).get("items",[])]'
```

Known working option from a Coway competitor audit session:
- `shu8hvrXbJbY3Eb9W` — Apify official **Instagram Scraper**

Run by actor id, not guessed slug:

```bash
curl -sS -X POST "https://api.apify.com/v2/acts/shu8hvrXbJbY3Eb9W/runs?token=$APIFY_TOKEN&waitForFinish=90" \
  -H 'Content-Type: application/json' \
  -d '{"directUrls":["https://www.instagram.com/lifecoway.id/"],"resultsType":"posts","resultsLimit":3,"searchType":"user"}'
```

Then fetch the dataset:

```bash
curl -sS "https://api.apify.com/v2/datasets/$DATASET_ID/items?token=$APIFY_TOKEN&clean=true&limit=50"
```

### `apidojo/instagram-scraper`
Can be useful, but verify via Store lookup first; stale docs/slugs may fail with `page-not-found`.

### `coderx/instagram-profile-scraper-posts-bio`
Good candidate for quick profile + latest posts extraction, but verify availability via Store lookup before assuming the slug works.

### Post-specific media actors
Use only after you already have post URLs/shortcodes:
- `scrapearchitect/instagram-post-image-scraper-image-post-downloader`
- `scrapearchitect/instagram-post-video-scraper-video-post-downloader`

## Minimal Verification Checklist

Before saying "repo/tool works":
1. Confirm `APIFY_TOKEN` exists or user provided it.
2. Run a small actor test with max 1–3 items.
3. Confirm dataset returned non-empty JSON.
4. Inspect fields for `type`/`productType`/`media_type`/`is_video`/`children` to classify single image vs carousel vs reel.
5. Save raw JSON or summary table for repeatability.

## Classification Fields to Look For

Depending on actor output, useful fields may include:
- `type`, `productType`, `mediaType`
- `isVideo`
- `isSidecar` / `children` / `carousel_media`
- `shortCode`, `url`
- `caption`, `hashtags`
- `timestamp`, `likesCount`, `commentsCount`
- `displayUrl`, `videoUrl`, `thumbnailUrl`

## Important Pitfall

Search snippets can reveal pricing, products, and captions, but **cannot prove feed format**. Only visual feed access, post metadata, or screenshots can verify whether a post is carousel, reel, or single image.

Apify success status is not enough. Always validate that dataset items match the target account before using them:
- Check `ownerUsername`, `user.username`, `inputUrl`, `from_url`, `url`, or profile metadata when present.
- Spot-check captions/topics for niche coherence.
- If one actor returns 0 items or unrelated content, mark that account unresolved and try another actor; do not mix contaminated data into the report.

Do not ask the user to resend credentials/handles if they already provided them in a visible screenshot or earlier platform message. First re-read current attachments, OCR/vision descriptions, and session recall. If Discord/channel history is not directly accessible, say that limitation briefly, but still extract what is visible from screenshots before asking again.

When a user says “cek di atas” / “kan udah semua,” treat it as a workflow correction: recover context from screenshots/session search before requesting the same information again.

Do not ask the user to resend credentials/handles if they already provided them in a visible screenshot or earlier platform message. First re-read current attachments, OCR/vision descriptions, and session recall. If Discord/channel history is not directly accessible, say that limitation briefly, but still extract what is visible from screenshots before asking again.

When a user says “cek di atas” / “kan udah semua,” treat it as a workflow correction: recover context from screenshots/session search before requesting the same information again.
