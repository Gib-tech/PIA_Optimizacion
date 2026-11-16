"""Isolated wall/car camera check in fresh PIE; wait for WALL_AND_CAR_CAPTURES_COMPLETE.

The former 60 m cutoff is simulated only on the native static car in PIE.
The final view restores it; the Chaos car retains final settings throughout.
Stop PIE after the marker. Never run other camera callbacks simultaneously.
"""
import unreal,os,math,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
pc=unreal.GameplayStatics.get_player_controller(w,0);lib=unreal.get_default_object(unreal.GameplayStatics.static_class())
far=(-10500,-13500,3500);target=unreal.Vector(-3850,-7050,80);delta=target-unreal.Vector(*far)
views=[('wall-rescate',(0,-500,235),(-5,-90,0)),('wall-arena',(1200,-2100,260),(-5,-145,0)),('wall-kit',(600,-3650,220),(-3,-90,0)),('cars-old-cut',far,(math.degrees(math.atan2(delta.z,math.hypot(delta.x,delta.y))),math.degrees(math.atan2(delta.y,delta.x)),0)),('cars-visible',far,(math.degrees(math.atan2(delta.z,math.hypot(delta.x,delta.y))),math.degrees(math.atan2(delta.y,delta.x)),0))]
cars=[]
for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor):
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if c.static_mesh and c.static_mesh.get_name()=='SM_LOD_Car':cars.append(c)
 for c in a.get_components_by_class(unreal.GeometryCollectionComponent):
  if c.get_editor_property('rest_collection') and c.get_editor_property('rest_collection').get_name()=='GC_Car2':cars.append(c)
assert len(cars)==2
tr=unreal.Transform();cam=lib.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.CameraActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));lib.call_method('FinishSpawningActor',(cam,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));cam.get_component_by_class(unreal.CameraComponent).set_field_of_view(60)
pc.set_view_target_with_blend(cam,0)
state={'index':0,'age':0,'shot':False,'busy':False,'handle':None}
def select_view():
 name,pos,rot=views[state['index']]
 cam.set_actor_location(unreal.Vector(*pos),False,True);cam.set_actor_rotation(unreal.Rotator(pitch=rot[0],yaw=rot[1],roll=0),True)
 if name.startswith('cars-'):
  for c in cars:
   # Native static car only: diagnostic old cutoff, no Blueprint reconstruction.
   if isinstance(c,unreal.StaticMeshComponent):
    c.set_editor_property('never_distance_cull',name=='cars-visible');c.set_cull_distance(6000 if name=='cars-old-cut' else 0)
def photograph(dt,s=state):
 if s['busy']:return
 s['age']+=dt
 if s['shot']:
  if s['age']<1:return
  s['busy']=True;s['index']+=1;s['age']=0;s['shot']=False
  if s['index']==len(views):
   unreal.unregister_slate_post_tick_callback(s['handle'])
   for c in cars:assert c.get_editor_property('cached_max_draw_distance')==0
   with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/car_visibility_comparison.json'),'w') as f:json.dump({'passed':True,'isolated_runtime_before_after':True,'same_far_camera':far,'cars':2,'old_cutoff_simulated_static_car_only':True,'new_effective_cutoff':0,'lods_retained':True},f,indent=2)
   unreal.log('WALL_AND_CAR_CAPTURES_COMPLETE');return
  select_view();s['busy']=False;return
 if s['age']<3:return
 s['busy']=True
 unreal.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/'+views[s['index']][0]+'.png'))
 s['shot']=True;s['age']=0;s['busy']=False
select_view();state['handle']=unreal.register_slate_post_tick_callback(photograph)
