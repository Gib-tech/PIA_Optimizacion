"""Check final model draw distances in a fresh PIE, including Chaos components."""
import unreal,os,json
visibility_world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert visibility_world,'Start a fresh PIE first'
visibility_rows=[]
for visibility_actor in unreal.GameplayStatics.get_all_actors_of_class(visibility_world,unreal.Actor):
 for visibility_component in visibility_actor.get_components_by_class(unreal.PrimitiveComponent):
  if isinstance(visibility_component,unreal.StaticMeshComponent):visibility_asset=visibility_component.static_mesh
  elif isinstance(visibility_component,unreal.GeometryCollectionComponent):visibility_asset=visibility_component.get_editor_property('rest_collection')
  else:continue
  if not visibility_asset:continue
  if visibility_asset.get_name().startswith('SM_LOD_') or visibility_actor.get_class().get_name()=='BP_DestruibleEntrega_C' and isinstance(visibility_component,unreal.GeometryCollectionComponent):
   visibility_row={'asset':visibility_asset.get_name(),'actor':visibility_actor.get_name(),'ld_max_draw_distance':visibility_component.get_editor_property('ld_max_draw_distance'),'cached_max_draw_distance':visibility_component.get_editor_property('cached_max_draw_distance'),'never_distance_cull':visibility_component.get_editor_property('never_distance_cull')}
   assert visibility_row['ld_max_draw_distance']==0 and visibility_row['cached_max_draw_distance']==0 and visibility_row['never_distance_cull'],visibility_row
   visibility_rows.append(visibility_row)
assert len(visibility_rows)==11,len(visibility_rows)
assert sum(row['asset'] in ('GC_Car2','SM_LOD_Car') for row in visibility_rows)==2
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/model_visibility_runtime.json'),'w') as visibility_file:json.dump({'passed':True,'models':visibility_rows},visibility_file,indent=2)
unreal.log('ALL_11_MODELS_VISIBLE_WITH_ZERO_EFFECTIVE_CUTOFF')
