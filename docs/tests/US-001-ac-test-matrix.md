---
artifact_type: ac_test_matrix
story: US-001
version: 2
status: DRAFT
created_at: 2026-08-31T11:25:00Z
updated_at: 2026-09-03T09:00:00Z
produced_by: test-writer
inputs:
  - path: docs/stories/US-001-register-customer.md
    version: null
  - path: docs/specifications/US-001-spec.md
    version: 2
  - path: docs/designs/api/US-001-api-design.md
    version: 2
  - path: docs/designs/api/US-001-openapi.yaml
    version: 2
  - path: docs/designs/database/US-001-db-design.md
    version: 2
  - path: docs/designs/database/US-001-entity-model.md
    version: 2
  - path: docs/impact-analysis/US-001-impact-analysis.md
    version: 2
  - path: docs/plans/US-001-implementation-plan.md
    version: 2
  - path: docs/reviews/plans/US-001-plan-review.md
    version: 2
supersedes: docs/tests/US-001-ac-test-matrix.md
---

# Acceptance-Criteria → Test Matrix — US-001

This matrix is **authoritative**. `implementation-verifier`, `security-reviewer`
and `reconciliation-reviewer` read it; they do not rebuild it.

`Status` is the state at this `TEST_WRITING` occurrence:

- `GREEN` — the test compiles, runs, and passes against the current
  implementation (`./gradlew clean test` → BUILD SUCCESSFUL, 67 / 0 / 0).

Every v1 `RED` and `DEFERRED → IMPLEMENTATION` row is now `GREEN` with a concrete
test method: the feature was built by the earlier IMPLEMENTATION occurrence in
the `RECONCILIATION` v3 loop-back cascade (no `src/**` change since commit
`640850d`), and this `TEST_WRITING` re-run refreshes the matrix to the all-v2
artifact chain, names the previously-deferred methods, and adds the
`RegistrationRequestTest` row (RC-1 / REJECT-3). See the test-generation report
§5 for the green-phase adjudication.

Base test package: `org.example.customerportal` (mirrors production tree,
`package-map.md` test rule).

## 1. Story / Specification Acceptance Criteria

| AC | Scenario | Level | Test class | Test method | Expected result | Status |
|---|---|---|---|---|---|---|
| AC-001 | Valid email + 12-char compliant password | web | `registration.CustomerRegistrationApiTest` | `validRegistrationReturns201WithLocationAndCustomerBody` | `201`; `Location` matches `.*/api/v1/customers/\d+`; body `{id:number, email, role:"CUSTOMER", createdAt}` | GREEN |
| AC-001 | Mixed-case / padded email normalized to lowercase + trimmed (OD-006:A) | web | `registration.CustomerRegistrationApiTest` | `emailIsStoredAndReturnedNormalisedToLowercase` | `201`; `$.email` equals the lowercased input | GREEN |
| AC-001 | 72-byte compliant password accepted (upper boundary) | web | `registration.CustomerRegistrationApiTest` | `password72CharsMeetingPolicyIsAccepted` | `201` | GREEN |
| AC-001 | Registration reachable without authentication (SEC-1) | security | `security.RegistrationSecurityPostureTest` | `registrationEndpointIsReachableWithoutAuthentication` | status not `401` and not `403` | GREEN |
| AC-001 / AC-004 | Service happy path: enabled `CUSTOMER`, BCrypt hash produced and verifies against the plaintext | service | `service.CustomerServiceTest` | `happyPathCreatesAnEnabledCustomerWithABcryptHash` | persisted entity `role=CUSTOMER`, `enabled=true`, `passwordHash` matches `^\$2[aby]\$\d\d\$.{53}$` and `!= raw`; `BCryptPasswordEncoder.matches(raw, hash)` true; response `role="CUSTOMER"` | GREEN |
| AC-001 / AC-002 | Service normalizes + trims the email before the uniqueness check and before save (OD-006:A) | service | `service.CustomerServiceTest` | `emailIsNormalisedToLowercaseAndTrimmedBeforeCheckAndSave` | `existsByEmail("alice@example.com")` and saved entity email both the normalized form | GREEN |
| AC-002 | Duplicate email, second attempt different case → `409`, one resource | web | `registration.CustomerRegistrationApiTest` | `duplicateEmailIsRejectedCaseInsensitivelyWith409` | `409`; `$.status==409`; `$.error=="Conflict"`; `$.message=="An account with this email already exists."` | GREEN |
| AC-002 | `email` has a `UNIQUE` constraint | persistence | `persistence.CustomerSchemaTest` | `emailHasAUniqueConstraint` | a `UNIQUE` `TABLE_CONSTRAINT` covers `EMAIL` | GREEN |
| AC-002 | Two rows, same normalized email → constraint violation | persistence | `persistence.CustomerSchemaTest` | `caseInsensitiveDuplicateEmailCollidesOnTheUniqueConstraint` | second `INSERT` throws | GREEN |
| AC-002 | Service detects the duplicate before insert and throws `DuplicateEmailException` (same case) | service | `service.CustomerServiceTest` | `duplicateEmailSameCaseThrowsAndDoesNotSave` | `DuplicateEmailException`; `save` never called | GREEN |
| AC-002 | Same, different case | service | `service.CustomerServiceTest` | `duplicateEmailDifferentCaseThrowsAndDoesNotSave` | `DuplicateEmailException`; `save` never called | GREEN |
| AC-002 | Concurrent duplicate: uniqueness check passes, then `save` trips `uq_customer_email` → mapped to `409` (RC-3 / REJECT-4) | service | `service.CustomerServiceTest` | `concurrentDuplicateEmailUniqueViolationIsMappedToDuplicateEmailException` | `DataIntegrityViolationException` naming `UQ_CUSTOMER_EMAIL` → `DuplicateEmailException` | GREEN |
| AC-002 | An unrelated integrity violation is **not** remapped to duplicate-email (RC-3 heuristic scope) | service | `service.CustomerServiceTest` | `anUnrelatedIntegrityViolationIsNotReportedAsADuplicateEmail` | `CK_CUSTOMER_ROLE` violation propagates unchanged | GREEN |
| AC-003 | Malformed email format | web | `registration.CustomerRegistrationApiTest` | `malformedEmailReturns400WithEmailFieldError` | `400`; `$.fieldErrors[*].field` has `email` | GREEN |
| AC-003 | Blank email | web | `registration.CustomerRegistrationApiTest` | `blankEmailReturns400WithEmailFieldError` | `400`; `fieldErrors` has `email` | GREEN |
| AC-003 | Email longer than 254 chars (OD-001:A) | web | `registration.CustomerRegistrationApiTest` | `emailLongerThan254CharsReturns400WithEmailFieldError` | `400`; `fieldErrors` has `email` | GREEN |
| AC-003 | `email` column is `VARCHAR(254) NOT NULL` | persistence | `persistence.CustomerSchemaTest` | `emailColumnIsVarchar254NotNull` | type `CHARACTER VARYING`, length `254`, not nullable | GREEN |
| AC-004 | `password_hash` column is `VARCHAR(60) NOT NULL` (PC-9) | persistence | `persistence.CustomerSchemaTest` | `passwordHashColumnIsVarchar60NotNull` | type `CHARACTER VARYING`, length `60`, not nullable | GREEN |
| AC-004 | No plaintext-password column exists (BR-005, SEC-3) | persistence | `persistence.CustomerSchemaTest` | `noPlaintextPasswordColumnExists` | zero columns named `PASSWORD` | GREEN |
| AC-004 | `customer` table exists (hand-written schema) | persistence | `persistence.CustomerSchemaTest` | `customerTableExists` | exactly one `CUSTOMER` table | GREEN |
| AC-004 | Service re-checks the byte-length password policy before hashing or touching the repository (FR-6) | service | `service.CustomerServiceTest` | `serviceRechecksThePasswordPolicyBeforeHashingOrTouchingTheRepository` | `InvalidPasswordException`; `existsByEmail` and `save` never called | GREEN |
| AC-005 | Success response excludes password, hash, `enabled`, `updatedAt` | web | `registration.CustomerRegistrationApiTest` | `successResponseNeverExposesCredentialOrInternalState` | `$.password`, `$.passwordHash`, `$.password_hash`, `$.enabled`, `$.updatedAt` all absent | GREEN |
| AC-005 | `RegistrationRequest.toString()` masks the submitted plaintext password (RC-1 / REJECT-3, SC-1 / SEC-3) | unit | `model.request.RegistrationRequestTest` | `toStringNeverRendersTheSubmittedPlaintextPassword` | rendered string contains `password=***`, the email, and **not** the secret | GREEN |
| AC-005 | `toString()` render is independent of the password value and null-safe | unit | `model.request.RegistrationRequestTest` | `toStringRenderIsIndependentOfThePasswordValueAndDoesNotThrowOnNull` | equal renders for different passwords; no NPE on `null` | GREEN |
| AC-005 | `password()` accessor still returns the real value (mask is render-only) | unit | `model.request.RegistrationRequestTest` | `passwordAccessorStillReturnsTheRealValue` | accessor returns the submitted string | GREEN |
| AC-006 | Password shorter than 12 bytes | web | `registration.CustomerRegistrationApiTest` | `passwordShorterThan12CharsReturns400WithPasswordFieldError` | `400`; `fieldErrors` has `password` | GREEN |
| AC-006 | Password without uppercase | web | `registration.CustomerRegistrationApiTest` | `passwordWithoutUppercaseReturns400WithPasswordFieldError` | `400`; `fieldErrors` has `password` | GREEN |
| AC-006 | Password without lowercase | web | `registration.CustomerRegistrationApiTest` | `passwordWithoutLowercaseReturns400WithPasswordFieldError` | `400`; `fieldErrors` has `password` | GREEN |
| AC-006 | Password without digit | web | `registration.CustomerRegistrationApiTest` | `passwordWithoutDigitReturns400WithPasswordFieldError` | `400`; `fieldErrors` has `password` | GREEN |
| AC-006 | Password without special char | web | `registration.CustomerRegistrationApiTest` | `passwordWithoutSpecialCharReturns400WithPasswordFieldError` | `400`; `fieldErrors` has `password` | GREEN |
| AC-006 | Blank password | web | `registration.CustomerRegistrationApiTest` | `blankPasswordReturns400WithPasswordFieldError` | `400`; `fieldErrors` has `password` | GREEN |
| AC-006 | **Byte-length boundary (R-3 / PD-2):** `"Aa1!"+"€"×23` = 27 chars / 73 bytes | web | `registration.CustomerRegistrationApiTest` | `passwordOver72BytesButUnder72CharsReturns400WithPasswordFieldError` | `400`; `fieldErrors` has `password` (fails if length is counted in characters) | GREEN |
| AC-006 | Validator: 11-byte reject | unit | `validation.PasswordPolicyValidatorTest` | `elevenBytesIsRejected` | `isCompliant` false | GREEN |
| AC-006 | Validator: 12-byte accept | unit | `validation.PasswordPolicyValidatorTest` | `twelveBytesIsAccepted` | `isCompliant` true | GREEN |
| AC-006 | Validator: 72-byte accept | unit | `validation.PasswordPolicyValidatorTest` | `seventyTwoBytesIsAccepted` | `isCompliant` true | GREEN |
| AC-006 | Validator: 73-byte reject | unit | `validation.PasswordPolicyValidatorTest` | `seventyThreeBytesIsRejected` | `isCompliant` false | GREEN |
| AC-006 | Validator: multi-byte 73-byte / 27-char reject | unit | `validation.PasswordPolicyValidatorTest` | `multiByteStringOver72BytesButUnder72CharsIsRejected` | `isCompliant` false | GREEN |
| AC-006 | Validator: multi-byte 72-byte accept | unit | `validation.PasswordPolicyValidatorTest` | `multiByteStringAtOrUnder72BytesIsAccepted` | `isCompliant` true | GREEN |
| AC-006 | Validator: each missing character class rejected | unit | `validation.PasswordPolicyValidatorTest` | `missingACharacterClassIsRejected` (parameterised ×4) | `isCompliant` false for no-upper / no-lower / no-digit / no-special | GREEN |
| AC-006 | Validator: compliant-flag matrix | unit | `validation.PasswordPolicyValidatorTest` | `compliantFlagMatchesExpectation` (parameterised ×3) | flag matches expectation incl. empty → false | GREEN |
| AC-006 | Validator: `null` is not compliant | unit | `validation.PasswordPolicyValidatorTest` | `nullIsNotCompliant` | `isCompliant(null)` false | GREEN |
| AC-006 | Validator delegates null / empty to `@NotBlank` | unit | `validation.PasswordPolicyValidatorTest` | `isValidLeavesNullAndEmptyToNotBlank` | `isValid(null)` and `isValid("")` both true | GREEN |
| AC-006 | Validator rejects a non-compliant value | unit | `validation.PasswordPolicyValidatorTest` | `isValidRejectsANonCompliantValue` | `isValid("short")` false | GREEN |
| AC-006 / SC-9 | Constraint default message echoes no submitted value | unit | `validation.PasswordPolicyValidatorTest` | `defaultMessageNeverEchoesASubmittedValue` | `@ValidPassword` default message is exactly `Password does not meet the security policy.` | GREEN |
| AC-006 / SC-9 | HTTP: password validation message does not echo the submitted value | web | `registration.CustomerRegistrationApiTest` | `passwordValidationMessageDoesNotEchoTheSubmittedValue` | no `$..message` contains the submitted string | GREEN |
| AC-007 | `Content-Type: text/plain` | web | `registration.CustomerRegistrationApiTest` | `nonJsonContentTypeReturns415` | `415` | GREEN |
| AC-007 | Missing `Content-Type` | web | `registration.CustomerRegistrationApiTest` | `missingContentTypeReturns415` | `415` | GREEN |

## 2. Derived rules (Specification §6.3, API design §3)

| Rule | Scenario | Level | Test class | Test method | Expected | Status |
|---|---|---|---|---|---|---|
| Unknown JSON property rejected (`fail-on-unknown-properties`, PD-1) | body has an extra `role` field | web | `registration.CustomerRegistrationApiTest` | `unknownJsonPropertyReturns400` | `400`; `$.status==400` | GREEN |
| Malformed JSON rejected | truncated JSON body | web | `registration.CustomerRegistrationApiTest` | `malformedJsonReturns400` | `400`; `$.status==400` | GREEN |
| AC-6 error-body shape | `400` body has `timestamp, status, error, message, path` | web | `registration.CustomerRegistrationApiTest` | `errorBodyHasTheApiConventionShape` | all five fields present; `path == "/api/v1/customers"` | GREEN |

## 3. Security posture (Specification §7, OD-002:B)

| Requirement | Scenario | Level | Test class | Test method | Expected | Status |
|---|---|---|---|---|---|---|
| SEC-7 / OD-002:B CSRF exemption scoped to the registration path | tokenless `POST /api/v1/customers` | security | `security.RegistrationSecurityPostureTest` | `registrationPostIsAcceptedWithoutACsrfToken` | status not `403` | GREEN |
| SEC-1 / SC-4 authentication-required by default elsewhere (`anyRequest().authenticated()`, not `denyAll()`) | unauthenticated `GET /api/v1/customers/1` | security | `security.RegistrationSecurityPostureTest` | `protectedRouteReturns401WhenUnauthenticated` | `401` (v1 plan-review F-3 tripwire — now passing; implementation uses a `401` posture, not form login) | GREEN |
| SC-6 / SEC-9 H2 console never exposed | `GET /h2-console` | security | `security.RegistrationSecurityPostureTest` | `h2ConsoleIsNotExposed` | status not `200` | GREEN |
| SC-9 / SEC-6 error message leaks no internals | malformed JSON | web | `registration.CustomerRegistrationApiTest` | `errorBodyNeverLeaksInternals` | `message` has no `Exception` / `org.example` / `org.springframework` / `jdbc:h2` / SQL keyword | GREEN |
| SEC-5 role + enabled columns non-null | schema | `persistence.CustomerSchemaTest` | `roleColumnIsNotNull`, `enabledColumnIsBooleanNotNull` | both `NOT NULL`; `enabled` is `BOOLEAN` | GREEN |

## 4. Persistence / NFR-4 / BR-007

| Requirement | Scenario | Level | Test class | Test method | Expected | Status |
|---|---|---|---|---|---|---|
| NFR-4 surrogate `Long id` | `id` column | persistence | `persistence.CustomerSchemaTest` | `idColumnIsBigintNotNull` | `BIGINT`, `NOT NULL` | GREEN |
| BR-007 / PC-6 UTC audit columns | `created_at` / `updated_at` | persistence | `persistence.CustomerSchemaTest` | `auditTimestampColumnsAreTimeZoneAwareAndNotNull` | both `TIMESTAMP WITH TIME ZONE`, `NOT NULL` | GREEN |
| BR-007 / PC-6 auditing writes UTC offsets | persist a `Customer` | persistence | `persistence.CustomerPersistenceTest` | `auditingPopulatesBothTimestampsInUtc` | `created_at` / `updated_at` non-null, offset `Z` | GREEN |
| PC-6 `created_at` not updatable | update a persisted `Customer` | persistence | `persistence.CustomerPersistenceTest` | `createdAtIsNotChangedByALaterUpdate` | `created_at` unchanged after a later `save` | GREEN |
| entity-model `EnumType.STRING` round-trip; entity ↔ `schema.sql` agreement under `ddl-auto=validate` (R-1 / PD-6) | persist + reload; context boots on `validate` | persistence | `persistence.CustomerPersistenceTest` | `roleIsPersistedAsTheEnumName` | stored `role` column is `"CUSTOMER"`; reloaded entity `Role.CUSTOMER`; slice boots clean under `validate` | GREEN |

## 5. Regression

| Scenario | Test class | Test method | Expected | Status |
|---|---|---|---|---|
| Context boots with Security + JPA active on the `test` profile (plan M-4 landed) | `CustomerPortalApplicationTests` | `contextLoads` | passes | GREEN |

## 6. Coverage check

Every mandatory Acceptance Criterion (AC-001..AC-007) has at least one `GREEN`
executable test, and most have coverage at two or three levels (web + service +
persistence / validation). The derived request-shape rules, the AC-6 error-body
shape, and every security-posture requirement the Story changes are covered.
No AC depends on a weak assertion: the two `not(4xx)` matchers in
`RegistrationSecurityPostureTest` are each paired with a strict-status test
elsewhere (test-strategy §8).

67 tests across 8 classes; `./gradlew clean test` → BUILD SUCCESSFUL, 0 failures,
0 errors, 0 skipped (test-generation report §6).
