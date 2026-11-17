"""Inspección previa de cielo, rutas de daño y paredes; no modifica assets."""
import unreal, os, json
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
folder=os.path.join(root,'Intermediate/inspect/daynight-attacks');os.makedirs(folder,exist_ok=True)
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not sub.get_game_world()
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
rows=[]
for a in actors:
 label=a.get_actor_label()
 if any(k in label.lower() for k in ['wall','pared','luz','light','sistema','destruible','postprocess']):
  center,extent=a.get_actor_bounds(False)
  row={'label':label,'class':a.get_class().get_name(),'pos':str(a.get_actor_location()),'rot':str(a.get_actor_rotation()),'center':[center.x,center.y,center.z],'extent':[extent.x,extent.y,extent.z]}
  if isinstance(a,unreal.Light):row['intensity']=a.light_component.intensity
  rows.append(row)
for name in ['BP_SistemasComplementarios','BP_PlayerEntrega','BP_DestruibleEntrega']:
 bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/'+name)
 task=unreal.AssetExportTask();task.object=bp;task.filename=os.path.join(folder,name+'.t3d');task.automated=True;task.prompt=False;task.replace_identical=True;assert unreal.Exporter.run_asset_export_task(task)
with open(os.path.join(folder,'scene-before.json'),'w',encoding='utf-8') as f:json.dump(rows,f,ensure_ascii=False,indent=2)
unreal.log('DAYNIGHT_INSPECT '+str({'helper':hasattr(unreal,'DeliveryBlueprintBuilder'),'actors':len(rows)}))
