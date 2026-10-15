import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('sync', Path(__file__).with_name('sync-bloct.py'))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cask = Path(self.tmp.name) / 'bloct.rb'
        self.original = 'cask "bloct" do\n  version "1.7.1"\n  sha256 "' + '0' * 64 + '"\n  app "Bloct.app"\nend\n'
        self.cask.write_text(self.original)
        self.data = b'release fixture'
        self.digest = hashlib.sha256(self.data).hexdigest()
        self.release = {'tag_name': 'v1.7.2', 'draft': False, 'prerelease': False,
                        'assets': [{'name': 'Bloct.zip', 'digest': 'sha256:' + self.digest}]}

    def test_upgrade_and_repeat(self):
        sync.update(self.cask, self.release, self.data)
        expected = self.original.replace('1.7.1', '1.7.2').replace('0' * 64, self.digest)
        self.assertEqual(self.cask.read_text(), expected)
        sync.update(self.cask, self.release, self.data)
        self.assertEqual(self.cask.read_text(), expected)

    def test_corrupted_download_keeps_cask(self):
        with self.assertRaisesRegex(ValueError, 'SHA256'):
            sync.update(self.cask, self.release, b'corrupt')
        self.assertEqual(self.cask.read_text(), self.original)

    def test_downgrade_keeps_cask(self):
        self.release['tag_name'] = 'v1.6.9'
        with self.assertRaisesRegex(ValueError, 'downgrade'):
            sync.update(self.cask, self.release, self.data)
        self.assertEqual(self.cask.read_text(), self.original)

    def test_prerelease_keeps_cask(self):
        self.release['prerelease'] = True
        with self.assertRaisesRegex(ValueError, 'stable'):
            sync.update(self.cask, self.release, self.data)
        self.assertEqual(self.cask.read_text(), self.original)


if __name__ == '__main__':
    unittest.main()
