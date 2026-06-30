# 9Router SearXNG web search integration

Session learning: user wants web search to use a free self-hosted SearXNG-backed 9Router endpoint when configured, but the endpoint is **not** vanilla SearXNG protocol.

## 9Router API shape

Endpoint:

```http
POST http://localhost:20128/v1/search
Content-Type: application/json
Authorization: Bearer <9Router_API_Key>
```

Body:

```json
{
  "model": "searxng",
  "query": "short focused query",
  "search_type": "web",
  "max_results": 5
}
```

`search_type` can be `web` or `news`.

Expected response shape:

```json
{
  "results": [
    {"title": "...", "url": "...", "snippet": "..."}
  ]
}
```

## Important compatibility pitfall

Hermes's built-in `searxng` web backend expects a vanilla SearXNG instance and uses SearXNG-style routes such as `/search?q=...&format=json` via `SEARXNG_URL`.

9Router's endpoint above is a custom OpenAI-like API route (`/v1/search`). Setting `SEARXNG_URL=http://localhost:20128` is not sufficient unless 9Router also exposes vanilla SearXNG-compatible routes. In the observed setup, `GET /search?q=test&format=json` returned 404, while `POST /v1/search` existed.

## Verification sequence before switching Hermes away from Tavily

1. Test vanilla SearXNG compatibility:

```bash
curl -s -m 5 "http://localhost:20128/search?q=test&format=json" -w "\nHTTP %{http_code}\n"
```

If this is 404, built-in Hermes `searxng` backend will not work directly.

2. Test 9Router custom API:

```bash
curl -s -m 5 -X POST "http://localhost:20128/v1/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NINEROUTER_API_KEY" \
  -d '{"model":"searxng","query":"test","search_type":"web","max_results":2}' \
  -w "\nHTTP %{http_code}\n"
```

If this returns `searxng error: fetch failed` / HTTP 502, the custom endpoint is reachable but the SearXNG service behind 9Router is down or misconfigured.

## Integration options

- Keep Tavily until 9Router-backed SearXNG is healthy.
- If 9Router exposes vanilla SearXNG routes, set Hermes web backend to `searxng` and configure `SEARXNG_URL` accordingly.
- If only `/v1/search` exists, implement a custom Hermes web provider plugin for 9Router rather than using the built-in SearXNG backend.

## Efficient search policy requested by user

- Call web search only for current/fresh facts, explicit web checks, or uncertain facts where fresh data materially improves accuracy.
- Use short focused queries under 400 characters.
- Default `max_results=5`; use 3 for narrow lookups, 8–10 only for broad research.
- Prefer one focused call; max three calls per user request.
- Use `news` only for actual news/current coverage.
- Summarize results; do not dump raw search results.