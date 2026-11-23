#!/usr/bin/env python3
"""Render, check and safely install the pinned Matt Pocock Wingman overlay."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import tarfile
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'integrations/matt-pocock'
ADAPTER = 'wingman-matt-adapter'
RECEIPT = '.wingman-matt-install.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def tree(directory):
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError(f'Expected canonical regular directory: {directory}')
    result = {}
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Symlink inside skill: {path}')
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = path.read_bytes()
        elif not path.is_dir():
            raise ValueError(f'Unsupported file: {path}')
    return result


def digests(files):
    return {name: sha(data) for name, data in files.items()}


def render():
    manifest = json.loads((BASE / 'manifest.json').read_text())
    raw = (BASE / 'upstream.tar').read_bytes()
    if sha(raw) != manifest['archive_sha256']:
        raise ValueError('Pinned upstream archive changed; review/re-pin explicitly')
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        members = {}
        for item in archive.getmembers():
            if Path(item.name).is_absolute() or '..' in Path(item.name).parts or not (item.isfile() or item.isdir()):
                raise ValueError(f'Unsafe upstream entry: {item.name}')
            if item.isfile():
                members[item.name] = archive.extractfile(item).read()
    pristine, adapted = {}, {}
    for name, spec in manifest['skills'].items():
        prefix = spec['path'] + '/'
        files = {p[len(prefix):]: data for p, data in members.items() if p.startswith(prefix)}
        if digests(files) != spec['files']:
            raise ValueError(f'Upstream file conflict: {name}')
        pristine[name] = files
        patched = dict(files)
        source = files['SKILL.md'].decode()
        if not source.startswith('---\n') or '\n---\n' not in source[4:]:
            raise ValueError(f'Unsupported frontmatter: {name}')
        end = source.index('\n---\n', 4) + 5
        block = ('\n<!-- wingman-matt-overlay:v1 -->\n'
                 '## Wingman routing takes precedence\n\n'
                 'When this work is in Wingman/NStack/Flight Deck/Ambulando context, '
                 'read [wingman-matt-adapter](../wingman-matt-adapter/SKILL.md) before '
                 'following any tracker, file-saving or output instructions below or in linked resources. '
                 'Its routing explicitly supersedes conflicting upstream saving defaults inside Wingman. '
                 'Outside Wingman, retain the standalone instructions below.\n\n'
                 + 'Inside Wingman: ' + spec['routing'] + '\n\n'
                 '<!-- /wingman-matt-overlay:v1 -->\n')
        patched['SKILL.md'] = (source[:end] + block + source[end:]).encode()
        adapted[name] = patched
    adapted[ADAPTER] = tree(ROOT / ADAPTER)
    return manifest, pristine, adapted


def materialize(files, directory):
    directory.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


def check_generated(adapted):
    expected = set(adapted) - {ADAPTER}
    for name in expected:
        if tree(ROOT / name) != adapted[name]:
            raise ValueError(f'Generated content conflict: {name}; render and review')


def install(target, aliases, manifest, pristine, adapted, check=False):
    target = target.expanduser().absolute()
    old = json.loads((target / RECEIPT).read_text()) if (target / RECEIPT).exists() else {}
    # Validate every destination and dependency before changing any installed skill.
    for name in ['flight-deck-workflow', 'ambulando-artefacts', 'wingman-sessions', 'artifacts']:
        if not (target / name / 'SKILL.md').is_file():
            raise ValueError(f'Missing installed dependency: {name}')
    observed = {}
    for name, files in adapted.items():
        dest = target / name
        if dest.exists() or dest.is_symlink():
            current = tree(dest)
            observed[name] = digests(current)
            allowed = [digests(files), digests(pristine.get(name, {}))]
            if old.get('files', {}).get(name):
                allowed.append(old['files'][name])
            if digests(current) not in allowed:
                raise ValueError(f'Installed local edits conflict: {dest}; preserve/reconcile first')
            if check and current != files:
                raise ValueError(f'Installed drift: {dest}')
        else:
            observed[name] = None
            if check:
                raise ValueError(f'Missing installed skill: {dest}')
    for alias_root in aliases:
        for name in adapted:
            alias = alias_root.expanduser().absolute() / name
            if alias.exists() or alias.is_symlink():
                if not alias.is_symlink() or alias.resolve() != (target / name).resolve():
                    raise ValueError(f'Unmanaged alias conflict: {alias}')
            elif check:
                raise ValueError(f'Missing alias: {alias}')
    if check:
        return
    target.mkdir(parents=True, exist_ok=True)
    # Retain previous trees outside the auto-cleaned stage, including on failure.
    # A concurrent editor holding an old inode must never lose its saved bytes.
    backup_root = target.parent / '.wingman-matt-backups' / str(uuid.uuid4())
    with tempfile.TemporaryDirectory(prefix='.matt-stage-', dir=target) as temporary:
        stage = Path(temporary)
        for name, files in adapted.items():
            materialize(files, stage / name)
        # Recheck all targets after staging so an observed concurrent edit aborts the batch.
        for name in adapted:
            dest = target / name
            now = digests(tree(dest)) if dest.exists() or dest.is_symlink() else None
            if now != observed[name]:
                raise ValueError(f'Concurrent installation edit: {dest}')
        for name, files in adapted.items():
            dest = target / name
            if observed[name] == digests(files):
                continue
            now = digests(tree(dest)) if dest.exists() or dest.is_symlink() else None
            if now != observed[name]:
                raise ValueError(f'Concurrent installation edit before swap: {dest}')
            backup = backup_root / name
            if dest.exists():
                backup_root.mkdir(parents=True, exist_ok=True)
                dest.rename(backup)
                if digests(tree(backup)) != observed[name]:
                    backup.rename(dest)
                    raise ValueError(f'Concurrent installation edit during swap: {dest}')
            try:
                (stage / name).rename(dest)
            except Exception:
                if backup.exists():
                    backup.rename(dest)
                raise
        for alias_root in aliases:
            alias_root = alias_root.expanduser().absolute()
            alias_root.mkdir(parents=True, exist_ok=True)
            for name in adapted:
                alias = alias_root / name
                if not alias.is_symlink():
                    alias.symlink_to(target / name, target_is_directory=True)
        receipt = {'schema_version': 1, 'upstream_commit': manifest['upstream_commit'],
                   'files': {name: digests(files) for name, files in adapted.items()}}
        for name, files in adapted.items():
            if tree(target / name) != files:
                raise ValueError(f'Post-install concurrent edit: {target / name}; previous trees retained at {backup_root}')
        receipt_tmp = stage / 'receipt.json'
        receipt_tmp.write_text(json.dumps(receipt, indent=2) + '\n')
        os.replace(receipt_tmp, target / RECEIPT)
    if backup_root.exists():
        print(f'Previous trees retained for explicit review/cleanup: {backup_root}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['render', 'check', 'install', 'check-installed'])
    parser.add_argument('--target', type=Path, help='Canonical installed root, normally ~/.agents/skills')
    parser.add_argument('--alias', action='append', type=Path, default=[], help='Harness root; symlinks only, repeatable')
    args = parser.parse_args()
    manifest, pristine, adapted = render()
    if args.action == 'render':
        lock_path = BASE / 'generated-lock.json'
        previous = json.loads(lock_path.read_text()) if lock_path.exists() else {}
        for name, files in adapted.items():
            if name == ADAPTER:
                continue
            dest = ROOT / name
            if dest.exists():
                current = digests(tree(dest))
                if current not in [digests(files), previous.get(name)]:
                    raise ValueError(f'Generated source edits conflict: {dest}; reconcile before render')
        for name, files in adapted.items():
            if name != ADAPTER:
                dest = ROOT / name
                if dest.exists() and set(tree(dest)) != set(files):
                    raise ValueError(f'Generated file inventory changed: {name}; reconcile explicitly')
                materialize(files, dest)
        lock_path.write_text(json.dumps({name: digests(files) for name, files in adapted.items()
                                        if name != ADAPTER}, indent=2) + '\n')
    else:
        check_generated(adapted)
    if args.action in ['install', 'check-installed']:
        if not args.target:
            parser.error('--target is required')
        install(args.target, args.alias, manifest, pristine, adapted, check=args.action == 'check-installed')
    print(f'{args.action}: 27 pinned skills + shared adapter verified')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        raise SystemExit(str(error))
