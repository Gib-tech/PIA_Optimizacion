"""Live HUD marker/voice selection and actual enemy-service fixation, including release controls."""
import unreal,json,os,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);ui=unreal.GameplayStatics.get_player_controller(w,0).get_hud()
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
hb=h.get_controller().get_component_by_class(unreal.BlackboardComponent);lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
def flag(a,name,value):lib.call_method('SetBoolPropertyByName',(a,name,value))
for a in [p,h]:flag(a,'bCanBeDamaged',False)
unreal.SystemLibrary.execute_console_command(w,'t.IdleWhenNotForeground 0')
s={'stage':'prompt','since':unreal.GameplayStatics.get_time_seconds(w),'handle':None,'results':{},'enemies':[]}
def spawn(name,pos,world=w):
 cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/'+name+'.'+name+'_C');tr=unreal.Transform(location=unreal.Vector(*pos));gs=unreal.get_default_object(unreal.GameplayStatics.static_class())
 e=gs.call_method('BeginDeferredActorSpawnFromClass',(world,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));gs.call_method('FinishSpawningActor',(e,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));e.character_movement.disable_movement();return e
def observe(dt,world=w,player=p,hostage=h,hud=ui,mission=d,bb=hb,state=s,project=root,flag=flag,spawn=spawn):
 try:
  now=unreal.GameplayStatics.get_time_seconds(world);age=now-state['since'];stage=state['stage'];result=state['results']
  if stage=='prompt' and age>.3:
   assert hud.get_editor_property('HostagePromptVisible') and hud.get_editor_property('HostagePromptInRange'),'Floating key missing at rescue'
   cue=hud.get_editor_property('CurrentVoiceCue');assert cue and cue.get_name().startswith('SW_HostageVoice_'),str(cue)
   result.update(rescue_marker_visible=True,hostage_voice=cue.get_name())
   unreal.SystemLibrary.execute_console_command(world,'HighResShot 1280x720 filename="'+os.path.join(project,'docs/validation/hostage-prompt-preview.png').replace('\\','/')+'"')
   state.update(stage='screenshot',since=now)
  elif stage=='screenshot' and age>.25:
   hostage.call_method('Interactuar');state.update(stage='following',since=now)
  elif stage=='following' and age>.3:
   assert bb.get_value_as_bool('bAccompanying') and not hud.get_editor_property('HostagePromptVisible')
   result['following_hides_marker']=True
   zone=mission.get_editor_property('Zona1');lib.call_method('SetIntPropertyByName',(zone,'Phase',2));lib.call_method('SetDoublePropertyByName',(zone,'NextWaveAt',now+999))
   state.update(stage='narrator',since=now)
  elif stage=='narrator' and age>.3:
   assert not hud.get_editor_property('HostageSpeaking')
   assert hud.get_editor_property('CurrentVoiceCue').get_name()=='SW_Text',hud.get_editor_property('CurrentVoiceCue')
   result['narrator_keeps_original_sound']=True
   lib.call_method('SetIntPropertyByName',(mission.get_editor_property('Zona1'),'Phase',0))
   hostage.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Isolate perception and marker states')
   player.set_actor_location(unreal.Vector(0,-2200,100),False,True);hostage.set_actor_location(unreal.Vector(0,-2500,100),False,True)
   bb.set_value_as_bool('bAccompanying',False);bb.set_value_as_bool('bWaiting',True);bb.set_value_as_bool('bMustFlee',False)
   state['enemies']=[spawn('BP_BaseEnemy',(-160,-2300,100)),spawn('BP_ChargerEnemy',(160,-2300,100))]
   state.update(stage='acquire',since=now)
  elif stage=='acquire' and age>.6:
   for e in state['enemies']:
    b=e.get_controller().get_component_by_class(unreal.BlackboardComponent)
    assert b.get_value_as_bool('bHostageLocked') and b.get_value_as_object('TargetActor')==hostage,e.get_name()
    assert e.get_distance_to(player)<220,'Player-proximity negative control failed'
   result['both_prioritize_hostage_over_close_player']=True
   hostage.set_actor_location(unreal.Vector(800,-2800,100),False,True);state.update(stage='retained',since=now)
  elif stage=='retained' and age>.5:
   assert all(e.get_distance_to(hostage)>650 and e.get_editor_property('CombatTarget')==hostage for e in state['enemies'])
   result['fixation_retained_beyond_acquisition_radius']=True
   for e,x in zip(state['enemies'],[-160,160]):e.set_actor_location(unreal.Vector(x,-3500,100),False,True)
   player.set_actor_location(unreal.Vector(0,-3300,100),False,True);hostage.set_actor_location(unreal.Vector(0,-4300,100),False,True);state.update(stage='occluded',since=now)
  elif stage=='occluded' and age>.5:
   for e in state['enemies']:
    assert not e.get_controller().line_of_sight_to(hostage)
    assert e.get_editor_property('CombatTarget')==hostage
   result['temporary_occlusion_keeps_fixation']=True
   bb.set_value_as_bool('bRescued',False);state.update(stage='release',since=now)
  elif stage=='release' and age>1.2:
   result['release_targets']=[{'enemy':e.get_class().get_name(),'target':str(e.get_editor_property('CombatTarget')),'locked':e.get_controller().get_component_by_class(unreal.BlackboardComponent).get_value_as_bool('bHostageLocked')} for e in state['enemies']]
   assert all(e.get_editor_property('CombatTarget')==player and not e.get_controller().get_component_by_class(unreal.BlackboardComponent).get_value_as_bool('bHostageLocked') for e in state['enemies'])
   result['unrescued_hostage_releases_fixation']=True
   bb.set_value_as_bool('bRescued',True);hostage.set_actor_location(unreal.Vector(0,-3650,100),False,True);state.update(stage='reacquire',since=now)
  elif stage=='reacquire' and age>1.2:
   assert all(e.get_editor_property('CombatTarget')==hostage for e in state['enemies'])
   hostage.set_actor_location(unreal.Vector(4000,-3500,100),False,True);state.update(stage='leash',since=now)
  elif stage=='leash' and age>1.2:
   assert all(e.get_editor_property('CombatTarget')==player for e in state['enemies'])
   result.update(leash_releases_fixation=True,passed=True)
   for e in state['enemies']:e.destroy_actor()
   unreal.unregister_slate_post_tick_callback(state['handle'])
   with open(os.path.join(project,'Intermediate/inspect/hostage_feedback_assertions.json'),'w') as f:json.dump(result,f,indent=2)
   unreal.log('HOSTAGE_FEEDBACK_ASSERTIONS_PASSED '+json.dumps(result));return
  assert age<5,'Timeout '+stage
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  for e in state['enemies']:e.destroy_actor()
  with open(os.path.join(project,'Intermediate/inspect/hostage_feedback_assertions.json'),'w') as f:json.dump({'passed':False,'stage':state['stage'],'error':traceback.format_exc(),'results':state['results']},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('HOSTAGE_FEEDBACK_OBSERVER_STARTED')
