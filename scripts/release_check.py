"""Offline release gate: source replay, negative tests and export roundtrip."""
from pathlib import Path
import json
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]

# Shared interoperability contract: fail releases if the machine-readable
# semantics required by sibling corpora are missing or drift structurally.
contract_path = ROOT / 'schemas' / 'interoperability-contract.json'
contract = json.loads(contract_path.read_text(encoding='utf-8'))
if contract.get('contract') != 'hawkinsnick-epigraphic-corpus-interoperability':
    raise SystemExit('Invalid interoperability contract identifier')
if contract.get('version') != '1.0.0':
    raise SystemExit('Unsupported interoperability contract version')
required = {
    'source_attribution_required': True,
    'source_integrity_hash_required': True,
    'uncertainty_preserved': True,
    'unknown_physical_object_count_is_null': True,
    'cross_language_pooling_default': False,
    'cross_project_links_create_independent_witnesses': False,
    'language_or_script_identity_inferred_from_links': False,
    'decipherment_claimed': False,
}
if contract.get('principles') != required:
    raise SystemExit('Interoperability principles drifted from contract 1.0.0')

for args in [['-m','corpuskit','validate'], ['-m','unittest','discover','-s','tests','-v'], ['-m','corpuskit','verify-export','exports']]:
    result = subprocess.run([sys.executable,*args],cwd=ROOT)
    if result.returncode:
        raise SystemExit(result.returncode)
print('Release integrity passed; independent epigraphic review remains a separate gate.')
