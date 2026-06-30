# ECC (Everything Claude Code) Agent Patterns

> Adapted from [affaan-m/ECC](https://github.com/affaan-m/ECC) — 220k★ agent harness operating system.

## Overview

ECC is a production-ready AI coding plugin by Affaan Mustafa (Anthropic hackathon winner).
It provides 67 specialized agents, 271 skills, and 92 commands for Claude Code, Codex,
OpenCode, Cursor, and other coding agents.

This reference extracts the patterns most relevant to Hermes subagent orchestration.

## Agent Catalog (Notable)

| Agent | Trigger | Delegation Pattern |
|-------|---------|-------------------|
| planner | Complex feature requests | Break into phases, identify dependencies & risks |
| architect | Architectural decisions | System design, scalability analysis, trade-off docs |
| tdd-guide | Bug fix or new feature | RED-GREEN-REFACTOR, 80%+ coverage, evidence report |
| code-reviewer | After writing/modifying code | Quality, maintainability, inline comments |
| security-reviewer | Security-sensitive code | Vulnerability detection, OWASP Top 10 |
| spec-miner | Brownfield project onboarding | Extract spec from existing code, reverse-engineer intent |
| build-error-resolver | Build/type errors | Incremental fix, verify after each fix |
| e2e-runner | Critical user flows | Playwright E2E, page objects, cross-browser |
| refactor-cleaner | Dead code cleanup | Static analysis, dependency graph, safe deletion |
| doc-updater | Documentation sync | Codemaps, API docs, README, changelog |
| loop-operator | Autonomous loop execution | Monitor stalls, intervene on infinite loops |
| harness-optimizer | Config tuning | Reliability, cost, throughput optimization |

## Agent Orchestration Rules (from ECC SOUL.md)

1. **Agent-First** — route work to the right specialist as early as possible.
2. **Test-Driven** — write or refresh tests before trusting implementation changes.
3. **Security-First** — validate inputs, protect secrets, and keep safe defaults.
4. **Immutability** — prefer explicit state transitions over mutation.
5. **Plan Before Execute** — complex changes should be broken into deliberate phases.

## Verification Loop (Full Pipeline)

ECC enforces a structured verification after every feature:

```
Phase 1: Build Verification  — compile/transpile check
Phase 2: Type Check          — static type analysis
Phase 3: Lint Check          — code style & quality rules
Phase 4: Test Run            — unit + integration + E2E
Phase 5: Security Scan       — dependency audit + SAST
Phase 6: Evidence Report     — summary of what passed/failed
```

## Continuous Learning Architecture (v2.1)

ECC has a formal instinct-based learning system:

1. **Observation phase**: Hook captures PreToolUse/PostToolUse events per session.
2. **Analysis phase**: Background agent extracts atomic "instincts" (one trigger, one action).
3. **Confidence scoring**: 0.3 (tentative) → 0.9 (near-certain) based on repetition count + user correction signals.
4. **Domain tagging**: code-style, testing, git, debugging, workflow, architecture.
5. **Scope isolation**: v2.1+ separates project-scoped instincts from global ones.
6. **Evolution pipeline**: Instincts → cluster of related instincts → skill/command/agent.

Instinct example:
```yaml
id: prefer-functions-over-classes
trigger: "when writing new modules"
confidence: 0.7
domain: code-style
scope: project
project_id: a1b2c3d4e5f6
project_name: my-app
---
# Prefer Functions

## Action
Use functional patterns over classes when appropriate.

## Evidence
- Observed 5 instances of functional pattern preference
- User corrected class-based approach to functional on 2025-01-15
```

This maps loosely to Hermes' memory + skill_manage system. Memory = instincts
(atomic facts), skill_manage = evolution pipeline (instinct → skill).

## Cross-Skill References

- ECC's `skills/()` contain 271 workflow skills — Hermes has comparable coverage
  in its own skills directory.
- ECC's `hooks/` system (60+ Node.js hooks) maps to Hermes' gateway hooks
  and builtin_hooks extension point.
- ECC's `commands/` (92 slash commands) maps to Hermes' slash command registry.
- ECC's `rules/` maps to Hermes' `AGENTS.md`, `CLAUDE.md`, and guardrail skills.

## Key Difference

ECC is designed for **Claude Code CLI** (interactive coding agent).
Hermes is designed for **persistent multi-platform agent** (Telegram, Discord, CLI, web).
The patterns translate but the deployment model differs — ECC hooks are per-session
shell scripts, Hermes hooks are per-event gateway extensions.
