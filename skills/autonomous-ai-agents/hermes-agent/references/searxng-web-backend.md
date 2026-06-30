# SearXNG web backend setup notes

Use when moving Hermes `web_search` from a paid backend (for example Tavily) to native self-hosted SearXNG.

## Key distinction

Hermes native `searxng` backend expects a real SearXNG instance that supports:

```text
GET <SEARXNG_URL>/search?q=test&format=json
```

A 9Router-style endpoint such as:

```text
POST /v1/search
{"model":"searxng","query":"..."}
```

is not SearXNG-compatible unless it also exposes the vanilla `/search?format=json` route. If 9Router returns 502 for `model=searxng`, fix/deploy its SearXNG backend first rather than switching Hermes prematurely.

## Minimal Docker deployment

On RPM/OpenCloudOS-like systems, Docker's generic install script may reject the distro. Prefer native packages if available:

```bash
dnf install -y docker docker-buildx docker-compose
systemctl enable --now docker
```

Deploy SearXNG:

```bash
mkdir -p /opt/searxng
docker run -d \
  --name searxng \
  -p 8888:8080 \
  -v /opt/searxng:/etc/searxng \
  searxng/searxng:latest
```

Edit `/opt/searxng/settings.yml` to enable JSON:

```yaml
search:
  formats:
    - html
    - json
```

If container config binds only to localhost inside container, set:

```yaml
server:
  bind_address: "0.0.0.0"
```

Restart and verify:

```bash
docker restart searxng
curl -s -H 'X-Forwarded-For: 127.0.0.1' \
  'http://localhost:8888/search?q=test&format=json' | head -c 300
```

SearXNG may log individual engine timeouts/rate limits; those are not blockers if JSON returns useful `results`.

## Hermes config

Set env and search backend:

```bash
SEARXNG_URL=http://localhost:8888
web.search_backend: searxng
web.backend: searxng
```

Do not blindly set `web.extract_backend` or `web.crawl_backend` to `searxng`: native SearXNG is search-only. Keep a working extract/crawl backend if those tools are needed.

Restart the gateway/session after config/env changes so tools reload.
