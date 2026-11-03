"""Portable project selection and progress. Never controls or creates Unity projects."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
PHASES = ('idea', 'design', 'prototype', 'production', 'verification', 'blocked', 'complete')


class WorkspaceError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def safe_path(root: Path, relative: str) -> Path:
    """Reject lexical traversal and every existing link/reparse point below root."""
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise WorkspaceError('Use a nonempty relative path with forward slashes.')
    parts = relative.split('/')
    for part in parts:
        if (not part or part in ('.', '..') or part.rstrip(' .') != part
                or re.search(r'[<>:"|?*\x00-\x1f]', part)
                or re.fullmatch(r'(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?', part)):
            raise WorkspaceError('Unsafe or nonportable path component.')
    root = root.resolve(strict=True)
    path = root
    for part in parts:
        path /= part
        try:
            info = path.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise WorkspaceError('Linked paths and reparse points are not supported.')
    try:
        path.resolve().relative_to(root)
    except ValueError as exc:
        raise WorkspaceError('Path escapes repository.') from exc
    return path


def read_json(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8-sig'))
    except (OSError, ValueError) as exc:
        raise WorkspaceError(f'Cannot read valid JSON: {path.name}; preserve it for recovery.') from exc
    if not isinstance(value, dict):
        raise WorkspaceError(f'Expected an object in {path.name}.')
    return value


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix=path.name + '.', suffix='.tmp', delete=False) as f:
            tmp = Path(f.name)
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if tmp and tmp.exists():
            tmp.unlink()


@contextmanager
def locked(root):
    path = safe_path(root, '.workspace.lock')
    try:
        f = path.open('x', encoding='utf-8')
    except FileExistsError as exc:
        raise WorkspaceError('Workspace is locked; see docs/project-state.md before recovery.') from exc
    try:
        with f:
            f.write(str(os.getpid()))
            f.flush()
            yield
    finally:
        path.unlink()


def project_info(root, relative):
    path = safe_path(root, relative)
    if len(relative.split('/')) != 2 or relative.split('/')[0] != 'UnityProjects':
        raise WorkspaceError('Project must be a direct child of UnityProjects/.')
    assets = safe_path(root, relative + '/Assets')
    manifest = safe_path(root, relative + '/Packages/manifest.json')
    version_path = safe_path(root, relative + '/ProjectSettings/ProjectVersion.txt')
    settings_path = safe_path(root, relative + '/ProjectSettings/ProjectSettings.asset')
    if not assets.is_dir():
        raise WorkspaceError('Assets directory missing; create/initialize the real project in Unity.')
    if not isinstance(read_json(manifest).get('dependencies'), dict):
        raise WorkspaceError('Package manifest has no dependencies object.')
    try:
        version = re.search(r'^m_EditorVersion:\s*(\S+)\s*$', version_path.read_text(encoding='utf-8-sig'), re.M)
        guid = re.search(r'^\s*productGUID:\s*([0-9a-fA-F]{32})\s*$', settings_path.read_text(encoding='utf-8-sig'), re.M)
    except OSError as exc:
        raise WorkspaceError('Unity project settings missing; initialize/save the project in Unity.') from exc
    if not version or not guid:
        raise WorkspaceError('Editor version or productGUID missing; inspect the real Unity project.')
    return path, version.group(1), guid.group(1).lower()


def metadata_path(root, relative):
    return safe_path(root, relative + '/.game-workspace/state.json')


def registered(root, relative, allow_version_change=False):
    path, version, guid = project_info(root, relative)
    data = read_json(metadata_path(root, relative))
    if data.get('schema_version') != 1 or data.get('project_path') != relative:
        raise WorkspaceError('Project state schema/path mismatch; do not inherit stale state.')
    try:
        uuid.UUID(data['project_id'])
    except (KeyError, ValueError, TypeError, AttributeError) as exc:
        raise WorkspaceError('Project identity is invalid.') from exc
    if data.get('product_guid') != guid:
        raise WorkspaceError('Unity productGUID changed; possible replaced project. Review identity first.')
    if data.get('editor_version') != version and not allow_version_change:
        raise WorkspaceError('Editor version changed. Review the upgrade, then use refresh-version.')
    if data.get('phase') not in PHASES or not isinstance(data.get('entries'), list):
        raise WorkspaceError('Project progress state is invalid.')
    return path, data, version


def root_state(root):
    data = read_json(safe_path(root, 'workspace.json'))
    if data.get('schema_version') != 1 or 'active_project' not in data or 'active_id' not in data:
        raise WorkspaceError('Unsupported or incomplete workspace state.')
    if (data['active_project'] is None) != (data['active_id'] is None):
        raise WorkspaceError('Incomplete active project identity.')
    return data


def active(root, allow_version_change=False):
    selection = root_state(root)
    if selection['active_project'] is None:
        raise WorkspaceError('No active project. Register/select a real Unity project first.')
    path, data, version = registered(root, selection['active_project'], allow_version_change)
    if selection['active_id'] != data['project_id']:
        raise WorkspaceError('Active identity does not match project state; select deliberately after review.')
    return path, data, version


def register(root, relative):
    with locked(root):
        _, version, guid = project_info(root, relative)
        path = metadata_path(root, relative)
        if path.exists():
            raise WorkspaceError('Already has state. Use select; do not overwrite previous progress.')
        data = dict(schema_version=1, project_path=relative, project_id=str(uuid.uuid4()),
                    product_guid=guid, editor_version=version, phase='idea', updated_utc=now(), entries=[])
        atomic_json(path, data)
    return data


def select(root, relative):
    with locked(root):
        root_state(root)
        _, data, _ = registered(root, relative)
        atomic_json(safe_path(root, 'workspace.json'), dict(schema_version=1, active_project=relative,
                                                          active_id=data['project_id']))
    return data


def check(root, editor_path=None):
    path, data, _ = active(root)
    if editor_path is not None:
        observed = Path(editor_path)
        if not observed.is_absolute() or not observed.is_dir() or observed.resolve() != path.resolve():
            raise WorkspaceError('Observed Editor path does not exactly match the active project.')
    return data


def record(root, fields, phase=None):
    if phase is not None and phase not in PHASES:
        raise WorkspaceError('Invalid phase.')
    cleaned = {}
    for key in ('done', 'next', 'decision', 'blocker', 'evidence'):
        items = fields.get(key, [])
        if not isinstance(items, list) or any(not isinstance(i, str) or not i.strip() for i in items):
            raise WorkspaceError('Progress fields must contain nonblank strings.')
        if items:
            cleaned[key] = [i.strip() for i in items]
    if not cleaned:
        raise WorkspaceError('Record at least one meaningful progress item.')
    with locked(root):
        _, data, _ = active(root)
        stamp = now()
        if phase:
            data['phase'] = phase
        data['entries'].append(dict(at_utc=stamp, phase=data['phase'], **cleaned))
        data['updated_utc'] = stamp
        atomic_json(metadata_path(root, data['project_path']), data)
    return data


def refresh_version(root):
    with locked(root):
        _, data, version = active(root, allow_version_change=True)
        if data['editor_version'] == version:
            return data
        data['entries'].append(dict(at_utc=now(), phase=data['phase'],
                                   decision=[f"Confirmed Editor version change: {data['editor_version']} -> {version}"]))
        data['editor_version'] = version
        data['updated_utc'] = now()
        atomic_json(metadata_path(root, data['project_path']), data)
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('status')
    for command in ('register', 'select'):
        sub.add_parser(command).add_argument('project')
    p = sub.add_parser('check')
    p.add_argument('--editor-path', help='Canonical full path just observed from the connected Editor')
    p = sub.add_parser('record')
    p.add_argument('--phase', choices=PHASES)
    for name in ('done', 'next', 'decision', 'blocker', 'evidence'):
        p.add_argument('--' + name, action='append', default=[])
    sub.add_parser('clear')
    sub.add_parser('refresh-version')
    args = parser.parse_args(argv)
    try:
        if args.command == 'status':
            result = root_state(ROOT)
            if result['active_project'] is not None:
                result = dict(selection=result, project=check(ROOT))
        elif args.command == 'register':
            result = register(ROOT, args.project)
        elif args.command == 'select':
            result = select(ROOT, args.project)
        elif args.command == 'check':
            result = check(ROOT, args.editor_path)
        elif args.command == 'record':
            result = record(ROOT, vars(args), args.phase)
        elif args.command == 'refresh-version':
            result = refresh_version(ROOT)
        else:
            with locked(ROOT):
                root_state(ROOT)
                result = dict(schema_version=1, active_project=None, active_id=None)
                atomic_json(safe_path(ROOT, 'workspace.json'), result)
        print(json.dumps(dict(ok=True, result=result), indent=2))
        return 0
    except (WorkspaceError, OSError) as exc:
        print(json.dumps(dict(ok=False, error=str(exc))), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
