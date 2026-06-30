# Setup and Ops

## 1) Install and run server

```bash
bash skills/lightrag-memory-main/scripts/setup_lightrag.sh
```

This script will:
- create `~/lightrag`
- create Python venv
- install `lightrag-hku[api]`
- write a starter `.env` (if missing)
- start `lightrag-server` on port `9621`

## 2) Health check

```bash
curl -sS ${LIGHTRAG_BASE_URL:-http://127.0.0.1:9621}/health
```

## 3) Memory strategy

- Put long text/docs into LightRAG for semantic retrieval.
- Keep short critical facts (identity, preferences, commitments) in `MEMORY.md`.
- Keep recent chronology in `memory/YYYY-MM-DD.md`.

## 4) Failure fallback

If server is down:
1. restart server,
2. save critical item to `memory/YYYY-MM-DD.md` immediately,
3. retry ingestion later.
