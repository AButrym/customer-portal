---
artifact_type: implementation_verification
story: US-001
version: 2
status: DRAFT
created_at: 2026-09-02T15:04:46Z
updated_at: 2026-09-02T15:04:46Z
produced_by: implementation-verifier
inputs:
  - path: docs/stories/US-001-register-customer.md
    version: null
  - path: docs/specifications/US-001-spec.md
    version: 1
  - path: docs/reviews/specifications/US-001-spec-review.md
    version: 1
  - path: docs/impact-analysis/US-001-impact-analysis.md
    version: 1
  - path: docs/plans/US-001-implementation-plan.md
    version: 1
  - path: docs/reviews/plans/US-001-plan-review.md
    version: 1
  - path: docs/evidence/US-001-implementation-report.md
    version: 2
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
  - path: docs/tests/US-001-test-strategy.md
    version: 1
  - path: docs/tests/US-001-ac-test-matrix.md
    version: 1
supersedes: docs/verification/US-001-implementation-verification.md
build_status: PASS
tests_status: PASS
acceptance_criteria_verified: 7
acceptance_criteria_total: 7
critical_findings: 0
major_findings: 0
minor_findings: 3
semantic_analysis: TEXT_FALLBACK
---

# Implementation Verification — US-001 Customer Registration (v2, post-corrective-pass re-run)

## 1. Executive Summary

**Verdict: PASS.** The corrective implementation pass (implementation_report v2,
attempt 2) is functionally correct, complete, traceable, architecturally
compliant, and ready for the mandated Security Review re-run.

- **Why this re-run:** the `HUMAN_PR_APPROVAL` rejection of 2026-09-01 escalated
  three previously-Minor items to required code changes and mandated
  `IMPLEMENTATION_VERIFICATION` → `SECURITY_REVIEW` → `RECONCILIATION` be repeated
  against the changed source. Verification **v1 is superseded** by this document.
- **Build:** `./gradlew clean build` independently reproduced — **BUILD
  SUCCESSFUL** (exit 0).
- **Tests:** independently reproduced — **67 tests, 0 failures, 0 errors,
  0 skipped** across **8 suites** (v1 baseline was 62 / 7; +5: 3
  `RegistrationRequestTest`, 2 `CustomerServiceTest`).
- **Acceptance Criteria:** 7 of 7 (AC-001..AC-007) **VERIFIED**; AC-002 and
  AC-004 — `PARTIALLY_RECONCILED` in traceability v2 — are now fully covered by
  the corrective changes (see §7).
- **Corrective delta (RC-1 / RC-3 / RC-9 / RC-10):** all four verified applied
  and correct (§17). Prior v1 findings **MF-3** (concurrent duplicate → 500) and
  **MF-5** (`RegistrationRequest.toString()` renders plaintext) are **CLOSED**.
- **Findings:** 0 Critical, 0 Major, 3 Minor — all carried, none blocking, none
  requiring a code change for this Story. MF-a is the documentation half of RC-9
  (owned by `spec-writer` / `openapi-designer`, tracked for `RECONCILIATION`
  closure); MF-b is the OpenAPI illustrative-example wording (carried v1 MF-2);
  MF-c is the `open_decisions` staleness waiver on three upstream inputs.
- **Recommended next action:** advance to `SECURITY_REVIEW`.

## 2. Verified Artifacts

| Artifact | Path | Version | Status |
|---|---|---|---|
| Story | docs/stories/US-001-register-customer.md | (unversioned) | IN_PROGRESS |
| Specification | docs/specifications/US-001-spec.md | 1 | APPROVED |
| Specification Review | docs/reviews/specifications/US-001-spec-review.md | 1 | APPROVED (PASS) |
| API Design | docs/designs/api/US-001-api-design.md | 1 | APPROVED |
| OpenAPI Contract | docs/designs/api/US-001-openapi.yaml | 1 | APPROVED |
| DB Design | docs/designs/database/US-001-db-design.md | 1 | APPROVED |
| Entity Model | docs/designs/database/US-001-entity-model.md | 1 | APPROVED |
| Design Review | docs/reviews/designs/US-001-design-review.md | 1 | APPROVED (PASS) |
| Impact Analysis | docs/impact-analysis/US-001-impact-analysis.md | 1 | DRAFT (PASS; no review stage follows) |
| Implementation Plan | docs/plans/US-001-implementation-plan.md | 1 | APPROVED (PASS + HUMAN_PLAN_APPROVAL) |
| Plan Review | docs/reviews/plans/US-001-plan-review.md | 1 | APPROVED (PASS) |
| Test Strategy | docs/tests/US-001-test-strategy.md | 1 | DRAFT |
| AC–Test Matrix | docs/tests/US-001-ac-test-matrix.md | 1 | DRAFT (authoritative AC→test map) |
| Implementation Report | docs/evidence/US-001-implementation-report.md | **2** | DRAFT (corrective pass) |
| Reconciliation (loop-back source) | docs/reviews/reconciliation/US-001-reconciliation.md | 2 | CHANGES_REQUIRED (RC-1/RC-3/RC-9/RC-10) |

No consumed input is `SUPERSEDED`.

**Staleness waiver (carried, not re-opened — MF-c):** `specification` v1,
`implementation_plan` v1 and `ac_test_matrix` v1 record `open_decisions` version
1 in front matter while `open_decisions` is now v2. `open_decisions` v2's
change-log records *"No decision content changed"* (same six letters OD-001:A
OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A, as resolved at
`HUMAN_SPEC_APPROVAL`). `open_decisions` is **not an input** to this stage
(`stage-map.yaml` `IMPLEMENTATION_VERIFICATION.inputs`); the code always used the
resolved values. Proceeding is correct; `RECONCILIATION` should note, not
re-open, the version references.

## 3. Environment

- JDK: Gradle toolchain Java 21; Spring Boot 4.1.1; Hibernate ORM 7.4.5; H2 2.x;
  Gradle 9.7.1 (wrapper).
- Build tool: `./gradlew` (Kotlin DSL), run from the repo root.
- Active profile under test: `test` (`@ActiveProfiles("test")` on every
  Spring-context test; `src/test/resources/application-test.yaml`).
- Database mode: isolated in-memory H2 for tests
  (`jdbc:h2:mem:us001;DB_CLOSE_DELAY=-1`); file H2 for the default profile
  (`jdbc:h2:file:./data/customer-portal;AUTO_SERVER=TRUE`).
- Verification tooling: built-in file inspection, `git`, Gradle. IDEA MCP
  semantic tooling not invoked — architecture checks are text/inspection
  fallback (`semantic_analysis: TEXT_FALLBACK`); layering conclusions rest on
  import graphs and method signatures, not PSI call analysis.
- No secrets encountered or recorded.

## 4. Repository State

- **Branch: `us-001`** (v1 recorded `main` — corrected here). `git status`:
  working tree **clean**.
- Corrective pass committed as `6c7d9e8 "Stage IMPLEMENTATION corrective pass
  completed"`; prior workflow commits `7ad07e1`, `155cf5c`, `408edd0`, `a96ebd5`,
  `580ba72`, `5e17151`, `ba6e0c0`.
- `git diff main...HEAD` — 52 files (`7969 (+) / 9 (−)`): the full US-001 story
  change set plus 3 harness-maintenance files
  (`docs/workflow/history.jsonl`, `docs/workflow/workflow-state.yaml`,
  `docs/evidence/.gitignore`) and `.gitignore`. Classification is reconciliation
  v2 §15's responsibility; no change here.
- Corrective diff `7ad07e1..6c7d9e8` touches `src/`: 3 production files modified
  (`RegistrationRequest.java`, `SecurityConfig.java`, `CustomerService.java`),
  2 test files modified (`CustomerServiceTest.java`,
  `RegistrationSecurityPostureTest.java`), 1 new test file
  (`RegistrationRequestTest.java`). No other `src/` change.
- **Deleted:** `src/main/java/org/example/customerportal/docs/` subtree
  (stray `hooks/tool-usage.jsonl`) — confirmed **absent**
  (`ls` → "No such file or directory"); the `customerportal` package tree now
  contains only `config`, `controller`, `exception`, `model`, `repository`,
  `security`, `service`, `validation`.
- Untracked: none under `src/**`. Generated `./data/` — not present, git-ignored
  (`.gitignore` `/data/`).

## 5. Build Evidence

| Check | Command | Result |
|---|---|---|
| Full build | `./gradlew clean build` | **BUILD SUCCESSFUL in 12s**, exit 0 |
| Compilation | `:compileJava` / `:compileTestJava` | no errors, no warnings |
| `:test` + `:check` | (part of `build`) | pass |
| `bootJar` / `assemble` | (part of `build`) | pass |

Only non-functional output: a Gradle 10 deprecation notice (Gradle-internal,
not project code). No `HHH*` Hibernate schema-validation error at context
startup.

## 6. Test Evidence

Independently reproduced via `./gradlew clean build`; per-suite counts read from
`build/test-results/test/TEST-*.xml`.

| Suite | Tests | Fail | Err | Skip | Δ vs v1 |
|---|---|---|---|---|---|
| `registration.CustomerRegistrationApiTest` | 22 | 0 | 0 | 0 | — |
| `validation.PasswordPolicyValidatorTest` | 17 | 0 | 0 | 0 | — |
| `persistence.CustomerSchemaTest` | 10 | 0 | 0 | 0 | — |
| `service.CustomerServiceTest` | 7 | 0 | 0 | 0 | +2 (RC-3) |
| `security.RegistrationSecurityPostureTest` | 4 | 0 | 0 | 0 | — (1 comment reworded) |
| `model.request.RegistrationRequestTest` | 3 | 0 | 0 | 0 | +3 new (RC-1) |
| `persistence.CustomerPersistenceTest` | 3 | 0 | 0 | 0 | — |
| `CustomerPortalApplicationTests` | 1 | 0 | 0 | 0 | — |
| **Total** | **67** | **0** | **0** | **0** | **+5** |

No test is `@Disabled`; no test is skipped. Matches implementation_report v2 §5
exactly.

## 7. Acceptance Criteria Matrix

Full AC verification is carried from v1 §7 (unchanged for AC-001, AC-003, AC-005,
AC-006, AC-007). This re-run re-confirms all seven and records the delta for
AC-002 and AC-004.

| AC | Required behavior | Status | Delta evidence |
|---|---|---|---|
| **AC-001** | Valid email + compliant password → `201` + `Location`, account persisted (role `CUSTOMER`, enabled) | VERIFIED | unchanged — `CustomerRegistrationApiTest` (validRegistration…, normalisedToLowercase, password72…), `CustomerServiceTest.happyPath…` (real `BCryptPasswordEncoder.matches`) |
| **AC-002** | Duplicate email (any case) → `409`, no 2nd account — **single-request and concurrent** | VERIFIED | Single-request path unchanged (`existsByEmail` guard → `DuplicateEmailException` → 409). **Concurrent race now covered:** `CustomerService.register` wraps `save` in `try/catch (DataIntegrityViolationException)`; `isEmailUniquenessViolation(...)` maps a `uq_customer_email` violation (Hibernate `ConstraintViolationException#getConstraintName()` + cause-chain message fallback, both case-insensitive) to `DuplicateEmailException` → existing `409`; any other integrity violation is rethrown. Tests: `CustomerServiceTest.concurrentDuplicateEmailUniqueViolationIsMappedToDuplicateEmailException`, `.anUnrelatedIntegrityViolationIsNotReportedAsADuplicateEmail` (asserts `isSameAs` the original — negative case is load-bearing). |
| **AC-003** | Invalid/blank/over-length email → `400` + `fieldErrors[email]`, no account | VERIFIED | unchanged |
| **AC-004** | Password persisted only as BCrypt hash, never plaintext — **incl. no plaintext in `toString()`** | VERIFIED | Persistence/hash path unchanged. **`toString()` leak closed:** `RegistrationRequest.toString()` now returns `"RegistrationRequest{email='…', password=***}"`, mirroring `Customer.toString()` (which excludes `passwordHash`). Tests: `RegistrationRequestTest.toStringNeverRendersTheSubmittedPlaintextPassword` (asserts the distinctive secret is absent, `password=***` present), `.toStringRenderIsIndependentOfThePasswordValueAndDoesNotThrowOnNull` (null-safe), `.passwordAccessorStillReturnsTheRealValue` (accessor unchanged). |
| **AC-005** | Response contains neither password nor hash (nor `enabled`/`updatedAt`) | VERIFIED | unchanged — `CustomerResponse` = `id, email, role, createdAt`; `successResponseNeverExposesCredentialOrInternalState` |
| **AC-006** | Password policy incl. 72-**byte** bound → `400` + `fieldErrors[password]`; service re-check | VERIFIED | unchanged — `@ValidPassword` / `PasswordPolicyValidator` (UTF-8 bytes, 4 classes); service `isCompliant` re-check → `InvalidPasswordException`; 8 web vectors + 17 validator unit tests + service test |
| **AC-007** | Missing / non-JSON `Content-Type` → `415`, no account | VERIFIED | unchanged — `consumes=APPLICATION_JSON_VALUE`; `handleMediaType` → `415`; `nonJsonContentTypeReturns415`, `missingContentTypeReturns415` |

Derived rules (unknown property → `400`, malformed JSON → `400`, AC-6 error body
shape, no internal leakage) — re-confirmed via
`CustomerRegistrationApiTest.unknownJsonPropertyReturns400`, `.malformedJsonReturns400`,
`.errorBodyHasTheApiConventionShape`, `.errorBodyNeverLeaksInternals`.

## 8. API Contract Verification

Re-compared against `docs/designs/api/US-001-openapi.yaml` v1. No contract
element changed in the corrective pass.

- `POST /api/v1/customers`, public, `application/json` only, `415` otherwise,
  `additionalProperties:false`, `201` + `Location` + `CustomerResponse` — all ✅
  (unchanged from v1 §8).
- **`409` path:** the corrective change routes the concurrent-race
  `DataIntegrityViolationException` into the **same** `DuplicateEmailException` →
  `GlobalExceptionHandler.handleDuplicateEmail` → `409` +
  `"An account with this email already exists."` (matches the OpenAPI `409`
  example verbatim). No new status code, no new response shape.
- **Deviation (Minor, MF-b — carried v1 MF-2):** implemented `400` (single
  missing/malformed/unknown-field message) and `415`
  (`"Content-Type must be application/json."`) message strings differ verbatim
  from the OpenAPI illustrative `examples`. The `examples` are non-normative; the
  `409` message matches exactly; every test asserts status + body **shape**.
  Consistent with disclosed D-4 / plan-review F-4. No contract-behavior mismatch.

## 9. Persistence Verification

No persistence change in the corrective pass. `schema.sql`, the `Customer`
entity, `CustomerRepository`, `application.yaml` / `application-test.yaml`
(`ddl-auto: validate`, `open-in-view: false`, file vs in-memory H2) are byte-for-byte
unchanged from v1. All v1 §9 conclusions carry:

- `customer` table, `id BIGINT` identity PK, `email VARCHAR(254) NOT NULL` +
  `uq_customer_email` UNIQUE, `password_hash VARCHAR(60) NOT NULL`,
  `role VARCHAR(20) NOT NULL` (`EnumType.STRING` + CHECK), `enabled BOOLEAN NOT NULL`,
  `created_at`/`updated_at` `TIMESTAMP WITH TIME ZONE NOT NULL` UTC,
  `created_at` not updatable — all ✅ against H2 `INFORMATION_SCHEMA` assertions
  in `CustomerSchemaTest` (10 tests) and round-trips in `CustomerPersistenceTest`
  (3 tests).
- **R-1 CLOSED (re-verified):** `OffsetDateTime` ↔ `TIMESTAMP WITH TIME ZONE`
  validates under `ddl-auto=validate` on H2 2.x / Hibernate 7.4.5; context boots
  clean.
- The RC-3 change relies on the already-present `uq_customer_email` constraint;
  it adds no schema element.

## 10. Architecture Verification

Method: import-graph + signature inspection (`TEXT_FALLBACK`). The corrective
pass introduces one new cross-package reference to check:

| Rule | Evidence | Status |
|---|---|---|
| Controller → Service only | unchanged from v1 | ✅ |
| Service owns business logic | `CustomerService` — normalize, policy re-check, duplicate guard (pre-check **and** post-insert constraint mapping), encode, map | ✅ |
| No HTTP types in Service | RC-3 catch block uses `org.springframework.dao.DataIntegrityViolationException` and `org.hibernate.exception.ConstraintViolationException` — **persistence/DAO exceptions, not `org.springframework.http` / servlet types**. The service still imports no HTTP type; the domain `DuplicateEmailException` (no HTTP concern) carries the mapping to the advice. Compliant with AD-3 / "no HTTP in service". | ✅ |
| New declared dependency? | No. `org.hibernate.exception.ConstraintViolationException` is a compile-time reference to a transitive `spring-boot-starter-data-jpa` class; `build.gradle.kts` diff `7ad07e1..6c7d9e8` is empty. | ✅ |
| Single `@RestControllerAdvice` | still exactly one — `GlobalExceptionHandler`; the RC-3 mapping reuses its existing `handleDuplicateEmail` branch | ✅ |
| `RegistrationRequest.toString()` override | a DTO rendering concern, no layering impact; mirrors `Customer.toString()` | ✅ |
| `SecurityConfig` change | javadoc + one inline comment only; `anyRequest().authenticated()` unchanged | ✅ |
| No new architectural layer | none | ✅ |

No architecture violation. (Confidence: high for imports/signatures; call-path
direction not PSI-cross-checked — see §18.)

## 11. Validation and Error Handling

- Request-layer validation unchanged and still runtime-active (AC-003 / AC-006
  web tests exercise the real MVC stack).
- **RC-3 mapping is deterministically unit-tested** with a mocked repository —
  `save(...)` throws a constructed `DataIntegrityViolationException` wrapping a
  `SQLIntegrityConstraintViolationException` whose message names
  `UQ_CUSTOMER_EMAIL_INDEX_5`; the service maps it to `DuplicateEmailException`.
  The negative test uses a `CK_CUSTOMER_ROLE` message and asserts the **original**
  exception propagates (`isSameAs`), so the constraint-scoping is proven
  load-bearing, not incidental.
- `InvalidPasswordException` (service re-check) → `400`; media-type → `415`;
  malformed/unknown JSON → `400`; unmapped → `500` generic. Unchanged.
- `GlobalExceptionHandler` still reads only `HttpServletRequest` +
  `BindingResult.getFieldErrors()` — never the bound DTO.

## 12. Basic Security Readiness

| Check | Evidence | Result |
|---|---|---|
| No plaintext password persisted | unchanged — no plaintext column; `CustomerSchemaTest.noPlaintextPasswordColumnExists` | PASS |
| Password hash never returned | unchanged — `CustomerResponse` excludes it; `successResponseNeverExposesCredentialOrInternalState` | PASS |
| **Password not exposed via `toString()`** | **RC-1 closed:** `RegistrationRequest.toString()` masks `password` (`password=***`); `RegistrationRequestTest` (3 tests) proves the submitted plaintext is never rendered and is null-safe. Consistent with `Customer.toString()`. | PASS (v1 MF-5 CLOSED) |
| Password not logged | unchanged — production code has **no logger / `System.out` / `println`**; `GlobalExceptionHandler` never touches the request DTO | PASS |
| BCrypt encoder, no no-op | unchanged — `BCryptPasswordEncoder`; `CustomerServiceTest` asserts a genuine `$2a$`-format verifying hash | PASS |
| **Concurrent duplicate → `409` not `500`** | **RC-3 closed:** constraint-scoped mapping; `CustomerServiceTest` +2 | PASS (v1 MF-3 CLOSED) |
| Public scope minimal | unchanged — `REGISTRATION_ENDPOINT` matcher = exactly `POST /api/v1/customers`; `anyRequest().authenticated()` | PASS |
| CSRF exemption scoped | unchanged — same single matcher; CSRF otherwise enabled | PASS (depth arbitration is SECURITY_REVIEW's — R-2) |
| Authentication-required by default | `RegistrationSecurityPostureTest.protectedRouteReturns401WhenUnauthenticated` (401, not a form-login 302); `HttpStatusEntryPoint(401)`; `formLogin`/`httpBasic`/`logout` disabled. **RC-9 code wording** reworded to "authentication-required by default (SC-4) … not a literal `denyAll()`" — behavior identical, test comment reworded, assertion unchanged (still green). | PASS |
| H2 console not exposed | unchanged — `spring.h2.console.enabled=false` both profiles; `h2ConsoleIsNotExposed` | PASS |
| Validation message hygiene | unchanged — fixed generic strings; no-echo asserted | PASS |

**Forwarded to `SECURITY_REVIEW` (mandated full re-run):**
(a) final CSRF-scope / posture arbitration (R-2);
(b) message-hygiene sign-off (R-7);
(c) confirm the RC-3 constraint-name/message matching cannot be induced to
misclassify by a crafted email value (the negative test covers the
`CK_CUSTOMER_ROLE` case; SECURITY_REVIEW to judge completeness);
(d) confirm no debug-level logging config could still surface a bound
`RegistrationRequest` before the `toString()` mask (mask is now in place
regardless);
(e) sign-off that the RC-9 wording resolution (documented, not `denyAll()`) is
acceptable and that `security-conventions.md` SC-4 is satisfied.

## 13. Configuration Verification

No configuration change in the corrective pass (`build.gradle.kts`,
`application.yaml`, `application-test.yaml`, `schema.sql`, `.gitignore` all
unchanged in `7ad07e1..6c7d9e8`). All v1 §13 conclusions carry:
file-H2 default / in-memory test, `ddl-auto=validate`, `open-in-view=false`,
`h2.console.enabled=false`, `fail-on-unknown-properties=true`,
`.gitignore /data/`. No secrets, no new ports, no JVM options.

## 14. Test Quality Review

- Every mandatory AC still has ≥1 web- or persistence-level test on the real
  stack; no AC depends solely on a mock.
- **New `RegistrationRequestTest`** (unit): asserts observable `toString()`
  output, uses a distinctive secret literal, checks null-safety and
  value-independence, and confirms the `password()` accessor is untouched — no
  false-positive risk.
- **New `CustomerServiceTest` RC-3 cases:** positive maps to
  `DuplicateEmailException`; negative asserts `isSameAs` the injected unrelated
  exception (fails if the constraint-token check is removed). Deterministic,
  no reliance on a real DB race.
- `RegistrationSecurityPostureTest` — only a doc comment changed; 4/4 still green
  against the real `SecurityFilterChain`.
- No test was weakened, disabled, or had an assertion relaxed. `git diff
  7ad07e1..6c7d9e8 -- src/test/` shows only additions plus the one comment
  reword.

## 15. Scope Verification

Corrective change set vs. reconciliation v2 §17 (RC-1 / RC-3 / RC-9 / RC-10):

| Class | Files | Status |
|---|---|---|
| RC-1 (planned corrective) | `model/request/RegistrationRequest.java` (+`toString()` + javadoc); new `model/request/RegistrationRequestTest.java` | matches reconciliation directive |
| RC-3 (planned corrective) | `service/CustomerService.java` (try/catch + `isEmailUniquenessViolation` + javadoc + import); `service/CustomerServiceTest.java` (+2 tests + import) | matches directive; mapping placed in service (D-3, reconciliation allowed either) |
| RC-9 (planned corrective, code half) | `security/SecurityConfig.java` (javadoc + 1 inline comment); `security/RegistrationSecurityPostureTest.java` (1 comment) | matches directive; behavior + assertions unchanged |
| RC-10 (planned corrective) | deleted `src/main/java/org/example/customerportal/docs/` subtree | confirmed removed |
| Unexpected | none | — |
| Unrelated | none | — |

`git diff 7ad07e1..6c7d9e8 -- src/` confirms **exactly** these changes and
nothing else. No dependency, schema, or config change. OD-005:A scope respected
(no `GET /{id}`, no login / `UserDetailsService`, no rate limiting).

## 16. Implementation Report Accuracy

Implementation report **v2** is **materially consistent with observed evidence**.

- Build / test claims (BUILD SUCCESSFUL; 67 tests / 8 suites / 0 failures) —
  independently reproduced, exact.
- The four corrective changes and their file lists (§4) — confirmed present and
  as described.
- Deviations D-1..D-4 in report v2 §7 are disclosed with accurate detail; D-1
  (spec/api-design doc note) and D-2 (hook output-path) are correctly identified
  as out-of-scope findings for other owners / the human.
- `front-matter status: DRAFT` on the report is expected at this stage.
- Report v2's "State Correction" note (open_decisions v2 / clarification_report
  v2 already committed in `7ad07e1`) is accurate — `git log` confirms.

No omitted files, no incorrect status claims, no undisclosed security-sensitive
change.

## 17. Findings

0 Critical, 0 Major, 3 Minor. None blocks progression to Security Review; none
requires a code change for this Story.

### Closed since v1

- **MF-3 (v1) → CLOSED.** Concurrent duplicate registration now maps to `409`
  via the constraint-scoped `DataIntegrityViolationException` catch in
  `CustomerService.register`. Verified by
  `CustomerServiceTest.concurrentDuplicateEmailUniqueViolationIsMappedToDuplicateEmailException`
  and the load-bearing negative case.
- **MF-5 (v1) → CLOSED.** `RegistrationRequest.toString()` masks the plaintext
  password. Verified by `RegistrationRequestTest` (3 tests).
- **MF-1 (v1) — no longer in scope.** The `CustomerSchemaTest` BCrypt-literal
  fixture correction was in the `IMPLEMENTATION` attempt-1 diff; unchanged in the
  corrective pass. `RECONCILIATION` still owns the note about the test-ownership
  crossing (carried).

### MF-a — RC-9 documentation half still pending in `spec` / `api-design`

- **Severity:** Minor. **Category:** documentation consistency.
- **Evidence:** `docs/specifications/US-001-spec.md:135` (SEC-1 row) and
  `docs/designs/api/US-001-api-design.md:138` / `:174` still read
  "deny-by-default (SC-4)" without the clarifying note that this means
  *authentication-required by default* (`anyRequest().authenticated()`), not a
  literal `denyAll()`.
- **Assessment:** the **code** side of RC-9 is complete and correct — behavior
  matches `security-conventions.md` SC-4 as authoritatively worded, tests match,
  and `SecurityConfig` now documents the interpretation. The residual is a
  phrasing inconsistency in two artifacts owned by `spec-writer` and
  `openapi-designer` (`artifact-paths.yaml`) — outside this stage's only
  loop-back (`IMPLEMENTATION`). Reconciliation v2 itself split RC-9 into
  "code half → IMPLEMENTATION" + "coordinated doc note". No behavioral impact.
- **Required correction:** `spec-writer` / `openapi-designer` add the one-line
  note. If it is still unpublished when `RECONCILIATION` re-runs, RECONCILIATION
  must **not** record RC-9 as closed — it must route the doc half via its own
  `loop_back` keys `specification_gap` → `SPECIFICATION` and/or `design_gap` →
  `API_DESIGN` (those keys exist for exactly this). RC-9 is closable only when
  both the code half (done) and the spec/api-design note are in place.
- **Loop-back target:** none from this stage (`IMPLEMENTATION_VERIFICATION`'s only
  loop-back is `IMPLEMENTATION`, and the code is correct). The responsible stages
  are `SPECIFICATION` / `API_DESIGN`, reachable only from `RECONCILIATION` — which
  is why the correct move here is PASS-and-forward, not `BLOCKED`.

### MF-b — Error `message` strings differ from OpenAPI illustrative examples (carried v1 MF-2)

- **Severity:** Minor. **Category:** contract documentation.
- **Evidence:** implemented `415` / combined-`400` messages vs. the OpenAPI
  `examples`; `409` matches exactly.
- **Assessment:** `examples` are non-normative; AC-6 body shape preserved; tests
  assert status + shape. Consistent with disclosed D-4 / plan-review F-4.
- **Required correction:** none required; optional `openapi-designer` example
  alignment in a future revision.
- **Loop-back target:** none.

### MF-c — `open_decisions` v1→v2 staleness on three upstream inputs (carried v1 MF-4, reframed)

- **Severity:** Minor. **Category:** documentation lag.
- **Evidence:** `specification` v1 / `implementation_plan` v1 / `ac_test_matrix`
  v1 front matter records `open_decisions` v1; current is v2.
- **Assessment:** `open_decisions` v2 change-log = "No decision content changed";
  same six option letters; code uses the resolved values throughout;
  `open_decisions` is not an input to this stage. No impact.
- **Required correction:** none for this Story; `RECONCILIATION` to note (not
  re-open) the version references. Upstream owners may refresh front matter in a
  future revision.
- **Loop-back target:** none.

## 18. Verification Limitations

- **Semantic analysis:** IDEA MCP not invoked; architecture conclusions rest on
  import graphs and method signatures (`TEXT_FALLBACK`), not PSI call-path
  analysis. The one new cross-package reference (service → Spring DAO / Hibernate
  exception types) was checked by import inspection and the empty
  `build.gradle.kts` diff.
- **Concurrency:** the RC-3 race is verified by deterministic unit tests with an
  injected exception, not by a reproduced concurrent insert. This matches the
  reconciliation directive ("deterministic test coverage").
- **RC-3 constraint matching:** `SECURITY_REVIEW` should judge whether the
  name + cause-chain-message heuristic is complete against all H2 / Hibernate
  message shapes; the negative test covers one non-email constraint.
- **Runtime (default profile):** file-H2 boot / `ddl-auto=validate` taken from
  the test-profile context boot (same `schema.sql` + mapping under `validate`)
  plus report v2 evidence; not separately re-run.
- **Manual checks still open for humans:** diff review and PR approval
  (`HUMAN_PR_APPROVAL`); adversarial security review (`SECURITY_REVIEW`);
  final reconciliation (`RECONCILIATION`).

## 19. Verdict Rationale

Build passes (independently reproduced). All 67 tests pass with observed
evidence (independently reproduced); the +5 delta is exactly the RC-1 and RC-3
coverage. Every Acceptance Criterion AC-001..AC-007 is `VERIFIED`; the two
`PARTIALLY_RECONCILED` items from traceability v2 (AC-002 concurrent path,
AC-004 `toString()` path) are now fully covered and their prior v1 findings
(MF-3, MF-5) are closed. The four mandated corrective changes (RC-1, RC-3, RC-9
code half, RC-10) are all applied, correct, in scope, and free of unrelated
edits. Persistence, configuration, and the API contract are byte-for-byte
unchanged and remain compliant. Architecture layering holds — the new service
references are DAO/persistence exception types, not HTTP types, with no new
declared dependency. The three remaining findings are Minor: MF-a (RC-9 doc half,
owned by spec-writer / openapi-designer, tracked for RECONCILIATION), MF-b
(OpenAPI illustrative examples), MF-c (open_decisions staleness waiver). None
blocks Security Review; none originates in an upstream artifact in a way that
requires `BLOCKED`.

Verdict: **PASS** → advance to `SECURITY_REVIEW`.

```yaml
result:
  verdict: PASS
  stage: IMPLEMENTATION_VERIFICATION
  story: US-001
  artifact_status: APPROVED
  artifacts:
    - docs/verification/US-001-implementation-verification.md
  next_stage: SECURITY_REVIEW
  loop_back_stage: null
  blocking_issues: []
  non_blocking_findings:
    - "Verification v2 SUPERSEDES v1 (v1 consumed implementation_report v1 + open_decisions v1 and predates the corrective pass; invalidated by the HUMAN_PR_APPROVAL rejection 2026-09-01). Independently reproduced: ./gradlew clean build = BUILD SUCCESSFUL (exit 0); 67 tests / 0 failures / 0 errors / 0 skipped across 8 suites (was 62/7; +5)."
    - "RC-1 VERIFIED (closes v1 MF-5): RegistrationRequest.toString() masks password as password=*** (mirrors Customer.toString()); RegistrationRequestTest (3 tests) proves the submitted plaintext is never rendered, null-safe, accessor unchanged."
    - "RC-3 VERIFIED (closes v1 MF-3): CustomerService.register wraps save() in try/catch(DataIntegrityViolationException); isEmailUniquenessViolation() maps a uq_customer_email violation (Hibernate constraint name + case-insensitive cause-chain message fallback) to DuplicateEmailException -> existing 409; any other integrity violation is rethrown unchanged. CustomerServiceTest +2 (positive + isSameAs negative; negative is load-bearing). AC-002 concurrent path now RECONCILED. Placed in service (D-3, reconciliation allowed either); no HTTP type added to service; no new declared dependency (org.hibernate.exception.ConstraintViolationException is transitive via spring-boot-starter-data-jpa; build.gradle.kts diff empty)."
    - "RC-9 code half VERIFIED: SecurityConfig javadoc + one inline comment reworded 'deny-by-default' -> 'authentication-required by default (SC-4), not a literal denyAll()'; anyRequest().authenticated() unchanged; RegistrationSecurityPostureTest 4/4 green (one doc comment reworded, no assertion change)."
    - "RC-10 VERIFIED: src/main/java/org/example/customerportal/docs/ subtree (stray hooks/tool-usage.jsonl) confirmed absent; package tree now only config/controller/exception/model/repository/security/service/validation."
    - "MF-a (Minor, forwarded — NOT a loop-back from this stage): RC-9 documentation half still pending — docs/specifications/US-001-spec.md:135 (SEC-1) and docs/designs/api/US-001-api-design.md:138/:174 still say 'deny-by-default (SC-4)' without the clarifying note. Owned by spec-writer / openapi-designer. RC-9 is closable ONLY when both halves are in place; if the note is still unpublished when RECONCILIATION re-runs, RECONCILIATION must route it via its loop_back keys specification_gap -> SPECIFICATION and/or design_gap -> API_DESIGN, not mark RC-9 closed. Code side complete and SC-4-compliant; no behavioural impact. PASS-and-forward is correct here because the responsible stages are unreachable from IMPLEMENTATION_VERIFICATION (whose only loop-back is IMPLEMENTATION)."
    - "MF-b (Minor, carried v1 MF-2): implemented 400/415 error message strings differ verbatim from the OpenAPI illustrative examples; 409 matches exactly; AC-6 body shape preserved; tests assert status+shape. Optional openapi-designer example alignment; no loop-back."
    - "MF-c (Minor, carried v1 MF-4, reframed): specification v1 / implementation_plan v1 / ac_test_matrix v1 front matter reference open_decisions v1 (now v2). open_decisions v2 change-log = 'No decision content changed'; open_decisions is not an input to IMPLEMENTATION_VERIFICATION; code uses resolved values. Staleness WAIVED; RECONCILIATION to note, not re-open."
    - "Repository state: branch us-001 (v1 wrongly said main); corrective pass committed 6c7d9e8. git diff main...HEAD = 52 files incl. 3 harness-maintenance (history.jsonl, workflow-state.yaml, docs/evidence/.gitignore) + .gitignore — classification is reconciliation v2 section 15's responsibility, not changed here."
    - "Persistence, configuration, build.gradle.kts, schema.sql, application*.yaml: byte-for-byte unchanged in 7ad07e1..6c7d9e8; all v1 conclusions carry. R-1 CLOSED re-verified (OffsetDateTime <-> TIMESTAMP WITH TIME ZONE validates under ddl-auto=validate, H2 2.x / Hibernate 7.4.5)."
    - "Forwarded to SECURITY_REVIEW (mandated re-run): R-2 CSRF-scope arbitration; R-7 message-hygiene sign-off; completeness of the RC-3 constraint-name/message heuristic against crafted inputs; confirm no debug logging config surfaces a bound RegistrationRequest pre-mask; sign-off that the documented RC-9 resolution satisfies SC-4."
    - "Semantic analysis TEXT_FALLBACK (IDEA MCP not invoked); concurrency verified by deterministic unit tests with an injected exception, not a reproduced race (matches the reconciliation directive)."
```
