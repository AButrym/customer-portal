---
artifact_type: test_strategy
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
supersedes: docs/tests/US-001-test-strategy.md
---

# Test Strategy — US-001 Customer Registration

## 1. Story

Public self-service customer registration: `POST /api/v1/customers` validates
`email` + `password` server-side, rejects a duplicate email case-insensitively
with `409`, stores a BCrypt hash, creates an enabled `CUSTOMER` account with UTC
audit timestamps, and returns `201` + `Location` + a credential-free body.

Authoritative inputs: Specification `docs/specifications/US-001-spec.md` **v2**
(§5 Acceptance Criteria, §6 Validation Rules, §7 Security, §8 Error Handling),
API design + `docs/designs/api/US-001-openapi.yaml` **v2**, DB design + entity
model **v2**, Implementation Plan **v2**, Plan Review **v2**. All six Open
Decisions are RESOLVED and recorded in `docs/decisions/US-001-open-decisions.md`
v2 / APPROVED (OD-001:A, OD-002:B, OD-003:A, OD-004:A, OD-005:A, OD-006:A).

## 1a. v1 → v2 delta (why this artifact was re-issued)

This is the `TEST_WRITING` re-run in the `RECONCILIATION` v3 loop-back cascade
(`specification_gap` / RC-9). The cascade's only substantive change is
**documentation-only**: SC-4 "deny by default" is now explicitly stated to mean
*authentication-required by default* (`anyRequest().authenticated()`), not a
literal `denyAll()` — aligned across `specification` v2 §7 SEC-1, `api_design`
v2 §6/§8, `openapi` v2 `x-auth-posture`, and `design_review` v2 D-10. There is
**no** change to any Acceptance Criterion, validation rule, status code, error
model, request/response schema, or database constraint.

Consequently v2 of this strategy:

- refreshes every input reference to the all-v2 artifact chain;
- records that **production code and the full executable suite already exist**
  in the tree (built in the earlier IMPLEMENTATION occurrence of this cascade;
  no `src/**` change since commit `640850d`). The suite is **green**, not red —
  see §3;
- realizes the v1 `DEFERRED → IMPLEMENTATION` rows into the concrete test
  classes / methods that now exist, and closes the `ac_test_matrix` half of the
  prior staleness waiver;
- adds the `RegistrationRequestTest` class (RC-1 / REJECT-3 `toString` masking,
  SC-1 / SEC-3) that was introduced in the corrective pass but had no matrix
  row in v1;
- re-adjudicates the v1 §8 "known limitations" list — three items are now
  resolved, not open (see §8).

`test-writer` makes **no edit under `src/`** in this run. Nothing
requirement-driven forces a test change (the cascade delta is doc-only), and any
`src/test/**` edit would re-stale `implementation_verification` v2 and
`security_review` v2, which both consume this artifact and the `ac_test_matrix`.

## 2. Test scope

**In scope** — every US-001 Acceptance Criterion (spec AC-001..AC-007) plus the
two derived request-shape rules (unknown JSON property → `400`, malformed JSON →
`400`), the AC-6 error-body shape, the credential-hygiene rules (SC-1 / SC-9 /
SEC-3 / SEC-6), and the security posture the Story changes (registration path
public + CSRF-exempt; every other route authentication-required by default; H2
console never exposed).

**Out of scope** — login / authentication (US-002), `GET /api/v1/customers/{id}`
response contract (future Story; only referenced by the `Location` header),
password reset, email verification, MFA, account activation, rate limiting
(OD-005:A). No test asserts behavior for these; `GET /api/v1/customers/{id}` is
exercised only as an authentication-required guard.

## 3. Implementation state — green phase

At this `TEST_WRITING` occurrence the feature is **already implemented** (the
cascade re-entered the pipeline above IMPLEMENTATION and has now come back down
to it). `src/main/java/org/example/customerportal/` contains the entity, `Role`
enum, repository, password constraint + validator, request/response/error DTOs,
domain exceptions, service, controller, `SecurityConfig`, `JpaAuditingConfig`,
`schema.sql`, and the profile fixtures. The full test suite (8 classes, 67
tests) is present and **passes** — `./gradlew clean test` → BUILD SUCCESSFUL,
0 failures / 0 errors / 0 skipped (per-suite counts in the test-generation
report §6).

Per the `test-writer` "all new behavior tests pass before implementation" check:
this is not a weak-assertion or layer-bypass situation — the functionality
genuinely exists, built by the prior IMPLEMENTATION stage in this same cascade
and verified by `implementation_verification` v2 (PASS) and `security_review`
v2 (PASS). The suite therefore serves as the regression contract for
IMPLEMENTATION and every downstream review.

## 4. Test levels

| Level | Mechanism | Used for | Classes |
|---|---|---|---|
| Contract / web (integration) | `@SpringBootTest` + `@AutoConfigureMockMvc`, `@ActiveProfiles("test")` | status codes, `Location`, response body shape, `fieldErrors[]`, AC-6 error-body shape, media-type handling, request-shape rules, duplicate-email flow, SC-9 hygiene | `registration.CustomerRegistrationApiTest` |
| Security posture | `@SpringBootTest` + `MockMvc` | public registration path, CSRF exemption scope, authentication-required-by-default elsewhere, H2 console not exposed | `security.RegistrationSecurityPostureTest` |
| Persistence — schema | `@SpringBootTest` + `JdbcTemplate` on H2 `INFORMATION_SCHEMA` | column names / types / lengths / nullability, `uq_customer_email`, absence of a plaintext column, timezone-aware audit columns | `persistence.CustomerSchemaTest` |
| Persistence — slice | `@SpringBootTest` + `@Transactional`, repository + `JdbcTemplate` | JPA auditing writes UTC `created_at` / `updated_at`; `created_at` not modified by a later update; `EnumType.STRING` round-trip; entity ↔ `schema.sql` agreement under `ddl-auto=validate` (R-1 / PD-6) | `persistence.CustomerPersistenceTest` |
| Unit — validation | plain `ConstraintValidator` unit test, parameterised | byte-precise 12..72 boundary (PD-2 / R-3), each character-class rule, `@NotBlank` delegation, static no-echo message (SC-9 / R-7) | `validation.PasswordPolicyValidatorTest` |
| Unit / slice — service | `@ExtendWith(MockitoExtension.class)`, mocked repository + real `BCryptPasswordEncoder` | email normalization + trim, service-layer policy re-check before hashing (FR-6), BCrypt hash produced and verifies, duplicate guard (same + different case), concurrent-duplicate unique-violation → `409` mapping (RC-3), unrelated integrity violation not misreported | `service.CustomerServiceTest` |
| Unit — DTO hygiene | plain unit test | `RegistrationRequest.toString()` masks the plaintext password (RC-1 / REJECT-3, SC-1 / SEC-3); accessor still returns the real value | `model.request.RegistrationRequestTest` |
| Regression | existing smoke test, now `@ActiveProfiles("test")` (plan M-4, landed) | context boots with Spring Security + Spring Data JPA active | `CustomerPortalApplicationTests` |

## 5. Scenarios

### 5.1 Positive

- Valid email + 12-char policy-compliant password → `201`, `Location`
  `.../api/v1/customers/{digits}`, body `{ id, email, role="CUSTOMER", createdAt }`.
- Mixed-case / whitespace-padded email → stored and echoed trimmed + lowercase
  (OD-006:A).
- 72-byte ASCII policy-compliant password → `201` (upper boundary accepted).
- Service happy path → entity has `role=CUSTOMER`, `enabled=true`, a BCrypt hash
  that verifies against the plaintext; response carries no credential field.
- JPA auditing → `created_at` / `updated_at` non-null, UTC offset; `role`
  persists as the enum name.

### 5.2 Negative

- Duplicate email, second attempt in a different letter case → `409`, body
  `error="Conflict"`, message exactly `An account with this email already exists.`
  (OD-003:A), no second resource.
- Concurrent duplicate (uniqueness check passes, then `save` trips
  `uq_customer_email`) → mapped to `DuplicateEmailException` → `409` (RC-3);
  an unrelated integrity violation is **not** remapped.
- Malformed email, blank email, email > 254 chars → `400` + `fieldErrors[]`
  entry `field = "email"`.
- Password failing each rule individually (too short, no upper, no lower, no
  digit, no special, blank) → `400` + `fieldErrors[]` entry `field = "password"`.
- Service-layer re-check: a policy-violating password throws
  `InvalidPasswordException` before `existsByEmail` or `save` is called (FR-6).
- Unknown / extra JSON property → `400`.
- Malformed JSON body → `400`.
- `Content-Type` not `application/json`, and missing `Content-Type` → `415`.

### 5.3 Boundary

- Password length is measured in **UTF-8 bytes** (R-3 / PD-2, spec-review F-5).
  Vectors: 11-byte reject, 12-byte accept, 72-byte accept, 73-byte reject;
  `"Aa1!" + "€"×23` = 27 characters / 73 bytes → reject (would wrongly pass if
  the limit were counted in characters); `"Aa1!" + "€"×22 + "aa"` = 72 bytes →
  accept.
- Web layer: `"Aa1!" + "b"×68` = 72 chars / 72 bytes, all classes present →
  `201`; `"Aa1!" + "€"×23` (73 bytes) → `400` password field error.
- Email `"a"×250 + "@example.com"` = 262 chars → `400` (over 254).
- Minimum-length compliant password `"Aa1!aaaaaaaa"` (12 chars) → accepted.

### 5.4 Validation

- Server-side only (NFR-002): every rule is asserted through the HTTP API or the
  validator unit with no client-side assumption.
- `fieldErrors[]` uses the JSON field name (`email` / `password`) per
  `api-conventions.md` AC-6 and API design §7.
- The error body carries `timestamp, status, error, message, path` (AC-6 shape);
  `path == "/api/v1/customers"`.

### 5.5 Security

- `POST /api/v1/customers` is reachable unauthenticated (SEC-1, SC-4) — status
  is neither `401` nor `403`.
- The same POST is accepted **without a CSRF token** (OD-002:B, SC-5) — the
  exemption is scoped to this path.
- An unauthenticated `GET /api/v1/customers/1` returns `401`
  (authentication-required by default; SC-4 = `anyRequest().authenticated()`,
  not `denyAll()`). This row was a v1 tripwire for plan-review F-3 / risk R-2 —
  it now **passes** (the implementation uses a `401` entry point, not form
  login).
- `GET /h2-console` is not served (`200` never returned) — SC-6 / SEC-9.
- Success response never contains `password`, `passwordHash`, `password_hash`,
  `enabled`, or `updatedAt` (SEC-3, SEC-4, OD-004:A).
- No validation `message` echoes the submitted password (SC-9); the constraint's
  default message is the fixed string `Password does not meet the security
  policy.`
- Error `message` never contains `Exception`, an `org.example` / `org.springframework`
  package name, a `jdbc:h2` URL, or a SQL keyword (SC-9, SEC-6).
- `RegistrationRequest.toString()` renders `password=***`, never the submitted
  value (RC-1 / REJECT-3, SC-1 / SEC-3).

### 5.6 Persistence

- Table `customer` exists (hand-written `schema.sql`, PC-2 / SC-8).
- `id BIGINT NOT NULL`; `email VARCHAR(254) NOT NULL`;
  `password_hash VARCHAR(60) NOT NULL`; `role VARCHAR NOT NULL`;
  `enabled BOOLEAN NOT NULL`.
- `created_at` / `updated_at` are `TIMESTAMP WITH TIME ZONE`, `NOT NULL`
  (BR-007, PC-6).
- A `UNIQUE` constraint covers `email` (`uq_customer_email`); a second row with
  the same normalized email violates it.
- No column named `password` (no plaintext at rest — BR-005, SEC-3).
- Entity ↔ `schema.sql` agree under `ddl-auto=validate` (the persistence slice
  boots clean; R-1 / PD-6).
- `created_at` is not changed by a later update; JPA auditing writes a UTC
  offset; `role` round-trips as `EnumType.STRING`.

## 6. Required fixtures

- `src/test/resources/application-test.yaml` (profile `test`): isolated
  in-memory H2 `jdbc:h2:mem:...`, `spring.jpa.hibernate.ddl-auto=validate`,
  `spring.sql.init.mode` for the embedded schema, `spring.h2.console.enabled=false`,
  `spring.jackson.deserialization.fail-on-unknown-properties=true`. Present
  (plan C-17).
- No shared mutable state between tests: every HTTP test generates a unique
  email (`System.nanoTime()`), so ordering is irrelevant and the in-memory DB is
  not assumed empty. The service and validator units hold no state.
- `CustomerServiceTest` uses a **real** `BCryptPasswordEncoder` (not a mock) so
  the "hash is genuine and verifies" assertion is meaningful.
- No external services, no sleeps, no time-dependent assertions.

## 7. Excluded scenarios (with justification)

| Excluded | Why |
|---|---|
| "Customer can authenticate later" (Story AC-001 clause) | Authentication is US-002. Verified indirectly: the stored value is a BCrypt hash of the submitted password that `BCryptPasswordEncoder.matches` accepts, and `role` is present. |
| `GET /api/v1/customers/{id}` response contract | Not implemented by US-001 (API design §1). Only an authentication-required guard is kept. |
| Rate limiting / lockout | Out of scope, OD-005:A. |
| CSRF enforcement on *other* writable endpoints | US-001 adds no second writable endpoint; R-2 assigns full CSRF-scope verification to `SECURITY_REVIEW`. |
| DB `DEFAULT` / `CHECK` clause runtime behavior | Hibernate `validate` does not exercise them (db-design §8.1); asserting them adds no requirement coverage. The `CK_CUSTOMER_ROLE` name is used only as the "unrelated violation" fixture in the service unit. |

## 8. Known limitations & carried findings (re-adjudicated for v2)

| Item | v1 status | v2 status |
|---|---|---|
| Plan-review F-3 — unauthenticated protected route `401` vs form-login `302` | open tripwire; `protectedRouteReturns401WhenUnauthenticated` asserts `401` | **Resolved.** The test passes: `SecurityConfig` uses a `401` posture, not form login. Full CSRF-elsewhere scope remains `SECURITY_REVIEW`'s (R-2) — already signed off in `security_review` v2. |
| `docs/decisions/US-001-open-decisions.md` still lists OD-001..OD-006 `OPEN` | documentation lag noted | **Resolved.** `open_decisions` is v2 / APPROVED, "No `OPEN` decisions remain". |
| Plan edit M-4 (`@ActiveProfiles("test")` on `CustomerPortalApplicationTests`) owned by IMPLEMENTATION | not yet applied | **Landed.** The smoke test carries `@ActiveProfiles("test")` and passes with Security + JPA active (R-5 closed). |
| R-3 / PD-2 byte-vs-character boundary | covered only at the HTTP layer; validator matrix deferred | **Realized.** `PasswordPolicyValidatorTest` has the full byte-length matrix (11/12/72/73-byte + multi-byte vectors) plus HTTP-layer coverage. |
| Weak matchers in `RegistrationSecurityPostureTest` | not noted | **Investigated, adequate — non-blocking.** `registrationEndpointIsReachableWithoutAuthentication` and `registrationPostIsAcceptedWithoutACsrfToken` assert `not(401)` / `not(403)` rather than a strict status. This is deliberate: the strict success path (`201` + `Location` + body) is asserted by `CustomerRegistrationApiTest.validRegistrationReturns201WithLocationAndCustomerBody`, and the strict deny path by `protectedRouteReturns401WhenUnauthenticated`. The posture test isolates the single property "CSRF / auth does not block this path" so it stays valid regardless of body-level changes. No mandatory AC depends solely on a `not(...)` matcher. |

## 9. Open Decisions affecting testing

None open. All six are RESOLVED (`open_decisions` v2 / APPROVED) and applied
consistently across the Story artifacts and this suite.
