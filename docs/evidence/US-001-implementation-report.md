---
artifact_type: implementation_report
story: US-001
version: 2
status: DRAFT
created_at: 2026-08-31T12:07:06Z
updated_at: 2026-09-02T14:45:00Z
produced_by: springboot-implementor
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
  - path: docs/reviews/reconciliation/US-001-reconciliation.md
    version: 2
supersedes: docs/evidence/US-001-implementation-report.md
tests_status: PASS
build_status: PASS
diagnostics_status: PASS
security_sensitive: true
---

# Implementation Report — US-001 Customer Registration (v2, corrective pass)

## 1. Summary

This is a **corrective implementation pass** (attempt 2), loop-back from
`RECONCILIATION` v2 (key `implementation_drift`) after the `HUMAN_PR_APPROVAL`
rejection of 2026-09-01. The registration feature delivered in v1 is unchanged;
this pass applies exactly the four code/hygiene corrections the human made
mandatory pre-PR and adds their test coverage.

| Item | Finding | Change | Status |
|---|---|---|---|
| 1 | RC-1 / REJECT-3 (Major) — record `RegistrationRequest.toString()` renders the plaintext password | Added a masking `toString()` (`password=***`), consistent with `Customer.toString()`; new `RegistrationRequestTest` | Done |
| 2 | RC-3 / REJECT-4 (Major) — concurrent duplicate trips `uq_customer_email` → unmapped `DataIntegrityViolationException` → `500` | `CustomerService.register` now maps a `uq_customer_email` violation (constraint-scoped) to `DuplicateEmailException` → existing `409`; any other integrity violation propagates unchanged; 2 new deterministic `CustomerServiceTest` cases | Done |
| 3 | RC-9 / REJECT-5 (Major, code half) — "deny-by-default" wording vs `anyRequest().authenticated()` | Aligned `SecurityConfig` javadoc + inline comment to "authentication-required by default (SC-4)"; behaviour and tests unchanged (option 1, the reconciliation's preferred path); one test comment reworded | Done (code); spec §7 / api-design §6 note is a documentation-direction finding for their owners — see §7 |
| 4 | RC-10 / REJECT-6 (Major, file removal) — stray `src/main/java/org/example/customerportal/docs/hooks/tool-usage.jsonl` | Deleted the stray `docs/` subtree under the package root | Done; hook output-path fix is a finding for the human — see §7 |

- **Validation status:** `./gradlew clean build` = **BUILD SUCCESSFUL**;
  **67 tests, 0 failures, 0 errors, 0 skipped** across 8 suites (was 62; +5:
  3 `RegistrationRequestTest`, 2 `CustomerServiceTest`).
- **Scope:** OD-005:A respected — no `GET /api/v1/customers/{id}`, no
  login / `UserDetailsService`, no rate limiting. No new dependency. No schema
  change (`uq_customer_email` already exists). No configuration change.
- **Open Decisions:** consumed `open_decisions` **v2** + `clarification_report`
  **v2** (both `APPROVED`, committed in `7ad07e1`): OD-001:A OD-002:B OD-003:A
  OD-004:A OD-005:A OD-006:A, all `RESOLVED`. None touched, none newly required.

## 2. Source Artifacts

| Artifact | Path | Version | Status |
|---|---|---|---|
| Story | `docs/stories/US-001-register-customer.md` | (unversioned) | IN_PROGRESS |
| Open Decisions | `docs/decisions/US-001-open-decisions.md` | 2 | APPROVED (OD-001..OD-006 RESOLVED; supersedes v1) |
| Clarification Report | `docs/evidence/US-001-clarification-report.md` | 2 | APPROVED (supersedes v1) |
| Specification | `docs/specifications/US-001-spec.md` | 1 | APPROVED |
| Specification Review | `docs/reviews/specifications/US-001-spec-review.md` | 1 | APPROVED (PASS) |
| API Design | `docs/designs/api/US-001-api-design.md` | 1 | APPROVED |
| OpenAPI Contract | `docs/designs/api/US-001-openapi.yaml` | 1 | APPROVED |
| DB Design | `docs/designs/database/US-001-db-design.md` | 1 | APPROVED |
| Entity Model | `docs/designs/database/US-001-entity-model.md` | 1 | APPROVED |
| Design Review | `docs/reviews/designs/US-001-design-review.md` | 1 | APPROVED (PASS) |
| Impact Analysis | `docs/impact-analysis/US-001-impact-analysis.md` | 1 | DRAFT (PASS; no review stage follows) |
| Implementation Plan | `docs/plans/US-001-implementation-plan.md` | 1 | APPROVED (PASS + HUMAN_PLAN_APPROVAL) |
| Plan Review | `docs/reviews/plans/US-001-plan-review.md` | 1 | APPROVED (PASS) |
| Test Strategy | `docs/tests/US-001-test-strategy.md` | 1 | DRAFT |
| AC-Test Matrix | `docs/tests/US-001-ac-test-matrix.md` | 1 | DRAFT (authoritative AC→test map) |
| Reconciliation (loop-back source) | `docs/reviews/reconciliation/US-001-reconciliation.md` | 2 | CHANGES_REQUIRED (RC-1/RC-3/RC-9/RC-10) |

No consumed input is `SUPERSEDED`.

**Staleness note (waiver):** `specification` v1, `implementation_plan` v1 and
`ac_test_matrix` v1 record `open_decisions` version 1 in their front matter,
while `open_decisions` is now v2. `open_decisions` v2 records "No decision
content changed" (same six option letters as resolved at `HUMAN_SPEC_APPROVAL`);
the code always used the resolved values, and `stage-map.yaml` gives
`IMPLEMENTATION` no loop-back to `SPECIFICATION`. Proceeding is correct; the
mandated `RECONCILIATION` re-run should note the version references rather than
re-open them.

## 3. Implemented Acceptance Criteria (delta only)

Full AC coverage is unchanged from v1 §3. This pass affects:

| AC | v1 status | Change in v2 | v2 status | Verifying test(s) |
|---|---|---|---|---|
| AC-002 Duplicate email, case-insensitive → `409` | RECONCILED (single-request) / PARTIALLY_RECONCILED (concurrent) | Concurrent `uq_customer_email` race now also → `409` via `CustomerService.register` catch → `DuplicateEmailException` → `GlobalExceptionHandler.handleDuplicateEmail` | RECONCILED (both paths) | `CustomerServiceTest.concurrentDuplicateEmailUniqueViolationIsMappedToDuplicateEmailException`, `.anUnrelatedIntegrityViolationIsNotReportedAsADuplicateEmail`; existing `.duplicateEmailSameCaseThrowsAndDoesNotSave`, `.duplicateEmailDifferentCaseThrowsAndDoesNotSave`, `CustomerRegistrationApiTest.duplicateEmailIsRejectedCaseInsensitivelyWith409` |
| AC-004 Password stored as BCrypt hash, never plaintext | PARTIALLY_RECONCILED (RC-1 latent `toString()` leak) | `RegistrationRequest.toString()` masks `password` | RECONCILED | `RegistrationRequestTest.toStringNeverRendersTheSubmittedPlaintextPassword`, `.toStringOfANullPasswordStillDoesNotLeakAndDoesNotThrow`, `.passwordAccessorStillReturnsTheRealValue` |
| SEC-1 / SC-4 posture | PARTIALLY_RECONCILED (RC-9 wording) | `SecurityConfig` javadoc/comment aligned to "authentication-required by default (SC-4)"; mechanism (`anyRequest().authenticated()`) unchanged | RECONCILED (code); doc note pending for spec/api-design owners | `RegistrationSecurityPostureTest.protectedRouteReturns401WhenUnauthenticated` (unchanged, still green) |

## 4. Change Set

Base path `src/main/java/org/example/customerportal/`. Classified against
`docs/reviews/reconciliation/US-001-reconciliation.md` v2 §17 (RC-1, RC-3, RC-9,
RC-10).

### Modified — production (Planned corrective)

| File | Change | Finding |
|---|---|---|
| `model/request/RegistrationRequest.java` | Added `@Override toString()` returning `"RegistrationRequest{email='" + email + "', password=***}"`; javadoc note | RC-1 |
| `service/CustomerService.java` | `register(...)` wraps `customerRepository.save` in `try/catch (DataIntegrityViolationException)`; new private `isEmailUniquenessViolation(...)` (Hibernate `ConstraintViolationException#getConstraintName()` + message-chain fallback, both matched case-insensitively against `uq_customer_email`); maps a match to `DuplicateEmailException`, rethrows anything else; import + javadoc | RC-3 |
| `security/SecurityConfig.java` | Class javadoc bullet and one inline comment reworded from "deny-by-default" to "authentication-required by default (SC-4)"; no behavioural change | RC-9 |

### Modified — test (Planned corrective)

| File | Change | Finding |
|---|---|---|
| `service/CustomerServiceTest.java` | +2 tests (constraint-scoped `uq_customer_email` → `DuplicateEmailException`; unrelated integrity violation propagates unchanged, asserted `isSameAs`); import `DataIntegrityViolationException` | RC-3 |
| `security/RegistrationSecurityPostureTest.java` | Reworded the `protectedRouteReturns401WhenUnauthenticated` doc comment ("deny-by-default" → "authentication-required by default"); no assertion change | RC-9 |

### Created — test (Planned corrective)

| File | Level | Tests | Finding |
|---|---|---|---|
| `model/request/RegistrationRequestTest.java` | unit | 3 — `toString()` masks the plaintext password / keeps email; null-password `toString()` does not throw or leak; `password()` accessor still returns the real value | RC-1 |

### Deleted

| Path | Reason | Finding |
|---|---|---|
| `src/main/java/org/example/customerportal/docs/` (subtree: `hooks/tool-usage.jsonl`) | Stray, untracked hook telemetry misplaced under the Java source root; not covered by the `/docs/hooks/tool-usage.jsonl` ignore rule; must not enter the PR or sit in `src/` | RC-10 |

### Unrelated changes

None. No change to `build.gradle.kts`, `application.yaml`,
`application-test.yaml`, `schema.sql`, `.gitignore`, or any entity/repository.

## 5. Validation Evidence

Environment: Gradle 9.7.1 (wrapper), toolchain Java 21, Spring Boot 4.1.1,
Hibernate ORM 7.4.5, H2 2.x. Commands run from the repo root.

| Check | Command | Result |
|---|---|---|
| Compile (main + test) | `./gradlew --offline compileJava compileTestJava` | SUCCESS, no warnings |
| Full test run | `./gradlew --offline clean test` | **67 tests, 0 failures, 0 errors, 0 skipped** |
| Full build (`check` + assemble) | `./gradlew --offline clean build` | **BUILD SUCCESSFUL** |
| `service.CustomerServiceTest` | (in run) | 7/7 PASS (was 5; +2 RC-3) |
| `model.request.RegistrationRequestTest` | (in run) | 3/3 PASS (new, RC-1) |
| `security.RegistrationSecurityPostureTest` | (in run) | 4/4 PASS (unchanged behaviour, RC-9) |
| `registration.CustomerRegistrationApiTest` | (in run) | 22/22 PASS (regression) |
| `persistence.CustomerSchemaTest` / `CustomerPersistenceTest` | (in run) | 10/10 + 3/3 PASS (regression) |
| `validation.PasswordPolicyValidatorTest` | (in run) | 17/17 PASS (regression) |
| `CustomerPortalApplicationTests.contextLoads` | (in run) | 1/1 PASS |
| `ddl-auto=validate` (test profile) | test-suite context boot | clean — no schema-validation error |
| Working-tree hygiene | `git status --short` | 4 modified source files + 1 new test dir; no `data/`, no stray files |

IDEA MCP semantic/diagnostic tooling was not invoked by this Skill; layering was
re-checked by inspection (the RC-3 change keeps `service` → `exception` only;
`org.hibernate.exception.ConstraintViolationException` is a compile-time
reference to a transitive `spring-boot-starter-data-jpa` dependency, no new
declared dependency). Independent semantic/dependency checks remain
`IMPLEMENTATION_VERIFICATION`'s.

## 6. Configuration Changes

None.

## 7. Deviations and Discovered Problems

### D-1 — RC-9 documentation note is out of this Skill's authority (finding for spec-writer / openapi-designer)

The reconciliation's preferred RC-9 fix pairs the code-comment alignment with a
one-line note in `docs/specifications/US-001-spec.md` §7 (SEC-1 row) and
`docs/designs/api/US-001-api-design.md` §6 / §8, both of which currently say
"deny-by-default". Those artifacts are owned by `spec-writer` and
`openapi-designer` (`artifact-paths.yaml`); this Skill did not edit them. The
required note: *"'deny by default' here means authentication-required by default
per SC-4 — `anyRequest().authenticated()`, not a literal `denyAll()`."*
No behavioural change; the code side (SecurityConfig + tests) is complete and
consistent with SC-4 as written in `security-conventions.md`.

### D-2 — RC-10 hook output-path fix is hook configuration (finding for the human)

The stray file was deleted. Its root cause — a hook writing tool-usage telemetry
to a path that resolved under `src/main/java/...` instead of the repo-level
`docs/hooks/` — is hook configuration, outside this Skill's authority and the
implementation scope. The human should correct the hook's output path (and/or
broaden the `.gitignore` rule) so the telemetry lands under `docs/hooks/`.

### D-3 — RC-3 mapping placed in the service, not `GlobalExceptionHandler`

The reconciliation allowed either. The service-layer catch was chosen: it reuses
the existing `DuplicateEmailException` → `409` mapping in
`GlobalExceptionHandler` (no HTTP concern added to the service — the domain
exception carries none), and it is deterministically unit-testable with a mocked
repository. `save()` executes the INSERT synchronously under
`GenerationType.IDENTITY`, so the violation surfaces inside the `try` rather than
at transaction commit.

### D-4 — RC-3 constraint scoping is name + message based

`isEmailUniquenessViolation` first inspects
`org.hibernate.exception.ConstraintViolationException#getConstraintName()`, then
falls back to a case-insensitive `contains("uq_customer_email")` scan of the
cause-chain messages (H2 names the backing unique index after the constraint).
The fallback matches the **constraint token**, not any email-shaped text, so a
non-email integrity violation whose message quotes the row's email value does
not false-positive. The two new `CustomerServiceTest` cases exercise the
message-fallback path (positive and negative) without coupling the test to a
Hibernate exception constructor signature; the negative case was confirmed
load-bearing (it fails if the constraint-token check is removed).

### RC-2, RC-5, RC-6, RC-7, RC-8 — not addressed here (by design)

Per reconciliation v2 these are Minor/Informational with **no required
correction** or are already-committed harness-maintenance items; none is in this
loop-back's scope.

## 8. Open Decisions

None touched; none newly required. `open_decisions` v2 (OD-001:A OD-002:B
OD-003:A OD-004:A OD-005:A OD-006:A, all `RESOLVED`) was consumed as-is. No
security-sensitive decision is missing: the RC-1 masking closes the last latent
credential-exposure path, and RC-3 makes the concurrent duplicate path behave
identically to the pre-checked one.

## 9. Result

```yaml
result:
  verdict: PASS
  stage: IMPLEMENTATION
  story: US-001
  artifact_status: DRAFT
  artifacts:
    - docs/evidence/US-001-implementation-report.md
  next_stage: IMPLEMENTATION_VERIFICATION
  loop_back_stage: null
  blocking_issues: []
  non_blocking_findings:
    - "RC-1 DONE: RegistrationRequest.toString() now masks password (password=***), consistent with Customer.toString(); RegistrationRequestTest (3 tests) proves the submitted plaintext is never rendered and the password() accessor is unchanged."
    - "RC-3 DONE: CustomerService.register maps a uq_customer_email DataIntegrityViolationException (constraint-scoped via Hibernate constraint name + message-chain fallback) to DuplicateEmailException -> existing 409; any other integrity violation is rethrown unchanged. CustomerServiceTest +2 deterministic cases (positive + isSameAs negative)."
    - "RC-9 DONE (code half): SecurityConfig javadoc + inline comment reworded from 'deny-by-default' to 'authentication-required by default (SC-4)'; anyRequest().authenticated() unchanged; RegistrationSecurityPostureTest unchanged (still green), one doc comment reworded. Documentation-direction finding D-1: spec §7 / api-design §6/§8 still say 'deny-by-default' and need the one-line clarifying note from their owners (spec-writer / openapi-designer)."
    - "RC-10 DONE (removal): deleted src/main/java/org/example/customerportal/docs/ (stray hooks/tool-usage.jsonl). Finding D-2 for the human: fix the hook's output path so telemetry lands under docs/hooks/ (hook config, out of implementation scope)."
    - "Staleness waiver: specification v1 / implementation_plan v1 / ac_test_matrix v1 reference open_decisions v1; open_decisions v2 changed no decision content. Proceed; RECONCILIATION re-run should note, not re-open."
    - "Validation: ./gradlew clean build BUILD SUCCESSFUL; 67 tests (was 62; +5), 0 failures/errors/skipped, 8 suites. No dependency, schema, or config change. OD-005:A scope respected."
    - "Human-mandated post-correction sequence still pending: rerun done here; IMPLEMENTATION_VERIFICATION, SECURITY_REVIEW, RECONCILIATION must re-run against these changes and open_decisions v2 (implementation_verification v1 + security_review v1 consumed open_decisions v1 and predate RC-1/RC-3/RC-9/RC-10)."
```
