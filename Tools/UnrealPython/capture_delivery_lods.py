import unreal,os,math,json
lod_world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert lod_world
lod_pc=unreal.GameplayStatics.get_player_controller(lod_world,0);lod_native=unreal.get_default_object(unreal.GameplayStatics.static_class())
lod_tr=unreal.Transform();lod_cam=lod_native.call_method('BeginDeferredActorSpawnFromClass',(lod_world,unreal.CameraActor.static_class(),lod_tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));lod_native.call_method('FinishSpawningActor',(lod_cam,lod_tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
lod_cam.get_component_by_class(unreal.CameraComponent).set_field_of_view(60);lod_pc.set_view_target_with_blend(lod_cam,0)
unreal.SystemLibrary.execute_console_command(lod_world,'viewmode lodcoloration');unreal.SystemLibrary.execute_console_command(lod_world,'showhud')
lod_folder=os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()),'Intermediate/inspect/lod-demo');os.makedirs(lod_folder,exist_ok=True)
lod_targets=[]
for actor in unreal.GameplayStatics.get_all_actors_of_class(lod_world,unreal.StaticMeshActor):
 c=actor.static_mesh_component
 if c.static_mesh and c.static_mesh.get_name().startswith('SM_LOD_'):
  center,extent,radius=unreal.SystemLibrary.get_component_bounds(c)
  for index,factor in enumerate([4,16,24,80]):lod_targets.append({'model':c.static_mesh.get_name(),'lod_step':index,'radius':radius,'center':center,'distance':radius*factor})
assert len(lod_targets)==20
lod_state={'i':0,'age':0,'shot':False,'handle':None,'rows':[],'busy':False}
def lod_select(s):
 item=lod_targets[s['i']];center=item['center'];d=item['distance']
 lod_cam.set_actor_location(center+unreal.Vector(0,-d*.5,d*math.sqrt(.75)),False,True);lod_cam.set_actor_rotation(unreal.Rotator(pitch=-60,yaw=90,roll=0),True)
def lod_tick(dt,s=lod_state):
 if s['busy']:return
 s['age']+=dt
 if not s['shot'] and s['age']>.3:
  item=lod_targets[s['i']];s['busy']=True
  filename=os.path.join(lod_folder,item['model']+'-'+str(item['lod_step'])+'.png')
  unreal.SystemLibrary.execute_console_command(lod_world,'Shot filename="'+filename+'"')
  s['rows'].append({'model':item['model'],'distance_cm':item['distance'],'radius_cm':item['radius'],'camera_fov':60,'forced_lod':False,'file_prefix':os.path.basename(filename).removesuffix('.png')})
  s.update(shot=True,age=0,busy=False)
 elif s['shot'] and s['age']>.2:
  s['i']+=1;s.update(age=0,shot=False)
  if s['i']==len(lod_targets):
   unreal.unregister_slate_post_tick_callback(s['handle']);unreal.SystemLibrary.execute_console_command(lod_world,'viewmode lit');unreal.SystemLibrary.execute_console_command(lod_world,'showhud')
   with open(os.path.join(lod_folder,'observations.json'),'w') as f:json.dump({'camera_test_not_manual_playthrough':True,'viewmode':'lodcoloration','no_forced_lods':True,'rows':s['rows']},f,indent=2)
   unreal.log('LOD_CAMERA_CAPTURE_COMPLETE');return
  lod_select(s)
lod_select(lod_state);lod_state['handle']=unreal.register_slate_post_tick_callback(lod_tick)
