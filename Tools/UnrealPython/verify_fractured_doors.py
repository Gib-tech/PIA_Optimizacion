"""Actual door damage events: geometry swap, matched irregular pieces, physics, traversal and cleanup."""
import unreal,os,json,traceback,time
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
doors=[d.get_editor_property('Baliza'+str(i)).get_editor_property('Door') for i in [1,2,3]]
cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DoorFragment.BP_DoorFragment_C')
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());state={'index':0,'stage':'setup','since':0,'handle':None,'results':[]}
def flag(o,key,value):lib.call_method('SetBoolPropertyByName',(o,key,value))
def path_open(world,door,player):
 pos=door.get_actor_location();path=unreal.NavigationSystemV1.find_path_to_location_synchronously(world,pos+unreal.Vector(0,170,0),pos+unreal.Vector(0,-170,0),player,None)
 return bool(path and path.is_valid() and not path.is_partial())
def observe(dt,world=w,player=p,ds=doors,fragment_class=cls,s=state,project=root,flag=flag,path_open=path_open):
 try:
  now=unreal.GameplayStatics.get_time_seconds(world);age=now-s['since'];door=ds[s['index']];stage=s['stage']
  shards=[a for a in unreal.GameplayStatics.get_all_actors_of_class(world,fragment_class) if a.get_owner()==door]
  if stage=='setup':
   player.set_actor_location(door.get_actor_location()+unreal.Vector(0,250,100),False,True);player.set_actor_rotation(unreal.Rotator(yaw=-90),True);player.get_controller().set_control_rotation(unreal.Rotator(pitch=-5,yaw=-90))
   flag(door,'bUnlocked',True);player.call_method('GrantHammerUpgrade',(door,));flag(player,'IsAttacking',True);flag(player,'bLightAttackActive',False)
   assert not path_open(world,door,player),'Closed gate is passable'
   unreal.GameplayStatics.apply_damage(door,25,None,player,None)
   assert door.get_editor_property('Health')==25 and door.get_editor_property('bCracked')
   assert door.static_mesh_component.static_mesh==door.get_editor_property('CrackedMesh')
   s.update(stage='cracked',since=now)
  elif stage=='cracked' and age>.5:
   assert not path_open(world,door,player),'Cracks opened navigation early'
   if s['index']==0:unreal.SystemLibrary.execute_console_command(world,'HighResShot 1280x720 filename="'+os.path.join(project,'docs/validation/fracture-cracks-preview.png').replace('\\','/')+'"')
   s.update(stage='break',since=now)
  elif stage=='break' and age>.2:
   start=time.perf_counter();unreal.GameplayStatics.apply_damage(door,25,None,player,None);cost=(time.perf_counter()-start)*1000
   shards=[a for a in unreal.GameplayStatics.get_all_actors_of_class(world,fragment_class) if a.get_owner()==door]
   expected=list(door.get_editor_property('FragmentMeshes'));offsets=list(door.get_editor_property('FragmentOffsets'))
   assert len(shards)==len(expected) and len(shards) in [42,56,72],(len(shards),len(expected))
   initial={};errors=[]
   for a in shards:
    mesh=a.static_mesh_component.static_mesh;assert mesh==a.get_editor_property('ShardMesh') and mesh in expected
    index=expected.index(mesh);goal=door.get_actor_transform().transform_location(offsets[index]);errors.append(a.get_actor_location().distance(goal))
    assert a.static_mesh_component.is_simulating_physics(),a.get_name()
    assert a.static_mesh_component.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)==unreal.CollisionResponseType.ECR_IGNORE
    assert a.static_mesh_component.get_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA)==unreal.CollisionResponseType.ECR_IGNORE
    assert not a.static_mesh_component.get_editor_property('can_ever_affect_navigation')
    initial[a.get_name()]=a.get_actor_location()
   assert max(errors)<.1,max(errors)
   assert door.get_editor_property('bDestroyed') and not door.get_actor_enable_collision()
   s.update(stage='burst',since=now,initial=initial,current={'door':s['index']+1,'pieces':len(shards),'matching_initial_geometry_cm':max(errors),'spawn_cost_ms':round(cost,2),'first_hit_blocks_navigation':True,'physics_and_pawn_camera_ignore':True})
  elif stage=='burst' and age>.25:
   movement=[a.get_actor_location().distance(s['initial'][a.get_name()]) for a in shards]
   spinning=[a for a in shards if a.static_mesh_component.get_physics_angular_velocity_in_degrees().length()>10]
   assert sum(x>5 for x in movement)>=len(shards)*.8,movement
   assert len(spinning)>=len(shards)*.7,len(spinning)
   s['current'].update(moving_shards=sum(x>5 for x in movement),spinning_shards=len(spinning),max_displacement_cm=round(max(movement),1))
   if s['index']==0:unreal.SystemLibrary.execute_console_command(world,'HighResShot 1280x720 filename="'+os.path.join(project,'docs/validation/door-shatter-preview.png').replace('\\','/')+'"')
   s.update(stage='cleanup',burst_at=s['since'],since=now)
  elif stage=='cleanup' and now-s['burst_at']>.85 and not s['current'].get('opens_navigation_with_debris'):
   assert path_open(world,door,player),'Debris blocks live navigation'
   s['current']['opens_navigation_with_debris']=True
   if s['index']==0:unreal.SystemLibrary.execute_console_command(world,'HighResShot 1280x720 filename="'+os.path.join(project,'docs/validation/door-shatter-late-preview.png').replace('\\','/')+'"')
  elif stage=='cleanup' and now-s['burst_at']>4.3:
   assert not shards,'Fragments did not expire'
   assert path_open(world,door,player),'Destroyed door still blocks navigation'
   s['current'].update(fragments_expired=True,opens_navigation=True);s['results'].append(s['current'])
   if s['index']<2:s.update(index=s['index']+1,stage='setup',since=now)
   else:
    unreal.unregister_slate_post_tick_callback(s['handle'])
    with open(os.path.join(project,'Intermediate/inspect/fracture_assertions.json'),'w') as f:json.dump({'passed':True,'doors':s['results']},f,indent=2)
    unreal.log('FRACTURE_ASSERTIONS_PASSED '+json.dumps(s['results']));return
  assert age<8,'Timeout '+stage
 except Exception:
  unreal.unregister_slate_post_tick_callback(s['handle'])
  with open(os.path.join(project,'Intermediate/inspect/fracture_assertions.json'),'w') as f:json.dump({'passed':False,'index':s['index'],'stage':s['stage'],'error':traceback.format_exc(),'doors':s['results']},f,indent=2)
  unreal.log_error(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('FRACTURE_OBSERVER_STARTED')
