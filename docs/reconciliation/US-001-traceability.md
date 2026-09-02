---
artifact_type: traceability
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
supersedes: docs/reconciliation/US-001-traceability.md
---

# End-to-End Traceability Matrix — US-001 Customer Registration  (v3)

Authoritative Acceptance-Criteria → artifact / code / test matrix for US-001.
`implementation-verifier`, `security-reviewer`, and `pr-preparer` reference this
matrix; they do not rebuild it. It is owned by `reconciliation-reviewer`.

> **v3.** Supersedes traceability v2. The corrective implementation pass
> (`implementation_report` v2, attempt 2) applied RC-1, RC-3, RC-9 (code half),
> and RC-10; `implementation_verification` v2 (PASS, 67/67) and
> `security_review` v2 (PASS, 0 Critical / 0 Major) independently confirmed them.
> **All seven Acceptance Criteria are now `RECONCILED`** — AC-002 and AC-004,
> `PARTIALLY_RECONCILED` in v2, are closed. The security-posture row
> **SEC-1 / SC-4 remains `PARTIALLY_RECONCILED`**: the RC-9 *documentation half*
> (spec §7 SEC-1 row line 135; api-design §6 line 138 / §8 line 174) is still
> unpublished — those artifacts still read "deny-by-default (SC-4)" without the
> clarifying note. See `docs/reviews/reconciliation/US-001-reconciliation.md` v3
> §17 (RC-9).

Base package `org.example.customerportal`. Production base path
`src/main/java/org/example/customerportal/`. Test base path
`src/test/java/org/example/customerportal/`.

Final status vocabulary: `RECONCILED` (intent, spec, design, plan,
implementation, test, verification, and security evidence all agree);
`PARTIALLY_RECONCILED`; `NOT_RECONCILED`; `BLOCKED`.

## 1. Story Acceptance Criteria → full chain

### AC-001 — Successful Registration  (Spec AC-001)

| Dimension | Reference |
|---|---|
| Story | AC-001 Successful Registration |
| Specification | §4 FR-1, FR-5, FR-8, FR-9; §5 AC-001; §6.1 / §6.2 valid path |
| Resolved decisions | OD-001:A, OD-004:A, OD-006:A — all `RESOLVED` in `open_decisions.md` v2 |
| API design | api-design §4, §4.2, §4.3 `201`; openapi.yaml `paths./customers.post` `201` + `Location` + `CustomerResponse` |
| DB design | db-design §4.2, §8.1 DDL; entity-model §2, §4.1 |
| Impact analysis | §6, §7, §8, §16 |
| Plan step / files | Steps 4, 8, 9; C-13, C-12, C-3, C-2, C-1, C-7, C-16 |
| Production code | `controller/CustomerController.register`; `service/CustomerService.register` (BCrypt encode, `Role.CUSTOMER`, `enabled=true`, `Location`); `repository/CustomerRepository.save`; `model/entity/Customer`; `model/dto/CustomerResponse`; `src/main/resources/schema.sql` |
| Tests | `registration.CustomerRegistrationApiTest.validRegistrationReturns201WithLocationAndCustomerBody`, `.emailIsStoredAndReturnedNormalisedToLowercase`, `.password72CharsMeetingPolicyIsAccepted`; `service.CustomerServiceTest.happyPathCreatesAnEnabledCustomerWithABcryptHash`; `security.RegistrationSecurityPostureTest.registrationEndpointIsReachableWithoutAuthentication` |
| Impl. Verification | v2 §7 AC-001 VERIFIED (carried; unchanged in the corrective pass) |
| Security Review | v2 §5 (auth), §7 (BCrypt hash verifies, `role=CUSTOMER`, `enabled=true`) |
| **Final status** | **RECONCILED** |

### AC-002 — Unique Email  (Spec AC-002)

| Dimension | Reference |
|---|---|
| Story | AC-002 Unique Email |
| Specification | §4 FR-4; §6.1 uniqueness; §8 duplicate-email row; SEC-8 |
| Resolved decisions | OD-003:A (explicit `409` + message `"An account with this email already exists."`), OD-006:A (case-insensitive via lowercasing + plain `UNIQUE`) |
| API design | api-design §4.3 `409`; openapi.yaml `409` `duplicateEmail` example |
| DB design | db-design §4.3 `uq_customer_email`, §5 case-insensitive mechanism; entity-model §3 |
| Impact analysis | §6, §7, §8, §16 |
| Plan step / files | Step 8; C-12, C-10, C-11, C-3, C-16 |
| Production code | `service/CustomerService.register`: pre-check `existsByEmail(normalizeEmail(...))` → `DuplicateEmailException`; **and** `try/catch (DataIntegrityViolationException)` around `save` → `isEmailUniquenessViolation(...)` (Hibernate constraint name + case-insensitive cause-chain message-token match on `uq_customer_email`) → `DuplicateEmailException`, any other integrity violation rethrown. `exception/GlobalExceptionHandler.handleDuplicateEmail` → `409` + OD-003:A message. `Customer` `@UniqueConstraint(uq_customer_email)`; `schema.sql` `uq_customer_email`. |
| Tests | `registration.CustomerRegistrationApiTest.duplicateEmailIsRejectedCaseInsensitivelyWith409`; `service.CustomerServiceTest.duplicateEmailSameCaseThrowsAndDoesNotSave`, `.duplicateEmailDifferentCaseThrowsAndDoesNotSave`, `.emailIsNormalisedToLowercaseAndTrimmedBeforeCheckAndSave`, **`.concurrentDuplicateEmailUniqueViolationIsMappedToDuplicateEmailException`**, **`.anUnrelatedIntegrityViolationIsNotReportedAsADuplicateEmail`** (`isSameAs` negative — load-bearing); `persistence.CustomerSchemaTest.emailHasAUniqueConstraint`, `.caseInsensitiveDuplicateEmailCollidesOnTheUniqueConstraint` |
| Impl. Verification | **v2 §7 AC-002 VERIFIED — single-request and concurrent paths**; v1 finding MF-3 CLOSED |
| Security Review | v2 §11 (concurrent duplicate → `409` VERIFIED, v1 F-3 CLOSED; residual robustness note SR-3, Minor, no loop-back); §16 abuse case PROTECTED |
| Corrective change (RC-3 / REJECT-4) | **APPLIED & VERIFIED** — `implementation_report` v2 §4, `implementation_verification` v2 §7/§17, `security_review` v2 §11. |
| **Final status** | **RECONCILED** — single-request and concurrent-duplicate paths both return `409`; deterministic test coverage present. |

### AC-003 — Email Validation  (Spec AC-003)

| Dimension | Reference |
|---|---|
| Story | AC-003 Email Validation |
| Specification | §4 FR-3; §6.1 format + max length |
| Resolved decisions | OD-001:A (`@Email` semantics + max 254) |
| API design | api-design §4.1; openapi.yaml `RegistrationRequest.email` (`minLength 1`, `maxLength 254`, `format: email`), `400` `invalidEmail` example |
| DB design | db-design §4.2 `email VARCHAR(254) NOT NULL` |
| Impact analysis | §7, §16 |
| Plan step / files | Steps 6, 9, 11; C-6, C-11 |
| Production code | `model/request/RegistrationRequest` (`@NotBlank @Email @Size(max = 254)` on `email`); `exception/GlobalExceptionHandler.handleValidation` → `400` + `fieldErrors[]` |
| Tests | `registration.CustomerRegistrationApiTest.malformedEmailReturns400WithEmailFieldError`, `.blankEmailReturns400WithEmailFieldError`, `.emailLongerThan254CharsReturns400WithEmailFieldError`; `persistence.CustomerSchemaTest.emailColumnIsVarchar254NotNull` |
| Impl. Verification | v2 §7 AC-003 VERIFIED (carried) |
| Security Review | v2 §9 input validation VERIFIED |
| **Final status** | **RECONCILED** |

### AC-004 — Password Storage  (Spec AC-004)

| Dimension | Reference |
|---|---|
| Story | AC-004 Password Storage (not stored in plain text) |
| Specification | §4 FR-5, FR-6, FR-7; §7 SEC-2, SEC-3, SEC-4; PC-9 |
| Resolved decisions | — (no OD; PC-9 `password_hash VARCHAR(60)`) |
| API design | api-design §4.1 (`password` `writeOnly`, dual-layer policy); openapi.yaml `password` `writeOnly` |
| DB design | db-design §4.2 `password_hash VARCHAR(60) NOT NULL`, §7 sensitive-data handling; entity-model §2, §4.1 |
| Impact analysis | §8, §9 |
| Plan step / files | Steps 8, 10; C-12, C-14, C-2 |
| Production code | `service/CustomerService.register` (`passwordEncoder.encode(password)`, plaintext discarded); `security/SecurityConfig.passwordEncoder` = `new BCryptPasswordEncoder()`; `model/entity/Customer.passwordHash` `@Column(length = 60, nullable = false)`; `schema.sql` `password_hash VARCHAR(60) NOT NULL`, no plaintext column; `Customer.toString()` excludes `passwordHash`; **`model/request/RegistrationRequest.toString()` overridden to `"RegistrationRequest{email='…', password=***}"`** |
| Tests | `persistence.CustomerSchemaTest.passwordHashColumnIsVarchar60NotNull`, `.noPlaintextPasswordColumnExists`; `service.CustomerServiceTest.happyPathCreatesAnEnabledCustomerWithABcryptHash`, `.serviceRechecksThePasswordPolicyBeforeHashingOrTouchingTheRepository`; **`model.request.RegistrationRequestTest`** (3 tests — `toString()` never renders the plaintext, `password=***` present, null-safe, `password()` accessor unchanged) |
| Impl. Verification | **v2 §7 AC-004 VERIFIED incl. no plaintext in `toString()`**; v1 finding MF-5 CLOSED |
| Security Review | v2 §7 (plaintext not renderable via `toString()` — VERIFIED, v1 F-1 CLOSED); §8, §20 positive control 2 |
| Corrective change (RC-1 / REJECT-3) | **APPLIED & VERIFIED** — `implementation_report` v2 §4, `implementation_verification` v2 §7/§12, `security_review` v2 §7. |
| **Final status** | **RECONCILED** — BCrypt-only storage, no plaintext column, not returned, and the request DTO `toString()` masks the password with a proving test. |

### AC-005 — Secure Response  (Spec AC-005)

| Dimension | Reference |
|---|---|
| Story | AC-005 Secure Response (password and hash not returned) |
| Specification | §4 FR-7, FR-8; §7 SEC-3, SEC-4 |
| Resolved decisions | OD-004:A (`201` body = `id, email, role, createdAt` only) |
| API design | api-design §4.2 `CustomerResponse`; openapi.yaml `CustomerResponse` schema (no credential / internal fields) |
| DB design | db-design §7; entity-model §4.2 (`passwordHash` never mapped; `enabled` / `updatedAt` not exposed) |
| Impact analysis | §7, §9 |
| Plan step / files | Steps 7, 8; C-7, C-12 |
| Production code | `model/dto/CustomerResponse` = `record(Long id, String email, String role, OffsetDateTime createdAt)`; `service/CustomerService.toResponse` |
| Tests | `registration.CustomerRegistrationApiTest.successResponseNeverExposesCredentialOrInternalState` (`$.password`, `$.passwordHash`, `$.password_hash`, `$.enabled`, `$.updatedAt` all absent) |
| Impl. Verification | v2 §7 AC-005 VERIFIED (carried) |
| Security Review | v2 §8, §20 positive control 4 |
| **Final status** | **RECONCILED** |

### AC-006 — Password Policy Enforcement  (Spec AC-006, derived from Story AC-001 / AC-003)

| Dimension | Reference |
|---|---|
| Story | derived — password policy (Business Value: self-registration with a valid password) |
| Specification | §4 FR-3, FR-6; §6.2 password policy (12–72 bytes, upper/lower/digit/special); SC-1; SC-9 |
| Resolved decisions | — (spec-review F-5 / design-review D-6: 72 is BCrypt input **bytes**; plan PD-2) |
| API design | api-design §4.1; design-review D-1, D-6 |
| DB design | db-design §10 note 5 |
| Impact analysis | §7, §10; risk R-3 |
| Plan step / files | Steps 6, 8; C-4, C-5, C-12; PD-2 |
| Production code | `validation/ValidPassword` (static generic message); `validation/PasswordPolicyValidator` (`MIN_BYTES = 12`, `MAX_BYTES = 72` UTF-8, 4 char-class checks); `service/CustomerService.register` re-check via `PasswordPolicyValidator.isCompliant` → `InvalidPasswordException`; `exception/GlobalExceptionHandler.handleInvalidPassword` / `.handleValidation` → `400` |
| Tests | `registration.CustomerRegistrationApiTest` 8 password scenarios incl. `.passwordOver72BytesButUnder72CharsReturns400WithPasswordFieldError`, `.passwordValidationMessageDoesNotEchoTheSubmittedValue`; `validation.PasswordPolicyValidatorTest` (17 tests); `service.CustomerServiceTest.serviceRechecksThePasswordPolicyBeforeHashingOrTouchingTheRepository` |
| Impl. Verification | v2 §7 AC-006 VERIFIED (carried) |
| Security Review | v2 §7 (policy = SC-1, enforced twice, byte-measured, non-echoing message — VERIFIED); R-7 signed off; §20 positive control 12 |
| **Final status** | **RECONCILED** |

### AC-007 — Media Type Enforcement  (Spec AC-007, derived from api-conventions.md AC-2)

| Dimension | Reference |
|---|---|
| Story | derived — `api-conventions.md` AC-2 + clarification assumption |
| Specification | §4 FR-2; §8 `415` row |
| Resolved decisions | — |
| API design | api-design §4.3 `415`; openapi.yaml `415` `unsupportedMediaType` example |
| DB design | n/a |
| Impact analysis | §7, §16 |
| Plan step / files | Steps 9, 11; C-13 (`consumes`), C-11 |
| Production code | `controller/CustomerController` `@PostMapping(consumes = APPLICATION_JSON_VALUE)`; `exception/GlobalExceptionHandler.handleMediaType` → `415` |
| Tests | `registration.CustomerRegistrationApiTest.nonJsonContentTypeReturns415`, `.missingContentTypeReturns415` |
| Impl. Verification | v2 §7 AC-007 VERIFIED (carried) |
| Security Review | v2 §10 API security VERIFIED |
| **Final status** | **RECONCILED** (finding RC-2 — implemented `415` `message` string differs verbatim from the OpenAPI illustrative example; AC-6 body **shape** preserved; no behaviour mismatch). |

## 2. Derived rules

| Rule | Spec / design | Production code | Test | Status |
|---|---|---|---|---|
| Unknown / extra JSON property → `400` | Spec §6.3; api-design §3; openapi.yaml `additionalProperties: false` | `spring.jackson.deserialization.fail-on-unknown-properties: true`; `GlobalExceptionHandler.handleUnreadable` (single branch, PD-1) | `registration.CustomerRegistrationApiTest.unknownJsonPropertyReturns400` | RECONCILED (RC-2 — single combined message vs two OpenAPI examples; shape preserved) |
| Malformed JSON → `400` | Spec §6.3; api-design §3 | same `HttpMessageNotReadableException` branch | `registration.CustomerRegistrationApiTest.malformedJsonReturns400` | RECONCILED |
| AC-6 error body shape (`timestamp, status, error, message, path`, optional `fieldErrors[]`) | api-conventions.md AC-6; api-design §7 | `model/dto/ErrorResponse` (`@JsonInclude(NON_EMPTY)`), `model/dto/ApiFieldError`; single `@RestControllerAdvice` | `registration.CustomerRegistrationApiTest.errorBodyHasTheApiConventionShape`, `.errorBodyNeverLeaksInternals` | RECONCILED |

## 3. Security posture

| Requirement | Spec | Production code | Test | Status |
|---|---|---|---|---|
| SEC-1 / SC-4 — registration public, everything else authentication-required by default | §7 SEC-1 | `security/SecurityConfig` `REGISTRATION_ENDPOINT` matcher `permitAll()` + `anyRequest().authenticated()`; `HttpStatusEntryPoint(401)`; `formLogin`/`httpBasic`/`logout` disabled. **Class javadoc + inline comment now state "authentication-required by default (SC-4) … not a literal `denyAll()`" (RC-9 code half).** | `security.RegistrationSecurityPostureTest.registrationEndpointIsReachableWithoutAuthentication`, `.protectedRouteReturns401WhenUnauthenticated` | **PARTIALLY_RECONCILED** — behaviour is secure and tested; the `SecurityConfig` code comment is aligned; **but `docs/specifications/US-001-spec.md:135` (SEC-1 row) and `docs/designs/api/US-001-api-design.md:138` / `:174` still read "deny-by-default (SC-4)" without the clarifying note.** RC-9 / REJECT-5 is closable only with both halves in place. Routed to `SPECIFICATION` (`specification_gap`); the API design note follows in the cascade. |
| SEC-7 / OD-002:B — CSRF exemption scoped to the registration POST only | §7 SEC-7; api-design §6 | `SecurityConfig` `.csrf(c -> c.ignoringRequestMatchers(REGISTRATION_ENDPOINT))` — the same single matcher | `security.RegistrationSecurityPostureTest.registrationPostIsAcceptedWithoutACsrfToken` | RECONCILED (security_review v2 R-2 signed off) |
| SEC-9 / SC-6 — H2 console disabled every profile | §7 SEC-9 | `spring.h2.console.enabled: false` in `application.yaml` **and** `application-test.yaml` | `security.RegistrationSecurityPostureTest.h2ConsoleIsNotExposed` | RECONCILED |
| SEC-6 — error responses leak no internals | §7 SEC-6 | `GlobalExceptionHandler` — one static client-safe `message` per branch; `500` fallback | `registration.CustomerRegistrationApiTest.errorBodyNeverLeaksInternals` | RECONCILED |
| SEC-5 — new account `ROLE_CUSTOMER`, `enabled = true` | §7 SEC-5 | `CustomerService` sets `Role.CUSTOMER`, `enabled = true`; `schema.sql` `role`/`enabled` `NOT NULL` | `persistence.CustomerSchemaTest.roleColumnIsNotNull`, `.enabledColumnIsBooleanNotNull`; `CustomerServiceTest` happy path | RECONCILED |
| SEC-10 / SC-8 — `ddl-auto` `validate`, hand-written `schema.sql` | §7 SEC-10 | `ddl-auto: validate` both profiles; `src/main/resources/schema.sql` | context boots clean under `validate` (Impl. Verification v2 §5, §9) | RECONCILED |
| SEC-11 / SC-7 — no secrets introduced | §7 SEC-11 | `application.yaml` `password: ""` is the H2 default (not a secret); no tokens/keys | Security Review v2 §17 | RECONCILED (findings SR-4 / SR-5 — Informational: blank H2 credential + `AUTO_SERVER`; approved config, local-dev only) |
| SEC-3 — plaintext password never logged / echoed | §7 SEC-3 | plaintext confined to `RegistrationRequest`; discarded after `encode`; **`RegistrationRequest.toString()` masks `password`** | `model.request.RegistrationRequestTest` (3 tests); `service.CustomerServiceTest`; `security_review` v2 §7/§13 | **RECONCILED** — RC-1 closed; no reachable leak path and the latent `toString()` path is now masked with a proving test. |

## 4. Persistence / NFR-4 / BR-007

| Requirement | Design | Production code | Test | Status |
|---|---|---|---|---|
| Surrogate `Long id`, `BIGINT` identity | db-design §4.2; entity-model §2 | `Customer.id` `@GeneratedValue(IDENTITY)`; `schema.sql` `id BIGINT GENERATED BY DEFAULT AS IDENTITY`, `pk_customer` | `persistence.CustomerSchemaTest.idColumnIsBigintNotNull` | RECONCILED (finding RC-7 — Informational: `id` DDL has no explicit `NOT NULL`; H2 2.x implicit; `validate` passes) |
| Explicit column length / nullability on every column | db-design §4.2; NFR-4; PC-4 | `Customer` explicit `@Column(...)` per field | `persistence.CustomerSchemaTest` (email 254, password_hash 60, role/enabled/id NOT NULL) | RECONCILED |
| UTC audit timestamps, `created_at` immutable | db-design §4.2; entity-model §3; BR-007; PC-6 | `Customer.createdAt` `@CreatedDate @Column(updatable = false)`, `updatedAt` `@LastModifiedDate`; `config/JpaAuditingConfig` UTC `DateTimeProvider`; `schema.sql` `TIMESTAMP WITH TIME ZONE NOT NULL` | `persistence.CustomerSchemaTest.auditTimestampColumnsAreTimeZoneAwareAndNotNull`; `persistence.CustomerPersistenceTest.auditingPopulatesBothTimestampsInUtc`, `.createdAtIsNotChangedByALaterUpdate` | RECONCILED (R-1 / R-6 closed) |
| `role` persisted as enum name (`EnumType.STRING`) | db-design §4.2; entity-model §2.2 | `Customer.role` `@Enumerated(EnumType.STRING) @Column(length = 20)`; `ck_customer_role` CHECK in DDL | `persistence.CustomerPersistenceTest.roleIsPersistedAsTheEnumName` | RECONCILED |
| Generated `./data/*` git-ignored | db-design §8; impact §6 M-3 | `.gitignore` `/data/` | not tracked, not in tree (Impl. Verification v2 §4) | RECONCILED |

## 5. Regression

| Scenario | Test | Status |
|---|---|---|
| Context still boots with Security + JPA active | `CustomerPortalApplicationTests.contextLoads` (`@ActiveProfiles("test")`, M-4) | RECONCILED — 1/1 PASS (independently reproduced by `implementation-verifier` v2) |

## 6. Coverage summary

| | Count |
|---|---|
| Story / Specification Acceptance Criteria (AC-001..AC-007) | 7 |
| RECONCILED | **7** (AC-001..AC-007) |
| PARTIALLY_RECONCILED | 0 |
| NOT_RECONCILED / BLOCKED | 0 |
| Security-posture rows PARTIALLY_RECONCILED | **1** (SEC-1 / SC-4 — RC-9 documentation half unpublished; routed to `SPECIFICATION`) |
| Executable tests (independently reproduced by `implementation-verifier` v2) | **67** across 8 suites, 0 failures / 0 errors / 0 skipped |

Every mandatory Acceptance Criterion has an approved requirement, an
implementation location, a test, and independent verification / security
evidence — **all seven are `RECONCILED`**. The one open item is a
documentation-consistency residual on the SEC-1 / SC-4 posture row: the RC-9
"deny-by-default" → "authentication-required by default" note, made mandatory by
the human at `HUMAN_PR_APPROVAL` (REJECT-5), is present in `SecurityConfig` code
but not yet in `docs/specifications/US-001-spec.md` §7 or
`docs/designs/api/US-001-api-design.md` §6 / §8. Reconciliation v3 routes it to
`SPECIFICATION` (`specification_gap`); `API_DESIGN` picks up its half in the
cascade. No code, test, persistence, or behaviour change is required.
