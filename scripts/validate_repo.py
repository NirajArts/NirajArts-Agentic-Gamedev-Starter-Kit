"""Check required structure, skill headers, local Markdown links and portable state."""
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote
from workspace import safe_path, root_state, WorkspaceError

ROOT = Path(__file__).resolve().parents[1]


def validate(root):
    errors = []
    required = ('AGENTS.md', 'CLAUDE.md', 'README.md', 'WORKSPACE.md', 'workspace.json',
                'LICENSE-DECISION.md', 'THIRD-PARTY-NOTICES.md', 'VALIDATION.md',
                'UnityProjects/README.md', 'tools/photocraft/README.md', 'package-manifest.json')
    for relative in required:
        if not safe_path(root, relative).is_file():
            errors.append('Missing required file: ' + relative)
    try:
        root_state(root)
    except WorkspaceError as exc:
        errors.append(str(exc))
    manifest = json.loads((root / 'package-manifest.json').read_text(encoding='utf-8'))
    paths = manifest.get('files', [])
    if not isinstance(paths, list) or not paths or len(paths) != len(set(paths)):
        errors.append('Package file list must be a nonempty, unique list.')
    links = 0
    skills = 0
    for relative in paths:
        try:
            path = safe_path(root, relative)
        except WorkspaceError as exc:
            errors.append(f'{relative}: {exc}')
            continue
        if not path.is_file():
            errors.append('Missing packaged file: ' + relative)
            continue
        if path.suffix != '.md':
            continue
        source = path.read_text(encoding='utf-8')
        if path.name == 'SKILL.md':
            skills += 1
            match = re.match(r'^---\nname: ([a-z0-9-]{1,63})\ndescription: ("[^\n]+")\n---\n', source)
            if not match or match.group(1) != path.parent.name:
                errors.append('Invalid skill frontmatter: ' + relative)
            elif not isinstance(json.loads(match.group(2)), str):
                errors.append('Skill description must be a string: ' + relative)
            if re.search(r'\b(TODO|TBD)\b', source):
                errors.append('Unfinished skill scaffold: ' + relative)
        # Ignore code fences so command examples are not parsed as Markdown links.
        markdown = re.sub(r'```.*?```', '', source, flags=re.S)
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', markdown):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            links += 1
            target = unquote(target.split('#', 1)[0]).strip('<>')
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append('Link escapes repository: ' + relative + ' -> ' + target)
                continue
            if not resolved.exists():
                errors.append('Broken local link: ' + relative + ' -> ' + target)
    if skills != 14:
        errors.append(f'Expected 14 focused skills; found {skills}.')
    return dict(ok=not errors, files=len(paths), skills=skills, local_links=links, errors=errors)


def main():
    try:
        result = validate(ROOT)
    except (OSError, ValueError) as exc:
        result = dict(ok=False, errors=[str(exc)])
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
