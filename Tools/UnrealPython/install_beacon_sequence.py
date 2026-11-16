"""Install the challenge, persistence and HUD, preserving current controls."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert hasattr(unreal,'DeliveryBlueprintBuilder')
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/'
for path in [R+'BP_DirectorEntrega',R+'BP_BeaconEntrega','/Game/ThirdPerson/Blueprints/Aliado/BTTask_ActivateBeacon',R+'BP_BeaconLabel',R+'BP_DeliverySaveManager','/Game/Menu/Menu_Inicio',R+'BP_HUD_Entrega']:
 bp=unreal.load_asset(path)
 unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
 assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs',bp.get_name()+'.t3d')),path
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(root,'Intermediate/inspect/live',bp.get_name()+'.t3d')
 t.automated=True;t.prompt=False;t.replace_identical=True;assert unreal.Exporter.run_asset_export_task(t)
 unreal.log('BEACON_INSTALLED '+path)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
