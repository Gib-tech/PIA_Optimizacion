"""PIE: real orbit/charge attacks target the escort; protection, damage grace and death outcome."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0)
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent);bb.set_value_as_bool('bRescued',True)
h.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Stationary damage test target')
p.set_actor_location(unreal.Vector(1000,-1600,100),False,True);h.set_actor_location(unreal.Vector(0,-2000,100),False,True)
def spawn(name,x,y,world=w):
 cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/'+name+'.'+name+'_C');tr=unreal.Transform(location=unreal.Vector(x,y,100));gs=unreal.get_default_object(unreal.GameplayStatics.static_class())
 a=gs.call_method('BeginDeferredActorSpawnFromClass',(world,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));gs.call_method('FinishSpawningActor',(a,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));return a
enemy=spawn('BP_BaseEnemy',0,-2170)
s={'stage':'orbiter','since':unreal.GameplayStatics.get_time_seconds(w),'enemy':enemy,'handle':None,'results':{}}
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
def observe(delta,world=w,player=p,hostage=h,mission=d,state=s,root=project,spawn=spawn):
 try:
  now=unreal.GameplayStatics.get_time_seconds(world);e=state['enemy'];hp=hostage.get_editor_property('Health');stage=state['stage']
  if stage=='orbiter' and hp<100:
   assert abs(hp-86.8)<.001 and e.get_editor_property('CombatTarget')==hostage
   unreal.GameplayStatics.apply_damage(hostage,13.2,None,e,None);assert abs(hostage.get_editor_property('Health')-86.8)<.001,'No hit grace'
   state['results'].update(orbiter_damage=13.2,hostage_target=True,immediate_repeat_damage=0)
   e.destroy_actor();state.update(stage='charger_wait',since=now)
  elif stage=='charger_wait' and now-state['since']>1:
   state.update(stage='charger',since=now,enemy=spawn('BP_ChargerEnemy',-400,-2000))
  elif stage=='charger' and hp<86.7:
   assert abs(hp-73.6)<.001 and e.get_editor_property('ChargeVictim')==hostage
   state['results']['charger_damage']=13.2;e.destroy_actor()
   player.set_actor_location(unreal.Vector(0,-1800,100),False,True)
   state.update(stage='intercept',since=now,enemy=spawn('BP_BaseEnemy',0,-1630))
  elif stage=='intercept' and now-state['since']>1:
   assert e.get_editor_property('CombatTarget')==hostage,'Hostage fixation lost to a closer player'
   assert hp<=73.601 and hp>0
   state['results']['hostage_fixation_survives_player_proximity']=True
   unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetDoublePropertyByName',(hostage,'InvulnerableUntil',0.0))
   unreal.GameplayStatics.apply_damage(hostage,200,None,e,None)
   assert hostage.get_editor_property('bIsDead') and hostage.get_editor_property('Health')==0
   assert mission.get_editor_property('Paso')==6 and unreal.GameplayStatics.is_game_paused(world)
   state['results'].update(hostage_death_ends_mission=True,passed=True)
   unreal.unregister_slate_post_tick_callback(state['handle'])
   with open(os.path.join(root,'Intermediate/inspect/hostage_combat_assertions.json'),'w') as f:json.dump(state['results'],f,indent=2)
   unreal.log('HOSTAGE_COMBAT_ASSERTIONS_PASSED');return
  assert now-state['since']<25,'Timeout '+stage
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(os.path.join(root,'Intermediate/inspect/hostage_combat_assertions.json'),'w') as f:json.dump({'passed':False,'stage':state['stage'],'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('HOSTAGE_COMBAT_ASSERTIONS_STARTED')
