"""Metric wall projection and visibility-driven mesh culling, without distance popping."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.project_dir();folder='/Game/ThirdPerson/Environment/Atmosphere'
tools=unreal.AssetToolsHelpers.get_asset_tools();edit=unreal.MaterialEditingLibrary
fn=unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions01/Texturing/WorldAlignedTexture');assert fn
mapping={}
for number,texname in [(1,'wood_inlaid_stone_wall_diff_2k'),(2,'rock_boulder_dry_diff_2k'),(3,'wood_inlaid_stone_wall_diff_2k'),(4,'rock_wall_16_diff_2k')]:
 name='M_WallMetric_'+texname.split('_diff')[0];mat=unreal.load_asset(folder+'/'+name)
 if not mat:mat=tools.create_asset(name,folder,unreal.Material,unreal.MaterialFactoryNew())
 edit.delete_all_material_expressions(mat)
 texture=edit.create_material_expression(mat,unreal.MaterialExpressionTextureObject,-600,0)
 texture.set_editor_property('texture',unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/Textures/'+texname))
 size=edit.create_material_expression(mat,unreal.MaterialExpressionConstant3Vector,-600,200);size.set_editor_property('constant',unreal.LinearColor(400,400,400,1))
 call=edit.create_material_expression(mat,unreal.MaterialExpressionMaterialFunctionCall,-250,0);call.set_editor_property('material_function',fn)
 assert edit.connect_material_expressions(texture,'',call,'TextureObject')
 assert edit.connect_material_expressions(size,'',call,'TextureSize')
 assert edit.connect_material_property(call,'XYZ Texture',unreal.MaterialProperty.MP_BASE_COLOR)
 rough=edit.create_material_expression(mat,unreal.MaterialExpressionConstant,-200,250);rough.set_editor_property('r',.85)
 edit.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS);mat.set_editor_property('two_sided',True)
 edit.recompile_material(mat);unreal.EditorAssetLibrary.save_loaded_asset(mat,only_if_is_dirty=False)
 mapping['/Game/ThirdPerson/Environment/EscenarioIan/Sector'+str(number)+'.Sector'+str(number)]=mat
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
report={'walls':[],'models':[],'world_tile_cm':[400,400,400]}
for a in actors:
 if a.get_actor_label().startswith(('LOD_','Destruible_')):
  a.modify();a.set_editor_property('is_spatially_loaded',False)
 # Editing a Blueprint component reconstructs its actor. Resolve each name again.
 component_names=[c.get_name() for c in a.get_components_by_class(unreal.PrimitiveComponent) if isinstance(c,(unreal.StaticMeshComponent,unreal.GeometryCollectionComponent))]
 for component_name in component_names:
  c=next(c for c in a.get_components_by_class(unreal.PrimitiveComponent) if c.get_name()==component_name)
  a.modify();c.modify()
  # No hard distance cut on visible world geometry. Frustum/occlusion and LODs remain.
  c.set_editor_properties({'ld_max_draw_distance':0.0,'never_distance_cull':True})
  c=next(c for c in a.get_components_by_class(unreal.PrimitiveComponent) if c.get_name()==component_name)
  changed=[]
  for i,mat in enumerate(c.get_materials()):
   if mat and mat.get_path_name() in mapping:
    c.set_material(i,mapping[mat.get_path_name()]);changed.append(i)
   elif mat and mat.get_path_name().startswith(folder+'/M_WallMetric_'):changed.append(i)
  if changed:report['walls'].append({'actor':a.get_actor_label(),'component':c.get_name(),'slots':changed})
  if a.get_actor_label().startswith(('LOD_','Destruible_')):report['models'].append({'actor':a.get_actor_label(),'component':c.get_name(),'max_distance':0,'never_distance_cull':True})
# Blueprint reconstruction can retain a serialized CachedMaxDrawDistance.
# Refresh it after every component edit, including the last reconstruction.
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 for c in a.get_components_by_class(unreal.PrimitiveComponent):
  if isinstance(c,(unreal.StaticMeshComponent,unreal.GeometryCollectionComponent)):
   c.set_cull_distance(1);c.set_cull_distance(0)
   assert c.get_editor_property('cached_max_draw_distance')==0,(a.get_actor_label(),c.get_name())
# The probe was created by this task and is not a deliverable resource.
if unreal.EditorAssetLibrary.does_asset_exist(folder+'/M_WallProjectionProbe'):unreal.EditorAssetLibrary.delete_asset(folder+'/M_WallProjectionProbe')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
owned=[p for p in dirty if p.get_path_name().startswith(('/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/','/Game/ThirdPerson/Environment/Atmosphere/'))]
unreal.EditorLoadingAndSavingUtils.save_packages(owned,only_dirty=True)
assert len(report['walls'])>=100,len(report['walls'])
with open(os.path.join(root,'Intermediate/inspect/wall_visibility_changes.json'),'w') as f:json.dump(report,f,indent=2)
unreal.log('METRIC_WALLS_AND_VISIBLE_MODELS '+str(len(report['walls']))+' wall components')
