---
name: lightrag-memory-main
description: Use LightRAG as the primary external memory workflow for long-term knowledge capture and recall. Trigger when user asks to save memory, build memory bank, ingest notes/docs for future recall, query past knowledge semantically, or replace plain file-based memory with RAG memory.
---

# LightRAG Memory Main

Treat this skill as the default approach when user intent is **store/retrieve long-term memory** from documents, chat notes, SOP, or knowledge base.

## Operating Rule

- Use LightRAG-backed memory workflow first.
- Keep OpenClaw built-in `MEMORY.md` and `memory/*.md` for concise canonical facts and audit trail.
- Mirror critical saved items to both systems when possible:
  1) LightRAG (semantic retrieval),
  2) MEMORY.md/daily memory (deterministic recall and continuity).

## Quick Workflow

1. Setup once (if not ready): run `scripts/setup_lightrag.sh`.
2. Save memory/doc: run `scripts/memory_add.sh "<text>"`.
3. Query memory: run `scripts/memory_query.sh "<question>"`.
4. For bulk docs, place files under `data/` and ingest via server/API (see references).

## Required Env

- `OPENAI_API_KEY` (or compatible provider in `.env`)
- Optional: `LIGHTRAG_BASE_URL` (default: `http://127.0.0.1:9621`)

## Read next

- Setup and architecture: `references/setup-and-ops.md`
- API payload examples: `references/api-examples.md`
