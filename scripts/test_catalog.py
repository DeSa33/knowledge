"""Regression tests for real catalog input and generated-output failures."""

from contextlib import redirect_stderr, redirect_stdout
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import catalog


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name, text in {'entry.md': '# Entry', 'provenance.md': '# Source',
                           'artifact.txt': 'Original artifact',
                           'README.md': '# My work\n\n' + catalog.START + '\n' + catalog.END + '\n'}.items():
            (self.root / name).write_text(text, encoding='utf-8')
        self.entry = {
            'id': 'sample-project', 'title': 'Sample project', 'summary': 'A different project.',
            'kind': 'Project notes', 'version': '1', 'date': '2026-10-24',
            'status': 'Draft', 'topics': ['Systems design'], 'landing': 'entry.md',
            'provenance': 'provenance.md', 'artifacts': [{'label': 'Design note', 'path': 'artifact.txt',
            'format': 'Text', 'sha256': catalog.digest_file(self.root / 'artifact.txt')}]}
        self.write([self.entry])

    def write(self, entries, schema=1):
        (self.root / 'catalog.json').write_text(json.dumps({'schema_version': schema, 'collections': entries}), encoding='utf-8')

    def generate(self):
        for name, content in catalog.generated_files(self.root, catalog.load_catalog(self.root)).items():
            (self.root / name).write_text(content, encoding='utf-8')

    def test_non_bsg_collections_and_multiple_files(self):
        other = copy.deepcopy(self.entry)
        other.update(id='another-project', title='Another project')
        (self.root / 'second.csv').write_text('x,y\n1,2\n')
        other['artifacts'].append({'label': 'Data', 'path': 'second.csv', 'format': 'CSV',
                                   'sha256': catalog.digest_file(self.root / 'second.csv')})
        self.write([self.entry, other])
        self.generate()
        sums = (self.root / 'SHA256SUMS').read_text()
        self.assertEqual(len(sums.splitlines()), 2)
        self.assertIn('second.csv', sums)
        self.assertEqual(catalog.check_outputs(self.root, catalog.load_catalog(self.root)), [])

    def test_unknown_date_and_unversioned_notes(self):
        self.entry.update(date=None, version=None)
        self.write([self.entry])
        self.generate()
        rendered = (self.root / 'CATALOG.md').read_text()
        self.assertIn('Unversioned', rendered)
        self.assertNotIn('vNone', rendered)
        self.assertIn('Date not recorded', rendered)

    def test_bool_schema_version_rejected(self):
        self.write([self.entry], schema=True)
        with self.assertRaisesRegex(ValueError, 'integer 1'):
            catalog.load_catalog(self.root)

    def test_invalid_shapes_and_unknown_fields_rejected(self):
        for entries in ([None], [{}], [{'id': 'item', 'artfacts': []}], {}):
            with self.subTest(entries=entries):
                self.write(entries)
                with self.assertRaises(ValueError):
                    catalog.load_catalog(self.root)

    def test_duplicate_ids_rejected(self):
        self.write([self.entry, self.entry])
        with self.assertRaisesRegex(ValueError, 'Duplicate collection ID'):
            catalog.load_catalog(self.root)

    def test_digest_mismatch_and_generation_do_not_bless_corruption(self):
        self.generate()
        before = {p: (self.root / p).read_bytes() for p in ['README.md', 'CATALOG.md', 'SHA256SUMS']}
        (self.root / 'artifact.txt').write_text('Corrupt artifact')
        with redirect_stderr(io.StringIO()):
            self.assertEqual(catalog.main(['--write'], self.root), 1)
        for p, original in before.items():
            self.assertEqual((self.root / p).read_bytes(), original)

    def test_missing_file_and_wrong_case_rejected(self):
        for name in ('missing.txt', 'Artifact.txt'):
            with self.subTest(name=name):
                self.entry['artifacts'][0]['path'] = name
                self.write([self.entry])
                with self.assertRaisesRegex(ValueError, 'Missing file or wrong filename case'):
                    catalog.load_catalog(self.root)

    def test_traversal_and_windows_paths_rejected(self):
        for name in ('../artifact.txt', '/etc/passwd', 'C:/artifact.txt', 'a/../artifact.txt', 'a\\b'):
            with self.subTest(name=name):
                self.entry['landing'] = name
                self.write([self.entry])
                with self.assertRaisesRegex(ValueError, 'relative path'):
                    catalog.load_catalog(self.root)

    def test_invalid_optional_values_rejected(self):
        for value in (True, 0, -1, '17'):
            with self.subTest(pages=value):
                self.entry['artifacts'][0]['pages'] = value
                self.write([self.entry])
                with self.assertRaisesRegex(ValueError, 'positive integer'):
                    catalog.load_catalog(self.root)

    def test_bad_dates_and_non_text_values_rejected(self):
        for value in ('2026-02-30', '20261024', 20261024, ''):
            with self.subTest(date=value):
                self.entry['date'] = value
                self.write([self.entry])
                with self.assertRaises(ValueError):
                    catalog.load_catalog(self.root)

    def test_filters_json_and_empty_results(self):
        entries = catalog.load_catalog(self.root)
        self.assertEqual(catalog.select(entries, query='different', topic='systems DESIGN', kind='project notes', status='DRAFT'), entries)
        self.assertEqual(catalog.select(entries, topic='systems'), [])
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(catalog.main(['--json', '--query', 'absent'], self.root), 0)
        self.assertEqual(json.loads(out.getvalue()), [])

    def test_deterministic_rendering_and_escaped_labels(self):
        other = copy.deepcopy(self.entry)
        other.update(id='another-project', title='A [second] | <project>')
        self.write([self.entry, other])
        first = catalog.load_catalog(self.root)
        self.write([other, self.entry])
        second = catalog.load_catalog(self.root)
        self.assertEqual(catalog.render_catalog(first), catalog.render_catalog(second))
        self.assertIn('\\[second\\] \\| &lt;project&gt;', catalog.render_catalog(first))
        self.assertEqual(catalog.link('PDF', 'paper(BSG).pdf'), '[PDF](paper%28BSG%29.pdf)')

    def test_readme_refresh_preserves_personal_text(self):
        before = 'I keep my notes here.\n' + catalog.START + '\nold listing\n' + catalog.END + '\nFeedback welcome.\n'
        (self.root / 'README.md').write_text(before)
        self.generate()
        after = (self.root / 'README.md').read_text()
        self.assertTrue(after.startswith('I keep my notes here.\n'))
        self.assertTrue(after.endswith('\nFeedback welcome.\n'))
        self.assertNotIn('old listing', after)

    def test_stale_output_detected_independently(self):
        self.generate()
        for name in ('README.md', 'CATALOG.md', 'SHA256SUMS'):
            with self.subTest(name=name):
                original = (self.root / name).read_text()
                (self.root / name).write_text(original + '\nchanged\n')
                # Changes outside the README markers are author-controlled.
                if name != 'README.md':
                    self.assertIn(name, catalog.check_outputs(self.root, catalog.load_catalog(self.root)))
                (self.root / name).write_text(original)
        (self.root / 'README.md').write_text((self.root / 'README.md').read_text().replace('Sample project', 'Wrong project'))
        self.assertIn('README.md', catalog.check_outputs(self.root, catalog.load_catalog(self.root)))

    def test_missing_readme_markers_rejected_before_write(self):
        for text in ('No markers', catalog.END + catalog.START, catalog.START * 2 + catalog.END):
            (self.root / 'README.md').write_text(text)
            with self.assertRaisesRegex(ValueError, 'marker pair'):
                catalog.generated_files(self.root, catalog.load_catalog(self.root))

    def test_empty_catalog_is_valid(self):
        self.write([])
        self.generate()
        self.assertEqual((self.root / 'SHA256SUMS').read_text(), '')
        self.assertEqual(catalog.check_outputs(self.root, []), [])

    def test_topics_with_punctuation_and_case_are_consistent(self):
        self.entry['topics'] = ['C++', 'Machine learning']
        other = copy.deepcopy(self.entry)
        other.update(id='second', title='Second project', topics=['machine learning'])
        self.write([self.entry, other])
        entries = catalog.load_catalog(self.root)
        self.assertEqual(len(catalog.topics_for(entries)), 2)
        self.assertIn('topic-c-plus-plus', catalog.render_catalog(entries))

    def test_topic_collision_and_duplicate_topics_rejected(self):
        for topics in (['A-B', 'A B'], ['Design', 'design']):
            self.entry['topics'] = topics
            self.write([self.entry])
            with self.assertRaises(ValueError):
                catalog.load_catalog(self.root)

    def test_declared_pdf_header_is_checked(self):
        self.entry['artifacts'][0]['format'] = 'PDF'
        self.write([self.entry])
        with self.assertRaisesRegex(ValueError, 'PDF header'):
            catalog.load_catalog(self.root)

    def test_generation_cannot_be_mixed_with_search(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                catalog.main(['--write', '--query', 'absent'], self.root)
        self.assertEqual(result.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
