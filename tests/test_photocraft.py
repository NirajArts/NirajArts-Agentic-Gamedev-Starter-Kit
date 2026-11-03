import io
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import photocraft_inspect as pc


class Duplex:
    def __init__(self, replies):
        self.input = io.BytesIO(replies)
        self.output = io.BytesIO()
    def readline(self, limit):
        return self.input.readline(limit)
    def write(self, data):
        return self.output.write(data)
    def flush(self):
        pass


class PhotoCraftTests(unittest.TestCase):
    def test_auth_before_inspection(self):
        stream = Duplex(b'{"id":"auth","ok":true,"result":{}}\n{"id":"inspect","ok":true,"result":{"ready":true}}\n')
        result = pc.inspect_stream(stream, 'synthetic-test-value')
        sent = [json.loads(line) for line in stream.output.getvalue().splitlines()]
        self.assertEqual([x['method'] for x in sent], ['auth', 'ui.inspect'])
        self.assertEqual(result, {'ready': True})

    def test_auth_failure_sends_no_inspection_and_does_not_echo_peer(self):
        stream = Duplex(b'{"id":"auth","ok":false,"error":"secret echoed by peer"}\n')
        with self.assertRaises(pc.ProtocolError) as result:
            pc.inspect_stream(stream, 'synthetic-test-value')
        self.assertNotIn('secret echoed', str(result.exception))
        self.assertEqual(len(stream.output.getvalue().splitlines()), 1)

    def test_wrong_id_rejected(self):
        with self.assertRaises(pc.ProtocolError):
            pc.receive(io.BytesIO(b'{"id":"wrong","ok":true}\n'), 'auth')

    def test_incomplete_reply_rejected(self):
        with self.assertRaises(pc.ProtocolError):
            pc.receive(io.BytesIO(b'{"id":"auth","ok":true}'), 'auth')

    def test_redaction(self):
        value = {'secret': 'hidden', 'document': ['prefix synthetic-test-value suffix'], 'controlToken': 'another'}
        result = pc.redacted(value, 'synthetic-test-value')
        self.assertEqual(result['secret'], '[REDACTED]')
        self.assertNotIn('synthetic-test-value', json.dumps(result))
        self.assertEqual(result['controlToken'], '[REDACTED]')


if __name__ == '__main__':
    unittest.main()
