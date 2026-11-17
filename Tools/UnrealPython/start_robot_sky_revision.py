"""Respaldo nuevo de partidas y preferencias antes de probar esta revisión."""
import unreal,os,shutil,json,hashlib
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());folder=os.path.join(root,'Intermediate/inspect/robot-sky/backup');os.makedirs(folder,exist_ok=True)
marker=os.path.join(folder,'manifest.json')
if not os.path.exists(marker):
 report={'files':[]}
 for rel in ['Saved/SaveGames','Saved/Config/WindowsEditor/GameUserSettings.ini']:
  path=os.path.join(root,rel)
  files=[os.path.join(path,n) for n in os.listdir(path) if os.path.isfile(os.path.join(path,n))] if os.path.isdir(path) else [path] if os.path.isfile(path) else []
  for source in files:
   name=os.path.relpath(source,root);target=os.path.join(folder,name);os.makedirs(os.path.dirname(target),exist_ok=True);shutil.copy2(source,target)
   report['files'].append({'path':name,'sha256':hashlib.sha256(open(source,'rb').read()).hexdigest()})
 with open(marker,'w',encoding='utf-8') as f:json.dump(report,f,indent=2)
unreal.log('ROBOT_SKY_USER_BACKUP_READY')
