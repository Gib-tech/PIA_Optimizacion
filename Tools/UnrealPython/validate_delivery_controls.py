"""Compile/export all touched interface assets and check single map managers."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
R='/Game/ThirdPerson/Blueprints/Entrega/'
paths=[R+'BP_DeliveryInterface',R+'BP_DeliveryOptions',R+'BP_PlayerEntrega',R+'BP_DirectorEntrega','/Game/Menu/Menu_Inicio','/Game/Menu/Menu_Pausa','/Game/Menu/Menu_Opciones']
out=[];root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
for path in paths:
 bp=unreal.load_asset(path);unreal.BlueprintEditorLibrary.compile_blueprint(bp)
 status='compiled and exported; cook must confirm no errors'
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 task=unreal.AssetExportTask();task.object=bp;task.filename=os.path.join(root,'Intermediate/inspect/live',bp.get_name()+'.t3d');task.automated=True;task.prompt=False;task.replace_identical=True
 assert unreal.Exporter.run_asset_export_task(task)
 out.append({'asset':path,'status':status})
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
for path in ['/Game/LevelMenu/MainMenuLevel','/Game/ThirdPerson/Maps/Nivel_Entrega']:
 assert levels.load_level(path)
 actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
 assert len([a for a in actors if a.get_class().get_name()=='BP_DeliveryInterface_C'])==1
 levels.save_current_level()
result={'passed':True,'blueprints':out,'one_interface_actor_in_each_map':True}
with open(os.path.join(root,'Intermediate/inspect/delivery_controls_compile_assertions.json'),'w') as f:json.dump(result,f,indent=2)
unreal.log('CONTROLS_VALIDATED '+json.dumps(result))
