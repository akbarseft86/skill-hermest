---
name: agent-skills-eval
description: Use when evaluating whether an AI agent skill actually improves agent output, not just "looks smart". Build before publishing HTML/demo artifacts.
version: 1.0.0
author: Hermest CEO
---

# Agent Skills Eval

Use this skill when the task is about testing whether an AI Agent is genuinely better after loading a skill, or when turning a screenshot/post about AgentSkillsEval into a proper Hermest workflow.

## Core Idea

An agent skill should be tested by comparing outputs:

1. **Baseline run** — agent answers the same prompt without the skill.
2. **Skill-loaded run** — agent answers with the target skill loaded.
3. **Evaluation** — compare both outputs using clear rubrics.

The goal is to prove the skill gives operational advantage, not just extra text.

## Evaluation Workflow

1. Define the task prompt clearly.
2. Run the prompt without the skill.
3. Run the same prompt with the skill loaded.
4. Score both outputs on:
   - correctness
   - specificity
   - procedural accuracy
   - tool/path awareness
   - constraint adherence
   - verification discipline
   - usefulness to the user
5. Record concrete differences: what improved, what got worse, what stayed generic.
6. Patch the skill if the skill-loaded output still misses important steps.

## Scoring Rubric

Use 1–5 scale per dimension:

- **1** = generic, wrong, or unsafe
- **2** = partially useful but misses key constraints
- **3** = acceptable but not clearly skill-enhanced
- **4** = skill clearly improves workflow and accuracy
- **5** = strong operational advantage with verification and pitfalls handled

## Output Template

```markdown
# Skill Evaluation: <skill-name>

## Prompt Tested
<prompt>

## Baseline Result Summary
- Strengths:
- Weaknesses:

## Skill-Loaded Result Summary
- Strengths:
- Weaknesses:

## Score Table
| Dimension | Baseline | With Skill | Delta | Notes |
|---|---:|---:|---:|---|
| Correctness | | | | |
| Specificity | | | | |
| Procedure | | | | |
| Tool/path awareness | | | | |
| Constraints | | | | |
| Verification | | | | |
| User usefulness | | | | |

## Verdict
- Keep / patch / retire skill:
- Patch needed:
```

## Publishing Rule

If the user asks to make a demo/HTML from a screenshot about a skill or agent workflow:

1. Create or update the relevant Hermest skill first.
2. Only publish HTML if the user explicitly asks for a public artifact after the skill exists.
3. Do not clutter `/var/www/html/` with temporary demos unless the user explicitly wants a public link.

## Pitfalls

- Do not assume a GitHub repo exists from a social screenshot. Verify the URL first.
- If search backend is down, use direct GitHub/browser/API checks and clearly state uncertainty.
- Do not publish first and rationalize later; if the content is about skills, codify the workflow into Hermest skill first.
