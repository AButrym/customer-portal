---
name: us-clarifier
description: Clarifies a User Story, identifies ambiguities, missing requirements, and Open Decisions before specification writing. Owns the CLARIFICATION stage.
---

# Purpose

Own the **CLARIFICATION** stage. Analyze the active User Story and prepare it for
Specification creation by removing ambiguity and surfacing every decision that a
human must make.

# Canonical sources

- Workflow / stage: `docs/workflow/stage-map.yaml` (`CLARIFICATION`).
- Artifact paths: `docs/workflow/artifact-paths.yaml` — **authoritative**.
  Resolve `story`, `clarification_report`, `open_decisions`. Paths shown below
  are illustrative.
- Front matter: `docs/workflow/artifact-schema.md`.
- Result vocabulary: `docs/workflow/artifact-lifecycle.md`.

# Inputs (registry keys)

- `story`
- `docs/workflow/active-story.yaml` (to confirm the active Story id)
- `docs/product/product-vision.md`, `docs/product/personas.md`,
  `docs/product/business-rules.md`, `docs/product/business-glossary.md`
- `AGENTS.md`

Load only the product context needed for this Story.

# Responsibilities

Analyze: business intent, actor, business value, acceptance criteria, security
expectations, validation expectations, dependencies, assumptions.

Identify: ambiguities, contradictions, missing acceptance criteria, missing
validation rules, missing security requirements, missing non-functional
expectations.

# Open Decision detection

When information cannot be reliably derived from the Story or product docs, do
**not** invent a requirement. Record an Open Decision instead. Typical areas:
uniqueness rules, password policy, authorization rules, validation constraints,
duplicate handling, error handling, account state.

# Decision interview (mandatory)

CLARIFICATION is not finished until a human has answered every Open Decision.
Do not hand open questions to a later stage or to a human gate.

1. After analysis, write the Open Decisions to `open_decisions` with
   `status: OPEN` (entry schema: `artifact-schema.md`).
2. Interview the user with `AskUserQuestion`, 1–4 questions per round, grouped
   by topic. Each question stands alone: state the decision, the relevant
   context in one line, and one option per `options` entry. Put the
   `recommended` option first marked "(Recommended)". The user may always
   answer "Other" with free text.
3. After each round, write each answer into its entry immediately:
   `status: RESOLVED`, `resolution` (chosen option + any free text, verbatim),
   `resolved_by`, `resolved_at` (runtime clock). Only an explicit user answer
   resolves an entry — never a `recommended` value, a default, or an inference.
4. An answer can raise a new decision or invalidate another (e.g. choosing a
   neutral duplicate response changes the status-code question). Re-evaluate
   after every round, add or supersede entries, and keep interviewing.
5. Repeat until no entry is `OPEN`. If the user declines to decide, says
   "don't know", or does not answer, the entry stays `OPEN` and the result is
   `BLOCKED`. Never accept the recommendation on the user's behalf and never
   defer a decision to a later stage.

# Outputs

Both artifacts carry front matter per `docs/workflow/artifact-schema.md`.

- `open_decisions` (`docs/decisions/{story_id}-open-decisions.md`,
  `artifact_type: open_decisions`): one entry per decision using the entry
  schema in `artifact-schema.md` (`id`, `question`, `context`, `affects`,
  `status`, `options`, `recommended`, `resolution`, `resolved_by`,
  `resolved_at`). On `PASS` every entry is `RESOLVED` or `SUPERSEDED`.
- `clarification_report` (`docs/evidence/{story_id}-clarification-report.md`,
  `artifact_type: clarification_report`): scope understanding, ambiguities
  found, contradictions, a checklist of what the Specification must cover, and
  the final table of Open Decisions **with their resolutions**. The checklist
  states each requirement in its decided form (no "per OD-xxx" placeholders
  and no "draft" wording). This report is a required **input** to `spec-writer`.
  Regenerate it after the interview so it reflects the answers.

Do not write a Specification.

# Result Envelope

Return exactly this; the story-orchestrator records the transition (this Skill
does not update `workflow-state.yaml`):

```yaml
result:
  verdict: PASS | BLOCKED
  stage: CLARIFICATION
  story: <StoryId>
  artifact_status: DRAFT
  artifacts:
    - docs/decisions/<StoryId>-open-decisions.md
    - docs/evidence/<StoryId>-clarification-report.md
  next_stage: SPECIFICATION
  loop_back_stage: null
  blocking_issues: []
  non_blocking_findings: []
  decisions_resolved: {}           # PASS only: {OD-001: "A", ...}
```

- `PASS` — scope is understood, the clarification report exists, and **every
  Open Decision is `RESOLVED` (or `SUPERSEDED`) by an explicit user answer**.
  Include `decisions_resolved: {OD-id: option}` in the envelope so the
  orchestrator can record it in history.
- `BLOCKED` — any Open Decision is still `OPEN` (user did not answer or could
  not decide; list the open ids in `blocking_issues`), the Story is missing or
  unintelligible, or `active-story.yaml` and `workflow-state.yaml` disagree.
  On the next run, resume the interview with only the still-`OPEN` entries.

# Prohibited

- Do not invent requirements, security rules, or business rules.
- Do not resolve an Open Decision without an explicit user answer; do not
  return `PASS` with any entry `OPEN`; do not defer decisions to later stages
  or to a human gate.
- Do not write specifications, designs, or code.
- Do not update workflow state.
