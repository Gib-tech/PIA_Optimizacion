"""Prepare challenge fields and place reachable fixed A/B/C identities."""
import unreal,os,sys
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
sys.path.insert(0,os.path.join(root,'Tools/UnrealPython'))
from delivery_save_schema import FIELDS
R='/Game/ThirdPerson/Blueprints/Entrega/'
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_name()=='Nivel_Entrega'
lib=unreal.BlueprintEditorLibrary
def add(bp,name,kind):
 try:unreal.get_default_object(bp.generated_class()).get_editor_property(name);return
 except Exception:pass
 typ=lib.get_object_reference_type(unreal.load_class(None,kind)) if kind.startswith('/') else lib.get_basic_type_by_name(kind)
 assert lib.add_member_variable(bp,name,typ),(name,kind)

director=unreal.load_asset(R+'BP_DirectorEntrega')
for name,kind in {'OrderCode':'int','MissionElapsed':'real','CurrentBeacon':'/Script/Engine.StaticMeshActor'}.items():add(director,name,kind)
gi=unreal.load_asset('/Game/LevelMenu/BP_GameInstance');add(gi,'LastBeaconOrder','int')
save=unreal.load_asset(R+'BP_DeliverySave')
for name in ['OrderCode','MissionElapsed']:add(save,name,FIELDS[name])
label=unreal.load_asset(R+'BP_BeaconLabel')
if not label:
 factory=unreal.BlueprintFactory();factory.set_editor_property('parent_class',unreal.TextRenderActor)
 label=unreal.AssetToolsHelpers.get_asset_tools().create_asset('BP_BeaconLabel',R.rstrip('/'),unreal.Blueprint,factory)
add(label,'Beacon',R+'BP_BeaconEntrega.BP_BeaconEntrega_C')
lib.set_blueprint_variable_instance_editable(label,'Beacon',True)
for bp in [director,gi,save,label]:
 lib.compile_blueprint(bp)
 if bp==gi:unreal.get_default_object(bp.generated_class()).set_editor_property('LastBeaconOrder',-1)
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)

actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
d=next(a for a in actors.get_all_level_actors() if a.get_class().get_name()=='BP_DirectorEntrega_C')
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
mesh=unreal.load_asset('/Game/ThirdPerson/Environment/Baliza/SM_Baliza')
assert mesh.get_bounds().box_extent.z>70,'Beacon import must be 150 cm tall'
# The existing eastern route was already walkable; the other two targets spread
# across the final courtyard, before its extraction bulkhead.
positions=[(-2600,-8500,0),(0,-9100,0),(2600,-8500,0)]
for i,pos in enumerate(positions,1):
 b=d.get_editor_property('Baliza'+str(i));b.set_actor_location(unreal.Vector(*pos),False,True)
 b.set_actor_scale3d(unreal.Vector(1,1,1));b.set_actor_label('Baliza_'+chr(64+i))
 b.static_mesh_component.set_static_mesh(mesh)
 b.static_mesh_component.set_editor_property('override_materials',[])
 b.static_mesh_component.set_collision_profile_name('BlockAllDynamic')
 approach=b.get_editor_property('ApproachPoint')
 approach.set_actor_location(unreal.Vector(pos[0],pos[1]+190,0),False,True)
 b.set_editor_property('RequiredZone',d.get_editor_property('Zona2'))
 labelname='Nombre_Baliza_'+chr(64+i)
 a=next((a for a in actors.get_all_level_actors() if a.get_actor_label()==labelname),None)
 if not a:a=actors.spawn_actor_from_class(label.generated_class(),unreal.Vector(pos[0],pos[1],190))
 a.set_actor_label(labelname);a.set_folder_path('Mision/Balizas');a.set_editor_property('Beacon',b)
 c=a.text_render;c.set_world_size(38);c.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
 c.set_text('BALIZA '+chr(64+i));c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
 c.set_text_render_color(unreal.Color(170,230,255,255))
 # Keep local refuge candidates available after moving channeling to this patio.
 for side in [-1,1]:
  name='Refugio_Baliza_'+chr(64+i)+('_Izq' if side<0 else '_Der')
  point=next((a for a in actors.get_all_level_actors() if a.get_actor_label()==name),None)
  if not point:point=actors.spawn_actor_from_class(unreal.TargetPoint,unreal.Vector())
  point.set_actor_label(name);point.set_folder_path('Combate/RefugiosLocales')
  point.set_actor_location(unreal.Vector(pos[0]+side*1200,pos[1]+190,0),False,True)
  point.set_editor_property('tags',['RefugioRehen'])
unreal.SystemLibrary.execute_console_command(world,'RebuildNavigation')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('BEACON_SEQUENCE_PREPARED')
