"""Synthetic project fixtures exercise helper invariants, not Unity itself."""
import copy
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import workspace as ws


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='niraj starter test ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        ws.atomic_json(self.root / 'workspace.json', dict(schema_version=1, active_project=None, active_id=None))
        (self.root / 'UnityProjects').mkdir()

    def project(self, name='Game A', guid='a' * 32):
        relative = 'UnityProjects/' + name
        path = self.root / relative
        (path / 'Assets').mkdir(parents=True)
        ws.atomic_json(path / 'Packages/manifest.json', {'dependencies': {}})
        (path / 'ProjectSettings').mkdir()
        (path / 'ProjectSettings/ProjectVersion.txt').write_text('m_EditorVersion: 6000.0.1f1\n')
        (path / 'ProjectSettings/ProjectSettings.asset').write_text('PlayerSettings:\n  productGUID: ' + guid + '\n')
        return relative

    def selected(self):
        relative = self.project()
        ws.register(self.root, relative)
        ws.select(self.root, relative)
        return relative

    def test_initial_state_is_empty(self):
        self.assertIsNone(ws.root_state(self.root)['active_project'])
        with self.assertRaises(ws.WorkspaceError):
            ws.check(self.root)

    def test_register_does_not_select(self):
        relative = self.project()
        data = ws.register(self.root, relative)
        self.assertEqual(data['phase'], 'idea')
        self.assertIsNone(ws.root_state(self.root)['active_project'])

    def test_select_and_record(self):
        relative = self.selected()
        data = ws.record(self.root, {'done': ['Implemented movement'], 'next': ['Playtest'], 'decision': ['Touch controls']}, 'prototype')
        self.assertEqual(data['entries'][-1]['next'], ['Playtest'])
        self.assertEqual(ws.check(self.root)['project_path'], relative)

    def test_switch_keeps_each_games_history(self):
        a = self.selected()
        ws.record(self.root, {'decision': ['A controls']})
        b = self.project('Game B', 'b' * 32)
        ws.register(self.root, b)
        ws.select(self.root, b)
        self.assertEqual(ws.check(self.root)['entries'], [])
        ws.record(self.root, {'done': ['B prototype']})
        ws.select(self.root, a)
        self.assertEqual(ws.check(self.root)['entries'][0]['decision'], ['A controls'])

    def test_reject_path_traversal_and_nonportable_paths(self):
        for path in ('../outside', '/absolute', 'C:/outside', 'UnityProjects/../Bad',
                     'UnityProjects\\Bad', 'UnityProjects/CON', 'UnityProjects/name.',
                     'UnityProjects/name ', 'UnityProjects/x:y', 'UnityProjects//bad',
                     'UnityProjects/a/b', 'Other/Game', 'UnityProjects'):
            with self.subTest(path=path), self.assertRaises(ws.WorkspaceError):
                ws.register(self.root, path)

    def test_missing_project_is_not_fabricated(self):
        with self.assertRaises(ws.WorkspaceError):
            ws.register(self.root, 'UnityProjects/Missing')
        self.assertFalse((self.root / 'UnityProjects/Missing').exists())

    def test_missing_manifest_fails(self):
        relative = self.project()
        (self.root / relative / 'Packages/manifest.json').unlink()
        with self.assertRaises(ws.WorkspaceError):
            ws.register(self.root, relative)

    def test_invalid_manifest_fails(self):
        relative = self.project()
        ws.atomic_json(self.root / relative / 'Packages/manifest.json', {'dependencies': []})
        with self.assertRaises(ws.WorkspaceError):
            ws.register(self.root, relative)

    def test_missing_guid_fails(self):
        relative = self.project()
        (self.root / relative / 'ProjectSettings/ProjectSettings.asset').write_text('PlayerSettings: {}')
        with self.assertRaises(ws.WorkspaceError):
            ws.register(self.root, relative)

    def test_registration_cannot_overwrite(self):
        relative = self.selected()
        before = ws.check(self.root)
        with self.assertRaises(ws.WorkspaceError):
            ws.register(self.root, relative)
        self.assertEqual(ws.check(self.root), before)

    def test_select_unregistered_project_fails(self):
        relative = self.project()
        with self.assertRaises(ws.WorkspaceError):
            ws.select(self.root, relative)

    def test_replaced_project_rejected(self):
        relative = self.selected()
        (self.root / relative / 'ProjectSettings/ProjectSettings.asset').write_text('productGUID: ' + 'b' * 32)
        with self.assertRaises(ws.WorkspaceError):
            ws.check(self.root)

    def test_missing_state_after_replacement_rejected(self):
        relative = self.selected()
        (self.root / relative / '.game-workspace/state.json').unlink()
        with self.assertRaises(ws.WorkspaceError):
            ws.check(self.root)

    def test_stale_active_id_rejected(self):
        self.selected()
        data = ws.root_state(self.root)
        data['active_id'] = 'stale'
        ws.atomic_json(self.root / 'workspace.json', data)
        with self.assertRaises(ws.WorkspaceError):
            ws.check(self.root)

    def test_renamed_game_rejected(self):
        relative = self.selected()
        (self.root / relative).rename(self.root / 'UnityProjects/Renamed')
        with self.assertRaises(ws.WorkspaceError):
            ws.select(self.root, 'UnityProjects/Renamed')

    def test_editor_mismatch_and_relative_observation_rejected(self):
        relative = self.selected()
        other = self.project('Game B')
        self.assertEqual(ws.check(self.root, str(self.root / relative))['project_path'], relative)
        for path in (str(self.root / other), relative, str(self.root / 'Missing')):
            with self.assertRaises(ws.WorkspaceError):
                ws.check(self.root, path)

    def test_whole_workspace_move_is_portable(self):
        self.selected()
        dest = self.root / 'relocated workspace'
        dest.mkdir()
        shutil.copy2(self.root / 'workspace.json', dest / 'workspace.json')
        shutil.copytree(self.root / 'UnityProjects', dest / 'UnityProjects')
        self.assertEqual(ws.check(self.root), ws.check(dest))

    def test_version_change_requires_review(self):
        relative = self.selected()
        (self.root / relative / 'ProjectSettings/ProjectVersion.txt').write_text('m_EditorVersion: 6000.0.2f1\n')
        with self.assertRaises(ws.WorkspaceError):
            ws.check(self.root)
        ws.refresh_version(self.root)
        data = ws.check(self.root)
        self.assertEqual(data['editor_version'], '6000.0.2f1')
        self.assertIn('6000.0.1f1 -> 6000.0.2f1', data['entries'][-1]['decision'][0])

    def test_empty_progress_and_invalid_phase_rejected(self):
        self.selected()
        for fields in ({}, {'done': [' ']}, {'done': 'not a list'}):
            with self.assertRaises(ws.WorkspaceError):
                ws.record(self.root, fields)
        with self.assertRaises(ws.WorkspaceError):
            ws.record(self.root, {'done': ['Something']}, 'imaginary')

    def test_lock_prevents_mutation(self):
        relative = self.project()
        with ws.locked(self.root):
            with self.assertRaises(ws.WorkspaceError):
                ws.register(self.root, relative)
        self.assertFalse((self.root / '.workspace.lock').exists())

    def test_malformed_state_is_preserved(self):
        self.selected()
        path = self.root / 'workspace.json'
        path.write_text('{broken')
        with self.assertRaises(ws.WorkspaceError):
            ws.check(self.root)
        self.assertEqual(path.read_text(), '{broken')

    def test_link_and_reparse_metadata_rejected(self):
        # Portable simulation of Windows junction metadata; no link privileges required.
        class Linked:
            st_mode = stat.S_IFDIR
            st_file_attributes = 0x400
        with patch.object(Path, 'lstat', return_value=Linked()):
            with self.assertRaises(ws.WorkspaceError):
                ws.safe_path(self.root, 'UnityProjects/Outside')

    def test_atomic_failure_preserves_previous_json(self):
        path = self.root / 'workspace.json'
        old = path.read_bytes()
        with patch('workspace.os.replace', side_effect=OSError('simulated disk failure')):
            with self.assertRaises(OSError):
                ws.atomic_json(path, {'new': True})
        self.assertEqual(path.read_bytes(), old)
        self.assertEqual(list(self.root.glob('*.tmp')), [])


if __name__ == '__main__':
    unittest.main()
