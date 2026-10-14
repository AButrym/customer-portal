---
artifact_type: security_review
story: US-001
version: 3
status: APPROVED
created_at: 2026-09-02T15:34:00Z
updated_at: 2026-10-14T15:05:00Z
produced_by: security-reviewer
inputs:
  - path: docs/stories/US-001-register-customer.md
    version: null
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
  - path: docs/verification/US-001-implementation-verification.md
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

# Security Review — US-001 Customer Registration (v3, re-run against the v2 input chain)

Supersedes v2 (recorded v1 upstream inputs, implementation_report v2, verification v2). v1/v2 remain in git history.

## 1. Executive Summary

**Verdict: PASS.** No Critical or Major security risk. Every control in Specification §7 is independently observable in code, configuration and tests exercising the real `SecurityFilterChain`.

- **Source unchanged:** `src/**` and `build.gradle.kts` are byte-identical to commit `6c7d9e8` (the code v2 reviewed); the v2 cascade re-versioned artifacts only. Build/test evidence is reused from `implementation_verification` v3 (clean test, 67/67), since no tracked source changed after it.
- **Closed since v2:** **SR-1** (RC-9 documentation half) — the SC-4 clarification ("deny by default" = authentication-required by default, `anyRequest().authenticated()`, not literal `denyAll()`) is now published in `US-001-spec.md` SEC-1 / change-log v2 and `US-001-api-design.md` §6/§8 v2.
- **Open:** 3 Minor (SR-2, SR-3 carried; SR-6 new), 2 Informational (SR-4, SR-5 carried). None requires a code change for this Story.
- **Next:** `RECONCILIATION`.

## 2. Reviewed Artifacts

Exact versions are in the front matter `inputs`. Spec/API/DB/entity v2 carry front-matter `DRAFT` with recorded PASS reviews and `HUMAN_SPEC_APPROVAL` (carried waiver, design_review D-11 / plan_review F-6; no security impact). `specification_review`, `design_review`, `plan_review`, `open_decisions` v2 are `APPROVED`; `implementation_verification` v3 verdict PASS. `HUMAN_SPEC_APPROVAL` and `HUMAN_PLAN_APPROVAL` (occ. 2) recorded in history. No consumed input is SUPERSEDED.

## 3. Security-Relevant Scope

- **Exposed:** `POST /api/v1/customers` (public, unauthenticated). All other routes: authentication required.
- **Assets:** plaintext password (request boundary only), BCrypt hash (`password_hash VARCHAR(60)`), email, id, role, enabled flag.
- **Trust boundaries:** client → controller; service → repository; application → file-based H2.

## 4. Environment and Tools

Spring Boot 4.x, toolchain Java 21, Gradle 9.7.1, H2. Profile `test` uses isolated in-memory H2; default profile file-based H2. Review by file inspection, grep, git, and reused Gradle evidence (`TEXT_FALLBACK`). No application server was started; no penetration testing; no dependency vulnerability scan.

## 5. Authentication Review

Login/session are out of scope for US-001 (Story Out Of Scope). Registration creates an `enabled=true` `CUSTOMER` account with a BCrypt hash, which supports later authentication (AC-001). `httpBasic`/`formLogin`/`logout` are disabled; unauthenticated access to protected routes returns `401` via `HttpStatusEntryPoint` (`protectedRouteReturns401WhenUnauthenticated`). No findings.

## 6. Authorization Review

`SecurityConfig`: `requestMatchers(POST /api/v1/customers).permitAll()`, `anyRequest().authenticated()` (SC-4, SEC-1). The matcher is an exact method+URI match. Role is set server-side (`Role.CUSTOMER`); `RegistrationRequest` has only `email`/`password` and `fail-on-unknown-properties: true`, so a client cannot submit `role`/`enabled` (mass-assignment closed). CSRF remains enabled globally and is exempted only for this endpoint per **OD-002:B** (human-approved architecture decision satisfying SC-5). No findings.

## 7. Password and Credential Handling

- `PasswordEncoder` bean = `BCryptPasswordEncoder` (SC-1), not a no-op.
- Policy 12–72 **UTF-8 bytes**, upper/lower/digit/special, enforced by `@ValidPassword` and re-checked in `CustomerService` before hashing or repository access.
- Persisted only as hash; no password column (`noPlaintextPasswordColumnExists`); BCrypt format asserted in `CustomerServiceTest`.
- `RegistrationRequest.toString()` masks the password; `Customer.toString()` excludes the hash; no `src/main` logging statements exist (grep for `log.`/`logger`/`System.out` empty).
- Validation message is constant and never echoes the submitted value. No findings.

## 8. Sensitive Data Exposure

`CustomerResponse` = `id, email, role, createdAt` only; entity never crosses the controller boundary; `successResponseNeverExposesCredentialOrInternalState` asserts absence of password, hash, `enabled`, `updatedAt`. `GlobalExceptionHandler` returns generic client-safe messages; unmapped exceptions → generic 500 with no internal detail. No findings.

## 9. Input Validation

`spring-boot-starter-validation` present; `@Valid @RequestBody` active at runtime (400 tests). Email: `@NotBlank @Email @Size(max=254)`; normalised lowercase/trim in service (OD-006:A). Malformed JSON and unknown fields → single generic 400; missing/non-JSON content type → 415. Boundary tests include the 73-byte/27-char multi-byte case. No findings.

## 10. API Security

Only the approved endpoint exists; contract statuses 201/400/409/415/500 match the implementation. 409 uses the OD-003:A message (account enumeration is the human-accepted behaviour, OD-003:A). See SR-2 (non-normative example wording).

## 11. Persistence Security

`schema.sql` (hand-maintained): `email VARCHAR(254) NOT NULL` + `uq_customer_email`, `password_hash VARCHAR(60) NOT NULL`, role check constraint, explicit lengths; `ddl-auto: validate` in main and test; schema verified against the live H2 information schema in `CustomerSchemaTest` (10). Duplicate race handled by mapping only `uq_customer_email` violations to 409 (see SR-3). `/data/` is git-ignored; `./data/` not present in the tree.

## 12. H2 and Application Configuration

`spring.h2.console.enabled: false` (main and test); `/h2-console` not exposed (`h2ConsoleIsNotExposed`). No `ddl-auto` of `update/create*`. `open-in-view: false`. See SR-4/SR-5 (Informational). No secrets in `application*.yaml`.

## 13. Logging and Telemetry

Application code logs nothing. Harness hook `.claude/hooks/log-tool.py` records metadata plus a `response_head` (first 200 chars of the tool response) — see SR-6. `docs/hooks/tool-usage.jsonl` is git-ignored (root-anchored pattern) and was not committed.

## 14. Dependencies

`build.gradle.kts` dependencies: data-jpa, security, validation, webmvc, H2 (runtime), Lombok (annotation processor), and matching test starters — consistent with the approved plan (validation starter confirmed at HUMAN_PLAN_APPROVAL occ.2). No dependency vulnerability scan was performed; no claim of vulnerability-freedom is made.

## 15. Security Test Coverage

| Requirement | Test |
|---|---|
| SEC-1 public registration, others authenticated | `registrationEndpointIsReachableWithoutAuthentication`, `protectedRouteReturns401WhenUnauthenticated` |
| OD-002:B CSRF exemption only on registration | `registrationPostIsAcceptedWithoutACsrfToken` (see SR-2 note on the CSRF-elsewhere gap) |
| SC-6 H2 console | `h2ConsoleIsNotExposed` |
| SC-1 hashing / no plaintext | `happyPathCreatesAnEnabledCustomerWithABcryptHash`, `noPlaintextPasswordColumnExists`, `passwordHashColumnIsVarchar60NotNull` |
| SC-1 no secret in render | `RegistrationRequestTest` (3) |
| AC-005 response minimisation | `successResponseNeverExposesCredentialOrInternalState` |
| Password policy and bytes boundary | 8 web + 17 validator tests |
| SC-9 no echo of submitted value | `passwordValidationMessageDoesNotEchoTheSubmittedValue` |
| AC-002 duplicate incl. race | web, schema and 2 service tests |

Security tests run through the real filter chain, not mocks.

## 16. Abuse Case Review

| Scenario | Protection | Evidence | Status |
|---|---|---|---|
| Repeated/case-variant duplicate registration | pre-check + unique constraint | web + schema + service tests | Mitigated |
| Concurrent duplicate | constraint race → 409 | service test | Mitigated |
| Oversized email / password | `@Size(254)`, 72-byte cap | web tests | Mitigated |
| Submit `role`/`enabled`/extra fields | unknown-field rejection, server-set role | config + 400 behaviour | Mitigated |
| Response inspection for secrets | DTO whitelist | AC-005 test | Mitigated |
| Rate limiting / anti-abuse | OD-005:A resolved (out of scope for this Story) | open_decisions v2 | Accepted by human decision |

## 17. Repository Hygiene

Tracked `.mcp.json` carries `GITHUB_PERSONAL_ACCESS_TOKEN` as a placeholder/reference (no literal token-like value; value not reproduced here). No `.env`, key, or `*.mv.db` file is tracked. `/data/` and `/docs/hooks/tool-usage.jsonl` are ignored. One untracked stray path exists: see SR-6.

## 18. Deviations

None between approved security requirements and implementation. SC-4 wording alignment is complete in code, spec v2 and API design v2.

## 19. Findings

### SR-1 — CLOSED
RC-9 documentation half: SC-4 clarification now present in `US-001-spec.md` (SEC-1, change-log v2) and `US-001-api-design.md` (§6, §8, change-log v2). No residual.

### SR-2 — Minor (API_SECURITY / TEST_COVERAGE), carried
- **Observed:** implemented 415/combined-400 `message` strings differ from the OpenAPI illustrative `examples`; and "CSRF enforced everywhere else" cannot be asserted because US-001 adds no second writable endpoint.
- **Assessment:** examples are non-normative, body shape preserved, messages are more generic; the CSRF-elsewhere assertion belongs to the first Story adding a writable protected endpoint. No risk.
- **Correction:** none required (optional `openapi-designer` example alignment). **Loop-back:** none.

### SR-3 — Minor (PERSISTENCE / ERROR_HANDLING), carried
- **Observed:** `CustomerService.isEmailUniquenessViolation` falls back to a message-substring match on `uq_customer_email`.
- **Assessment:** practically unreachable false positive (other constraints cannot be tripped by user input); worst case a real integrity error shows as 409 instead of 500, with no data exposure.
- **Correction:** none; optional hardening to constraint-name-only matching. **Loop-back:** none.

### SR-4 — Informational (CONFIGURATION), carried
Default-profile H2 URL uses `AUTO_SERVER=TRUE` with user `sa` and an empty password. Acceptable for the training project; future H2 credential hardening via externalised config (SC-7). Not a US-001 requirement.

### SR-5 — Informational (CONFIGURATION), carried
Datasource credentials are literal in `application.yaml` (empty password, no real secret). Same future hardening as SR-4.

### SR-6 — Minor (LOGGING / REPOSITORY_HYGIENE), new
- **Observed:** untracked `src/main/docs/hooks/tool-usage.jsonl` (1 metadata-only line, no credentials) exists in the working tree. `.claude/hooks/log-tool.py` writes to the **relative** path `docs/hooks/tool-usage.jsonl`, so a tool call made while the shell's working directory was `src/main` created `src/main/docs/`. The ignore rule `/docs/hooks/tool-usage.jsonl` is root-anchored and does not cover it. This is the same defect class as earlier RC-10 / D-2. The hook also stores `response_head` (first 200 chars of tool responses), which SC-9 prefers to be metadata only.
- **Risk:** the stray file could be swept into the PR (`git add -A`) and would reintroduce a non-Story path under `src/`; `response_head` could in principle capture a credential-bearing tool response.
- **Required correction (human / harness, not Story code):** delete `src/main/docs/`; make the hook resolve `$CLAUDE_PROJECT_DIR` and drop `response_head` (or redact). This review did not delete the file.
- **Loop-back:** none; **Reconciliation/PR-prep must exclude `src/main/docs/` from the candidate file list.**

## 20. Positive Controls (independently observed)

BCrypt encoder; policy enforced in two layers; hash-only persistence with explicit column lengths and DB uniqueness; response DTO whitelist; masked `toString()`; generic error bodies; exact-match public route with `anyRequest().authenticated()`; CSRF exemption scoped to one endpoint per OD-002:B; H2 console disabled and untested-exposed; `ddl-auto: validate`; server-side role/enabled; unknown-field rejection; git-ignored data directory; security tests through the real filter chain.

## 21. Open Decisions

No blocking security Open Decisions were identified. OD-001..OD-006 are RESOLVED in `open_decisions` v2.

## 22. Review Limitations

- No IDEA semantic/PSI analysis (`TEXT_FALLBACK`).
- No running-server or penetration testing; runtime evidence is the reused 67-test suite.
- No dependency vulnerability scan.
- Telemetry reviewed from the hook script and one local log line only.

## 23. Verdict Rationale

`implementation_verification` v3 is PASS; no Critical/Major findings; security-sensitive ACs (AC-001, AC-002, AC-004, AC-005) are verified with tests passing; no unresolved security Open Decision; source is unchanged since the prior reviewed commit and consistent with the v2 chain → `PASS`, advance to `RECONCILIATION`.
