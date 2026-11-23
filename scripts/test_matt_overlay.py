"""Behavioral checks for the public render/install contract; no live side effects."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import shutil
import subprocess
import sys
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('matt_overlay', Path(__file__).with_name('matt-overlay.py'))
overlay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(overlay)


class InstallContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.target = self.root / 'agents'
        self.target.mkdir()
        self.alias = self.root / 'codex'
        self.manifest, self.pristine, self.adapted = overlay.render()
        for name in ['flight-deck-workflow', 'ambulando-artefacts', 'wingman-sessions', 'artifacts']:
            overlay.materialize({'SKILL.md': b'dependency'}, self.target / name)

    def run_install(self):
        overlay.install(self.target, [self.alias], self.manifest, self.pristine, self.adapted)

    def test_pristine_install_repeated_save_and_aliases(self):
        for name, files in self.pristine.items():
            overlay.materialize(files, self.target / name)
        self.run_install()
        self.run_install()
        overlay.install(self.target, [self.alias], self.manifest, self.pristine, self.adapted, check=True)
        for name in self.adapted:
            self.assertEqual((self.alias / name).resolve(), (self.target / name).resolve())

    def test_local_edit_blocks_entire_batch_without_overwrite(self):
        self.run_install()
        changed = self.target / 'wayfinder/SKILL.md'
        changed.write_text('concurrent private local change')
        before = {name: overlay.tree(self.target / name) for name in self.adapted}
        with self.assertRaisesRegex(ValueError, 'local edits conflict'):
            self.run_install()
        self.assertEqual(changed.read_text(), 'concurrent private local change')
        self.assertEqual(before, {name: overlay.tree(self.target / name) for name in self.adapted})

    def test_unmanaged_alias_refuses_before_canonical_mutation(self):
        (self.alias / 'wayfinder').mkdir(parents=True)
        (self.alias / 'wayfinder/private.txt').write_text('keep me')
        with self.assertRaisesRegex(ValueError, 'Unmanaged alias conflict'):
            self.run_install()
        self.assertFalse((self.target / 'ask-matt').exists())
        self.assertEqual((self.alias / 'wayfinder/private.txt').read_text(), 'keep me')

    def test_missing_dependency_and_internal_symlink_refuse(self):
        (self.target / 'ambulando-artefacts/SKILL.md').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing installed dependency'):
            self.run_install()
        self.assertFalse((self.target / 'ask-matt').exists())
        (self.target / 'ambulando-artefacts/SKILL.md').write_text('dependency')
        (self.target / 'wayfinder').mkdir()
        (self.target / 'wayfinder/SKILL.md').symlink_to(self.target / 'artifacts/SKILL.md')
        with self.assertRaisesRegex(ValueError, 'Symlink inside skill'):
            self.run_install()

    def test_edit_at_rename_is_preserved_and_refused(self):
        for name, files in self.pristine.items():
            overlay.materialize(files, self.target / name)
        victim = self.target / 'ask-matt'
        original_rename = Path.rename

        def racing_rename(source, destination):
            if source == victim:
                (source / 'SKILL.md').write_text('edit at rename boundary')
            return original_rename(source, destination)

        with patch.object(Path, 'rename', racing_rename):
            with self.assertRaisesRegex(ValueError, 'during swap'):
                self.run_install()
        self.assertEqual((victim / 'SKILL.md').read_text(), 'edit at rename boundary')

    def test_previous_tree_survives_success_for_concurrent_inode_writers(self):
        for name, files in self.pristine.items():
            overlay.materialize(files, self.target / name)
        self.run_install()
        retained = list((self.target.parent / '.wingman-matt-backups').glob('*/wayfinder/SKILL.md'))
        self.assertEqual(len(retained), 1)
        self.assertEqual(retained[0].read_bytes(), self.pristine['wayfinder']['SKILL.md'])

    def test_overlay_retains_complete_upstream_method_and_policy(self):
        for name, files in self.pristine.items():
            original = files['SKILL.md'].decode()
            patched = self.adapted[name]['SKILL.md'].decode()
            start = patched.index('\n<!-- wingman-matt-overlay:v1 -->')
            end = patched.index('<!-- /wingman-matt-overlay:v1 -->\n') + len('<!-- /wingman-matt-overlay:v1 -->\n')
            self.assertEqual(patched[:start] + patched[end:], original)
            for path, content in files.items():
                if path != 'SKILL.md':
                    self.assertEqual(self.adapted[name][path], content)

    def render_fixture(self):
        root = self.root / 'source'
        (root / 'scripts').mkdir(parents=True)
        shutil.copyfile(Path(__file__).with_name('matt-overlay.py'), root / 'scripts/matt-overlay.py')
        shutil.copytree(overlay.BASE, root / 'integrations/matt-pocock')
        for name, files in self.adapted.items():
            overlay.materialize(files, root / name)
        return root

    def test_generated_source_edit_refuses_without_overwriting(self):
        root = self.render_fixture()
        victim = root / 'wayfinder/SKILL.md'
        victim.write_text('concurrent reusable source edit')
        result = subprocess.run([sys.executable, str(root / 'scripts/matt-overlay.py'), 'render'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Generated source edits conflict', result.stderr)
        self.assertEqual(victim.read_text(), 'concurrent reusable source edit')

    def test_changed_upstream_archive_refuses_before_render(self):
        root = self.render_fixture()
        archive = root / 'integrations/matt-pocock/upstream.tar'
        archive.write_bytes(archive.read_bytes() + b'changed')
        before = (root / 'wayfinder/SKILL.md').read_bytes()
        result = subprocess.run([sys.executable, str(root / 'scripts/matt-overlay.py'), 'render'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Pinned upstream archive changed', result.stderr)
        self.assertEqual((root / 'wayfinder/SKILL.md').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
