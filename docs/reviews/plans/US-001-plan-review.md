---
artifact_type: plan_review
story: US-001
version: 2
status: APPROVED
created_at: 2026-08-31T11:05:00Z
updated_at: 2026-09-02T22:55:00Z
produced_by: plan-reviewer
inputs:
  - path: docs/plans/US-001-implementation-plan.md
    version: 2
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
  - path: docs/impact-analysis/US-001-impact-analysis.md
    version: 2
  - path: docs/decisions/US-001-open-decisions.md
    version: 2
supersedes: docs/reviews/plans/US-001-plan-review.md
critical_findings: 0
major_findings: 0
minor_findings: 4
---

# Plan Review — US-001 Customer Registration (v2)

## 1. Review Summary

**Verdict: PASS.** `docs/plans/US-001-implementation-plan.md` **v2** is safe,
complete, traceable, and executable. It implements exactly the approved
Specification v2, the approved API and database designs v2, the design review v2,
and the predicted impact surface v2, and introduces no new business behavior.

Plan v2 is a loop-back cascade re-issue from `RECONCILIATION` v3
(`specification_gap` / RC-9). Compared with v1 (which passed `PLAN_REVIEW` and
`HUMAN_PLAN_APPROVAL` on 2026-08-31), v2:

- refreshes every input reference to the all-v2 artifact chain;
- records the SC-4 "deny by default" wording alignment — **"deny by default"
  means authentication-required by default (`anyRequest().authenticated()`), not
  a literal `denyAll()`** — in the Goal, C-14, R-2, execution step 1, and the
  traceability table, matching `specification` v2 §7 SEC-1, `api_design` v2
  §6/§8, `openapi` v2 `x-auth-posture`, and `design_review` v2 D-10;
- closes the v1 F-1 finding: `open_decisions` is now v2 / `APPROVED` with
  OD-001..OD-006 `RESOLVED`.

**No plan task, file to create/modify, execution step, dependency, configuration
change, risk, or test changed between v1 and v2** — C-14 already carried the
correct SC-4 reading in v1. This review therefore re-affirms the v1 assessment
(full detail retained below) and updates the findings set.

- **Plan readiness:** ready for `HUMAN_PLAN_APPROVAL`.
- **Principal risks:** unchanged from v1 — the known Spring Boot 4 / H2 2.x
  integration trip points (R-1 `ddl-auto=validate` type match, R-2 Security
  filter-chain scope, R-3 72-byte BCrypt bound), each owned by IMPLEMENTATION /
  IMPLEMENTATION_VERIFICATION / SECURITY_REVIEW with a concrete mitigation.
- **Recommended next action:** proceed to `HUMAN_PLAN_APPROVAL`. The human
  re-confirms the one new dependency (`spring-boot-starter-validation`, mandated
  by AD-5) and notes the four Minor findings below, none of which block
  execution.

## 2. Reviewed Artifacts

| Artifact | Path | Version | Status |
|---|---|---|---|
| Implementation Plan | `docs/plans/US-001-implementation-plan.md` | 2 | DRAFT |
| Story | `docs/stories/US-001-register-customer.md` | (unversioned) | IN_PROGRESS |
| Specification | `docs/specifications/US-001-spec.md` | 2 | APPROVED — SPEC_REVIEW v2 PASS + HUMAN_SPEC_APPROVAL occ. 2 (front-matter reads DRAFT; design-review v2 D-11) |
| Specification Review | `docs/reviews/specifications/US-001-spec-review.md` | 2 | APPROVED (PASS) |
| API Design | `docs/designs/api/US-001-api-design.md` | 2 | APPROVED — DESIGN_REVIEW v2 PASS (front-matter DRAFT; D-11) |
| OpenAPI Contract | `docs/designs/api/US-001-openapi.yaml` | 2 | APPROVED — DESIGN_REVIEW v2 PASS |
| DB Design | `docs/designs/database/US-001-db-design.md` | 2 | APPROVED — DESIGN_REVIEW v2 PASS (front-matter DRAFT; D-11) |
| Entity Model | `docs/designs/database/US-001-entity-model.md` | 2 | APPROVED — DESIGN_REVIEW v2 PASS (front-matter DRAFT; D-11) |
| Design Review | `docs/reviews/designs/US-001-design-review.md` | 2 | APPROVED (PASS) |
| Impact Analysis | `docs/impact-analysis/US-001-impact-analysis.md` | 2 | DRAFT (PASS; no review stage follows IMPACT_ANALYSIS) |
| Open Decisions | `docs/decisions/US-001-open-decisions.md` | 2 | APPROVED (OD-001..OD-006 RESOLVED) |

Architecture / product references consulted: `architecture.md` (AD-1..AD-8),
`package-map.md`, `api-conventions.md` (AC-1..AC-9), `persistence-conventions.md`
(PC-1..PC-9), `security-conventions.md` (SC-1..SC-9 + policy block),
`business-rules.md` (BR-001..BR-007), `non-functional-requirements.md`
(NFR-001..NFR-008).

### Artifact chain / staleness

Plan v2's `inputs` front matter and its Source Artifacts table reference
specification v2, specification-review v2, api-design v2, openapi v2, db-design
v2, entity-model v2, design-review v2, impact-analysis v2, and open-decisions v2.
Every one is the current version; none is `SUPERSEDED` or `ARCHIVED`. No
downstream artifact records consuming an older upstream version. **Plan v2 is not
stale** — the v1 plan review (which reviewed plan v1 against the v1 chain) is the
stale artifact this review supersedes.

Front-matter note: specification v2, api_design v2, database_design v2, and
entity_model v2 carry `status: DRAFT` even though each cleared its review stage
(`SPEC_REVIEW` v2 PASS, `DESIGN_REVIEW` v2 PASS) and, for the specification,
`HUMAN_SPEC_APPROVAL` occurrence 2 (`history.jsonl` 2026-09-02T19:50:00Z). The
recorded review/gate decisions are authoritative; this is `design_review` v2
D-11, owned by spec-writer / openapi-designer / db-designer, with no plan or PR
impact. Not a `BLOCKED` condition — the protective invariant (a recorded PASS
review / human approval per gated input) is satisfied. Carried as a non-blocking
finding (F-6).

## 3. Strengths

Unchanged from v1:

- **Complete file-level decomposition** (C-1..C-17, M-1..M-4) with a
  Responsibility column and a Traceability column on every row.
- **Impact-Analysis reconciliation table** — every predicted file is created
  as-is or its consolidation/rename is explained (no `JacksonConfig`,
  `PasswordEncoder` bean in `SecurityConfig`, mapping in `CustomerService`,
  `FieldError` → `ApiFieldError`, no `local` profile). No silent scope change.
- **Planning decisions PD-1..PD-6** make the deferred items concrete with a
  rationale and a convention citation each.
- **Execution Order** — 14 ordered steps, each with an explicit observable
  completion criterion.
- **Validation Strategy** and **Testing Strategy** tables give deterministic
  pass criteria and defer the definitive suite to `test-writer`.
- **Risks section** carries all eight Impact-Analysis risks forward with a
  per-risk mitigation and an owner stage.
- **Scope discipline** — `GET /api/v1/customers/{id}`, login, and rate limiting
  are explicitly excluded (R-8).

New in v2:

- The SC-4 wording alignment is now stated in the plan itself (Goal, C-14 code
  comment requirement, R-2 mitigation, execution step 1), so IMPLEMENTATION and
  SECURITY_REVIEW have an unambiguous target and RC-9 cannot regress.

## 4. Scope Review

| Dimension | Assessment |
|---|---|
| Required scope | Fully covered. One endpoint `POST /api/v1/customers`; server-side email + password validation; case-insensitive duplicate → `409`; BCrypt hash; enabled `CUSTOMER` account; UTC audit timestamps; `201` + `Location` + credential-free body. |
| Missing scope | None. All FR-1..FR-11 and AC-001..AC-007 have a home in the file list and the execution order. |
| Scope expansion | None. No speculative abstraction, no mapper library, no extra endpoint, no `local` profile, no runtime OpenAPI serving. The v1→v2 delta adds only documentation. |
| Out-of-Scope compliance | Compliant. Spec §10 items (login, password reset, email verification, MFA, activation, profile, rate limiting, admin account management) are all absent. R-8 explicitly guards the `Location` target and a `UserDetailsService`. |

## 5. Requirements Traceability

| AC | Spec section | Design artifact | Impact Analysis | Plan step / files | Planned verification |
|---|---|---|---|---|---|
| AC-001 Successful registration | FR-1/FR-5/FR-8/FR-9, §5 | API §4 + OpenAPI `201`; DB §4, entity-model §4.1 | §7, §8, §16 | Steps 4/8/9; C-13, C-12, C-3, C-2, C-1, C-7, C-16 | web-layer (C-T4) + service (C-T3) + persistence (C-T2) + IT (C-T5) |
| AC-002 Unique email (case-insensitive) | FR-4, §6.1, §8 | API §4.3 `409`; DB §5 `uq_customer_email` | §7, §8 | Step 8; C-12, C-10, C-11, C-3, C-16 | service (C-T3) + IT (C-T5) + persistence (C-T2) |
| AC-003 Email validation | FR-3, §6.1 | OpenAPI `RegistrationRequest.email`; API §4.1 | §7 | Steps 6/9/11; C-6, C-11 | validation/web (C-T4) |
| AC-004 Password storage | FR-5/FR-6/FR-7, §7 | DB §4.2/§7; entity-model §4.1 | §8, §9 | Steps 8/10; C-12, C-14, C-2 | service (C-T3) + persistence (C-T2) |
| AC-005 Secure response | FR-7/FR-8, §7 | API §4.2 `CustomerResponse`; OpenAPI schema | §7, §9 | Steps 7/8; C-7, C-12 | web-layer + contract assertion (C-T4) |
| AC-006 Password policy | FR-3/FR-6, §6.2 | API §4.1; design-review D-1/D-6 | §7, §10 | Steps 6/8; C-4, C-5, C-12 | validation unit (C-T1, incl. multi-byte boundary) + web (C-T4) |
| AC-007 Media type | FR-2, §8 | OpenAPI `415`; API §4.3 | §7 | Steps 9/11; C-13 (`consumes`), C-11 | web-layer (C-T4) |
| Derived: unknown / malformed JSON | §6.3 | API §3, OpenAPI `additionalProperties: false` | §7 (derived), R-4 | Steps 3/11; M-2 (PD-1), C-17, C-11 | web-layer (C-T4) |
| NFR-4 / BR-007 explicit mapping + UTC audit | §9 NFR-4 | DB §4, entity-model §2/§3 | §8 | Steps 3/4; C-2, C-15, C-16 | persistence (C-T2) |
| SEC-1/SEC-2 / SC-4/SC-5 security posture | §7 SEC-1 (v2 wording) | API §6/§8; design-review v2 D-10 | §9 | Step 10; C-14 | security (C-T6) |

Every AC is covered by at least one file and one verification activity. No
orphan plan step. No unmet AC. The SEC-1 row now traces to the aligned v2
wording in every artifact.

## 6. Impact Analysis Coverage

Impact Analysis v2 kept the v1 change surface, module/package/file predictions,
API contract, persistence model, and risk set R-1..R-8 **unchanged** (the
v1→v2 cascade carries no functional impact). The plan v2 disposition is
therefore identical to v1:

| Impact Analysis item (confidence) | Plan disposition |
|---|---|
| All app packages are **Create** — HIGH | Covered — C-1..C-15 create exactly the `package-map.md` packages (AD-8, D-9). |
| `controller/CustomerController` — HIGH | Covered — C-13. |
| `service/CustomerService` — HIGH | Covered — C-12. |
| `repository/CustomerRepository` (`existsByEmail` / `findByEmail`) — HIGH | Covered — C-3 (both methods). |
| `model/entity/Customer` + `Role` — HIGH | Covered — C-2, C-1. |
| `model/request/RegistrationRequest` — HIGH | Covered — C-6. |
| `model/dto/CustomerResponse`, `ErrorResponse`, `FieldError` — HIGH | Covered — C-7, C-9, C-8 (`FieldError` → `ApiFieldError`, PD-5; serialized shape unchanged). |
| `validation/ValidPassword` + `PasswordPolicyValidator` — HIGH | Covered — C-4, C-5 (length in **bytes**, PD-2). |
| `security/SecurityConfig` + `PasswordEncoder` bean — HIGH | Covered — C-14 (both in one class, PD-4). |
| `exception/DuplicateEmailException` + handler — HIGH | Covered — C-10, C-11. |
| `config/JpaAuditingConfig` — HIGH | Covered — C-15 (`@EnableJpaAuditing` off the main class, AD-7; UTC `DateTimeProvider`). |
| `config/JacksonConfig` *(conditional)* — MEDIUM | **Not created** — replaced by `spring.jackson.deserialization.fail-on-unknown-properties: true` (PD-1). Justified difference. |
| `schema.sql` — HIGH | Covered — C-16 (DDL from DB design §8.1). |
| `src/test/resources/application-test.yaml` — MEDIUM | Covered — C-17. |
| `build.gradle.kts` add `spring-boot-starter-validation` — HIGH | Covered — M-1 (BOM-managed). |
| `application.yaml` datasource + JPA + naming + console off — HIGH | Covered — M-2. |
| `.gitignore` `/data/` — MEDIUM | Covered — M-3. |
| `CustomerPortalApplicationTests` `@ActiveProfiles("test")` — MEDIUM | Covered — M-4. |
| Risks R-1..R-8 | All carried into the plan's Risks section with mitigations + owner stages. |

No HIGH- or MEDIUM-confidence affected area is ignored. The two divergences
(no `JacksonConfig`, no `local` profile) are stated with justification and do
not change scope.

## 7. Architecture Review

| Check | Result |
|---|---|
| Layering `controller → service → repository → model.entity` (AD-2) | Pass — C-13 delegates to C-12; C-12 uses C-3; C-3 depends only on `Customer`. |
| Controller has no business logic, no repository access, no entity in a signature (AD-2, AD-4) | Pass — C-13 explicitly: "No error handling, no repository access, no entity in signature". |
| Service owns transactions (AD-3) | Pass — C-12 `@Transactional` on the public `register(...)` write method. |
| DTO / entity boundary (AD-4) | Pass — request binds to `model.request.RegistrationRequest`; responses are `model.dto` records; `Customer` never in a controller signature or a body; mapping in the service (PD-3). |
| Validation split (AD-5) | Pass — request-shape via Bean Validation on C-6 + custom `@ValidPassword` (C-4/C-5); business-rule (uniqueness) + password re-check in C-12 before persistence. |
| Single `@RestControllerAdvice` (AD-6, AC-9) | Pass — C-11 is the only advice; C-13 builds no error bodies; `DuplicateEmailException` (C-10) carries no HTTP concept. |
| Configuration boundaries (AD-7) | Pass — `JpaAuditingConfig` (C-15) in `config`; `SecurityConfig` (C-14) in `security`; settings in `application.yaml` / test profile. |
| Package ownership (`package-map.md`) | Pass — every new class lands in a mapped package; no feature package (D-9, AD-8). |
| Reuse over duplication (AD-8) | Pass — no mapper class, one `SecurityConfig` for both beans, `application.yaml` reused; the only new dependency is the AD-5-mandated first-party starter. |

No architecture finding.

## 8. API Review

| Check | Result |
|---|---|
| Contract alignment | Pass — plan targets the approved OpenAPI v2 operation `registerCustomer` verbatim; no invented behavior. Step 1 re-confirms the contract before coding. OpenAPI v2 changed only `info.version`, `x-source-specification-version`, and the `x-auth-posture` note — no endpoint/schema/status-code/validation/error-model/example change. |
| Status codes | Pass — `201` (C-13), `400` (C-11: `MethodArgumentNotValidException` / `HandlerMethodValidationException` / `HttpMessageNotReadableException`), `409` (C-11: `DuplicateEmailException`), `415` (C-11: `HttpMediaTypeNotSupportedException`; C-13 `consumes`), `500` (C-11 fallback, no leak). |
| Request / response models | Pass — `RegistrationRequest { email, password }` as a `record` (PD-1, no unknown-field annotation); `CustomerResponse { id, email, role, createdAt }` matches OD-004:A and the OpenAPI schema. |
| Validation behavior | Pass — `@NotBlank` + `@Email` + `@Size(max = 254)` on `email`; `@NotBlank` + `@ValidPassword` on `password`; policy re-checked in the service (FR-6). |
| Error mapping | Pass — all mapping in C-11; `ErrorResponse` maps to the AC-6 body; `ApiFieldError` serializes to the contract `FieldError` shape; messages never echo the submitted value (SC-9). |
| Auth / authorization | Pass — public, no authorization; CSRF exemption and the public matcher are both scoped to `POST /api/v1/customers` (C-14, OD-002:B, SC-5). C-14 now also requires a code comment stating that `anyRequest().authenticated()` **is** the SC-4 "deny by default" reading (not `denyAll()`), matching spec v2 §7 SEC-1 / api-design v2 §6/§8 / design-review v2 D-10. |
| Compatibility | Pass — purely additive; no existing contract to break (AC-1). |
| Planned contract tests | Pass — C-T4 covers `201` + `Location` + body, `400` for email and password, `415`, unknown field, malformed JSON; C-T5 end-to-end IT. |

See F-2 (unauthenticated response for protected routes) and F-3 (single advice
branch, two OpenAPI example messages) — both Minor, carried from v1.

## 9. Persistence Review

| Check | Result |
|---|---|
| Entity changes | Pass — one entity `Customer` (C-2) / table `customer`; `Role` enum (C-1); matches entity-model v2 §2 field-by-field (v2 changed no field/mapping/enum/invariant). |
| Explicit constraints / nullability / length | Pass — C-2 mandates explicit `@Column` on every field; `email` 254, `password_hash` 60, `role` 20; all `nullable = false`; `createdAt` `updatable = false`. |
| Uniqueness | Pass — table-level `@UniqueConstraint(name = "uq_customer_email", columnNames = "email")` + plain `UNIQUE` in `schema.sql`; case-insensitivity via service `toLowerCase(Locale.ROOT)` (OD-006:A). |
| Indexes | Pass — `uq_customer_email` serves the `email` lookup (PC-7); no redundant index; no FKs. |
| Schema initialization | Pass — hand-written `schema.sql` (C-16) from DB design §8.1; `spring.sql.init.mode=always` (main) / `embedded` (test); `ddl-auto=validate` in both profiles. No `create` / `update` shortcut (SC-8, PC-2). |
| Migration implications | None — new table, no data, no migration tool (PC-2). |
| Auditing | Pass — `@EntityListeners(AuditingEntityListener.class)` on C-2; `@EnableJpaAuditing` on C-15 with a UTC `DateTimeProvider` (BR-007, PC-6). |
| Persistence tests | Pass — C-T2 (`@DataJpaTest`, `test` profile) asserts column constraints, `uq_customer_email` collision, `EnumType.STRING`, UTC audit values, `created_at` not updatable, and `ddl-auto=validate` agreement. |

R-1 (`OffsetDateTime` ↔ `TIMESTAMP WITH TIME ZONE` strict match; H2 2.x IDENTITY
clause ordering) is gated at execution step 4 and owned by IMPLEMENTATION /
IMPLEMENTATION_VERIFICATION (PD-6). Acceptable — an execution-time integration
detail, not a plan defect.

## 10. Security Review

| Area | Result |
|---|---|
| Authentication boundary | Addressed — C-14 `SecurityFilterChain`: `requestMatchers(POST, "/api/v1/customers").permitAll()` + `anyRequest().authenticated()`, with an explicit code comment that this is the SC-4 "deny by default" reading (authentication-required by default, not `denyAll()`) per spec v2 §7 SEC-1 / api-design v2 §6/§8 / design-review v2 D-10. See F-2: the plan still does not fix the exact unauthenticated response for a protected route (401 vs form-login 302), which C-T6 asserts. |
| Authorization boundary | Addressed — none required for the operation (`x-authorization: none`); no other route added. |
| Password hashing | Addressed — `BCryptPasswordEncoder` bean in `security` (C-14, PD-4); no-op / plaintext encoder forbidden (SC-1, SEC-2); C-T6 asserts the encoder bean is present and not a no-op. |
| Password exposure | Addressed — `password` only on the inbound record; `toString()` on `Customer` excludes `passwordHash` (C-2); `CustomerResponse` has no credential field (C-7); service discards plaintext after `encode` (C-12). |
| Dual-layer policy | Addressed — `@ValidPassword` (C-4/C-5) at the request layer **and** a byte-length + char-class re-check in `CustomerService` before hashing (C-12, FR-6, PD-2). |
| Input validation | Addressed — server-side only (NFR-002); unknown fields rejected explicitly (PD-1). |
| Sensitive-data logging | Addressed — C-4/C-5 static generic message (no value echo, SC-9); C-11 fallback `500` leaks nothing; R-7 tracked. |
| H2 console | Addressed — `spring.h2.console.enabled=false` in `application.yaml` (M-2) and the test profile (C-17), every profile (SC-6, SEC-9). |
| Dev-only / insecure config | None — file H2 for local, isolated in-memory for tests; `ddl-auto=validate`; no permissive security rule. |
| Secret management | Addressed — no secret introduced or committed; `/data/` git-ignored (M-3); H2 `sa` / empty is the H2 default, not a secret (SEC-11). |
| Security tests | Addressed — C-T6: public path reachable unauthenticated, a second path still denied, CSRF exemption scoped to the one path. |

The Story handles passwords, credentials, and account state, and the plan
contains explicit security steps (execution step 10 + C-14 + C-4/C-5 + the
Validation Strategy "Credential safety" and "Security posture" rows). SEC review
requirement satisfied — no blocking security finding. Final verification of the
filter chain and the CSRF scope is owned by SECURITY_REVIEW (R-2). The RC-9
wording ambiguity that triggered this cascade is now closed in the plan text.

## 11. Testing and Validation Review

- **AC coverage:** every AC (§5 table) maps to at least one planned test level.
  The multi-byte password boundary vector (>72 bytes, ≤72 chars) is explicitly
  called out for C-T1 (R-3 / PD-2 / design-review D-6).
- **Test categories:** unit (validation), service slice, `@DataJpaTest`
  persistence, `@WebMvcTest` / full-slice web-layer, `@SpringBootTest` end-to-end
  IT, security, plus the `contextLoads` regression — matches NFR-005 and the
  Impact Analysis §10 prediction.
- **Negative scenarios:** invalid email, each missing password character class,
  length boundaries, duplicate email (same and different case), non-JSON
  `Content-Type`, unknown JSON field, malformed JSON, credential absent from the
  response — all listed.
- **Deterministic validation:** the Validation Strategy table gives an
  observable pass criterion per concern; execution step 13 requires
  `./gradlew clean build` green (NFR-7) and a clean `ddl-auto=validate` boot;
  MCP `idea-validation` / `idea-semantic-analysis` are named for
  IMPLEMENTATION_VERIFICATION.
- **Structure vs behavior:** the planned tests assert observable outcomes
  (status codes, headers, persisted values, hash verification), not
  implementation shape.
- **Ownership:** the plan states `test-writer` owns the definitive AC→test
  matrix at TEST_WRITING and that C-T1..C-T6 are indicative skeletons — it does
  not pre-empt that stage.
- **Missing evidence:** none blocking. See F-1 — some per-step completion
  criteria in steps 6–10 name assertions that only pass once the advice (step
  11) and security wiring (step 10) exist; the step-13 full build is the real
  gate.

## 12. Execution Order Review

The 14-step order is dependency-safe (unchanged from v1):

1–2. Contract confirmation, then the build dependency (M-1).
3. Persistence config + `schema.sql` + test profile + `.gitignore`.
4. Entity + repository + `Role` + JPA auditing — gated on a clean
`ddl-auto=validate` boot (closes R-1, R-6 here).
5. Test skeletons — red before implementation.
6–7. Validation constraint + request DTO, then domain exception + DTOs.
8. Service — needs the entity, repository, encoder, DTOs.
9. Controller — needs the service and DTOs.
10. Security wiring — needs the encoder bean location fixed (C-14).
11. Exception handler — consolidates all error mapping.
12. Adjust the smoke test (M-4).
13. Full `./gradlew clean build` + `validate` boot (NFR-7).
14. Documentation reconciliation prep.

This differs from the canonical guidance only by placing the exception handler
(step 11) after the controller (step 9) and security (step 10); the plan states
the reason (consolidate every error branch once the producing paths exist) and
the step-13 build is the gate. Acceptable. See F-1 for the per-step criteria
wording.

## 13. Reviewability

The change is one reviewable Pull Request: a single Gradle module, ~17 new files
+ 4 small modifications, one first-party dependency, one new table, one endpoint.
No unrelated module, no broad refactor, no multiple independent capabilities, no
discretionary third-party library. No decomposition needed. The v1→v2 delta adds
no files.

## 14. Findings

### F-1 — Per-step completion criteria in steps 6–10 reference tests that pass only after steps 10–11

- **Severity:** Minor (carried from v1 F-2)
- **Location:** plan "Execution Order" steps 6, 8, 9.
- **Problem:** e.g. step 9 lists "`415` … unknown field and malformed JSON →
  `400`" as its evidence, but those paths are only wired in step 11 (advice) and
  step 10 (security context for `@WebMvcTest`).
- **Why it matters:** read literally, a step cannot be "done" by its own
  criterion until later steps land; this can confuse progress tracking during
  IMPLEMENTATION.
- **Required correction:** the Planner may add one sentence that the per-step
  criteria are cumulative and the authoritative gate is step 13
  (`./gradlew clean build` green). No structural change needed.
- **Loop-back target:** `IMPLEMENTATION_PLANNING` (cosmetic; not required for
  approval).

### F-2 — C-14 does not specify the unauthenticated response for protected (non-registration) routes

- **Severity:** Minor (carried from v1 F-3)
- **Location:** plan C-14; execution step 10; C-T6.
- **Problem:** With `spring-boot-starter-security` on the classpath and a custom
  `SecurityFilterChain` that only sets `permitAll()` for the registration path
  and `anyRequest().authenticated()`, the default behavior for an unauthenticated
  request to another path is a `302` redirect to a generated login page, not a
  `401`. C-T6's evidence line ("an arbitrary second path … returns `401`") is
  only well-defined if the chain also configures an entry point (e.g. `httpBasic`,
  or `exceptionHandling` with an `HttpStatusEntryPoint(UNAUTHORIZED)`, or
  disables form login). The v2 SC-4 wording note does not resolve this — a `302`
  is still a denial, so it is not a scope defect, just an under-specified
  assertion.
- **Required correction:** state the intended unauthenticated response for
  protected routes in C-14 (recommend `401` via an `HttpStatusEntryPoint`,
  consistent with a JSON API), or defer the exact assertion to `test-writer` /
  SECURITY_REVIEW and soften C-T6's wording.
- **Loop-back target:** `IMPLEMENTATION_PLANNING` (small clarification; not
  required for approval — SECURITY_REVIEW (R-2) owns final verification).

### F-3 — One `HttpMessageNotReadableException` advice branch vs two distinct OpenAPI example messages

- **Severity:** Minor (carried from v1 F-4)
- **Location:** plan C-11 / PD-1; `US-001-openapi.yaml` `400` examples
  `unknownField` and `malformedJson`.
- **Problem:** PD-1 routes both malformed JSON and an unknown property through a
  single `HttpMessageNotReadableException` mapping, implying one `message`, while
  the contract illustrates two different messages.
- **Why it matters:** the OpenAPI `examples` are illustrative, not normative, and
  the AC-6 body **shape** is preserved either way — not a contract break — but
  IMPLEMENTATION_VERIFICATION should know the messages may be unified.
- **Required correction:** none required. If distinct messages are wanted, the
  advice can branch on `ex.getCause() instanceof UnrecognizedPropertyException`.
- **Loop-back target:** none (advisory).

### F-4 — New dependency confirmation

- **Severity:** Minor (advisory; already flagged by the plan — carried from v1 F-5)
- **Location:** M-1; plan "New Dependencies" and "Open Questions" §1.
- **Problem / why it matters:** `spring-boot-starter-validation` is not currently
  on the classpath. It is mandated by AD-5, is a first-party Spring Boot starter,
  and is version-managed by the existing 4.1.1 BOM — not discretionary — but
  adding any dependency is a `HUMAN_PLAN_APPROVAL` confirmation point.
- **Required correction:** none. The human confirms at the gate.
- **Loop-back target:** none.

### F-5 — (v1 F-1) `open_decisions.md` still marks OD-001..OD-006 `OPEN` — **RESOLVED in v2**

- **Status:** closed. `open_decisions.md` is now v2 / `APPROVED` with
  OD-001..OD-006 recorded `RESOLVED` (OD-001:A, OD-002:B, OD-003:A, OD-004:A,
  OD-005:A, OD-006:A) and "No `OPEN` decisions remain". No longer a finding.

### F-6 — Upstream v2 inputs carry front-matter `status: DRAFT` despite clearing their review/gate

- **Severity:** Minor (advisory; = `design_review` v2 D-11)
- **Location:** front matter of `specification` v2, `api_design` v2,
  `database_design` v2, `entity_model` v2.
- **Problem:** each reads `status: DRAFT` although `SPEC_REVIEW` v2 PASS +
  `HUMAN_SPEC_APPROVAL` occ. 2 (spec) and `DESIGN_REVIEW` v2 PASS (designs) are
  recorded in `history.jsonl`.
- **Why it matters:** a fresh reader could mistake these for un-reviewed drafts.
  The recorded review/gate decisions are authoritative; the invariant that
  protects a gated input (a recorded PASS review / human approval) is satisfied.
- **Required correction:** none by the Planner. Owners spec-writer /
  openapi-designer / db-designer should set `status: APPROVED`. No plan or PR
  impact.
- **Loop-back target:** none.

No `Critical` findings. No `Major` findings.

## 15. Open Decisions

**No blocking Open Decisions were identified.** OD-001..OD-006 are all `RESOLVED`
in `open_decisions.md` v2 (`APPROVED`) and applied consistently across every
upstream v2 artifact and this plan.

No unresolved `TODO` / `TBD` / `FIXME` / `???` / "to be decided" marker was found
in any `APPROVED` input artifact that would affect implementation. (Spec v2 §6.1
/ §6.2 retain parenthetical "draft:" wording next to resolved OD references and
§6.3 says "left to API_DESIGN" — presentation residue tracked as spec-review v2
F-1..F-7; the decisions are made and the plan implements the resolved outcomes,
so this does not block.)

## 16. Required Plan Changes

None are required before `HUMAN_PLAN_APPROVAL`. Optional clarity improvements the
Planner may fold into a revision (none blocks execution):

1. Add one sentence to the Execution Order noting that per-step completion
   criteria are cumulative and step 13 (`./gradlew clean build`) is the
   authoritative gate (F-1).
2. State the intended unauthenticated response for protected routes in C-14
   (recommend `401` via `HttpStatusEntryPoint`) so C-T6 has a fixed target, or
   soften C-T6's assertion and defer it to SECURITY_REVIEW (F-2).
3. Optionally note in C-11 whether the malformed-JSON and unknown-field `400`
   responses share one `message` or branch on the cause (F-3).

Separately (not a Planner action): spec-writer / openapi-designer / db-designer
should set the v2 specification and design artifacts' front-matter `status` to
`APPROVED` (F-6).

## 17. Verdict Rationale

Plan v2 has zero `Critical` and zero `Major` findings. It covers every
Acceptance Criterion with a planned file and a planned verification; it is
consistent with the approved Specification v2, the approved API and database
designs v2, the design review v2, and the predicted impact surface v2; it adds no
business behavior and no out-of-scope work; it complies with AD-2..AD-8,
`package-map.md`, `api-conventions.md`, `persistence-conventions.md`, and
`security-conventions.md`; its security handling is explicit and sufficient for a
Story that processes credentials, and it now records the SC-4 "deny by default" =
authentication-required-by-default reading that closes RC-9; its execution order
is dependency-safe with observable evidence per step and a deterministic
full-build gate; and the change is reviewable as a single Pull Request. The v1→v2
delta is documentation-only (input-reference refresh + SC-4 wording alignment) —
no plan task, file, step, dependency, configuration, risk, or test changed. The
four Minor findings are advisory and are carried as `non_blocking_findings`.

Per `stage-map.yaml`, `PLAN_REVIEW` with verdict `PASS` advances to
`HUMAN_PLAN_APPROVAL`. A `PASS` here is not human approval — a human records the
decision with `/so:approve` (or `/so:reject`) and re-confirms the new dependency
at that gate.

```yaml
result:
  verdict: PASS
  stage: PLAN_REVIEW
  story: US-001
  artifact_status: APPROVED
  artifacts:
    - docs/reviews/plans/US-001-plan-review.md
  next_stage: HUMAN_PLAN_APPROVAL
  loop_back_stage: null
  blocking_issues: []
  non_blocking_findings:
    - "F-1: Execution-order per-step completion criteria for steps 6-10 reference assertions (415, unknown-field/malformed-JSON 400) that only pass after steps 10-11; step 13 (./gradlew clean build) is the real gate. Add a note that criteria are cumulative. Loop-back IMPLEMENTATION_PLANNING (cosmetic)."
    - "F-2: C-14 does not specify the unauthenticated response for protected non-registration routes (401 vs form-login 302); C-T6 asserts 401. Planner should fix an entry point (recommend HttpStatusEntryPoint 401) or defer the assertion to SECURITY_REVIEW (R-2). The v2 SC-4 wording note does not resolve this."
    - "F-3: PD-1 maps malformed JSON and unknown-field both via one HttpMessageNotReadableException branch (one message); OpenAPI shows two distinct example messages. Examples are illustrative; AC-6 shape preserved. Branch on the cause if distinct messages are wanted. Advisory."
    - "F-4: New dependency spring-boot-starter-validation (M-1) is absent from build.gradle.kts; mandated by AD-5, first-party, BOM-version-managed. Re-confirm at HUMAN_PLAN_APPROVAL."
    - "F-5 (was v1 F-1): CLOSED — open_decisions.md is now v2/APPROVED with OD-001..OD-006 RESOLVED (OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A)."
    - "F-6 (= design_review v2 D-11): specification v2 / api_design v2 / database_design v2 / entity_model v2 carry front-matter status DRAFT though each cleared SPEC_REVIEW v2 / HUMAN_SPEC_APPROVAL occ.2 / DESIGN_REVIEW v2 (recorded in history.jsonl). Recorded decisions authoritative; owners spec-writer / openapi-designer / db-designer; no plan or PR impact."
    - "v2 is a loop-back cascade re-issue from RECONCILIATION v3 (specification_gap / RC-9). Input refs refreshed to the all-v2 chain; SC-4 'deny by default' = authentication-required by default (anyRequest().authenticated()), not literal denyAll() — now recorded in the plan Goal, C-14, R-2, execution step 1, traceability. NO plan task/file/step/dependency/config/risk/test change; plan v1 passed PLAN_REVIEW + HUMAN_PLAN_APPROVAL on 2026-08-31 and C-14 already carried the correct SC-4 reading."
    - "Carried: R-1 ddl-auto=validate vs OffsetDateTime<->TIMESTAMP WITH TIME ZONE + H2 2.x IDENTITY clause ordering (PD-6; execution step 4 gate; IMPLEMENTATION/IMPLEMENTATION_VERIFICATION own it)."
    - "Carried: R-2 Spring Security filter chain must scope the public matcher AND the CSRF exemption to POST /api/v1/customers and keep anyRequest().authenticated(); SECURITY_REVIEW verifies (C-T6)."
    - "Carried: R-3/PD-2 password 12..72 bound is UTF-8 BYTES in both the validator and the service re-check; C-T1 needs a multi-byte (>72 bytes, <=72 chars) boundary vector."
    - "Carried: R-5 M-4 adds @ActiveProfiles(\"test\") to CustomerPortalApplicationTests so contextLoads still boots with Security + JPA active."
    - "Carried: R-6 JPA auditing DateTimeProvider pinned to OffsetDateTime.now(ZoneOffset.UTC) in config (C-15), not the main application class (AD-7)."
    - "Carried: R-7 password constraint message is static/generic, never echoes the submitted value (SC-9); SECURITY_REVIEW checks."
    - "Carried: R-8 scope guard - GET /api/v1/customers/{id}, login, UserDetailsService, rate limiting all explicitly out of scope."
    - "Test skeletons C-T1..C-T6 are indicative; test-writer owns the definitive AC->test matrix at TEST_WRITING and may restructure them. The ac_test_matrix v1 half of the prior staleness waiver stays open until TEST_WRITING re-runs."
```
