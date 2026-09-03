#!/usr/bin/env python3
"""Synchronize or drift-check the portable Wingman skill set."""

from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import sys
import tempfile
from pathlib import Path


IGNORED_NAMES = {".DS_Store", "__pycache__"}


def discover_skills(repo_root: Path) -> tuple[str, ...]:
    return tuple(
        path.name
        for path in sorted(repo_root.iterdir(), key=lambda item: item.name)
        if path.is_dir() and (path / "SKILL.md").is_file()
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Synchronize or compare Wingman skills at explicit Codex/Claude destinations."
    )
    parser.add_argument("action", choices=("sync", "check"))
    parser.add_argument("--codex-dir", type=Path)
    parser.add_argument("--claude-dir", type=Path)
    args = parser.parse_args()
    if not args.codex_dir and not args.claude_dir:
        parser.error("pass --codex-dir, --claude-dir, or both")
    return args


def managed_entries(root: Path) -> dict[str, tuple[str, int | None]]:
    entries: dict[str, tuple[str, int | None]] = {}
    if not root.is_dir():
        return entries
    for current, directories, files in os.walk(root):
        directories[:] = sorted(name for name in directories if name not in IGNORED_NAMES)
        for name in directories:
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            entries[relative] = ("symlink" if path.is_symlink() else "directory", None)
        for name in sorted(files):
            if name in IGNORED_NAMES:
                continue
            path = Path(current) / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                entries[relative] = ("symlink", None)
            else:
                entries[relative] = ("file", path.stat().st_mode & 0o777)
    return entries


def compare_skill(source: Path, destination: Path) -> list[str]:
    if not destination.is_dir():
        return ["missing skill directory"]
    source_entries = managed_entries(source)
    destination_entries = managed_entries(destination)
    differences: list[str] = []
    for relative in sorted(source_entries.keys() - destination_entries.keys()):
        differences.append(f"missing {relative}")
    for relative in sorted(destination_entries.keys() - source_entries.keys()):
        differences.append(f"extra {relative}")
    for relative in sorted(source_entries.keys() & destination_entries.keys()):
        source_kind, source_mode = source_entries[relative]
        destination_kind, destination_mode = destination_entries[relative]
        if source_kind != destination_kind:
            differences.append(f"type differs {relative}")
            continue
        if source_mode != destination_mode:
            differences.append(f"mode differs {relative}")
        if source_kind == "file" and not filecmp.cmp(
            source / relative, destination / relative, shallow=False
        ):
            differences.append(f"content differs {relative}")
    return differences


def sync_skill(source: Path, destination_root: Path) -> None:
    destination_root.mkdir(parents=True, exist_ok=True)
    if not destination_root.is_dir():
        raise RuntimeError(f"destination is not a directory: {destination_root}")
    destination = destination_root / source.name
    if destination.resolve() == source.resolve():
        raise RuntimeError(f"source and destination skill are the same directory: {source}")
    stage_parent = Path(tempfile.mkdtemp(prefix=".wingman-skills-stage-", dir=destination_root))
    stage = stage_parent / source.name
    backup = destination_root / f".{source.name}.wingman-skills-backup"
    try:
        shutil.copytree(source, stage, ignore=shutil.ignore_patterns(*IGNORED_NAMES))
        if backup.exists():
            raise RuntimeError(f"stale backup blocks safe update: {backup}")
        if destination.exists():
            destination.rename(backup)
        try:
            stage.rename(destination)
        except Exception:
            if backup.exists() and not destination.exists():
                backup.rename(destination)
            raise
        if backup.exists():
            shutil.rmtree(backup)
    finally:
        shutil.rmtree(stage_parent, ignore_errors=True)


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    skills = discover_skills(repo_root)
    if not skills:
        raise RuntimeError(f"no skills found under {repo_root}")
    targets = []
    for label, target in (("codex", args.codex_dir), ("claude", args.claude_dir)):
        if target is not None:
            resolved = target.expanduser().resolve()
            if (label, resolved) not in targets:
                targets.append((label, resolved))

    drift_found = False
    for label, target in targets:
        for skill in skills:
            source = repo_root / skill
            if not (source / "SKILL.md").is_file():
                raise RuntimeError(f"invalid source skill: {source}")
            if args.action == "sync":
                sync_skill(source, target)
                print(f"synced {label}: {skill}")
                continue
            differences = compare_skill(source, target / skill)
            if differences:
                drift_found = True
                for difference in differences:
                    print(f"drift {label}: {skill}: {difference}")
            else:
                print(f"exact {label}: {skill}")
    return 1 if drift_found else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError) as error:
        print(f"sync-skills: {error}", file=sys.stderr)
        raise SystemExit(2)
