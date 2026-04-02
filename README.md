# run-skill

Portable `run` session planning and execution for Claude Code and Codex.

This repo pulls the reusable part of a high-trust `/run` workflow into a standalone package that works in any repo. It keeps the `run session` workshop, the `blueprint.json` contract, and the portable runner surface for validate, launch, status, and resume.

What is included:
- `$run` / `$run session` planning flow
- `$run status`
- `$run resume`
- portable runner command: `run-skill`
- generic run artifacts: `session.md`, `blueprint.json`, `progress.md`, `run-state.json`, `events.jsonl`, `completion-summary.txt`, `completion-recap.md`

What is intentionally not included:
- overnight workflows
- local briefing publishing
- SMS notifications
- workspace-specific operating assumptions

## Install

Clone the repo somewhere stable, then run:

```bash
python3 scripts/install.py --host both
```

That installs:
- Codex skills into `~/.codex/skills/run` and `~/.codex/skills/_shared`
- Claude Code skills into `~/.claude/skills/run` and `~/.claude/skills/_shared`
- Claude Code command wrapper into `~/.claude/commands/run.md`
- runner shim into `~/.local/bin/run-skill`

If `~/.local/bin` is not on your `PATH`, add it:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Install options:

```bash
python3 scripts/install.py --host codex
python3 scripts/install.py --host claude
python3 scripts/install.py --host both --mode copy
python3 scripts/install.py --host both --force
```

Restart Claude Code or Codex after install so the new skill is picked up cleanly.

## Use

Inside any repo:

- Codex: `$run`
- Claude Code: `/run`

The session flow will usually propose a run folder under `./runs/<project-slug>/`.

When the package is locked, use the runner:

```bash
run-skill --validate ./runs/<project>/blueprint.json
run-skill --launch-mode standard ./runs/<project>/blueprint.json
run-skill --status ./runs/<project>/blueprint.json
run-skill --follow ./runs/<project>/blueprint.json
```

## Skill steps

Blueprint steps can route to installed skills with:

```json
{
  "tool": "skill:research-brief"
}
```

The runner looks for sibling skills in:
1. this repo's bundled `skills/`
2. extra roots from `RUN_SKILL_PATHS`
3. `~/.codex/skills`
4. `~/.claude/skills`

## Repo layout

```text
skills/
  _shared/
  run/
commands/
scripts/
```

`commands/run.md` exists so Claude Code gets a plain `/run` entrypoint after install.
