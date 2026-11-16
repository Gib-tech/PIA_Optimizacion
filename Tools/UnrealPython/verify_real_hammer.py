"""PIE: actual input delegate, montage, collision window and two physical door impacts."""
import unreal,json,os,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0)
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'));door=d.get_editor_property('Baliza1').get_editor_property('Door');assert door.get_editor_property('Health')==50
p.set_actor_location(unreal.Vector(0,-3870,100),False,True);p.set_actor_rotation(unreal.Rotator(yaw=-90),True)
unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetBoolPropertyByName',(door,'bUnlocked',True));p.call_method('GrantHammerUpgrade',(door,))
assert not p.get_editor_property('bIsSwordEquipped') and p.get_editor_property('WeaponHitbox').get_attach_parent()==p.get_editor_property('hammer')
assert any(c.is_active() for c in p.get_components_by_class(unreal.NiagaraComponent)),'Upgrade FX missing'
def hit(pawn=p):pawn.call_method('InpActEvt_IA_Heavy_Attack_K2Node_EnhancedInputActionEvent_6',(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_Heavy_Attack')))
hit();s={'stage':'cancel','since':unreal.GameplayStatics.get_time_seconds(w),'handle':None,'saw_window':False};project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
def observe(delta,world=w,pawn=p,gate=door,state=s,root=project,hit=hit):
 try:
  now=unreal.GameplayStatics.get_time_seconds(world);age=now-state['since'];stage=state['stage'];box=pawn.get_editor_property('WeaponHitbox')
  if stage=='cancel' and age>.12:
   pawn.stop_anim_montage(pawn.get_current_montage());state.update(stage='cancelled',since=now)
  elif stage=='cancelled' and age>.15:
   assert not pawn.get_editor_property('IsAttacking') and box.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
   assert gate.get_editor_property('Health')==50,'Interrupted attack damaged gate'
   hit();state.update(stage='first',since=now)
   assert pawn.get_current_montage().get_name()=='Attack_3_Montage'
  elif stage in ['first','second']:
   if box.get_collision_enabled()==unreal.CollisionEnabled.QUERY_ONLY:state['saw_window']=True
   if not pawn.get_editor_property('IsAttacking') and age>.5:
    expected=25 if stage=='first' else 0
    assert gate.get_editor_property('Health')==expected,(stage,gate.get_editor_property('Health'))
    if box.get_collision_enabled()!=unreal.CollisionEnabled.NO_COLLISION:
     state.setdefault('ended_at',now);assert now-state['ended_at']<.15,'Hitbox stayed active after attack';return
    state.pop('ended_at',None)
    if stage=='first':
     assert gate.get_editor_property('bCracked') and gate.static_mesh_component.static_mesh==gate.get_editor_property('CrackedMesh')
     unreal.SystemLibrary.execute_console_command(world,'HighResShot 1280x720 filename="'+os.path.join(root,'docs/validation/cracked-door-preview.png').replace('\\','/')+'"')
     hit();state.update(stage='second',since=now)
    else:
     assert gate.get_editor_property('bDestroyed') and not gate.get_actor_enable_collision() and state['saw_window']
     # Return the same hitbox to the sword's authored transform when switching back.
     lib=unreal.get_default_object(unreal.SystemLibrary.static_class());lib.call_method('SetBoolPropertyByName',(pawn,'bIsHammerEquipped',False));lib.call_method('SetBoolPropertyByName',(pawn,'bIsSwordEquipped',True));state.update(stage='sword',since=now)
  elif stage=='sword' and age>.1:
   assert box.get_attach_parent()==pawn.get_editor_property('Weapon') and box.get_unscaled_box_extent().distance(unreal.Vector(45,45,90))<.001
   assert box.get_editor_property('relative_location').distance(pawn.get_editor_property('SwordHitboxRelativeTransform').translation)<.001
   unreal.unregister_slate_post_tick_callback(state['handle'])
   with open(os.path.join(root,'Intermediate/inspect/real_hammer_assertions.json'),'w') as f:json.dump({'passed':True,'real_input_and_hammer_montage':True,'physical_door_hits':2,'per_hit_damage':25,'cracked_geometry_after_first_hit':True,'upgrade_particles_active':True,'interrupted_attack_damage':0,'interruption_clears_attack_and_collision':True,'sword_hitbox_restored':True},f,indent=2)
   unreal.log('REAL_HAMMER_ASSERTIONS_PASSED');return
  assert age<8,'Timeout '+stage
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(os.path.join(root,'Intermediate/inspect/real_hammer_assertions.json'),'w') as f:json.dump({'passed':False,'stage':state['stage'],'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('REAL_HAMMER_ASSERTIONS_STARTED')
