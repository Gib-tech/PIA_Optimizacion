"""Actual input delegates, all equipped-weapon montages, physical enemy overlaps and cleanup."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
def flag(obj,key,value):lib.call_method('SetBoolPropertyByName',(obj,key,value))
flag(p,'bCanBeDamaged',False)
gs=unreal.get_default_object(unreal.GameplayStatics.static_class())
cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
tr=unreal.Transform(location=unreal.Vector(0,-2160,100))
e=gs.call_method('BeginDeferredActorSpawnFromClass',(w,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));gs.call_method('FinishSpawningActor',(e,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
e.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Isolate real weapon hits')
e.character_movement.disable_movement()
hp=next(c for c in e.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_E_Health_C')
lib.call_method('SetDoublePropertyByName',(hp,'E_Health',1000.))
cases=[('sword','light',i,d) for i,d in enumerate([15,15,19,22])]+[('sword','heavy',i,25) for i in range(3)]+[('hammer','light',i,15) for i in range(2)]+[('hammer','heavy',0,25)]
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
s={'index':0,'stage':'setup','since':0,'last_hp':1000.,'window':False,'handle':None,'results':[]}
def observe(dt,world=w,player=p,enemy=e,health=hp,state=s,project=root,cases=cases,flag=flag,lib=lib):
 try:
  now=unreal.GameplayStatics.get_time_seconds(world);weapon,kind,index,damage=cases[state['index']];age=now-state['since'];box=player.get_editor_property('WeaponHitbox')
  if state['stage']=='setup':
   player.stop_anim_montage(player.get_current_montage());player.call_method('ResetState')
   flag(player,'IsAttacking',False);flag(player,'bLightAttackActive',False);flag(player,'bIsHammerEquipped',weapon=='hammer');flag(player,'bIsSwordEquipped',weapon=='sword')
   player.set_actor_location(unreal.Vector(0,-2000,100),False,True);player.set_actor_rotation(unreal.Rotator(yaw=-90),True)
   enemy.set_actor_location(unreal.Vector(0,-2160,100),False,True)
   state.update(stage='equip',since=now,window=False,hits=[],positions=[],last_sample=-1,last_hp=health.get_editor_property('E_Health'))
  elif state['stage']=='equip' and age>.15:
   lib.call_method('SetIntPropertyByName',(player,'AttackIndex',index))
   asset=unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_'+('Light_Attack' if kind=='light' else 'Heavy_Attack'))
   name='InpActEvt_IA_'+('Light_Attack_K2Node_EnhancedInputActionEvent_7' if kind=='light' else 'Heavy_Attack_K2Node_EnhancedInputActionEvent_6')
   player.call_method(name,(unreal.InputActionValue(),0.,0.,asset))
   assert player.get_current_montage(),'Input failed to play montage'
   state.update(stage='attack',since=now,montage=player.get_current_montage().get_name())
  elif state['stage']=='attack':
   if age-state['last_sample']>.03:
    bpos=box.get_world_location();epos=enemy.get_actor_location();state['positions'].append([round(age,3),round(bpos.x-epos.x,1),round(bpos.y-epos.y,1),round(bpos.z-epos.z,1),box.get_collision_enabled()==unreal.CollisionEnabled.QUERY_ONLY]);state['last_sample']=age
   current=health.get_editor_property('E_Health')
   if box.get_collision_enabled()==unreal.CollisionEnabled.QUERY_ONLY:state['window']=True
   if current<state['last_hp']:state['hits'].append(state['last_hp']-current);state['last_hp']=current
   if not player.get_editor_property('IsAttacking') and age>.5:
    if box.get_collision_enabled()!=unreal.CollisionEnabled.NO_COLLISION and age<4:return
    result={'weapon':weapon,'kind':kind,'index':index,'montage':state['montage'],'window_opened':state['window'],'damage_events':state['hits'],'expected':damage,'collision_closed':box.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION}
    result['passed']=result['window_opened'] and result['damage_events']==[damage] and result['collision_closed']
    if not result['passed']:result['hitbox_positions_relative_to_enemy']=state['positions']
    state['results'].append(result)
    if state['index']+1<len(cases):state.update(index=state['index']+1,stage='setup',since=now)
    else:
     unreal.unregister_slate_post_tick_callback(state['handle']);enemy.destroy_actor()
     result={'passed':all(r['passed'] for r in state['results']),'attacks':state['results']}
     with open(os.path.join(project,'Intermediate/inspect/all_attack_assertions.json'),'w') as f:json.dump(result,f,indent=2)
     unreal.log('ALL_ATTACK_WINDOWS_RESULT '+json.dumps(result));return
   assert age<5,'Attack never completed '+state['montage']
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle']);enemy.destroy_actor()
  with open(os.path.join(project,'Intermediate/inspect/all_attack_assertions.json'),'w') as f:json.dump({'passed':False,'case':state['index'],'error':traceback.format_exc(),'attacks':state['results']},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('ALL_ATTACK_WINDOWS_OBSERVER_STARTED')
