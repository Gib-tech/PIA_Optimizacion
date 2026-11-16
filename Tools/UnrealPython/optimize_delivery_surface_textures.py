"""Budget opaque environment textures; preserve source pixels and marketplace resources."""
import unreal,os,json
specs={
 '/Game/ThirdPerson/Environment/EscenarioIan/Textures/wood_inlaid_stone_wall_diff_2k':2048,
 '/Game/ThirdPerson/Environment/EscenarioIan/Textures/rock_boulder_dry_diff_2k':1024,
 '/Game/ThirdPerson/Environment/EscenarioIan/Textures/rock_wall_16_diff_2k':1024,
 '/Game/coast_sand_rocks_02_diff_2k':1024,
 '/Game/ganges_river_pebbles_diff_2k':1024,
 '/Game/mixed_rock_tiles_diff_2k':2048,
 '/Game/rock_boulder_dry_diff_2k':1024,
 '/Game/ThirdPerson/RecursosPropios/Modelos/woodtexture':1024,
 '/Game/ThirdPerson/RecursosPropios/Modelos/old_metal_24_diffuse':1024,
 '/Game/ThirdPerson/RecursosPropios/Modelos/ConcreteBench_ncl1_1':1024,
 '/Game/ThirdPerson/RecursosPropios/Modelos/Light_Pole1':1024}
report=[]
for path,cap in specs.items():
 tex=unreal.load_asset(path);assert isinstance(tex,unreal.Texture2D),path
 def snapshot():
  return {key:str(tex.get_editor_property(key)) for key in ['max_texture_size','never_stream','mip_gen_settings','compression_settings','compression_no_alpha','power_of_two_mode']}
 before=snapshot();tex.modify()
 tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_DEFAULT)
 tex.set_editor_property('compression_no_alpha',True)
 tex.set_editor_property('srgb',True);tex.set_editor_property('lod_group',unreal.TextureGroup.TEXTUREGROUP_WORLD)
 tex.set_editor_property('max_texture_size',cap);tex.set_editor_property('never_stream',False)
 tex.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP)
 tex.set_editor_property('lod_bias',0)
 # Resampling the full normalized UV domain preserves image placement; padding would not.
 if path.endswith(('woodtexture','old_metal_24_diffuse')):
  tex.set_editor_property('power_of_two_mode',unreal.TexturePowerOfTwoSetting.STRETCH_TO_POWER_OF_TWO)
 unreal.EditorAssetLibrary.save_loaded_asset(tex,only_if_is_dirty=False)
 report.append({'texture':path,'before':before,'after':snapshot(),'source_pixels_preserved':True})
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/surface_texture_budget.json'),'w') as f:json.dump(report,f,indent=2)
unreal.log('SURFACE_TEXTURE_BUDGET_APPLIED '+str(len(report)))
