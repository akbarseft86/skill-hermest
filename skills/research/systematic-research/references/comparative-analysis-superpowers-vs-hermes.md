# Superpowers vs Hermes Skills — Content-Level Comparison Notes

## Context

User asked about `obra/superpowers` and corrected the assistant to inspect actual contents, not only titles: "cek isinya bukan hanya judul".

This reference captures the durable comparison pattern and key findings from reading actual skill content.

## External System: obra/superpowers

Repo: `github.com/obra/superpowers`

Observed Superpowers skill directories:

- `brainstorming`
- `dispatching-parallel-agents`
- `executing-plans`
- `finishing-a-development-branch`
- `receiving-code-review`
- `requesting-code-review`
- `subagent-driven-development`
- `systematic-debugging`
- `test-driven-development`
- `using-git-worktrees`
- `using-superpowers`
- `verification-before-completion`
- `writing-plans`
- `writing-skills`

## Key Content Findings

### 1. Hermes Already Ports Some Superpowers Skills

Hermes skills `writing-plans` and `test-driven-development` include metadata indicating they are adapted from `obra/superpowers`.

Implication: do not describe Superpowers as a pure competitor. It is also an upstream methodological source for some Hermes skills.

### 2. Superpowers' Strongest Methodological Ideas

- **Brainstorming before implementation**: use before creative work, avoid the "too simple to need design" anti-pattern.
- **Writing plans**: bite-sized tasks, exact files/commands, TDD-first, handoff-ready.
- **TDD**: strict RED-GREEN-REFACTOR with an iron law: no production code without a failing test.
- **Systematic debugging**: root cause before fix.
- **Verification before completion**: evidence before claims.
- **Using Superpowers**: hard meta-enforcement — if a skill applies, invoke it.
- **Receiving code review**: verify feedback before implementing; avoid reflexively agreeing or rejecting.

### 3. Hermes Advantages

Hermes has a much broader full-agent stack:

- Native tool system
- Persistent memory
- Gateway platforms
- Cron jobs
- Kanban / delegate_task orchestration
- More skills across domains
- Hermes Stability Protocol with stronger operational guardrails than Superpowers' verification skill
- Meta Ads / Scalev / business integrations

### 4. Gap Worth Porting

Superpowers has `receiving-code-review`; Hermes has strong code review requesting/reviewing skills but lacks a dedicated skill for receiving and processing review feedback.

Potential future action: add or adapt a class-level `receiving-code-review` skill under the GitHub/software-development category.

## Comparison Rule Learned

When comparing skills/frameworks:

1. Read the actual SKILL.md or source files.
2. Compare mechanisms, rules, anti-patterns, and enforcement — not names.
3. Check metadata/provenance before declaring one system independent of another.
4. Produce a dimension-by-dimension table with gaps and suggested action.

## User Preference Signal

Akbar expects depth-first evaluation. If he challenges comparison quality, fix the exact weakness immediately: inspect actual contents and report evidence tersely.
