#!/usr/bin/env python3
"""Append ONE validated event to docs/workflow/history.jsonl.

Deterministic writer for story-orchestrator (the only caller). It removes the
hand-written parts of a history event: the timestamp (runtime UTC clock), the
`attempt` number (derived from history), JSON formatting and schema checks.
It does NOT edit workflow-state.yaml, commit, or decide routing.

Schema: docs/workflow/state-schema.md. Routing: docs/workflow/stage-map.yaml.

Examples:
  record_transition.py --from SPEC_REVIEW --to HUMAN_SPEC_APPROVAL \
      --skill spec-verifier --verdict PASS \
      --artifact docs/reviews/specifications/US-001-spec-review.md
  record_transition.py --from HUMAN_SPEC_APPROVAL --to API_DESIGN \
      --verdict HUMAN_APPROVED --decided-by "name (email)" --comment "ok"
  record_transition.py ... --dry-run     # print the event, write nothing

Exit codes: 0 ok, 2 validation error (nothing written).
Prints the written event as one JSON line on stdout.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

STAGE_VERDICTS = {"PASS", "CHANGES_REQUIRED", "BLOCKED", "NOT_APPLICABLE"}
MARKER_VERDICTS = {"ACTIVATED", "HUMAN_APPROVED", "HUMAN_REJECTED", "ARCHIVED"}
FORWARD = {"PASS", "NOT_APPLICABLE"}
MAX_COMMENT = 300
SECRET_RE = re.compile(
    r"(password\s*[:=]|passwd\s*[:=]|secret\s*[:=]|api[_-]?key\s*[:=]|"
    r"authorization:\s*bearer|ghp_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY)",
    re.I,
)


def fail(msg):
    print(f"record_transition: {msg}", file=sys.stderr)
    sys.exit(2)


def project_root():
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(env) if env else Path(__file__).resolve().parents[4]


def load_stage_map(root):
    """Return (stage_order, stages) ; stages is None if PyYAML is unavailable."""
    path = root / "docs" / "workflow" / "stage-map.yaml"
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # optional

        data = yaml.safe_load(text)
        return list(data["stage_order"]), data.get("stages", {})
    except ImportError:
        m = re.search(r"^stage_order:\s*\n((?:\s+-\s+\S+\s*(?:#.*)?\n)+)", text, re.M)
        if not m:
            fail("cannot parse stage_order from stage-map.yaml")
        order = re.findall(r"-\s+(\S+)", m.group(1))
        return order, None


def read_history(path):
    events = []
    if not path.exists():
        return events
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            fail(f"history.jsonl line {n} is not valid JSON; refusing to append")
    return events


def read_state_story(root):
    p = root / "docs" / "workflow" / "workflow-state.yaml"
    try:
        m = re.search(r"^story:\s*(\S+)", p.read_text(encoding="utf-8"), re.M)
        return m.group(1) if m else None
    except OSError:
        return None


def parse_decisions(items):
    out = {}
    for it in items or []:
        if "=" not in it:
            fail(f"--decision expects OD-001=A, got {it!r}")
        k, v = it.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--story", help="default: story in workflow-state.yaml")
    ap.add_argument("--from", dest="from_stage", help="canonical stage, omit for ACTIVATED")
    ap.add_argument("--to", dest="to_stage", required=True)
    ap.add_argument("--skill", help="omit for human gates / activation")
    ap.add_argument("--verdict", required=True, choices=sorted(STAGE_VERDICTS | MARKER_VERDICTS))
    ap.add_argument("--artifact", action="append", default=[], help="relative path; repeatable")
    ap.add_argument("--comment", help=f"max {MAX_COMMENT} chars; detail belongs in the artifact")
    ap.add_argument("--decided-by", help="required for HUMAN_APPROVED / HUMAN_REJECTED")
    ap.add_argument("--decision", action="append", help="OD-001=A (CLARIFICATION PASS only); repeatable")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    root = project_root()
    hist_path = root / "docs" / "workflow" / "history.jsonl"
    order, stages = load_stage_map(root)

    story = a.story or read_state_story(root)
    if not story:
        fail("story unknown: pass --story or initialise workflow-state.yaml")

    # --- stage / verdict validation -----------------------------------------
    for label, val in (("--from", a.from_stage), ("--to", a.to_stage)):
        if val is not None and val not in order:
            fail(f"{label} {val!r} is not a canonical stage (stage-map.yaml stage_order)")
    if a.verdict == "ACTIVATED":
        if a.from_stage not in (None, "BACKLOG_SYNC"):
            fail("ACTIVATED must have no --from (or BACKLOG_SYNC)")
        if a.skill:
            fail("ACTIVATED has no skill")
    elif not a.from_stage:
        fail("--from is required")

    if a.verdict in {"HUMAN_APPROVED", "HUMAN_REJECTED"}:
        if a.skill:
            fail("human decisions have no skill")
        if not a.decided_by:
            fail("--decided-by is required for human decisions")
        if stages and stages.get(a.from_stage, {}).get("type") != "human_gate":
            fail(f"{a.from_stage} is not a human_gate")
        if a.verdict == "HUMAN_REJECTED" and not a.comment:
            fail("HUMAN_REJECTED requires --comment (the reason)")
    elif a.verdict in STAGE_VERDICTS and not a.skill:
        fail("stage verdicts require --skill")

    if stages and a.verdict in STAGE_VERDICTS:
        spec = stages.get(a.from_stage, {})
        if spec.get("skill") and spec["skill"] != a.skill:
            fail(f"{a.from_stage} is owned by {spec['skill']}, not {a.skill}")
        if a.verdict in FORWARD and a.to_stage != spec.get("next"):
            fail(f"{a.verdict} from {a.from_stage} must go to {spec.get('next')}, not {a.to_stage}")
        if a.verdict == "NOT_APPLICABLE" and not spec.get("optional"):
            fail(f"{a.from_stage} is not optional; NOT_APPLICABLE not allowed")
        if a.verdict == "CHANGES_REQUIRED" and a.to_stage not in (spec.get("loop_back") or {}).values():
            fail(f"{a.to_stage} is not a loop_back target of {a.from_stage}")
        if a.verdict == "BLOCKED" and a.to_stage != a.from_stage:
            fail("BLOCKED holds the stage: --to must equal --from")
    elif stages and a.verdict == "HUMAN_APPROVED":
        want = stages[a.from_stage].get("on_approve")
        if a.to_stage != want:
            fail(f"approve from {a.from_stage} must go to {want}")
    elif stages and a.verdict == "HUMAN_REJECTED":
        want = stages[a.from_stage].get("on_reject")
        if a.to_stage != want:
            fail(f"reject from {a.from_stage} must go to {want}")

    decisions = parse_decisions(a.decision)
    if decisions and not (a.from_stage == "CLARIFICATION" and a.verdict == "PASS"):
        fail("--decision is only valid for CLARIFICATION PASS")
    if a.from_stage == "CLARIFICATION" and a.verdict == "PASS" and not decisions:
        fail("CLARIFICATION PASS requires --decision OD-xxx=<option> for every Open Decision")

    # --- hygiene -------------------------------------------------------------
    if a.comment and len(a.comment) > MAX_COMMENT:
        fail(f"--comment is {len(a.comment)} chars (max {MAX_COMMENT}); move detail into the artifact")
    for text in [a.comment or "", a.decided_by or ""] + a.artifact:
        if SECRET_RE.search(text):
            fail("possible secret detected in event text; not written")
    for p in a.artifact:
        if os.path.isabs(p) or ".." in Path(p).parts:
            fail(f"artifact path must be repo-relative: {p}")
        if not a.dry_run and not (root / p).exists():
            fail(f"artifact does not exist: {p}")

    # --- attempt: occurrence number of the executing stage in history -------
    history = read_history(hist_path)
    if history and history[-1].get("story") not in (None, story) and a.verdict != "ACTIVATED":
        fail(f"last history event belongs to {history[-1].get('story')}, not {story}")
    prior = sum(
        1
        for e in history
        if e.get("story") == story and e.get("from_stage") == a.from_stage
        and e.get("verdict") not in {"BLOCKED"}
    )
    attempt = prior + 1

    event = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "story": story,
        "from_stage": a.from_stage,
        "to_stage": a.to_stage,
        "skill": a.skill,
        "verdict": a.verdict,
        "artifacts": a.artifact,
        "attempt": attempt,
    }
    if a.decided_by:
        event["decided_by"] = a.decided_by
    if decisions:
        event["decisions_resolved"] = decisions
    if a.comment:
        event["comment"] = a.comment

    line = json.dumps(event, ensure_ascii=False)
    if not a.dry_run:
        hist_path.parent.mkdir(parents=True, exist_ok=True)
        needs_nl = hist_path.exists() and hist_path.stat().st_size > 0 and not hist_path.read_bytes().endswith(b"\n")
        with open(hist_path, "a", encoding="utf-8", newline="\n") as f:
            f.write(("\n" if needs_nl else "") + line + "\n")
    print(line)


if __name__ == "__main__":
    main()
