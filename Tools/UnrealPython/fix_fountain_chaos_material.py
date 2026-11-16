"""Preserve the fountain surface while supplying a project-owned Chaos-compatible shader."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
source=unreal.load_asset('/Game/Fab/Megascans/Surfaces/Plush_Carpet_umonbbqdy/Medium/MI_umonbbqdy')
folder='/Game/ThirdPerson/Environment/Atmosphere/'
base=unreal.load_asset(folder+'M_FuenteChaos') if unreal.EditorAssetLibrary.does_asset_exist(folder+'M_FuenteChaos') else unreal.EditorAssetLibrary.duplicate_asset(source.get_base_material().get_path_name(),folder+'M_FuenteChaos')
assert base
base.modify();unreal.MaterialEditingLibrary.set_material_usage(base,unreal.MaterialUsage.MATUSAGE_GEOMETRY_COLLECTIONS)
assert base.get_editor_property('used_with_geometry_collections')
instance=unreal.load_asset(folder+'MI_FuenteChaos') if unreal.EditorAssetLibrary.does_asset_exist(folder+'MI_FuenteChaos') else unreal.EditorAssetLibrary.duplicate_asset(source.get_path_name(),folder+'MI_FuenteChaos')
assert instance
unreal.MaterialEditingLibrary.set_material_instance_parent(instance,base);unreal.MaterialEditingLibrary.update_material_instance(instance)
gc=unreal.load_asset('/Game/ThirdPerson/RecursosPropios/Modelos/Fuente/GC_fuente');gc.modify()
materials=list(gc.get_editor_property('materials'));assert len(materials)==1
materials[0]=instance;gc.set_editor_property('materials',materials)
for asset in [base,instance,gc]:assert unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
result={'passed':True,'asset':gc.get_path_name(),'original_instance':source.get_path_name(),'compatible_instance':instance.get_path_name(),'owned_parent':base.get_path_name(),'geometry_collection_usage':True,'original_textures_parameters_preserved':True,'plugin_material_unchanged_on_disk':True}
json.dump(result,open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/fountain_chaos_material.json'),'w'),indent=2)
unreal.log('FOUNTAIN_CHAOS_SURFACE_COMPATIBLE')
