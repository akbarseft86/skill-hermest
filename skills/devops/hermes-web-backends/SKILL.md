---
name: hermes-web-backends
description: Use when configuring, migrating, or troubleshooting Hermes Agent web search/extract/crawl backends. Covers backend selection, self-hosted SearXNG, partial migrations, verification, rollback, and provider-protocol gotchas.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes-agent, web, search, searxng, backend, devops]
    related_skills: [hermes-agent, hermes-web-backend-searxng]
---

# Hermes Web Backends

## Overview

Use this skill for class-level work on Hermes Agent web tooling: selecting a search backend, migrating away from paid/quota providers, deploying self-hosted search, wiring environment/config values, verifying `web_search`, and avoiding regressions in `web_extract` / `web_crawl`.

The core mental model: Hermes web support is not one monolithic backend. Search, extract, crawl, and fallback backend settings can be split. A provider that supports search may not support extraction or crawling.

## When to Use

- User wants to change Hermes `web_search` provider/backend.
- User wants to self-host search, especially with SearXNG.
- User asks why `web_search`, `web_extract`, or web crawling broke after a backend change.
- User mentions Tavily, Exa, Firecrawl, Brave, DDGS, SearXNG, or a custom `/v1/search` wrapper.
- User asks to reduce web-search costs or avoid paid quotas.

Do **not** deploy anything if the user only asks whether it is possible; answer first and ask before making infrastructure changes.

## Backend Selection Rules

1. **Search backend** answers queries and returns result URLs/snippets.
2. **Extract backend** fetches and parses a URL into readable content.
3. **Crawl backend** follows multiple pages.
4. **Fallback/backend** may be used as default, but do not assume it implements every operation.

Safe migration shape when moving only search to a free/self-hosted option:

```yaml
web:
  backend: searxng
  search_backend: searxng
  extract_backend: tavily   # or another provider known to support extraction
  crawl_backend: tavily
```

Never flip `extract_backend` or `crawl_backend` to a search-only provider unless you have confirmed that provider implements those operations.

## Self-Hosted SearXNG Recipe

Use this when the user wants a free self-hosted replacement for a paid/quota search backend.

### Preconditions

Verify before touching Hermes config:

```bash
docker ps
ss -ltnp | grep ':8888' || true
```

- Docker must be installed and running.
- Port `8888` should be free or intentionally chosen.
- Warn that `web_search` can break temporarily if config is switched before SearXNG is healthy.

### Deploy

```bash
docker pull searxng/searxng:latest
mkdir -p /opt/searxng
docker run -d \
  --name searxng \
  -p 8888:8080 \
  -v /opt/searxng:/etc/searxng \
  searxng/searxng:latest
```

### Required `settings.yml` tweaks

The default config often blocks JSON output and may bind too narrowly inside the container.

```yaml
search:
  formats:
    - html
    - json

server:
  bind_address: "0.0.0.0"
```

Then restart:

```bash
docker restart searxng
```

### Verify SearXNG JSON

```bash
curl -s -H 'X-Forwarded-For: 127.0.0.1' \
  "http://localhost:8888/search?q=test&format=json" | head -c 400
```

Expected: JSON with a `results` array. Engine-specific warnings in logs can be cosmetic if JSON results are returned.

## Wire Hermes to SearXNG

Set the URL in `~/.hermes/.env`:

```bash
SEARXNG_URL=http://localhost:8888
```

Set Hermes config so only search moves to SearXNG unless extract/crawl alternatives are ready:

```yaml
web:
  backend: searxng
  search_backend: searxng
  extract_backend: tavily
  crawl_backend: tavily
```

Restart the relevant Hermes gateway/service so env and config are re-read. The exact service may differ by installation; prefer `hermes-agent` skill or local service inspection if unsure.

## Verification Checklist

```bash
grep -E "^web:|backend:|search_backend:|extract_backend:|crawl_backend:" ~/.hermes/config.yaml
grep SEARXNG_URL ~/.hermes/.env
systemctl --user is-active hermes-gateway || true
```

Then run a small `web_search` from chat and confirm results. If it hangs or returns empty, inspect:

```bash
docker logs --tail=100 searxng
```

and Hermes gateway logs for backend exceptions.

## 9Router / Custom Wrapper Gotcha

A local endpoint such as `localhost:20128` with `POST /v1/search` and a JSON body like `{model, query, search_type, max_results}` is **not** vanilla SearXNG.

- Hermes built-in `searxng` backend expects `/search?format=json`.
- A custom Next.js or 9Router wrapper returning HTML 404 at `/search?format=json` cannot be used as a SearXNG backend directly.
- A wrapper may have its own upstream failures such as `502`; fix that infrastructure or deploy a real SearXNG container.
- Speaking a custom wrapper protocol requires a custom Hermes web provider/plugin, not a config-only switch.

## Rollback

If search breaks after a migration:

```bash
hermes config set web.search_backend tavily
grep TAVILY_API_KEY ~/.hermes/.env
systemctl --user restart hermes-gateway
```

Keep the old provider key around until extraction/crawling have known-good replacements.

## Common Pitfalls

1. **Switching config before the new backend serves JSON.** Always curl the backend first.
2. **Treating search and extract as interchangeable.** SearXNG is search-only in this workflow.
3. **Assuming custom `/v1/search` APIs are SearXNG.** Protocol shape matters.
4. **Overpromising coverage improvements.** Backend choice mainly affects cost, control, reliability, and provider behavior; it does not magically make a single search call exhaustive.
5. **Forgetting restart.** Hermes gateway/services need restart after env/config changes.

## Proven Subcase: SearXNG Migration

The archived `hermes-web-backend-searxng` narrow skill was absorbed here. Its unique lessons are preserved in the SearXNG sections above: JSON output must be enabled, bind address may need `0.0.0.0`, `X-Forwarded-For` can avoid request-blocking errors, and extract/crawl should remain on a provider that supports them.
