import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import package_starter as pkg
from workspace import WorkspaceError


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='niraj packaging test ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = json.loads((ROOT / 'package-manifest.json').read_text(encoding='utf-8'))
        for relative in self.manifest['files']:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, target)

    def test_clean_allowlist_ignores_runtime_and_binaries(self):
        for relative in ('.local/photocraft-control.token', 'tools/photocraft/PhotoCraftData/recovery.txt',
                         'tools/photocraft/photocraft.exe', 'UnityProjects/Unrelated/private.txt'):
            p = self.root / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('SYNTHETIC-NON-CREDENTIAL test fixture')
        result = pkg.package(self.root)
        with zipfile.ZipFile(result['path']) as archive:
            names = archive.namelist()
            self.assertEqual(names, [pkg.ARCHIVE_ROOT + '/' + p for p in sorted(self.manifest['files'])])
            self.assertIsNone(archive.testzip())
        self.assertEqual(result['sha256'], pkg.package(self.root)['sha256'])

    def test_manifest_cannot_include_runtime_data(self):
        for relative in ('.local/secret.json', 'tools/photocraft/PhotoCraftData/settings.json'):
            with self.subTest(relative=relative):
                p = self.root / relative
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('{}')
                manifest = dict(self.manifest, files=self.manifest['files'] + [relative])
                (self.root / 'package-manifest.json').write_text(json.dumps(manifest))
                with self.assertRaises(WorkspaceError):
                    pkg.package(self.root)

    def test_active_game_cannot_be_packaged_as_blank_starter(self):
        (self.root / 'workspace.json').write_text(json.dumps(dict(schema_version=1, active_project='UnityProjects/Game', active_id='test')))
        with self.assertRaises(WorkspaceError):
            pkg.package(self.root)

    def test_link_validator_reports_missing_target(self):
        with (self.root / 'README.md').open('a') as f:
            f.write('\n[Missing](docs/absent.md)\n')
        with self.assertRaises(WorkspaceError):
            pkg.package(self.root)


if __name__ == '__main__':
    unittest.main()
