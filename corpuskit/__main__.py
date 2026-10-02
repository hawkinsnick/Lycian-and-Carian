"""Run with python -m corpuskit from the repository root."""
import argparse
import json
from pathlib import Path
import sys
from . import core

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description='Source-preserving epigraphic corpus tools')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('build', 'validate', 'audit'):
        sub.add_parser(name)
    p = sub.add_parser('frequency')
    p.add_argument('--language', required=True)
    p = sub.add_parser('search')
    p.add_argument('query')
    p.add_argument('--language')
    p = sub.add_parser('export')
    p.add_argument('--output', default='exports')
    p = sub.add_parser('verify-export')
    p.add_argument('directory', nargs='?', default='exports')
    args = parser.parse_args()
    try:
        if args.command == 'build':
            errors = core.verify_lock(ROOT) + core.validate_family(ROOT)
            if errors:
                raise ValueError('; '.join(errors))
            records = core.build(ROOT)
            core.write_json(ROOT / 'data/records.json', records)
            core.write_json(ROOT / 'analysis/current-status.json', core.audit(ROOT, records))
            print('Built ' + str(len(records)) + ' attributed records')
            return 0
        if args.command == 'validate':
            errors = core.validate(ROOT)
            print(json.dumps({'valid': not errors, 'errors': errors}, indent=2))
            return bool(errors)
        if args.command == 'verify-export':
            errors = core.verify_export(ROOT, ROOT / args.directory)
            print(json.dumps({'valid': not errors, 'errors': errors}, indent=2))
            return bool(errors)
        errors = core.validate(ROOT)
        if errors:
            raise ValueError('; '.join(errors))
        records = core.read_json(ROOT / 'data/records.json')
        if args.command == 'audit':
            print(json.dumps(core.audit(ROOT, records), ensure_ascii=False, indent=2))
        elif args.command == 'frequency':
            if args.language not in {r['language'] for r in records}:
                raise ValueError('Unknown language partition')
            print(json.dumps(core.frequency(records, args.language), ensure_ascii=False, indent=2))
        elif args.command == 'search':
            result = [{'record_id': r['record_id'], 'label': r['label'], 'language': r['language'],
                       'line': l['label'], 'text': l['text'], 'source': r['source'],
                       'source_locator': l['source_locator'], 'analysis_eligible': l['analysis_eligible']}
                      for r in records if not args.language or r['language'] == args.language
                      for l in r['lines'] if args.query.casefold() in l['text'].casefold()]
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == 'export':
            core.export(ROOT, ROOT / args.output)
            print('Exported ' + str(len(records)) + ' attributed records')
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
