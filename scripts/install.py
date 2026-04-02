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
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
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
    shared_skill = repo_root / "skills" / "_shared"
    runner_script = repo_root / "skills" / "run" / "scripts" / "run.sh"

    home = Path.home()
    installs = []

    if args.host in {"codex", "both"}:
        codex_root = Path(os.environ.get("CODEX_HOME", home / ".codex")) / "skills"
        installs.extend(
            [
                (run_skill, codex_root / "run"),
                (shared_skill, codex_root / "_shared"),
            ]
        )

    if args.host in {"claude", "both"}:
        claude_root = home / ".claude"
        installs.extend(
            [
                (run_skill, claude_root / "skills" / "run"),
                (shared_skill, claude_root / "skills" / "_shared"),
            ]
        )

    for src, dest in installs:
        install_path(src, dest, args.mode, args.force)

    if args.host in {"claude", "both"}:
        command_target = home / ".claude" / "commands" / "run.md"
        command_body = f"Read and follow `{home / '.claude' / 'skills' / 'run' / 'SKILL.md'}`.\n"
        write_file(command_target, command_body, args.force)

    bin_dir = home / ".local" / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    runner_target = bin_dir / "run-skill"
    install_path(runner_script, runner_target, "symlink", args.force)
    runner_target.chmod(0o755)

    print("Installed run-skill.")
    print(f"Runner: {runner_target}")
    if str(bin_dir) not in os.environ.get("PATH", "").split(":"):
        print(f"PATH note: add {bin_dir} to your PATH if run-skill is not found.")
    print("Restart Claude Code or Codex to pick up the new skill cleanly.")


if __name__ == "__main__":
    main()
