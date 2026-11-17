"""Sólo posiciones y recuadros. Guarda sin reconstruir ni compilar el Blueprint."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());folder=os.path.join(root,'Intermediate/inspect/robot-sky');plan=json.load(open(os.path.join(folder,'cinema-layout.json'),encoding='utf-8'))
bp=unreal.load_asset('/Game/ThirdPerson/Cinematics/BP_CinematicDirector');bp.modify()
for name,(x,y) in plan['positions'].items():
 n=unreal.find_object(None,bp.get_path_name()+':EventGraph.'+name);assert n,name;n.modify()
 assert unreal.DeliveryBlueprintBuilder.set_property_text(n,'NodePosX',str(x))
 assert unreal.DeliveryBlueprintBuilder.set_property_text(n,'NodePosY',str(y))
for c in plan['comments']:
 assert unreal.DeliveryBlueprintBuilder.add_layout_comment(bp,c['name'],c['title'],unreal.Vector2D(*c['position']),unreal.Vector2D(*c['size']),unreal.LinearColor(*c['color']))
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(folder,'cinema-after.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;assert unreal.Exporter.run_asset_export_task(t)
unreal.log('CINEMATIC_LAYOUT_APPLIED_WITHOUT_REBUILD')
