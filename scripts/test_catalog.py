"""Contract tests for multi-collection metadata, filtering, and integrity failures."""
from pathlib import Path
import copy
import hashlib
import json
import tempfile
import unittest
import catalog


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name, text in [('entry.md', '# Entry'), ('provenance.md', '# Provenance'), ('artifact.txt', 'Original artifact')]:
            (self.root / name).write_text(text, encoding='utf-8')
        self.entry = {
            'id': 'sample-project', 'title': 'Sample project', 'summary': 'A different project.',
            'kind': 'Project documentation', 'version': '1', 'date': '2026-10-24',
            'status': 'Draft', 'topics': ['Systems design'], 'landing': 'entry.md',
            'provenance': 'provenance.md', 'artifacts': [{'label': 'Design note', 'path': 'artifact.txt',
            'format': 'Text', 'sha256': hashlib.sha256((self.root/'artifact.txt').read_bytes()).hexdigest()}]}
        self.write([self.entry])

    def write(self, entries):
        (self.root/'catalog.json').write_text(json.dumps({'schema_version': 1, 'collections': entries}))

    def test_non_bsg_collection_and_multiple_projects(self):
        other = copy.deepcopy(self.entry)
        other.update(id='another-project', title='Another project')
        self.write([self.entry, other])
        self.assertEqual(len(catalog.load_catalog(self.root)), 2)

    def test_duplicate_ids_rejected(self):
        self.write([self.entry, self.entry])
        with self.assertRaisesRegex(ValueError, 'Duplicate collection ID'):
            catalog.load_catalog(self.root)

    def test_changed_artifact_rejected(self):
        (self.root/'artifact.txt').write_text('Changed')
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            catalog.load_catalog(self.root)

    def test_missing_artifact_rejected(self):
        (self.root/'artifact.txt').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing or escaping'):
            catalog.load_catalog(self.root)

    def test_path_traversal_rejected(self):
        self.entry['landing'] = '../outside.md'
        self.write([self.entry])
        with self.assertRaisesRegex(ValueError, 'Missing or escaping'):
            catalog.load_catalog(self.root)

    def test_filters_and_no_matches(self):
        entries = catalog.load_catalog(self.root)
        self.assertEqual(catalog.select(entries, query='different', topic='systems DESIGN', kind='project documentation', status='DRAFT'), entries)
        self.assertEqual(catalog.select(entries, query='absent'), [])
        self.assertEqual(catalog.select(entries, topic='systems'), [])

    def test_deterministic_rendering_and_encoded_paths(self):
        entries = catalog.load_catalog(self.root)
        other = copy.deepcopy(entries[0])
        other.update(id='a-second-project', title='A second project', topics=['Other topic'])
        entries.append(other)
        self.assertEqual(catalog.render_catalog(entries), catalog.render_catalog(list(reversed(entries))))
        self.assertEqual(catalog.link('PDF', 'paper(BSG).pdf'), '[PDF](paper%28BSG%29.pdf)')
        self.assertIn('## Browse by topic', catalog.render_catalog(entries))

    def test_invalid_date_rejected(self):
        self.entry['date'] = '2026-02-30'
        self.write([self.entry])
        with self.assertRaises(ValueError):
            catalog.load_catalog(self.root)


if __name__ == '__main__':
    unittest.main()
