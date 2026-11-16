"""Real heavy inputs followed by sustained movement; full-body recovery must release locomotion."""
import unreal,json,os,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);lib=unreal.get_default_object(unreal.SystemLibrary.static_class());root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
s={'index':0,'stage':'setup','since':0,'handle':None,'results':[],'samples':[]}
def observe(dt,world=w,player=p,state=s,project=root,lib=lib):
 try:
  now=unreal.GameplayStatics.get_time_seconds(world);age=now-state['since'];box=player.get_editor_property('WeaponHitbox');index=state['index'];cut=[1.18,1.05,1.70][index]
  if state['stage']=='setup':
   player.stop_anim_montage(player.get_current_montage());player.call_method('ResetState');player.character_movement.stop_movement_immediately()
   for name,value in [('IsAttacking',False),('bLightAttackActive',False),('bIsSwordEquipped',True),('bIsHammerEquipped',False)]:lib.call_method('SetBoolPropertyByName',(player,name,value))
   player.set_actor_location(unreal.Vector(0,-2000,100),False,True);player.set_actor_rotation(unreal.Rotator(yaw=-90),True);state.update(stage='equip',since=now,samples=[])
  elif state['stage']=='equip' and age>.2:
   lib.call_method('SetIntPropertyByName',(player,'AttackIndex',index));player.call_method('InpActEvt_IA_Heavy_Attack_K2Node_EnhancedInputActionEvent_6',(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_Heavy_Attack')))
   assert player.get_current_montage().get_name()=='H_attack_'+str(index+1)+'_Montage'
   state.update(stage='attack',since=now)
  elif state['stage']=='attack':
   if age>cut+.05:
    player.add_movement_input(unreal.Vector(0,-1,0),1.,False)
    state['samples'].append({'age':round(age,3),'speed':player.get_velocity().length(),'montage':player.get_current_montage().get_name() if player.get_current_montage() else None,'attacking':player.get_editor_property('IsAttacking'),'hand':str(player.mesh.get_socket_transform('hand_r',unreal.RelativeTransformSpace.RTS_COMPONENT).translation)})
   if age>cut+.7:
    steady=[v for v in state['samples'] if v['age']>cut+.25]
    assert steady and all(v['montage'] is None and not v['attacking'] for v in steady),steady
    assert max(v['speed'] for v in steady)>200
    assert box.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
    state['results'].append({'montage':'H_attack_'+str(index+1)+'_Montage','recovery_limit':cut,'movement_speed':round(max(v['speed'] for v in steady),1),'moving_without_attack_pose':True,'hitbox_off':True})
    if index<2:state.update(index=index+1,stage='setup',since=now)
    else:
     unreal.unregister_slate_post_tick_callback(state['handle']);player.character_movement.stop_movement_immediately()
     with open(os.path.join(project,'Intermediate/inspect/sword_recovery_assertions.json'),'w') as f:json.dump({'passed':True,'attacks':state['results']},f,indent=2)
     unreal.log('SWORD_RECOVERY_ASSERTIONS_PASSED');return
  assert age<6,'Timeout '+state['stage']
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(os.path.join(project,'Intermediate/inspect/sword_recovery_assertions.json'),'w') as f:json.dump({'passed':False,'stage':state['stage'],'index':state['index'],'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('SWORD_RECOVERY_OBSERVER_STARTED')
