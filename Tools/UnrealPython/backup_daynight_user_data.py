"""Respaldo independiente de partidas/preferencias antes de las pruebas de esta revisión."""
from pathlib import Path
import hashlib,json,shutil
root=Path(__file__).resolve().parents[2];backup=root/'Intermediate/inspect/daynight-attacks/user-backup'
assert not (backup/'manifest.json').exists(),'El respaldo de esta revisión ya existe'
rows=[]
for relative in ['Saved/SaveGames','Saved/Config/WindowsEditor/GameUserSettings.ini']:
 source=root/relative
 files=list(source.rglob('*')) if source.is_dir() else [source] if source.is_file() else []
 for file in files:
  if not file.is_file():continue
  rel=file.relative_to(root);dest=backup/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(file,dest)
  rows.append({'path':rel.as_posix(),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
backup.mkdir(parents=True,exist_ok=True)
(backup/'manifest.json').write_text(json.dumps({'files':rows},indent=2),encoding='utf-8')
print('DAYNIGHT_USER_DATA_BACKED_UP',len(rows))
