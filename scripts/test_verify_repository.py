"""Regression tests for actual navigation failures rather than file counts."""

from pathlib import Path
import tempfile
import unittest

import verify_repository as verify


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.page = self.root / 'README.md'
        self.page.write_text('# Home\n')
        (self.root / 'guide.md').write_text('# Guide\n## More details\n## Repeat\n## Repeat\n<a id="custom-anchor"></a>\n')
        (self.root / 'paper(BSG).pdf').write_bytes(b'%PDF-1.7\n')

    def errors(self, text):
        self.page.write_text(text, encoding='utf-8')
        return verify.check_links(self.root, self.page, text)[0]

    def test_inline_encoded_and_balanced_filenames(self):
        self.assertEqual(self.errors('[Read](paper(BSG).pdf) and [Read](paper%28BSG%29.pdf?raw=true)'), [])

    def test_missing_files_and_wrong_case_fail(self):
        for target in ('missing.md', 'Guide.md'):
            with self.subTest(target=target):
                self.assertTrue(self.errors(f'[Read]({target})'))

    def test_missing_same_page_section_fails(self):
        self.assertTrue(self.errors('# Home\n[Broken](#this-section-does-not-exist)'))

    def test_cross_file_headings_duplicates_and_html_ids(self):
        self.assertEqual(self.errors('[A](guide.md#more-details) [B](guide.md#repeat-1) [C](guide.md#custom-anchor)'), [])
        self.assertTrue(self.errors('[Broken](guide.md#repeat-2)'))

    def test_inline_and_reference_images_are_checked(self):
        self.assertTrue(self.errors('<img src="missing.svg" alt="x">'))
        self.assertTrue(self.errors('![Image][pic]\n\n[pic]: missing.png'))

    def test_reference_links_and_code_examples(self):
        self.assertEqual(self.errors('[Guide][g]\n\n[g]: guide.md\n\n```md\n[example](missing.md)\n```\n`[also example](missing.md)`\n'), [])
        self.assertTrue(self.errors('[Guide][g]\n\n[g]: guide.md#missing'))

    def test_parent_links_stay_inside_repository(self):
        sub = self.root / 'papers'; sub.mkdir()
        page = sub / 'README.md'; text = '[Home](../README.md#home)'
        page.write_text(text)
        self.assertEqual(verify.check_links(self.root, page, text)[0], [])
        self.assertTrue(self.errors('[Outside](../elsewhere.md)'))

    def test_headings_with_code_emphasis_and_unicode(self):
        self.assertEqual(self.errors('# `load_catalog()`\n[Here](#load_catalog)\n'), [])
        self.assertEqual(self.errors('# _Hello_\n[Here](#hello)\n'), [])
        self.assertEqual(self.errors('# Café\n[Here](#caf%C3%A9)\n'), [])

    def test_external_links_are_outside_network_check_scope(self):
        self.assertEqual(self.errors('[External](https://example.com/unknown) [Mail](mailto:example@example.com)'), [])

    def test_malformed_url_is_a_diagnostic_not_a_crash(self):
        self.assertTrue(self.errors('[Malformed](https://[invalid)'))


if __name__ == '__main__':
    unittest.main()
