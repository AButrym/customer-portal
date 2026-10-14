#!/usr/bin/env python3
"""PostToolUse telemetry hook: appends one metadata-only record per tool call.

Writes <project root>/docs/hooks/tool-usage.jsonl (schema 2). Never stores
prompt text, tool input/response content, commands, paths or skill args
(security-conventions.md SC-9). Never blocks a tool call: any error exits 0.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def size(value):
    return len(json.dumps(value, ensure_ascii=False, default=str).encode("utf-8"))


def read_workflow(project_dir):
    """Return (story, stage) from workflow-state.yaml, or (None, None)."""
    try:
        text = (project_dir / "docs" / "workflow" / "workflow-state.yaml").read_text(encoding="utf-8")
    except OSError:
        return None, None
    story = re.search(r"^story:\s*(\S+)", text, re.M)
    stage = re.search(r"^current_stage:\s*(\S+)", text, re.M)
    return (story.group(1) if story else None, stage.group(1) if stage else None)


def relative_cwd(project_dir, cwd):
    try:
        return Path(cwd).resolve().relative_to(project_dir.resolve()).as_posix() or "."
    except (ValueError, OSError, TypeError):
        return None


def is_success(response):
    if isinstance(response, dict):
        if response.get("is_error") or response.get("error"):
            return False
        if response.get("success") is False:
            return False
        if "interrupted" in response and response.get("interrupted"):
            return False
    return True


def main():
    payload = json.load(sys.stdin)

    project_dir = Path(
        os.environ.get("CLAUDE_PROJECT_DIR")
        or Path(__file__).resolve().parents[2]
    )

    tool_input = payload.get("tool_input", payload.get("inputs"))
    tool_response = payload.get("tool_response", payload.get("response"))
    tool_name = payload.get("tool_name", payload.get("tool", "UNKNOWN"))
    tool_input = tool_input if tool_input is not None else {}

    mcp_server = mcp_tool = skill = None
    if tool_name.startswith("mcp__"):
        parts = tool_name.split("__", 2)
        mcp_server = parts[1] if len(parts) > 1 else None
        mcp_tool = parts[2] if len(parts) > 2 else None
        category = mcp_server if mcp_server in ("idea", "github") else "mcp_other"
    elif tool_name == "Skill":
        category = "skill"
        if isinstance(tool_input, dict):
            skill = tool_input.get("skill")
    else:
        category = "builtin"

    in_size = size(tool_input)
    out_size = size(tool_response)
    story, stage = read_workflow(project_dir)

    entry = {
        "schema": 2,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "session_id": payload.get("session_id"),
        "tool_use_id": payload.get("tool_use_id"),
        "tool": tool_name,
        "category": category,
        "mcp_server": mcp_server,
        "mcp_tool": mcp_tool,
        "skill": skill,
        "success": is_success(tool_response),
        "story": story,
        "stage": stage,
        "cwd_rel": relative_cwd(project_dir, payload.get("cwd")),
        "input_size_bytes": in_size,
        "response_size_bytes": out_size,
        "total_size_bytes": in_size + out_size,
        "input_keys": list(tool_input.keys()) if isinstance(tool_input, dict) else [],
        "response_type": type(tool_response).__name__ if tool_response is not None else "None",
    }

    log_file = project_dir / "docs" / "hooks" / "tool-usage.jsonl"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
