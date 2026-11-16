"""Fit visible bulkheads to each checkpoint; no invisible route blockers."""
import unreal,math
R='/Game/ThirdPerson/Blueprints/Entrega/';ART='/Game/ThirdPerson/Environment/Progression/'
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);actors=list(sub.get_all_level_actors())
director=next(a for a in actors if a.get_class().get_name()=='BP_DirectorEntrega_C')
zones=[director.get_editor_property('Zona1'),director.get_editor_property('Zona2')]
beacon_info=[]
for i in [1,2,3]:
 old=director.get_editor_property('Baliza%d'%i)
 beacon_info.append((old,old.get_actor_location(),old.get_actor_scale3d(),old.static_mesh_component.static_mesh))
for z in zones:
 old=z.get_editor_property('Blocker')
 z.set_editor_property('Blocker',None)
 if old:sub.destroy_actor(old)
for a in actors:
 if a.get_actor_label().startswith('Progression_'):sub.destroy_actor(a)
def mesh(name,label,pos,scale=(1,1,1),collision=True):
 a=sub.spawn_actor_from_object(unreal.load_asset(ART+name),unreal.Vector(*pos));a.set_actor_label('Progression_'+label);a.set_folder_path('Escenario/Puertas');a.set_actor_scale3d(unreal.Vector(*scale));a.static_mesh_component.set_collision_profile_name('BlockAll' if collision else 'NoCollision');return a
for i,(cx,y,w,h) in enumerate([(-4.6,-4021,258,256),(-21,-6261,344,333),(0,-10200,600,350)],1):
 d=sub.spawn_actor_from_class(unreal.load_class(None,R+'BP_DestructibleDoor.BP_DestructibleDoor_C'),unreal.Vector(cx,y,0));d.set_actor_label('Progression_Puerta_%d'%i);d.set_folder_path('Escenario/Puertas');d.set_editor_property('BeaconIndex',i)
 c=d.static_mesh_component;c.set_mobility(unreal.ComponentMobility.MOVABLE);c.set_static_mesh(unreal.load_asset(ART+'SM_DoorPanel_%02d'%i));c.set_collision_profile_name('BlockAllDynamic');c.set_editor_property('generate_overlap_events',True)
 mesh('SM_DoorFrame_%02d'%i,'Marco_%d'%i,(cx,y,0),collision=False)
 # Slabs have a centimeter of overhang, preventing seams between modules.
 for side,(left,right) in enumerate([(-5500,cx-w/2),(cx+w/2,5500)]):
  n=math.ceil((right-left)/400);size=(right-left)/n
  for j in range(n):mesh('SM_BulkheadModule','Muro_%d_%d_%02d'%(i,side,j),(left+size*(j+.5),y,0),(size/400,1,1))
 mesh('SM_BulkheadModule','Dintel_%d'%i,(cx,y,h),(w/400,1,(420-h)/420))
 old,loc,scale,oldmesh=beacon_info[i-1]
 b=sub.spawn_actor_from_class(unreal.load_class(None,R+'BP_BeaconEntrega.BP_BeaconEntrega_C'),loc);b.set_actor_label('Progression_Baliza_%d'%i);b.set_folder_path('Mision/Balizas');b.set_actor_scale3d(scale);b.static_mesh_component.set_static_mesh(oldmesh);b.static_mesh_component.set_material(0,unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/M_Baliza_Pendiente'));b.set_editor_property('Index',i);b.set_editor_property('Door',d);b.set_editor_property('RequiredZone',zones[min(i-1,1)]);director.set_editor_property('Baliza%d'%i,b);sub.destroy_actor(old)
 approach=sub.spawn_actor_from_class(unreal.TargetPoint,unreal.Vector(loc.x,loc.y+180,0));approach.set_actor_label('Progression_Approach_%d'%i);approach.set_folder_path('Mision/Balizas');b.set_editor_property('ApproachPoint',approach)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
for a in sub.get_all_level_actors():
 if isinstance(a,unreal.RecastNavMesh):
  unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetBytePropertyByName',(a,'RuntimeGeneration',2))
unreal.SystemLibrary.execute_console_command(world,'RebuildNavigation')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('PROGRESSION_PLACED')
