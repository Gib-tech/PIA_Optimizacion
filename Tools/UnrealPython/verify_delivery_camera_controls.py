"""Enhanced Input dispatch across real frames, both camera states and post-pause movement."""
import unreal,json,os,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs=unreal.GameplayStatics
p=gs.get_player_pawn(w,0);pc=gs.get_player_controller(w,0)
lib=unreal.get_default_object(unreal.load_class(None,'/Script/Engine.SubsystemBlueprintLibrary'))
sub=lib.call_method('GetLocalPlayerSubSystemFromPlayerController',(pc,unreal.EnhancedInputLocalPlayerSubsystem.static_class()))
assert sub.has_mapping_context(unreal.load_asset('/Game/ThirdPerson/Input/IMC_Default')) is not None
assert not pc.is_move_input_ignored() and not pc.is_look_input_ignored()
root=unreal.Paths.project_dir();s={'stage':0,'at':gs.get_time_seconds(w),'handle':None,'checks':[]}
def inject(name,x=1,y=0):sub.inject_input_vector_for_action(unreal.load_asset('/Game/ThirdPerson/Input/Actions/'+name),unreal.Vector(x,y,0),[],[])
def observe(dt,state=s,world=w,player=p,controller=pc,project=root):
 try:
  now=gs.get_time_seconds(world);age=now-state['at'];stage=state['stage']
  if age<.2:return
  if stage==0:
   assert not player.get_editor_property('CamaraPrimera');inject('IA_Camera')
  elif stage==1:
   assert player.get_editor_property('CamaraPrimera') and player.get_editor_property('FPC').is_active()
   assert not player.get_editor_property('TPC').is_active() and player.mesh.get_editor_property('owner_no_see')
   assert player.get_editor_property('FPC').get_editor_property('relative_location')==unreal.Vector(0,0,64)
   controller.set_control_rotation(unreal.Rotator(pitch=22,yaw=33));state['checks'].append('first_person_eye_height_body_hidden')
  elif stage==2:
   r=player.get_editor_property('FPC').get_world_rotation();assert abs(r.pitch-22)<.1 and abs(r.yaw-33)<.1
   inject('IA_Camera');state['checks'].append('first_person_follows_pitch_yaw')
  elif stage==3:
   assert not player.get_editor_property('CamaraPrimera') and player.get_editor_property('TPC').is_active()
   assert not player.get_editor_property('FPC').is_active() and not player.mesh.get_editor_property('owner_no_see')
   state['checks'].append('third_person_mesh_and_camera_restored');inject('IA_SwitchToHammer')
  elif stage==4:
   # Existing action names and equipped flags are historically inverted.
   state['switch_to_hammer_action']={'hammer':player.get_editor_property('bIsHammerEquipped'),'sword':player.get_editor_property('bIsSwordEquipped')}
   inject('IA_SwitchToSword')
  elif stage==5:
   state['switch_to_sword_action']={'hammer':player.get_editor_property('bIsHammerEquipped'),'sword':player.get_editor_property('bIsSwordEquipped')}
   assert state['switch_to_hammer_action']!=state['switch_to_sword_action']
   state['checks'].append('both_weapon_actions_dispatch');state['start_location']=player.get_actor_location()
   inject('IA_Move',0,1)
  elif stage==6:
   assert player.get_actor_location().distance(state['start_location'])>0.1
   state['checks'].append('enhanced_move_after_resume');inject('IA_Light_Attack')
  elif stage==7:
   assert player.get_current_montage();state['checks'].append('light_attack_after_resume')
  elif stage==8:
   if player.get_editor_property('IsAttacking'):return
   state['jump_z']=player.get_actor_location().z;inject('IA_Jump')
  elif stage==9:
   assert player.get_actor_location().z>state['jump_z']+5
   state['checks'].append('jump_action_after_resume')
   unreal.unregister_slate_post_tick_callback(state['handle'])
   out={'passed':True,'agent_test_not_owner_acceptance':True,'method':'Enhanced Input injected actions over real frames; no physical gamepad test','checks':state['checks'],'Y_action':state['switch_to_hammer_action'],'T_action':state['switch_to_sword_action']}
   with open(os.path.join(project,'Intermediate/inspect/delivery_camera_controls_assertions.json'),'w') as f:json.dump(out,f,indent=2)
   unreal.log('CAMERA_CONTROLS_REGRESSION '+json.dumps(out));return
  state['stage']+=1;state['at']=now
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  out={'passed':False,'stage':state['stage'],'error':traceback.format_exc()}
  with open(os.path.join(project,'Intermediate/inspect/delivery_camera_controls_assertions.json'),'w') as f:json.dump(out,f,indent=2)
  unreal.log_error(json.dumps(out))
s['handle']=unreal.register_slate_post_tick_callback(observe)
