"""Build a clean, deterministic starter ZIP from an explicit reviewed allowlist."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from workspace import safe_path, root_state, WorkspaceError
from validate_repo import validate

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = 'NirajArts-GameDev-Starter'
FORBIDDEN = {'.local', 'photocraftdata', '.git', '__pycache__', 'library', 'temp', 'build', 'builds', 'dist'}
ALLOWED_SUFFIXES = {'.md', '.json', '.py', '.ps1'}


def package(root):
    result = validate(root)
    if not result['ok']:
        raise WorkspaceError('Repository validation failed: ' + '; '.join(result['errors']))
    if root_state(root)['active_project'] is not None:
        raise WorkspaceError('Starter packaging requires no selected game. This is not a game backup tool.')
    manifest = json.loads(safe_path(root, 'package-manifest.json').read_text(encoding='utf-8'))
    files = manifest['files']
    for relative in files:
        path = safe_path(root, relative)
        lowered = [part.lower() for part in relative.split('/')]
        if (any(part in FORBIDDEN for part in lowered)
                or any('token' in part or part.startswith('.env') for part in lowered)
                or (path.suffix not in ALLOWED_SUFFIXES and relative != '.gitignore')
                or (relative.startswith('UnityProjects/') and relative != 'UnityProjects/README.md')
                or (relative.startswith('tools/') and relative != 'tools/photocraft/README.md')):
            raise WorkspaceError('Forbidden package entry: ' + relative)
    out = safe_path(root, 'dist/NirajArts-GameDev-Starter.zip')
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in sorted(files):
            data = safe_path(root, relative).read_bytes()
            info = zipfile.ZipInfo(ARCHIVE_ROOT + '/' + relative, date_time=(2026, 11, 2, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(out) as archive:
        if archive.testzip() is not None or len(archive.namelist()) != len(files):
            raise WorkspaceError('ZIP integrity check failed.')
    return dict(path=str(out), bytes=out.stat().st_size, files=len(files),
                sha256=hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == '__main__':
    try:
        print(json.dumps(package(ROOT), indent=2))
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
