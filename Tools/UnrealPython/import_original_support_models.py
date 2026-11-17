"""Integra modelos originales útiles y un estanque con superficie animada."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());src=os.path.join(root,'Tools/ArtSource/Complementos');ART='/Game/ThirdPerson/Environment/Complementos'
manifest=json.load(open(os.path.join(src,'manifest.json'),encoding='utf-8'));tools=unreal.AssetToolsHelpers.get_asset_tools();edit=unreal.MaterialEditingLibrary;assets=unreal.EditorAssetLibrary
def constant(m,val,prop,y):
 n=edit.create_material_expression(m,unreal.MaterialExpressionConstant,-250,y);n.r=val;edit.connect_material_property(n,'',prop);return n
def color(m,val,prop,y):
 n=edit.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-250,y);n.constant=unreal.LinearColor(*val[:3],1);edit.connect_material_property(n,'',prop);return n
materials={}
for name,col in manifest['palette'].items():
 path=ART+'/Materials/M_Apoyo_'+name;m=unreal.load_asset(path) or tools.create_asset('M_Apoyo_'+name,ART+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
 edit.delete_all_material_expressions(m);color(m,col,unreal.MaterialProperty.MP_BASE_COLOR,0)
 constant(m,.65 if name in ['Metal','Bronce'] else .05,unreal.MaterialProperty.MP_METALLIC,160)
 constant(m,.55 if name in ['Concreto','Goma'] else .36,unreal.MaterialProperty.MP_ROUGHNESS,250)
 if name=='Cian':color(m,[v*1.3 for v in col[:3]],unreal.MaterialProperty.MP_EMISSIVE_COLOR,400)
 edit.recompile_material(m);assets.save_loaded_asset(m,only_if_is_dirty=False);materials['M_Apoyo_'+name]=m
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for row in manifest['models']:
 task=unreal.AssetImportTask();task.filename=os.path.join(src,row['name']+'.fbx');task.destination_path=ART;task.destination_name=row['name'];task.automated=True;task.save=True;task.replace_existing=True
 opt=unreal.FbxImportUI();opt.set_editor_property('import_materials',False);opt.set_editor_property('import_textures',False)
 opt.static_mesh_import_data.set_editor_property('combine_meshes',True);opt.static_mesh_import_data.set_editor_property('auto_generate_collision',True);task.options=opt
 tools.import_asset_tasks([task]);mesh=unreal.load_asset(ART+'/'+row['name'])
 assert mesh
 for i,slot in enumerate(mesh.static_materials):
  key=str(slot.material_slot_name).split('.')[0]
  if key in materials:mesh.set_material(i,materials[key])
 options=unreal.EditorScriptingMeshReductionOptions(auto_compute_lod_screen_size=False,reduction_settings=[unreal.EditorScriptingMeshReductionSettings(percent_triangles=x,screen_size=y) for x,y in [(1,1),(.6,.45),(.3,.2),(.12,.07)]])
 sm.set_lods(mesh,options);assets.save_loaded_asset(mesh,only_if_is_dirty=False)
waterpath=ART+'/Materials/M_AguaRetencion';water=unreal.load_asset(waterpath) or tools.create_asset('M_AguaRetencion',ART+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
edit.delete_all_material_expressions(water);water.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT)
water.set_editor_property('two_sided',True);water.set_editor_property('translucency_lighting_mode',unreal.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
color(water,[.015,.13,.17],unreal.MaterialProperty.MP_BASE_COLOR,0);constant(water,.15,unreal.MaterialProperty.MP_ROUGHNESS,160);constant(water,.7,unreal.MaterialProperty.MP_SPECULAR,220);constant(water,.75,unreal.MaterialProperty.MP_OPACITY,280)
panner=edit.create_material_expression(water,unreal.MaterialExpressionPanner,-650,400)
assert unreal.DeliveryBlueprintBuilder.set_property_text(panner,'SpeedX','.018')
assert unreal.DeliveryBlueprintBuilder.set_property_text(panner,'SpeedY','.012')
sample=edit.create_material_expression(water,unreal.MaterialExpressionTextureSample,-400,400);sample.texture=unreal.load_asset('/Game/ParagonKallari/FX/Textures/Water/T_Water_N');sample.sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL
edit.connect_material_expressions(panner,'',sample,'Coordinates');edit.connect_material_property(sample,'RGB',unreal.MaterialProperty.MP_NORMAL)
edit.recompile_material(water);assets.save_loaded_asset(water,only_if_is_dirty=False)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
def prop(label,name,loc,scale=1):
 a=placed.get(label) or actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*loc));a.modify();a.set_actor_label(label);a.set_folder_path('Entrega/Complementos');a.set_editor_property('is_spatially_loaded',False)
 a.static_mesh_component.modify();a.static_mesh_component.set_static_mesh(unreal.load_asset(ART+'/'+name));a.set_actor_scale3d(unreal.Vector(scale,scale,scale));a.static_mesh_component.set_collision_profile_name('NoCollision');return a
for i in range(1,5):
 a=placed['Suministro_Temporal_'+str(i)];a.modify();a.static_mesh_component.modify();a.static_mesh_component.set_static_mesh(unreal.load_asset(ART+'/SM_CajaSuministros'));a.static_mesh_component.set_collision_profile_name('NoCollision');a.set_actor_scale3d(unreal.Vector(1,1,1));pos=a.get_actor_location();a.set_actor_location(unreal.Vector(pos.x,pos.y,2),False,True)
table=prop('Consola_Bruno','SM_ConsolaTecnico',(-520,-960,0));table.static_mesh_component.set_collision_profile_name('BlockAll')
for label,name,x,scale in [('Muestra_Botiquin','SM_BotiquinTemporal',-43,.75),('Muestra_Celda','SM_CeldaTemporal',0,.65),('Muestra_Credito','SM_CreditoCronal',43,.6)]:
 a=prop(label,name,(-520+x,-942,95),scale);bounds=a.static_mesh_component.get_editor_property('static_mesh').get_bounds();bottom=bounds.origin.z-bounds.box_extent.z
 a.set_actor_location(unreal.Vector(-520+x,-942,92.6-bottom*scale),False,True)
 a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY);a.static_mesh_component.set_collision_response_to_all_channels(unreal.CollisionResponseType.ECR_IGNORE);a.static_mesh_component.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK)
pond=prop('Lago_Retencion_Borde','SM_EstanqueRetencion',(3000,-1850,2))
pond.static_mesh_component.set_collision_profile_name('BlockAll')
surface=placed.get('Lago_Retencion_Agua') or actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(3000,-1850,5))
surface.modify();surface.set_actor_label('Lago_Retencion_Agua');surface.set_folder_path('Entrega/Complementos');surface.set_editor_property('is_spatially_loaded',False)
surface.static_mesh_component.modify();surface.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cylinder'));surface.set_actor_scale3d(unreal.Vector(5.7,5.7,.015));surface.static_mesh_component.set_material(0,water);surface.static_mesh_component.set_collision_profile_name('NoCollision');surface.static_mesh_component.set_cast_shadow(False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
if dirty:unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
unreal.log('ORIGINAL_MODELS_AND_WATER_INSTALLED')
