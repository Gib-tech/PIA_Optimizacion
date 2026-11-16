"""Arrange the existing kit as a compound, with purposeful shelters and local light."""
import unreal,os,json,math
root=unreal.Paths.project_dir();ART='/Game/ThirdPerson/Environment/Atmosphere';KIT='/Game/ThirdPerson/Environment/Progression/'
level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem);sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world();assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert unreal.DeliveryBlueprintBuilder.load_editor_region(world,unreal.Vector(-6500,-12500,-1000),unreal.Vector(6500,1000,3000))
tools=unreal.AssetToolsHelpers.get_asset_tools();sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
placed={a.get_actor_label():a for a in sub.get_all_level_actors()}
buildings=json.load(open(os.path.join(root,'Tools/ArtSource/Atmosphere/building_layout.json')))
names=['SM_Walls_'+b['name'] for b in buildings]+['SM_'+kind+'_'+room for kind in ['Roof','UpperWalls'] for room in ['Rescate','Deposito']]
reimport_flag=os.path.join(root,'Intermediate/inspect/reimport_compound_walls.flag')
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
for name in names:
    if unreal.EditorAssetLibrary.does_asset_exist(ART+'/'+name) and name.startswith('SM_Walls_') and not os.path.exists(reimport_flag):continue
    options=unreal.FbxImportUI();options.automated_import_should_detect_type=False;options.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
    options.import_materials=False;options.import_textures=False;options.static_mesh_import_data.combine_meshes=True;options.static_mesh_import_data.auto_generate_collision=False
    task=unreal.AssetImportTask();task.filename=os.path.join(root,'Tools/ArtSource/Atmosphere',name+'.fbx');task.destination_path=ART;task.automated=True;task.save=True;task.options=options;task.replace_existing=True
    tools.import_asset_tasks([task])
def actor(label,cls,pos,folder='Escenario/Compound'):
    a=placed.get(label)
    if not a:a=sub.spawn_actor_from_class(cls,unreal.Vector(*pos));placed[label]=a
    a.modify()
    a.set_actor_label(label);a.set_folder_path(folder);a.set_actor_location(unreal.Vector(*pos),False,True);return a
for name in names:
    mesh=unreal.load_asset(ART+'/'+name);assert mesh,name
    for i,slot in enumerate(mesh.static_materials):
        if name.startswith('SM_Walls_'):
            mat=unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/'+str(slot.material_slot_name).split('.')[0])
            assert mat,(name,str(slot.material_slot_name))
        else:mat=unreal.load_asset(KIT+'M_DoorSteel') if '_Roof_' in name else unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/Sector'+('2' if name.endswith('Deposito') else '1'))
        mesh.set_material(i,mat)
    body=mesh.get_editor_property('body_setup')
    if not body:body=unreal.new_object(unreal.BodySetup,outer=mesh);mesh.set_editor_property('body_setup',body)
    body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
    body.set_editor_property('double_sided_geometry',True)
    settings=sm.get_nanite_settings(mesh);settings.enabled=name.startswith('SM_Walls_');sm.set_nanite_settings(mesh,settings)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
    origin=next((b['center'] for b in buildings if name=='SM_Walls_'+b['name']),[0,0,0])
    a=actor('Compound_'+name,unreal.StaticMeshActor,origin);c=a.static_mesh_component;c.modify();c.set_static_mesh(None);c.set_static_mesh(mesh);c.set_mobility(unreal.ComponentMobility.STATIC);c.set_collision_profile_name('BlockAll')
    c.set_editor_property('ld_max_draw_distance',0);c.set_editor_property('never_distance_cull',True);c.set_editor_property('bounds_scale',1.0)
for a in list(sub.get_all_level_actors()):
    if a.get_actor_label().startswith('Ian_Sector_') or a.get_actor_label() in ('Luz_Puntual_Rescate','Luz_Foco_Puerta1','Luz_Rect_Patio','FX_NS_Luces'):sub.destroy_actor(a)

# Move already fitted props by their visual ground center, retaining their pivots/scales.
positions={'LOD_Banco':(1100,-1900,0),'LOD_Tree1':(1450,-1750,0),'LOD_Car':(-4500,-7050,0),'LOD_Light_Pole':(1900,-8050,0),'LOD_fuente':(0,-7300,0),
 'Destruible_Caja':(520,-900,0),'Destruible_Basurero':(900,-1900,0),'Destruible_Banca':(2900,-3350,0),'Destruible_Barril':(-4500,-5300,0),'Destruible_Auto':(-3200,-7050,0),'Destruible_Fuente':(3200,-3800,0)}
for label,position in positions.items():
    a=placed[label]
    visible=a.get_component_by_class(unreal.GeometryCollectionComponent if label.startswith('Destruible_') else unreal.StaticMeshComponent)
    center,extent,sphere=unreal.SystemLibrary.get_component_bounds(visible)
    a.modify()
    desired=unreal.Vector(position[0],position[1],position[2]+extent.z)
    a.set_editor_property('is_spatially_loaded',False)
    a.set_actor_location(a.get_actor_location()+desired-center,False,True)
    a.set_folder_path('Escenario/Compound/Equipo')
    for c in a.get_components_by_class(unreal.PrimitiveComponent):
        c.modify()
        c.set_editor_property('ld_max_draw_distance',0);c.set_editor_property('never_distance_cull',True)
        c.set_editor_property('bounds_scale',1.0)
    if label.startswith('Destruible_'):
        assert unreal.DeliveryBlueprintBuilder.set_property_text(a,'PrimaryActorTick','(bStartWithTickEnabled=False)')
        a.get_component_by_class(unreal.GeometryCollectionComponent).set_simulate_physics(False)
        a.get_component_by_class(unreal.GeometryCollectionComponent).set_editor_property('generate_overlap_events',True)
        proxy=a.get_editor_property('Colision');proxy.modify()
        proxy.set_world_location(desired,False,False);proxy.set_world_scale3d(unreal.Vector(1,1,1));proxy.set_box_extent(extent,False)
        proxy.set_collision_profile_name('BlockAllDynamic');proxy.set_collision_object_type(unreal.CollisionChannel.ECC_DESTRUCTIBLE)
        proxy.set_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA,unreal.CollisionResponseType.ECR_IGNORE)
        proxy.set_editor_property('generate_overlap_events',True);proxy.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY)
        a.get_component_by_class(unreal.GeometryCollectionComponent).set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
for label,position in [('FX_NS_Hojas',(1450,-1750,250)),('FX_NS_Polvo',(-2660,-4550,40))]:
    a=placed.get(label)
    if a:a.modify();a.set_actor_location(unreal.Vector(*position),False,True)
for name,pos in [('Norte',(-2150,-4600,0)),('Sur',(-2150,-5500,0))]:
    point=actor('Refugio_Deposito_Entrada'+name,unreal.TargetPoint,pos,'Combate/RefugiosLocales')
    point.set_editor_property('tags',['RefugioRehen']);point.set_editor_property('is_spatially_loaded',False)

edit=unreal.MaterialEditingLibrary
lamp=unreal.load_asset(ART+'/M_LampWarm')
if not lamp:
    lamp=tools.create_asset('M_LampWarm',ART,unreal.Material,unreal.MaterialFactoryNew())
    color=edit.create_material_expression(lamp,unreal.MaterialExpressionConstant3Vector,-200,0);color.constant=unreal.LinearColor(4.0,2.8,1.5,1)
    edit.connect_material_property(color,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR);edit.recompile_material(lamp);unreal.EditorAssetLibrary.save_loaded_asset(lamp)
def fixture(label,pos,dim):
    a=actor('Lampara_'+label,unreal.StaticMeshActor,pos,'Escenario/Compound/Luminarias');c=a.static_mesh_component;c.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));c.set_material(0,lamp);c.set_mobility(unreal.ComponentMobility.STATIC)
    a.set_actor_scale3d(unreal.Vector(*(d/100 for d in dim)));c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);c.set_editor_property('ld_max_draw_distance',0);c.set_editor_property('never_distance_cull',True)
lights=[]
for name,cls,pos,radius,power,rotation in [
 ('Rescate',unreal.RectLight,(0,-650,395),1000,3500,(-90,0,0)),
 ('Deposito',unreal.PointLight,(-3650,-4950,350),700,1800,(0,0,0)),
 ('AccesoPatio',unreal.SpotLight,(1900,-8050,355),1100,3500,(-55,180,0))]:
    a=actor('Luz_Compound_'+name,cls,pos,'Escenario/Compound/Luminarias');a.set_actor_rotation(unreal.Rotator(pitch=rotation[0],yaw=rotation[1],roll=rotation[2]),True);c=a.light_component;c.modify();c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_editor_property('intensity_units',unreal.LightUnits.LUMENS);c.set_intensity(power);c.set_light_color(unreal.LinearColor(1,.78,.52,1));c.set_editor_property('attenuation_radius',radius)
    c.set_cast_shadows(name=='Rescate');c.set_editor_property('max_draw_distance',2400);c.set_editor_property('max_distance_fade_range',350)
    c.set_editor_property('volumetric_scattering_intensity',0)
    if name=='Rescate':c.set_editor_property('source_width',180);c.set_editor_property('source_height',25);fixture(name,(0,-650,410),(200,40,10))
    elif name=='Deposito':fixture(name,(-3650,-4950,370),(50,50,16))
    else:
        c.set_editor_property('inner_cone_angle',25);c.set_editor_property('outer_cone_angle',42);fixture(name,(1900,-8050,370),(35,45,20))
    lights.append({'name':name,'type':cls.__name__,'radius':radius,'max_draw_distance':2400,'shadows':name=='Rescate','lumens':power})
for a in sub.get_all_level_actors():
    if isinstance(a,unreal.DirectionalLight):
        a.modify();a.light_component.modify()
        a.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);a.light_component.set_cast_shadows(True)
        a.set_actor_rotation(unreal.Rotator(pitch=-38,yaw=-28,roll=0),True);a.light_component.set_intensity(15000);a.light_component.set_light_color(unreal.LinearColor(1,.93,.82,1))
    elif isinstance(a,unreal.SkyLight):
        a.modify();a.light_component.modify()
        c=a.light_component;c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_cast_shadows(True);c.set_editor_property('real_time_capture',False);c.set_intensity(.65);c.recapture_sky()
    elif isinstance(a,unreal.PostProcessVolume) and a.get_actor_label()=='Iluminacion_Entrega':
        a.modify()
        settings=a.get_editor_property('settings')
        for key,value in {'override_dynamic_global_illumination_method':True,'dynamic_global_illumination_method':unreal.DynamicGlobalIlluminationMethod.LUMEN,'override_auto_exposure_bias':True,'auto_exposure_bias':-.75,'override_auto_exposure_speed_up':True,'auto_exposure_speed_up':4.,'override_auto_exposure_speed_down':True,'auto_exposure_speed_down':2.}.items():settings.set_editor_property(key,value)
        a.set_editor_property('settings',settings)
unreal.SystemLibrary.execute_console_command(world,'RebuildNavigation');level.save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
owned=[p for p in dirty if p.get_path_name().startswith(('/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/','/Game/ThirdPerson/Environment/Atmosphere/','/Game/ThirdPerson/Environment/EscenarioIan/'))]
unreal.EditorLoadingAndSavingUtils.save_packages(owned,only_dirty=True)
with open(os.path.join(root,'Intermediate/inspect/compound_scene.json'),'w') as f:json.dump({'buildings':buildings,'shelters':json.load(open(os.path.join(root,'Tools/ArtSource/Atmosphere/shelters.json'))),'props':positions,'lights':lights,'sky_real_time_capture':False,'sun_lux':15000,'model_distance_cull_cm':0,'visibility_and_lod_culling_only':True},f,indent=2)
unreal.log('COMPOUND_SCENE_READY')
if os.path.exists(reimport_flag):os.remove(reimport_flag)
