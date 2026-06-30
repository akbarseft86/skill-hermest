---
name: tavily-search
description: Search the web using Tavily API for fast research summaries with source URLs. Use when user asks to use Tavily, Tavily search, or wants AI-ready web research output.
metadata: {"openclaw":{"requires":{"bins":["curl","jq"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Tavily Search

Use Tavily via `curl` and parse JSON with `jq`.

## Quick search

Run:

```bash
curl -sS https://api.tavily.com/search \
  -H 'Content-Type: application/json' \
  -d "{\"api_key\":\"$TAVILY_API_KEY\",\"query\":\"<QUERY>\",\"search_depth\":\"basic\",\"max_results\":5}" \
| jq '{answer, results: [.results[] | {title, url, score, content}]}'
```

## Deeper search

Use `search_depth":"advanced"` and increase `max_results`.

## Safety

- Never print full API key in chat output.
- Return source URLs for claims.
