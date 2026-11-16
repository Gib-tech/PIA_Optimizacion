"""Preserve the team's painted layers and provide visible five-texture unpainted terrain."""
import unreal,os,re
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
m=unreal.load_asset('/Game/Landscape');assert m
tools=unreal.AssetToolsHelpers.get_asset_tools();edit=unreal.MaterialEditingLibrary
backup='/Game/ThirdPerson/Environment/Evaluation/M_Landscape_Equipo_Original'
if not unreal.EditorAssetLibrary.does_asset_exist(backup):tools.duplicate_asset('M_Landscape_Equipo_Original','/Game/ThirdPerson/Environment/Evaluation',m)
def connect_final(final):
 data=unreal.find_object(None,m.get_path_name()+':LandscapeEditorOnlyData');assert data
 text='(Expression="/Script/Engine.MaterialExpressionBlendMaterialAttributes\''+final.get_path_name()+'\'")'
 assert unreal.DeliveryBlueprintBuilder.set_property_text(data,'MaterialAttributes',text)
 final.set_editor_property('desc','EvaluationTerrainBlend')
 edit.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
marker=unreal.find_object(None,m.get_path_name()+':MaterialExpressionBlendMaterialAttributes_0')
if marker and marker.get_editor_property('desc')=='EvaluationTerrainBlend':
 path=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/evaluation_terrain_material.t3d')
 task=unreal.AssetExportTask();task.object=m;task.filename=path;task.automated=True;task.prompt=False;task.replace_identical=True;assert unreal.Exporter.run_asset_export_task(task)
 text=open(path,encoding='utf-8-sig').read()
 for name,body in re.findall(r'Begin Object Name="(MaterialExpressionComponentMask_\d+)"([^\r]*[\s\S]*?)End Object',text):
  if 'MaterialExpressionEditorY=-1000' in body:
   mask=unreal.find_object(None,m.get_path_name()+':'+name);assert mask
   mask.set_editor_property('r',False);mask.set_editor_property('g',True)
   edit.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m)
 unreal.log('TERRAIN_FALLBACK_ALREADY_PRESENT')
elif marker:
 connect_final(marker)
else:
 for name in ['MaterialExpressionWorldPosition_0','MaterialExpressionComponentMask_0']:
  partial=unreal.find_object(None,m.get_path_name()+':'+name)
  if partial:edit.delete_material_expression(m,partial)
 def node(cls,x,y):return edit.create_material_expression(m,cls,x,y)
 def link(a,ap,b,bp):
  names=list(edit.get_material_expression_input_names(b))
  if bp=='Input' and bp not in names and names:bp=names[0]
  assert edit.connect_material_expressions(a,ap,b,bp),(a,b,bp,names)
 position=node(unreal.MaterialExpressionWorldPosition,-2500,-1200)
 uv=node(unreal.MaterialExpressionComponentMask,-2300,-1200);uv.set_editor_property('r',True);uv.set_editor_property('g',True);link(position,'',uv,'Input')
 tiling=node(unreal.MaterialExpressionMultiply,-2100,-1200);tiling.set_editor_property('const_b',.0025);link(uv,'',tiling,'A')
 y=node(unreal.MaterialExpressionComponentMask,-2300,-1000);y.set_editor_property('r',False);y.set_editor_property('g',True);link(position,'',y,'Input')
 textures=['mixed_rock_tiles_diff_2k','stone_wall_04_diff_2k','rock_wall_16_diff_2k','ganges_river_pebbles_diff_2k','coast_sand_rocks_02_diff_2k']
 samples=[]
 for i,name in enumerate(textures):
  sample=node(unreal.MaterialExpressionTextureSample,-1900,-1500+i*200)
  sample.texture=unreal.load_asset('/Game/'+name);assert sample.texture,name
  sample.set_editor_property('sampler_source',unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS)
  link(tiling,'',sample,'UVs');samples.append(sample)
 color=samples[0]
 for i,threshold in enumerate([-9200,-6600,-4500,-2800]):
  delta=node(unreal.MaterialExpressionSubtract,-1600+i*250,-1000);delta.set_editor_property('const_b',threshold);link(y,'',delta,'A')
  divide=node(unreal.MaterialExpressionDivide,-1600+i*250,-850);divide.set_editor_property('const_b',600);link(delta,'',divide,'A')
  add=node(unreal.MaterialExpressionAdd,-1600+i*250,-700);add.set_editor_property('const_b',.5);link(divide,'',add,'A')
  alpha=node(unreal.MaterialExpressionSaturate,-1600+i*250,-550);link(add,'',alpha,'Input')
  blend=node(unreal.MaterialExpressionLinearInterpolate,-1300+i*250,-1300);link(color,'RGB' if color in samples else '',blend,'A');link(samples[i+1],'RGB',blend,'B');link(alpha,'',blend,'Alpha');color=blend
 attributes=node(unreal.MaterialExpressionMakeMaterialAttributes,-200,-1000);link(color,'',attributes,'BaseColor')
 rough=node(unreal.MaterialExpressionConstant,-400,-800);rough.set_editor_property('r',.9);link(rough,'',attributes,'Roughness')
 weight=None
 for i,name in enumerate(['Pasto','Tierra','SueloCuadros','SueloLadrillos','SueloLadrilloOscuro']):
  sample=node(unreal.MaterialExpressionLandscapeLayerSample,-1400+i*210,-250);sample.set_editor_property('parameter_name',name)
  if weight is None:weight=sample
  else:
   add=node(unreal.MaterialExpressionAdd,-1300+i*210,-50);link(weight,'',add,'A');link(sample,'',add,'B');weight=add
 clamp=node(unreal.MaterialExpressionSaturate,-200,-200);link(weight,'',clamp,'Input')
 original=unreal.find_object(None,m.get_path_name()+':MaterialExpressionLandscapeLayerBlend_0');assert original
 final=node(unreal.MaterialExpressionBlendMaterialAttributes,200,-600)
 link(attributes,'',final,'A');link(original,'',final,'B');link(clamp,'',final,'Alpha')
 connect_final(final)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('TERRAIN_FIVE_TEXTURE_FALLBACK_READY')
