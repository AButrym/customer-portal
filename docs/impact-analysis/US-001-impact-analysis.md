---
artifact_type: impact_analysis
story: US-001
version: 2
status: DRAFT
created_at: 2026-08-31T10:00:04Z
updated_at: 2026-09-02T20:08:34Z
produced_by: impact-analyzer
inputs:
  - path: docs/stories/US-001-register-customer.md
    version: null
  - path: docs/specifications/US-001-spec.md
    version: 2
  - path: docs/reviews/specifications/US-001-spec-review.md
    version: 2
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
  - path: docs/decisions/US-001-open-decisions.md
    version: 2
supersedes: docs/impact-analysis/US-001-impact-analysis.md
semantic_analysis: IDEA_MCP
---

# Impact Analysis — US-001 Customer Registration

Predictive analysis of the expected change surface for US-001, produced before
implementation planning. It describes where and how the approved Story is
expected to affect the system based on the approved Specification (v2), the
approved API design (v2), the approved database design (v2), the design review
(v2, PASS), and the current repository state. It is **not** a record of files
actually changed — Reconciliation captures that later.

## Change Log

| Version | Date | Change |
|---|---|---|
| 1 | 2026-08-31 | Initial predictive impact analysis (all-v1 inputs). Verdict PASS. |
| 2 | 2026-09-02 | Loop-back cascade re-run (occurrence 2) from `RECONCILIATION` v3, key `specification_gap`. Input references refreshed to all-v2 artifacts. The only substantive upstream change in the cascade is the RC-9 **SC-4 wording clarification** ("deny by default" = *authentication-required by default* per `anyRequest().authenticated()`, not a literal `denyAll()`) — applied in §9 Security Impact and §16. `open_decisions` is now v2 / `APPROVED` with OD-001..OD-006 recorded `RESOLVED`, so the v1 "entries still OPEN" documentation-lag caveat is removed (§2, §14, §17). New advisory limitation added for design-review D-11 (spec v2 front-matter still `DRAFT`). **No change to the expected change surface, module/package/file predictions, API contract, persistence model, or risk set** — the v1..v2 cascade carries no functional, validation, error-handling, API-contract, schema, or test impact. |

## 1. Executive Summary

- **Change purpose:** add public self-service customer registration —
  `POST /api/v1/customers` — that validates input server-side, rejects duplicate
  emails (case-insensitive), stores a BCrypt password hash, and creates an
  enabled `CUSTOMER` account with UTC audit timestamps.
- **Expected scope:** greenfield feature slice on a bare Spring Boot skeleton.
  At the time of the original prediction the repository contained only
  `CustomerPortalApplication` and a context-load test; **none** of the
  architecture packages (`controller`, `service`, `repository`, `model.*`,
  `validation`, `security`, `exception`, `config`) existed. Almost every change
  is **Create**. (Implementation has since landed under the cascade — see §17;
  this artifact stays a prediction against the approved designs, not a record of
  actual changes.)
- **Affected architectural areas:** all layers of AD-2
  (`controller → service → repository → model.entity`), plus `model.request`,
  `model.dto`, `validation`, `security`, `exception`, `config`; persistence
  bootstrap (`schema.sql`, datasource + JPA config in `application.yaml`, a test
  profile); the Gradle build (add `spring-boot-starter-validation`, mandated by
  AD-5).
- **Overall risk:** **Low–Medium.** The feature is small, additive, and fully
  specified with all six Open Decisions resolved (`open_decisions` v2,
  `APPROVED`). Residual risk is concentrated in three known Spring Boot 4 / H2
  2.x integration trip points (identity-column DDL syntax, `OffsetDateTime` ↔
  `TIMESTAMP WITH TIME ZONE` under `ddl-auto=validate`, and Spring Security 6
  filter-chain config for one public CSRF-exempt path) and in the 72-**byte**
  BCrypt input boundary. No blocking Open Decisions. No upstream artifact defect
  requiring loop-back.

## 2. Source Artifacts

| Artifact | Path | Version | Status |
|---|---|---|---|
| Story | `docs/stories/US-001-register-customer.md` | (unversioned input) | IN_PROGRESS |
| Specification | `docs/specifications/US-001-spec.md` | 2 | APPROVED at HUMAN_SPEC_APPROVAL occurrence 2 (front-matter reads `DRAFT` — design-review D-11, advisory) |
| Specification Review | `docs/reviews/specifications/US-001-spec-review.md` | 2 | APPROVED (PASS) |
| API Design | `docs/designs/api/US-001-api-design.md` | 2 | APPROVED (front-matter `DRAFT`; cleared DESIGN_REVIEW v2 — D-11 class) |
| OpenAPI Contract | `docs/designs/api/US-001-openapi.yaml` | 2 | APPROVED |
| DB Design | `docs/designs/database/US-001-db-design.md` | 2 | APPROVED (front-matter `DRAFT`; cleared DESIGN_REVIEW v2 — D-11 class) |
| Entity Model | `docs/designs/database/US-001-entity-model.md` | 2 | APPROVED (front-matter `DRAFT`; cleared DESIGN_REVIEW v2 — D-11 class) |
| Design Review | `docs/reviews/designs/US-001-design-review.md` | 2 | APPROVED (PASS) |
| Open Decisions | `docs/decisions/US-001-open-decisions.md` | 2 | APPROVED — OD-001..OD-006 recorded `RESOLVED` |

Architecture inputs: `architecture.md` (AD-1..AD-8), `package-map.md`,
`api-conventions.md` (AC-1..AC-9), `persistence-conventions.md` (PC-1..PC-9),
`security-conventions.md` (SC-1..SC-9, policy block). Product inputs:
`business-rules.md` (BR-001..BR-007), `business-glossary.md`,
`non-functional-requirements.md` (NFR-001..NFR-008).

**Open Decision resolutions** (resolved by the human at `HUMAN_SPEC_APPROVAL`
2026-08-31T07:48:48Z, `history.jsonl`; now recorded in `open_decisions` v2,
`APPROVED`, and applied consistently across the Specification and both designs
per design-review v2):

| OD | Resolution | Effect relevant to planning |
|---|---|---|
| OD-001 | A | `email` `VARCHAR(254)`, Jakarta `@Email` semantics, `maxLength 254` |
| OD-002 | B | `POST /api/v1/customers` CSRF-exempt; API design §6 is the recorded SC-5 architecture decision; CSRF stays enabled elsewhere |
| OD-003 | A | duplicate email → `409 Conflict`, message `"An account with this email already exists."` |
| OD-004 | A | `201` body = `id, email, role, createdAt` only |
| OD-005 | A | anti-abuse / rate limiting out of scope |
| OD-006 | A | normalize `email` to lowercase in the service; plain `UNIQUE (email)` |

## 3. Business Capability Impact

| Capability | Change | Notes |
|---|---|---|
| Customer self-registration (`business-glossary.md` Registration; BR-001..BR-007) | **Introduced** | First write path in the application. Creates the `Customer` concept end to end. |
| Password credential handling (BR-005, SC-1, NFR-001) | **Introduced** | BCrypt hashing + dual-layer policy enforcement (request constraint + service re-check). |
| Role assignment (BR-006, SC-2) | **Introduced (partial)** | Only the `CUSTOMER` default is exercised; `ADMIN` exists in the model but is unused. |
| Account enabled state (BR-004) | **Introduced (partial)** | Always `true` on create; the disabled-account authentication check belongs to US-002. |
| Authentication (`business-glossary.md`; US-002) | **Not changed** | US-001 only makes the stored hash + role usable later. No `UserDetailsService`, no login. |
| Profile management (`business-glossary.md` Profile; US-003) | **Not changed** | Out of scope. |

## 4. Module Impact

| Module | Impact | Rationale | Confidence |
|---|---|---|---|
| `customer-portal` (single Gradle module, `main` + `test` source sets — confirmed via IDEA MCP module list) | **Modify** | New production classes + resources under the existing module; new test classes under the mirrored test tree. Add one build dependency. No new module / source set (AD-1). | HIGH |

No multi-module split, no new Gradle subproject, no new source set (AD-1).

## 5. Package Impact

Base package `org.example.customerportal`. All packages below are **new** — the
only pre-existing production class is `CustomerPortalApplication`. No package
outside `package-map.md` is introduced (AD-8; design-review D-9 explicitly
forbids a feature package such as `customer`).

| Package | Responsibility for US-001 | Impact | Architecture constraint |
|---|---|---|---|
| `controller` | `CustomerController` — `POST /api/v1/customers`, `@Valid` request binding, delegate to service, build `201` + `Location`, return `CustomerResponse` | **Create** | No business logic, no repository access, no entity in a signature (AD-2, AD-4). Must not build error bodies (AD-6, FR-10). |
| `service` | `CustomerService` (or `RegistrationService`) — normalize email, uniqueness check, password policy re-check, BCrypt hash, construct + persist `Customer`, map to `CustomerResponse` | **Create** | Owns `@Transactional` (AD-3). Entity↔DTO mapping here (AD-4). No servlet/MVC types (AD-2). |
| `repository` | `CustomerRepository extends JpaRepository<Customer, Long>` with `existsByEmail(String)` (and/or `findByEmail`) | **Create** | Queries only (AD-2). Depends only on `model.entity`. |
| `model.entity` | `Customer` entity, `Role` enum | **Create** | Never serialized as an API type (AD-4). Explicit `@Column` mapping (PC-4). `toString()` excludes `passwordHash`. |
| `model.request` | `RegistrationRequest { email, password }` with Bean Validation + the custom password constraint | **Create** | Bound with `@Valid` (AD-5). Unknown JSON fields rejected → `400` (API design §3). |
| `model.dto` | `CustomerResponse { id, email, role, createdAt }`; `ErrorResponse`, `FieldError` (error body shape) | **Create** | No credential fields ever (AD-4, PC-9). |
| `validation` | `@ValidPassword` (or similar) constraint annotation + `ConstraintValidator` implementing the SC-1 12–72 / char-class policy | **Create** | Custom constraints live here (AD-5). Message must not echo the submitted value (SC-9). |
| `security` | `SecurityConfig` (`SecurityFilterChain`) making `POST /api/v1/customers` public + CSRF-exempt, everything else **authentication-required by default** (`anyRequest().authenticated()`, SC-4); `PasswordEncoder` bean (`BCryptPasswordEncoder`) | **Create** | Security config lives here (AD-7, `package-map.md`). CSRF exemption limited to the one path (OD-002:B, SC-5). |
| `exception` | `DuplicateEmailException` (domain, no HTTP concepts) + one `@RestControllerAdvice` mapping validation→400, duplicate→409, unknown-field/malformed-JSON→400, media-type→415, unmapped→500 | **Create** | Single exception→HTTP mapping point (AD-6, AC-9, FR-10). No leakage (SC-9). |
| `config` | JPA auditing enablement (`@EnableJpaAuditing` + UTC `DateTimeProvider`/clock); Jackson `FAIL_ON_UNKNOWN_PROPERTIES` if not achieved via `additionalProperties` handling in the request DTO | **Create** | Framework `@Configuration` only, no business logic (AD-7). Auditing config required by PC-6. |

## 6. Expected File Changes

Paths are predictions from the approved designs and `package-map.md`, not facts.
Base path `src/main/java/org/example/customerportal/`.

### Files To Create

| Expected path | Responsibility | Reason | Source requirement | Confidence |
|---|---|---|---|---|
| `controller/CustomerController.java` | `POST /api/v1/customers` handler | one new operation | FR-1, FR-8, API design §4, AC-4 | HIGH |
| `service/CustomerService.java` | registration business logic + mapping + `@Transactional` | all business logic in the service | FR-3..FR-7, AD-2, AD-3, entity-model §4 | HIGH |
| `repository/CustomerRepository.java` | JPA repository, `existsByEmail` / `findByEmail` | duplicate check + future auth lookup | FR-4, DB design §5, PC-7 | HIGH |
| `model/entity/Customer.java` | `customer` table entity, 7 columns, auditing listener | one new table | DB design §4, entity-model §2, NFR-4, PC-3..PC-6 | HIGH |
| `model/entity/Role.java` | `enum Role { CUSTOMER, ADMIN }` | role persisted as enum name | entity-model §2.2, SC-2, BR-006 | HIGH |
| `model/request/RegistrationRequest.java` | inbound DTO, `@Email`/`@Size`/`@NotBlank` + `@ValidPassword`, no unknown fields | request binding + validation | API design §4.1, §6.1–§6.2, AD-5 | HIGH |
| `model/dto/CustomerResponse.java` | `201` response DTO (`id, email, role, createdAt`) | OD-004:A field list | API design §4.2, OD-004 | HIGH |
| `model/dto/ErrorResponse.java` | AC-6 error body (`timestamp, status, error, message, path, fieldErrors[]`) | standard error shape | AC-6, API design §7 | HIGH |
| `model/dto/FieldError.java` | `{ field, message }` element of `fieldErrors[]` | field-level validation errors | AC-6, FR-3 | HIGH |
| `validation/ValidPassword.java` | constraint annotation | dual-layer password policy | SC-1, FR-6, Spec §6.2 | HIGH |
| `validation/PasswordPolicyValidator.java` | `ConstraintValidator` — length **in bytes** + 4 char-class checks, safe message | SC-1 policy, 72-byte BCrypt bound | Spec §6.2, design-review D-1/D-6 | HIGH |
| `security/SecurityConfig.java` | `SecurityFilterChain`: permit `POST /api/v1/customers`, CSRF-exempt that path, `anyRequest().authenticated()` elsewhere | one public CSRF-exempt endpoint | SC-4, SC-5, OD-002:B, API design §6 | HIGH |
| `security/PasswordEncoderConfig.java` (or a bean in `SecurityConfig`) | `BCryptPasswordEncoder` bean | BCrypt hashing | SC-1, SEC-2 | HIGH |
| `exception/DuplicateEmailException.java` | domain exception, no HTTP concept | duplicate email → 409 | AD-6, FR-4, OD-003:A | HIGH |
| `exception/GlobalExceptionHandler.java` (`@RestControllerAdvice`) | maps validation/duplicate/unknown-field/malformed-JSON/media-type/unmapped → 400/409/400/400/415/500 | single mapping point | AD-6, AC-9, FR-10, API design §7 | HIGH |
| `config/JpaAuditingConfig.java` | `@EnableJpaAuditing` + UTC `DateTimeProvider` | UTC audit timestamps | PC-6, BR-007, NFR-4 | HIGH |
| `config/JacksonConfig.java` *(only if unknown-field rejection is not handled via the request DTO / advice)* | `FAIL_ON_UNKNOWN_PROPERTIES = true` | reject unknown JSON fields → 400 | API design §3, design-review D-7 | MEDIUM |
| `src/main/resources/schema.sql` | authoritative `customer` DDL (see DB design §8.1) | hand-written schema (no `schema.sql` exists) | PC-2, SC-8, DB design §8 | HIGH |
| `src/test/resources/application-test.yaml` (or `application.yml` under `src/test/resources`) | isolated in-memory H2, `ddl-auto=validate`, `sql.init.mode=embedded`, H2 console off | test DB isolation | PC-1, SC-6, DB design §8 | MEDIUM |
| `model/entity/` test(s), `service/` test(s), `controller/` test(s), integration test | AC coverage (see §10) | NFR-005 | NFR-005, plan/test stages own the exact set | MEDIUM |

### Files To Modify

| Expected path | Change | Reason | Source | Confidence |
|---|---|---|---|---|
| `build.gradle.kts` | add `implementation("org.springframework.boot:spring-boot-starter-validation")` | Bean Validation is not currently on the classpath; AD-5 states it is **required** for `@Valid` request validation | AD-5, NFR-002 | HIGH |
| `src/main/resources/application.yaml` | add H2 file datasource (`jdbc:h2:file:./data/customer-portal;AUTO_SERVER=TRUE`), `spring.jpa.hibernate.ddl-auto=validate`, `spring.jpa.properties` for `TIMESTAMP WITH TIME ZONE` if needed, `spring.sql.init.mode=always`, `spring.h2.console.enabled=false`, physical naming strategy = snake_case | no persistence config exists; PC-1, PC-2, PC-5, SC-6, SC-8 | PC-1/PC-2/PC-5, SC-6, DB design §8 | HIGH |
| `.gitignore` | confirm `./data/` (generated H2 files) is ignored | PC-1 / SC-7 repository hygiene | PC-1, SC-7 | MEDIUM |

### Files To Reuse

| Path | Use | Note |
|---|---|---|
| `src/main/java/org/example/customerportal/CustomerPortalApplication.java` | app entry point / component scan root | No change expected; new packages sit under it. `@EnableJpaAuditing` should go on a `config` class, not here (AD-7). |
| `src/test/java/org/example/customerportal/CustomerPortalApplicationTests.java` | existing context-load smoke test | Must still pass once security + JPA config is added (it will need the test profile / an in-memory datasource to boot). |
| `build.gradle.kts` Spring Boot BOM / dependency-management | version-manages the new `-validation` starter | No explicit version pin needed. |

### Files Potentially Affected

| Path | Why it might change | Confidence it changes |
|---|---|---|
| `src/main/resources/application.yaml` profile split (e.g. `application-local.yaml`) | if planning decides to separate local file-H2 from the default profile | LOW |
| `CustomerPortalApplicationTests` | may need `@ActiveProfiles("test")` or `@Import` of test config once security is enabled | MEDIUM |
| `config/OpenApiConfig` / springdoc | only if the team decides to serve the contract at runtime — **not required** by US-001 (the contract is a design artifact) | LOW |

## 7. API Impact

- **New operation:** `POST /api/v1/customers` (`registerCustomer`). Public, no
  authentication, CSRF-exempt for this path only (OD-002:B). Purely additive —
  no existing contract changes, no compatibility concern (AC-1, API design §1).
- **Request:** `application/json` required; `RegistrationRequest { email,
  password }`, `additionalProperties: false`. `email`: required, `minLength 1`,
  `maxLength 254`, `@Email` semantics. `password`: required, 12–72 (enforced as
  **72 bytes**, design-review D-6), ≥1 upper / lower / digit / special;
  `writeOnly`, never on any response.
- **Responses:** `201` + `Location: /api/v1/customers/{id}` + `CustomerResponse`;
  `400` (bean-validation, malformed JSON, unknown field) with `fieldErrors[]`
  for field failures; `409` (duplicate email, case-insensitive) with the
  OD-003:A message; `415` (missing/non-JSON `Content-Type`); `500` (unmapped, no
  leak). `401`/`403` not applicable (public endpoint).
- **Error contract:** single AC-6 body from the one `@RestControllerAdvice`
  (AC-9). `message` client-safe; `fieldErrors[].message` never echoes input
  (SC-9).
- **`Location` target:** `GET /api/v1/customers/{id}` is **not** implemented by
  US-001 (design-review D-8); the header value is still correct and stable.
- **OpenAPI sections:** `paths./customers.post`, `components.schemas`
  (`RegistrationRequest`, `CustomerResponse`, `ErrorResponse`, `FieldError`).
  The contract is authoritative for shapes; the character-class policy lives in
  the schema `description` only, not a `pattern` (design-review D-1) — tests
  source password cases from Spec §6.2. OpenAPI v2 adds only the `x-auth-posture`
  traceability key and `info.version` / `x-source-specification-version` bumps
  (design-review D-10) — no path, schema, response, example, or `security`
  change.

## 8. Persistence Impact

- **New table `customer`** (one row per registered account). No foreign keys, no
  join tables, no changes to existing schema (there is none).
- **Columns** (DB design §4.2 / entity-model §2):
  `id BIGINT` identity PK (`pk_customer`, `GenerationType.IDENTITY`);
  `email VARCHAR(254) NOT NULL` unique (`uq_customer_email`), stored lowercased;
  `password_hash VARCHAR(60) NOT NULL` (BCrypt output is exactly 60 chars);
  `role VARCHAR(20) NOT NULL DEFAULT 'CUSTOMER'` + `ck_customer_role` CHECK;
  `enabled BOOLEAN NOT NULL DEFAULT TRUE`;
  `created_at TIMESTAMP WITH TIME ZONE NOT NULL` (not updatable);
  `updated_at TIMESTAMP WITH TIME ZONE NOT NULL`.
- **Constraints / indexes:** `pk_customer`, `uq_customer_email` (also serves as
  the `email` lookup index — no separate `ix_customer_email`, PC-7),
  `ck_customer_role` (defensive, DDL-only; not verified by `validate` —
  design-review D-4).
- **Case-insensitive uniqueness (OD-006:A):** service normalizes `email` with
  `toLowerCase(Locale.ROOT)` before both the `existsByEmail` check and entity
  construction; plain `UNIQUE`, no functional index.
- **Schema management:** hand-written `src/main/resources/schema.sql` (this Story
  creates it); `spring.sql.init.mode=always` (dev) / `embedded` (test);
  `ddl-auto=validate` (or `none`) in every profile — `create`/`create-drop`/
  `update` forbidden (SC-8, PC-2). The entity mapping and `schema.sql` must agree
  exactly or the `validate` startup fails.
- **Auditing:** `@CreatedDate` / `@LastModifiedDate` via `AuditingEntityListener`
  + `@EnableJpaAuditing`, UTC (PC-6, BR-007).
- **Migration implications:** none — new table, no existing data, no migration
  tool in this project (PC-2).
- **Known trip points (design-review D-5, DB design §8.1):** on H2 2.x /
  Hibernate (Spring Boot 4), (a) `GENERATED BY DEFAULT AS IDENTITY` clause
  ordering and implicit `NOT NULL`, and (b) `OffsetDateTime` ↔ `TIMESTAMP WITH
  TIME ZONE` strict type match under `validate`. IMPLEMENTATION must make the
  build pass against `schema.sql` (NFR-7); IMPLEMENTATION_VERIFICATION checks it.
- **v1 → v2 cascade:** DB design v2 + entity-model v2 refreshed input references
  and change-log only; **no table / column / constraint / index / schema-init /
  entity / field / mapping / enum change** (db-designer occurrence 2, PASS).

## 9. Security Impact

- **Authentication:** none added for the endpoint; it is the single public route
  (SC-4). No `UserDetailsService`, no login flow (US-002). Every other route
  stays **authentication-required by default** — a `SecurityFilterChain` must be
  created with `anyRequest().authenticated()` that does not accidentally open
  anything else. Per the RC-9 clarification carried into Specification v2 §7
  SEC-1, API design v2 §6/§8, OpenAPI v2 `x-auth-posture`, and design-review v2
  D-10: "deny by default" in this Story means *authentication-required by
  default* (`anyRequest().authenticated()`), **not** a literal `denyAll()`. This
  is a wording alignment only — no behaviour, filter-chain, or test change; the
  implemented `SecurityConfig` is already SC-4-compliant.
- **Authorization:** none for the operation (`x-authorization: none`). No role or
  ownership check.
- **CSRF:** disabled for `POST /api/v1/customers` only; API design §6 is the
  recorded SC-5 architecture decision (OD-002:B). CSRF stays enabled for all
  other (future) endpoints — the config must scope the exemption to the one path.
- **Password handling:** `BCryptPasswordEncoder` (default strength), bean in
  `security`. Plaintext only on `RegistrationRequest`; never persisted, logged,
  returned, or placed on a response DTO. Policy enforced twice (request
  constraint + service re-check before hashing) — FR-6, SC-1.
- **Sensitive data / exposure:** `password_hash` only in its column, excluded
  from `toString()`, absent from `CustomerResponse` (OD-004:A, SEC-4). `email`
  (PII) stored normalized, not emitted in error messages beyond
  `fieldErrors[].field` (SC-9).
- **Account enumeration:** the explicit `409` duplicate-email response is a
  human-approved exposure (OD-003:A / SEC-8), not a default.
- **Config safety:** `spring.h2.console.enabled=false` in every profile (SC-6);
  no secrets introduced (SC-7, SEC-11); `ddl-auto` stays `validate`/`none`
  (SC-8, SEC-10).
- **Out of scope:** rate limiting / anti-abuse on registration (OD-005:A).

## 10. Testing Impact

Mapped to Acceptance Criteria (Spec §5). TEST_WRITING owns the definitive set;
this is the predicted coverage.

| AC | Test focus | Likely test type(s) |
|---|---|---|
| AC-001 | valid registration → `201`, `Location` header, `CustomerResponse` with `role=CUSTOMER`; account persisted, hash verifies | controller/web-layer + integration + persistence |
| AC-002 | duplicate email (same case and different case, e.g. `Alice@Example.com` vs `alice@example.com`) → `409` + OD-003:A message; no second row | integration + service + persistence |
| AC-003 | invalid email format / over-length → `400` + `fieldErrors[].field="email"`; no row | controller/web-layer + validation unit |
| AC-004 | stored credential is a BCrypt string in `password_hash`, not plaintext; plaintext never persisted | persistence + service |
| AC-005 | `201` body contains neither `password` nor a hash; response schema = `id, email, role, createdAt` | controller/web-layer + contract assertion |
| AC-006 | password policy violations (too short, missing each class, **72-byte** boundary) → `400` + `fieldErrors[].field="password"`; message does not echo input | validation unit + controller/web-layer |
| AC-007 | missing / non-JSON `Content-Type` → `415`; no row | controller/web-layer |
| (derived) | unknown/extra JSON field → `400`; malformed JSON → `400` | controller/web-layer |
| (derived) | `created_at` / `updated_at` populated, UTC, `created_at` not updatable | persistence |
| (regression) | `CustomerPortalApplicationTests.contextLoads` still passes with security + JPA enabled (needs the test profile) | Spring Boot context |
| SC-4/SC-5 | public path reachable unauthenticated; a second arbitrary path still `401` (`anyRequest().authenticated()`, D-10) | security test |

Test packages mirror production packages under `src/test/java`
(`package-map.md`); a cross-layer integration test may sit in a
`…​.registration` package under the base package.

## 11. Configuration and Dependency Impact

| Item | Change | Approval |
|---|---|---|
| `spring-boot-starter-validation` | **Add** to `build.gradle.kts` | Explicitly mandated by AD-5 ("`spring-boot-starter-validation` is a required dependency for this"). It is a first-party Spring Boot starter version-managed by the existing BOM — **not** a discretionary third-party dependency. Recorded here for visibility; PLAN_REVIEW / a human should still confirm at HUMAN_PLAN_APPROVAL. |
| `application.yaml` (main) | **Modify** — datasource, JPA `ddl-auto=validate`, `sql.init.mode`, snake_case naming, `h2.console.enabled=false` | Within Story scope (PC-1, PC-2, PC-5, SC-6). No human decision beyond plan approval. |
| Test resources (`src/test/resources/application-test.yaml` or `application.yml`) | **Create** — isolated in-memory H2, `ddl-auto=validate`, `sql.init.mode=embedded` | PC-1. |
| `schema.sql` | **Create** | PC-2. |
| Profiles | Possibly introduce `local` / `test` profiles | Planning decision, low impact. |
| External services | none | — |
| Runtime (JVM, ports) | none | — |

**No new third-party dependency** is required. `spring-boot-starter-data-jpa`,
`spring-boot-starter-security`, `spring-boot-starter-webmvc`, `h2`, and `lombok`
are already present.

## 12. Documentation Impact

| Document | Expected update | Owner stage |
|---|---|---|
| `docs/designs/api/US-001-openapi.yaml` | none further for US-001 (v2 authoritative as-is); a future read endpoint will extend it | — |
| `docs/architecture/api-conventions.md` AC-7 | none — session auth unchanged; token auth not introduced | — |
| `docs/architecture/architecture.md` | none — no new AD; the CSRF exemption is recorded in API design §6, not here (per SC-5 "recorded for that Story") | — |
| `docs/specifications/US-001-spec.md`, API/DB design front-matter `status:` | should read `APPROVED` (all cleared their review + gate); front-matter still `DRAFT` — design-review D-11, advisory | spec-writer / openapi-designer / db-designer |
| `docs/catalog/stories.yaml` | `US-001` state transitions handled by the orchestrator, not this Story's code | story-orchestrator |
| Implementation Report / Reconciliation / PR summary | produced by their own later stages | later stages |
| `README` / `AGENTS.md` | none required | — |

No architecture document needs editing for US-001. If IMPLEMENTATION discovers a
genuinely new architectural need, it must raise an Open Decision (AD-8) rather
than edit a convention doc silently.

## 13. Risks

| # | Severity | Description | Affected area | Mitigation | Human decision required |
|---|---|---|---|---|---|
| R-1 | Major | `ddl-auto=validate` startup fails because Hibernate (Spring Boot 4 / H2 2.x) maps `OffsetDateTime` to a SQL type other than `TIMESTAMP WITH TIME ZONE`, or rejects the `GENERATED BY DEFAULT AS IDENTITY` clause ordering in `schema.sql` (design-review D-5). | persistence bootstrap, build (NFR-7) | IMPLEMENTATION aligns the column type / field mapping and verifies a clean `validate` boot before completion; IMPLEMENTATION_VERIFICATION re-checks. DB design §8.1 already calls this out. | No |
| R-2 | Major | Spring Security 6 `SecurityFilterChain` misconfiguration: CSRF disabled globally instead of for the one path, or another route left unintentionally permitted, or the public matcher wrong (`/api/v1/customers` vs `/customers` under the `servers` prefix). | `security` package, SC-4/SC-5 | Explicit `requestMatchers(HttpMethod.POST, "/api/v1/customers").permitAll()` + `.csrf(c -> c.ignoringRequestMatchers(...))`; `anyRequest().authenticated()`; a test asserting a second arbitrary path is still `401`. SECURITY_REVIEW verifies. | No |
| R-3 | Major | 72-**byte** BCrypt input bound implemented as 72 **characters** (design-review D-6), so a multi-byte password between 72 bytes and 72 chars is wrongly accepted and truncated by BCrypt. | `validation` + `service` | Validator measures `getBytes(StandardCharsets.UTF_8).length`; service re-check does the same; TEST_WRITING adds the boundary vector. | No |
| R-4 | Minor | Unknown-JSON-field rejection wired inconsistently (Jackson `FAIL_ON_UNKNOWN_PROPERTIES` vs. DTO-level handling) so malformed-JSON and unknown-field both need a clean `400` mapping in the advice (design-review D-7, API Q-3). | `config` / `exception` | Decide the mechanism in planning; one advice branch each for `HttpMessageNotReadableException` and unknown-property. IMPLEMENTATION_VERIFICATION confirms the `400` paths. | No |
| R-5 | Minor | Existing `CustomerPortalApplicationTests.contextLoads` starts failing once Security + JPA auto-config is added, because it has no datasource/profile. | test | Provide `src/test/resources` config / `@ActiveProfiles("test")`; treat as part of this Story's test work (NFR-7). | No |
| R-6 | Minor | JPA auditing produces non-UTC timestamps if the `DateTimeProvider` / clock is not pinned to UTC (BR-007, PC-6). | `config`, persistence | `DateTimeProvider` returning `OffsetDateTime.now(ZoneOffset.UTC)` (or a `Clock` bean); persistence test asserts UTC offset. | No |
| R-7 | Minor | Password constraint validation message accidentally echoes the submitted value or is built from the raw input (SC-9 violation). | `validation` | Static, generic message; validator never includes the value; SECURITY_REVIEW checks. | No |
| R-8 | Minor | Scope creep — implementing `GET /api/v1/customers/{id}` to satisfy the `Location` header, or adding login/`UserDetailsService`. | scope (AGENTS.md Git policy) | Plan and review explicitly exclude it; the header target is a future Story (design-review D-8). | No |

No `Critical` risks. No risk requires a new human decision beyond the normal
HUMAN_PLAN_APPROVAL gate; all resolutions are already fixed by the approved
artifacts. The v1 → v2 cascade introduces no new risk (the SC-4 change is a
wording alignment).

## 14. Open Decisions

**No blocking Open Decisions were identified.** All six (OD-001..OD-006) were
resolved by the human at `HUMAN_SPEC_APPROVAL` (see §2) and are now recorded
`RESOLVED` in `open_decisions` v2 (`APPROVED`), applied consistently across the
Specification and both designs (confirmed by design-review v2, PASS). The v1
"entries still show `OPEN`" documentation lag is closed.

No `TODO` / `TBD` / `FIXME` / `???` / "to be decided" markers were found in the
approved input artifacts that would materially change the affected components.

## 15. Planning Inputs

Facts the Implementation Planner must consume (not implementation steps):

1. Greenfield: no `controller`/`service`/`repository`/`model.*`/`validation`/
   `security`/`exception`/`config` package existed at prediction time —
   everything is Create.
2. One operation only: `POST /api/v1/customers`, public, CSRF-exempt for that
   path, `application/json` required.
3. One table only: `customer`, 7 columns, `uq_customer_email`, hand-written
   `schema.sql`, `ddl-auto=validate`.
4. Entity name is `Customer` / table `customer` (covers glossary Customer +
   Account for US-001; design-review D-2). `role` is an `EnumType.STRING`
   `VARCHAR(20)` column, not a table (D-3).
5. Email normalized to lowercase **in the service** before the uniqueness check
   and the insert; plain `UNIQUE` (OD-006:A).
6. Password policy (12–72, 4 char classes) enforced **twice** — custom
   `validation` constraint **and** service re-check before hashing; the 72 bound
   is **bytes** (D-6).
7. `password_hash VARCHAR(60)`, BCrypt via `BCryptPasswordEncoder` bean in
   `security`; plaintext never persisted/logged/returned.
8. `201` body = `id, email, role, createdAt` exactly (OD-004:A). No `password`,
   no hash, no `enabled`, no `updatedAt`.
9. Duplicate email → `409` with message `"An account with this email already
   exists."` (OD-003:A), from a `DuplicateEmailException` mapped by the single
   `@RestControllerAdvice`.
10. Unknown/extra JSON field and malformed JSON → `400` (API design §3, D-7);
    choose the Jackson/DTO mechanism in the plan.
11. Add `spring-boot-starter-validation` to `build.gradle.kts` (AD-5). No other
    dependency.
12. JPA auditing config (`@EnableJpaAuditing` + UTC provider) is required
    (PC-6, BR-007) and belongs in `config`, not the main application class.
13. `application.yaml` needs datasource + JPA + snake_case naming + H2 console
    off; a test resource config with isolated in-memory H2 must be created; the
    existing `contextLoads` test must still pass.
14. No new package outside `package-map.md` (AD-8); the entity-model §6 mention
    of a "customer" feature package is advisory and must not be followed (D-9).
15. Security posture: one public endpoint; `anyRequest().authenticated()`
    everywhere else. "Deny by default" (SC-4) = authentication-required by
    default, **not** literal `denyAll()` (Specification v2 §7 SEC-1, API design
    v2 §6/§8, design-review v2 D-10).
16. Out of scope: login/auth, `GET /customers/{id}`, rate limiting, profile,
    email verification, account activation.

## 16. Traceability

| AC | Spec section | Design artifact | Affected system area | Expected test category |
|---|---|---|---|---|
| AC-001 Successful registration | §4 FR-1/FR-5/FR-8/FR-9, §5 | API design §4, OpenAPI `201`; DB design §4, entity-model §4.1 | `controller`, `service`, `repository`, `model.entity`, `schema.sql` | web-layer + integration + persistence (happy path) |
| AC-002 Unique email (case-insensitive) | §4 FR-4, §6.1, §8 | API design §4.3 `409`; DB design §5, `uq_customer_email` | `service` (normalize + `existsByEmail`), `exception` advice, DB constraint | integration + service + persistence |
| AC-003 Email validation | §4 FR-3, §6.1 | OpenAPI `RegistrationRequest.email`; API design §4.1 | `model.request`, `exception` advice | validation unit + web-layer |
| AC-004 Password storage | §4 FR-5/FR-6/FR-7, §7 | DB design §4.2/§7; entity-model §4.1 | `service` (BCrypt), `model.entity` `password_hash` | persistence + service |
| AC-005 Secure response | §4 FR-7/FR-8, §7 | API design §4.2 `CustomerResponse`; OpenAPI schema | `model.dto`, `service` mapping | web-layer + contract assertion |
| AC-006 Password policy | §4 FR-3/FR-6, §6.2 | API design §4.1; design-review D-1/D-6 | `validation` constraint + validator, `service` re-check | validation unit + web-layer (incl. 72-byte boundary) |
| AC-007 Media type | §4 FR-2, §8 | OpenAPI `415`; API design §4.3 | MVC content negotiation, `exception` advice | web-layer |
| (derived) unknown/malformed JSON | §6.3 | API design §3, OpenAPI `additionalProperties: false` | `config`/`model.request`, `exception` advice | web-layer |
| NFR-4 explicit mapping / UTC audit | §9 NFR-4 | DB design §4, entity-model §2/§3 | `model.entity`, `config` auditing, `schema.sql` | persistence |
| SC-4/SC-5 security posture | §7 SEC-1/SEC-7 (v2 wording) | API design §6/§8; OpenAPI `x-auth-posture`; design-review D-10 | `security` filter chain (`anyRequest().authenticated()`) | security test (public path + other path still `401`) |

## 17. Analysis Limitations

- **Semantic analysis: IDEA_MCP** was available and used for module discovery
  (`get_project_modules`) and repository structure inspection. It confirmed the
  single-module layout (AD-1).
- **Occurrence 2 / cascade context:** this re-run is a loop-back cascade from
  `RECONCILIATION` v3 (`specification_gap`). Implementation, tests,
  `IMPLEMENTATION_VERIFICATION` v2, and `SECURITY_REVIEW` v2 have already run and
  are current/PASS; no `src/**` change since commit `640850d`. This artifact
  remains a **prediction against the approved designs**, not a record of actual
  changes — Reconciliation owns the actual-change record. The v1 predictions are
  broadly borne out by the landed code (all predicted packages/classes exist;
  `InvalidPasswordException` is an additional class; `PasswordEncoderConfig` /
  `JacksonConfig` were folded into `SecurityConfig` / the advice rather than
  standalone).
- All predicted file paths remain **MEDIUM** confidence as predictions where the
  file did not exist at prediction time — final class names / splits are
  IMPLEMENTATION_PLANNING's to fix.
- This analysis did **not** re-execute the Gradle build or boot the application.
  The `ddl-auto=validate` / `OffsetDateTime` / H2 identity-syntax risks (R-1)
  are owned by IMPLEMENTATION / IMPLEMENTATION_VERIFICATION.
- **design-review D-11 (advisory):** Specification v2 and the API/DB design v2
  artifacts carry front-matter `status: DRAFT` although each cleared its review
  and (for the spec) `HUMAN_SPEC_APPROVAL` occurrence 2. The recorded gate/review
  decisions are authoritative; owners are `spec-writer` / `openapi-designer` /
  `db-designer`. Not a blocker and no design/PR impact.
- Areas that would need re-analysis: any further change to the approved
  Specification or either design (would trigger a loop-back), or discovery during
  planning that a new package / dependency / architectural decision is genuinely
  required.

## 18. Readiness Result

**Verdict: PASS.** The expected change surface is identified with acceptable
confidence and is unchanged by the v1 → v2 cascade. US-001 is a small, additive,
fully specified feature; every Open Decision is resolved and consistently applied
(`open_decisions` v2, `APPROVED`); the only substantive upstream change is the
RC-9 SC-4 wording clarification, which is a documentation alignment with no
behaviour, contract, schema, or test impact. No approved upstream artifact is
wrong or incomplete, so no loop-back is warranted. Residual risks (R-1..R-8) are
owned by later stages and carried forward as non-blocking findings. The Story may
proceed to IMPLEMENTATION_PLANNING.

```yaml
result:
  verdict: PASS
  stage: IMPACT_ANALYSIS
  story: US-001
  artifact_status: DRAFT
  artifacts:
    - docs/impact-analysis/US-001-impact-analysis.md
  next_stage: IMPLEMENTATION_PLANNING
  loop_back_stage: null
  blocking_issues: []
  non_blocking_findings:
    - "Occurrence 2 (loop-back cascade from RECONCILIATION v3, specification_gap). Input references refreshed to all-v2 artifacts; expected change surface, module/package/file predictions, API contract, persistence model, and risk set all unchanged."
    - "SC-4 wording alignment (RC-9 / design-review D-10): 'deny by default' = authentication-required by default (anyRequest().authenticated()), not literal denyAll(). Applied in spec v2 §7 SEC-1, API design v2 §6/§8, OpenAPI v2 x-auth-posture. Documentation-only; no behaviour/contract/schema/test change."
    - "R-1: ddl-auto=validate startup vs OffsetDateTime <-> TIMESTAMP WITH TIME ZONE and H2 2.x IDENTITY clause ordering (design-review D-5); IMPLEMENTATION/IMPLEMENTATION_VERIFICATION own it."
    - "R-2: Spring Security 6 SecurityFilterChain must scope the CSRF exemption + public matcher to POST /api/v1/customers only and keep anyRequest().authenticated(); SECURITY_REVIEW verifies."
    - "R-3/D-6: password 72 limit is BYTES of BCrypt input, not characters; enforce in the validation constraint and the service re-check; TEST_WRITING adds the boundary vector."
    - "R-4/D-7: choose the unknown-JSON-field rejection mechanism (Jackson FAIL_ON_UNKNOWN_PROPERTIES vs DTO) in planning; advice maps unknown-field and malformed JSON to 400 (API Q-3)."
    - "R-5: existing CustomerPortalApplicationTests.contextLoads needs a test profile / in-memory datasource once Security + JPA are enabled (NFR-7)."
    - "R-6: JPA auditing DateTimeProvider must be pinned to UTC (BR-007, PC-6); config class, not the main application class (AD-7)."
    - "Dependency: add spring-boot-starter-validation to build.gradle.kts - required by AD-5, first-party starter version-managed by the existing BOM, not a discretionary third-party dependency; confirm at HUMAN_PLAN_APPROVAL."
    - "Entity naming (D-2) and role-as-enum-column (D-3) confirmed by DESIGN_REVIEW; planning must use package-map.md packages, not the entity-model 'customer' feature-package note (D-9, AD-8)."
    - "open_decisions is now v2 / APPROVED with OD-001..OD-006 RESOLVED; the v1 'entries still OPEN' documentation lag is closed."
    - "design-review D-11 (advisory): specification v2 + API/DB design v2 front-matter status reads DRAFT though each cleared its review/gate; owners spec-writer / openapi-designer / db-designer; no design or PR impact."
```
