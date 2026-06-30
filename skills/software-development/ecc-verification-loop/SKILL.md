---
name: ecc-verification-loop
description: Use after completing code changes, before PR, or after refactoring. Quality gate from ECC — build, typecheck, lint, test, security scan, and diff review with evidence report.
version: 1.0.0
author: Hermes Agent (extracted from affaan-m/ECC)
license: MIT
metadata:
  hermes:
    tags: [ecc, verification, quality-gate, testing, code-review]
    related_skills: [requesting-code-review, test-driven-development, hermes-stability-protocol, karpathy-guidelines]
---

# ECC Verification Loop

> Extracted from `affaan-m/ECC` (Everything Claude Code, 220k★, MIT).
> Source: `skills/verification-loop/SKILL.md`

## Overview

Comprehensive verification system dari ECC — 6 fase quality gate: build, typecheck, lint, test, security scan, dan diff review. Setiap fase harus PASS sebelum lanjut.

## When to Use

- Setelah menyelesaikan feature atau significant code change
- Sebelum membuat PR
- Setelah refactoring
- Saat ingin memastikan quality gates pass

## Verification Phases

Jalankan berurutan. **STOP dan fix** di setiap fase sebelum lanjut.

### Phase 1: Build Verification

```bash
# Node/JS
npm run build 2>&1 | tail -20
pnpm build 2>&1 | tail -20

# Python
python -c "import <main_package>" 2>&1

# Go
go build ./... 2>&1

# Rust
cargo build 2>&1 | tail -20
```

Build FAIL → STOP. Fix dulu.

### Phase 2: Type Check

```bash
# TypeScript
npx tsc --noEmit 2>&1 | head -30

# Python
pyright . 2>&1 | head -30
mypy . 2>&1 | head -30

# Rust
cargo check 2>&1 | head -30
```

Critical type errors → STOP. Warnings → catat.

### Phase 3: Lint Check

```bash
# JS/TS
npm run lint 2>&1 | head -30
npx eslint . 2>&1 | head -30

# Python
ruff check . 2>&1 | head -30
flake8 . 2>&1 | head -30

# Go
golint ./... 2>&1 | head -30

# Rust
cargo clippy 2>&1 | head -30
```

Fix semua lint errors. Jangan commit dengan lint errors.

### Phase 4: Test Suite

```bash
# Node
npm test 2>&1 | tail -50
npm run test -- --coverage 2>&1 | tail -50

# Python
pytest -v 2>&1 | tail -50
pytest --cov=. 2>&1 | tail -50

# Go
go test ./... -v 2>&1 | tail -50
```

**Target coverage: 80% minimum.**

Report:
- Total tests: N
- Passed: N
- Failed: N
- Coverage: N%

Ada test fail → STOP. Fix.

### Phase 5: Security Scan

```bash
# Hardcoded secrets
grep -rn "sk-\|api_key\|API_KEY\|apikey\|password\|PASSWORD\|secret\|SECRET\|token\|TOKEN" --include="*.py" --include="*.ts" --include="*.js" . 2>/dev/null | head -10

# Debug leftovers
grep -rn "console.log\|console.debug\|print(" --include="*.ts" --include="*.tsx" src/ 2>/dev/null | head -10
grep -rn "print(" --include="*.py" src/ 2>/dev/null | head -10

# eval/exec
grep -rn "\beval\b\|\bexec\b" --include="*.py" --include="*.js" --include="*.ts" src/ 2>/dev/null | head -10
```

Security issues = **CRITICAL**. Wajib fix semua.

### Phase 6: Diff Review

```bash
git diff --stat
git diff --name-only
```

Review setiap file untuk:
- Unintended changes
- Missing error handling
- Potential edge cases
- Dead code / commented code
- Magic numbers / hardcoded values

## Output Format

```
VERIFICATION REPORT
==================

Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...

Files Changed:
- path/to/file.ts — [minor/medium/critical] what changed
```

## Common Pitfalls

1. **Skip fase karena "bentaran aja"** — jangan. Satu fase gagal = cascade error.
2. **Security scan dianggap opsional** — ini paling penting untuk production code.
3. **Cuma liat test pass, tapi coverage rendah** — false sense of security.
4. **Diff review dilewatin** — unintended changes paling bahaya karena silent.

## Verification Checklist

- [ ] Build PASS
- [ ] Typecheck PASS (critical errors = 0)
- [ ] Lint PASS (errors = 0)
- [ ] Tests PASS (coverage ≥ 80%)
- [ ] Security PASS (0 critical issues)
- [ ] Diff review selesai (no unintended changes)
- [ ] Verification report dihasilkan
