"""Restaura el respaldo de esta revisión después de cerrar el editor/ejecutable."""
from pathlib import Path
import json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[1];BACKUP=ROOT/'Intermediate/inspect/robot-sky/backup';manifest=json.loads((BACKUP/'manifest.json').read_text(encoding='utf-8'))
original={row['path'].replace('\\','/') for row in manifest['files']};hashes={}
for row in manifest['files']:
 rel=row['path'].replace('\\','/');source=(BACKUP/rel).resolve();target=(ROOT/rel).resolve()
 assert source.is_relative_to(BACKUP.resolve()) and target.is_relative_to((ROOT/'Saved').resolve())
 assert hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256']
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target);assert hashlib.sha256(target.read_bytes()).hexdigest()==row['sha256'];hashes[rel]=row['sha256']
for name in ['TimeOut_Delivery_v1.sav','TimeOut_Options_v1.sav']:
 rel='Saved/SaveGames/'+name;target=(ROOT/rel).resolve();assert target.parent==(ROOT/'Saved/SaveGames').resolve()
 if rel not in original and target.exists():target.unlink()
(ROOT/'docs/validation/robot-cielo-inventario/datos-usuario-restaurados.json').write_text(json.dumps({'passed':True,'backup':'Respaldo nuevo previo a esta revisión; no se usa el respaldo histórico de modelos del equipo.','sha256':hashes,'isolated_native_user_dir':'Intermediate/inspect/revision-native-user'},ensure_ascii=False,indent=2),encoding='utf-8')
print('ROBOT_REVISION_USER_DATA_RESTORED')
