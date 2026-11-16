"""Replace the Y bands with an authored surface-use map using existing textures."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.project_dir();ART='/Game/ThirdPerson/Environment/Atmosphere'
tools=unreal.AssetToolsHelpers.get_asset_tools();edit=unreal.MaterialEditingLibrary
task=unreal.AssetImportTask();task.filename=os.path.join(root,'Tools/ArtSource/Atmosphere/T_TerrainUseMask.png');task.destination_path=ART;task.automated=True;task.save=True;task.replace_existing=True
tools.import_asset_tasks([task]);mask=unreal.load_asset(ART+'/T_TerrainUseMask');assert mask
mask.set_editor_property('srgb',False);mask.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_MASKS)
mask.set_editor_property('address_x',unreal.TextureAddress.TA_CLAMP);mask.set_editor_property('address_y',unreal.TextureAddress.TA_CLAMP)
unreal.EditorAssetLibrary.save_loaded_asset(mask)
m=unreal.load_asset(ART+'/M_TerrenoRecorrido')
if not m:m=tools.create_asset('M_TerrenoRecorrido',ART,unreal.Material,unreal.MaterialFactoryNew())
edit.delete_all_material_expressions(m)
def node(cls,x,y):return edit.create_material_expression(m,cls,x,y)
def link(a,ap,b,bp):
    names=list(edit.get_material_expression_input_names(b))
    if bp=='Input' and bp not in names and names:bp=names[0]
    assert edit.connect_material_expressions(a,ap,b,bp),(a,b,bp,names)
pos=node(unreal.MaterialExpressionWorldPosition,-1800,0)
xy=node(unreal.MaterialExpressionComponentMask,-1600,0);xy.set_editor_property('r',True);xy.set_editor_property('g',True);link(pos,'',xy,'Input')
offset=node(unreal.MaterialExpressionConstant2Vector,-1700,220);offset.set_editor_property('r',6300);offset.set_editor_property('g',12000)
add=node(unreal.MaterialExpressionAdd,-1400,200);link(xy,'',add,'A');link(offset,'',add,'B')
uv=node(unreal.MaterialExpressionMultiply,-1200,200);uv.set_editor_property('const_b',1/12600);link(add,'',uv,'A')
control=node(unreal.MaterialExpressionTextureSample,-1000,300);control.texture=mask;control.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_MASKS);link(uv,'',control,'UVs')
samples=[]
# All surfaces already existed. Four genuinely different textures, with paving
# reused at a different scale inside rooms. No ornamental wall texture on paths.
for i,(name,scale,tint) in enumerate([
 ('coast_sand_rocks_02_diff_2k',1/500,(.78,.73,.66)),
 ('mixed_rock_tiles_diff_2k',1/360,(.88,.86,.82)),
 ('ganges_river_pebbles_diff_2k',1/220,(.62,.61,.59)),
 ('mixed_rock_tiles_diff_2k',1/250,(.68,.72,.75)),
 ('rock_boulder_dry_diff_2k',1/500,(.67,.65,.59))]):
    tile=node(unreal.MaterialExpressionMultiply,-1300,-700+i*160);tile.set_editor_property('const_b',scale);link(xy,'',tile,'A')
    tex=node(unreal.MaterialExpressionTextureSample,-1100,-700+i*160);tex.texture=unreal.load_asset('/Game/'+name);assert tex.texture
    tex.set_editor_property('sampler_source',unreal.SamplerSourceMode.SSM_WRAP_WORLD_GROUP_SETTINGS);link(tile,'',tex,'UVs')
    color=node(unreal.MaterialExpressionConstant3Vector,-850,-650+i*160);color.set_editor_property('constant',unreal.LinearColor(*tint,1))
    mul=node(unreal.MaterialExpressionMultiply,-650,-700+i*160);link(tex,'RGB',mul,'A');link(color,'',mul,'B');samples.append(mul)
color=samples[0]
for i,channel in enumerate(['R','G','B','A']):
    blend=node(unreal.MaterialExpressionLinearInterpolate,-400+i*240,-400)
    link(color,'',blend,'A');link(samples[i+1],'',blend,'B');link(control,channel,blend,'Alpha');color=blend
assert edit.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR)
rough=node(unreal.MaterialExpressionConstant,250,200);rough.set_editor_property('r',.92);edit.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
edit.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False)
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    if isinstance(a,unreal.LandscapeProxy):a.set_editor_property('landscape_material',m)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('COMPOUND_AUTHORED_TERRAIN_READY')
