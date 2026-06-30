# API Examples

Base URL:

```bash
export LIGHTRAG_BASE_URL=${LIGHTRAG_BASE_URL:-http://127.0.0.1:9621}
```

## Insert memory text

```bash
curl -sS -X POST "$LIGHTRAG_BASE_URL/documents/text" \
  -H 'Content-Type: application/json' \
  -d '{"text":"Meeting: client prefers weekly report every Monday 09:00 WIB"}'
```

## Query memory

```bash
curl -sS -X POST "$LIGHTRAG_BASE_URL/query" \
  -H 'Content-Type: application/json' \
  -d '{"query":"Kapan jadwal report client?","mode":"mix"}'
```

## Delete/rebuild notes

Use WebUI/API according to current LightRAG version. If endpoint changes, inspect `lightrag/api/README.md` from installed package/repo.
