"""Install interface before widget callers, keeping native editing helper out of gameplay."""
import unreal, os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/'
paths=[R+'BP_DeliveryInterface','/Game/Menu/Menu_Pausa','/Game/Menu/Menu_Opciones','/Game/Menu/Menu_Inicio',R+'BP_PlayerEntrega',R+'BP_DirectorEntrega']
for path in paths:
    bp=unreal.load_asset(path)
    unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
    assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs',bp.get_name()+'.t3d')),path
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
    t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(root,'Intermediate/inspect/live',bp.get_name()+'.t3d')
    t.automated=True;t.prompt=False;t.replace_identical=True
    assert unreal.Exporter.run_asset_export_task(t)
    unreal.log('CONTROLS_INSTALLED '+path)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
