# Reference-directory repos

Use this when the user asks to "pasang repo" for a repository that is primarily a curated list/directory rather than executable software.

## Pattern

1. Clone into a stable workspace path, usually `/root/.hermes/workspace/<repo-name>`.
2. Verify the clone with:
   - `git rev-parse --show-toplevel`
   - `git rev-parse --short HEAD`
   - file size / root listing for the main README or dataset files.
3. Inspect whether the repo contains code, data, or only Markdown/link directories before implying it is "installed" as runnable software.
4. If the user has a concrete research target, create a small adjacent workspace folder for outputs, e.g. `/root/.hermes/workspace/ig-research/`.
5. Extract a shortlist from the directory into a machine-readable file such as CSV/Markdown.
6. Report the local path, source URL, verified commit, and what can be done next.

## Example: Social Media Scraping APIs repo

Source: `https://github.com/cporter202/social-media-scraping-apis`

Observed durable structure from the session:
- Huge root `README.md` plus `social-media-apis-3268/README.md`.
- It is mainly a curated directory of third-party scraping tools/APIs, not a runnable scraper package.
- Many Instagram links point to Apify Actors and may contain referral parameters such as `?fpr=...`.

Good downstream artifact for IG research:
- `/root/.hermes/workspace/ig-research/README.md` — explains the local repo and research rules.
- `/root/.hermes/workspace/ig-research/instagram_scraper_shortlist.csv` — shortlist of relevant Instagram scrapers.

## Pitfalls

- Do not tell the user the repo is "installed" in the sense of a working scraper unless it contains executable setup and credentials are configured.
- For social-media scraping, separate the directory install from API/vendor setup. Apify or other vendors may require account tokens, paid credits, actor-specific pricing, and per-platform ToS checks.
- Prefer public-data, aggregate market research framing. Avoid private-account scraping, spam/auto-DM, or sensitive personal-data extraction.
