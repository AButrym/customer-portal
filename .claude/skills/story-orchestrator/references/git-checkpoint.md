# Git Checkpoints

Authoritative parameters: `docs/workflow/git-policy.yaml`. This file is the
procedure. Used by `start`, `continue`, `run`, `approve`, `reject`.

## When

After a transition is recorded in `workflow-state.yaml` + `history.jsonl`, if
the verdict is `PASS`, `NOT_APPLICABLE`, `CHANGES_REQUIRED`, `HUMAN_APPROVED`,
`HUMAN_REJECTED` or `ACTIVATED`. **Never** for `BLOCKED`, and never when the
allowlisted file set has no changes.

## Procedure

1. Confirm the current branch equals the story branch
   (`git-policy.yaml.story_branch.pattern`). If not → `BLOCKED`, no commit.
2. `git status --porcelain`. Partition changed/untracked files into:
   allowlisted · `ignored_paths` · unexpected.
   Allowlist = `checkpoint.allowlist` (always keys + outputs of the stage that
   just ran + gate `required_artifacts` for human decisions + `code_stages`
   globs), all resolved through `artifact-paths.yaml`.
3. Any unexpected file → do not commit, set `BLOCKED`, list the files, recommend
   removing/ignoring them or moving the change to a `chore/*` branch.
4. No allowlisted changes → no commit.
5. `git add -- <explicit allowlisted paths>` (never `-A`/`.`), then
   `git commit -m "<message template>"` with an optional ≤5-line body.
   Never `--no-verify`, `--amend`, push, rebase, reset, force.
6. If a hook rejects the commit: report the guardrail output, leave the tree
   as is, set `BLOCKED`. Do not bypass.
7. Report the short sha in the Orchestration / Run Result. Do not write the sha
   back into state files (it would dirty the tree right after committing);
   `git log --grep "<story_id>"` is the lookup.

A loop-back produces a new commit; history is never rewritten.
