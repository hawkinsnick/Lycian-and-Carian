"""Negative and roundtrip tests for source integrity and analytical boundaries."""
import copy
import csv
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from corpuskit import core

ROOT = Path(__file__).resolve().parents[1]


class TokenBoundaries(unittest.TestCase):
    def test_damage_not_silently_stripped(self):
        ts = core.tokens('a[.]mob sδi worḍ word? me=ti [restored] 𐋆', 'carian')
        self.assertEqual([t['text'] for t in ts if t['eligible']], ['sδi', 'me=ti'])

    def test_combining_vowels_retained_without_normalization(self):
        text = 'am̃mãma ẽni m=ẽne'
        ts = core.tokens(text, 'lycian')
        self.assertTrue(all(t['eligible'] for t in ts))
        self.assertEqual([text[t['start']:t['end']] for t in ts], ['am̃mãma', 'ẽni', 'm=ẽne'])

    def test_greek_parallel_screen_does_not_remove_conventional_transliteration(self):
        self.assertTrue(core.greek_parallel('Μασα Κοατα', 'lycian'))
        self.assertFalse(core.greek_parallel('qastte τerñ', 'lycian'))
        self.assertFalse(core.greek_parallel('sδi', 'carian'))

    def test_greek_strings_not_lycian_tokens(self):
        self.assertFalse(any(t['eligible'] for t in core.tokens('Μασα Κοατα', 'lycian')))

    def test_clitic_segmentation_not_expanded_into_independent_words(self):
        self.assertEqual([t['text'] for t in core.tokens('me=ti', 'lycian')], ['me=ti'])


class CorpusIntegrity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', 'dist', '__pycache__', 'exports'))

    def tearDown(self):
        self.temp.cleanup()

    def write(self, relative, value):
        core.write_json(self.root / relative, value)

    def test_exact_source_replay(self):
        self.assertEqual(core.validate(self.root), [])

    def test_changed_raw_source_rejected(self):
        lock = core.read_json(self.root / 'data/source-lock.json')
        p = self.root / lock['files'][0]['path']
        p.write_bytes(p.read_bytes() + b' ')
        self.assertTrue(core.validate(self.root))

    def test_changed_language_partition_rejected(self):
        records = core.read_json(self.root / 'data/records.json')
        records[0]['language'] = 'grc'
        self.write('data/records.json', records)
        self.assertTrue(core.validate(self.root))

    def test_changed_reading_rejected(self):
        records = core.read_json(self.root / 'data/records.json')
        r = next(r for r in records if r['lines'])
        r['lines'][0]['text'] += ' altered'
        self.write('data/records.json', records)
        self.assertTrue(core.validate(self.root))

    def test_unsafe_source_path_rejected(self):
        for value in ('../outside', '/etc/passwd', 'data/../../outside'):
            with self.assertRaises(ValueError):
                core.safe(self.root, value)

    def test_source_symlink_rejected(self):
        p = self.root / 'data/source-link'
        p.symlink_to(self.root / 'VERSION')
        with self.assertRaises(ValueError):
            core.safe(self.root, 'data/source-link')

    def test_native_status_tampering_rejected(self):
        x = core.read_json(self.root / 'research/family/index.json')['native_snapshots'][0]
        p = self.root / x['report_path']
        p.write_bytes(p.read_bytes() + b' ')
        self.assertTrue(core.validate(self.root))

    def test_cross_project_link_cannot_create_language_identity(self):
        relations = core.read_json(self.root / 'research/family/relations.json')
        relations[0]['implies_language_identity'] = True
        self.write('research/family/relations.json', relations)
        self.assertTrue(core.validate(self.root))

    def test_export_json_jsonl_and_csv_preserve_text(self):
        output = self.root / 'exports'
        core.export(self.root, output)
        self.assertEqual(core.verify_export(self.root, output), [])
        with (output / 'lines.csv').open(newline='', encoding='utf-8') as f:
            csvrows = list(csv.DictReader(f))
        records = core.build(self.root)
        expected = [(r['record_id'], l['label'], l['text']) for r in records for l in r['lines']]
        self.assertEqual([(x['record_id'], x['line_label'], x['text']) for x in csvrows], expected)

    def test_export_mutation_rejected(self):
        output = self.root / 'exports'
        core.export(self.root, output)
        p = output / 'lines.csv'
        p.write_bytes(p.read_bytes() + b'edited')
        self.assertTrue(core.verify_export(self.root, output))

    def test_manifest_cannot_hide_replaced_corpus(self):
        output = self.root / 'exports'
        core.export(self.root, output)
        core.write_json(output / 'corpus.json', [])
        manifest = core.read_json(output / 'manifest.json')
        for x in manifest['files']:
            if x['path'] == 'corpus.json':
                x['sha256'] = core.sha(output / 'corpus.json')
        core.write_json(output / 'manifest.json', manifest)
        self.assertIn('JSON source roundtrip mismatch', core.verify_export(self.root, output))

    def test_unlisted_export_rejected(self):
        output = self.root / 'exports'
        core.export(self.root, output)
        (output / 'unlisted.json').write_text('{}')
        self.assertTrue(core.verify_export(self.root, output))

    def test_manifest_traversal_rejected(self):
        output = self.root / 'exports'
        core.export(self.root, output)
        manifest = core.read_json(output / 'manifest.json')
        manifest['files'][0]['path'] = '../VERSION'
        core.write_json(output / 'manifest.json', manifest)
        self.assertTrue(core.verify_export(self.root, output))

    def test_token_offsets_recover_exact_spelling(self):
        for r in core.build(self.root):
            for line in r['lines']:
                for token in line['tokens']:
                    self.assertEqual(line['text'][token['start']:token['end']], token['text'])


class ProjectBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = core.build(ROOT)
        cls.adapter = core.read_json(ROOT / 'project.json')['adapter']

    def test_unknown_physical_witnesses_not_fabricated(self):
        self.assertTrue(all(r['independent_witness_count'] is None for r in self.records))

    def test_partitioned_frequencies_only(self):
        for lang in {r['language'] for r in self.records}:
            f = core.frequency(self.records, lang)
            expected = sum(t['eligible'] for r in self.records if r['language'] == lang for l in r['lines'] if l['analysis_eligible'] for t in l['tokens'])
            self.assertEqual(f['total'], expected)

    def test_source_membership_and_deleted_entry(self):
        if self.adapter == 'ediana':
            index = core.read_json(ROOT / 'data/source-index.json')
            self.assertEqual({(x['language'], x['docid']) for x in index}, {(r['language'], r['source_id']) for r in self.records})
            deleted = next(r for r in self.records if r['record_id'] == 'EDIANA-CARIAN-637')
            self.assertEqual(deleted['category'], 'deleted_by_source')
            self.assertEqual(deleted['lines'], [])
        else:
            self.assertEqual(len({r['object_id'] for r in self.records}), 8)
            self.assertEqual(len(self.records), 12)

    def test_parallel_and_secondary_exclusions(self):
        if self.adapter == 'ediana':
            greek = [l for r in self.records for l in r['lines'] if l['partition'] == 'greek_script_parallel_candidate']
            self.assertGreater(len(greek), 0)
            self.assertFalse(any(l['analysis_eligible'] for l in greek))
        else:
            secondary = [l for r in self.records if r['source_level'] == 'secondary_reference' for l in r['lines']]
            self.assertFalse(any(l['analysis_eligible'] for l in secondary))

    def test_alternatives_and_uncertainties_not_pooled(self):
        if self.adapter == 'ediana':
            excluded = [l for r in self.records if r['category'] in ('aggregated_source_group', 'uncertain_reading_or_direction') for l in r['lines']]
            self.assertGreater(len(excluded), 0)
            self.assertFalse(any(l['analysis_eligible'] for l in excluded))
        else:
            versions = [r for r in self.records if r['object_id'] == 'ECR-PRAISOS-2']
            self.assertEqual(len(versions), 3)
            self.assertEqual(sum(r['default_reading'] for r in versions), 1)
            alt = next(r for r in versions if r['record_id'].endswith('-II'))
            self.assertFalse(any(l['analysis_eligible'] for l in alt['lines']))

    def test_coverage_does_not_claim_exhaustiveness(self):
        audit = core.audit(ROOT, self.records)
        self.assertIn('exhaustive_world_corpus', audit['blocked_claims'])
        self.assertFalse(audit['independent_human_epigraphic_review'])
        if self.adapter == 'eteocretan':
            self.assertTrue(audit['coverage_register']['known_incomplete'])


if __name__ == '__main__':
    unittest.main()
