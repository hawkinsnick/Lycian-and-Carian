"""Offline, source-preserving epigraphic adapters. No linguistic reconstruction."""
from collections import Counter
import csv
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import shutil
import unicodedata


def read_json(path):
    return json.loads(Path(path).read_bytes())


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def safe(root, relative):
    p = Path(relative)
    if p.is_absolute() or not p.parts or '..' in p.parts:
        raise ValueError('Unsafe relative path: ' + str(relative))
    target = root / p
    if target.is_symlink() or root.resolve() not in target.resolve().parents:
        raise ValueError('Unsafe source path: ' + str(relative))
    return target


class IndexParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.current = [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'span' and a.get('langid') in ('lycian', 'carian', 'milyan') and 'docid' in a:
            if self.current is not None:
                raise ValueError('Nested index span')
            self.current = {'docid': a['docid'], 'language': a['langid'], 'label': ''}

    def handle_data(self, data):
        if self.current is not None:
            self.current['label'] += data

    def handle_endtag(self, tag):
        if tag == 'span' and self.current is not None:
            self.rows.append(self.current)
            self.current = None


class MatrixParser(HTMLParser):
    """Retain upstream table rows and cells, including duplicated clitic columns."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        elif tag in ('td', 'th'):
            self.cell = ''
        elif tag == 'br' and self.cell is not None:
            self.cell += '\n'

    def handle_data(self, data):
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            if self.row is None:
                raise ValueError('Annotation cell without row')
            self.row.append(self.cell)
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None


def pointer(value):
    return value.replace('~', '~0').replace('/', '~1')


class IdTextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.values = [], {}

    def handle_starttag(self, tag, attrs):
        self.stack.append((tag, dict(attrs).get('id')))
        ident = self.stack[-1][1]
        if ident:
            self.values[ident] = ''
        if tag in ('br', 'img', 'meta', 'link', 'input', 'hr', 'wbr'):
            self.stack.pop()

    def handle_data(self, text):
        for _, ident in self.stack:
            if ident:
                self.values[ident] += text

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return


def greek_parallel(text, language):
    # Greek theta/tau are also upstream Lycian transliteration conventions.
    # This is a script screen, not an independently verified language assignment.
    if language != 'lycian':
        return False
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and any(c not in 'θτ' for c in letters) and all(
        'GREEK' in unicodedata.name(c, '') for c in letters)


def tokens(text, language):
    """Only whole unmarked whitespace/colon-separated source strings are eligible."""
    result = []
    conventions = {'lycian': 'θτ', 'carian': 'βτδλγ', 'milyan': '', 'ecr': 'φ'}[language]
    for m in re.finditer(r'[^\s:|]+', text):
        value = m.group()
        eligible = bool(value) and value[0] != '=' and value[-1] != '=' and all(
            (c.isalpha() and ('LATIN' in unicodedata.name(c, '') or c in conventions))
            or (unicodedata.category(c) == 'Mn' and c not in '\u0323\u0325')
            or c == '=' for c in value)
        result.append({'text': value, 'start': m.start(), 'end': m.end(),
                       'eligible': eligible,
                       'reason': 'whole_unmarked_source_string' if eligible else 'damage_uncertainty_editorial_or_unmapped_sign'})
    return result


def ediana(root):
    parser = IndexParser()
    parser.feed((root / 'data/raw/ediana/corpus-index.html').read_bytes().decode('utf-8'))
    index = read_json(root / 'data/source-index.json')
    if sorted(parser.rows, key=lambda x: (x['language'], x['docid'])) != sorted(index, key=lambda x: (x['language'], x['docid'])):
        raise ValueError('Source index does not replay from public catalogue')
    entries = {(x['language'], x['docid']): x for x in index}
    if len(entries) != len(index):
        raise ValueError('Duplicate authority/language/source ID')
    records, seen = [], set()
    for acquisition in read_json(root / 'data/acquisition.json'):
        if 'error' in acquisition:
            raise ValueError('Unresolved acquisition: ' + str(acquisition))
        language = acquisition['language']
        raw = safe(root, acquisition['raw_path'])
        if sha(raw) != acquisition['sha256']:
            raise ValueError('Raw source checksum mismatch: ' + str(raw))
        if acquisition['license'] != 'CC-BY-SA-4.0':
            raise ValueError('Missing admissible licence')
        form = acquisition['request_form']
        if form != {'searchterms': '{}', 'corpus_text': 'true', 'language': language,
                    'docids': ','.join(acquisition['source_ids'])}:
            raise ValueError('Request membership mismatch')
        response = read_json(raw)
        if not isinstance(response, dict):
            raise ValueError('Expected response groups')
        received = set()
        for group, rows in response.items():
            if not rows or any(not isinstance(r, dict) for r in rows):
                raise ValueError('Malformed source rows')
            source_ids = {r['docid'] for r in rows}
            if len(source_ids) != 1:
                raise ValueError('Mixed source IDs in group')
            source_id = next(iter(source_ids))
            key = (language, source_id)
            if key in seen or source_id not in acquisition['source_ids'] or key not in entries:
                raise ValueError('Unexpected or duplicated response source ID')
            seen.add(key)
            received.add(source_id)
            label = entries[key]['label']
            if label != group:
                raise ValueError('Response title does not match catalogue: ' + group)
            if 'deleted' in label.lower():
                category = 'deleted_by_source'
            elif 'uncertain' in label.lower() or 'unknown' in label.lower():
                category = 'uncertain_reading_or_direction'
            elif label == 'Coin Legends':
                category = 'aggregated_source_group'
            else:
                category = 'source_attributed_transcription'
            lines = []
            for i, row in enumerate(rows):
                text = row.get('sentence')
                if text is None or text == '':
                    continue
                if not isinstance(text, str) or row['graph'] != 'line':
                    raise ValueError('Unrecognized text representation')
                parallel = greek_parallel(text, language)
                mp = MatrixParser()
                mp.feed(row['sentence_total'])
                if len(mp.rows) != 6:
                    raise ValueError('Unexpected annotation matrix rows')
                lines.append({'source_row': i, 'source_locator': '/' + pointer(group) + '/' + str(i),
                              'label': row['word'], 'text': text,
                              'representation': 'upstream_transcription_string',
                              'partition': 'greek_script_parallel_candidate' if parallel else language,
                              'partition_evidence': 'project_unicode_script_screen' if parallel else 'upstream_corpus_membership',
                              'analysis_eligible': category == 'source_attributed_transcription' and not parallel,
                              'annotations': dict(zip(('surface', 'segmentation', 'lemma', 'translation', 'part_of_speech', 'morphology'), mp.rows)),
                              'tokens': tokens(text, language)})
            records.append({'record_id': 'EDIANA-' + language.upper() + '-' + source_id,
                            'source_id': source_id, 'authority': 'eDiAna', 'language': language,
                            'label': label, 'category': category,
                            'unit': 'digital_catalogue_entry', 'object_id': None,
                            'independent_witness_count': None,
                            'source': {'url': f'https://www.ediana.gwi.uni-muenchen.de/corpus.php?corpus={language}&docid={source_id}',
                                       'raw_path': acquisition['raw_path'], 'sha256': acquisition['sha256'],
                                       'group_locator': '/' + pointer(group), 'license': 'CC-BY-SA-4.0',
                                       'principal_editions': rows[0]['ref']},
                            'lines': lines})
        if received != set(acquisition['source_ids']):
            raise ValueError('Incomplete batch response')
    if seen != set(entries):
        raise ValueError('Catalogue coverage mismatch')
    return sorted(records, key=lambda x: (x['language'], int(x['source_id'])))


def eteocretan(root):
    readings = read_json(root / 'data/readings.json')
    wikipedia = IdTextParser()
    wikipedia.feed((root / 'data/raw/wikipedia-es.html').read_bytes().decode('utf-8'))
    records, ids = [], set()
    for r in readings:
        if r['record_id'] in ids:
            raise ValueError('Duplicate reading ID')
        ids.add(r['record_id'])
        if r['source_level'] not in ('primary_historical_edition', 'secondary_reference'):
            raise ValueError('Unknown evidence level')
        source = r['source']
        if sha(safe(root, source['evidence_path'])) != source['sha256']:
            raise ValueError('Reading evidence changed')
        if source['license'] not in ('public_domain_original', 'CC-BY-SA-4.0'):
            raise ValueError('Unlicensed reading')
        lines = []
        for i, line in enumerate(r['lines']):
            if r['source_level'] == 'secondary_reference' and wikipedia.values.get(line['source_text_id']) != line['text']:
                raise ValueError('Secondary reading does not replay from source element')
            partition = line.get('partition', 'ecr')
            eligible = (r['default_reading'] and r['source_level'] == 'primary_historical_edition' and partition == 'ecr'
                        and not line.get('uncertain', False) and not line.get('injured', False))
            t = tokens(line['text'], 'ecr')
            # Historical readings are strings, not safely delimited ancient words.
            # Source doubts and injury annotations remain explicit and block token use.
            for token in t:
                if line.get('uncertain', False) or line.get('injured', False):
                    token['eligible'] = False
                    token['reason'] = 'source_marks_line_as_injured_or_uncertain'
            lines.append({'source_row': i, 'source_locator': line['locator'], 'label': line['label'],
                          'text': line['text'], 'representation': r['representation'],
                          'partition': partition, 'partition_evidence': line.get('partition_evidence', 'attributed_source_reading'),
                          'analysis_eligible': eligible,
                          'annotations': {'injured': line.get('injured', False), 'uncertain': line.get('uncertain', False),
                                          'note': line.get('note', '')}, 'tokens': t})
        records.append({'record_id': r['record_id'], 'source_id': r['source_id'], 'authority': r['authority'],
                        'language': 'ecr', 'label': r['label'],
                        'category': 'historical_edition' if r['source_level'] == 'primary_historical_edition' else 'secondary_reference',
                        'unit': 'attributed_reading_version', 'object_id': r['object_id'],
                        'independent_witness_count': None, 'source': source,
                        'source_level': r['source_level'], 'default_reading': r['default_reading'],
                        'lines': lines})
    return records


def build(root):
    config = read_json(root / 'project.json')
    if config['adapter'] not in ('ediana', 'eteocretan') or config['data_license'] != 'CC-BY-SA-4.0':
        raise ValueError('Unknown adapter or invalid data licence')
    return ediana(root) if config['adapter'] == 'ediana' else eteocretan(root)


def audit(root, records=None):
    records = build(root) if records is None else records
    config = read_json(root / 'project.json')
    out = {'version': (root / 'VERSION').read_text().strip(), 'scope': config['scope'],
           'records': len(records), 'record_unit': config['record_unit'],
           'categories': dict(sorted(Counter(r['category'] for r in records).items())),
           'languages': {}, 'blocked_claims': ['exhaustive_world_corpus', 'independently_verified_critical_edition',
                                            'linguistic_gold_standard', 'cross_script_phonetic_equivalence',
                                            'decipherment', 'unique_physical_monument_total'],
           'independent_human_epigraphic_review': False,
           'source_snapshot_reconciled': True}
    for language in sorted({r['language'] for r in records}):
        rs = [r for r in records if r['language'] == language]
        ls = [l for r in rs for l in r['lines']]
        out['languages'][language] = {'records': len(rs), 'source_text_rows': len(ls),
            'analysis_eligible_rows': sum(l['analysis_eligible'] for l in ls),
            'excluded_greek_script_rows': sum(l['partition'] == 'greek_script_parallel_candidate' for l in ls),
            'conservative_source_string_tokens': sum(t['eligible'] and l['analysis_eligible'] for l in ls for t in l['tokens'])}
    if config['adapter'] == 'eteocretan':
        registry = read_json(root / 'research/coverage-register.json')
        out['coverage_register'] = {'entries': len(registry), 'statuses': dict(Counter(x['status'] for x in registry)),
                                    'known_incomplete': True}
        out['distinct_objects_with_readings'] = len({r['object_id'] for r in records})
    return out


def frequency(records, language):
    counts = Counter(t['text'] for r in records if r['language'] == language for l in r['lines']
                     if l['analysis_eligible'] for t in l['tokens'] if t['eligible'])
    return {'language': language, 'measure': 'whole_unmarked_source_strings_not_phonemes_or_signs',
            'case_sensitive': True, 'unicode_normalized': False,
            'counts': dict(sorted(counts.items(), key=lambda x: (-x[1], x[0]))), 'total': sum(counts.values())}


def verify_lock(root):
    errors = []
    lock = read_json(root / 'data/source-lock.json')
    if not lock['files'] or len({x['path'] for x in lock['files']}) != len(lock['files']):
        return ['Empty or duplicate source-lock paths']
    expected = {p.relative_to(root).as_posix() for directory in ('data/raw', 'data/source-evidence')
                for p in (root / directory).rglob('*') if p.is_file()}
    inputs = ('data/source-index.json', 'data/acquisition.json') if read_json(root / 'project.json')['adapter'] == 'ediana' else ('data/readings.json', 'research/coverage-register.json')
    expected.update((*inputs, 'project.json'))
    if expected != {x['path'] for x in lock['files']}:
        errors.append('Source lock membership mismatch')
    for x in lock['files']:
        try:
            if sha(safe(root, x['path'])) != x['sha256']:
                errors.append('Source lock checksum: ' + x['path'])
        except (ValueError, OSError) as e:
            errors.append(str(e))
    return errors


def validate_family(root):
    index = read_json(root / 'research/family/index.json')
    errors = []
    for r in index['native_snapshots']:
        p = safe(root, r['report_path'])
        if sha(p) != r['report_sha256']:
            errors.append('Native report checksum changed: ' + r['repository'])
        if r['commit'] not in r['source_url']:
            errors.append('Unpinned family report')
    relations = read_json(root / 'research/family/relations.json')
    for relation in relations:
        if relation['kind'] not in ('geographic_context', 'research_comparison', 'same_object_different_language_component'):
            errors.append('Unknown relation kind')
        if relation['implies_language_identity'] or relation['implies_sign_equivalence'] or relation['creates_independent_witnesses'] != 0:
            errors.append('Unsupported cross-project inference')
    if (root / 'research/coverage-register.json').exists():
        register = read_json(root / 'research/coverage-register.json')
        ids = [x['object_id'] for x in register]
        if len(ids) != len(set(ids)):
            errors.append('Duplicate registered object')
        for x in register:
            if x['status'] in ('disputed_script', 'disputed_authenticity', 'uncertain_language', 'collection_lead') and x['analysis_eligible']:
                errors.append('Disputed or uncollated object admitted to analysis')
            if x['object_id'] == 'CRET-DISPUTED-HM-X2416' and (x['language'] is not None or x['status'] != 'disputed_script'):
                errors.append('Arkalochori incorrectly assigned to Eteocretan')
    return errors


def validate(root):
    errors = verify_lock(root) + validate_family(root)
    try:
        records = build(root)
        if records != read_json(root / 'data/records.json'):
            errors.append('Derived records differ from source replay')
        for r in records:
            for l in r['lines']:
                for t in l['tokens']:
                    if l['text'][t['start']:t['end']] != t['text']:
                        errors.append('Token offset mismatch')
        if audit(root, records) != read_json(root / 'analysis/current-status.json'):
            errors.append('Audit differs from source replay')
    except (OSError, ValueError, KeyError, TypeError) as e:
        errors.append(str(e))
    return errors


def export(root, output):
    records = build(root)
    output = Path(output)
    if output.resolve() == root.resolve() or root.resolve() not in output.resolve().parents:
        raise ValueError('Export directory must be beneath repository root')
    if output.exists() and (output / 'manifest.json').exists():
        old = read_json(output / 'manifest.json')
        for r in old['files']:
            p = safe(output, r['path'])
            if p.exists():
                p.unlink()
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / 'corpus.json', records)
    write_json(output / 'audit.json', audit(root, records))
    with (output / 'corpus.jsonl').open('w', encoding='utf-8', newline='\n') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n')
    with (output / 'lines.csv').open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(('record_id', 'language', 'category', 'line_label', 'partition', 'analysis_eligible', 'text', 'source_url', 'source_locator'))
        for r in records:
            for l in r['lines']:
                w.writerow((r['record_id'], r['language'], r['category'], l['label'], l['partition'], l['analysis_eligible'], l['text'], r['source']['url'], l['source_locator']))
    for language in sorted({r['language'] for r in records}):
        write_json(output / ('frequency-' + language + '.json'), frequency(records, language))
    (output / 'ATTRIBUTION.md').write_bytes((root / 'NOTICE').read_bytes())
    files = sorted(p for p in output.rglob('*') if p.is_file() and p.name != 'manifest.json')
    write_json(output / 'manifest.json', {'version': (root / 'VERSION').read_text().strip(),
               'license': 'CC-BY-SA-4.0', 'files': [{'path': p.relative_to(output).as_posix(), 'sha256': sha(p)} for p in files]})


def verify_export(root, output):
    output = Path(output)
    errors = []
    try:
        manifest = read_json(output / 'manifest.json')
        paths = [x['path'] for x in manifest['files']]
        if len(paths) != len(set(paths)) or manifest['license'] != 'CC-BY-SA-4.0':
            return ['Invalid export manifest']
        if manifest['version'] != (root / 'VERSION').read_text().strip():
            errors.append('Export version mismatch')
        actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
        if actual != set(paths) | {'manifest.json'}:
            errors.append('Unlisted or missing export file')
        for x in manifest['files']:
            if sha(safe(output, x['path'])) != x['sha256']:
                errors.append('Export checksum mismatch: ' + x['path'])
        source = build(root)
        if read_json(output / 'corpus.json') != source:
            errors.append('JSON source roundtrip mismatch')
        lines = [json.loads(x) for x in (output / 'corpus.jsonl').read_text().splitlines()]
        if lines != source:
            errors.append('JSONL source roundtrip mismatch')
        if read_json(output / 'audit.json') != audit(root, source):
            errors.append('Export audit mismatch')
        with (output / 'lines.csv').open(newline='', encoding='utf-8') as f:
            actual_csv = list(csv.DictReader(f))
        expected_csv = [{'record_id': r['record_id'], 'language': r['language'], 'category': r['category'],
                         'line_label': l['label'], 'partition': l['partition'], 'analysis_eligible': str(l['analysis_eligible']),
                         'text': l['text'], 'source_url': r['source']['url'], 'source_locator': l['source_locator']}
                        for r in source for l in r['lines']]
        if actual_csv != expected_csv:
            errors.append('CSV source roundtrip mismatch')
        if (output / 'ATTRIBUTION.md').read_bytes() != (root / 'NOTICE').read_bytes():
            errors.append('Export attribution mismatch')
        for lang in {r['language'] for r in source}:
            if read_json(output / ('frequency-' + lang + '.json')) != frequency(source, lang):
                errors.append('Export frequency mismatch')
    except (OSError, ValueError, KeyError, TypeError) as e:
        errors.append(str(e))
    return errors
