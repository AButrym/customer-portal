---
artifact_type: security_review
story: US-001
version: 2
status: APPROVED
created_at: 2026-09-02T15:34:00Z
updated_at: 2026-09-02T15:34:00Z
produced_by: security-reviewer
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
  - path: docs/verification/US-001-implementation-verification.md
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
  - path: docs/decisions/US-001-open-decisions.md
    version: 2
supersedes: docs/reviews/security/US-001-security-review.md
critical_findings: 0
major_findings: 0
minor_findings: 3
informational_findings: 2
security_sensitive: true
runtime_checks: PARTIAL
semantic_analysis: TEXT_FALLBACK
---

# Security Review — US-001 Customer Registration (v2, post-corrective-pass re-run)

## 1. Executive Summary

**Verdict: PASS.** The US-001 registration implementation, as amended by the
corrective pass (`implementation_report` v2, attempt 2), introduces no Critical
or Major security risk. Every security requirement in Specification §7
(SEC-1..SEC-11) is independently verifiable in code, configuration, and tests
that exercise the real `SecurityFilterChain`, and every security-sensitive Open
Decision (OD-002 CSRF, OD-003 enumeration, OD-005 anti-abuse) was resolved by a
human at `HUMAN_SPEC_APPROVAL` and is now recorded in `open_decisions` **v2**
(`status: APPROVED`, all six RESOLVED).

**Why this re-run:** the `HUMAN_PR_APPROVAL` rejection of 2026-09-01 escalated
three previously-Minor items to mandatory code changes and required
`IMPLEMENTATION_VERIFICATION` → `SECURITY_REVIEW` → `RECONCILIATION` be repeated.
Security Review **v1 is superseded** by this document (v1 consumed
`implementation_report` v1, `implementation_verification` v1, `open_decisions`
v1 and predated RC-1/RC-3/RC-9/RC-10).

**Corrective delta reviewed (all security-positive or neutral):**

- **RC-1** — `RegistrationRequest.toString()` now masks `password` (`password=***`).
  The last latent plaintext-credential rendering path is closed. **v1 finding F-1
  → CLOSED.**
- **RC-3** — `CustomerService.register` maps a `uq_customer_email` constraint
  violation (concurrent-race path) to the existing `409`; any other integrity
  violation propagates unchanged. **v1 finding F-3 → CLOSED** (residual heuristic
  note below, Minor).
- **RC-9 (code half)** — `SecurityConfig` javadoc/comment aligned to
  "authentication-required by default (SC-4) … not a literal `denyAll()`";
  `anyRequest().authenticated()` unchanged. Code side is SC-4-compliant.
- **RC-10** — stray `src/main/java/org/example/customerportal/docs/` subtree
  removed; confirmed absent.
- **v1 finding F-4 → CLOSED** — `open_decisions` v2 is published and APPROVED
  (satisfies the human's REJECT-2).

**Findings:** 0 Critical, 0 Major, 3 Minor (SR-1, SR-2, SR-3), 2 Informational
(SR-4, SR-5). None blocks progression; none requires a code change for this
Story. Security Review v1's four Minor findings resolve as: F-1 → CLOSED (RC-1),
F-3 → CLOSED (RC-3), F-4 → CLOSED (open_decisions v2); only F-2 survives, as
SR-2. SR-1 and SR-3 are new.

**Principal residual item for the next stage:** the RC-9 **documentation half**
(spec §7 SEC-1 row, api-design §6/§8) is still unpublished — those artifacts
still read "deny-by-default (SC-4)" without the clarifying note. This is Minor
and outside SECURITY_REVIEW's loop-back reach; **RECONCILIATION must not record
RC-9 as closed** until the note is published, and must route it via its own
`specification_gap` → `SPECIFICATION` / `design_gap` → `API_DESIGN` keys
(finding SR-1 below).

**Recommended next action:** advance to `RECONCILIATION`.

## 2. Reviewed Artifacts

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
| Implementation Plan | docs/plans/US-001-implementation-plan.md | 1 | APPROVED (+ HUMAN_PLAN_APPROVAL 2026-08-31T11:20:00Z) |
| Plan Review | docs/reviews/plans/US-001-plan-review.md | 1 | APPROVED (PASS) |
| Implementation Report | docs/evidence/US-001-implementation-report.md | **2** | DRAFT (corrective pass) |
| Implementation Verification | docs/verification/US-001-implementation-verification.md | **2** | see note below (verdict PASS) |
| Test Strategy | docs/tests/US-001-test-strategy.md | 1 | DRAFT |
| AC–Test Matrix | docs/tests/US-001-ac-test-matrix.md | 1 | DRAFT (authoritative AC→test map) |
| Open Decisions | docs/decisions/US-001-open-decisions.md | **2** | APPROVED (OD-001..OD-006 RESOLVED) |
| Reconciliation (loop-back source) | docs/reviews/reconciliation/US-001-reconciliation.md | 2 | CHANGES_REQUIRED (RC-1/RC-3/RC-9/RC-10) |

Front matter of the three review artifacts read directly: `specification_review`
`status: APPROVED`, `design_review` `status: APPROVED`, `plan_review`
`status: APPROVED`. `history.jsonl` records `SPEC_REVIEW` / `DESIGN_REVIEW` /
`PLAN_REVIEW` PASS and both human gates (`HUMAN_SPEC_APPROVAL`
2026-08-31T07:48:48Z, `HUMAN_PLAN_APPROVAL` 2026-08-31T11:20:00Z).

**No consumed input is `SUPERSEDED`.** `implementation_verification` v2 verdict
is **PASS** (precondition satisfied).

**Observation (not a blocker):** `implementation_verification` v2 front matter
reads `status: DRAFT` while its embedded result envelope reads
`artifact_status: APPROVED`. This mismatch mirrors the v1 verification artifact
(also DRAFT in front matter with a PASS verdict) and is the established pattern
for verification artifacts in this repository; the orchestrator already recorded
the `IMPLEMENTATION_VERIFICATION` → `SECURITY_REVIEW` transition on it
(`history.jsonl` 2026-09-02T15:04:46Z). Recorded here for the human diff
reviewer; it does not create a stale-input condition for this stage.

**Staleness note (waived, carried):** `specification` v1, `implementation_plan`
v1, `ac_test_matrix` v1 record `open_decisions` v1 in front matter while
`open_decisions` is now v2. `open_decisions` v2's change-log records *"No
decision content changed"* (same six option letters). The code always used the
resolved values; none of these three artifacts is a security-behaviour source
that changed. No blocking staleness. `RECONCILIATION` should note, not re-open,
the version references.

## 3. Security-Relevant Scope

- **Exposed functionality:** one endpoint, `POST /api/v1/customers` (public,
  unauthenticated, `application/json` only). No endpoint added or changed in the
  corrective pass.
- **Protected assets:** customer credential (plaintext password in transit /
  request binding; BCrypt hash at rest), customer email (PII), account role and
  `enabled` state, the local H2 database file.
- **Trust boundaries:** external client → `CustomerController` (`@Valid`
  binding); controller → `CustomerService` (normalization, policy re-check,
  duplicate guard, hashing, post-insert constraint mapping); service →
  `CustomerRepository` → H2; developer environment → repository (secrets /
  generated DB files).
- **Security components touched by the corrective pass:**
  `model/request/RegistrationRequest` (`toString()` override),
  `service/CustomerService` (constraint-violation catch + `isEmailUniquenessViolation`),
  `security/SecurityConfig` (comment wording only — no behavioural change).

## 4. Environment and Tools

- Spring Boot 4.1.1; Spring Security (session stack; `httpBasic` / `formLogin` /
  `logout` disabled); Hibernate ORM 7.4.5; H2 2.x; Java 21 (Gradle toolchain);
  Gradle 9.7.1.
- Active profile under test: `test` (`src/test/resources/application-test.yaml`,
  isolated in-memory H2). Default profile: file-based H2.
- Review tooling: built-in file inspection, `git`, `grep`. IDEA MCP semantic /
  build / runtime tools not invoked → `semantic_analysis: TEXT_FALLBACK`,
  `runtime_checks: PARTIAL`.
- **Build/test evidence is reused** from `implementation_verification` **v2**,
  which independently reproduced `./gradlew clean build` = **BUILD SUCCESSFUL**
  (exit 0) and **67 tests / 0 failures / 0 errors / 0 skipped** across 8 suites
  (v1 baseline 62 / 7; +5: 3 `RegistrationRequestTest`, 2 `CustomerServiceTest`).
  This review did **not** re-run the build and did **not** perform dependency
  vulnerability scanning (see §22).
- No secrets encountered or recorded.

## 5. Authentication Review

| Item | Evidence | Result |
|---|---|---|
| Story adds no authentication mechanism | no `UserDetailsService`, no `formLogin`, no `httpBasic` in `SecurityConfig` (all three explicitly `disable()`d); login is US-002 | OK |
| Registration requires no authentication (SEC-1) | `SecurityConfig` `REGISTRATION_ENDPOINT` → `permitAll()`; `RegistrationSecurityPostureTest.registrationEndpointIsReachableWithoutAuthentication` (not 401, not 403) | VERIFIED |
| Created account is a future auth subject (FR-9) | BCrypt hash verifies against the submitted password (`CustomerServiceTest.happyPathCreatesAnEnabledCustomerWithABcryptHash`, real encoder); `role = CUSTOMER`, `enabled = true` | VERIFIED |
| Protected routes deny unauthenticated access | `anyRequest().authenticated()`; `HttpStatusEntryPoint(401)`; `RegistrationSecurityPostureTest.protectedRouteReturns401WhenUnauthenticated` (401, not a 302 redirect) | VERIFIED |

No findings.

## 6. Authorization Review

| Item | Evidence | Result |
|---|---|---|
| SC-4 satisfied (SEC-1) | `authorizeHttpRequests` = one exact-match `permitAll` matcher + `anyRequest().authenticated()`. SC-4's own text ("every endpoint requires authentication unless the approved API design lists it as public") is exactly what `anyRequest().authenticated()` enforces. **RC-9 code half VERIFIED.** | VERIFIED |
| Public scope is minimal | `REGISTRATION_ENDPOINT` matches **exactly** method `POST` + URI `/api/v1/customers`; any other method or path on the same URI falls through to `authenticated()` | VERIFIED |
| No role / ownership operation introduced | US-001 adds no read/update/delete endpoint; no `@PreAuthorize`; nothing to bypass. OD-005:A scope respected (no `GET /{id}`) | N/A (in scope) |
| Service cannot be reached around authorization | `CustomerService.register` is called only by `CustomerController.register`; that path is the `permitAll` route by design | VERIFIED (text/import analysis; see §22) |

**Finding SR-1** (Minor, AUTHORIZATION / documentation consistency) — the RC-9
**documentation half** is unpublished. See §19.

## 7. Password and Credential Handling

| Requirement | Evidence | Result |
|---|---|---|
| Plaintext only on inbound DTO (SEC-3, SC-1) | `RegistrationRequest.password`; in `CustomerService` it flows only to `PasswordPolicyValidator.isCompliant` and `passwordEncoder.encode`; never copied to `Customer`, `CustomerResponse`, or any exception | VERIFIED |
| **Plaintext not renderable via `toString()`** (SEC-3) | **RC-1 CLOSED:** `RegistrationRequest.toString()` is hand-overridden to `"RegistrationRequest{email='…', password=***}"`, mirroring `Customer.toString()`. `RegistrationRequestTest` (3 tests): distinctive-secret literal is absent and `password=***` present; null-safe; value-independent; `password()` accessor unchanged. | VERIFIED (v1 F-1 CLOSED) |
| Never persisted (AC-004, FR-7) | `schema.sql` has no plaintext column; `Customer` has only `passwordHash`; `CustomerSchemaTest.noPlaintextPasswordColumnExists` | VERIFIED |
| Never logged (SEC-3, SC-9) | `grep -nE "(Logger|LoggerFactory|System\.out|System\.err|println|slf4j|@Slf4j|log\.(info\|debug\|warn\|error\|trace))"` over `src/main` → **no matches**; no `logging.*` / `spring.jpa.show-sql` in either properties file; `GlobalExceptionHandler` reads only `HttpServletRequest.getRequestURI()` + `BindingResult.getFieldErrors()`, never the bound DTO | VERIFIED |
| Never returned (AC-005, SEC-4) | `CustomerResponse` = `id, email, role, createdAt` only; `CustomerRegistrationApiTest.successResponseNeverExposesCredentialOrInternalState` asserts `$.password`, `$.passwordHash`, `$.password_hash`, `$.enabled`, `$.updatedAt` all absent | VERIFIED |
| BCrypt, no no-op encoder (SEC-2, NFR-1) | `SecurityConfig.passwordEncoder()` = `new BCryptPasswordEncoder()` (default strength), bean in `security` package; `CustomerServiceTest` asserts a real `^\$2[aby]\$\d\d\$.{53}$` hash that verifies and `!= raw` | VERIFIED |
| Policy enforced request-layer **and** service re-check (FR-6, SC-1) | `@ValidPassword` → `PasswordPolicyValidator.isValid` at binding; `CustomerService.register` calls `PasswordPolicyValidator.isCompliant` before `encode` (and before `existsByEmail` — `serviceRechecksThePasswordPolicyBeforeHashingOrTouchingTheRepository`) | VERIFIED |
| Policy matches SC-1 exactly | 12..72 **bytes** (UTF-8 — BCrypt input bound) + one upper / lower / digit / special; `PasswordPolicyValidatorTest` (17 cases incl. 11/12/72/73-byte + multi-byte) | VERIFIED |
| Validation message never echoes the value (SC-9, R-7) | `@ValidPassword` message is the fixed string `"Password does not meet the security policy."`; `InvalidPasswordException` → fixed `"The submitted password does not meet the security policy."`; `PasswordPolicyValidatorTest.defaultMessageNeverEchoesASubmittedValue`, `CustomerRegistrationApiTest.passwordValidationMessageDoesNotEchoTheSubmittedValue` | VERIFIED (R-7 signed off — §16) |
| Test fixtures introduce no real credentials | passwords in tests are synthetic policy strings (`Aa1!aaaaaaaa`, `Aa1!s3cr3t-plaintext`); BCrypt literals are obvious placeholders | VERIFIED |

No findings. (v1 F-1 closed.)

## 8. Sensitive Data Exposure

| Surface | Review | Result |
|---|---|---|
| Response DTO | `CustomerResponse` minimal; no hash, no `enabled`, no `updatedAt` | OK |
| Entity serialization | `Customer` never on a controller signature (AD-4); not a Jackson type on any endpoint | OK |
| Exception responses | `ErrorResponse` = `timestamp, status, error, message, path, fieldErrors[]`; `message` is one fixed client-safe string per branch; `fieldErrors[]` carries only `field` + the static constraint message | OK |
| `toString()` of the request record | **RC-1 CLOSED** — masked (§7) | OK |
| Logs / debug output | none — no logger in `src/main`; no debug logging config | OK |
| Implementation report / verification / telemetry | contain no secret; `docs/hooks/tool-usage.jsonl` is git-ignored | OK |

No findings.

## 9. Input Validation

| Item | Evidence | Result |
|---|---|---|
| Server-side, no framework-default reliance (NFR-2) | explicit `@NotBlank @Email @Size(max=254)` on `email`; explicit `@NotBlank @ValidPassword` + custom validator on `password` | VERIFIED |
| Runtime activation | `@Valid @RequestBody` on `CustomerController.register` → `MethodArgumentNotValidException` → `handleValidation` → `400` + `fieldErrors[]`; proven by the real-MVC web tests | VERIFIED |
| Length bounds explicit | email `@Size(max=254)` + `VARCHAR(254)`; password 12..72 bytes | VERIFIED |
| Required fields enforced | `@NotBlank` on both; the service `isCompliant` gate also treats null/empty as non-compliant | VERIFIED |
| Unknown / extra JSON fields | `spring.jackson.deserialization.fail-on-unknown-properties=true` (both profiles) → `HttpMessageNotReadableException` → `400`; `unknownJsonPropertyReturns400` | VERIFIED |
| Mass assignment (role / enabled injection) | only `email` + `password` are record components; any other property → `400`. `role` / `enabled` set server-side in `CustomerService` only | VERIFIED |
| Malformed JSON | `400` via the same handler; `malformedJsonReturns400` | VERIFIED |
| Errors reveal no internals | `errorBodyNeverLeaksInternals` | VERIFIED |

No findings.

## 10. API Security

| Item | Evidence | Result |
|---|---|---|
| Only the approved endpoint exists | one `@PostMapping` on `/api/v1/customers`; no other controller; corrective pass added none | VERIFIED |
| Method + content type constrained | `consumes = APPLICATION_JSON_VALUE`; missing/other `Content-Type` → `415` (`nonJsonContentTypeReturns415`, `missingContentTypeReturns415`) | VERIFIED |
| Request fields restricted | `{email, password}` only; `additionalProperties:false` enforced at runtime | VERIFIED |
| Response fields minimized | `CustomerResponse` = OD-004:A field set | VERIFIED |
| `201` + `Location` | `ResponseEntity.created(location)`; `Location: /api/v1/customers/{id}` | VERIFIED |
| `409` path (RC-3) | the concurrent-race `DataIntegrityViolationException` is routed into the **same** `DuplicateEmailException` → `GlobalExceptionHandler.handleDuplicateEmail` → `409` + `"An account with this email already exists."` (matches the OpenAPI `409` example verbatim). No new status code, no new response shape. | VERIFIED |
| Error responses match AC-6 shape, no leak | one `@RestControllerAdvice`, one branch per status; `errorBodyHasTheApiConventionShape` | VERIFIED |
| Auth declaration matches implementation | OpenAPI `security: []` / `x-public: true` for this path ↔ `permitAll` matcher | VERIFIED |

**Finding SR-2** (Minor, API_SECURITY / documentation) — implemented `400`/`415`
`message` strings differ verbatim from the OpenAPI *illustrative* `examples`
(`409` matches exactly; all tests assert status + body shape). Carried from v1
F-2 / verification MF-b. See §19.

## 11. Persistence Security

| Item | Evidence | Result |
|---|---|---|
| No plaintext password column | `schema.sql`; `CustomerSchemaTest.noPlaintextPasswordColumnExists` | VERIFIED |
| `password_hash VARCHAR(60) NOT NULL` (PC-9) | `schema.sql` + `@Column(length=60, nullable=false)`; `passwordHashColumnIsVarchar60NotNull` | VERIFIED |
| `email VARCHAR(254) NOT NULL`, `uq_customer_email` UNIQUE | `schema.sql` + entity `@UniqueConstraint`; `emailColumnIsVarchar254NotNull`, `emailHasAUniqueConstraint` | VERIFIED |
| Case-insensitive uniqueness (BR-001/BR-002, OD-006:A) | `CustomerService.normalizeEmail` (`trim().toLowerCase(ROOT)`) before check **and** save + plain UNIQUE; `duplicateEmailIsRejectedCaseInsensitivelyWith409` | VERIFIED |
| **Concurrent duplicate → `409`, not `500`** | **RC-3 CLOSED:** `CustomerService.register` wraps `save` in `try/catch (DataIntegrityViolationException)`; `isEmailUniquenessViolation(...)` maps a `uq_customer_email` violation to `DuplicateEmailException`; any other integrity violation is rethrown. `CustomerServiceTest` +2 (positive; `isSameAs` negative — load-bearing). The `uq_customer_email` constraint always prevented the duplicate row; this upgrades the response quality. | VERIFIED (v1 F-3 CLOSED; residual note SR-3) |
| `role` constrained | `EnumType.STRING` + `ck_customer_role CHECK (role IN ('CUSTOMER','ADMIN'))` | VERIFIED |
| Audit timestamps UTC, `created_at` immutable | `JpaAuditingConfig` UTC `DateTimeProvider`; `created_at updatable=false`; `CustomerPersistenceTest` | VERIFIED |
| Generated DB files git-ignored | `.gitignore` `/data/`; not tracked, not in tree | VERIFIED |
| `ddl-auto` = `validate` both profiles (SEC-10, SC-8) | `application.yaml`, `application-test.yaml` | VERIFIED |
| No HTTP type leaked into the service by RC-3 | catch uses `org.springframework.dao.DataIntegrityViolationException` + `org.hibernate.exception.ConstraintViolationException` — persistence/DAO types, not `org.springframework.http` / servlet types; domain `DuplicateEmailException` carries no HTTP concern; `build.gradle.kts` diff `7ad07e1..6c7d9e8` empty (no new declared dependency) | VERIFIED |

**Finding SR-3** (Minor, PERSISTENCE / robustness) — the `isEmailUniquenessViolation`
name+message heuristic. See §19.

## 12. H2 and Application Configuration

| Item | Value / Evidence | Result |
|---|---|---|
| H2 console (SC-6, SEC-9) | `spring.h2.console.enabled=false` in `application.yaml` **and** `application-test.yaml`; `RegistrationSecurityPostureTest.h2ConsoleIsNotExposed`; no `/h2-console` permit rule | VERIFIED |
| H2 mode | file-based default (`jdbc:h2:file:./data/customer-portal;AUTO_SERVER=TRUE`), isolated in-memory for tests | matches DB design §8 |
| `ddl-auto` | `validate` (both) | VERIFIED |
| `spring.sql.init.mode` | `always` (default) / `embedded` (test) | matches DB design §8 |
| Datasource credentials | `username: sa`, `password: ""` (H2 default, local file DB) | SR-5 (Informational) |
| `AUTO_SERVER=TRUE` | present in the **approved** DB design §8, plan M-2, impact analysis — approved configuration | SR-4 (Informational) |
| Unsafe defaults becoming runtime defaults | test-only settings isolated in `application-test.yaml`; no profile leakage | OK |
| Corrective pass config changes | none (`build.gradle.kts`, `application*.yaml`, `schema.sql`, `.gitignore` unchanged in `7ad07e1..6c7d9e8`) | OK |

Findings **SR-4**, **SR-5** (both Informational) — see §19.

## 13. Logging and Telemetry

- **Application logging:** none added, none present. `grep` over `src/main`
  finds no logger, `System.out`/`System.err`, `println`, or `@Slf4j`. No
  `logging.level.*`, `spring.jpa.show-sql`, or Hibernate SQL logging in either
  properties file.
- **Exception logging:** `GlobalExceptionHandler` does not log; it never reads
  the bound DTO.
- **Debug-logging risk for a bound `RegistrationRequest` (forwarded item d):**
  even if a future `logging.level` / framework debug config were added, RC-1's
  masking `toString()` now prevents the plaintext from being rendered. No
  reachable pre-mask path exists today. **Signed off.**
- **Tool-usage telemetry:** `docs/hooks/tool-usage.jsonl` is git-ignored; this
  Story does not modify hook configuration. The stray copy that had been
  misplaced under `src/main/java/...` (RC-10) is removed. Payload content not
  audited (out of Story scope); AGENTS.md / SC-9 state it is metadata-only by
  policy. The hook output-path fix remains a finding for the human (D-2, carried).

No findings.

## 14. Dependencies

| Dependency | Status |
|---|---|
| `spring-boot-starter-validation` | approved — plan M-1 |
| `spring-boot-starter-security`, `-data-jpa`, `-webmvc`, `h2`, `lombok` | pre-existing, unchanged |
| Test: `-security-test`, `-data-jpa-test`, `-webmvc-test`, `junit-platform-launcher` | test scope only; not on the runtime classpath |
| `org.hibernate.exception.ConstraintViolationException` (RC-3) | **not a new dependency** — compile-time reference to a class already transitive via `spring-boot-starter-data-jpa`; `build.gradle.kts` diff `7ad07e1..6c7d9e8` is empty |

No unapproved dependency. All versions managed by the Spring Boot BOM 4.1.1.
**Vulnerability database scanning was not performed** — no claim is made about
known-CVE status of the resolved dependency tree (§22).

## 15. Security Test Coverage

| Security requirement / abuse case | Test(s) | Status |
|---|---|---|
| SEC-2 BCrypt hash before persistence | `CustomerServiceTest.happyPathCreatesAnEnabledCustomerWithABcryptHash` (real encoder) | COVERED |
| SEC-3 plaintext not rendered by `toString()` (RC-1) | `RegistrationRequestTest` (3 tests) | COVERED (new) |
| AC-004 no plaintext column / stored | `CustomerSchemaTest.noPlaintextPasswordColumnExists`, `.passwordHashColumnIsVarchar60NotNull` | COVERED |
| AC-005 / SEC-3/SEC-4 hash + internal state absent from response | `CustomerRegistrationApiTest.successResponseNeverExposesCredentialOrInternalState` | COVERED |
| AC-006 invalid password rejected pre-persistence | `CustomerRegistrationApiTest` (8 vectors) + `CustomerServiceTest.serviceRechecksThePasswordPolicyBeforeHashingOrTouchingTheRepository` | COVERED |
| AC-003 invalid email rejected | `CustomerRegistrationApiTest` (malformed / blank / >254) | COVERED |
| AC-002 / SEC-8 duplicate email (any case) → OD-003:A `409` — single-request | `CustomerRegistrationApiTest.duplicateEmailIsRejectedCaseInsensitivelyWith409`; `CustomerServiceTest` (same-case + different-case, `save` never called) | COVERED |
| AC-002 concurrent duplicate → `409` (RC-3) | `CustomerServiceTest.concurrentDuplicateEmailUniqueViolationIsMappedToDuplicateEmailException`, `.anUnrelatedIntegrityViolationIsNotReportedAsADuplicateEmail` (`isSameAs` negative — load-bearing) | COVERED (new, deterministic) |
| Mass assignment (unknown field) | `CustomerRegistrationApiTest.unknownJsonPropertyReturns400` | COVERED |
| SEC-9 validation message never echoes value | `PasswordPolicyValidatorTest.defaultMessageNeverEchoesASubmittedValue`, `CustomerRegistrationApiTest.passwordValidationMessageDoesNotEchoTheSubmittedValue` | COVERED |
| SEC-1 registration public / other routes authentication-required | `RegistrationSecurityPostureTest` (reachable w/o auth; protected route → 401) | COVERED |
| SEC-7 CSRF exemption scoped to the registration POST | `RegistrationSecurityPostureTest.registrationPostIsAcceptedWithoutACsrfToken` | COVERED (config-verified for "everywhere else" — §16) |
| SEC-6/SEC-9 H2 console not exposed | `RegistrationSecurityPostureTest.h2ConsoleIsNotExposed` | COVERED |
| SEC-6 error body leaks no internals | `CustomerRegistrationApiTest.errorBodyNeverLeaksInternals` | COVERED |

Test quality: security tests use the real `SecurityFilterChain`
(`@SpringBootTest` + `@AutoConfigureMockMvc`), not a stubbed `@WebMvcTest`;
persistence tests hit H2 `INFORMATION_SCHEMA`; service tests use a real
`BCryptPasswordEncoder`. The two new RC-3 tests are deterministic (injected
exception, no reliance on a real DB race) — this matches the reconciliation
directive. No test mocks away the property it asserts; no test was weakened,
disabled, or relaxed in the corrective pass (`git diff 7ad07e1..6c7d9e8 --
src/test/` = additions + one reworded comment).

## 16. Abuse Case Review

| Scenario | Expected protection | Evidence | Status |
|---|---|---|---|
| Submit `role` / `enabled` in the JSON to self-escalate | field rejected; server sets role | `fail-on-unknown-properties=true` → `400`; `unknownJsonPropertyReturns400` | PROTECTED |
| Repeated duplicate registrations (single-request) | `409`, no second account | AC-002 tests | PROTECTED |
| **Concurrent duplicate registrations (race)** | `409` (was `500`), no second account, `uq_customer_email` blocks the row | RC-3; `CustomerServiceTest` +2 | PROTECTED (RC-3) |
| Oversized email / password | `400` | `emailLongerThan254CharsReturns400…`, `passwordOver72BytesButUnder72CharsReturns400…` | PROTECTED |
| Malformed / non-JSON body | `400` / `415` | `malformedJsonReturns400`, `nonJsonContentTypeReturns415` | PROTECTED |
| Weak / non-compliant password | `400`, no account, no hash computed | 8 password vectors + service re-check | PROTECTED |
| Inspect success response for credentials | none present | `successResponseNeverExposesCredentialOrInternalState` | PROTECTED |
| **Crafted email value induces RC-3 misclassification** | a non-uniqueness integrity error is *not* mapped to `409` | negative test (`CK_CUSTOMER_ROLE`); reachability analysis (§19 SR-3) | PROTECTED (residual Minor note) |
| Account enumeration via the `409` message | accepted risk (OD-003:A / SEC-8) | human-approved decision | ACCEPTED RISK (not a finding) |
| CSRF forgery against a state-changing endpoint | CSRF enabled except the one public matcher | **R-2 sign-off below** | PROTECTED |
| High-volume automated signups (DoS / spam) | out of scope (OD-005:A) | no NFR/AC requires rate limiting | OUT OF SCOPE (follow-up recommended) |
| Reach the H2 TCP server started by `AUTO_SERVER` | blank `sa` password on a local file DB | SR-4 | INFORMATIONAL (approved config; local dev only) |

**R-2 — CSRF-scope / posture arbitration (forwarded from planning F-3 and
verification):** signed off. Basis:

- `SecurityConfig.csrf(csrf -> csrf.ignoringRequestMatchers(REGISTRATION_ENDPOINT))`
  leaves CSRF at its framework default (enabled) for every request that is not
  the exact `POST /api/v1/customers` match. The **same** exact-match
  `RequestMatcher` instance drives both `permitAll` and the CSRF exemption, so
  the exemption cannot be broader than the public route.
- The exemption is the recorded SC-5 architecture decision (OD-002:B, api-design
  §6).
- Unauthenticated access to a protected route returns `401`
  (`HttpStatusEntryPoint`), not a form-login `302` — the JSON-API posture the
  plan recommended. `formLogin` / `httpBasic` / `logout` are explicitly disabled.
- **Limitation:** "CSRF still enforced for every other writable endpoint" cannot
  be asserted by a test — US-001 introduces no second writable endpoint
  (`RegistrationSecurityPostureTest` says so in its own javadoc). The sign-off
  rests on the configuration above, not on test coverage. Recorded in §22.

**R-7 — message hygiene (forwarded):** signed off. Every error `message` is a
fixed generic string built in `GlobalExceptionHandler` / the `@ValidPassword`
constraint; none interpolates a submitted value; `fieldErrors[].message` is the
static constraint message only. Tested by `defaultMessageNeverEchoesASubmittedValue`
and `passwordValidationMessageDoesNotEchoTheSubmittedValue`.

## 17. Repository Hygiene

- **Working tree:** `git status --short` → **clean**. The corrective pass is
  committed (`6c7d9e8`).
- **Secret-like files:** none tracked or untracked in scope. `application.yaml`
  `password: ""` is the H2 default for a local file DB, not a real secret (SR-5).
- **Generated H2 files:** `/data/` git-ignored; not present in the working tree.
- **Stray source subtree (RC-10):** `src/main/java/org/example/customerportal/docs/`
  confirmed absent; the `customerportal` package tree is now only
  `config / controller / exception / model / repository / security / service / validation`.
- **`git diff main...HEAD`:** 52 files — the full US-001 story change set plus
  harness-maintenance (`.gitignore` +4 lines, `docs/evidence/.gitignore`,
  `docs/workflow/history.jsonl`, `docs/workflow/workflow-state.yaml`). The
  `.gitignore` additions (`/docs/hooks/tool-usage.jsonl`,
  `/docs/harness-consistency-review.md`) are harness scaffolding, not
  security-relevant, and are RECONCILIATION §15's classification responsibility —
  not changed or removed here.
- No secret value is reproduced in this report.

## 18. Deviations

| Deviation | Security assessment |
|---|---|
| RC-3 mapping placed in `CustomerService`, not `GlobalExceptionHandler` (report D-3) | Reconciliation allowed either. Benign — reuses the existing `DuplicateEmailException` → `409` branch; no HTTP type in the service; deterministically testable. |
| RC-3 constraint scoping is name + message-token based (report D-4) | See SR-3. Match token is the literal constraint identifier `uq_customer_email`, not email-shaped text. Minor robustness note; no security impact. |
| RC-9 documentation half unpublished (report D-1) | See SR-1. Minor documentation-consistency; code side is SC-4-compliant. |
| RC-10 hook output-path root cause unfixed (report D-2) | Hook configuration, outside implementation scope. Finding for the human. Stray file itself is removed. |
| Implemented error `message` strings differ from OpenAPI examples (SR-2) | Illustrative examples only; AC-6 shape preserved; implemented messages are *more* generic — no additional disclosure. |

No undisclosed security-relevant deviation found.

## 19. Findings

### SR-1 — RC-9 documentation half unpublished in `spec` / `api-design`

- **Severity:** Minor. **Category:** AUTHORIZATION / documentation consistency.
- **Affected:** `docs/specifications/US-001-spec.md:135` (SEC-1 row),
  `docs/designs/api/US-001-api-design.md:138` and `:174`.
- **Observed:** all three still read "deny-by-default (SC-4)" without the
  clarifying note that this means *authentication-required by default*
  (`anyRequest().authenticated()`), not a literal `denyAll()`. The
  `SecurityConfig` code comment (RC-9 code half) has been aligned; these two
  artifacts have not.
- **Expected:** reconciliation v2 (§78) and implementation_verification v2
  (MF-a) both classified RC-9 as *code half + coordinated doc note*, and state
  RC-9 is **closable only with both halves in place**.
- **Security assessment:** the **code** is SC-4-compliant —
  `security-conventions.md` SC-4's own wording is "every endpoint requires
  authentication unless the approved API design lists it as public", which is
  exactly `anyRequest().authenticated()`. There is **no security risk** and no
  behavioural gap. This is a documentation-consistency residual only.
- **Required correction:** `spec-writer` / `openapi-designer` add the one-line
  note. **This is not a SECURITY_REVIEW loop-back** — `SECURITY_REVIEW.loop_back`
  reaches only `IMPLEMENTATION` (code is correct) and `API_DESIGN` via
  `invalid_security_design` (reserved for an *unsafe* design — a bare phrasing is
  not unsafe). The responsible stages (`SPECIFICATION`, `API_DESIGN`) are
  reachable only from `RECONCILIATION`.
- **Instruction to RECONCILIATION:** do **not** record RC-9 as closed while the
  note is unpublished; route it via `specification_gap` → `SPECIFICATION` and/or
  `design_gap` → `API_DESIGN`.
- **Loop-back target (this stage):** none — PASS-and-forward.

### SR-2 — Error `message` strings differ from OpenAPI illustrative examples

- **Severity:** Minor. **Category:** API_SECURITY / documentation.
- **Affected:** `exception/GlobalExceptionHandler.java`,
  `docs/designs/api/US-001-openapi.yaml`.
- **Observed:** implemented `415` message `"Content-Type must be
  application/json."` and one combined `400` message vs. the contract's
  illustrative `examples`. The `409` message matches exactly.
- **Security assessment:** `examples` are non-normative; AC-6 body **shape** is
  fixed and preserved; the implemented messages are *more* generic, so no extra
  information is disclosed.
- **Required correction:** none. Optional `openapi-designer` example alignment.
- **Loop-back target:** none. Carried from v1 F-2 / verification MF-b.

### SR-3 — `isEmailUniquenessViolation` name + message-token heuristic

- **Severity:** Minor. **Category:** PERSISTENCE / ERROR_HANDLING (robustness).
- **Affected:** `service/CustomerService.java:89-104`.
- **Observed:** the method returns `true` if any cause in the chain is a
  Hibernate `ConstraintViolationException` whose `getConstraintName()` contains
  `uq_customer_email` (case-insensitive), or — fallback — if any cause's
  `getMessage()` contains the substring `uq_customer_email` (case-insensitive).
- **Could a crafted email induce a false positive (map an unrelated integrity
  error to `409`)?** For that, `save()` must throw a
  `DataIntegrityViolationException` for a **non-uniqueness** constraint whose
  message *also* contains the literal token `uq_customer_email`. The remaining
  constraints on `customer` are `pk_customer` (id — server-generated identity),
  `ck_customer_role` (role — server-set to `CUSTOMER`), and the `NOT NULL`
  columns (all server-populated). None of these can be tripped by user-supplied
  email content, and their H2 messages name the failing constraint, not the row
  email. The match token is a fixed constraint identifier, not email-shaped
  text, so an email value like `uq_customer_email@x.com` does not by itself
  trigger the match — it would still need an unrelated violation whose message
  quotes it. **Practically unreachable.**
- **Impact ceiling if it ever misfired:** a genuine integrity error surfaces as
  `409` instead of `500`. No data exposure, no authorization effect, no
  enumeration effect beyond the accepted OD-003:A.
- **Required correction:** none for US-001. Optional hardening: match the
  constraint name only (drop the message fallback) once a Hibernate/H2 version
  with a reliable `getConstraintName()` is confirmed, or match a more specific
  message pattern.
- **Loop-back target:** none. (v1 F-3 is CLOSED by RC-3; this is the residual
  note the verifier forwarded.)

### SR-4 — `AUTO_SERVER=TRUE` starts an H2 TCP listener guarded by a blank `sa` password

- **Severity:** Informational. **Category:** CONFIGURATION.
- **Affected:** `src/main/resources/application.yaml`.
- **Observed:** default-profile URL `jdbc:h2:file:./data/customer-portal;AUTO_SERVER=TRUE`,
  `username: sa`, `password: ""`. `AUTO_SERVER` starts an H2 automatic
  mixed-mode server; the account has no password.
- **Provenance:** this exact URL is in the **approved** DB design §8, the
  **approved** plan M-2, and the impact analysis. The test profile uses isolated
  in-memory H2 with no server.
- **Risk:** low and accepted by the approved design for a local training
  project; training data only; not exposed via the public API. It is nonetheless
  a blank-credential local network listener.
- **Required correction:** none. Recommendation: a future hardening Story drops
  `AUTO_SERVER` or binds it to loopback and externalizes an H2 password.
- **Loop-back target:** none.

### SR-5 — Empty datasource password committed in `application.yaml`

- **Severity:** Informational. **Category:** SECRET_MANAGEMENT.
- **Affected:** `src/main/resources/application.yaml`.
- **Observed:** `spring.datasource.password: ""`, `username: sa` checked in.
- **Assessment:** an empty string is the H2 default, not a secret, so SC-7 is
  not breached. The inline-credential pattern is worth noting before a real
  database is introduced.
- **Required correction:** none for US-001. Externalize when a real datasource
  is added.
- **Loop-back target:** none.

## 20. Positive Controls (independently observed)

1. **BCrypt, no no-op encoder** — `new BCryptPasswordEncoder()` in the `security`
   package; a real `$2[aby]$` verifying hash asserted with the real encoder.
2. **Plaintext password confined to the request DTO** — traced through
   `CustomerService`: used only for `isCompliant` and `encode`; **and its
   `toString()` is now masked (RC-1)**, closing the last latent rendering path.
3. **Zero logging in production code** — `grep` over `src/main` returns nothing;
   no SQL/debug logging config. Credentials cannot reach a log via US-001 paths.
4. **Response DTO isolation** — `CustomerResponse` = `id, email, role, createdAt`;
   positively-asserted absence of `password`/`passwordHash`/`enabled`/`updatedAt`.
5. **SC-4 authorization** — `anyRequest().authenticated()` with a single exact
   `POST /api/v1/customers` `permitAll` matcher; protected route returns `401`
   (verified, not a redirect).
6. **CSRF exemption minimally scoped** — the *same* single `RequestMatcher`
   drives `permitAll` and `csrf.ignoringRequestMatchers`; CSRF otherwise
   default-enabled (OD-002:B).
7. **Concurrent-duplicate integrity** — `uq_customer_email` blocks the second
   row; RC-3 maps the violation to `409` with constraint scoping that does not
   swallow unrelated integrity errors (load-bearing negative test).
8. **H2 console disabled in every profile** — `enabled: false` in both
   properties files; `GET /h2-console` asserted non-200; no permit rule.
9. **`ddl-auto=validate` in every profile** — hand-written `schema.sql`; entity
   mapping validated at boot (SC-8).
10. **Mass-assignment closed** — `fail-on-unknown-properties=true`; only
    `email`/`password` bindable; `role`/`enabled` server-side only.
11. **Error hygiene** — one `@RestControllerAdvice`, one static client-safe
    message per status, `500` fallback leaks nothing; `errorBodyNeverLeaksInternals`.
12. **Password policy = SC-1 exactly**, enforced twice (request constraint +
    service re-check), byte-measured for the BCrypt bound; static non-echoing
    message.

## 21. Open Decisions

All six US-001 Open Decisions are RESOLVED and recorded in `open_decisions`
**v2** (`status: APPROVED`): OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A
OD-006:A, resolved by a human at `HUMAN_SPEC_APPROVAL` (2026-08-31T07:48:48Z).
The security-sensitive ones — OD-002 (CSRF: exempt the registration POST only),
OD-003 (duplicate-email: explicit `409`, enumeration exposure accepted per
SEC-8), OD-005 (anti-abuse: out of scope) — are all resolved and correctly
implemented.

**v1 finding F-4 (stale `open_decisions` v1) is CLOSED** — v2 is published and
APPROVED, satisfying the `HUMAN_PR_APPROVAL` REJECT-2 requirement that a
non-stale Open Decisions artifact reach the PR.

**No blocking security Open Decisions were identified.**

## 22. Review Limitations

- **Build/test not re-run in this stage.** Evidence (`./gradlew clean build`
  BUILD SUCCESSFUL; 67/67) is reused from `implementation_verification` **v2**,
  which independently reproduced it. Per this Skill's tooling strategy, reusing
  verification evidence is expected; it is declared here rather than
  re-executed.
- **`runtime_checks: PARTIAL`** — no application boot, no live HTTP probing, no
  live H2/TCP reachability test this stage. Posture conclusions rest on the
  security tests (real filter chain) plus code/config inspection.
- **`semantic_analysis: TEXT_FALLBACK`** — IDEA MCP not invoked.
  Authorization / call-path conclusions rest on import graphs and method
  signatures, not PSI call analysis. Layering is unambiguous from imports here.
- **R-2 "CSRF enforced for every other writable endpoint"** is verified from
  configuration only — US-001 adds no second writable endpoint to assert it
  against (see §16).
- **RC-3 constraint matching (SR-3)** — completeness against every possible
  H2 / Hibernate message shape is argued from the constraint inventory, not
  exhaustively fuzzed. The negative test covers one non-email constraint.
- **No dependency vulnerability scanning.** No CVE database consulted; no claim
  about known vulnerabilities in the resolved dependency tree. An approved
  scanner should run if organizational policy requires it.
- **`implementation_verification` v2 front-matter `status: DRAFT` vs. envelope
  `artifact_status: APPROVED`** mismatch noted in §2 — observation for the human,
  not treated as a stale-input blocker.
- Human diff review and `HUMAN_PR_APPROVAL` remain outstanding by design.

## 23. Verdict Rationale

`implementation_verification` v2 verdict is PASS (precondition met).
`specification_review`, `design_review`, `plan_review` are all APPROVED; both
human gates are recorded; no consumed input is `SUPERSEDED`. The four mandated
corrective changes (RC-1, RC-3, RC-9 code half, RC-10) are all applied,
correct, in scope, and free of unrelated edits — and all are security-positive
or neutral: RC-1 closes v1 finding F-1, RC-3 closes v1 finding F-3, RC-9 aligns
the code comment to SC-4 without changing behaviour, RC-10 removes a stray file.
`open_decisions` v2 closes v1 finding F-4. Every security requirement
SEC-1..SEC-11 is independently verifiable in code, configuration, and executable
tests that exercise the real security filter chain. All security-sensitive Open
Decisions were resolved by a human and are correctly implemented. Mass
assignment, plaintext exposure (including `toString()`), console exposure,
schema-destruction, and authorization-bypass vectors are all closed. The
forwarded arbitration items (R-2 CSRF scope, R-7 message hygiene, RC-3 heuristic
completeness, debug-logging pre-mask risk, RC-9 SC-4 sign-off) are all signed
off in §16 / §13 / §6.

The three Minor findings are documentation-consistency (SR-1, SR-2) and
robustness (SR-3) items with no reachable exploit path; the two Informational
items (SR-4, SR-5) concern approved local-dev configuration. There is no
Critical or Major finding, so no `CHANGES_REQUIRED` loop-back is warranted; no
mandatory security requirement is undefined and no human security decision is
pending, so no `BLOCKED` condition applies. SR-1 (the RC-9 documentation half)
is real and must be tracked, but its owner stages are unreachable from
`SECURITY_REVIEW` — PASS-and-forward with an explicit instruction to
`RECONCILIATION` is the correct disposition.

**Verdict: PASS** → advance to `RECONCILIATION`.

```yaml
result:
  verdict: PASS
  stage: SECURITY_REVIEW
  story: US-001
  artifact_status: APPROVED
  artifacts:
    - docs/reviews/security/US-001-security-review.md
  next_stage: RECONCILIATION
  loop_back_stage: null
  blocking_issues: []
  non_blocking_findings:
    - "Security Review v2 SUPERSEDES v1 (v1 consumed implementation_report v1 + implementation_verification v1 + open_decisions v1 and predated RC-1/RC-3/RC-9/RC-10; invalidated by the HUMAN_PR_APPROVAL rejection 2026-09-01). Findings: 0 Critical, 0 Major, 3 Minor (SR-1, SR-2, SR-3), 2 Informational (SR-4, SR-5). v1's four Minor: F-1 CLOSED (RC-1), F-3 CLOSED (RC-3), F-4 CLOSED (open_decisions v2), F-2 survives as SR-2; SR-1/SR-3 new. Build/test evidence reused from implementation_verification v2 (BUILD SUCCESSFUL; 67 tests / 0 failures / 8 suites); not re-run this stage. runtime_checks PARTIAL, semantic_analysis TEXT_FALLBACK, NO dependency vulnerability scanning."
    - "Corrective delta reviewed — all security-positive or neutral: RC-1 (RegistrationRequest.toString() masks password) CLOSES v1 finding F-1; RC-3 (CustomerService maps uq_customer_email race to 409, unrelated integrity violations rethrown, +2 deterministic tests) CLOSES v1 finding F-3; RC-9 code half (SecurityConfig comment aligned to 'authentication-required by default (SC-4), not denyAll()'; anyRequest().authenticated() unchanged) is SC-4-compliant; RC-10 (stray src/main/.../docs/ subtree) confirmed removed. open_decisions v2 published + APPROVED CLOSES v1 finding F-4 (satisfies human REJECT-2)."
    - "SR-1 (Minor, AUTHORIZATION/doc): RC-9 DOCUMENTATION HALF still unpublished — docs/specifications/US-001-spec.md:135 (SEC-1 row) and docs/designs/api/US-001-api-design.md:138/:174 still read 'deny-by-default (SC-4)' without the clarifying note that this means authentication-required-by-default, not literal denyAll(). NO security risk (code is SC-4-compliant; SC-4's own wording is authentication-required-by-default). NOT a SECURITY_REVIEW loop-back (loop_back reaches only IMPLEMENTATION and API_DESIGN-via-invalid_security_design; the design is not unsafe, just under-worded). INSTRUCTION TO RECONCILIATION: do NOT record RC-9 as closed while the note is unpublished; route it via specification_gap -> SPECIFICATION and/or design_gap -> API_DESIGN. Owned by spec-writer / openapi-designer."
    - "SR-2 (Minor, API_SECURITY/doc): implemented 400/415 error message strings differ verbatim from the OpenAPI illustrative examples (409 matches exactly; AC-6 shape preserved; tests assert status+shape; implemented messages are more generic — no extra disclosure). Optional openapi-designer example alignment. Carried from v1 F-2 / verification MF-b. No loop-back."
    - "SR-3 (Minor, PERSISTENCE/robustness): CustomerService.isEmailUniquenessViolation uses Hibernate constraint name + case-insensitive message-token contains('uq_customer_email'). Crafted-email false-positive is practically unreachable — the only other customer constraints (pk_customer on a server-generated id, ck_customer_role on a server-set value, NOT NULL columns) cannot be tripped by user email content and their messages name the constraint, not the row email. Impact ceiling if it ever misfired: a real integrity error returns 409 instead of 500 — no data exposure, no authz/enumeration effect. Optional hardening: constraint-name-only match. No loop-back. (v1 F-3 is CLOSED by RC-3; this is the verifier-forwarded residual.)"
    - "SR-4 (Informational, CONFIGURATION): default-profile datasource URL uses AUTO_SERVER=TRUE with username sa / blank password — an H2 mixed-mode TCP listener with no credential. APPROVED configuration (DB design section 8, plan M-2, impact analysis); local-dev only; training data only; test profile uses isolated in-memory H2. Recommendation: future hardening Story drops AUTO_SERVER or binds it to loopback and externalizes an H2 password."
    - "SR-5 (Informational, SECRET_MANAGEMENT): spring.datasource.password: \"\" and username sa committed in application.yaml. Empty string is the H2 default, not a secret — SC-7 not breached. Externalize when a real datasource is introduced."
    - "Forwarded arbitration items — all SIGNED OFF: R-2 (CSRF scope) — csrf.ignoringRequestMatchers uses the SAME exact-match RequestMatcher as permitAll, CSRF otherwise default-enabled, 401 entry point not form-login 302, formLogin/httpBasic/logout disabled; 'CSRF enforced everywhere else' is config-verified only (no second writable endpoint to test — recorded as a limitation). R-7 (message hygiene) — every error message is a fixed generic string, no submitted value interpolated, tested. RC-3 heuristic completeness — see SR-3. Debug-logging pre-mask risk — no logging config/logger anywhere in src/main and RC-1 mask now prevents rendering regardless. RC-9 SC-4 sign-off — anyRequest().authenticated() fully satisfies security-conventions.md SC-4 as authoritatively worded."
    - "Positive controls verified: BCrypt (no no-op encoder); plaintext password confined to the request DTO AND toString()-masked (RC-1); zero logging in src/main; CustomerResponse credential/internal-state isolation (positively asserted); SC-4 authz with a single exact permitAll matcher (401, not redirect); CSRF exemption on the same single matcher only; concurrent-duplicate integrity (uq_customer_email + constraint-scoped 409 mapping); H2 console disabled every profile; ddl-auto=validate every profile; mass-assignment closed (fail-on-unknown-properties); error hygiene (single advice, static messages, 500 leaks nothing)."
    - "Observation (not a blocker): implementation_verification v2 front matter status: DRAFT vs its result envelope artifact_status: APPROVED — mirrors the v1 verification artifact, established repo pattern for verification artifacts; orchestrator already advanced on it. Noted for the human diff reviewer."
    - "Staleness (waived, carried): specification v1 / implementation_plan v1 / ac_test_matrix v1 front matter reference open_decisions v1 (now v2); v2 change-log = 'No decision content changed'. RECONCILIATION to note, not re-open."
    - "Working tree clean (git status --short empty); corrective pass committed 6c7d9e8. git diff main...HEAD = 52 files incl. harness-maintenance (.gitignore +4, docs/evidence/.gitignore, history.jsonl, workflow-state.yaml) — RECONCILIATION section 15 classification, not changed here. Hook output-path fix for the removed tool-usage.jsonl remains a finding for the human (D-2)."
```
