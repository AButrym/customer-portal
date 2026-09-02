---
artifact_type: specification_review
story: US-001
version: 2
status: APPROVED
created_at: 2026-09-02T17:00:00Z
updated_at: 2026-09-02T17:00:00Z
produced_by: spec-verifier
inputs:
  - path: docs/stories/US-001-register-customer.md
    version: null
  - path: docs/specifications/US-001-spec.md
    version: 2
  - path: docs/decisions/US-001-open-decisions.md
    version: 2
  - path: docs/evidence/US-001-clarification-report.md
    version: 2
  - path: docs/product/business-rules.md
    version: null
  - path: docs/product/business-glossary.md
    version: null
  - path: docs/product/non-functional-requirements.md
    version: null
  - path: docs/architecture/api-conventions.md
    version: null
  - path: docs/architecture/security-conventions.md
    version: null
  - path: docs/architecture/persistence-conventions.md
    version: null
supersedes: docs/reviews/specifications/US-001-spec-review.md
---

# Specification Review — US-001 Customer Registration (v2)

## Summary

**Verdict: PASS.** Specification v2 supersedes v1 with a single, tightly scoped
change: the SEC-1 row in §7 now states that "deny by default" means
*authentication-required by default* per `security-conventions.md` SC-4
(`anyRequest().authenticated()`), not a literal `denyAll()`. Input references
were refreshed to `clarification_report` v2 and `open_decisions` v2, and a change
log (§13) was added. No functional requirement, validation rule, error-handling
rule, API contract, acceptance criterion, or traceability entry changed between
v1 and v2.

The Specification remains complete, internally consistent, fully traceable to the
Story and the product/architecture conventions, and expressed in testable terms.
There are no `Critical` or `Major` findings. The v1 review's six `Minor` findings
(F-1..F-6) are unchanged and still advisory; one new `Minor` finding (F-7) covers
residual "draft" hedging language now that OD-001..OD-006 are resolved. None
block progression to `HUMAN_SPEC_APPROVAL`.

## Reviewed Artifacts

| Artifact | Path | Version |
|---|---|---|
| Story | `docs/stories/US-001-register-customer.md` | (unversioned input) |
| Specification | `docs/specifications/US-001-spec.md` | 2 (DRAFT) |
| Open Decisions | `docs/decisions/US-001-open-decisions.md` | 2 (APPROVED) |
| Clarification Report | `docs/evidence/US-001-clarification-report.md` | 2 (APPROVED) |
| Prior review (superseded) | `docs/reviews/specifications/US-001-spec-review.md` | 1 |

Precondition check: Specification v2 exists, is not `SUPERSEDED`, and its `inputs`
front matter references the current `clarification_report` (v2) and
`open_decisions` (v2). The `story` input is unversioned per the
`artifact-schema.md` Story-artifact exception. Not stale — review is not
`BLOCKED`.

## What Changed in v2 (delta review)

| Location | v1 | v2 | Assessment |
|---|---|---|---|
| §7 SEC-1 | "every other endpoint remains deny-by-default." | adds: 'Here "deny by default" means **authentication-required by default** per SC-4 (`anyRequest().authenticated()`) — not a literal `denyAll()`.' | **Accurate.** Matches `security-conventions.md` SC-4 verbatim in intent ("every endpoint requires authentication unless the approved API design lists it as public"). Resolves the RC-9 / SR-1 / MF-a wording ambiguity on the Specification side. |
| Front matter `inputs` | clarification_report v1, open_decisions v1 | clarification_report v2, open_decisions v2 | Correct; both upstreams are now at v2 and APPROVED. |
| §13 Change log | absent | added, records the v1→v2 delta and the OD resolutions | Good practice; content matches `history.jsonl`. |

The git-level diff (per the SPECIFICATION stage report: 14 insertions / 7
deletions, one file) is consistent with the above. No other section of the
Specification was touched.

## Completeness

| Area | Present | Location |
|---|---|---|
| Business goal | Yes | §2, cites `product-vision.md` and Story Business Value |
| Business flow | Yes | §3 |
| Functional requirements | Yes | §4, FR-1..FR-11 |
| Acceptance Criteria | Yes | §5, AC-001..AC-007 |
| Validation rules (server-side) | Yes | §6.1 email, §6.2 password, §6.3 request shape |
| Security requirements | Yes | §7, SEC-1..SEC-11, each cited to SC-* or an OD |
| Error handling | Yes | §8, status/`error`/body table via single `@RestControllerAdvice` |
| Non-functional requirements | Yes | §9, NFR-1..NFR-8 mapped to source NFRs |
| Out of scope | Yes | §10 |
| Open Decisions with impact | Yes | §11 |
| Traceability | Yes | §12.1–§12.3 |
| Change log | Yes | §13 (new in v2) |

No mandatory section is missing. The password policy (12–72, upper/lower/digit/
special) matches `security-conventions.md` SC-1 exactly. The success path
(BCrypt hash, `CUSTOMER` role, `enabled = true`, UTC audit timestamps,
`201` + `Location`, safe response body) is fully specified.

## Consistency

- **Story vs Specification** — consistent. Story AC-001..AC-005 map to Spec
  AC-001..AC-005 (§12.2); AC-006 (password-policy enforcement) and AC-007
  (media-type enforcement) are correctly labelled derived. Story Out-of-Scope
  items all reappear in §10.
- **Business rules vs Specification** — consistent. BR-001/BR-002 (unique,
  case-insensitive email) → §6.1 + FR-4; BR-003 (one account per customer) →
  FR-4; BR-006 (`CUSTOMER` default role) → FR-5/SEC-5; BR-007 (UTC timestamps)
  → FR-5/NFR-4.
- **Architecture conventions vs Specification** — consistent. `api-conventions.md`
  AC-1/AC-3 (`/api/v1/customers`, plural noun) → FR-1; AC-4 (`201` + `Location`
  + body) → FR-8; AC-5 (`400`/`409`/`415`) → §8; AC-6 (error body + `fieldErrors[]`)
  → FR-3/§8; AC-9 (single `@RestControllerAdvice`) → FR-10.
- **SC-4 wording (the v2 change)** — now consistent with
  `security-conventions.md` SC-4. SC-4 defines deny-by-default as "every endpoint
  requires authentication unless the approved API design lists it as public".
  The v2 SEC-1 note makes the Specification say exactly this rather than implying
  a literal `denyAll()` posture the codebase does not (and per SC-4 should not)
  implement. This aligns the Specification with `SecurityConfig`
  (`anyRequest().authenticated()` + the single permitted public path) and with
  `implementation_verification` v2 / `security_review` v2.
- **Open Decisions vs Specification** — all six OD resolutions
  (OD-001:A, OD-002:B, OD-003:A, OD-004:A, OD-005:A, OD-006:A) match the "draft"
  assumptions already embedded in the Specification requirements. No requirement
  needs a value change; see F-7 on the residual "draft" labelling.
- **Glossary terminology** — unchanged from v1; "Customer" / "Registration" /
  "Role" used consistently. The entity-name nuance ("Customer" vs glossary
  "Account") is still carried as F-6.
- No contradictions found.

## Traceability

Unchanged from v1 and re-verified against Specification v2 §12.1–§12.3:

| AC | FR(s) | Rule(s) | Testable outcome |
|---|---|---|---|
| AC-001 | FR-1, FR-5, FR-8, FR-9 | SEC-5; §6.1/§6.2 valid path | `201`, `Location` header, account with `CUSTOMER` role |
| AC-002 | FR-4 | §6.1 uniqueness; SEC-8; §8 | duplicate rejected (`409`, per OD-003:A), no 2nd account |
| AC-003 | FR-3 | §6.1 format + length | `400` + `fieldErrors[].field="email"`, no account |
| AC-004 | FR-5, FR-6, FR-7 | SEC-2, SEC-4; PC-9 | stored value is a BCrypt hash in `password_hash` |
| AC-005 | FR-7, FR-8 | SEC-3, SEC-4 | response body excludes password and hash |
| AC-006 | FR-3, FR-6 | §6.2 policy | `400` + `fieldErrors[].field="password"`, no account |
| AC-007 | FR-2 | §8 `415` row | `415`, no account |

No orphan requirement; no unmet Story AC. Requirement → source mapping (§12.3)
checks out against the cited documents.

## Security

All security requirements in §7 cite `security-conventions.md` (SC-1, SC-2,
SC-4, SC-5, SC-6, SC-7, SC-8, SC-9) or an Open Decision (OD-002, OD-003). None
are invented. The v2 change strengthens the security section by removing the
`denyAll()` ambiguity in SEC-1: the authentication posture is now stated in the
same terms as SC-4. Credential handling (BCrypt, plaintext only on the inbound
DTO, hash never returned), CSRF exemption scoped to the single public path
(OD-002:B, recorded per SC-5), the accepted account-enumeration exposure of the
`409` duplicate-email response (OD-003:A / SEC-8), and error/log hygiene
(SC-9, no stack traces / SQL / class names) are all stated. `spring.h2.console.enabled=false`
(SEC-9 / SC-6) and `ddl-auto` restricted to `validate`/`none` (SEC-10 / SC-8)
are preserved. No new security requirement is introduced by v2.

## Open Decisions

| OD | Resolution (open_decisions v2) | Reflected in Spec v2 | Impact documented |
|---|---|---|---|
| OD-001 email length + format | A — `@Email` + 254 | §6.1 (draft label — F-7), §11 | Yes |
| OD-002 CSRF classification | B — exempt the single path | FR-11, SEC-7, §11 | Yes |
| OD-003 duplicate-email response | A — `409` + explicit message | FR-4, §6.1, §8, SEC-8, §11 | Yes |
| OD-004 `201` body fields | A — `id, email, role, createdAt` | FR-8, §11 | Yes |
| OD-005 anti-abuse scope | A — out of scope | §7, §10, §11 | Yes |
| OD-006 email normalization | A — normalize in service + plain `UNIQUE` | §6.1 note, §11 | Yes (DB_DESIGN) |

All six Open Decisions are represented, and every resolved value matches the
draft assumption already written into the Specification. `open_decisions` v2 is
APPROVED and records the `HUMAN_SPEC_APPROVAL` resolution (2026-08-31). Because
every resolution equals the embedded draft, no requirement value is wrong; the
only residual is presentation (F-7).

## Findings

| # | Severity | Finding | Suggested handling |
|---|---|---|---|
| F-1 | Minor | AC-007 is annotated "derived (AC-2, `api-conventions.md`)". "AC-2" can be misread as Story AC-002; the intended reference is `api-conventions.md` AC-2 plus Clarification assumption A-2. | §12.2 already clarifies it. Optional cleanup on a future revision. Not blocking. |
| F-2 | Minor | §6.3 defers unknown/extra JSON field handling ("reject 400" vs "ignore") to API_DESIGN without an Open Decision entry. | Acceptable as an explicit design-stage deferral; API_DESIGN should record the choice. |
| F-3 | Minor | FR-2 couples two distinct failures — missing `Content-Type` (`415`) and body shape (`email`/`password` only). | Optionally split request-shape validation into §6.3 for a cleaner TEST_WRITING mapping. |
| F-4 | Minor | SEC-4 / §12.3 cite `persistence-conventions.md` PC-9 (`password_hash VARCHAR(60)`) early. Verified accurate against PC-9. | No change needed; DB_DESIGN owns the final column definition. |
| F-5 | Minor | §6.2 states the password max length as 72 "characters"; BCrypt's limit is 72 bytes. | TEST_WRITING / IMPLEMENTATION treat as 72 bytes. Not a spec defect. |
| F-6 | Minor | The Specification names the persisted entity "Customer"; `business-glossary.md` reserves "Account" for the credential representation. | Entity/table naming is a DB_DESIGN decision. `docs/designs/database/US-001-db-design.md` §3 and `US-001-entity-model.md` explicitly document the entity `Customer` / table `customer` as embodying both glossary concepts (Customer + Account) for US-001, with DESIGN_REVIEW confirmation recorded. No spec change needed. |
| F-7 | Minor (new in v2) | OD-001..OD-006 are now RESOLVED (`open_decisions` v2), but the Specification body still labels dependent values as "draft" (e.g. FR-4 "governed by OD-003 (draft: `409 Conflict`…)", §6.1 "OD-001 (draft: 254 characters)"). Every "draft" value equals the resolved choice, so no behavior is wrong; the wording is now stale. §11 and §13 acknowledge the resolutions. | Advisory only. spec-writer may drop the "draft:" qualifier and cite the resolution on a future revision. Downstream artifacts (API design, DB design, tests, implementation) already consume the resolved values, so this does not affect correctness or the PR. Not blocking. |

No `Critical` findings. No `Major` findings.

## Verdict

**PASS** — Specification v2 is implementation-ready and may proceed to
`HUMAN_SPEC_APPROVAL`. The v2 change (SC-4 wording clarification) is accurate and
resolves the Specification half of RC-9 / security_review v2 SR-1 /
implementation_verification v2 MF-a. Seven `Minor` findings (F-1..F-7) are
advisory and carried as `non_blocking_findings`. A `PASS` here is not human
approval; a human re-confirms the Specification at the approval gate.

```yaml
result:
  verdict: PASS
  stage: SPEC_REVIEW
  story: US-001
  artifact_status: APPROVED
  artifacts:
    - docs/reviews/specifications/US-001-spec-review.md
  next_stage: HUMAN_SPEC_APPROVAL
  loop_back_stage: null
  blocking_issues: []
  non_blocking_findings:
    - "F-1: AC-007 annotation \"AC-2\" is ambiguous with Story AC-002; means api-conventions.md AC-2."
    - "F-2: §6.3 defers unknown-JSON-field handling to API_DESIGN without an Open Decision entry."
    - "F-3: FR-2 bundles Content-Type (415) and body-shape rules; body-shape rule only in prose."
    - "F-4: PC-9 password_hash VARCHAR(60) cited early; DB_DESIGN owns the final column definition."
    - "F-5: §6.2 password max 72 'characters' vs BCrypt's 72-byte input limit; treat as bytes downstream."
    - "F-6: entity named 'Customer' vs business-glossary 'Account'; db-design §3 / entity-model document the Customer/customer choice as embodying both glossary concepts for US-001. No spec change needed."
    - "F-7: Spec v2 still labels OD-001..OD-006 dependent values 'draft' though open_decisions v2 marks them RESOLVED; every draft value equals the resolved choice, so no behavior is wrong (presentation only)."
```
