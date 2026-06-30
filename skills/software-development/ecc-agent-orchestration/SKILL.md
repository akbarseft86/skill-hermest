---
name: ecc-agent-orchestration
description: Use when deciding how to route coding work. Agent orchestration from ECC — delegate to specialized agents proactively based on task type, not one-size-fits-all.
version: 1.0.0
author: Hermes Agent (extracted from affaan-m/ECC)
license: MIT
metadata:
  hermes:
    tags: [ecc, orchestration, agents, delegation, workflow]
    related_skills: [subagent-driven-development, writing-plans, requesting-code-review, test-driven-development]
---

# ECC Agent Orchestration

> Extracted from `affaan-m/ECC` (Everything Claude Code, 220k★, MIT).
> Source: `AGENTS.md` — 67 specialized agents, 271 skills, 92 commands

## Overview

ECC menggunakan prinsip **Agent-First**: delegasikan ke specialist agent sesuai domain task, bukan handle semuanya sendiri. Ini adalah routing table untuk menentukan agent mana yang harus dipanggil untuk tiap jenis task.

## When to Use

- Memulai task coding baru — tanya dulu: "ini butuh agent apa?"
- Setelah selesai nulis code — siapa yang review?
- Ada error build — siapa yang fix?
- Ada keputusan arsitektur — siapa yang konsultasi?
- Security-sensitive code — siapa yang audit?

## Core Principles (dari ECC)

1. **Agent-First** — route work ke specialist sedini mungkin
2. **Test-Driven** — tulis/refresh test sebelum percaya perubahan
3. **Security-First** — validasi input, lindungi secret, safe defaults
4. **Immutability** — prefer explicit state transitions over mutation
5. **Plan Before Execute** — complex changes dipecah jadi deliberate phases

## Routing Rules (ECC → Hermes delegate_task)

### Coding & Development

| Task Type | ECC Agent | Hermes Equivalent |
|-----------|-----------|-------------------|
| Complex features, refactoring | planner | `skill_view("writing-plans")` → plan dulu |
| Architectural decisions | architect | `delegate_task` + goal = "evaluate architecture" |
| Bug fix, new feature | tdd-guide | `skill_view("test-driven-development")` |
| After writing/modifying code | code-reviewer | `skill_view("requesting-code-review")` |
| Brownfield project onboarding | spec-miner | Extract existing patterns via `search_files` + docs |

### Review & Security

| Task Type | ECC Agent | Hermes Equivalent |
|-----------|-----------|-------------------|
| Code quality & maintainability | code-reviewer | `delegate_task` with `requesting-code-review` skill |
| Vulnerability detection | security-reviewer | `skill_view("ecc-guardrails")` + search for secrets |
| Python code review | python-reviewer | `delegate_task` + "review this Python code for issues" |
| Django code review | django-reviewer | `delegate_task` + "review Django ORM/DRF patterns" |
| TypeScript/JS review | typescript-reviewer | `delegate_task` + "review this TypeScript code" |
| Rust code review | rust-reviewer | `delegate_task` + "review this Rust code" |
| Go code review | go-reviewer | `delegate_task` + "review this Go code" |
| Java/Spring Boot review | java-reviewer | `delegate_task` + "review this Java/Spring Boot code" |
| C/C++ review | cpp-reviewer | `delegate_task` + "review this C/C++ code" |
| Database schema/query | database-reviewer | `delegate_task` + "review this PostgreSQL schema/query" |

### Build & Error Resolution

| Task Type | ECC Agent | Hermes Equivalent |
|-----------|-----------|-------------------|
| Build failures | build-error-resolver | `delegate_task` + error output + "fix this build" |
| TypeScript build errors | typescript-reviewer | `delegate_task` + tsc errors |
| Python/Django errors | django-build-resolver | `delegate_task` + traceback |
| Rust build errors | rust-build-resolver | `delegate_task` + cargo errors |
| Go build errors | go-build-resolver | `delegate_task` + go build output |
| PyTorch/CUDA errors | pytorch-build-resolver | `delegate_task` + CUDA traceback |
| Java build errors | java-build-resolver | `delegate_task` + Maven/Gradle output |

### Testing & Quality

| Task Type | ECC Agent | Hermes Equivalent |
|-----------|-----------|-------------------|
| E2E testing | e2e-runner | `delegate_task` + "write Playwright E2E tests" |
| Dead code cleanup | refactor-cleaner | `delegate_task` + "find and remove dead code" |
| Documentation update | doc-updater | `delegate_task` + "update docs/codemaps" |
| Verification pass | (verification-loop) | `skill_view("ecc-verification-loop")` |

### Specialized

| Task Type | ECC Agent | Hermes Equivalent |
|-----------|-----------|-------------------|
| ML pipeline review | mle-reviewer | `delegate_task` + "review ML pipeline" |
| Loop monitoring | loop-operator | `delegate_task` + "monitor this loop for stalls" |
| Harness config tuning | harness-optimizer | `delegate_task` + "optimize config for reliability/cost" |

## Agent Orchestration Flow

```
Task masuk
   │
   ▼
[Routing Decision]
   │
   ├── Complex/multi-file → planning task → delegate_task (planner-like)
   ├── Bug fix / feature → skill_view("test-driven-development")
   ├── Architecture → delegate_task architect
   ├── Security-sensitive → skill_view("ecc-guardrails") + review
   │
   ▼
[Execution]
   │
   ▼
[Post-Execution Review]
   ├── Code written/modified → skill_view("requesting-code-review")
   ├── Build success → skill_view("ecc-verification-loop")
   │
   ▼
[Commit]
   └── Conventional commit
```

## Parallel Execution

ECC menyarankan parallel execution untuk independent operations.
Pakai `delegate_task(tasks=[...])` untuk menjalankan multiple agent sekaligus:

```python
# Parallel: review + test + docs simultaneously
delegate_task(tasks=[
    {"goal": "Review code quality of PR X", "toolsets": ["terminal", "file"]},
    {"goal": "Run test suite and report coverage", "toolsets": ["terminal"]},
    {"goal": "Update API documentation for changes", "toolsets": ["terminal", "file"]},
])
```

Maksimal **3 parallel tasks** untuk user ini.

## Security Guidelines from ECC

**Before ANY commit (ECC rule):**
- No hardcoded secrets (API keys, passwords, tokens)
- All user inputs validated
- SQL injection prevention (parameterized queries)
- XSS prevention (sanitized HTML)
- CSRF protection enabled
- Authentication/authorization verified
- Rate limiting on all endpoints
- Error messages don't leak sensitive data

**If security issue found:**
STOP → `skill_view("ecc-guardrails")` → fix CRITICAL issues → rotate exposed secrets → review codebase for similar issues

## Coding Style from ECC

- **Immutability**: Always create new objects, never mutate
- **File organization**: Small focused files (200-400 lines, max 800)
- **Organize by feature/domain**, not by type
- **Error handling**: Handle at every level. Never silently swallow errors
- **Input validation**: Validate at boundaries, fail fast, never trust external data
- **Functions**: < 50 lines, no nesting > 4 levels

## Common Pitfalls

1. **Handle everything sendiri** — ECC prinsipnya "agent-first". Kalau task besar, route ke specialist.
2. **Skip review setelah coding** — "ah cuman ganti dikit" justru paling sering error.
3. **Nggak parallel-in** — independent tasks jalanin parallel, jangan sequential.
4. **Security review cuma sekali** — security harus ada di setiap fase, bukan cuma final.

## Verification Checklist

- [ ] Task di-routing ke agent/approach yang sesuai
- [ ] Complex feature → planning dulu
- [ ] Code written → review
- [ ] Security-sensitive → audit
- [ ] Build errors → resolve
- [ ] Verification loop jalan
