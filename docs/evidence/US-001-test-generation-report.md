---
artifact_type: test_generation_report
story: US-001
version: 2
status: DRAFT
created_at: 2026-08-31T11:25:00Z
updated_at: 2026-09-03T09:00:00Z
produced_by: test-writer
inputs:
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
  - path: docs/tests/US-001-test-strategy.md
    version: 2
  - path: docs/tests/US-001-ac-test-matrix.md
    version: 2
supersedes: docs/evidence/US-001-test-generation-report.md
---

# Test-Generation Report — US-001 Customer Registration

## 1. Story

US-001 Customer Registration. This is the `TEST_WRITING` re-run in the
`RECONCILIATION` v3 loop-back cascade (`specification_gap` / RC-9). The cascade's
only substantive change is **documentation-only** (SC-4 "deny by default" =
authentication-required by default, `anyRequest().authenticated()`, not literal
`denyAll()` — aligned across `specification` v2 §7 SEC-1, `api_design` v2 §6/§8,
`openapi` v2 `x-auth-posture`, `design_review` v2 D-10). No Acceptance Criterion,
validation rule, status code, error model, schema, or constraint changed.

## 2. Environment

| Item | Value |
|---|---|
| Build tool | Gradle 9.7.1 (wrapper) |
| Launcher / daemon JVM | Temurin 25; Gradle Java toolchain pinned to Java 21 (`build.gradle.kts`) |
| Framework | Spring Boot 4.1.1 |
| DB (test) | isolated in-memory H2 (profile `test`, `src/test/resources/application-test.yaml`) |
| Command | `./gradlew clean test --console=plain` |
| Result | **BUILD SUCCESSFUL** |

## 3. What this run changed

**Workflow artifacts only** — no file under `src/` was created or modified
(`git status --porcelain src/` is empty; last `src/` commit is `6c7d9e8`
"Stage IMPLEMENTATION corrective pass completed").

| Path | Change |
|---|---|
| `docs/tests/US-001-test-strategy.md` | v1 → **v2**: input refs → all-v2 chain; green-phase adjudication (§3); level table updated to the 8 classes that exist; §8 re-adjudicated (F-3 tripwire, `open_decisions` v2, M-4 all resolved). |
| `docs/tests/US-001-ac-test-matrix.md` | v1 → **v2**: every `RED` / `DEFERRED → IMPLEMENTATION` row now `GREEN` with a concrete test method; `RegistrationRequestTest` rows added (RC-1 / REJECT-3); RC-3 concurrent-duplicate + heuristic-scope rows added. |
| `docs/evidence/US-001-test-generation-report.md` | this file, v1 → **v2**. |

### Why no `src/**` edit

1. The cascade delta is documentation-only; nothing requirement-driven forces a
   test change.
2. `implementation_verification` v2 (PASS) and `security_review` v2 (PASS) both
   consume `test_strategy` + `ac_test_matrix` and both rest on "no `src/**`
   change since `640850d`". A `src/test/**` edit here would re-stale both and
   extend the cascade for no requirement benefit.
3. The existing suite already covers every mandatory AC and passes.

If a test change had been required, `test-writer` would have returned
`CHANGES_REQUIRED` (`changes_required_tests`) or surfaced a `BLOCKED` upstream
conflict rather than editing silently. Neither applies.

## 4. Test inventory (existing suite, `src/test/java/org/example/customerportal/`)

| Path | Level | Tests | Covers |
|---|---|---|---|
| `registration/CustomerRegistrationApiTest.java` | web / contract (`@SpringBootTest` + `MockMvc`) | 22 | AC-001, AC-002, AC-003, AC-005, AC-006, AC-007, unknown/malformed JSON, AC-6 error body, SC-9 hygiene |
| `validation/PasswordPolicyValidatorTest.java` | unit (parameterised) | 17 | AC-006 — byte-length boundary matrix (PD-2 / R-3), character classes, `@NotBlank` delegation, SC-9 no-echo message |
| `persistence/CustomerSchemaTest.java` | schema (`@SpringBootTest` + `JdbcTemplate` on `INFORMATION_SCHEMA`) | 10 | AC-002 (unique), AC-003 (email length), AC-004 (`password_hash`, no plaintext column), NFR-4, BR-007, SEC-5 |
| `service/CustomerServiceTest.java` | service unit (`MockitoExtension`, real `BCryptPasswordEncoder`) | 7 | AC-001, AC-002, AC-004, AC-006 (FR-6 re-check), RC-3 concurrent-duplicate + heuristic scope |
| `security/RegistrationSecurityPostureTest.java` | security (`@SpringBootTest` + `MockMvc`) | 4 | SEC-1, SEC-7 / OD-002:B, SC-4 (F-3 — now passing), SC-6 / SEC-9 |
| `persistence/CustomerPersistenceTest.java` | persistence slice (`@SpringBootTest`, `@Transactional`) | 3 | AC-004, NFR-4, BR-007 — UTC auditing, `created_at` immutability, `EnumType.STRING`, `ddl-auto=validate` agreement (R-1 / PD-6) |
| `model/request/RegistrationRequestTest.java` | unit | 3 | AC-005 / SC-1 / SEC-3 — `toString()` password masking (RC-1 / REJECT-3) |
| `CustomerPortalApplicationTests.java` | regression (`@SpringBootTest`, `@ActiveProfiles("test")`) | 1 | context boots with Security + JPA active (plan M-4) |
| **Total** | | **67** | |

### Fixtures

| Path | Purpose |
|---|---|
| `src/test/resources/application-test.yaml` | profile `test`: isolated in-memory H2, `ddl-auto=validate`, embedded SQL init, H2 console off, `fail-on-unknown-properties=true` |

## 5. Green-phase adjudication

`test-writer`'s red-phase rule expects new behavior tests to fail before
implementation. Here the implementation **already exists** — built by the earlier
`IMPLEMENTATION` occurrence in this same `RECONCILIATION` v3 cascade and verified
by `implementation_verification` v2 and `security_review` v2. So every behavior
test passes. Per the Skill's "if all new behavior tests pass before
implementation, investigate" instruction:

- **The functionality genuinely exists** — controller, service, validator,
  entity, `SecurityConfig`, `schema.sql` are all present in `src/main`. Not a
  case of the tests not reaching the relevant layer.
- **Assertions are not too weak** — the web tests assert exact status codes,
  the `Location` pattern, exact `$.message` text, and field-error field names;
  the service test uses a real BCrypt encoder and asserts the hash format +
  `matches`; the schema tests read `INFORMATION_SCHEMA` for exact type / length /
  nullability. The two `not(401)` / `not(403)` matchers in the posture test are
  each paired with a strict-status test elsewhere (test-strategy §8) — recorded
  as a non-blocking observation, adequate as-is.
- **Tests do not bypass a layer** — web tests go through the full filter chain +
  `DispatcherServlet`; persistence tests hit a real H2 datasource under
  `ddl-auto=validate`.

Conclusion: the suite is a valid regression contract. `verdict: PASS`.

## 6. Execution evidence

`./gradlew clean test --console=plain` — **BUILD SUCCESSFUL** (13s).

```
67 tests completed, 0 failed, 0 skipped
```

Per-suite (from `build/test-results/test/*.xml`):

| Test class | tests | passed | failed | errors | skipped |
|---|---|---|---|---|---|
| `CustomerPortalApplicationTests` | 1 | 1 | 0 | 0 | 0 |
| `model.request.RegistrationRequestTest` | 3 | 3 | 0 | 0 | 0 |
| `persistence.CustomerPersistenceTest` | 3 | 3 | 0 | 0 | 0 |
| `persistence.CustomerSchemaTest` | 10 | 10 | 0 | 0 | 0 |
| `registration.CustomerRegistrationApiTest` | 22 | 22 | 0 | 0 | 0 |
| `security.RegistrationSecurityPostureTest` | 4 | 4 | 0 | 0 | 0 |
| `service.CustomerServiceTest` | 7 | 7 | 0 | 0 | 0 |
| `validation.PasswordPolicyValidatorTest` | 17 | 17 | 0 | 0 | 0 |
| **Total** | **67** | **67** | **0** | **0** | **0** |

### 6.1 Regression

`CustomerPortalApplicationTests.contextLoads` passes — context boots with Spring
Security + Spring Data JPA active on the `test` profile. No regression.

### 6.2 Unexpected failures

None. BUILD SUCCESSFUL; no compile error, no invalid import, no context-load
failure, no bad fixture, no missing dependency.

## 7. Untested / deferred Acceptance Criteria

None. Every v1 `DEFERRED → IMPLEMENTATION` row is now realized as a concrete
`GREEN` test method (see `ac_test_matrix` v2 §1, §4):

| v1 deferred item | Now realized as |
|---|---|
| `PasswordPolicyValidatorTest` byte-length matrix + class rules + safe message | `validation.PasswordPolicyValidatorTest` (17 tests) |
| `CustomerServiceTest` normalization, FR-6 re-check, BCrypt verify, duplicate guard | `service.CustomerServiceTest` (7 tests) |
| `CustomerPersistenceTest` `created_at` immutability, UTC offset, `EnumType.STRING`, `validate` agreement | `persistence.CustomerPersistenceTest` (3 tests) |

## 8. Open Decisions

None open. OD-001..OD-006 are RESOLVED (OD-001:A, OD-002:B, OD-003:A, OD-004:A,
OD-005:A, OD-006:A) and recorded in `docs/decisions/US-001-open-decisions.md` v2
/ APPROVED ("No `OPEN` decisions remain"). The v1 "still marks them `OPEN`"
documentation-lag note is closed.

## 9. Non-blocking findings

1. `security.RegistrationSecurityPostureTest` —
   `registrationEndpointIsReachableWithoutAuthentication` and
   `registrationPostIsAcceptedWithoutACsrfToken` assert `not(401)` / `not(403)`
   rather than a strict status. Investigated: each is paired with a strict test
   (`validRegistrationReturns201WithLocationAndCustomerBody`,
   `protectedRouteReturns401WhenUnauthenticated`); the posture test deliberately
   isolates the "auth/CSRF does not block this path" property. Adequate as-is;
   no change made (a `src/test/**` edit would re-stale
   `implementation_verification` v2 / `security_review` v2).
2. `CustomerPersistenceTest` uses `@SpringBootTest` + `@Transactional` rather
   than the plan's `@DataJpaTest` skeleton (C-T2). Deviation already recorded in
   the implementation report; it gives stronger evidence (real datasource + SQL
   init + auditing config) and does not weaken any assertion.

## 10. Overall result

`verdict: PASS`. The executable suite covers every mandatory Acceptance
Criterion at one or more levels, compiles, and passes (67 / 0 / 0). The
regression smoke test passes. `test_strategy` and `ac_test_matrix` are refreshed
to v2 with valid front matter; the `ac_test_matrix` half of the prior staleness
waiver is closed. No `src/**` change. No blocking Open Decisions.

Next stage: `IMPLEMENTATION` (`springboot-implementor`) — which, given the code
already exists and passes verification, is expected to be a no-op / confirmation
pass in this cascade.
