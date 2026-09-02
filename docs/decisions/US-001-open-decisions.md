---
artifact_type: open_decisions
story: US-001
version: 2
status: APPROVED
created_at: 2026-08-31T00:33:59Z
updated_at: 2026-09-02T13:14:34Z
produced_by: us-clarifier
inputs:
  - path: docs/stories/US-001-register-customer.md
    version: null
  - path: docs/workflow/history.jsonl
    version: null
supersedes: docs/decisions/US-001-open-decisions.md
---

# Open Decisions — US-001 Customer Registration

All six decisions below were **resolved by the human at `HUMAN_SPEC_APPROVAL`**
(`docs/workflow/history.jsonl`, event `2026-08-31T07:48:48Z`,
`from_stage: HUMAN_SPEC_APPROVAL`, `verdict: HUMAN_APPROVED`,
`comment: "OD-001:A OD-002:B OD-003:A OD-004:A OD-005:A OD-006:A"`).

This v2 records those resolutions. It does not create, change, or re-open any
decision — CLARIFICATION does not resolve Open Decisions; the human did, and this
artifact is now brought into line with the recorded outcome so it is not a stale
input to downstream stages or the Pull Request.

| id | Decision | Resolution | Chosen option |
|---|---|---|---|
| OD-001 | Email length limit and accepted format | **RESOLVED** | A |
| OD-002 | CSRF classification of the registration endpoint | **RESOLVED** | B |
| OD-003 | Duplicate-email response vs. account enumeration | **RESOLVED** | A |
| OD-004 | Fields returned in the successful `201` response body | **RESOLVED** | A |
| OD-005 | Anti-abuse controls on self-service registration (scope check) | **RESOLVED** | A |
| OD-006 | Email normalization mechanism at persistence | **RESOLVED** | A |

**No `OPEN` decisions remain.**

---

## OD-001 — Email length limit and accepted format

- **id:** OD-001
- **question:** What is the maximum stored length of a customer email, and what
  format rule accepts/rejects it (strict RFC 5321/5322, a pragmatic single-`@`
  pattern, or Bean Validation `@Email`)?
- **context:** AC-003 requires invalid email formats to be rejected with a
  validation error, but neither the Story nor the product docs define the rule.
  `persistence-conventions.md` PC-4 and NFR-004 require every `String` column to
  declare an explicit length, so a value must be chosen before DB_DESIGN. BR-002
  already fixes that comparison is case-insensitive.
- **affects:** SPECIFICATION, API_DESIGN, DB_DESIGN, TEST_WRITING
- **status:** RESOLVED
- **resolved_at:** 2026-08-31T07:48:48Z
- **resolved_by:** ayubutrym@gmail.com (HUMAN_SPEC_APPROVAL)
- **options:**
  - A. `@Email` (Jakarta) + max length 254 (RFC 5321 practical maximum).
  - B. Custom stricter regex (single `@`, non-empty local part, domain with a
    dot) + max length 254.
  - C. `@Email` + a shorter project cap (e.g. 190) to keep index size small.
- **decision:** **A** — `@Email` (Jakarta) validation with a 254-character
  `email` column (RFC 5321 practical maximum).
- **recommended (at CLARIFICATION, non-binding):** A.

---

## OD-002 — CSRF classification of the registration endpoint

- **id:** OD-002
- **question:** Is `POST /api/v1/customers` treated as a browser/session
  endpoint (CSRF token required) or as a stateless API endpoint (CSRF disabled
  for this path)?
- **context:** `security-conventions.md` SC-5 keeps CSRF enabled for
  browser/session endpoints (the MVP default) and states that disabling CSRF for
  a stateless API endpoint "requires an approved architecture decision recorded
  for that Story." Registration is unauthenticated and has no prior session, so
  the classification is genuinely undetermined and must be decided here.
- **affects:** SPECIFICATION, API_DESIGN, IMPLEMENTATION, SECURITY_REVIEW
- **status:** RESOLVED
- **resolved_at:** 2026-08-31T07:48:48Z
- **resolved_by:** ayubutrym@gmail.com (HUMAN_SPEC_APPROVAL)
- **options:**
  - A. Keep CSRF enabled globally; the registration form obtains a CSRF token
    first (consistent with the session-based MVP default).
  - B. Record an architecture decision exempting `POST /api/v1/customers` from
    CSRF as a stateless public endpoint.
- **decision:** **B** — `POST /api/v1/customers` is exempt from CSRF as a
  stateless public JSON endpoint; the exemption is scoped to that single path and
  recorded in API design §6 per SC-5. CSRF stays enabled everywhere else.
- **recommended (at CLARIFICATION, non-binding):** B.

---

## OD-003 — Duplicate-email response vs. account enumeration

- **id:** OD-003
- **question:** When registration uses an email that already exists, does the
  API return an explicit `409` "an account with this email already exists"
  message, or a response that does not disclose whether the email is registered?
- **context:** AC-002 requires the duplicate registration to be rejected and
  `api-conventions.md` AC-6 shows a `409` duplicate-email example. Separately
  SC-3 forbids account enumeration, but only in the scope of *failed
  authentication*. Whether that principle extends to registration is a policy
  choice the docs do not resolve.
- **affects:** SPECIFICATION, API_DESIGN, SECURITY_REVIEW, TEST_WRITING
- **status:** RESOLVED
- **resolved_at:** 2026-08-31T07:48:48Z
- **resolved_by:** ayubutrym@gmail.com (HUMAN_SPEC_APPROVAL)
- **options:**
  - A. Return `409 Conflict` with the explicit duplicate-email message from
    AC-6 (best UX, matches the documented example).
  - B. Return a neutral success-shaped response and send no account, hiding
    whether the email exists (strongest anti-enumeration).
  - C. `409` with a generic "registration could not be completed" message
    (compromise).
- **decision:** **A** — `409 Conflict` with the explicit duplicate-email message
  (`"An account with this email already exists."`). Account enumeration on a
  self-service registration form is accepted as low-risk for this training
  project.
- **recommended (at CLARIFICATION, non-binding):** A.

---

## OD-004 — Fields returned in the successful `201` response body

- **id:** OD-004
- **question:** Which customer fields does the `201 Created` registration
  response include in its body?
- **context:** `api-conventions.md` AC-4 requires `POST /collection` to return
  the "created resource body", and AC-005 states only what must be absent
  (password, password hash). The positive field list is undefined and
  `spec-writer` needs it to define the response DTO.
- **affects:** SPECIFICATION, API_DESIGN
- **status:** RESOLVED
- **resolved_at:** 2026-08-31T07:48:48Z
- **resolved_by:** ayubutrym@gmail.com (HUMAN_SPEC_APPROVAL)
- **options:**
  - A. `id`, `email`, `role`, `createdAt`.
  - B. `id`, `email` only.
  - C. `id`, `email`, `role`, `enabled`, `createdAt`.
- **decision:** **A** — the `201` body is `CustomerResponse { id, email, role,
  createdAt }`. No password, no password hash, no `enabled` / internal state.
- **recommended (at CLARIFICATION, non-binding):** A.

---

## OD-005 — Anti-abuse controls on self-service registration (scope check)

- **id:** OD-005
- **question:** Does US-001 include any rate limiting / abuse protection on the
  registration endpoint, or is that explicitly deferred?
- **context:** The Story enables self-registration "without administrator
  involvement" but the NFRs and the Out-of-Scope list are both silent on abuse
  protection. Recorded so the decision is explicit for `security-reviewer`.
- **affects:** SPECIFICATION, SECURITY_REVIEW
- **status:** RESOLVED
- **resolved_at:** 2026-08-31T07:48:48Z
- **resolved_by:** ayubutrym@gmail.com (HUMAN_SPEC_APPROVAL)
- **options:**
  - A. Out of scope for US-001; note as a follow-up.
  - B. In scope; add a basic per-IP rate limit.
- **decision:** **A** — rate limiting / anti-abuse is **out of scope** for
  US-001 and recorded as a follow-up. No AC or NFR requires it.
- **recommended (at CLARIFICATION, non-binding):** A.

---

## OD-006 — Email normalization mechanism at persistence

- **id:** OD-006
- **question:** How is case-insensitive uniqueness (BR-001 + BR-002) enforced in
  persistence — store the email lowercased, or store as entered with a
  functional / lower-case unique index?
- **context:** BR-002 already fixes the *requirement* (comparison is
  case-insensitive); only the storage mechanism is open, and it is a DB_DESIGN
  concern. Recorded so DB_DESIGN makes it explicitly rather than by default.
- **affects:** DB_DESIGN
- **status:** RESOLVED
- **resolved_at:** 2026-08-31T07:48:48Z
- **resolved_by:** ayubutrym@gmail.com (HUMAN_SPEC_APPROVAL)
- **options:**
  - A. Normalize to lowercase in the service before persisting; plain `UNIQUE`
    on the column.
  - B. Store as entered; enforce uniqueness with a lower-case/functional unique
    index.
- **decision:** **A** — the service normalizes the email
  (`trim().toLowerCase(ROOT)`) before the uniqueness check and before persisting;
  a plain `UNIQUE` constraint (`uq_customer_email`) backs it.
- **recommended (at CLARIFICATION, non-binding):** A.

---

## Change log

| Version | Date | Change |
|---|---|---|
| 1 | 2026-08-31 | Initial six Open Decisions recorded (all `OPEN`) at CLARIFICATION. |
| 2 | 2026-09-02 | Recorded the `HUMAN_SPEC_APPROVAL` resolutions (OD-001:A, OD-002:B, OD-003:A, OD-004:A, OD-005:A, OD-006:A); every decision `OPEN` → `RESOLVED`. No decision content changed. Published in response to the `HUMAN_PR_APPROVAL` rejection item requiring a non-stale Open Decisions artifact in the PR. |
