# Project operating rules for Claude Code Agent Teams

## What this repo is
This repository is a starter kit for **specialized Agent Teams** in Claude Code.

The main slash commands are:
- `/route-task`
- `/quant-research`
- `/quant-build`
- `/competition-design`
- `/competition-pitch`
- `/econ-explain`
- `/econ-policy`
- `/vibe-build`
- `/vibe-refactor`
- `/audit-final`
- `/full-pipeline`

## Global rules
1. Default to **Korean** when the user writes in Korean.
2. If the user sounds beginner-level, explain the result in:
   - one plain-language summary
   - one action checklist
   - one "copy this" prompt block
3. Use **Agent Teams only when parallel work is actually valuable**.
4. Prefer **4-5 teammates** plus the lead.
5. Never let multiple teammates edit the **same file at the same time**.
6. For risky coding tasks, require **plan approval before any changes**.
7. The lead should **wait for teammates** to finish before synthesizing.
8. Every final answer should end with:
   - Final recommendation
   - Main reasons
   - Risks / caveats
   - Next 3 actions
9. If a team already exists, do not create another one in the same session. Clean up first.
10. If the user asks for a quick, safe answer, prefer a single session over a team.

## Domain rules

### Quant / AI trading
- Do not overstate backtest results.
- Explicitly check for data leakage, survivorship bias, look-ahead bias, unrealistic fills, and regime instability.
- Separate:
  - idea generation
  - data assumptions
  - validation
  - execution / risk
- Treat any live-trading suggestion as a proposal to validate, not a guaranteed edge.

### Competition design
- Optimize for:
  - problem clarity
  - novelty
  - feasibility in the user's time/resource constraints
  - measurable evaluation
  - judge-perspective persuasion
- Distinguish "cool idea" from "winnable submission".

### Economics
- Separate theory, evidence, assumptions, and policy implications.
- If evidence is thin, say so.
- If the user asks for easy explanation, avoid jargon first.

### Vibe coding
- Start with repository understanding and a simple architecture sketch.
- Assign files or modules cleanly.
- Require tests or at least a validation checklist before calling work done.

## Clean output formats
When helpful, structure outputs as:
- TL;DR
- Team findings
- Decision
- Risks
- Next steps
