---
name: run
version: 1.0.0
description: |
  Project execution partner. Plan a substantial piece of work through a
  structured session workshop, then run it with a portable bash runner that
  routes each step to the right AI CLI tool or installed skill. Use for
  high-trust planning, run status checks, and resume/adjust flows that should
  work in any repo.
argument-hint: "[session | status | resume]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /run - Project Execution Partner

Plan ambitious work step by step, then execute it with the right AI tool or installed skill per step. The workshop builds the package; the runner does the work. Steps can invoke raw CLI tools (`claude-code`, `codex`, `gemini`) or installed skills through `skill:<name>`.

---

## Mode Routing

| Mode | Trigger | When | Node |
|------|---------|------|------|
| `session` | `/run` or `/run session` | Shape a high-trust, launch-ready run package | [[nodes/session.md]] |
| `status` | `/run status` | Check progress on a running project | [[nodes/status.md]] |
| `resume` | `/run resume` | Adjust and continue a stalled project | [[nodes/resume.md]] |

Default mode: `session`.

---

## Core Routing Rules

1. Load shared gates first:
   - [[../_shared/nodes/interaction-gates.md]]
   - [[../_shared/nodes/output-discipline.md]]
   - [[nodes/safety.md]]
2. Determine mode from the command argument. No argument means `session`.
3. All modes reference [[nodes/blueprint-schema.md]] for the `blueprint.json` contract.
4. Return the requested deliverable without auto-launching the run.

---

## Runner Handoff

After `session` or `resume` writes or updates `blueprint.json`, present these commands:

**Validate the package first**
```bash
run-skill --validate <path-to-blueprint.json>
```

**One-shot supervision summary**
```bash
run-skill --status <path-to-blueprint.json>
```

**Live follow surface**
```bash
run-skill --follow <path-to-blueprint.json>
```

`--follow` polls every 2 seconds by default. Override with `RUN_STATUS_POLL_SECONDS=<seconds>` when needed.

**Standard launch mode**
```bash
run-skill --launch-mode standard <path-to-blueprint.json>
```

**Adaptive launch mode**
```bash
run-skill --launch-mode adaptive <path-to-blueprint.json>
```

**Expansion launch mode**
```bash
run-skill --launch-mode expansion <path-to-blueprint.json>
```

**Legacy supervised compatibility**
```bash
run-skill --supervised <path-to-blueprint.json>
```

**Resume last blueprint path**
```bash
run-skill --resume-last
```

**Watch mode**
```bash
run-skill --watch <path-to-blueprint.json>
```

**Dry run**
```bash
run-skill --dry-run <path-to-blueprint.json>
```

**Autonomy profile override**
```bash
run-skill --autonomy-profile max <path-to-blueprint.json>
```

**Codex service-tier override**
```bash
run-skill --codex-service-tier fast <path-to-blueprint.json>
```

The shared operator contract for both Codex and Claude Code is `run-skill --status` and `run-skill --follow`. They read `run-state.json`, `events.jsonl`, `blockers.jsonl`, and step attempt logs first, then fall back to `progress.md` and `blockers.md` for older run directories.

When a run reaches terminal state, the runner writes both `completion-summary.txt` and `completion-recap.md` in the run directory. `completion-summary.txt` is the durable terminal snapshot. `completion-recap.md` is the operator-facing recap artifact to read first before briefing someone on the outcome.

Model defaults:
- Claude Code: `claude-opus-4-5`
- Codex: `gpt-5.4` with `xhigh` reasoning effort

Override those in `blueprint.json` with `defaults.models.*` or step-level fields.

---

## Node Map

- [[nodes/blueprint-schema.md]]
- [[nodes/safety.md]]
- [[nodes/session.md]]
- [[nodes/status.md]]
- [[nodes/resume.md]]

## Shared Dependencies

- [[../_shared/nodes/interaction-gates.md]]
- [[../_shared/nodes/output-discipline.md]]
