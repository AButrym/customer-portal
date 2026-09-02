---
artifact_type: reconciliation
story: US-001
version: 2
status: IN_REVIEW
created_at: 2026-08-31T12:52:00Z
updated_at: 2026-09-02T14:02:21Z
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
    version: 1
  - path: docs/verification/US-001-implementation-verification.md
    version: 1
  - path: docs/reviews/security/US-001-security-review.md
    version: 1
supersedes: docs/reviews/reconciliation/US-001-reconciliation.md
reconciled_acceptance_criteria: 5
total_acceptance_criteria: 7
critical_findings: 0
major_findings: 4
minor_findings: 2
informational_findings: 3
candidate_files: 51
excluded_files: 1
---

# Reconciliation — US-001 Customer Registration  (v2)

> **v2 re-run.** Reconciliation v1 (verdict PASS, 2026-08-31) was **rejected by
> the human at `HUMAN_PR_APPROVAL`** on 2026-09-01T08:41:01Z
> (`docs/workflow/history.jsonl`, `verdict: HUMAN_REJECTED`, decided_by
> `ayubutrym@gmail.com`) with six required changes (REJECT-1..REJECT-6). This
> version supersedes v1, corrects the two report defects the human identified
> (REJECT-1 finding counts, REJECT-6 PR accounting + stray file), records that
> REJECT-2 was resolved out-of-band, and routes the three code corrections
> (REJECT-3, REJECT-4, REJECT-5) back to `IMPLEMENTATION`.

## 0. Disposition of the six rejection items

| Item | Summary | Status in v2 | Routing |
|---|---|---|---|
| REJECT-1 | Reconciliation v1 finding counts inconsistent (5 Minor + 2 Informational / RC-1..RC-7 in the front matter & summary vs 5 Minor + 3 Informational / RC-1..RC-8 in the body) | **Fixed in this document** — front matter, §1, §16, §17, §21, and the result envelope now agree | none (report-only, fixed on re-run) |
| REJECT-2 | `open_decisions.md` must be published v2 marking OD-001..OD-006 RESOLVED | **Resolved out-of-band.** `docs/decisions/US-001-open-decisions.md` v2 and `docs/evidence/US-001-clarification-report.md` v2 exist (status `APPROVED`, all six `RESOLVED` with `OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A`), currently uncommitted in the working tree. Verified — see §3 / §14 / §19. No decision content changed. | none (finding RC-4 now **RESOLVED**) |
| REJECT-3 | `RegistrationRequest` record `toString()` renders the plaintext password — add a masking `toString()` + a test proving the submitted plaintext password is never rendered | **Open — code change pending** (no `src/**` change since `IMPLEMENTATION` commit `5e17151`) | `implementation_drift` → **IMPLEMENTATION** (finding RC-1, escalated Minor → Major) |
| REJECT-4 | `CustomerService.register` check-then-act — concurrent duplicate trips `uq_customer_email` as an unmapped `DataIntegrityViolationException` → `500`; map to `409` without over-catching; add deterministic test coverage | **Open — code change pending** | `implementation_drift` → **IMPLEMENTATION** (finding RC-3, escalated Minor → Major) |
| REJECT-5 | Resolve the SC-4 "deny-by-default" wording/behaviour ambiguity — literal `denyAll()` for non-registration requests, or document that the approved policy means authentication-required by default; tests must match | **Open — code/doc change pending** | `implementation_drift` → **IMPLEMENTATION** (finding RC-9, new Major) + coordinated doc note (spec §7 / api-design §6) |
| REJECT-6 | Reconciliation PR accounting must distinguish (a) US-001 story changes, (b) harness-maintenance changes, (c) excluded changes, and must not describe harness-maintenance changes as absent from the diff; classify the stray `src/main/.../docs/hooks/tool-usage.jsonl` | **PR accounting fixed in this document** (§15, three-category). Stray file classified **EXCLUDE / must be removed from `src/`** (finding RC-10, new Major) — reconciliation does not delete it | stray-file removal folded into the IMPLEMENTATION loop-back |

**Post-correction sequence required by the human (recorded here for the
orchestrator):** after the REJECT-3/4/5 code changes, rerun the affected tests,
then repeat `IMPLEMENTATION_VERIFICATION`, `SECURITY_REVIEW`, and
`RECONCILIATION` for the changed source and artifacts. The
`implementation_drift` → `IMPLEMENTATION` loop-back produces exactly that
downstream sequence.

## 1. Executive Summary

**Verdict: CHANGES_REQUIRED — loop back to `IMPLEMENTATION`
(`implementation_drift`).**

The US-001 implementation remains functionally complete and, on the
single-request paths, correct and secure — but the human review at
`HUMAN_PR_APPROVAL` escalated three previously-Minor items to **required code
changes** before a Pull Request. Those changes have not yet been made
(`git diff 47e3016..HEAD -- src/` shows the original `IMPLEMENTATION` change set
only; no correction commit exists). Reconciliation therefore cannot recommend
progression.

- **Acceptance Criteria:** 5 of 7 `RECONCILED`; **AC-002 and AC-004 downgraded
  to `PARTIALLY_RECONCILED`** in the `traceability` matrix because the human
  made the concurrent-duplicate mapping (RC-3 / REJECT-4) and the
  `RegistrationRequest.toString()` masking (RC-1 / REJECT-3) mandatory for this
  Story rather than follow-up work. The security-posture row SEC-1 / SC-4 is
  `PARTIALLY_RECONCILED` pending RC-9 / REJECT-5.
- **REJECT-1 (report defect) fixed:** v1's front matter (`minor_findings: 5`,
  `informational_findings: 2`) and Executive Summary ("RC-1..RC-7") disagreed
  with the body, which carried **RC-1..RC-8 = 5 Minor + 3 Informational**. v2's
  front matter, summaries, drift register (§16), findings (§17), verdict
  rationale (§21), and result envelope are now internally consistent.
- **REJECT-2 (stale artifact) resolved out-of-band:** `open_decisions.md` v2 +
  `clarification-report.md` v2 published (uncommitted); OD-001..OD-006 all
  `RESOLVED`, no decision content changed. Finding RC-4 moves to **RESOLVED**.
- **REJECT-6 (PR accounting) fixed:** §15 now classifies every branch change
  into (a) US-001 story, (b) harness-maintenance, (c) excluded, and names the
  stray `src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl`
  (RC-10) — untracked, misplaced under `src/main`, must be removed from `src/`;
  reconciliation surfaces it and does not delete it.
- **Verification / security currency:** `implementation_verification` v1 and
  `security_review` v1 were current *as of v1* (no `src/**` change after
  `IMPLEMENTATION`) and remain so now — **but they are about to become stale**:
  they consumed `open_decisions` **v1** (now superseded by v2), and the
  REJECT-3/4/5 code changes will change security-sensitive files. Both re-runs
  are already mandated by the human and are the natural consequence of the
  `IMPLEMENTATION` loop-back; this is **not** a separate `BLOCKED` condition.
- **Findings:** 0 Critical, **4 Major** (RC-1, RC-3, RC-9, RC-10), 2 Minor
  (RC-2, RC-8), 3 Informational (RC-5, RC-6, RC-7). RC-4 and the REJECT-1 count
  defect are **RESOLVED** in v2.
- **PR candidate scope:** 51 tracked files INCLUDE — 48 US-001 story changes
  (28 code / build / config incl. `.gitignore`, + 20 US-001 workflow-doc
  artifacts) + 3 harness-maintenance (`docs/workflow/history.jsonl`,
  `docs/workflow/workflow-state.yaml`, `docs/evidence/.gitignore`). 1 file
  EXCLUDE and itemized: the stray untracked
  `src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl`
  (RC-10). Standard git-ignored paths (`/data/`, `build/`, `.gradle/`,
  `.idea/`, `docs/hooks/`, pre-existing `harness-*`) are not itemized. No
  secret and no generated DB file is in the include set.

**Recommended next action:** `IMPLEMENTATION` — `springboot-implementor`
applies REJECT-3, REJECT-4, REJECT-5 (and removes the RC-10 stray file), then
the workflow re-runs `IMPLEMENTATION_VERIFICATION` → `SECURITY_REVIEW` →
`RECONCILIATION`.

## 2. Artifact Inventory

| Artifact | Path | Type | Ver | Status | Current | Mandatory | Producing stage |
|---|---|---|---|---|---|---|---|
| Story | docs/stories/US-001-register-customer.md | story | (unversioned) | active | yes | yes | BACKLOG_SYNC / human |
| Open Decisions | docs/decisions/US-001-open-decisions.md | open_decisions | **2** | **APPROVED** (all six RESOLVED) | yes | yes | CLARIFICATION |
| Clarification Report | docs/evidence/US-001-clarification-report.md | clarification_report | **2** | APPROVED | yes | yes | CLARIFICATION |
| Specification | docs/specifications/US-001-spec.md | specification | 1 | APPROVED | yes | yes | SPECIFICATION |
| Specification Review | docs/reviews/specifications/US-001-spec-review.md | specification_review | 1 | APPROVED (PASS) | yes | yes | SPEC_REVIEW |
| API Design | docs/designs/api/US-001-api-design.md | api_design | 1 | APPROVED | yes | yes (RC-9 doc note pending) | API_DESIGN |
| OpenAPI Contract | docs/designs/api/US-001-openapi.yaml | openapi | 1 | APPROVED | yes | yes | API_DESIGN |
| DB Design | docs/designs/database/US-001-db-design.md | database_design | 1 | APPROVED | yes | yes | DB_DESIGN |
| Entity Model | docs/designs/database/US-001-entity-model.md | entity_model | 1 | APPROVED | yes | yes | DB_DESIGN |
| Design Review | docs/reviews/designs/US-001-design-review.md | design_review | 1 | APPROVED (PASS) | yes | yes | DESIGN_REVIEW |
| Impact Analysis | docs/impact-analysis/US-001-impact-analysis.md | impact_analysis | 1 | DRAFT (PASS; no review stage follows) | yes | yes | IMPACT_ANALYSIS |
| Implementation Plan | docs/plans/US-001-implementation-plan.md | implementation_plan | 1 | APPROVED (PASS + HUMAN_PLAN_APPROVAL) | yes | yes | IMPLEMENTATION_PLANNING |
| Plan Review | docs/reviews/plans/US-001-plan-review.md | plan_review | 1 | APPROVED (PASS) | yes | yes | PLAN_REVIEW |
| Test Strategy | docs/tests/US-001-test-strategy.md | test_strategy | 1 | DRAFT | yes | yes | TEST_WRITING |
| AC–Test Matrix | docs/tests/US-001-ac-test-matrix.md | ac_test_matrix | 1 | DRAFT | yes (RC-1/RC-3 test additions pending) | yes | TEST_WRITING |
| Test-Generation Report | docs/evidence/US-001-test-generation-report.md | test_generation_report | 1 | DRAFT | yes | yes | TEST_WRITING |
| Implementation Report | docs/evidence/US-001-implementation-report.md | implementation_report | 1 | DRAFT | yes (will be re-issued after the loop-back) | yes | IMPLEMENTATION |
| Implementation Verification | docs/verification/US-001-implementation-verification.md | implementation_verification | 1 | DRAFT (verdict PASS) | **current now, will be stale after the loop-back** | yes | IMPLEMENTATION_VERIFICATION |
| Security Review | docs/reviews/security/US-001-security-review.md | security_review | 1 | APPROVED (PASS) | **current now, will be stale after the loop-back** | yes | SECURITY_REVIEW |
| Reconciliation | docs/reviews/reconciliation/US-001-reconciliation.md | reconciliation | **2** | this artifact (supersedes v1) | — | — | RECONCILIATION |
| Traceability | docs/reconciliation/US-001-traceability.md | traceability | **2** | this artifact's pair (supersedes v1) | — | — | RECONCILIATION |

- **Missing mandatory artifacts:** none.
- **Duplicate current artifacts:** none. Reconciliation v1 / traceability v1 are
  `supersedes` targets of this pair.
- **Stale artifacts:** `open_decisions` v1 and `clarification_report` v1 are
  superseded by v2 (resolves REJECT-2 / RC-4). `implementation_verification` v1
  and `security_review` v1 recorded `open_decisions` **v1** in their `inputs`
  and will additionally be invalidated by the REJECT-3/4/5 code changes — both
  re-runs are mandated (see §12, §13, §14).
- **Wrong Story id / wrong path / superseded reference:** none.

### Artifact chain validation

Story → Specification → Spec Review → API/DB Designs → Design Review → Impact
Analysis → Plan → Plan Review → Test artifacts → Implementation Report →
Implementation Verification → Security Review is intact for the *content* of
every artifact. `history.jsonl` records both human gates
(`HUMAN_SPEC_APPROVAL` 2026-08-31T07:48:48Z with
`OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A`,
`HUMAN_PLAN_APPROVAL` 2026-08-31T11:20:00Z) and the `HUMAN_PR_APPROVAL`
rejection (2026-09-01T08:41:01Z). The `open_decisions` v1→v2 supersession
records the decisions the human already made at `HUMAN_SPEC_APPROVAL`; it does
not invalidate any downstream approval because every downstream artifact was
already built against those resolved values.

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

See `docs/reconciliation/US-001-traceability.md` v2 (owned by this stage).

Summary: **AC-001, AC-003, AC-005, AC-006, AC-007 `RECONCILED`;
AC-002 `PARTIALLY_RECONCILED` (RC-3 / REJECT-4 concurrent-duplicate mapping now
mandatory); AC-004 `PARTIALLY_RECONCILED` (RC-1 / REJECT-3
`RegistrationRequest.toString()` masking + test now mandatory).** No
`NOT_RECONCILED`, no `BLOCKED`.

## 5. Specification and Design Alignment

Unchanged from v1 for the API contract, DTO field sets, error-body shape, and
persistence schema — all still match the approved artifacts. One wording
correction is now required:

| Check | Result |
|---|---|
| Specification → OpenAPI | Consistent (`POST /api/v1/customers`, `RegistrationRequest`/`CustomerResponse`, `201` + `Location`, `400/409/415/500`). |
| Specification → DB design | Consistent (FR-5 fields ↔ `customer` columns; `uq_customer_email`; `password_hash VARCHAR(60)`; UTC audit). |
| Design → implementation (API) | Consistent in shape/status/auth. Deviation RC-2 (error `message` strings vs illustrative OpenAPI examples) is documentation-direction, unchanged. |
| Design → implementation (persistence) | Consistent. `ddl-auto=validate` boots clean (R-1 closed). |
| **SC-4 wording (RC-9 / REJECT-5)** | `SecurityConfig` javadoc and `spec §7` describe the posture as "deny-by-default". `security-conventions.md` SC-4 actually defines deny-by-default as *"every endpoint requires authentication unless the approved API design lists it as public"* — i.e. **authentication-required by default**, which is exactly what `anyRequest().authenticated()` implements. The human requires this ambiguity resolved: either switch to a literal `denyAll()` for non-registration routes, or align the wording (code comment + spec/api-design note) to "authentication-required by default". Tests must match the chosen policy. |

## 6. Predicted Versus Actual Impact

No change from v1 for the delivered change set. The pending REJECT-3/4/5
corrections will add: a `toString()` override (or Lombok/explicit masking) on
`RegistrationRequest`; a `DataIntegrityViolationException` → `409` mapping in
`GlobalExceptionHandler` (constrained to `uq_customer_email`) plus a
catch/translate or `try`-around-`save` in `CustomerService`; a `SecurityConfig`
wording change (and possibly a policy change); and new tests. All land in
packages already predicted by `impact-analysis` §5–§6 (`model.request`,
`exception`, `service`, `security`, and the test tree) — no new package, no new
dependency expected.

### Actual changed items not individually predicted (unchanged from v1)

| File / component | Classification | Justification |
|---|---|---|
| `exception/InvalidPasswordException` | Required Supporting Change | FR-6 / SC-1 service re-check; disclosed D-1; accepted by `implementation_verification` §15 and `security_review` §18. |
| `src/test/.../persistence/CustomerSchemaTest.java` — 2 dummy-BCrypt-literal chars | Unexpected but Justified (test-fixture fix) | `git diff f6e7eae..fb833b0 -- src/test/` confirms this is the only change to a `test-writer`-owned test; no assertion/scenario/outcome changed. |
| `.gitignore` `/docs/harness-consistency-review.md`; `docs/evidence/.gitignore` (4 `harness-*` entries + BOM) | **Harness-maintenance** — committed in `a96ebd5` ("Stage security_review completed") | Not US-001 functional scope. See §15 category (b). |
| `docs/workflow/history.jsonl`, `docs/workflow/workflow-state.yaml` | Harness-maintenance — owned by `story-orchestrator` | Updated at every transition. See §15 category (b). |
| `src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl` | **EXCLUDE — misplaced runtime telemetry** (RC-10) | Untracked; a hook wrote tool-usage telemetry to a path that resolves under `src/main/java/...`. Not covered by the existing `/docs/hooks/tool-usage.jsonl` ignore rule (different path). Must be removed from `src/`; reconciliation does not delete it. |

## 7. Plan Versus Implementation

Every plan step C-1..C-16 and M-1..M-4 remains implemented as recorded in v1
§7 (unchanged). The REJECT-3/4/5 corrections are *additions* to C-6 / C-11 /
C-12 / C-14 and to the test set, driven by the human review rather than by a
plan gap — the plan itself is not defective, so the loop-back is
`implementation_drift`, not `plan_gap`.

## 8. Test Reconciliation

| | Detail |
|---|---|
| Actual tests (as of `IMPLEMENTATION`) | 7 suites, 62 tests; `./gradlew clean build` BUILD SUCCESSFUL, 0 failures / 0 errors / 0 skipped — independently reproduced by `implementation-verifier` v1. |
| Coverage gaps the human made mandatory | (a) **REJECT-3** — no test asserts that the submitted plaintext password is never rendered by `RegistrationRequest.toString()` / logging of the bound DTO; (b) **REJECT-4** — no test exercises the concurrent-duplicate race or asserts a `409` (not `500`) for a `uq_customer_email` violation. |
| REJECT-5 test impact | `security.RegistrationSecurityPostureTest.protectedRouteReturns401WhenUnauthenticated` already asserts authentication-required-by-default; if the policy is changed to literal `denyAll()` the expected status for a protected route changes and this test must be updated. |
| Stale evidence | The 62/62 result is valid for the current tree but will be superseded by the loop-back re-run. |

## 9. API Reconciliation

No contract-shape drift (v1 §9 table still holds). RC-2 (message-string vs
illustrative-example difference) remains Minor / documentation-direction. RC-4's
`409` message `"An account with this email already exists."` still matches the
contract exactly. After REJECT-4, the concurrent-duplicate path will *also*
return that `409` body — bringing runtime behaviour closer to the contract, not
further from it.

## 10. Persistence Reconciliation

Unchanged from v1 §10 — every column, constraint, identity strategy, and audit
behaviour matches DB design v1 / entity-model v1, verified by
`CustomerSchemaTest` / `CustomerPersistenceTest` against a booted H2 datasource.
RC-7 (`id` DDL has no explicit `NOT NULL`) stays Informational. REJECT-4 does
**not** change the schema — `uq_customer_email` already exists and already
prevents the duplicate row; only the exception-to-HTTP mapping changes.

## 11. Architecture Reconciliation

Unchanged from v1 §11 — layering, single `@RestControllerAdvice`, DTO/entity
boundary, validation split, config placement, package ownership all conform
(`semantic_analysis: TEXT_FALLBACK`; import-graph + signature inspection). The
REJECT-3/4/5 corrections stay within the existing layers (DTO, exception
handler, service, security config) — no architecture impact expected, to be
re-confirmed at the re-run.

## 12. Security Reconciliation

| Item | Detail |
|---|---|
| Security Review version | `docs/reviews/security/US-001-security-review.md` v1, `status: APPROVED`, verdict PASS (0 Critical, 0 Major, 4 Minor, 2 Informational). |
| Changes after Security Review (as of now) | None to `src/**` yet — `git diff a96ebd5..HEAD -- src/` is empty. |
| Currency now | v1 is still technically current as of this write. |
| Currency after the loop-back | **Will be stale.** REJECT-3 (`RegistrationRequest`), REJECT-4 (`GlobalExceptionHandler` + `CustomerService`), and REJECT-5 (`SecurityConfig`) all touch files inside `security_review` v1's scope; and v1 consumed `open_decisions` v1. `SECURITY_REVIEW` must re-run — already mandated by the human. |
| Security drift (behavioural) | RC-1 / REJECT-3: the record `toString()` renders the plaintext password — still **no reachable leak path today** (zero logger / `System.out` / `println` in `src/main`; `GlobalExceptionHandler` reads only `HttpServletRequest` + `BindingResult`), but the human has ruled the latent contradiction of SEC-3 unacceptable to ship. RC-9 / REJECT-5: SC-4 wording ambiguity. RC-3 / REJECT-4: concurrent duplicate → `500` (no enumeration or integrity impact; the constraint holds). |

This stage returns `CHANGES_REQUIRED` (not `BLOCKED`) because no post-review
change has actually been made yet — the loop-back is what triggers the changes
and the mandated `SECURITY_REVIEW` re-run.

## 13. Configuration and Dependency Reconciliation

Unchanged from v1 §13 — no undocumented dependency, no undocumented
configuration. RC-5 / RC-6 (`AUTO_SERVER` + blank H2 credential) stay
Informational / approved-config. No new dependency is expected for
REJECT-3/4/5 (`spring-tx` `DataIntegrityViolationException` and
`spring-security` are already on the classpath).

## 14. Documentation Reconciliation

| Document | State | Authority direction |
|---|---|---|
| `open_decisions.md` | **v2 — RESOLVED (REJECT-2 done).** All six decisions `status: RESOLVED` with the `HUMAN_SPEC_APPROVAL` options; change log records "no decision content changed". Currently uncommitted. | Documentation now follows the recorded decision. RC-4 **RESOLVED**. |
| `clarification-report.md` | **v2** — Open-Decisions summary table shows `RESOLVED` + chosen option; no clarification content changed. | — |
| Specification v1 §7 / API design v1 §6 | SC-4 posture described as "deny-by-default"; needs a one-line note that this means authentication-required-by-default (or a change record if literal `denyAll()` is chosen). RC-9 / REJECT-5. | Documentation must follow the resolved policy; coordinated with the IMPLEMENTATION loop-back. |
| OpenAPI contract v1 | Illustrative `400` / `415` `examples` differ from implemented `message` strings (RC-2). | Documentation may follow the implementation — optional, not required. |
| API design v1 / DB design v1 / entity model v1 (except the SC-4 note) | Current — match the implementation. | — |
| Implementation Report v1 | Will be re-issued by the IMPLEMENTATION loop-back. | — |

## 15. Pull Request Candidate Scope  (REJECT-6 — three-category accounting)

**Counting convention:** one entry per **path**. `candidate_files` (51) = every
tracked file in `git diff --name-status 47e3016..HEAD` (branch base = `main`
merge-base `47e3016`); all of them are INCLUDE and split into category (a) or
(b). `excluded_files` (1) = untracked paths present in the working tree that
must be kept out of the PR **and** need an action — i.e. the RC-10 stray file.
Standard git-ignored paths (`/data/`, `build/`, `.gradle/`, `.idea/`,
`docs/hooks/`, pre-existing `harness-*`) are listed in (c) for completeness but
not counted. Counts are **as of this write**; `docs/workflow/history.jsonl` and
`docs/workflow/workflow-state.yaml` change again when the
RECONCILIATION → IMPLEMENTATION transition is recorded (they stay in category
(b)). `pr-preparer` consumes this classification and must not re-derive it.

### (a) US-001 story changes — INCLUDE  (48 paths: 28 code/build/config + 20 workflow-doc)

**Production / build / configuration (28)**

- `src/main/java/org/example/customerportal/config/JpaAuditingConfig.java`
- `src/main/java/org/example/customerportal/controller/CustomerController.java`
- `src/main/java/org/example/customerportal/exception/DuplicateEmailException.java`
- `src/main/java/org/example/customerportal/exception/GlobalExceptionHandler.java`  *(will change — REJECT-4)*
- `src/main/java/org/example/customerportal/exception/InvalidPasswordException.java`
- `src/main/java/org/example/customerportal/model/dto/ApiFieldError.java`
- `src/main/java/org/example/customerportal/model/dto/CustomerResponse.java`
- `src/main/java/org/example/customerportal/model/dto/ErrorResponse.java`
- `src/main/java/org/example/customerportal/model/entity/Customer.java`
- `src/main/java/org/example/customerportal/model/entity/Role.java`
- `src/main/java/org/example/customerportal/model/request/RegistrationRequest.java`  *(will change — REJECT-3)*
- `src/main/java/org/example/customerportal/repository/CustomerRepository.java`
- `src/main/java/org/example/customerportal/security/SecurityConfig.java`  *(will change — REJECT-5)*
- `src/main/java/org/example/customerportal/service/CustomerService.java`  *(will change — REJECT-4)*
- `src/main/java/org/example/customerportal/validation/PasswordPolicyValidator.java`
- `src/main/java/org/example/customerportal/validation/ValidPassword.java`
- `src/main/resources/schema.sql`
- `src/main/resources/application.yaml` (M)
- `src/test/java/org/example/customerportal/CustomerPortalApplicationTests.java` (M — M-4)
- `src/test/java/org/example/customerportal/persistence/CustomerPersistenceTest.java`
- `src/test/java/org/example/customerportal/persistence/CustomerSchemaTest.java`
- `src/test/java/org/example/customerportal/registration/CustomerRegistrationApiTest.java`  *(will gain tests — REJECT-3/4)*
- `src/test/java/org/example/customerportal/security/RegistrationSecurityPostureTest.java`  *(may change — REJECT-5)*
- `src/test/java/org/example/customerportal/service/CustomerServiceTest.java`  *(will gain tests — REJECT-4)*
- `src/test/java/org/example/customerportal/validation/PasswordPolicyValidatorTest.java`
- `src/test/resources/application-test.yaml`
- `build.gradle.kts` (M — M-1 `spring-boot-starter-validation`)
- `.gitignore` (M) — **counted here** (28th path). Split hunks: the `/data/`
  block is US-001 story scope (M-3, "Generated H2 database files"); the trailing
  `/docs/harness-consistency-review.md` line is harness-maintenance (also listed
  under (b), RC-8). One file, one path, counted once in (a).

**US-001 workflow-doc artifacts (20)** —
`docs/decisions/US-001-open-decisions.md` (v2),
`docs/evidence/US-001-clarification-report.md` (v2),
`docs/evidence/US-001-implementation-report.md`,
`docs/evidence/US-001-test-generation-report.md`,
`docs/specifications/US-001-spec.md`,
`docs/reviews/specifications/US-001-spec-review.md`,
`docs/designs/api/US-001-api-design.md`, `docs/designs/api/US-001-openapi.yaml`,
`docs/designs/database/US-001-db-design.md`,
`docs/designs/database/US-001-entity-model.md`,
`docs/reviews/designs/US-001-design-review.md`,
`docs/impact-analysis/US-001-impact-analysis.md`,
`docs/plans/US-001-implementation-plan.md`,
`docs/reviews/plans/US-001-plan-review.md`,
`docs/tests/US-001-test-strategy.md`, `docs/tests/US-001-ac-test-matrix.md`,
`docs/verification/US-001-implementation-verification.md`,
`docs/reviews/security/US-001-security-review.md`,
`docs/reviews/reconciliation/US-001-reconciliation.md` (this file, v2),
`docs/reconciliation/US-001-traceability.md` (this file's pair, v2).
*(All of these will be re-issued or re-approved by the mandated re-run before
the PR is finally assembled.)*

### (b) Harness-maintenance changes — INCLUDE, but NOT US-001 functional scope  (3 paths + 1 shared hunk)

- `docs/workflow/history.jsonl` (M) — `story-orchestrator` transition log.
- `docs/workflow/workflow-state.yaml` (M) — `story-orchestrator` execution state.
- `docs/evidence/.gitignore` (M) — 4 `harness-*` ignore entries + a BOM,
  committed in `a96ebd5`. **No US-001 content.** Already on the branch;
  reconciliation cannot remove a committed change — recorded so it is not
  mistaken for Story scope. (RC-8)
- `.gitignore` (M) — the `/docs/harness-consistency-review.md` hunk only
  (committed in `a96ebd5`). The path itself is counted once in (a) (it also
  carries M-3 `/data/`); this line notes the harness hunk within it. (RC-8)

These are **present in the reviewed diff** and are described here as
harness-maintenance, not as absent (correcting the v1 omission the human
flagged in REJECT-6).

### (c) Excluded changes  (1 counted + standard ignores)

| Path | Classification | Counted | Reason |
|---|---|---|---|
| `src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl` | **EXCLUDE — misplaced telemetry (RC-10)** | **yes (1)** | Untracked; hook telemetry written under `src/main/java/...`. Must be removed from `src/` (and the responsible hook path fixed). Reconciliation surfaces it; it does **not** delete it. Needs implementation/human action in the loop-back. |
| `/data/` (generated H2 files) | EXCLUDE_RUNTIME_ARTIFACT | no | git-ignored (`/data/`), never in the tree. |
| `build/`, `.gradle/` | EXCLUDE_RUNTIME_ARTIFACT | no | git-ignored. |
| `.idea/`, `customer-portal.iml` | EXCLUDE_LOCAL_CONFIGURATION | no | git-ignored IDE files. |
| `docs/hooks/tool-usage.jsonl` | EXCLUDE_LOCAL_CONFIGURATION | no | git-ignored telemetry (the *correctly*-placed one). |
| pre-existing untracked `docs/evidence/harness-*.{py,md}`, `docs/harness-consistency-review.md` | EXCLUDE_UNRELATED | no | now git-ignored; outside US-001; left untouched. |

### Exclude — Sensitive Files (0)

None. No `.env`, token, key, or credential file is in scope.
`spring.datasource.password: ""` is the H2 default (RC-6), not a secret.

### Human Decision Required (1)

- `src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl` — the
  human should confirm removal from `src/` and that the hook writing it is
  reconfigured. Listed above as RC-10 / EXCLUDE.

**Totals:** `candidate_files: 51` = 48 category-(a) US-001 story paths
(28 code/build/config + 20 workflow-doc) + 3 category-(b) harness-maintenance
paths (`docs/workflow/history.jsonl`, `docs/workflow/workflow-state.yaml`,
`docs/evidence/.gitignore`). `.gitignore` is a category-(a) path that also
carries a harness hunk (counted once). `excluded_files: 1` = the RC-10 stray
telemetry file; standard git-ignored paths are not counted.

Cross-check against `git diff --name-status 47e3016..HEAD`: 51 tracked paths
(2 root: `.gitignore` M, `build.gradle.kts` M; 16 `src/main/java`; 2
`src/main/resources`; 7 `src/test/java`; 1 `src/test/resources`;
20 `docs/**/US-001-*`; 3 harness: `docs/evidence/.gitignore` M,
`docs/workflow/history.jsonl` M, `docs/workflow/workflow-state.yaml` M) —
matches `candidate_files: 51`.

## 16. Drift Register

| id | Type | Severity | Affected | Expected | Actual | Risk | Correction | Loop-back |
|---|---|---|---|---|---|---|---|---|
| RC-1 | Security (latent) / Test gap | **Major** (human-escalated from Minor) | `model/request/RegistrationRequest.java`; `CustomerRegistrationApiTest` | Plaintext password never rendered anywhere (SEC-3); `Customer.toString()` was hand-written to exclude `passwordHash` | `RegistrationRequest` is a `record` → generated `toString()` renders `password` | Low today (no reachable leak path) but the human requires it fixed before PR | Add a masking `toString()` to `RegistrationRequest` (consistent with `Customer`) + a test proving the submitted plaintext password is never rendered | `implementation_drift` → IMPLEMENTATION |
| RC-2 | Documentation (API) | Minor | `exception/GlobalExceptionHandler.java`, `docs/designs/api/US-001-openapi.yaml` | Implemented `message` strings could match the OpenAPI examples | `400` (one combined message) and `415` messages differ verbatim from the illustrative examples; `409` matches | None — examples are illustrative; AC-6 shape preserved; implemented messages are more generic | Optional `openapi-designer` example alignment (documentation-direction) | none |
| RC-3 | Robustness / error mapping / Test gap | **Major** (human-escalated from Minor) | `service/CustomerService.java`, `exception/GlobalExceptionHandler.java`; `CustomerServiceTest` / `CustomerRegistrationApiTest` | Duplicate email → `409` on every path | Check-then-act; a concurrent duplicate trips `uq_customer_email` as an unmapped `DataIntegrityViolationException` → `500` | Low integrity risk (constraint holds) but the human requires the `409` mapping before PR | Map `DataIntegrityViolationException` scoped to `uq_customer_email` → `409` without treating unrelated integrity violations as duplicate-email conflicts; deterministic test coverage | `implementation_drift` → IMPLEMENTATION |
| RC-4 | Artifact / Documentation | **RESOLVED in v2** | `docs/decisions/US-001-open-decisions.md` | Body reflects the recorded resolutions | v2 published — all six `RESOLVED` (`OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A`), no decision content changed; uncommitted | None | Commit `open_decisions.md` v2 + `clarification-report.md` v2 as part of the PR | none (resolved) |
| RC-5 | Configuration | Informational | `src/main/resources/application.yaml` | — | `AUTO_SERVER=TRUE` + blank `sa` password | Low — **approved** config (DB design §8, plan M-2); local-dev only; test profile isolated in-memory | Future hardening Story | none |
| RC-6 | Secret management | Informational | `src/main/resources/application.yaml` | Config secrets externalized (SC-7) | `spring.datasource.password: ""` committed | None — H2 default, not a secret | Externalize when a real datasource is introduced | none |
| RC-7 | Persistence (DDL style) | Informational | `src/main/resources/schema.sql` | — | `id BIGINT GENERATED BY DEFAULT AS IDENTITY` with no explicit `NOT NULL` | None — H2 2.x implicit; `validate` passes; `CustomerSchemaTest.idColumnIsBigintNotNull` confirms | None | none |
| RC-8 | Scope (repository hygiene) | Minor | `.gitignore`, `docs/evidence/.gitignore` | Story change set contains only US-001 files | Both `.gitignore` files also carry harness-scaffolding entries, committed in `a96ebd5` | None — no code/secret/runtime artifact | Classified as harness-maintenance in §15(b); already committed, not removable by reconciliation; flagged for the human diff reviewer | none |
| RC-9 | Design / Documentation (security wording) | **Major** (new — REJECT-5) | `security/SecurityConfig.java` javadoc; `spec §7`; `api-design §6`; `RegistrationSecurityPostureTest` | Unambiguous statement of the authorization policy consistent with SC-4 | Code/docs say "deny-by-default"; SC-4 defines that as authentication-required-by-default; `anyRequest().authenticated()` implements the latter, not a literal `denyAll()` | Low behavioural risk (posture is already secure) but the ambiguity is a required fix | Choose one policy: literal `denyAll()` for non-registration routes, OR align wording (comment + spec/api-design note) to "authentication-required by default". Update tests to match | `implementation_drift` → IMPLEMENTATION (+ coordinated doc note) |
| RC-10 | Scope / repository hygiene | **Major** (new — REJECT-6) | `src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl` | No non-source files under `src/main` | Untracked hook-telemetry file misplaced under `src/main/java/...`; not covered by the existing `/docs/hooks/tool-usage.jsonl` ignore rule | Low (build ignores a stray `.jsonl` under `java/`) but it must not enter the PR and must not sit in the source tree | Remove the file from `src/`; fix the hook's output path so telemetry lands under `docs/hooks/`. Reconciliation does **not** delete it | folded into the IMPLEMENTATION loop-back (human confirmation) |

Drift types present: **Security Drift** (RC-1 latent, RC-9 wording),
**Documentation Drift** (RC-2, RC-9), **Test Drift / gap** (RC-1, RC-3),
**Robustness** (RC-3), **Scope Drift** (RC-8 harness-maintenance, RC-10 stray
file), **Artifact Drift** (RC-4 — now resolved). No Requirement Drift, no
Design Drift in the API/DB contracts, no Plan Drift.

## 17. Findings

### RC-1 — `RegistrationRequest` record `toString()` renders the plaintext password  (Major; = REJECT-3, was v1 Minor / SEC F-1 / IMPL_VERIFICATION MF-5)

- **Severity:** Major (human-escalated). **Category:** security (latent) + test gap.
- **Evidence:** `model/request/RegistrationRequest.java` is a `record` with
  components `email`, `password`; the compiler-generated `toString()` renders
  both. `model/entity/Customer.toString()` was hand-written to exclude
  `passwordHash`; the request DTO has no equivalent guard.
- **Impact:** SEC-3 / SC-1 intent is that the plaintext password is never
  logged or echoed. No reachable leak path exists today (independently
  confirmed by `implementation_verification` §12 and `security_review` §7/§13:
  no logger / `System.out` / `println` in `src/main`; `GlobalExceptionHandler`
  reads only `HttpServletRequest` + `BindingResult.getFieldErrors()`). The
  human has nonetheless ruled the latent contradiction unacceptable to ship.
- **Required correction:** add a masking `toString()` to `RegistrationRequest`
  (e.g. `email` shown, `password` rendered as `"***"`), consistent with
  `Customer`; add a test asserting the submitted plaintext password never
  appears in `RegistrationRequest.toString()` (and, ideally, that a log of the
  bound object would not contain it).
- **Responsible stage / loop-back:** `IMPLEMENTATION` (`implementation_drift`).

### RC-2 — Implemented error `message` strings differ from the OpenAPI illustrative examples  (Minor; = SEC F-2 / IMPL_VERIFICATION MF-2 / IMPL D-4 / plan-review F-4)

- **Severity:** Minor. **Category:** documentation (API).
- **Evidence:** implemented `415` `"Content-Type must be application/json."` vs
  contract example `"Content-Type 'text/plain' is not supported."`; one
  combined `400` message vs two contract examples. `409` matches exactly.
- **Impact:** none — `examples` are illustrative, not normative; AC-6 body
  shape preserved; all tests assert status + shape; implemented messages are
  more generic (no extra disclosure).
- **Required correction:** none. Optional `openapi-designer` example alignment.
- **Responsible stage / loop-back:** none.

### RC-3 — Concurrent duplicate registration maps to `500`, not `409`  (Major; = REJECT-4, was v1 Minor / SEC F-3 / IMPL_VERIFICATION MF-3)

- **Severity:** Major (human-escalated). **Category:** robustness / error mapping + test gap.
- **Evidence:** `CustomerService.register` guards duplicates with check-then-act
  (`existsByEmail` → `save`). Two simultaneous requests for the same new email
  can both pass the check; the second `save` throws
  `DataIntegrityViolationException` from `uq_customer_email`, which
  `GlobalExceptionHandler` does not map → `handleUnexpected` → `500`.
- **Impact:** the unique constraint still prevents the duplicate row; the
  single-request AC-002 path is correctly `409`. The human requires the
  concurrent path to also return `409`.
- **Required correction:** catch `DataIntegrityViolationException` (in the
  service, or map it in `GlobalExceptionHandler`) **scoped to the
  `uq_customer_email` constraint** — inspect the constraint name / root cause so
  an unrelated integrity violation is not misreported as a duplicate-email
  `409`; fall back to `500` otherwise. Add deterministic test coverage (e.g. a
  test that pre-inserts a row bypassing the service check, then calls
  `register` with the same email and asserts `409`; optionally a real
  concurrency test).
- **Responsible stage / loop-back:** `IMPLEMENTATION` (`implementation_drift`).

### RC-4 — `open_decisions.md` stale (`OPEN`)  →  RESOLVED in v2  (= REJECT-2, was v1 Minor / spec-review F-1 / IMPL_VERIFICATION MF-4 / SEC F-4 / plan-review F-1)

- **Severity:** was Minor; now **RESOLVED**.
- **Evidence:** `docs/decisions/US-001-open-decisions.md` v2 (status
  `APPROVED`, `supersedes` v1) marks OD-001..OD-006 `RESOLVED` with
  `resolved_by: ayubutrym@gmail.com (HUMAN_SPEC_APPROVAL)` and the options
  `OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A`; a change-log entry
  records "No decision content changed". `docs/evidence/US-001-clarification-report.md`
  v2 updates its Open-Decisions summary table to match. Both are uncommitted in
  the working tree.
- **Impact:** none — the implementation always used the resolved values. The
  stale-artifact-in-PR concern the human raised is now addressed.
- **Required correction:** commit both v2 files with the PR. No further action.
- **Responsible stage / loop-back:** none (resolved). Produced out-of-band by
  the `open_decisions` owner (`us-clarifier` / CLARIFICATION) after the
  2026-09-02 orchestrator hold.

### RC-5 — `AUTO_SERVER=TRUE` H2 listener with a blank `sa` password  (Informational; = SEC F-5)

- Unchanged from v1. **Approved** config (DB design §8, plan M-2, impact
  analysis); local-dev only; test profile isolated in-memory. Future hardening
  Story. No loop-back.

### RC-6 — Empty datasource password committed in `application.yaml`  (Informational; = SEC F-6)

- Unchanged from v1. Empty string is the H2 default, not a secret; SC-7 not
  breached. Externalize when a real datasource is introduced. No loop-back.

### RC-7 — `schema.sql` `id` column has no explicit `NOT NULL`  (Informational; = IMPL D-5)

- Unchanged from v1. H2 2.x makes identity columns implicitly `NOT NULL`;
  `ddl-auto=validate` passes; `CustomerSchemaTest.idColumnIsBigintNotNull`
  confirms. No loop-back.

### RC-8 — Two `.gitignore` files carry harness-scaffolding entries  (Minor; from IMPL_VERIFICATION §4 / SEC §17)

- **Severity:** Minor. **Category:** scope / repository hygiene.
- **Evidence:** `.gitignore` gained `/docs/harness-consistency-review.md`;
  `docs/evidence/.gitignore` gained `/harness-dryrun.py`,
  `/harness-migration-baseline.md`, `/harness-migration-report.md`,
  `/harness-post-migration-review.md` (+ a BOM). Both committed in `a96ebd5`
  ("Stage security_review completed").
- **Impact:** none — no code, no secret, no runtime artifact.
- **Required correction:** none actionable by reconciliation (already
  committed). Classified as **harness-maintenance** in §15(b) — explicitly
  *present in the reviewed diff*, not absent (REJECT-6). Flagged for the human
  diff reviewer so the entries are not read as US-001 scope.
- **Responsible stage / loop-back:** none.

### RC-9 — SC-4 "deny-by-default" wording/behaviour ambiguity  (Major; new — REJECT-5)

- **Severity:** Major. **Category:** security wording / documentation.
- **Evidence:** `security/SecurityConfig.java` javadoc says
  *"every other request requires authentication (deny-by-default, SC-4)"* and
  implements `.anyRequest().authenticated()`. `security-conventions.md` SC-4
  states *"Deny by default: every endpoint requires authentication unless the
  approved API design lists it as public"* — i.e. authentication-required by
  default, which `anyRequest().authenticated()` implements exactly. A literal
  `denyAll()` would actually be *stricter* than SC-4 and would break any future
  authenticated endpoint without an explicit allow rule.
- **Impact:** no behavioural defect today — the posture is secure and
  `RegistrationSecurityPostureTest.protectedRouteReturns401WhenUnauthenticated`
  passes. The ambiguity is between the code comment / spec wording and the
  implemented mechanism; the human requires it removed.
- **Required correction (choose one, human/implementer decides):**
  1. **Preferred — align wording:** change the `SecurityConfig` javadoc and add
     a one-line note in `spec §7` / `api-design §6` that the approved policy is
     "authentication-required by default (SC-4)"; keep
     `anyRequest().authenticated()`. Existing tests already match.
  2. **Literal `denyAll()`:** replace `anyRequest().authenticated()` with
     `anyRequest().denyAll()` for non-registration routes; update
     `RegistrationSecurityPostureTest` (a protected route would then be
     unreachable even when authenticated) and note the deviation from SC-4.
- **Responsible stage / loop-back:** `IMPLEMENTATION` (`implementation_drift`)
  for the code/comment + test; coordinated documentation note in the spec /
  API design. IMPLEMENTATION is the earliest stage where actual corrective work
  occurs and matches the human's mandated re-run sequence
  (`IMPLEMENTATION_VERIFICATION` → `SECURITY_REVIEW` → `RECONCILIATION`).

### RC-10 — Stray hook-telemetry file under `src/main`  (Major; new — REJECT-6)

- **Severity:** Major. **Category:** scope / repository hygiene.
- **Evidence:** `src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl`
  exists on disk, untracked. A hook wrote tool-usage telemetry to a relative
  path that resolved inside the Java source tree. The existing ignore rule
  `/docs/hooks/tool-usage.jsonl` does not match this path.
- **Impact:** low for the build (`javac` / resource processing ignore a
  `.jsonl` under `java/`), but the file must not enter the PR and must not
  remain in `src/`.
- **Required correction:** delete
  `src/main/java/org/example/customerportal/docs/` (the stray `docs` subtree
  under the package root) and fix the hook so telemetry is written under the
  repo-level `docs/hooks/`. **Reconciliation does not delete it** — it is
  surfaced here for the IMPLEMENTATION loop-back / human confirmation.
- **Responsible stage / loop-back:** folded into `IMPLEMENTATION`
  (`implementation_drift`) with human confirmation; classified EXCLUDE in §15(c).

**No Critical findings. 4 Major (RC-1, RC-3, RC-9, RC-10). 2 Minor (RC-2,
RC-8). 3 Informational (RC-5, RC-6, RC-7). RC-4 RESOLVED. The v1 finding-count
inconsistency (REJECT-1) is corrected throughout this document.**

## 18. Positive Alignment

1. **Single-request behaviour is complete and correct** — AC-001, AC-003,
   AC-005, AC-006, AC-007 fully `RECONCILED`; AC-002 correct on the
   single-request path.
2. **Build + 62 tests reproduced independently** by `implementation-verifier`
   v1 (`./gradlew clean build` BUILD SUCCESSFUL, 0 failures / errors / skipped).
3. **Security fundamentals verified** — BCrypt (no no-op encoder); plaintext
   password confined to the request DTO and never persisted, logged, or
   returned; `CustomerResponse` credential isolation positively asserted;
   scoped `permitAll` + CSRF exemption on one exact matcher; H2 console
   disabled every profile; `ddl-auto=validate` every profile.
4. **All six Open Decisions resolved by the human** and now reflected in
   `open_decisions.md` v2.
5. **Persistence schema** matches DB design v1 exactly, verified against a
   booted H2 datasource.
6. **Architecture clean** — layering, single advice, DTO/entity boundary,
   config placement, package ownership all conform.
7. **PR scope is now fully accounted** (§15) in three categories with no
   omission.

## 19. Open Decisions

**No blocking Open Decisions remain.** OD-001..OD-006 were resolved by the
human at `HUMAN_SPEC_APPROVAL` and are now recorded `RESOLVED` in
`open_decisions.md` v2 (REJECT-2 / RC-4).

REJECT-5 (RC-9) is **not** an Open Decision in the CLARIFICATION sense — the
security *intent* (SC-4) is approved; what is open is a code-comment / spec
wording alignment (or an optional policy tightening), which the human delegated
to the implementer. It is routed as `implementation_drift`, not as a
`CLARIFICATION` blocker.

No unresolved `TODO` / `TBD` / `FIXME` / `???` / "to be decided" marker was
found in an `APPROVED` input artifact affecting an Acceptance Criterion,
observable behaviour, the API contract, persistence, security, validation,
architecture, testing, configuration, dependency selection, or PR scope.

## 20. Reconciliation Limitations

- **Semantic analysis:** IDEA MCP semantic tools not invoked
  (`semantic_analysis: TEXT_FALLBACK`) — architecture conclusions rest on
  import graphs and method signatures, consistent with
  `implementation_verification` §10 and `security_review` §4.
- **Build / tests not re-run in this stage.** The 62/62 result is reused from
  `implementation_verification` v1; it is valid for the current tree and will
  be superseded by the loop-back re-run.
- **Concurrency (RC-3)** is reasoned from code, not reproduced.
- **No dependency vulnerability scanning** at any stage.
- **Remote source:** no GitHub Issue for US-001; remote/local reconciliation
  n/a.
- **`open_decisions` v2 / `clarification-report` v2** are uncommitted working-
  tree changes verified by direct read; they were produced out-of-band by the
  `open_decisions` owner after the 2026-09-02 orchestrator hold, with no
  `CLARIFICATION` stage event in `history.jsonl` (analogous to the recorded
  "ORCHESTRATOR STATE REPAIR" precedent).
- **Human checks still required:** the REJECT-5 policy choice; confirmation
  that the RC-10 stray file is removed; diff review and PR approval.

## 21. Verdict Rationale

The human review at `HUMAN_PR_APPROVAL` (2026-09-01) escalated three
previously-Minor items — `RegistrationRequest.toString()` exposing the
plaintext password (RC-1), the concurrent-duplicate `500` (RC-3), and the SC-4
wording ambiguity (RC-9) — into **mandatory pre-PR code changes**, and added a
repository-hygiene item (RC-10, the stray `src/main/.../docs/hooks/tool-usage.jsonl`).
None of these corrections has been made: `git diff 47e3016..HEAD -- src/` is
still the original `IMPLEMENTATION` change set. With required code changes
outstanding, Reconciliation cannot find AC-002 and AC-004 fully `RECONCILED`
and cannot recommend progression.

The correct artifacts are in place — the Specification, both designs, the plan,
and the tests are not defective; the gaps are in the implementation and its
test coverage. Per `stage-map.yaml` `RECONCILIATION.loop_back`, that root cause
maps to the key **`implementation_drift`** → **`IMPLEMENTATION`**. This is also
the earliest stage at which corrective work actually happens (RC-9's wording
fix is a `SecurityConfig` edit; the spec/api-design note is a coordinated
follow-on, not a `specification_gap` requiring full re-approval), and it
produces exactly the downstream sequence the human mandated:
`IMPLEMENTATION` → `IMPLEMENTATION_VERIFICATION` → `SECURITY_REVIEW` →
`RECONCILIATION`.

The two report defects the human identified are fixed **in this document**:
REJECT-1 (finding counts — now 0 Critical / 4 Major / 2 Minor / 3 Informational,
RC-1..RC-10 with RC-4 resolved, consistent across front matter, §1, §16, §17,
and the envelope) and REJECT-6 (PR accounting — §15 now has explicit (a) story
/ (b) harness-maintenance / (c) excluded categories and names the stray file).
REJECT-2 is resolved out-of-band (`open_decisions.md` v2). These do not by
themselves require another RECONCILIATION-only loop; they are folded into the
re-run that the code changes force.

`implementation_verification` v1 and `security_review` v1 are still technically
current as of this write (no `src/**` change yet) but consumed `open_decisions`
v1 and will be invalidated by the REJECT-3/4/5 edits — their re-run is already
mandated and is a consequence of the loop-back, **not** a separate `BLOCKED`
condition, so this stage returns `CHANGES_REQUIRED`, not `BLOCKED`.

**Verdict: CHANGES_REQUIRED** → loop back to `IMPLEMENTATION`
(`implementation_drift`).

```yaml
result:
  verdict: CHANGES_REQUIRED
  stage: RECONCILIATION
  story: US-001
  artifact_status: IN_REVIEW
  artifacts:
    - docs/reviews/reconciliation/US-001-reconciliation.md
    - docs/reconciliation/US-001-traceability.md
  next_stage: IMPLEMENTATION
  loop_back_stage: IMPLEMENTATION            # stage-map.yaml RECONCILIATION.loop_back key: implementation_drift
  blocking_issues: []
  non_blocking_findings:
    - "LOOP-BACK REASON (implementation_drift → IMPLEMENTATION): the HUMAN_PR_APPROVAL rejection (2026-09-01, ayubutrym@gmail.com) made three previously-Minor items mandatory pre-PR code changes; none is done (git diff 47e3016..HEAD -- src/ is the original IMPLEMENTATION change set)."
    - "REJECT-3 / RC-1 (Major): RegistrationRequest is a Java record — generated toString() renders the plaintext password. Add a masking toString() consistent with Customer.toString() + a test proving the submitted plaintext password is never rendered. No reachable leak path today (zero logger/System.out/println in src/main) but the human requires it fixed before PR."
    - "REJECT-4 / RC-3 (Major): CustomerService.register is check-then-act; a concurrent duplicate trips uq_customer_email as an unmapped DataIntegrityViolationException → 500. Map the uq_customer_email violation to the approved 409 (scoped to that constraint — do not misreport unrelated integrity violations as duplicate-email), fall back to 500 otherwise; add deterministic test coverage."
    - "REJECT-5 / RC-9 (Major): SC-4 wording/behaviour ambiguity. security-conventions.md SC-4 defines deny-by-default as authentication-required-by-default, which anyRequest().authenticated() already implements; the SecurityConfig javadoc and spec §7 say 'deny-by-default'. Choose: (preferred) align the wording (code comment + spec §7 / api-design §6 note), or switch to literal denyAll() for non-registration routes. Tests must match the chosen policy."
    - "REJECT-6 / RC-10 (Major): src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl is an untracked hook-telemetry file misplaced under src/main and not covered by the /docs/hooks/tool-usage.jsonl ignore rule. Remove the stray docs subtree from src/ and fix the hook's output path. Reconciliation did NOT delete it."
    - "REJECT-1 (report defect) FIXED in reconciliation v2: v1 front matter (minor_findings: 5, informational_findings: 2) and Executive Summary (RC-1..RC-7) disagreed with the body (RC-1..RC-8 = 5 Minor + 3 Informational). v2 front matter/§1/§16/§17/§21/envelope are consistent: 0 Critical, 4 Major, 2 Minor, 3 Informational, RC-1..RC-10, RC-4 RESOLVED."
    - "REJECT-2 / RC-4 (report item) RESOLVED out-of-band: docs/decisions/US-001-open-decisions.md v2 and docs/evidence/US-001-clarification-report.md v2 exist (status APPROVED; OD-001..OD-006 RESOLVED with OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A; no decision content changed). Currently uncommitted — commit both with the PR. Produced by the open_decisions owner (us-clarifier / CLARIFICATION); no CLARIFICATION stage event in history.jsonl."
    - "REJECT-6 (report defect) FIXED in reconciliation v2 §15: PR accounting now has explicit categories (a) US-001 story changes, (b) harness-maintenance changes — docs/workflow/history.jsonl, docs/workflow/workflow-state.yaml, docs/evidence/.gitignore (4 harness-* entries + BOM, committed a96ebd5), the .gitignore /docs/harness-consistency-review.md line — described as PRESENT in the diff, and (c) excluded changes."
    - "RC-2 (Minor, unchanged): implemented 400/415 error message strings differ verbatim from the OpenAPI illustrative examples; 409 matches exactly; AC-6 body shape preserved; implemented messages more generic. Optional openapi-designer example alignment."
    - "RC-8 (Minor, unchanged): two .gitignore files carry pre-existing harness-scaffolding entries committed in a96ebd5 — classified harness-maintenance (§15b), already committed, not removable by reconciliation; flagged for the human diff reviewer."
    - "RC-5 / RC-6 / RC-7 (Informational, unchanged): AUTO_SERVER=TRUE + blank sa password (approved config, local-dev only); spring.datasource.password: \"\" (H2 default, not a secret); schema.sql id column has no explicit NOT NULL (H2 2.x implicit, ddl-auto=validate passes)."
    - "Post-correction sequence mandated by the human: after the code changes, rerun affected tests, then repeat IMPLEMENTATION_VERIFICATION, SECURITY_REVIEW, and RECONCILIATION. implementation_verification v1 and security_review v1 also consumed open_decisions v1 (now superseded by v2) and will be invalidated by the REJECT-3/4/5 edits — re-run required, not a separate BLOCKED."
    - "Traceability v2: AC-001/AC-003/AC-005/AC-006/AC-007 RECONCILED; AC-002 PARTIALLY_RECONCILED (RC-3/REJECT-4); AC-004 PARTIALLY_RECONCILED (RC-1/REJECT-3); security-posture SEC-1/SC-4 PARTIALLY_RECONCILED (RC-9/REJECT-5)."
    - "PR candidate scope (v2 §15, one entry per path): candidate_files 51 = 48 category-(a) US-001 story paths (28 code/build/config incl. .gitignore + 20 US-001 workflow-doc artifacts) + 3 category-(b) harness-maintenance paths (docs/workflow/history.jsonl, docs/workflow/workflow-state.yaml, docs/evidence/.gitignore). excluded_files 1 = the RC-10 stray src/main/.../docs/hooks/tool-usage.jsonl; standard git-ignored paths not counted. Cross-checked against git diff --name-status 47e3016..HEAD. No secret, no generated DB file in the include set. Counts as-of-write; docs/workflow/{history.jsonl,workflow-state.yaml} change again when this transition is recorded."
    - "Accepted deviations (from IMPLEMENTATION, re-confirmed): D-1 exception/InvalidPasswordException (FR-6 service re-check; plan C-12 left the type unspecified; mapped to 400, not reachable from the HTTP flow); D-2 CustomerPersistenceTest uses @SpringBootTest not @DataJpaTest; MF-1 the only change to a test-writer-owned test is a benign 2-char BCrypt-literal fix in CustomerSchemaTest, no assertion/scenario/outcome changed."
```
