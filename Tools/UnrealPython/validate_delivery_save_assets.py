"""Compile/export the final save integration and open the delivery map for review."""
import unreal, os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert level.load_level('/Game/ThirdPerson/Maps/Nivel_Entrega')
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
unreal.SystemLibrary.execute_console_command(world,'viewmode lit')
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
paths=[
    '/Game/LevelMenu/BP_GameInstance','/Game/Menu/Menu_Inicio',
    '/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySave',
    '/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager',
    '/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega',
    '/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega',
]
for path in paths:
    bp=unreal.load_asset(path);unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
    task=unreal.AssetExportTask();task.object=bp;task.filename=os.path.join(root,'Intermediate/inspect/live',bp.get_name()+'.t3d')
    task.automated=True;task.prompt=False;task.replace_identical=True
    assert unreal.Exporter.run_asset_export_task(task)
    unreal.log('SAVE_VALIDATED '+path)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
assert len([a for a in actors if a.get_class().get_name()=='BP_DeliverySaveManager_C'])==1
level.save_current_level()
unreal.log('DELIVERY_SAVE_ASSETS_VALIDATED')
