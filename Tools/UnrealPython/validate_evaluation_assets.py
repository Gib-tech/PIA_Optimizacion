"""Compile/export the owned evaluation Blueprints without counting unloaded WP actors."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/'
paths=[R+n for n in ['BP_DestruibleEntrega','BP_PlayerEntrega','BP_DirectorEntrega','BP_BeaconEntrega','BP_BeaconLabel','BP_DeliverySave','BP_DeliverySaveManager','BP_DeliveryInterface','BP_DeliveryOptions','BP_HUD_Entrega','BP_SenalExtraccion']]
paths+=['/Game/Menu/Menu_Pausa','/Game/Menu/Menu_Opciones','/Game/Menu/Menu_Inicio','/Game/ThirdPerson/Blueprints/Aliado/BTTask_ActivateBeacon']
for path in paths:
    bp=unreal.load_asset(path);assert bp,path
    unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
    task=unreal.AssetExportTask();task.object=bp;task.filename=os.path.join(root,'Intermediate/inspect/live',bp.get_name()+'.t3d')
    task.automated=True;task.prompt=False;task.replace_identical=True
    assert unreal.Exporter.run_asset_export_task(task),path
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert unreal.DeliveryBlueprintBuilder.is_partitioned(world)
bp=unreal.DeliveryBlueprintBuilder.get_level_blueprint(world);assert bp
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
task=unreal.AssetExportTask();task.object=bp;task.filename=os.path.join(root,'Intermediate/inspect/live/Nivel_Entrega_LevelBlueprint.t3d')
task.automated=True;task.prompt=False;task.replace_identical=True
assert unreal.Exporter.run_asset_export_task(task)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
with open(os.path.join(root,'Intermediate/inspect/evaluation_compile.json'),'w') as f:json.dump({'compiled_exported_assets':paths,'level_blueprint':bp.get_path_name(),'final_cook_is_compilation_gate':True},f,indent=2)
unreal.log('EVALUATION_ASSETS_COMPILED_EXPORTED')
