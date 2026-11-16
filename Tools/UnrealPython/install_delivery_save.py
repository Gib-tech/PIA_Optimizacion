"""Install only the new save manager and the existing menu's EventGraph."""
import unreal
import os

assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
builder = unreal.DeliveryBlueprintBuilder
project = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
for path in ['/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager', '/Game/Menu/Menu_Inicio', '/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega', '/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega']:
    bp = unreal.load_asset(path)
    unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
    assert builder.install_graph(bp, os.path.join(project, 'Intermediate/inspect/delivery_graphs', bp.get_name()+'.t3d')), path
    unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)
    task = unreal.AssetExportTask()
    task.object = bp
    task.filename = os.path.join(project, 'Intermediate/inspect/live', bp.get_name()+'.t3d')
    task.automated = True
    task.prompt = False
    task.replace_identical = True
    unreal.Exporter.run_asset_export_task(task)
    unreal.log('SAVE_INSTALLED '+path)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
