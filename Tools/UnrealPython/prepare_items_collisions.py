"""Mesa con UCX, robot bloqueante y tres objetos recogibles persistentes."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());R='/Game/ThirdPerson/Blueprints/Entrega/';ART='/Game/ThirdPerson/Environment/Complementos'
assets=unreal.EditorAssetLibrary;lib=unreal.BlueprintEditorLibrary;tools=unreal.AssetToolsHelpers.get_asset_tools()
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
task=unreal.AssetImportTask();task.filename=os.path.join(root,'Tools/ArtSource/Complementos/SM_ConsolaTecnico.fbx');task.destination_path=ART;task.destination_name='SM_ConsolaTecnico';task.automated=True;task.save=True;task.replace_existing=True
options=unreal.FbxImportUI();options.import_materials=False;options.import_textures=False;options.static_mesh_import_data.combine_meshes=True;options.static_mesh_import_data.auto_generate_collision=False;options.static_mesh_import_data.one_convex_hull_per_ucx=True;task.options=options;tools.import_asset_tasks([task])
mesh=unreal.load_asset(ART+'/SM_ConsolaTecnico');assert mesh
for i,slot in enumerate(mesh.static_materials):
 material=unreal.load_asset(ART+'/Materials/'+str(slot.material_slot_name).split('.')[0])
 if material:mesh.set_material(i,material)
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);options=unreal.EditorScriptingMeshReductionOptions(auto_compute_lod_screen_size=False,reduction_settings=[unreal.EditorScriptingMeshReductionSettings(percent_triangles=p,screen_size=s) for p,s in [(1,1),(.6,.45),(.3,.2),(.12,.07)]]);sm.set_lods(mesh,options);assets.save_loaded_asset(mesh,only_if_is_dirty=False)
extra=unreal.load_asset(R+'BP_SistemasComplementarios');save=unreal.load_asset(R+'BP_DeliverySave');robot=unreal.load_asset(R+'BP_TecnicoTemporal')
def add(bp,name,kind):
 try:unreal.get_default_object(bp.generated_class()).get_editor_property(name);return
 except Exception:pass
 typ=lib.get_object_reference_type(unreal.load_class(None,kind)) if kind.startswith('/') else lib.get_basic_type_by_name(kind)
 assert lib.add_member_variable(bp,name,typ),name
for i in range(1,4):
 add(extra,'ItemMesa'+str(i),'/Script/Engine.StaticMeshActor');lib.set_blueprint_variable_instance_editable(extra,'ItemMesa'+str(i),True)
 add(extra,'MesaRecogido'+str(i),'bool');add(save,'MesaRecogido'+str(i),'bool')
add(extra,'ObjetoEnMira','int')
add(extra,'bRobotEnMira','bool')
add(extra,'DestruibleEnMira',R+'BP_DestruibleEntrega.BP_DestruibleEntrega_C')
destructible=unreal.load_asset(R+'BP_DestruibleEntrega');add(destructible,'NombreDestruible','string');lib.set_blueprint_variable_instance_editable(destructible,'NombreDestruible',True)
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);fn=unreal.SubobjectDataBlueprintFunctionLibrary;handles=sub.k2_gather_subobject_data_for_blueprint(robot);collider=None
for h in handles:
 obj=fn.get_object(fn.get_data(h))
 if obj.get_name()=='ColisionRobot_GEN_VARIABLE':collider=obj
if not collider:
 h,error=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=handles[0],new_class=unreal.CapsuleComponent,blueprint_context=robot));assert not str(error),str(error);assert sub.rename_subobject(h,unreal.Text('ColisionRobot'));collider=fn.get_object(fn.get_data(h))
collider.set_editor_property('relative_location',unreal.Vector(0,0,79));collider.set_capsule_size(37,79,False);collider.set_collision_profile_name('BlockAllDynamic');collider.set_editor_property('can_ever_affect_navigation',True);collider.set_editor_property('hidden_in_game',True)
for bp in [extra,save,robot,destructible]:lib.compile_blueprint(bp);assets.save_loaded_asset(bp,only_if_is_dirty=False)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);placed={a.get_actor_label():a for a in actors.get_all_level_actors()};table=placed['Consola_Bruno'];table.modify();table.set_actor_location(unreal.Vector(-520,-960,0),False,True);table.static_mesh_component.modify();table.static_mesh_component.set_static_mesh(mesh);table.static_mesh_component.set_collision_profile_name('BlockAll');table.static_mesh_component.set_editor_property('can_ever_affect_navigation',True)
system=placed['Sistemas_Complementarios'];system.modify();rows=[]
names={'GC_box':'Caja','GC_Trash':'Basurero','GC_Banco':'Banca','GC_Barril':'Barril','GC_Car2':'Auto','GC_fuente':'Fuente'}
for a in actors.get_all_level_actors():
 if a.get_class().get_name()!='BP_DestruibleEntrega_C':continue
 gc=a.get_component_by_class(unreal.GeometryCollectionComponent);kind=gc.get_editor_property('rest_collection').get_name();a.modify();a.set_editor_property('NombreDestruible',names[kind]);a.set_actor_label('Destruible_'+names[kind])
 proxy=a.get_editor_property('Colision');proxy.modify();proxy.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK)
for i,(label,x,scale) in enumerate([('Muestra_Botiquin',-43,.75),('Muestra_Celda',0,.65),('Muestra_Credito',43,.6)],1):
 a=placed[label];a.modify();c=a.static_mesh_component;c.modify();c.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY);c.set_collision_response_to_all_channels(unreal.CollisionResponseType.ECR_IGNORE);c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK);c.set_editor_property('can_ever_affect_navigation',False)
 a.set_actor_scale3d(unreal.Vector(scale,scale,scale));a.set_actor_rotation(unreal.Rotator(),False)
 # La cota inferior visible del mesh coincide con la superficie real Z=92,5.
 bounds=c.get_editor_property('static_mesh').get_bounds();bottom=bounds.origin.z-bounds.box_extent.z;support_z=table.get_actor_location().z+92.5
 a.set_actor_location(table.get_actor_location()+unreal.Vector(x,18,92.5-bottom*scale+.1),False,True)
 system.set_editor_property('ItemMesa'+str(i),a);rows.append({'actor':label,'mesh_bottom_world_z':a.get_actor_location().z+bottom*scale,'support_top_world_z':support_z,'gap_cm':.1})
 # Añadir colisión simple si el modelo antiguo carecía de ella.
 item_mesh=c.get_editor_property('static_mesh')
 if sm.get_simple_collision_count(item_mesh)+sm.get_convex_collision_count(item_mesh)==0:sm.add_simple_collisions(item_mesh,unreal.ScriptingCollisionShapeType.BOX);assets.save_loaded_asset(item_mesh,only_if_is_dirty=False)
# Respetar el efecto existente al reconstruir los objetos de la mesa.
if not assets.does_asset_exist(R+'BP_PulsoTemporalVisual'):
 import sys
 sys.path.insert(0,os.path.join(root,'Tools','UnrealPython'))
 from prepare_pulse_visual import prepare as prepare_pulse
 prepare_pulse()
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
folder=os.path.join(root,'docs/validation/items-colisiones');os.makedirs(folder,exist_ok=True)
assert sm.get_convex_collision_count(mesh)==11,'La mesa debe importar sus once colisiones UCX'
with open(os.path.join(folder,'mesa-apoyo.json'),'w',encoding='utf-8') as f:json.dump({'source_ucx_hulls':11,'lod_count':sm.get_lod_count(mesh),'imported_convex_collision_count':sm.get_convex_collision_count(mesh),'items':rows,'robot_capsule_radius_cm':37,'robot_capsule_half_height_cm':79},f,ensure_ascii=False,indent=2)
unreal.log('ITEMS_COLLISIONS_PREPARED')
