# run-skill

`run` is a planning-and-execution skill for bigger pieces of work.

You use it when a task is too large, fuzzy, or high-stakes for a single prompt. Instead of throwing one giant instruction at an AI tool, `run` helps you shape the work into a clear execution package, then hands that package to a portable runner that can execute, monitor, and resume it.

The result is a repeatable workflow:

1. Plan the work in a guided session.
2. Lock the plan into a structured package.
3. Launch it with the runner.
4. Check progress, inspect blockers, and resume when needed.

This repo is designed to work as a standalone product. If you can install a skill in Claude Code or Codex and run a shell command, you can use it.

## What It Does

`run` gives you three user-facing modes:

- `run session`: turn a goal into a launch-ready run package
- `run status`: inspect a run that is active, blocked, or complete
- `run resume`: adjust a run and continue it after a blocker or pause

It also ships a companion CLI:

- `run-skill --validate`: verify a package before launch
- `run-skill --launch-mode ...`: execute the package
- `run-skill --status`: print a one-shot status summary
- `run-skill --follow`: stay attached to live progress
- `run-skill --watch`: open a light supervision loop
- `run-skill --dry-run`: inspect what would run without executing it

## Who It Is For

`run` is useful when you want an AI tool to handle a project with multiple steps, dependencies, and checkpoints.

Good fits:

- research and synthesis projects
- implementation plans that require several passes
- content or document production with review stages
- repo work that needs discovery, edits, validation, and recap
- anything you want to supervise without micromanaging every prompt

Bad fits:

- tiny one-shot tasks
- casual brainstorming
- work where a normal direct prompt is already enough

## How It Works

The workflow has two layers.

### 1. Planning layer

Inside Claude Code or Codex, you start with:

```text
/run
```

or:

```text
$run
```

The skill walks through the project with you, asks for clarification where it matters, and writes a run package to a folder like:

```text
./runs/<project-slug>/
```

That folder typically contains:

- `session.md`: the human-readable planning record
- `blueprint.json`: the structured execution contract
- `progress.md`: the durable progress log

### 2. Execution layer

Once the package is approved, you use the runner:

```bash
run-skill --validate ./runs/<project>/blueprint.json
run-skill --launch-mode standard ./runs/<project>/blueprint.json
```

The runner executes each step in order, records progress, and writes machine-readable and human-readable artifacts as it goes.

## Install

Clone this repo somewhere stable, then run:

```bash
python3 scripts/install.py --host both
```

That installs:

- the `run` skill into `~/.codex/skills/` for Codex
- the `run` skill into `~/.claude/skills/` for Claude Code
- a Claude Code command wrapper at `~/.claude/commands/run.md`
- a `run-skill` shim in `~/.local/bin`

The installer only manages `run`-owned paths. It does not claim or overwrite a host-level `~/.codex/skills/_shared` or `~/.claude/skills/_shared`.

If `~/.local/bin` is not already on your `PATH`, add it:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Other install variants:

```bash
python3 scripts/install.py --host codex
python3 scripts/install.py --host claude
python3 scripts/install.py --host both --mode copy
python3 scripts/install.py --host both --force
```

Restart Claude Code or Codex after install so the skill is discovered cleanly.

## First Use

Start in any project directory where you want the work to happen.

In Codex:

```text
$run
```

In Claude Code:

```text
/run
```

The skill will help you define:

- what the project is
- what success looks like
- what is out of scope
- what steps need to happen
- which tool should handle each step
- which launch mode fits the work

When the package is ready, it will hand you the exact commands to validate and launch it.

## Launch Modes

`run-skill` supports three main launch modes.

- `standard`: execute the approved plan and stop on failure or blocker
- `adaptive`: keep the same scope, but allow bounded recovery and retries
- `expansion`: adaptive behavior plus bounded step creation during execution

Most teams should start with `standard` unless the work clearly benefits from controlled autonomy.

## Run Artifacts

Each run lives in its own folder. Beyond the core planning files, the runner may create:

- `launch.json`
- `run-state.json`
- `events.jsonl`
- `blockers.md`
- `blockers.jsonl`
- `completion-summary.txt`
- `completion-recap.md`
- `handoff/`
- `logs/steps/...`

You do not need to read all of these manually. In normal use:

- `session.md` is the planning record
- `progress.md` is the narrative log
- `run-skill --status` is the fastest way to inspect state
- `completion-recap.md` is the best first read after a run finishes

## Checking Progress

To inspect a run:

```bash
run-skill --status ./runs/<project>/blueprint.json
```

To stay attached while it runs:

```bash
run-skill --follow ./runs/<project>/blueprint.json
```

To watch the run with a lighter supervision surface:

```bash
run-skill --watch ./runs/<project>/blueprint.json
```

## Resuming a Run

If a run stops, you can reopen it through the skill:

```text
/run resume
```

or:

```text
$run resume
```

That flow helps you review blockers, adjust the plan, update `blueprint.json`, and re-emit the next launch command.

You can also resume from the CLI:

```bash
run-skill --resume-last
```

## Tool Routing

Each step in a run can route to a specific execution tool.

Built-in tool targets include:

- `claude-code`
- `codex`
- `gemini`
- `skill:<name>`

That means a run can mix direct CLI execution and installed skills. For example, one step might use Codex for implementation, another might use Claude Code for synthesis, and another might invoke a separate installed skill.

## Skill-Based Steps

Blueprint steps can reference another installed skill like this:

```json
{
  "tool": "skill:research-brief"
}
```

The runner looks for skills in this order:

1. this repo's bundled `skills/`
2. extra roots from `RUN_SKILL_PATHS`
3. `~/.codex/skills`
4. `~/.claude/skills`

This lets you build runs that depend on shared team skills without hardcoding a single workspace layout.

## Repo Layout

```text
skills/
  run/
    _shared/
commands/
scripts/
```

## Mental Model

If you are using `run` for the first time, think of it this way:

- the skill is the planner
- `blueprint.json` is the contract
- the runner is the operator
- the run folder is the project record

You do not have to learn the full schema up front. Start with `/run` or `$run`, approve the package, and let the system generate the structure for you.
