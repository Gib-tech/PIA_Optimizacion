"""Install only the fractured actor and door graphs, preserving the mission and combat trees."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
for name in ['BP_DoorFragment','BP_DestructibleDoor']:
 bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/'+name);unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
 assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(project,'Intermediate/inspect/delivery_graphs',name+'.t3d')),name
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(project,'Intermediate/inspect/live',name+'.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;unreal.Exporter.run_asset_export_task(t)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('FRACTURED_DOOR_GRAPHS_INSTALLED')
