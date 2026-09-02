---
artifact_type: reconciliation
story: US-001
version: 3
status: IN_REVIEW
created_at: 2026-08-31T12:52:00Z
updated_at: 2026-09-02T16:10:00Z
produced_by: reconciliation-reviewer
inputs:
  - path: docs/stories/US-001-register-customer.md
    version: null
  - path: docs/decisions/US-001-open-decisions.md
    version: 2
  - path: docs/evidence/US-001-clarification-report.md
    version: 2
  - path: docs/specifications/US-001-spec.md
    version: 1
  - path: docs/reviews/specifications/US-001-spec-review.md
    version: 1
  - path: docs/designs/api/US-001-api-design.md
    version: 1
  - path: docs/designs/api/US-001-openapi.yaml
    version: 1
  - path: docs/designs/database/US-001-db-design.md
    version: 1
  - path: docs/designs/database/US-001-entity-model.md
    version: 1
  - path: docs/reviews/designs/US-001-design-review.md
    version: 1
  - path: docs/impact-analysis/US-001-impact-analysis.md
    version: 1
  - path: docs/plans/US-001-implementation-plan.md
    version: 1
  - path: docs/reviews/plans/US-001-plan-review.md
    version: 1
  - path: docs/tests/US-001-test-strategy.md
    version: 1
  - path: docs/tests/US-001-ac-test-matrix.md
    version: 1
  - path: docs/evidence/US-001-test-generation-report.md
    version: 1
  - path: docs/evidence/US-001-implementation-report.md
    version: 2
  - path: docs/verification/US-001-implementation-verification.md
    version: 2
  - path: docs/reviews/security/US-001-security-review.md
    version: 2
supersedes: docs/reviews/reconciliation/US-001-reconciliation.md
reconciled_acceptance_criteria: 7
total_acceptance_criteria: 7
critical_findings: 0
major_findings: 1
minor_findings: 2
informational_findings: 3
candidate_files: 52
excluded_files: 0
---

# Reconciliation — US-001 Customer Registration  (v3)

> **v3 re-run (RECONCILIATION occurrence 3).** The human-mandated post-correction
> sequence after the `HUMAN_PR_APPROVAL` rejection of 2026-09-01
> (`docs/workflow/history.jsonl`, `verdict: HUMAN_REJECTED`, decided_by
> `ayubutrym@gmail.com`) is complete for the code side: reconciliation v2 routed
> `implementation_drift` → `IMPLEMENTATION`; the corrective pass
> (`implementation_report` v2, attempt 2) applied RC-1, RC-3, RC-9 (code half)
> and RC-10; `implementation_verification` v2 (PASS, 67/67) and `security_review`
> v2 (PASS, 0 Critical / 0 Major) independently confirmed them. This version
> supersedes reconciliation v2 + traceability v2 (both `IN_REVIEW`, stale — they
> consumed `implementation_report` / `implementation_verification` /
> `security_review` **v1**).

## 0. Disposition of the six original rejection items (final state)

| Item | Summary | Status in v3 |
|---|---|---|
| REJECT-1 | Reconciliation v1 finding counts inconsistent | **CLOSED** — fixed in v2; v3 front matter / §1 / §16 / §17 / §21 / envelope all agree (0 Critical, 1 Major, 2 Minor, 3 Informational). |
| REJECT-2 | `open_decisions.md` must be published v2, OD-001..OD-006 RESOLVED | **CLOSED** — `docs/decisions/US-001-open-decisions.md` v2 + `docs/evidence/US-001-clarification-report.md` v2 (`status: APPROVED`, all six `RESOLVED`, `OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A`), committed in `7ad07e1`. `security_review` v2 §21 confirms F-4 CLOSED. |
| REJECT-3 | `RegistrationRequest.toString()` renders the plaintext password — add masking + a proving test | **CLOSED (RC-1)** — masking `toString()` (`password=***`) + `RegistrationRequestTest` (3 tests). Verified: `implementation_verification` v2 §7/§12 (v1 MF-5 CLOSED), `security_review` v2 §7 (v1 F-1 CLOSED). |
| REJECT-4 | Map the `uq_customer_email` race to `409` without over-catching; deterministic test | **CLOSED (RC-3)** — constraint-scoped `DataIntegrityViolationException` catch in `CustomerService.register` → `DuplicateEmailException` → `409`; unrelated integrity violations rethrown; `CustomerServiceTest` +2 (positive + `isSameAs` negative). Verified: `implementation_verification` v2 §7/§17 (v1 MF-3 CLOSED), `security_review` v2 §11 (v1 F-3 CLOSED). |
| REJECT-5 | Resolve the SC-4 "deny-by-default" wording/behaviour ambiguity — literal `denyAll()` **or** document that the approved policy means authentication-required by default; tests must match | **PARTIALLY CLOSED (RC-9).** Code half done — `SecurityConfig` javadoc + inline comment aligned to "authentication-required by default (SC-4) … not a literal `denyAll()`"; `anyRequest().authenticated()` unchanged; `RegistrationSecurityPostureTest` green. **Documentation half NOT done** — `docs/specifications/US-001-spec.md:135` (SEC-1 row) and `docs/designs/api/US-001-api-design.md:138` / `:174` still read "deny-by-default (SC-4)" without the clarifying note. This is the sole blocking item in v3 → **finding RC-9, Major**, routed `specification_gap` → `SPECIFICATION`. |
| REJECT-6 | Reconciliation PR accounting must distinguish story / harness-maintenance / excluded changes; classify the stray `src/main/.../docs/hooks/tool-usage.jsonl` | **CLOSED** — §15 three-category accounting retained and refreshed; the stray file was **removed** in the corrective pass (RC-10, confirmed absent by `implementation_verification` v2 §4 and `security_review` v2 §17). `excluded_files: 0`. |

## 1. Executive Summary

**Verdict: CHANGES_REQUIRED — loop back to `SPECIFICATION` (`specification_gap`).**

The US-001 implementation is functionally complete, correct, secure, and fully
traced. All seven Acceptance Criteria are `RECONCILED` in `traceability` v3
(AC-002 and AC-004 — `PARTIALLY_RECONCILED` in v2 — are now closed by the
verified RC-3 and RC-1 corrections). Build + 67 tests reproduced independently by
`implementation-verifier` v2. `implementation_verification` v2 and
`security_review` v2 are current (consumed `implementation_report` v2 +
`open_decisions` v2) and both `PASS` with zero Critical/Major findings.

**One human-mandated correction is still incomplete.** REJECT-5 (the SC-4
wording resolution) required *either* literal `denyAll()` *or* documenting that
the approved policy means authentication-required by default. The implementer
chose the "document" path and aligned the `SecurityConfig` code comment — but the
matching one-line note was **not** added to the two artifacts the human's wording
points at:

- `docs/specifications/US-001-spec.md` §7, SEC-1 row (line 135) — still
  *"every other endpoint remains deny-by-default."*
- `docs/designs/api/US-001-api-design.md` §6 (line 138) — still *"Every other
  endpoint remains deny-by-default (SC-4)"*; §8 conventions checklist (line 174)
  — still *"SC-4 deny-by-default, registration public"*.

Both downstream reviewers flagged this and explicitly instructed this stage:
`security_review` v2 SR-1 and `implementation_verification` v2 MF-a both state
**"RECONCILIATION must not record RC-9 as closed until the note is published, and
must route it via `specification_gap` → `SPECIFICATION` and/or `design_gap` →
`API_DESIGN`."** Neither reviewer could route it themselves — their loop-backs do
not reach the owning stages.

- **Security / behaviour risk of the open item: none.** `security-conventions.md`
  SC-4's own text is *"every endpoint requires authentication unless the approved
  API design lists it as public"*, which is exactly what
  `anyRequest().authenticated()` enforces. The code is SC-4-compliant; the spec /
  api-design phrasing is merely less explicit than the human required. This is a
  documentation-consistency gap on a **Major**, human-mandated item — not a
  security defect.
- **Loop-back target — earliest responsible stage.** SR-1 names both
  `SPECIFICATION` (spec §7) and `API_DESIGN` (api-design §6 / §8). Per the
  orchestrator's Loop-Back Precedence rule, the earliest stage in `stage_order`
  wins: `SPECIFICATION` (index 2) over `API_DESIGN` (index 5). Routing to
  `API_DESIGN` alone would leave `spec §7` unfixed — the cheaper correction, not
  the correct one. Re-entering `SPECIFICATION` cascades back through
  `SPEC_REVIEW` → `HUMAN_SPEC_APPROVAL` → `API_DESIGN` → … so both artifacts
  receive their note in one pass.
- **Consequence the human should expect:** the loop-back re-opens
  `SPECIFICATION`, which means `SPEC_REVIEW` and the **`HUMAN_SPEC_APPROVAL`
  human gate** run again, then `API_DESIGN`, `DB_DESIGN`, `DESIGN_REVIEW`,
  `IMPACT_ANALYSIS`, `IMPLEMENTATION_PLANNING`, `PLAN_REVIEW`, the
  **`HUMAN_PLAN_APPROVAL` human gate**, `TEST_WRITING`, `IMPLEMENTATION`,
  `IMPLEMENTATION_VERIFICATION`, `SECURITY_REVIEW`, and `RECONCILIATION` — the
  full pipeline, for a one-line wording note. `stage-map.yaml` provides no
  shorter path; the alternative is a human override at `HUMAN_PR_APPROVAL`
  accepting the phrasing as-is (the code is already SC-4-compliant and both
  automated reviews are `PASS` on everything else).
- **Findings:** 0 Critical, **1 Major** (RC-9 — documentation half of a
  human-mandated correction), 2 Minor (RC-2, RC-3-residual = `security_review`
  v2 SR-3), 3 Informational (RC-5, RC-6, RC-7). Previously-open RC-1, RC-3,
  RC-4, RC-8, RC-10 are all **CLOSED**.
- **PR candidate scope:** 52 tracked files, all INCLUDE — 49 US-001 story
  changes + 3 harness-maintenance (`docs/workflow/history.jsonl`,
  `docs/workflow/workflow-state.yaml`, `docs/evidence/.gitignore`). **0 excluded
  files** (the RC-10 stray file was removed). No secret, no generated DB file in
  the include set. Working tree clean.

**Recommended next action:** `SPECIFICATION` — `spec-writer` adds the one-line
SC-4 clarifying note to `docs/specifications/US-001-spec.md` §7 (SEC-1 row); the
cascade re-runs `API_DESIGN` where `openapi-designer` adds the matching note to
`docs/designs/api/US-001-api-design.md` §6 / §8. All other artifacts are current
and re-approve without content change.

## 2. Artifact Inventory

| Artifact | Path | Type | Ver | Status | Current | Mandatory | Producing stage |
|---|---|---|---|---|---|---|---|
| Story | docs/stories/US-001-register-customer.md | story | (unversioned) | active | yes | yes | BACKLOG_SYNC / human |
| Open Decisions | docs/decisions/US-001-open-decisions.md | open_decisions | 2 | APPROVED (all six RESOLVED) | yes | yes | CLARIFICATION |
| Clarification Report | docs/evidence/US-001-clarification-report.md | clarification_report | 2 | APPROVED | yes | yes | CLARIFICATION |
| Specification | docs/specifications/US-001-spec.md | specification | 1 | APPROVED | yes (**needs RC-9 note — see §14 / §17**) | yes | SPECIFICATION |
| Specification Review | docs/reviews/specifications/US-001-spec-review.md | specification_review | 1 | APPROVED (PASS) | yes | yes | SPEC_REVIEW |
| API Design | docs/designs/api/US-001-api-design.md | api_design | 1 | APPROVED | yes (**needs RC-9 note — see §14 / §17**) | yes | API_DESIGN |
| OpenAPI Contract | docs/designs/api/US-001-openapi.yaml | openapi | 1 | APPROVED | yes | yes | API_DESIGN |
| DB Design | docs/designs/database/US-001-db-design.md | database_design | 1 | APPROVED | yes | yes | DB_DESIGN |
| Entity Model | docs/designs/database/US-001-entity-model.md | entity_model | 1 | APPROVED | yes | yes | DB_DESIGN |
| Design Review | docs/reviews/designs/US-001-design-review.md | design_review | 1 | APPROVED (PASS) | yes | yes | DESIGN_REVIEW |
| Impact Analysis | docs/impact-analysis/US-001-impact-analysis.md | impact_analysis | 1 | DRAFT (PASS; no review stage follows) | yes | yes | IMPACT_ANALYSIS |
| Implementation Plan | docs/plans/US-001-implementation-plan.md | implementation_plan | 1 | APPROVED (PASS + HUMAN_PLAN_APPROVAL) | yes | yes | IMPLEMENTATION_PLANNING |
| Plan Review | docs/reviews/plans/US-001-plan-review.md | plan_review | 1 | APPROVED (PASS) | yes | yes | PLAN_REVIEW |
| Test Strategy | docs/tests/US-001-test-strategy.md | test_strategy | 1 | DRAFT | yes | yes | TEST_WRITING |
| AC–Test Matrix | docs/tests/US-001-ac-test-matrix.md | ac_test_matrix | 1 | DRAFT | yes | yes | TEST_WRITING |
| Test-Generation Report | docs/evidence/US-001-test-generation-report.md | test_generation_report | 1 | DRAFT | yes | yes | TEST_WRITING |
| Implementation Report | docs/evidence/US-001-implementation-report.md | implementation_report | 2 | DRAFT (corrective pass; supersedes v1) | yes | yes | IMPLEMENTATION |
| Implementation Verification | docs/verification/US-001-implementation-verification.md | implementation_verification | 2 | DRAFT front matter / PASS verdict (supersedes v1) | yes | yes | IMPLEMENTATION_VERIFICATION |
| Security Review | docs/reviews/security/US-001-security-review.md | security_review | 2 | APPROVED (PASS; supersedes v1) | yes | yes | SECURITY_REVIEW |
| Reconciliation | docs/reviews/reconciliation/US-001-reconciliation.md | reconciliation | 3 | this artifact (supersedes v2) | — | — | RECONCILIATION |
| Traceability | docs/reconciliation/US-001-traceability.md | traceability | 3 | this artifact's pair (supersedes v2) | — | — | RECONCILIATION |

- **Missing mandatory artifacts:** none.
- **Duplicate current artifacts:** none. Reconciliation v1/v2 + traceability
  v1/v2 are `supersedes` targets of this pair.
- **Stale artifacts:** none blocking. `implementation_report` v1,
  `implementation_verification` v1, `security_review` v1, `open_decisions` v1 and
  `clarification_report` v1 are all superseded by current versions consumed here.
  The carried `open_decisions` v1→v2 front-matter references in `specification`
  v1 / `implementation_plan` v1 / `ac_test_matrix` v1 remain a **noted, waived**
  lag (`open_decisions` v2 change-log: "No decision content changed") — see §14.
- **Wrong Story id / wrong path / superseded reference:** none.

### Artifact chain validation

Story → Specification → Spec Review → API/DB Designs → Design Review → Impact
Analysis → Plan → Plan Review → Test artifacts → Implementation Report (v2) →
Implementation Verification (v2) → Security Review (v2) is intact. `history.jsonl`
records both human gates (`HUMAN_SPEC_APPROVAL` 2026-08-31T07:48:48Z with
`OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A`, `HUMAN_PLAN_APPROVAL`
2026-08-31T11:20:00Z), the `HUMAN_PR_APPROVAL` rejection (2026-09-01T08:41:01Z),
the `implementation_drift` loop-back (2026-09-02T14:02:21Z), and the mandated
re-run of `IMPLEMENTATION` → `IMPLEMENTATION_VERIFICATION` → `SECURITY_REVIEW`
(2026-09-02T14:52 / 15:04 / 15:40). Every downstream re-run consumed the current
upstream version. No superseded input feeds a current review.

## 3. Source-of-Truth Review

| Item | Finding |
|---|---|
| Story origin | `active-story.yaml` `source.type: local_only`; no GitHub Issue configured or reachable. |
| Remote Issue inspected | No — nothing to sync. GitHub MCP not used (correct). |
| Local Story | `docs/stories/US-001-register-customer.md` — documented source of truth. |
| Source-of-truth policy | Local Story artifact is authoritative when no GitHub source exists. |
| Synchronization differences | None — single local source. |
| Required action | None. No `story_source_conflict`; no `BACKLOG_SYNC` loop-back. |

## 4. Acceptance Criteria Traceability Matrix

See `docs/reconciliation/US-001-traceability.md` v3 (owned by this stage).

Summary: **AC-001..AC-007 all `RECONCILED`.** No `PARTIALLY_RECONCILED`, no
`NOT_RECONCILED`, no `BLOCKED` at the Acceptance-Criterion level. The
security-posture row **SEC-1 / SC-4 is `PARTIALLY_RECONCILED`** — the RC-9
documentation half is unpublished (drives the verdict). SEC-3 is now
`RECONCILED` (RC-1 closed).

## 5. Specification and Design Alignment

| Check | Result |
|---|---|
| Specification → OpenAPI | Consistent (`POST /api/v1/customers`, `RegistrationRequest`/`CustomerResponse`, `201` + `Location`, `400/409/415/500`). |
| Specification → DB design | Consistent (FR-5 fields ↔ `customer` columns; `uq_customer_email`; `password_hash VARCHAR(60)`; UTC audit). |
| Design → implementation (API) | Consistent in shape / status / auth. Deviation RC-2 (error `message` strings vs illustrative OpenAPI examples) is documentation-direction, unchanged; `409` message matches the contract verbatim (including the RC-3 concurrent path, which routes into the same `409`). |
| Design → implementation (persistence) | Consistent. `ddl-auto=validate` boots clean. RC-3 adds no schema element — `uq_customer_email` already exists. |
| **SC-4 wording (RC-9 / REJECT-5)** | **Not aligned.** `security/SecurityConfig.java` javadoc + inline comment now say "authentication-required by default (SC-4) … not a literal `denyAll()`" — correct and SC-4-compliant. `docs/specifications/US-001-spec.md:135` and `docs/designs/api/US-001-api-design.md:138` / `:174` still say "deny-by-default (SC-4)" without the clarifying note. The human (REJECT-5) required the documentation to state the policy means authentication-required by default. → finding RC-9, Major, `specification_gap` → `SPECIFICATION`. |

## 6. Predicted Versus Actual Impact

The delivered change set matches `impact-analysis` §5–§6 predictions (packages
`config`, `controller`, `exception`, `model.dto`, `model.entity`,
`model.request`, `repository`, `security`, `service`, `validation`, plus the
test tree, `schema.sql`, `application*.yaml`, `build.gradle.kts` M-1). The
corrective pass added only: a `toString()` override on `RegistrationRequest`
(RC-1), a `DataIntegrityViolationException` catch + `isEmailUniquenessViolation`
in `CustomerService` (RC-3), a `SecurityConfig` comment reword (RC-9 code half),
and removal of the stray `docs/` subtree under the package root (RC-10) — all
within already-predicted packages, no new package, no new declared dependency
(`org.hibernate.exception.ConstraintViolationException` is transitive via
`spring-boot-starter-data-jpa`; `build.gradle.kts` diff `7ad07e1..6c7d9e8`
empty).

### Actual changed items not individually predicted

| File / component | Classification | Justification |
|---|---|---|
| `exception/InvalidPasswordException` | Required Supporting Change | FR-6 / SC-1 service re-check; disclosed D-1; accepted by `implementation_verification` v2 and `security_review` v2. |
| `src/test/.../persistence/CustomerSchemaTest.java` — 2 dummy-BCrypt-literal chars | Unexpected but Justified (test-fixture fix, from IMPLEMENTATION attempt 1) | No assertion / scenario / outcome changed. |
| `.gitignore` `/docs/harness-consistency-review.md`; `docs/evidence/.gitignore` (4 `harness-*` entries + BOM) | **Harness-maintenance** — committed in `a96ebd5` | Not US-001 functional scope. See §15 category (b) / finding RC-8 (now closed / recorded). |
| `docs/workflow/history.jsonl`, `docs/workflow/workflow-state.yaml` | Harness-maintenance — owned by `story-orchestrator` | Updated at every transition. See §15 category (b). |

## 7. Plan Versus Implementation

Every plan step C-1..C-16 and M-1..M-4 remains implemented (carried from
reconciliation v2 §7). The RC-1 / RC-3 / RC-9 corrections are *additions* to
C-6 / C-11 / C-12 / C-14 driven by the human review, not a plan defect —
consistent with the `implementation_drift` (not `plan_gap`) loop-back that
produced them. The RC-9 documentation half is a `specification_gap`: the
Specification omits the clarifying wording the human required, so the earliest
responsible stage is `SPECIFICATION`.

## 8. Test Reconciliation

| | Detail |
|---|---|
| Actual tests | 8 suites, **67 tests**; `./gradlew clean build` BUILD SUCCESSFUL, 0 failures / 0 errors / 0 skipped — independently reproduced by `implementation-verifier` v2 (per-suite counts from `build/test-results/test/TEST-*.xml`). |
| Delta vs v1 baseline (62 / 7) | +5: 3 `model.request.RegistrationRequestTest` (RC-1), 2 `service.CustomerServiceTest` (RC-3, positive + `isSameAs` negative). |
| Coverage the human made mandatory | **REJECT-3** — `RegistrationRequestTest` proves the submitted plaintext is never rendered by `toString()`, null-safe, accessor unchanged. **REJECT-4** — `CustomerServiceTest.concurrentDuplicateEmailUniqueViolationIsMappedToDuplicateEmailException` + `.anUnrelatedIntegrityViolationIsNotReportedAsADuplicateEmail` (load-bearing). Both present and green. |
| RC-9 test impact | None. Option 1 (align wording) keeps `anyRequest().authenticated()`; `RegistrationSecurityPostureTest` unchanged (one doc comment reworded), 4/4 green. |
| Test-writer-owned tests | No assertion / scenario weakened, disabled, or relaxed (`git diff 7ad07e1..6c7d9e8 -- src/test/` = additions + one reworded comment). |
| No `test_gap` | Every AC has a real-stack test; the RC-9 residual needs no test. |

## 9. API Reconciliation

No contract-shape drift. RC-2 (implemented `400` / `415` `message` strings vs
the OpenAPI *illustrative* `examples`; `409` matches exactly) remains Minor /
documentation-direction — carried as `security_review` v2 SR-2. The RC-3
concurrent-duplicate path routes into the **same** `DuplicateEmailException` →
`handleDuplicateEmail` → `409` + `"An account with this email already exists."`,
bringing runtime behaviour closer to the contract, not further from it. No new
status code, no new response shape.

## 10. Persistence Reconciliation

Every column, constraint, identity strategy, and audit behaviour matches DB
design v1 / entity-model v1, verified against a booted H2 datasource
(`CustomerSchemaTest` 10 tests / `CustomerPersistenceTest` 3 tests). RC-7 (`id`
DDL has no explicit `NOT NULL`) stays Informational. RC-3 changes only the
exception-to-HTTP mapping; `uq_customer_email` was already present and already
prevented the duplicate row. `security_review` v2 SR-3 (the
`isEmailUniquenessViolation` name + message-token heuristic) is a Minor
robustness note with no reachable exploit path — carried, no loop-back.

## 11. Architecture Reconciliation

Layering, single `@RestControllerAdvice`, DTO/entity boundary, validation split,
config placement, package ownership all conform
(`semantic_analysis: TEXT_FALLBACK`; import-graph + signature inspection). The
RC-3 catch uses `org.springframework.dao.DataIntegrityViolationException` +
`org.hibernate.exception.ConstraintViolationException` — persistence/DAO types,
not `org.springframework.http` / servlet types; the domain `DuplicateEmailException`
carries the HTTP mapping to the advice. No HTTP type entered the service; no new
architectural layer; no new declared dependency. `implementation_verification`
v2 §10 and `security_review` v2 §6 concur.

## 12. Security Reconciliation

| Item | Detail |
|---|---|
| Security Review version | `docs/reviews/security/US-001-security-review.md` **v2**, `status: APPROVED`, verdict PASS (0 Critical, 0 Major, 3 Minor SR-1/SR-2/SR-3, 2 Informational SR-4/SR-5). |
| Currency | **Current.** v2 consumed `implementation_report` v2 + `implementation_verification` v2 + `open_decisions` v2. `git diff` shows no `src/**` change after the `SECURITY_REVIEW` v2 commit (`640850d`); working tree clean. Not stale — **no `BLOCKED` condition.** |
| v1 findings | F-1 CLOSED (RC-1), F-3 CLOSED (RC-3), F-4 CLOSED (`open_decisions` v2); F-2 survives as SR-2. |
| Security drift | None. RC-1 closes the latent `toString()` path; RC-3 makes the concurrent path behave identically to the pre-checked one; RC-9 code half aligns the comment without changing behaviour. |
| SR-1 (RC-9 doc half) | `security_review` v2 explicitly forwards this to RECONCILIATION with the instruction to route `specification_gap` / `design_gap` and **not** mark RC-9 closed. Adopted as finding RC-9 (Major) below. |

## 13. Configuration and Dependency Reconciliation

No undocumented dependency, no undocumented configuration. `build.gradle.kts`,
`application.yaml`, `application-test.yaml`, `schema.sql`, `.gitignore` are
byte-for-byte unchanged in the corrective diff `7ad07e1..6c7d9e8`. RC-5 / RC-6
(`AUTO_SERVER` + blank H2 credential = `security_review` v2 SR-4 / SR-5) stay
Informational / approved-config. M-1 (`spring-boot-starter-validation`) is the
only added dependency, approved in the plan.

## 14. Documentation Reconciliation

| Document | State | Authority direction |
|---|---|---|
| `open_decisions.md` v2 / `clarification-report.md` v2 | **Current — RESOLVED, APPROVED, committed.** RC-4 CLOSED. | Documentation follows the recorded decision. |
| **`docs/specifications/US-001-spec.md` §7, SEC-1 row (line 135)** | **STALE for RC-9.** Reads *"every other endpoint remains deny-by-default."* Needs the note: *"'deny by default' here means authentication-required by default per SC-4 — `anyRequest().authenticated()`, not a literal `denyAll()`."* | **Documentation must be updated** to reflect the human-approved RC-9 resolution (REJECT-5). Owner: `spec-writer` / `SPECIFICATION`. → finding RC-9. |
| **`docs/designs/api/US-001-api-design.md` §6 (line 138) + §8 checklist (line 174)** | **STALE for RC-9.** §6: *"Every other endpoint remains deny-by-default (SC-4)"*; §8: *"SC-4 deny-by-default, registration public"*. Needs the same clarifying note. | **Documentation must be updated.** Owner: `openapi-designer` / `API_DESIGN` — picked up in the cascade from the `SPECIFICATION` loop-back. |
| OpenAPI contract v1 | Illustrative `400` / `415` `examples` differ from implemented `message` strings (RC-2 / SR-2). | Documentation *may* follow the implementation — optional, not required. |
| `SecurityConfig.java` javadoc / comment | **Current** — aligned to "authentication-required by default (SC-4)". | — |
| `specification` v1 / `implementation_plan` v1 / `ac_test_matrix` v1 front matter | Record `open_decisions` **v1**; current is v2. | **Waived** — `open_decisions` v2 change-log: "No decision content changed"; same six option letters; code used the resolved values throughout. Noted, not re-opened. When `SPECIFICATION` re-runs for RC-9, `spec-writer` may refresh the `specification` front-matter reference opportunistically; the plan / matrix references are out of RC-9's scope. |
| Implementation Report v2 / Verification v2 / Security Review v2 | Current — match the implementation. | — |

## 15. Pull Request Candidate Scope  (three-category accounting — REJECT-6)

**Counting convention:** one entry per **path**. `candidate_files` (52) = every
tracked file in `git diff --name-status 47e3016..HEAD` (branch base = `main`
merge-base `47e3016`). All 52 are INCLUDE, split into category (a) or (b).
`excluded_files` (**0**) — the RC-10 stray file was removed in the corrective
pass; the working tree is clean (`git status --short` empty); no untracked path
needs an action. Standard git-ignored paths (`/data/`, `build/`, `.gradle/`,
`.idea/`, `docs/hooks/`, pre-existing `harness-*`) are listed in (c) for
completeness, not counted. Counts are **as of this write**;
`docs/workflow/history.jsonl` and `docs/workflow/workflow-state.yaml` change
again when the RECONCILIATION → SPECIFICATION transition is recorded (they stay
category (b)), and `docs/reviews/reconciliation/US-001-reconciliation.md` +
`docs/reconciliation/US-001-traceability.md` are updated in place to v3 (already
in category (a), still counted once each). `pr-preparer` consumes this
classification and must not re-derive it.

### (a) US-001 story changes — INCLUDE  (49 paths)

**Production / build / configuration (29)**

- `src/main/java/org/example/customerportal/config/JpaAuditingConfig.java`
- `src/main/java/org/example/customerportal/controller/CustomerController.java`
- `src/main/java/org/example/customerportal/exception/DuplicateEmailException.java`
- `src/main/java/org/example/customerportal/exception/GlobalExceptionHandler.java`
- `src/main/java/org/example/customerportal/exception/InvalidPasswordException.java`
- `src/main/java/org/example/customerportal/model/dto/ApiFieldError.java`
- `src/main/java/org/example/customerportal/model/dto/CustomerResponse.java`
- `src/main/java/org/example/customerportal/model/dto/ErrorResponse.java`
- `src/main/java/org/example/customerportal/model/entity/Customer.java`
- `src/main/java/org/example/customerportal/model/entity/Role.java`
- `src/main/java/org/example/customerportal/model/request/RegistrationRequest.java`  *(RC-1: masking `toString()`)*
- `src/main/java/org/example/customerportal/repository/CustomerRepository.java`
- `src/main/java/org/example/customerportal/security/SecurityConfig.java`  *(RC-9 code half: comment reword)*
- `src/main/java/org/example/customerportal/service/CustomerService.java`  *(RC-3: constraint-scoped `409` mapping)*
- `src/main/java/org/example/customerportal/validation/PasswordPolicyValidator.java`
- `src/main/java/org/example/customerportal/validation/ValidPassword.java`
- `src/main/resources/schema.sql`
- `src/main/resources/application.yaml` (M)
- `src/test/java/org/example/customerportal/CustomerPortalApplicationTests.java` (M — M-4)
- `src/test/java/org/example/customerportal/model/request/RegistrationRequestTest.java`  *(new — RC-1, 3 tests)*
- `src/test/java/org/example/customerportal/persistence/CustomerPersistenceTest.java`
- `src/test/java/org/example/customerportal/persistence/CustomerSchemaTest.java`
- `src/test/java/org/example/customerportal/registration/CustomerRegistrationApiTest.java`
- `src/test/java/org/example/customerportal/security/RegistrationSecurityPostureTest.java`  *(1 comment reworded — RC-9)*
- `src/test/java/org/example/customerportal/service/CustomerServiceTest.java`  *(+2 tests — RC-3)*
- `src/test/java/org/example/customerportal/validation/PasswordPolicyValidatorTest.java`
- `src/test/resources/application-test.yaml`
- `build.gradle.kts` (M — M-1 `spring-boot-starter-validation`)
- `.gitignore` (M) — **counted here.** The `/data/` block is US-001 story scope
  (M-3); the trailing `/docs/harness-consistency-review.md` +
  `/docs/hooks/tool-usage.jsonl` lines are harness-maintenance (also noted under
  (b)). One path, counted once in (a).

*(Path count above: 29 — 16 `src/main/java` + 2 `src/main/resources` + 8 `src/test/java` + 1 `src/test/resources` + `build.gradle.kts` + `.gitignore`.)*

**US-001 workflow-doc artifacts (20)** —
`docs/decisions/US-001-open-decisions.md` (v2),
`docs/evidence/US-001-clarification-report.md` (v2),
`docs/evidence/US-001-implementation-report.md` (v2),
`docs/evidence/US-001-test-generation-report.md`,
`docs/specifications/US-001-spec.md`  *(will gain the RC-9 note in the loop-back)*,
`docs/reviews/specifications/US-001-spec-review.md`,
`docs/designs/api/US-001-api-design.md`  *(will gain the RC-9 note in the loop-back)*,
`docs/designs/api/US-001-openapi.yaml`,
`docs/designs/database/US-001-db-design.md`,
`docs/designs/database/US-001-entity-model.md`,
`docs/reviews/designs/US-001-design-review.md`,
`docs/impact-analysis/US-001-impact-analysis.md`,
`docs/plans/US-001-implementation-plan.md`,
`docs/reviews/plans/US-001-plan-review.md`,
`docs/tests/US-001-test-strategy.md`, `docs/tests/US-001-ac-test-matrix.md`,
`docs/verification/US-001-implementation-verification.md` (v2),
`docs/reviews/security/US-001-security-review.md` (v2),
`docs/reviews/reconciliation/US-001-reconciliation.md` (this file, v3),
`docs/reconciliation/US-001-traceability.md` (this file's pair, v3).
*(All of these re-issue or re-approve in the mandated re-run before the PR is
finally assembled — most with no content change.)*

*(29 + 20 = 49 category-(a) paths.)*

### (b) Harness-maintenance changes — INCLUDE, NOT US-001 functional scope  (3 paths + 1 shared hunk)

- `docs/workflow/history.jsonl` (M) — `story-orchestrator` transition log.
- `docs/workflow/workflow-state.yaml` (M) — `story-orchestrator` execution state.
- `docs/evidence/.gitignore` (M) — 4 `harness-*` ignore entries + a BOM,
  committed in `a96ebd5`; no US-001 content. Already on the branch;
  reconciliation cannot remove a committed change — recorded so it is not
  mistaken for Story scope. (was RC-8)
- `.gitignore` (M) — the harness hunk (`/docs/harness-consistency-review.md`,
  `/docs/hooks/tool-usage.jsonl`) only. The path is counted once in (a) (it also
  carries M-3 `/data/`).

Present in the reviewed diff; described here as harness-maintenance, not as
absent (REJECT-6 correction, retained from v2).

### (c) Excluded changes  (0 counted + standard ignores)

| Path | Classification | Counted | Reason |
|---|---|---|---|
| *(none)* | — | **0** | The RC-10 stray `src/main/.../docs/hooks/tool-usage.jsonl` was **removed** in the corrective pass; `implementation_verification` v2 §4 and `security_review` v2 §17 confirm it is absent. |
| `/data/` (generated H2 files) | EXCLUDE_RUNTIME_ARTIFACT | no | git-ignored; not in the tree. |
| `build/`, `.gradle/` | EXCLUDE_RUNTIME_ARTIFACT | no | git-ignored. |
| `.idea/`, `customer-portal.iml` | EXCLUDE_LOCAL_CONFIGURATION | no | git-ignored IDE files. |
| `docs/hooks/tool-usage.jsonl` | EXCLUDE_LOCAL_CONFIGURATION | no | git-ignored telemetry (the correctly-placed one). |
| pre-existing untracked `docs/evidence/harness-*.{py,md}`, `docs/harness-consistency-review.md` | EXCLUDE_UNRELATED | no | git-ignored; outside US-001; untouched. |

### Exclude — Sensitive Files (0)

None. No `.env`, token, key, or credential file in scope.
`spring.datasource.password: ""` is the H2 default (SR-5), not a secret.

### Human Decision Required (0)

None. (The RC-10 stray file that was here in v2 has been removed. The hook
output-path root cause remains finding D-2 for the human — hook configuration,
not a PR file.)

**Totals:** `candidate_files: 52` = 49 category-(a) US-001 story paths + 3
category-(b) harness-maintenance paths (`.gitignore` is a category-(a) path that
also carries a harness hunk, counted once). `excluded_files: 0`. Cross-checked
against `git diff --name-status 47e3016..HEAD` (52 tracked paths: 2 root —
`.gitignore` M, `build.gradle.kts` M; 16 `src/main/java`; 2 `src/main/resources`;
8 `src/test/java`; 1 `src/test/resources`; 20 `docs/**/US-001-*`; 2 harness —
`docs/workflow/history.jsonl` M, `docs/workflow/workflow-state.yaml` M; 1
`docs/evidence/.gitignore` M) — matches `candidate_files: 52`. No secret, no
generated DB file in the include set.

## 16. Drift Register

| id | Type | Severity | Affected | Expected | Actual | Risk | Correction | Loop-back |
|---|---|---|---|---|---|---|---|---|
| RC-1 | Security (latent) / Test gap | **CLOSED** | `model/request/RegistrationRequest.java`; `RegistrationRequestTest` | Plaintext password never rendered (SEC-3) | Masking `toString()` (`password=***`) + 3 proving tests | — | Done (corrective pass) | none — closed |
| RC-2 | Documentation (API) | Minor | `exception/GlobalExceptionHandler.java`, `docs/designs/api/US-001-openapi.yaml` | Implemented `message` strings could match the OpenAPI examples | `400` / `415` messages differ verbatim from the illustrative examples; `409` matches | None — examples illustrative; AC-6 shape preserved; tests assert status+shape | Optional `openapi-designer` example alignment | none |
| RC-3 | Robustness / error mapping / Test gap | **CLOSED** (residual note as `security_review` v2 SR-3, Minor) | `service/CustomerService.java`; `CustomerServiceTest` | Duplicate email → `409` on every path incl. concurrent | Constraint-scoped `DataIntegrityViolationException` catch → `409`; unrelated integrity violations rethrown; +2 deterministic tests | Residual: name+message heuristic — practically unreachable false-positive; impact ceiling `409` instead of `500` | Done (corrective pass). Optional hardening: constraint-name-only match | none — closed |
| RC-4 | Artifact / Documentation | **CLOSED** | `docs/decisions/US-001-open-decisions.md` | Body reflects the recorded resolutions | v2 published + APPROVED + committed; all six `RESOLVED` | None | Commit with the PR (done) | none — closed |
| RC-5 | Configuration | Informational | `src/main/resources/application.yaml` | — | `AUTO_SERVER=TRUE` + blank `sa` password | Low — **approved** config (DB design §8, plan M-2); local-dev only | Future hardening Story | none |
| RC-6 | Secret management | Informational | `src/main/resources/application.yaml` | Config secrets externalized (SC-7) | `spring.datasource.password: ""` committed | None — H2 default, not a secret | Externalize when a real datasource is introduced | none |
| RC-7 | Persistence (DDL style) | Informational | `src/main/resources/schema.sql` | — | `id BIGINT GENERATED BY DEFAULT AS IDENTITY` with no explicit `NOT NULL` | None — H2 2.x implicit; `validate` passes; `CustomerSchemaTest.idColumnIsBigintNotNull` confirms | None | none |
| RC-8 | Scope (repository hygiene) | **Recorded / not actionable** | `.gitignore`, `docs/evidence/.gitignore` | Story change set contains only US-001 files | Both carry harness-scaffolding entries, committed in `a96ebd5` | None — no code / secret / runtime artifact | Classified harness-maintenance in §15(b); already committed; flagged for the human diff reviewer | none |
| **RC-9** | **Design / Documentation (security wording)** | **Major** (human-mandated — REJECT-5; code half done, doc half open) | `docs/specifications/US-001-spec.md:135`; `docs/designs/api/US-001-api-design.md:138` / `:174` | Spec + API design state the approved policy is *authentication-required by default* (SC-4), consistent with `SecurityConfig` | Both still read "deny-by-default (SC-4)" without the clarifying note; only the `SecurityConfig` code comment was aligned | **No security / behaviour risk** — code is SC-4-compliant; SC-4's own text is authentication-required-by-default. Risk is an incomplete human-mandated correction reaching the PR. | `spec-writer` adds the one-line note to spec §7 SEC-1 row; `openapi-designer` adds it to api-design §6 / §8 (cascade). No code / test change. | **`specification_gap` → `SPECIFICATION`** (earliest responsible stage; `design_gap` → `API_DESIGN` also applies and is reached in the cascade) |
| RC-10 | Scope / repository hygiene | **CLOSED** | (was) `src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl` | No non-source files under `src/main` | Stray subtree **removed** in the corrective pass; confirmed absent | — | Done. Hook output-path fix remains finding D-2 for the human (hook config) | none — closed |

Drift types present in v3: **Documentation Drift** (RC-2, **RC-9**),
**Configuration** (RC-5/RC-6 Informational), **Persistence style** (RC-7
Informational), **Scope** (RC-8 recorded harness-maintenance). Closed since v2:
Security Drift (RC-1), Robustness (RC-3), Artifact Drift (RC-4), Scope Drift
(RC-10). No Requirement Drift, no API/DB contract Design Drift, no Plan Drift, no
Test Drift, no Security Drift remaining.

## 17. Findings

### RC-9 — SC-4 "deny-by-default" documentation note unpublished in `spec` / `api-design`  (Major; = REJECT-5 documentation half; = `security_review` v2 SR-1 / `implementation_verification` v2 MF-a)

- **Severity:** Major. **Category:** documentation consistency / security wording.
  Major because it is the unfinished half of a **human-mandated** pre-PR
  correction (REJECT-5), not because of residual security risk (there is none).
- **Evidence:**
  - `docs/specifications/US-001-spec.md:135` (§7, SEC-1 row): *"`POST /api/v1/customers` is the only public endpoint added by this Story; every other endpoint remains deny-by-default."* — no clarifying note.
  - `docs/designs/api/US-001-api-design.md:138` (§6 Auth model): *"Every other endpoint remains deny-by-default (SC-4); this Story adds no other route."*
  - `docs/designs/api/US-001-api-design.md:174` (§8 checklist): *"SC-4 deny-by-default, registration public | ✅ §6"*.
  - `security/SecurityConfig.java` (RC-9 code half, done): javadoc + inline comment now say *"authentication-required by default (SC-4) … it is not a literal `denyAll()`"*; `anyRequest().authenticated()` unchanged.
- **Human requirement (REJECT-5, verbatim):** *"Resolve the SC-4 wording/behavior
  ambiguity: either use literal `denyAll()` for all non-registration requests, or
  document that the approved policy means authentication-required by default
  rather than literal deny-by-default. Ensure tests match the selected policy."*
  The implementer selected the second option and completed the code side; the
  documentation side (spec + api-design) is the remaining obligation.
- **Impact:** the code posture is secure, tested, and compliant with
  `security-conventions.md` SC-4 as authoritatively worded. There is no
  behavioural gap and no exploit path (`security_review` v2 §6 / §19 SR-1,
  `implementation_verification` v2 §17 MF-a). The defect is that an approved,
  mandated correction would reach the Pull Request only half-applied, with the
  Specification and API design still carrying the wording the human asked to have
  clarified.
- **Required correction:** `spec-writer` adds a one-line note to
  `docs/specifications/US-001-spec.md` §7 (SEC-1 row) — e.g. *"'deny by default'
  here means authentication-required by default per SC-4
  (`anyRequest().authenticated()`), not a literal `denyAll()`."*
  `openapi-designer` adds the matching note to
  `docs/designs/api/US-001-api-design.md` §6 and §8. No OpenAPI contract change,
  no code change, no test change.
- **Responsible stage / loop-back:** **`SPECIFICATION` (`specification_gap`)** —
  the earliest stage in `stage_order` that owns an affected artifact. `API_DESIGN`
  (`design_gap`) also owns an affected artifact and is reached in the cascade
  from the `SPECIFICATION` re-run (`SPECIFICATION` → `SPEC_REVIEW` →
  `HUMAN_SPEC_APPROVAL` → `API_DESIGN` → …). Routing to `API_DESIGN` alone would
  leave `spec §7` unfixed — the cheaper correction, not the correct one
  (orchestrator Loop-Back Precedence). Both downstream reviews (`security_review`
  v2 SR-1, `implementation_verification` v2 MF-a) explicitly directed this stage
  to route it here and to **not** record RC-9 as closed until both halves are in
  place.

### RC-2 — Implemented error `message` strings differ from the OpenAPI illustrative examples  (Minor; = `security_review` v2 SR-2 / `implementation_verification` v2 MF-b)

- **Severity:** Minor. **Category:** documentation (API).
- **Evidence:** implemented `415` `"Content-Type must be application/json."` vs
  contract example `"Content-Type 'text/plain' is not supported."`; one combined
  `400` message vs two contract examples. `409` matches exactly.
- **Impact:** none — `examples` are illustrative, not normative; AC-6 body shape
  preserved; all tests assert status + shape; implemented messages are more
  generic (no extra disclosure).
- **Required correction:** none. Optional `openapi-designer` example alignment in
  a future revision.
- **Responsible stage / loop-back:** none.

### RC-3-residual — `isEmailUniquenessViolation` name + message-token heuristic  (Minor; = `security_review` v2 SR-3)

- **Severity:** Minor. **Category:** persistence / error handling (robustness).
- **Evidence:** `service/CustomerService.java:89-104` — returns `true` if a
  Hibernate `ConstraintViolationException#getConstraintName()` contains
  `uq_customer_email` (case-insensitive) or, as a fallback, any cause message
  contains that token.
- **Impact:** a crafted-email false positive is practically unreachable — the
  other `customer` constraints (`pk_customer` on a server-generated id,
  `ck_customer_role` on a server-set value, `NOT NULL` columns) cannot be tripped
  by user email content and their H2 messages name the failing constraint, not
  the row email. Impact ceiling if it ever misfired: a genuine integrity error
  returns `409` instead of `500` — no data exposure, no authz / enumeration
  effect beyond the accepted OD-003:A.
- **Required correction:** none for US-001. Optional hardening: constraint-name
  match only, once a Hibernate/H2 version with reliable `getConstraintName()` is
  confirmed.
- **Responsible stage / loop-back:** none. (RC-3 itself is CLOSED; this is the
  verifier-/security-forwarded residual.)

### RC-5 / RC-6 / RC-7 — Informational (unchanged from v2)

- **RC-5** — `AUTO_SERVER=TRUE` + blank `sa` password: **approved** config (DB
  design §8, plan M-2, impact analysis); local-dev only; test profile isolated
  in-memory. = `security_review` v2 SR-4. No loop-back.
- **RC-6** — `spring.datasource.password: ""` committed: H2 default, not a
  secret; SC-7 not breached. = `security_review` v2 SR-5. No loop-back.
- **RC-7** — `schema.sql` `id` column has no explicit `NOT NULL`: H2 2.x implicit;
  `ddl-auto=validate` passes; `CustomerSchemaTest.idColumnIsBigintNotNull`
  confirms. No loop-back.

**No Critical findings. 1 Major (RC-9). 2 Minor (RC-2, RC-3-residual).
3 Informational (RC-5, RC-6, RC-7). RC-1, RC-3, RC-4, RC-8, RC-10 CLOSED.**

## 18. Positive Alignment

1. **All seven Acceptance Criteria `RECONCILED`** — AC-002 (concurrent-duplicate
   path) and AC-004 (`toString()` masking) closed by the verified corrective
   pass; the other five carried from v2 unchanged.
2. **Build + 67 tests reproduced independently** by `implementation-verifier` v2
   (`./gradlew clean build` BUILD SUCCESSFUL, 0 failures / errors / skipped;
   +5 tests = exactly the RC-1 and RC-3 coverage).
3. **All four HUMAN_PR_APPROVAL code/hygiene mandates applied and verified** —
   RC-1, RC-3, RC-9 code half, RC-10; prior verification findings MF-3 / MF-5 and
   security findings F-1 / F-3 / F-4 all CLOSED.
4. **Security fundamentals re-verified** by `security_review` v2 against the real
   `SecurityFilterChain` — BCrypt (no no-op), plaintext confined to the request
   DTO and now `toString()`-masked, zero logging in `src/main`, `CustomerResponse`
   credential isolation, scoped `permitAll` + CSRF exemption on one matcher, H2
   console disabled, `ddl-auto=validate` every profile.
5. **All six Open Decisions resolved by the human** and recorded in
   `open_decisions.md` v2 (`APPROVED`, committed).
6. **Stray `src/` telemetry file removed** (RC-10); working tree clean.
7. **Architecture clean** — layering, single advice, DTO/entity boundary, config
   placement, package ownership all conform; the RC-3 service references are
   DAO/persistence exception types, no new declared dependency.
8. **PR scope fully accounted** (§15) in three categories with 0 excluded files
   and 0 human-decision files.

## 19. Open Decisions

**No blocking Open Decisions remain.** OD-001..OD-006 were resolved by the human
at `HUMAN_SPEC_APPROVAL` and are recorded `RESOLVED` in `open_decisions.md` v2.

RC-9 (REJECT-5) is **not** an Open Decision in the CLARIFICATION sense — the
security *intent* (SC-4) is approved and the *policy choice* was made (align
wording, not `denyAll()`). What remains is applying that resolution to two
documents. It is routed as `specification_gap`, not as a `CLARIFICATION` blocker.

No unresolved `TODO` / `TBD` / `FIXME` / `???` / "to be decided" marker was found
in an `APPROVED` input artifact affecting an Acceptance Criterion, observable
behaviour, the API contract, persistence, security, validation, architecture,
testing, configuration, dependency selection, or PR scope.

## 20. Reconciliation Limitations

- **Semantic analysis:** IDEA MCP semantic tools not invoked
  (`semantic_analysis: TEXT_FALLBACK`) — architecture conclusions rest on import
  graphs and method signatures, consistent with `implementation_verification` v2
  §18 and `security_review` v2 §22.
- **Build / tests not re-run in this stage** — the 67/67 result is reused from
  `implementation_verification` v2, which independently reproduced it; valid for
  the current clean tree.
- **Concurrency (RC-3)** is verified by deterministic unit tests with an injected
  exception, not a reproduced race (matches the reconciliation directive).
- **No dependency vulnerability scanning** at any stage.
- **Remote source:** no GitHub Issue for US-001; remote/local reconciliation n/a.
- **`implementation_verification` v2 front matter `status: DRAFT` vs envelope
  `artifact_status: APPROVED`** — established repo pattern for verification
  artifacts (mirrors v1); the orchestrator already advanced on it
  (`history.jsonl` 2026-09-02T15:04:46Z). Observation for the human diff
  reviewer, not a stale-input condition.
- **Human checks still required:** approval of the RC-9 documentation note at the
  re-run `HUMAN_SPEC_APPROVAL` / `HUMAN_PLAN_APPROVAL` gates; the eventual
  `HUMAN_PR_APPROVAL` diff review; the hook output-path fix (D-2).

## 21. Verdict Rationale

The code side of the `HUMAN_PR_APPROVAL` rejection is fully discharged: RC-1,
RC-3, RC-9 (code half) and RC-10 are applied, in scope, free of unrelated edits,
and independently verified by `implementation_verification` v2 (PASS, 67/67) and
`security_review` v2 (PASS, 0 Critical / 0 Major). All seven Acceptance Criteria
are `RECONCILED`; the artifact chain is current; no input is `SUPERSEDED`; no
change was made after verification / security review (working tree clean); PR
scope is fully classified with no secret, runtime artifact, or unrelated change
in the include set and **0 excluded files**. On every one of those axes this is a
PASS.

It is **not** a PASS on one axis: REJECT-5. The human made the SC-4 wording
resolution mandatory and offered two options; the implementer chose "document
that the approved policy means authentication-required by default" and completed
that in `SecurityConfig` code, but `docs/specifications/US-001-spec.md` §7 and
`docs/designs/api/US-001-api-design.md` §6 / §8 still carry the un-clarified
"deny-by-default (SC-4)" wording. Both downstream reviews raised this and
explicitly instructed RECONCILIATION to route it and not to mark RC-9 closed.
Per Step 22, Reconciliation may recommend progression only when "no Major
findings exist" and "documentation is consistent"; RC-9 is a Major, human-
mandated item that is documentation-inconsistent. That is `CHANGES_REQUIRED`, not
PASS, and not `BLOCKED` (the fix maps cleanly to a `RECONCILIATION.loop_back`
key and needs no human decision to define — only the standard gate approvals).

Root cause: the Specification omits wording the human required. Per Step 21 that
is `specification_gap` → `SPECIFICATION`. `API_DESIGN` also owns an affected
artifact; it is the second-earliest responsible stage and is reached
automatically in the cascade from the `SPECIFICATION` re-run, so a single
loop-back target (`SPECIFICATION`) covers both. Routing to `API_DESIGN` alone
would be the cheaper correction and would leave `spec §7` unfixed — the
orchestrator's Loop-Back Precedence rule forbids that.

The security / behavioural risk of shipping the current wording is nil, so if the
human prefers, they may instead override at `HUMAN_PR_APPROVAL` and accept the
phrasing as-is — but that is a human decision to make at the gate, not one
Reconciliation can make by returning PASS.

**Verdict: CHANGES_REQUIRED** → loop back to `SPECIFICATION`
(`specification_gap`).

```yaml
result:
  verdict: CHANGES_REQUIRED
  stage: RECONCILIATION
  story: US-001
  artifact_status: IN_REVIEW
  artifacts:
    - docs/reviews/reconciliation/US-001-reconciliation.md
    - docs/reconciliation/US-001-traceability.md
  next_stage: SPECIFICATION
  loop_back_stage: SPECIFICATION            # stage-map.yaml RECONCILIATION.loop_back key: specification_gap
  blocking_issues: []
  non_blocking_findings:
    - "LOOP-BACK REASON (specification_gap -> SPECIFICATION): RC-9 / REJECT-5 is only half done. The HUMAN_PR_APPROVAL rejection (2026-09-01, ayubutrym@gmail.com) required resolving the SC-4 'deny-by-default' wording ambiguity by EITHER literal denyAll() OR documenting that the approved policy means authentication-required by default. The implementer chose option 2 and aligned the SecurityConfig code comment (RC-9 code half, verified), but did NOT add the matching note to docs/specifications/US-001-spec.md:135 (SEC-1 row) or docs/designs/api/US-001-api-design.md:138 / :174 - all three still read 'deny-by-default (SC-4)'."
    - "RC-9 (Major, human-mandated, documentation half): NO security or behaviour risk - the code is SC-4-compliant and security-conventions.md SC-4's own wording IS authentication-required-by-default (anyRequest().authenticated()). Major because a mandated pre-PR correction would otherwise reach the PR half-applied. Both downstream reviews forwarded this with an explicit instruction: security_review v2 SR-1 and implementation_verification v2 MF-a both say 'RECONCILIATION must NOT record RC-9 as closed and must route via specification_gap -> SPECIFICATION and/or design_gap -> API_DESIGN'."
    - "LOOP-BACK PRECEDENCE: SR-1 names both SPECIFICATION (spec sec 7) and API_DESIGN (api-design sec 6 / sec 8). SPECIFICATION is index 2 in stage_order, API_DESIGN is index 5 -> route to SPECIFICATION (earliest responsible stage). The cascade SPECIFICATION -> SPEC_REVIEW -> HUMAN_SPEC_APPROVAL -> API_DESIGN -> ... re-runs API_DESIGN, so openapi-designer adds its half of the note then. Routing to API_DESIGN alone would leave spec sec 7 unfixed (cheaper, not correct)."
    - "CONSEQUENCE FOR THE HUMAN: re-entering SPECIFICATION re-runs SPEC_REVIEW and the HUMAN_SPEC_APPROVAL human gate, then API_DESIGN / DB_DESIGN / DESIGN_REVIEW / IMPACT_ANALYSIS / IMPLEMENTATION_PLANNING / PLAN_REVIEW / HUMAN_PLAN_APPROVAL human gate / TEST_WRITING / IMPLEMENTATION / IMPLEMENTATION_VERIFICATION / SECURITY_REVIEW / RECONCILIATION - the full pipeline, for a one-line wording note. stage-map.yaml has no shorter path. Alternative: a human override at HUMAN_PR_APPROVAL accepting the current wording (code is already SC-4-compliant; both automated reviews PASS on everything else) - but that is a gate decision, not something RECONCILIATION can return as PASS."
    - "REQUIRED CORRECTION (no code / test / OpenAPI-contract change): spec-writer adds to docs/specifications/US-001-spec.md sec 7 SEC-1 row a note like \"'deny by default' here means authentication-required by default per SC-4 (anyRequest().authenticated()), not a literal denyAll()\"; openapi-designer adds the same note to docs/designs/api/US-001-api-design.md sec 6 and sec 8. All other US-001 artifacts are current and re-approve without content change."
    - "CLOSED since reconciliation v2: RC-1 (RegistrationRequest.toString() masks password + RegistrationRequestTest, 3 tests) - verified, closes verification v1 MF-5 / security v1 F-1. RC-3 (CustomerService constraint-scoped uq_customer_email -> 409, unrelated integrity violations rethrown, CustomerServiceTest +2 incl. load-bearing isSameAs negative) - verified, closes verification v1 MF-3 / security v1 F-3. RC-4 (open_decisions v2 + clarification_report v2 APPROVED + committed 7ad07e1) - closes security v1 F-4 / REJECT-2. RC-10 (stray src/main/.../docs/hooks/tool-usage.jsonl) - removed, confirmed absent. RC-8 (harness .gitignore entries) - recorded harness-maintenance, already committed, not actionable."
    - "ALL 7 ACCEPTANCE CRITERIA RECONCILED (traceability v3): AC-001..AC-007. AC-002 (concurrent-duplicate 409) and AC-004 (toString() masking) - PARTIALLY_RECONCILED in v2 - are now closed. Security-posture row SEC-1 / SC-4 is PARTIALLY_RECONCILED (RC-9 doc half); SEC-3 is now RECONCILED (RC-1)."
    - "Build/tests: ./gradlew clean build BUILD SUCCESSFUL; 67 tests / 0 failures / 0 errors / 0 skipped across 8 suites (was 62/7; +5 = exactly RC-1 + RC-3 coverage) - independently reproduced by implementation-verifier v2, reused here (not re-run this stage). Working tree clean; no src/** change after security_review v2."
    - "CURRENCY: implementation_verification v2 + security_review v2 are current (consumed implementation_report v2 + open_decisions v2) and both PASS with 0 Critical / 0 Major. Not stale - NOT a BLOCKED condition. implementation_verification v2 front matter status: DRAFT vs envelope artifact_status: APPROVED is the established repo pattern; orchestrator already advanced on it."
    - "RC-2 (Minor, unchanged = security_review v2 SR-2): implemented 400/415 error message strings differ verbatim from the OpenAPI illustrative examples; 409 matches exactly; AC-6 body shape preserved; tests assert status+shape. Optional openapi-designer example alignment; no loop-back."
    - "RC-3-residual (Minor = security_review v2 SR-3): CustomerService.isEmailUniquenessViolation uses Hibernate constraint name + case-insensitive message-token contains('uq_customer_email'). Crafted-email false-positive practically unreachable; impact ceiling a real integrity error returns 409 instead of 500 - no data exposure, no authz/enumeration effect. Optional hardening: constraint-name-only match. No loop-back."
    - "RC-5 / RC-6 / RC-7 (Informational, unchanged): AUTO_SERVER=TRUE + blank sa password (approved config, local-dev only) = security_review v2 SR-4; spring.datasource.password: \"\" (H2 default, not a secret) = SR-5; schema.sql id column no explicit NOT NULL (H2 2.x implicit, ddl-auto=validate passes)."
    - "PR CANDIDATE SCOPE (v3 sec 15, one entry per path): candidate_files 52 = 49 category-(a) US-001 story paths (29 code/build/config incl. .gitignore = 16 src/main/java + 2 src/main/resources + 8 src/test/java + 1 src/test/resources + build.gradle.kts + .gitignore; plus 20 US-001 workflow-doc artifacts) + 3 category-(b) harness-maintenance paths (docs/workflow/history.jsonl, docs/workflow/workflow-state.yaml, docs/evidence/.gitignore). excluded_files 0 (RC-10 stray file removed; working tree clean; 0 human-decision files). Cross-checked against git diff --name-status 47e3016..HEAD (2 root + 16 src/main/java + 2 src/main/resources + 8 src/test/java + 1 src/test/resources + 20 docs/**/US-001-* + 3 harness = 52). No secret, no generated DB file in the include set. Counts as-of-write; docs/workflow/{history.jsonl,workflow-state.yaml} change again when this transition is recorded; the reconciliation + traceability v3 files are updated in place (still counted once each in category (a)). pr-preparer consumes this classification and must not re-derive it."
    - "Accepted deviations (carried, re-confirmed): D-1 exception/InvalidPasswordException (FR-6 service re-check; mapped to 400, not reachable from the HTTP flow); D-3 RC-3 mapping placed in the service not GlobalExceptionHandler (reconciliation allowed either; no HTTP type in service; deterministically testable); D-4 RC-3 constraint scoping is name + message-token based (= RC-3-residual / SR-3). D-2 (hook output-path fix for the removed tool-usage.jsonl) remains a finding for the human - hook configuration, not a PR file."
    - "Staleness (waived, carried): specification v1 / implementation_plan v1 / ac_test_matrix v1 front matter reference open_decisions v1 (now v2); open_decisions v2 change-log = 'No decision content changed'. When SPECIFICATION re-runs for RC-9, spec-writer may refresh the specification front-matter reference opportunistically; plan / matrix references are out of RC-9 scope. Not re-opened."
```
