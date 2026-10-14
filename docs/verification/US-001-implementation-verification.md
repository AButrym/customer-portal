---
artifact_type: implementation_verification
story: US-001
version: 3
status: DRAFT
created_at: 2026-09-02T15:04:46Z
updated_at: 2026-10-14T14:54:15Z
produced_by: implementation-verifier
inputs:
  - path: docs/stories/US-001-register-customer.md
    version: null
  - path: docs/decisions/US-001-open-decisions.md
    version: 2
  - path: docs/specifications/US-001-spec.md
    version: 2
  - path: docs/reviews/specifications/US-001-spec-review.md
    version: 2
  - path: docs/impact-analysis/US-001-impact-analysis.md
    version: 2
  - path: docs/plans/US-001-implementation-plan.md
    version: 2
  - path: docs/reviews/plans/US-001-plan-review.md
    version: 2
  - path: docs/evidence/US-001-implementation-report.md
    version: 3
  - path: docs/designs/api/US-001-api-design.md
    version: 2
  - path: docs/designs/api/US-001-openapi.yaml
    version: 2
  - path: docs/designs/database/US-001-db-design.md
    version: 2
  - path: docs/designs/database/US-001-entity-model.md
    version: 2
  - path: docs/reviews/designs/US-001-design-review.md
    version: 2
  - path: docs/tests/US-001-test-strategy.md
    version: 2
  - path: docs/tests/US-001-ac-test-matrix.md
    version: 2
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

# Implementation Verification — US-001 Customer Registration (v3, re-run against the v2 input chain)

Supersedes v2 (recorded v1 upstream inputs and implementation_report v2). v1 and v2 remain in git history.

## 1. Executive Summary

**Verdict: PASS.** Independently reproduced against the v2 artifact chain and implementation_report v3.

- **Build:** `./gradlew clean test` — BUILD SUCCESSFUL, exit 0.
- **Tests:** 67 run, 0 failed, 0 errors, 0 skipped, 8 suites (counts read from `build/test-results/test/*.xml`).
- **Acceptance Criteria:** 7 of 7 (AC-001..AC-007) VERIFIED.
- **Source:** `git diff 6c7d9e8 HEAD -- src build.gradle.kts` is empty — production and test code is byte-identical to what v2 verified. Only the artifact chain was re-versioned (SC-4 wording clarification, "deny-by-default" → "authentication-required by default"), and `SecurityConfig` already carries that wording.
- **Findings:** 0 Critical, 0 Major, 3 Minor (carried, non-blocking).
- **Next:** `SECURITY_REVIEW`.

## 2. Verified Artifacts

| Artifact | Path | Version | Front-matter status |
|---|---|---|---|
| Story | docs/stories/US-001-register-customer.md | unversioned | n/a |
| Open decisions | docs/decisions/US-001-open-decisions.md | 2 | APPROVED |
| Specification | docs/specifications/US-001-spec.md | 2 | DRAFT (PASS review + HUMAN_SPEC_APPROVAL recorded; carried waiver) |
| Specification review | docs/reviews/specifications/US-001-spec-review.md | 2 | APPROVED |
| API design / OpenAPI | docs/designs/api/US-001-api-design.md, -openapi.yaml | 2 | DRAFT (carried waiver) |
| DB design / entity model | docs/designs/database/US-001-db-design.md, -entity-model.md | 2 | DRAFT (carried waiver) |
| Design review | docs/reviews/designs/US-001-design-review.md | 2 | APPROVED |
| Impact analysis | docs/impact-analysis/US-001-impact-analysis.md | 2 | DRAFT (no review stage follows) |
| Implementation plan | docs/plans/US-001-implementation-plan.md | 2 | DRAFT (PASS plan review + HUMAN_PLAN_APPROVAL occ.2) |
| Plan review | docs/reviews/plans/US-001-plan-review.md | 2 | APPROVED |
| Test strategy / AC matrix | docs/tests/US-001-test-strategy.md, -ac-test-matrix.md | 2 | DRAFT |
| Implementation report | docs/evidence/US-001-implementation-report.md | 3 | DRAFT |

No consumed input is SUPERSEDED/ARCHIVED. The implementation report's own `inputs` list the same all-v2 chain — no staleness. Open Decisions v2: no TODO/TBD/FIXME/??? markers in the specification or open_decisions.

## 3. Environment

Gradle 9.7.1 (launcher JVM 25.0.4; project toolchain Java 21), Spring Boot 4.x, H2. Profile `test`, isolated in-memory H2 (`jdbc:h2:mem:us001`); default profile uses file H2 (`./data/customer-portal`). IDEA MCP semantic tooling not used — architecture conclusions rest on import/signature inspection (`TEXT_FALLBACK`). No secrets encountered.

## 4. Repository State

Branch `us-001`. Modified: `docs/evidence/US-001-implementation-report.md` (v3), `docs/workflow/history.jsonl`, `docs/workflow/workflow-state.yaml`. No modified or untracked file under `src/` or `build.gradle.kts`. `./data/` absent and git-ignored (`/data/`). Verification added no files other than this report.

## 5. Build Evidence

`./gradlew clean test` → compileJava, compileTestJava, processResources, test all executed; BUILD SUCCESSFUL in 34s, exit 0. No compile errors or Story-relevant warnings (only a Gradle 10 deprecation notice, unrelated).

## 6. Test Evidence

| Suite | Tests | Fail/Err/Skip |
|---|---|---|
| CustomerPortalApplicationTests | 1 | 0 |
| model.request.RegistrationRequestTest | 3 | 0 |
| persistence.CustomerPersistenceTest | 3 | 0 |
| persistence.CustomerSchemaTest | 10 | 0 |
| registration.CustomerRegistrationApiTest | 22 | 0 |
| security.RegistrationSecurityPostureTest | 4 | 0 |
| service.CustomerServiceTest | 7 | 0 |
| validation.PasswordPolicyValidatorTest | 17 | 0 |
| **Total** | **67** | **0** |

Full suite run; no tests disabled or skipped. Matches implementation_report v3 (67/67).

## 7. Acceptance Criteria Matrix

| AC | Behavior | Implementation | Test evidence | Status |
|---|---|---|---|---|
| AC-001 | Valid registration → 201, role CUSTOMER, can authenticate later (persisted BCrypt hash, enabled) | `CustomerController.register`, `CustomerService.register` | `validRegistrationReturns201WithLocationAndCustomerBody`, `emailIsStoredAndReturnedNormalisedToLowercase`, `password72CharsMeetingPolicyIsAccepted`, `registrationEndpointIsReachableWithoutAuthentication`, `happyPathCreatesAnEnabledCustomerWithABcryptHash` | VERIFIED |
| AC-002 | Duplicate email rejected, no second account | `existsByEmail` pre-check + `uq_customer_email` race mapping → 409 | `duplicateEmailIsRejectedCaseInsensitivelyWith409`, `CustomerSchemaTest.emailHasAUniqueConstraint`, `caseInsensitiveDuplicateEmailCollidesOnTheUniqueConstraint`, `concurrentDuplicateEmailUniqueViolationIsMappedToDuplicateEmailException`, `anUnrelatedIntegrityViolationIsNotReportedAsADuplicateEmail` | VERIFIED |
| AC-003 | Invalid email → 400 + validation error | `@NotBlank @Email @Size(max=254)`, `GlobalExceptionHandler.handleValidation` | malformed / blank / >254 tests; `emailColumnIsVarchar254NotNull` | VERIFIED |
| AC-004 | Password not stored in plain text | `passwordEncoder.encode`; column `password_hash VARCHAR(60)`; no password column | `noPlaintextPasswordColumnExists`, `passwordHashColumnIsVarchar60NotNull`, BCrypt-pattern assertion in service test | VERIFIED |
| AC-005 | Password and hash not returned | `CustomerResponse` record = id, email, role, createdAt; `RegistrationRequest.toString()` masked | `successResponseNeverExposesCredentialOrInternalState`, `RegistrationRequestTest` (3) | VERIFIED |
| AC-006 | Password policy (12–72 bytes, 4 classes) → 400 with `password` field error | `@ValidPassword`/`PasswordPolicyValidator` + service re-check | 8 web tests incl. byte-length boundary, 17 validator tests, `serviceRechecksThePasswordPolicyBeforeHashingOrTouchingTheRepository` | VERIFIED |
| AC-007 | Non-JSON / missing Content-Type → 415 | `consumes=APPLICATION_JSON`, `handleMediaType` | `nonJsonContentTypeReturns415`, `missingContentTypeReturns415` | VERIFIED |

## 8. API Contract Verification

OpenAPI declares `POST /customers` with 201/400/409/415/500. Code: controller `@PostMapping(consumes/produces JSON)` under `/api/v1/customers`; 201 + `Location`; 400 (validation, unreadable/unknown field, service policy); 409; 415; 500 catch-all with generic message. Response body fields match `CustomerResponse` schema. No undocumented endpoint. Residual: OpenAPI illustrative-example wording (carried, MF-b).

## 9. Persistence Verification

`schema.sql` matches the entity: `customer` with `BIGINT IDENTITY` id, `email VARCHAR(254) NOT NULL` + `uq_customer_email`, `password_hash VARCHAR(60) NOT NULL`, `role` check constraint, `enabled`, UTC timestamps. `ddl-auto: validate` in both main and test config. `CustomerSchemaTest` (10) inspects the live H2 information schema; `CustomerPersistenceTest` (3) validates mapping. Default profile is file H2; test profile in-memory; `/data/` git-ignored.

## 10. Architecture Verification

Package tree (`config, controller, exception, model, repository, security, service, validation`) matches package-map. Controller imports only the service and DTO/request types (no `repository` import — grep confirmed); service owns logic and entity↔DTO mapping; entity never in a controller signature; error mapping centralised in `GlobalExceptionHandler`. No PSI call analysis (text fallback).

## 11. Validation and Error Handling

`spring-boot-starter-validation` present; `@Valid @RequestBody` active (validation tests return 400 at runtime). `fail-on-unknown-properties: true`. Error bodies are generic; password validation message does not echo submitted value (`passwordValidationMessageDoesNotEchoTheSubmittedValue`). Unmapped exceptions → generic 500.

## 12. Basic Security Readiness

BCrypt via `PasswordEncoder`; hash never in response; no logging statements in `src/main` (grep for `log.`/`logger`/`System.out` empty); `toString()` of request and entity exclude/mask secrets; H2 console disabled; `POST /api/v1/customers` the only public route, CSRF exempted only for it, `anyRequest().authenticated()`, 401 entry point. Forwarded to Security Review: CSRF exemption on the public endpoint (OD-002:B), SR-4/SR-5 H2 credential hardening.

## 13. Configuration Verification

Main config: file H2, `ddl-auto: validate`, `open-in-view: false`, console disabled, `sql.init.mode: always` for hand-maintained schema. No secrets. Dependencies in `build.gradle.kts` are the expected set (JPA, security, validation, webmvc, H2 runtime, Lombok annotation processor, test starters).

## 14. Test Quality Review

Tests map to every AC, include negative paths (400/409/415, boundary bytes, unknown-field), assert persistence constraints against the live schema, and assert absence of sensitive fields. Security posture tests run through the real filter chain. No false-positive patterns observed (no disabled tests; mocks used only for the service unit tests where the repository is the collaborator, with real-DB coverage in persistence/web suites).

## 15. Scope Verification

`src/` and `build.gradle.kts` have no uncommitted change and no diff since `6c7d9e8`. Working-tree changes are workflow artifacts only. No unrelated refactoring, no extra dependencies, no generated runtime artifacts in the tree.

## 16. Implementation Report Accuracy

Report v3 is materially consistent with observed evidence: claims of no `src/**` change and 67/67 tests verified independently.

## 17. Findings

| ID | Sev | Finding | Target |
|---|---|---|---|
| MF-a | Minor | Spec/design/entity artifacts v2 carry front-matter `DRAFT` despite recorded PASS reviews / human approval (design_review D-11, plan_review F-6). | spec-writer / openapi-designer / db-designer (no loop-back) |
| MF-b | Minor | OpenAPI illustrative example wording differs from the single `HttpMessageNotReadableException` message (plan_review F-3, RC-2/SR-2). | optional, non-blocking |
| MF-c | Minor | Spec review F-1..F-7 presentation residue open in specification v2. | spec-writer, non-blocking |

No Critical or Major findings.

## 18. Verification Limitations

- No IDEA MCP semantic/PSI analysis; layering checked by imports and signatures.
- No live-server manual exercise or IDEA diagnostics pass; evidence is Gradle build + 67 automated tests.
- The tracked-file diff base for "unchanged source" is commit `6c7d9e8`.

## 19. Verdict Rationale

Build passes, all 67 tests pass with observed evidence, every AC is VERIFIED, source is unchanged since the prior verified commit and consistent with the v2 chain, and no Critical/Major findings exist → `PASS`; advance to `SECURITY_REVIEW`.
