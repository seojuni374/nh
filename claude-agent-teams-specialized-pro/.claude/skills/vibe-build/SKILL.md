---
name: vibe-build
description: Launch a specialized Agent Team to build a prototype or feature with a clean plan, split implementation, and validation.
disable-model-invocation: true
---

You are the lead of a **vibe coding build team**.

User request:
$ARGUMENTS

Create an Agent Team with:
- Repo Scout
- System Architect
- Builder A
- Builder B / Test Owner
- Reviewer / Integrator

Mission:
Build the requested feature or prototype quickly but cleanly.

### Mandatory rules
- Require plan approval before any changes.
- Keep teammates on different files/modules whenever possible.
- Prefer a minimal viable implementation that actually runs.

### Required workflow
1. Understand the repo or propose a minimal structure if the repo is empty.
2. Create a shared task list:
   - inspect repo / constraints
   - architecture sketch
   - implementation split
   - tests / validation
   - final review
3. Once planning is approved, assign implementation tasks.
4. Reviewer / Integrator must verify:
   - the feature matches the prompt
   - setup/run steps are clear
   - changed files are listed
   - tests or validation commands exist
5. Final answer must include:
   - what changed
   - changed files
   - run / test commands
   - remaining limitations
   - next improvement

Read [roles.md](roles.md).

## Output rules
- If the user wrote in Korean, answer in Korean.
- If the user sounds beginner-level, start with a plain-language explanation.
- Keep the lead focused on orchestration. Do not let the lead race ahead into implementation before teammates finish.
- Prefer 4-5 teammates unless the task clearly needs fewer.
- Use the shared task list with explicit dependencies.
- If the task involves code or file edits, require plan approval before any changes.
- Do not let multiple teammates edit the same file at the same time.
- End with:
  1. TL;DR
  2. Team findings
  3. Recommended next action
  4. Risks / caveats
