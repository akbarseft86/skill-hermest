---
name: ecc-continuous-learning
description: Use when learning new patterns from sessions. Instinct-based learning from ECC — observe sessions, create atomic instincts with confidence scoring, promote to skills when confident enough.
version: 1.0.0
author: Hermes Agent (extracted from affaan-m/ECC)
license: MIT
metadata:
  hermes:
    tags: [ecc, learning, instincts, patterns, knowledge]
    related_skills: [ecc-verification-loop, ecc-guardrails, karpathy-guidelines]
---

# ECC Continuous Learning — Instinct-Based Architecture

> Extracted from `affaan-m/ECC` (Everything Claude Code, 220k★, MIT).
> Source: `skills/continuous-learning-v2/SKILL.md`

## Overview

ECC memiliki sistem **instinct-based learning**: observasi sesi, deteksi pola, simpan sebagai "instinct" kecil dengan confidence score, lalu evolve jadi skill penuh kalau pola terus berulang.

Ini adalah panduan untuk menerapkan pola yang sama di Hermes menggunakan tools yang sudah ada (`memory`, `skill_manage`, `session_search`).

## When to Use

- Saat menemukan pola berulang dalam sesi coding
- Setelah user mengoreksi/memperbaiki approach
- Saat workflow tertentu dilakukan lebih dari 2x
- Saat ada teknik/pattern yang solve masalah lebih baik
- Saat ada project-specific convention yang perlu diingat

## The Instinct Model (from ECC)

ECC mendefinisikan instinct sebagai **atomic learned behavior**:

```yaml
id: prefer-functional-style
trigger: "when writing new functions"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project

# Prefer Functional Style

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2025-01-15
```

**Properties:**
- **Atomic** — satu trigger, satu action
- **Confidence-weighted** — 0.3 = tentative, 0.9 = near certain
- **Domain-tagged** — code-style, testing, git, debugging, workflow, dsb
- **Evidence-backed** — track apa yang membuatnya tercipta
- **Scope-aware** — `project` atau `global`

## Hermes Implementation

### Level 1: Memory (Intuisi / "instinct" ringan)

Untuk pola yang baru muncul 1-2x, simpan ke `memory` sebagai fakta deklaratif:

```python
memory(action="add", target="memory",
       content="User prefers functional patterns over classes in this project.")
```

Properti:
- Minimal effort
- Auto-injected di every session
- Tapi nggak structured — nggak ada trigger/confidence

### Level 2: Skill (Instinct matang / evolved)

Untuk pola yang sudah confirmed (user koreksi 2-3x atau pattern muncul 3+ kali), bikin skill:

```python
# Check apakah sudah perlu dijadikan skill
# Kriteria:
# - Sudah disimpan di memory 3+ kali terkait topic sama
# - User menegaskan "ingat ini" atau "catat ini"
# - Pola / workflow terjadi berulang

skill_manage(action="create", name="<nama>",
            category="software-development",
            content="...")
```

### Level 3: Skill Update (Evolution)

Ketika menemukan instruksi yang lebih baik dari skill yang sudah ada:

```python
skill_manage(action="patch", name="<nama>",
            old_string="<teks_lama>",
            new_string="<teks_baru>")
```

## Confidence Scoring (ECC mapping for Hermes)

| Score | ECC Meaning | Hermes Action |
|-------|-------------|---------------|
| 0.3 | Tentative | Simpan ke memory saja. Jangan dijadikan skill. |
| 0.5 | Moderate | Catat di memory dengan trigger context. |
| 0.7 | Strong | Bisa dijadikan skill jika pattern berguna untuk masa depan. |
| 0.9 | Near-certain | **WAJIB** bikin skill — ini core behavior. |

**Confidence naik** saat:
- Pola terlihat berulang
- User nggak mengoreksi
- Instinct lain setuju

**Confidence turun** saat:
- User eksplisit mengoreksi
- Pola tidak terlihat dalam waktu lama
- Ada kontradiksi

## Scope Decision (proyek vs global)

| Pattern Type | Scope | Contoh |
|-------------|-------|--------|
| Language/framework conventions | project | "Gunakan React hooks", "ORM Django patterns" |
| File structure preferences | project | "Test di direktori tests/" |
| Code style | project | "Pakai functional style" |
| Error handling strategies | project | "Gunakan Result type untuk error" |
| Security practices | **global** | "Validate user input", "Sanitize SQL" |
| General best practices | **global** | "Write tests first" |
| Tool workflow preferences | **global** | "Grep sebelum Edit" |
| Git practices | **global** | "Conventional commits" |

## When to Evolve Instinct → Skill

ECC menggunakan aturan:
1. Instinct yang sama muncul di 2+ project → auto-promote ke global
2. Confidence ≥ 0.7 → siap dijadikan skill
3. Flow kompleks (5+ langkah) → layak dijadikan skill

Hermes equivalent:
1. Pattern muncul 3+ kali dalam sesi berbeda → save as `memory`
2. User bilang "jangan lupa ini" / "catat" → langsung simpan
3. Workflow 5+ tool calls + berhasil → offer to save as skill
4. Skill yang sudah ada tapi outdated → patch immediately

## Privacy (dari ECC)

- Observations stay **local** — semua memory & skill Hermes sudah lokal
- Project-scoped instincts terisolasi per project
- Hanya **patterns** (bukan raw data) yang disimpan
- Tidak ada code atau percakapan yang dibagikan
- User kontrol penuh apa yang di-save

## Common Pitfalls

1. **Semua pola langsung dijadikan skill** — nggak semua. Confident dulu.
2. **Nggak pernah update skill** — skill yang outdated lebih berbahaya daripada tidak punya skill.
3. **Memory overload** — jangan simpan task progress ke memory. Simpan fakta durable.
4. **Skip project scope** — nggak semua pattern layak global. Kalau spesifik framework/language, biarkan di project scope (memory).

## Verification Checklist

- [ ] Pattern sudah muncul cukup sering (min 3x) sebelum jadi skill
- [ ] Confidence ≥ 0.7 sebelum promosi ke skill
- [ ] Memory nggak diisi task progress / temporary state
- [ ] Project-scoped patterns nggak dipromosi ke global
- [ ] Skill yang outdated sudah di-patch
