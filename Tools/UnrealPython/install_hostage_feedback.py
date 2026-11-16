"""Install the five requested feedback refinements and refresh affected function callers."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
builder=unreal.DeliveryBlueprintBuilder
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/';E='/Game/ThirdPerson/Blueprints/EnemigoIA/';A='/Game/ThirdPerson/Blueprints/Aliado/'
for folder,name in [(R,'BP_DestructibleDoor'),(R,'BP_PlayerEntrega'),(R,'BP_BeaconEntrega'),(A,'BTTask_ActivateBeacon'),(R,'BP_HUD_Entrega'),(E,'BTService_LocatePlayer'),(E,'BTService_ChargerSense')]:
 bp=unreal.load_asset(folder+name);unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
 assert builder.install_graph(bp,os.path.join(project,'Intermediate/inspect/delivery_graphs',name+'.t3d')),name
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(project,'Intermediate/inspect/live',name+'.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;unreal.Exporter.run_asset_export_task(t)
 unreal.log('FEEDBACK_INSTALLED '+name)
unreal.log('HOSTAGE_FEEDBACK_INSTALLED')
