#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def ensure_installable(path: Path, force: bool, noun: str) -> None:
    if (path.exists() or path.is_symlink()) and not force:
        raise SystemExit(f"Refusing to overwrite existing {noun}: {path}")


def install_path(src: Path, dest: Path, mode: str, force: bool) -> None:
    if dest.exists() or dest.is_symlink():
        if not force:
            raise SystemExit(f"Refusing to overwrite existing path: {dest}")
        remove_existing(dest)

    dest.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        dest.symlink_to(src, target_is_directory=src.is_dir())
    else:
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() or path.is_symlink():
        if not force:
            raise SystemExit(f"Refusing to overwrite existing file: {path}")
        remove_existing(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Install run-skill for Codex and Claude Code.")
    parser.add_argument("--host", choices=["codex", "claude", "both"], default="both")
    parser.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    run_skill = repo_root / "skills" / "run"
    runner_script = repo_root / "skills" / "run" / "scripts" / "run.sh"

    home = Path.home()
    installs = []

    if args.host in {"codex", "both"}:
        codex_root = Path(os.environ.get("CODEX_HOME", home / ".codex")) / "skills"
        installs.append((run_skill, codex_root / "run"))

    if args.host in {"claude", "both"}:
        claude_root = home / ".claude"
        installs.append((run_skill, claude_root / "skills" / "run"))

    for _, dest in installs:
        ensure_installable(dest, args.force, "path")

    command_target = None
    if args.host in {"claude", "both"}:
        command_target = home / ".claude" / "commands" / "run.md"
        ensure_installable(command_target, args.force, "file")

    runner_target = home / ".local" / "bin" / "run-skill"
    ensure_installable(runner_target, args.force, "path")

    for src, dest in installs:
        install_path(src, dest, args.mode, args.force)

    if command_target is not None:
        command_body = f"Read and follow `{home / '.claude' / 'skills' / 'run' / 'SKILL.md'}`.\n"
        write_file(command_target, command_body, args.force)

    install_path(runner_script, runner_target, "symlink", args.force)
    runner_target.chmod(0o755)

    print("Installed run-skill.")
    print(f"Runner: {runner_target}")
    bin_dir = runner_target.parent
    if str(bin_dir) not in os.environ.get("PATH", "").split(":"):
        print(f"PATH note: add {bin_dir} to your PATH if run-skill is not found.")
    print("Restart Claude Code or Codex to pick up the new skill cleanly.")


if __name__ == "__main__":
    main()
