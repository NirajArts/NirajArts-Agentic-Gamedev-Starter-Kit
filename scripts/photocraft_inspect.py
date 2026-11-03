"""Read-only authenticated PhotoCraft inspection; never prints the credential."""
import json
from pathlib import Path
import re
import socket
import sys
from workspace import safe_path, WorkspaceError

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 8 * 1024 * 1024


class ProtocolError(ValueError):
    pass


def receive(stream, expected_id):
    raw = stream.readline(LIMIT + 1)
    if not raw.endswith(b'\n') or len(raw) > LIMIT:
        raise ProtocolError('Incomplete or oversized protocol reply.')
    value = json.loads(raw)
    if not isinstance(value, dict) or value.get('id') != expected_id or value.get('ok') is not True:
        # Do not echo remote errors: an untrusted peer could return the credential.
        raise ProtocolError('PhotoCraft rejected the request or returned an unexpected reply.')
    return value.get('result')


def inspect_stream(stream, token):
    for request in (
        {'id': 'auth', 'method': 'auth', 'params': {'token': token}},
        {'id': 'inspect', 'method': 'ui.inspect', 'params': {}},
    ):
        stream.write(json.dumps(request).encode('utf-8') + b'\n')
        stream.flush()
        result = receive(stream, request['id'])
    return result


def redacted(value, token):
    if isinstance(value, dict):
        return {str(k).replace(token, '[REDACTED]'): ('[REDACTED]' if re.search(r'token|secret|password', str(k), re.I)
                    else redacted(v, token)) for k, v in value.items()}
    if isinstance(value, list):
        return [redacted(v, token) for v in value]
    if isinstance(value, str):
        return value.replace(token, '[REDACTED]')
    return value


def main():
    try:
        path = safe_path(ROOT, '.local/photocraft-control.token')
        token = path.read_text(encoding='utf-8').strip()
        if not re.fullmatch('[0-9a-fA-F]{64}', token):
            raise ProtocolError('Invalid local credential format.')
        with socket.create_connection(('127.0.0.1', 9880), timeout=5) as conn:
            conn.settimeout(10)
            with conn.makefile('rwb') as stream:
                result = inspect_stream(stream, token)
        print(json.dumps(redacted(result, token), indent=2))
        return 0
    except (OSError, ValueError, WorkspaceError):
        print('Inspection failed. Check local credential, intended instance and authenticated protocol; no secret was logged.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
