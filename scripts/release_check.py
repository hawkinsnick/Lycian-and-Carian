"""Offline release gate: source replay, negative tests and export roundtrip."""
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[1]
for args in [['-m','corpuskit','validate'], ['-m','unittest','discover','-s','tests','-v'], ['-m','corpuskit','verify-export','exports']]:
    result = subprocess.run([sys.executable,*args],cwd=ROOT)
    if result.returncode:
        raise SystemExit(result.returncode)
print('Release integrity passed; independent epigraphic review remains a separate gate.')
