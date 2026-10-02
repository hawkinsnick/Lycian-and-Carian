"""Deterministic archive of tracked files only."""
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile
ROOT=Path(__file__).resolve().parents[1]
version=(ROOT/'VERSION').read_text().strip()
name=json.loads((ROOT/'project.json').read_text())['project']+'-'+version
out=ROOT/'dist';out.mkdir(exist_ok=True)
paths=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
if not any(paths):raise ValueError('No tracked release files')
with zipfile.ZipFile(out/(name+'.zip'),'w') as archive:
    for relative in sorted(p for p in paths if p):
        path=ROOT/relative
        if not path.is_file() or path.is_symlink():raise ValueError('Invalid release path')
        info=zipfile.ZipInfo(name+'/'+relative,date_time=(2026,10,2,0,0,0));info.external_attr=0o100644<<16
        archive.writestr(info,path.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
digest=hashlib.sha256((out/(name+'.zip')).read_bytes()).hexdigest()
(out/'SHA256SUMS').write_text(digest+'  '+name+'.zip\n')
print(name+'.zip: '+digest)
