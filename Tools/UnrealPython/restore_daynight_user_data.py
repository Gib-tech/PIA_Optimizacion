"""Restaura el respaldo propio y verifica hashes; ejecutar con editor cerrado."""
from pathlib import Path
import json,hashlib,shutil
root=Path(__file__).resolve().parents[2];backup=root/'Intermediate/inspect/daynight-attacks/user-backup'
manifest=json.loads((backup/'manifest.json').read_text(encoding='utf-8'));rows=[]
for row in manifest['files']:
 target=(root/row['path']).resolve();assert target.is_relative_to((root/'Saved').resolve())
 source=backup/row['path'];assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256']
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
 digest=hashlib.sha256(target.read_bytes()).hexdigest();assert digest==row['sha256'];rows.append({'path':row['path'],'sha256':digest})
report=root/'docs/validation/ciclo-luces-ataques/datos-usuario-restaurados.json'
report.write_text(json.dumps({'passed':True,'files':rows},indent=2),encoding='utf-8')
print('DAYNIGHT_USER_DATA_RESTORED',len(rows))
