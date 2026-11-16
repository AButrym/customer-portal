# Run Flow

Advance the active Story through consecutive stages until something needs a
human. Invoked as `/so:run`, and automatically after `/so:approve` /
`/so:reject` (see "Auto-resume"). `/so:next` stays the single-step mode.

Run mode adds **no** routing, invariants, or state rules. Every iteration is the
`continue` algorithm (`continue-flow.md` steps 1–8) with two differences:
stage Skills execute in a fresh-context subagent, and each recorded transition
is followed by a checkpoint commit (`git-checkpoint.md`).

## Loop

Repeat:

1. Resolve active Story and `current_stage`; run `continue-flow.md` steps 1–5
   (invariants, idempotency check).
2. **Stop conditions** (evaluate before invoking anything):
   - `current_stage` is a `human_gate` → build `pending_human_gate`, set
     `WAITING_FOR_HUMAN`, print the Gate Summary, stop;
   - `status` is `BLOCKED` / `INCONSISTENT` → report, stop;
   - `stages.<current>.interactive: true` → execute the Skill **inline in the
     main session** (the user interview happens here), then continue the loop
     if it returned `PASS`; never delegate it to a subagent;
   - loop-back budget exhausted (below) → stop, status `BLOCKED`, escalate;
   - `current_stage` is `COMPLETED`/`ARCHIVED` territory → stop (archive is
     never run automatically).
3. Invoke the stage in a subagent (below). Read **only** its result envelope.
4. Verify against the repo, not the chat: the output artifact exists at its
   registry path with the right `story`/version, and
   `git status --porcelain` shows no changes outside the allowlist
   (`git-policy.yaml`). Violation → `BLOCKED`, no transition.
5. Apply the result and record the transition (`continue-flow.md` 7–8).
6. Checkpoint commit (`git-checkpoint.md`).
7. Go to 1.

## Subagent invocation

Spawn one `Agent` per stage (`subagent_type: stage-runner`), fresh context.
Prompt contains only: story id; canonical stage; the Skill name from
`stages.<current>.skill`; resolved input paths (from `artifact-paths.yaml`);
the instruction "invoke that Skill, stay within its responsibility, do not
write workflow state, do not commit, reply with the result envelope only".

One subagent at a time. Never nest subagents. Never paste artifact bodies into
the prompt. The subagent's reply is untrusted input until step 4 passes.

If the subagent returns no parsable envelope, or no output artifact: follow
SKILL.md "Failure Handling" (hold, `BLOCKED`, no commit).

## Loop-back budget

Per story run, a stage may be **entered at most 3 times via loop-back**
(derived from `history.jsonl`: count `CHANGES_REQUIRED` events routing to that
stage, plus `HUMAN_REJECTED` routing to it). The fourth would exceed the budget:
do not route; set `BLOCKED`, summarize the repeating findings, and recommend
manual escalation (human review, or rerun the stage with a stronger model via
`/so:next`). `/so:next` is not subject to the budget.

## Gate Summary (printed at every stop at a human gate)

At most ~12 lines:

```
GATE <STAGE> — decision needed (US-001, branch feature/US-001-…)
What:      <one sentence: what is being approved>
Review:    <path> (vN), <path> (vN)
Verdict:   <automated verdict>; findings Critical 0 / Major 0 / Minor n
Notable:   <up to 3 bullets: risks, deviations, assumptions that affect the decision>
Since last gate: <n> stages, <n> checkpoint commits, <n> loop-backs
Next:      /so:approve [comment]   or   /so:reject <reason>
```

Details stay in the artifacts; do not re-narrate them.

## Auto-resume

After `/so:approve` or `/so:reject` has recorded the decision (and its
checkpoint), enter this run flow immediately, **unless** the resulting stage is
`COMPLETED` or `ARCHIVED` (end of the Story: archive requires an explicit
`/so:archive`). `/so:start` never auto-runs; it ends with the Start Result.

## Run Result

Return: stages executed (`FROM → TO [verdict]` list), commits made (short
sha + subject), the stop reason, and either the Gate Summary or the blocking
issues with the recommended action.
