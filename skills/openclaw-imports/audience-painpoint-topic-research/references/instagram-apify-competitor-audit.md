# Instagram competitor audit via Apify

Use this when a user wants ATM/competitor-led content strategy from an Instagram account and browser/Instagram direct access is blocked or unreliable.

## Workflow

1. Use a valid Apify API token (`APIFY_TOKEN`) through the Apify REST API.
2. First run `apify/instagram-profile-scraper` with the username to confirm profile metadata and retrieve `latestPosts` if available.
3. Then run `apify/instagram-scraper` for a larger post sample.
4. Export dataset items and classify each post by `type`.
5. Summarize format distribution before making content recommendations.

## Actor input examples

Profile scraper:

```json
{
  "usernames": ["lifecoway.id"],
  "resultsLimit": 50
}
```

Instagram scraper:

```json
{
  "directUrls": ["https://www.instagram.com/lifecoway.id/"],
  "resultsType": "posts",
  "resultsLimit": 30,
  "searchType": "user"
}
```

## Format classification

- `type == "Image"`: single image / flyer
- `type == "Sidecar"`: carousel
- `childPosts` non-empty: carousel evidence
- `type == "Video"`: video/reel candidate

## Reporting rule

State the numbers first, then strategy. Example:

> From 30 posts: 27 Image, 2 Sidecar, 1 Video. Therefore the competitor is single-image/flyer dominant; do not recommend carousel as the main ATM format.

## Pitfalls

- Do not confuse profile/search snippets with visual feed audit. Snippets can validate bio/products/offers, but not the post format mix.
- Some actor variants require `directUrls`; others use `startUrls`. If an actor log says “Start URLs must be provided,” inspect that actor’s expected input instead of assuming the profile is inaccessible.
- Actor output order may not be strictly newest-first. Sort by `timestamp` before labeling “latest 30.”
- Keep API tokens out of skill files and final reports.
