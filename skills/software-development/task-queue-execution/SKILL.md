---
name: task-queue-execution
version: 1.0.0
description: "Ralph-inspired execution loop: takes a plan from writing-plans, converts to machine-readable task queue JSON, then executes one task per iteration with fresh subagent. Priority-ordered, dependency-aware, with progress tracking between iterations."
author: Hermes Agent (adapted from snarktank/ralph loop pattern)
tags: [execution, task-queue, loop, ralph, progress, automation]
---

# Task Queue Execution — Ralph-Style Loop

## Overview

Execute implementation plans using a **Ralph-inspired loop**: convert plan into a machine-readable task queue, then work through tasks one-by-one with fresh subagents per iteration, tracking progress persistently.

**Core principle:** Plan once, queue once, execute one task at a time. Each iteration is a fresh agent with clean context. Progress persists in a machine-readable queue file.

## When to Use

Use this skill when you have a plan (from `writing-plans`) with 3+ tasks that:
- Are mostly independent or have one-directional dependencies
- Need to be executed one at a time
- Benefit from fresh context per task (no accumulated state)
- Would be risky to batch-execute (large plan, long implementation)

**Don't use this for:** 1-2 task plans (just use subagent-driven-development directly), tasks that genuinely need cross-task context, or research tasks that build on each other.

## The Task Queue Format

A machine-readable JSON queue at `.hermes/task-queue.json`:

```json
{
  "project": "Feature X",
  "description": "Full feature description from plan",
  "tasks": [
    {
      "id": "T-001",
      "title": "Create User model with email and password_hash",
      "description": "As a developer, I want a User model...",
      "acceptanceCriteria": [
        "User model exists in src/models/user.py",
        "Has email (unique) and password_hash fields",
        "Uses bcrypt for password hashing",
        "Tests pass"
      ],
      "priority": 1,
      "dependencies": [],
      "passes": false,
      "notes": "",
      "files": ["src/models/user.py", "tests/models/test_user.py"]
    },
    {
      "id": "T-002",
      "title": "Add password validation",
      "description": "As a user, I want password validation...",
      "acceptanceCriteria": [
        "Min 8 characters enforced",
        "Meaningful error message",
        "Tests pass"
      ],
      "priority": 2,
      "dependencies": ["T-001"],
      "passes": false,
      "notes": "",
      "files": ["src/auth/validation.py", "tests/auth/test_validation.py"]
    }
  ],
  "status": {
    "total": 8,
    "completed": 0,
    "failed": 0,
    "currentTask": "T-001"
  }
}
```

### Field Rules

| Field | Rule |
|---|---|
| `id` | `T-001`, `T-002`, etc. — unique, sequential |
| `priority` | 1 = highest, executed first. Must be unique per task. |
| `dependencies` | Array of task IDs that must be `passes: true` before this starts |
| `passes` | `false` = not done, `true` = completed and verified |
| `files` | Expected files this task touches — used for verification |
| `notes` | Learnings for future iterations (like Ralph's `progress.txt`) |

### Priority Rules

- Tasks with **dependencies** must have **higher priority number** (lower priority) than their dependencies
- Example: T-002 depends on T-001 → T-001 priority=1, T-002 priority=2
- This ensures dependency tasks run first
- Ties broken by declaration order in the plan

## The Process

### Phase 1: Create Queue from Plan

```python
# 1. Read the plan
plan = read_file("docs/plans/feature-plan.md")

# 2. Extract all tasks from the plan
# Each task needs: title, description, acceptance criteria, priority, dependencies, files

# 3. Create the queue JSON
# Save to .hermes/task-queue.json

# 4. Mark Phase 1 complete
```

### Phase 2: Write Initial Progress Log

```python
write_file(".hermes/task-queue-progress.md", """# Task Queue Progress
Project: Feature X
Started: 2024-01-01T10:00:00Z
Status: IN PROGRESS

## Task Queue
See `.hermes/task-queue.json` for full queue.

## Learnings & Patterns
(Accumulated across iterations)
""")
```

### Phase 3: Execute Loop

For each iteration:

```python
# Step 1: Read current queue
queue = read_file(".hermes/task-queue.json")
# Parse JSON

# Step 2: Find next task
# - Priority 1..N (lowest number first)
# - passes: false
# - All dependencies passes: true
# - Skip failed tasks (report them)

# Step 3: Mark current task
queue["status"]["currentTask"] = task["id"]

# Step 4: Dispatch implementer subagent
result = delegate_task(
    goal=f"Implement Task {task['id']}: {task['title']}",
    context=f"""
    TASK FROM QUEUE:
    ID: {task['id']}
    Title: {task['title']}
    Description: {task['description']}
    Acceptance Criteria:
    {chr(10).join('- ' + ac for ac in task['acceptanceCriteria'])}
    Files: {', '.join(task['files'])}
    
    Notes from previous iterations:
    {task.get('notes', 'None yet')}
    
    PROJECT CONTEXT:
    {project_context}
    
    INSTRUCTIONS:
    1. Follow TDD: write failing test first, then implement
    2. Only implement THIS task — no scope creep
    3. Run tests to verify
    4. Commit with message: "feat: [{task['id']}] {task['title']}"
    5. Report: what was done, any issues found
    """,
    toolsets=['terminal', 'file']
)

# Step 5: Verify task completion
verification = delegate_task(
    goal=f"Verify Task {task['id']} is complete",
    context=f"""
    TASK: {task['title']}
    ACCEPTANCE CRITERIA:
    {chr(10).join('- ' + ac for ac in task['acceptanceCriteria'])}
    
    FILES EXPECTED: {', '.join(task['files'])}
    
    CHECK:
    - [ ] All acceptance criteria met
    - [ ] Files exist at expected paths
    - [ ] Tests pass for this task
    - [ ] No unintended changes outside task scope
    - [ ] Nothing extra added (scope creep check)
    
    OUTPUT: PASS or list specific failures
    """,
    toolsets=['file', 'terminal']
)

# Step 6: Update queue
if verification == "PASS":
    task["passes"] = True
    task["notes"] = extract_learnings(result)
    queue["status"]["completed"] += 1
else:
    task["notes"] = f"FAILED: {verification}"
    queue["status"]["failed"] += 1
    # Decide: retry or skip
    if queue["status"]["failed"] <= max_retries:
        # Retry — don't mark passes
        pass
    else:
        # Skip after max retries
        task["passes"] = True  # Mark to skip
        queue["status"]["failed"] += 1

# Step 7: Update progress log
append_to_progress_log(task["id"], task["title"], result, verification)

# Step 8: Write updated queue
write_file(".hermes/task-queue.json", updated_queue)
```

### Phase 4: Complete

```python
# After all tasks done:
queue["status"]["status"] = "COMPLETED"  # or "COMPLETED_WITH_FAILURES"

write_file(".hermes/task-queue.json", updated_queue)

append_to_progress_log("SUMMARY", f"""
All {total} tasks processed:
- Completed: {completed}
- Failed: {failed}
- Pass rate: {completed/total*100:.0f}%

Learnings Summary:
{all_learnings}
""")
```

## Story Sizing Discipline

**Each task must be completable in ONE subagent invocation (one context window).**

### Right-sized (examples):
- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list
- Create one model file
- Wire up one API endpoint

### Too big (must split):
- ❌ "Build the entire dashboard" → Split into: schema, queries, UI components, filters
- ❌ "Add authentication" → Split into: schema, middleware, login UI, session handling
- ❌ "Refactor the API" → Split into one task per endpoint or pattern

**Rule of thumb:** If you can't describe the change in 2-3 sentences, it's too big for one task.

## Dependencies

Rules for `dependencies` array:

1. **Dependencies must have LOWER priority numbers** (run first)
2. **No circular dependencies** — the queue creator validates this
3. **Keep dependencies minimal** — if T-003 doesn't truly need T-001's output, leave it empty
4. **Parallel execution** — tasks with no dependencies and same priority can run in parallel
5. **If dependencies get complex** (>3 deps on one task), the plan needs reorganization

## Integration with Hermes Skills

### With writing-plans
This skill EXECUTES plans. Workflow:
1. User requirements → `writing-plans` → implementation plan (`.md`)
2. Implementation plan → `task-queue-execution` Phase 1 → `.hermes/task-queue.json`
3. `.hermes/task-queue.json` → Phase 3 loop → working code

### With subagent-driven-development
Each iteration dispatches a `delegate_task` subagent to implement one task. The subagent gets:
- Full task spec (title, description, acceptance criteria)
- Files to touch
- Project context
- TDD instructions
- No cross-task state (fresh context)

### With test-driven-development
Include TDD instructions in every implementer context:
1. Write failing test first
2. Implement minimal code
3. Verify test passes
4. Check no regressions

### With hermes-stability-protocol
After each iteration:
1. Update `HERMES_TASK_CHECKPOINT.md`
2. Verify files exist at expected paths
3. Run tests
4. Commit before moving to next task

### With requesting-code-review
Each task goes through:
1. Implementer subagent
2. Verification subagent (checks acceptance criteria)
3. If needed, full code review via `requesting-code-review` skill

### With kanban-worker (optional)
For multi-profile setups, each task can become a Kanban card:
```python
kanban_create(
    title=f"Task {task['id']}: {task['title']}",
    assignee="worker-profile",
    body=f"Queue task. Files: {', '.join(task['files'])}",
    parents=[parent_card_id] if task['dependencies'] else []
)
```

## Progress Log Format

File: `.hermes/task-queue-progress.md`

```
# Task Queue Progress
Project: Feature X
Started: 2024-01-01T10:00:00
Status: IN PROGRESS

## Completed Tasks

### T-001: Create User model
- Implemented: User model with email (unique) and password_hash
- Tests: 3/3 passing
- Files: src/models/user.py, tests/models/test_user.py
- Learnings: None
---

### T-002: Add password validation
- Implemented: Validation function in auth/validation.py
- Tests: 5/5 passing
- Files: src/auth/validation.py, tests/auth/test_validation.py
- Learnings: MIN_PASSWORD_LENGTH should be a constant
---

## Failed Tasks
None

## Accumulated Learnings
- MIN_PASSWORD_LENGTH should be a constant, not magic number
- User model IDs use UUIDs, not auto-increment integers
- Test DB uses in-memory SQLite — import db_test.py for fixtures
---

## Final Status
Completed: 2/8 | Failed: 0/8
```

## Anti-Temptation Rules

- **Do NOT implement multiple tasks in one subagent** — one task per invocation
- **Do NOT skip verification** — always verify after each task
- **Do NOT accumulate state** — read queue fresh each iteration
- **Do NOT merge tasks** — if a task seems too small, it's fine; if too big, split
- **Do NOT skip scope creep check** — each task should only touch its declared files
- **Do NOT re-run completed tasks** — only `passes: false` tasks
- **Do NOT add dependencies retroactively** — plan dependencies before execution

## Pitfalls

**Stale queue file:** Always read the queue fresh each iteration. A previous run may have updated it.

**Context pollution:** The parent session should NOT carry code from previous tasks. Read queue → dispatch subagent → update queue → repeat.

**Over-ambitious tasks:** If a task keeps failing, it's probably too big. Split it and update the queue.

**Silent scope creep:** Subagents may add extra features. Always run scope creep check in verification.

**Lost learnings:** Always extract learnings from each subagent's output and store in queue. Next iteration's subagent gets these.

**Dependency deadlock:** If T-003 depends on T-002 which depends on T-001, but T-001 priority=2 and T-002 priority=1, the loop deadlocks. Validate priority ordering.

## Comparison: Ralph vs This Skill

| Ralph (original) | This skill (Hermes) |
|---|---|
| Bash loop → fresh CLI | Python loop → fresh `delegate_task` subagent |
| `prd.json` | `.hermes/task-queue.json` |
| `progress.txt` | `.hermes/task-queue-progress.md` |
| Supports Amp / Claude Code | Uses Hermes subagents |
| No verification subagent | Has verification subagent per task |
| Just commits blindly | Checks scope creep, runs tests |
| No retry logic | Max retries before skipping |
| No dependency validation | Validates priority ordering |
| Standalone project | Integrated with Hermes skills |

## Quickstart

```python
# 1. From a writing-plans document:
# Read plan → convert to queue JSON → save

# 2. Start the loop:
queue = load_queue()
while len([t for t in queue["tasks"] if not t["passes"]]) > 0:
    task = find_next_task(queue)
    if not task:
        break
    
    # Implement
    implement(task)
    
    # Verify
    if verify(task):
        mark_done(task, queue)
    else:
        mark_failed(task, queue)
    
    # Update
    save_queue(queue)
    update_checkpoint()

# 3. Report
summarize(queue)
```

**Remember:** Fresh subagent per task. One task per iteration. Queue is the source of truth.
