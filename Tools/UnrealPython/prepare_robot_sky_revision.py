"""Integra BRUNO original y restaura un ciclo solar en lux con cielo nocturno."""
import unreal, os, json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/'; ART='/Game/ThirdPerson/Environment/RobotBRUNO'
assets=unreal.EditorAssetLibrary; tools=unreal.AssetToolsHelpers.get_asset_tools(); edit=unreal.MaterialEditingLibrary
manifest=json.load(open(os.path.join(root,'Tools/ArtSource/RobotBRUNO/manifest.json'),encoding='utf-8'))
materials={}
for name,col in manifest['palette'].items():
 m=unreal.load_asset(ART+'/Materials/M_BRUNO_'+name) or tools.create_asset('M_BRUNO_'+name,ART+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
 edit.delete_all_material_expressions(m)
 c=edit.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-300,0);c.constant=unreal.LinearColor(*col[:3],1);edit.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
 for y,value,prop in [(160,.75 if name in ['Metal','Chasis','Cobre'] else .05,unreal.MaterialProperty.MP_METALLIC),(260,.34 if name!='Goma' else .72,unreal.MaterialProperty.MP_ROUGHNESS)]:
  n=edit.create_material_expression(m,unreal.MaterialExpressionConstant,-300,y);n.r=value;edit.connect_material_property(n,'',prop)
 if name in ['Energia','Ambar']:
  e=edit.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-300,400);e.constant=unreal.LinearColor(*[v*3 for v in col[:3]],1);edit.connect_material_property(e,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
 edit.recompile_material(m);assets.save_loaded_asset(m,only_if_is_dirty=False);materials['M_BRUNO_'+name]=m
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for row in manifest['parts']:
 mesh=unreal.load_asset(ART+'/'+row['name'])
 if not mesh:
  task=unreal.AssetImportTask();task.filename=os.path.join(root,'Tools/ArtSource/RobotBRUNO',row['name']+'.fbx');task.destination_path=ART;task.destination_name=row['name'];task.automated=True;task.save=True
  opt=unreal.FbxImportUI();opt.import_materials=False;opt.import_textures=False;opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;task.options=opt;tools.import_asset_tasks([task]);mesh=unreal.load_asset(ART+'/'+row['name'])
 assert mesh,row['name']
 for i,slot in enumerate(mesh.static_materials):
  key=str(slot.material_slot_name).split('.')[0]
  if key in materials:mesh.set_material(i,materials[key])
 options=unreal.EditorScriptingMeshReductionOptions(auto_compute_lod_screen_size=False,reduction_settings=[unreal.EditorScriptingMeshReductionSettings(percent_triangles=x,screen_size=y) for x,y in [(1,1),(.6,.5),(.3,.25),(.12,.08)]])
 sm.set_lods(mesh,options);assets.save_loaded_asset(mesh,only_if_is_dirty=False)
lib=unreal.BlueprintEditorLibrary
def add(bp,name,kind):
 try:unreal.get_default_object(bp.generated_class()).get_editor_property(name);return
 except Exception:pass
 typ=lib.get_object_reference_type(unreal.load_class(None,kind)) if kind.startswith('/') else lib.get_basic_type_by_name(kind)
 assert lib.add_member_variable(bp,name,typ),name
systems=unreal.load_asset(R+'BP_SistemasComplementarios');robot=unreal.load_asset(R+'BP_TecnicoTemporal');save=unreal.load_asset(R+'BP_DeliverySave')
for name,kind in [('RobotEnergy','int'),('bFabricating','bool'),('FabricationProgress','real')]:add(systems,name,kind);add(save,name,kind)
for name,kind in [('SkyDome','/Script/Engine.StaticMeshActor'),('SkyMID','/Script/Engine.MaterialInstanceDynamic'),('Moon','/Script/Engine.DirectionalLight')]:
 add(systems,name,kind)
 if name!='SkyMID':lib.set_blueprint_variable_instance_editable(systems,name,True)
for name,kind in [('TiempoVisual','real'),('Sistema',R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C')]:add(robot,name,kind)
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);fn=unreal.SubobjectDataBlueprintFunctionLibrary
handles=sub.k2_gather_subobject_data_for_blueprint(robot)
def component(name,cls):
 for h in sub.k2_gather_subobject_data_for_blueprint(robot):
  o=fn.get_object(fn.get_data(h))
  if o.get_name()==name+'_GEN_VARIABLE':return o
 h,error=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=handles[0],new_class=cls,blueprint_context=robot));assert not str(error),str(error)
 assert sub.rename_subobject(h,unreal.Text(name));return fn.get_object(fn.get_data(h))
for name,part,z in [('ChasisRobot','Chasis',0),('CabezaRobot','Cabeza',121),('AroConversion','Aro',58)]:
 c=component(name,unreal.StaticMeshComponent);c.set_static_mesh(unreal.load_asset(ART+'/SM_BRUNO_'+part));c.set_editor_property('relative_location',unreal.Vector(0,0,z));c.set_editor_property('relative_rotation',unreal.Rotator(yaw=90));c.set_collision_profile_name('NoCollision');c.set_editor_property('can_ever_affect_navigation',False)
light=component('LuzConversion',unreal.PointLightComponent);light.set_editor_property('relative_location',unreal.Vector(35,0,85));light.set_editor_property('intensity',3);light.set_editor_property('attenuation_radius',110);light.set_light_color(unreal.LinearColor(.05,.7,1,1));light.set_cast_shadows(False)
for bp in [systems,robot,save]:lib.compile_blueprint(bp)
cdo=unreal.get_default_object(robot.generated_class());cdo.skeletal_mesh_component.set_skeletal_mesh_asset(None);cdo.skeletal_mesh_component.set_anim_instance_class(None);cdo.skeletal_mesh_component.set_collision_profile_name('NoCollision')
for bp in [systems,robot,save]:assets.save_loaded_asset(bp,only_if_is_dirty=False)
# Atmósfera física más estrellas propias; ningún cielo pintado congela la iluminación.
SKY='/Game/ThirdPerson/Environment/Complementos/Materials'
m=unreal.load_asset(SKY+'/M_CieloTemporal') or tools.create_asset('M_CieloTemporal',SKY,unreal.Material,unreal.MaterialFactoryNew())
edit.delete_all_material_expressions(m);m.set_editor_property('shading_model',unreal.MaterialShadingModel.MSM_UNLIT);m.set_editor_property('two_sided',True);m.set_editor_property('is_sky',True)
world=edit.create_material_expression(m,unreal.MaterialExpressionWorldPosition,-900,100);camera=edit.create_material_expression(m,unreal.MaterialExpressionCameraPositionWS,-900,260)
direction=edit.create_material_expression(m,unreal.MaterialExpressionSubtract,-650,100);edit.connect_material_expressions(world,'XYZ',direction,'A');edit.connect_material_expressions(camera,'',direction,'B')
night=edit.create_material_expression(m,unreal.MaterialExpressionScalarParameter,-650,400);assert unreal.DeliveryBlueprintBuilder.set_property_text(night,'ParameterName','NightAmount');assert unreal.DeliveryBlueprintBuilder.set_property_text(night,'DefaultValue','0')
stars=edit.create_material_expression(m,unreal.MaterialExpressionCustom,-350,170)
stars.set_editor_property('description','Estrellas procedurales y luz nocturna')
assert unreal.DeliveryBlueprintBuilder.set_property_text(stars,'OutputType','CMOT_Float3')
assert unreal.DeliveryBlueprintBuilder.set_property_text(stars,'Inputs','((InputName="Direction"),(InputName="Night"))')
stars.set_editor_property('code','''float3 d=normalize(Direction); float2 uv=float2(atan2(d.y,d.x)/6.2831853+.5,asin(clamp(d.z,-1,1))/3.14159265+.5); float2 p=uv*float2(1600,800); float2 cell=floor(p); float h=frac(sin(dot(cell,float2(127.1,311.7)))*43758.5453); float star=step(.998,h)*pow(saturate(1-length(frac(p)-.5)*2),8)*18; float horizon=saturate(d.z*8); return Night*(float3(.003,.006,.015)*(0.5+0.5*saturate(d.z))+star*float3(.7,.85,1)*horizon);''')
edit.connect_material_expressions(direction,'',stars,'Direction');edit.connect_material_expressions(night,'',stars,'Night')
atmo=edit.create_material_expression(m,unreal.MaterialExpressionSkyAtmosphereViewLuminance,-350,-150)
addsky=edit.create_material_expression(m,unreal.MaterialExpressionAdd,0,0);edit.connect_material_expressions(atmo,'',addsky,'A');edit.connect_material_expressions(stars,'',addsky,'B')
combined=addsky
for index in [0,1]:
 disk=edit.create_material_expression(m,unreal.MaterialExpressionSkyAtmosphereLightDiskLuminance,-350,650+index*180);disk.set_editor_property('light_index',index)
 plus=edit.create_material_expression(m,unreal.MaterialExpressionAdd,350+index*250,150);edit.connect_material_expressions(combined,'',plus,'A');edit.connect_material_expressions(disk,'',plus,'B');combined=plus
edit.connect_material_property(combined,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR);edit.recompile_material(m);assets.save_loaded_asset(m,only_if_is_dirty=False)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
system=placed['Sistemas_Complementarios'];technician=placed['Tecnico_Bruno'];technician.modify();technician.skeletal_mesh_component.modify();technician.skeletal_mesh_component.set_skeletal_mesh_asset(None);technician.skeletal_mesh_component.set_anim_instance_class(None);technician.set_actor_rotation(unreal.Rotator(yaw=216),False)
def spawn(label,cls):
 a=placed.get(label) or actors.spawn_actor_from_class(cls,unreal.Vector());a.modify();a.set_actor_label(label);a.set_folder_path('Entrega/Cielo');a.set_editor_property('is_spatially_loaded',False);return a
moon=spawn('Luz_Luna',unreal.DirectionalLight);moon.get_component_by_class(unreal.DirectionalLightComponent).modify();moon.get_component_by_class(unreal.DirectionalLightComponent).set_mobility(unreal.ComponentMobility.MOVABLE);moon.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property('atmosphere_sun_light',True);moon.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property('atmosphere_sun_light_index',1);moon.get_component_by_class(unreal.DirectionalLightComponent).set_intensity(0);moon.get_component_by_class(unreal.DirectionalLightComponent).set_light_color(unreal.LinearColor(.45,.6,1,1));moon.get_component_by_class(unreal.DirectionalLightComponent).set_editor_property('light_source_angle',.7);moon.set_actor_rotation(unreal.Rotator(pitch=145,yaw=-35),False)
dome=spawn('Cielo_Temporal',unreal.StaticMeshActor);dome.static_mesh_component.modify();dome.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/EngineSky/SM_SkySphere'));dome.set_actor_scale3d(unreal.Vector(5000,5000,5000));dome.static_mesh_component.set_material(0,m);dome.static_mesh_component.set_collision_profile_name('NoCollision');dome.static_mesh_component.set_cast_shadow(False);dome.static_mesh_component.set_editor_property('can_ever_affect_navigation',False)
sun=placed['Luz_Sol'];sun.modify();sun.get_component_by_class(unreal.DirectionalLightComponent).modify();sun.get_component_by_class(unreal.DirectionalLightComponent).set_intensity(14913);sun.set_actor_rotation(unreal.Rotator(pitch=-35,yaw=-35),False)
sky=placed['Luz_Ambiente'];sky.modify();sky.light_component.modify();sky.light_component.set_editor_property('real_time_capture',True);sky.light_component.set_editor_property('cubemap_resolution',128);sky.light_component.set_intensity(.65)
system.modify()
for field,obj in [('Tecnico',technician),('Sun',sun),('Sky',sky),('Moon',moon),('SkyDome',dome)]:system.set_editor_property(field,obj)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
if dirty:unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
unreal.log('ROBOT_SKY_PREPARED')
