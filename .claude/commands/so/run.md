---
description: Run the active User Story through consecutive stages (fresh-context subagents) until a human gate or blocker.
argument-hint: ""
---

Invoke the story-orchestrator Skill in run mode (load
`references/run-flow.md` and `references/git-checkpoint.md`).

Requirements:

- process only the active User Story, on its story branch;
- each automated stage Skill runs in its own fresh-context `stage-runner`
  subagent; the CLARIFICATION interview runs inline in this session;
- only story-orchestrator writes workflow state and makes checkpoint commits;
- verify each stage's artifacts and changed files before recording it;
- stop at every human gate (never pass one), on BLOCKED/INCONSISTENT, or when
  the loop-back budget (3) is exhausted;
- at a human gate print the short Gate Summary and the exact `/so:approve` /
  `/so:reject` command;
- never push, create or merge a Pull Request, or run archive;
- finish with the Run Result.
