"""Respaldo independiente y lectura del estado anterior a corregir los ítems."""
import unreal,os,json,shutil,hashlib
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());folder=os.path.join(root,'Intermediate/inspect/items-revision');os.makedirs(folder,exist_ok=True)
marker=os.path.join(folder,'backup/manifest.json')
if not os.path.isfile(marker):
 rows=[]
 for rel in ['Saved/SaveGames','Saved/Config/WindowsEditor/GameUserSettings.ini']:
  p=os.path.join(root,rel);files=[os.path.join(p,n) for n in os.listdir(p) if os.path.isfile(os.path.join(p,n))] if os.path.isdir(p) else [p] if os.path.isfile(p) else []
  for source in files:
   name=os.path.relpath(source,root);target=os.path.join(folder,'backup',name);os.makedirs(os.path.dirname(target),exist_ok=True);shutil.copy2(source,target);rows.append({'path':name,'sha256':hashlib.sha256(open(source,'rb').read()).hexdigest()})
 os.makedirs(os.path.dirname(marker),exist_ok=True)
 with open(marker,'w',encoding='utf-8') as f:json.dump({'files':rows},f,indent=2)
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);w=sub.get_game_world();unreal.log('ITEM_REVISION_STATE '+str({'pie':bool(w),'helper':hasattr(unreal,'DeliveryBlueprintBuilder')}))
if w:
 p=unreal.GameplayStatics.get_player_character(w,0)
 if p:unreal.log('CURRENT_HEALTH '+str(p.get_editor_property('BPC_Health').get_editor_property('Health')))
