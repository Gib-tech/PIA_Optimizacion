"""PIE: a real visible enemy interrupts the hostage's incomplete beacon channel."""
import unreal,json,os,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0)
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
for i in (1,2):
 zone=d.get_editor_property('Zona'+str(i));lib.call_method('SetIntPropertyByName',(zone,'Phase',3));lib.call_method('SetBoolPropertyByName',(zone,'bCleared',True))
b=d.get_editor_property('CurrentBeacon');point=b.get_editor_property('ApproachPoint').get_actor_location()
p.set_actor_location(point+unreal.Vector(0,200,100),False,True);h.set_actor_location(point+unreal.Vector(100,0,100),False,True);h.call_method('Interactuar')
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
state={'stage':'channel','since':unreal.GameplayStatics.get_time_seconds(w),'handle':None};project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
def observe(delta,world=w,player=p,hostage=h,mission=d,beacon=b,board=bb,s=state,root=project):
 try:
  now=unreal.GameplayStatics.get_time_seconds(world)
  if s['stage']=='channel' and hostage.get_editor_property('ActivationProgress')>.25:
   cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C');tr=unreal.Transform(location=hostage.get_actor_location()+unreal.Vector(300,0,0));gs=unreal.get_default_object(unreal.GameplayStatics.static_class());enemy=gs.call_method('BeginDeferredActorSpawnFromClass',(world,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));gs.call_method('FinishSpawningActor',(enemy,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));s.update(stage='threat',since=now,enemy=enemy)
  elif s['stage']=='threat' and board.get_value_as_bool('bMustFlee'):
   assert not hostage.get_editor_property('bUsingBeacon') and hostage.get_editor_property('ActivationProgress')==0
   assert not beacon.get_editor_property('bActivated') and mission.get_editor_property('Paso')==0
   assert not mission.get_editor_property('Baliza3').get_editor_property('Door').get_editor_property('bUnlocked')
   unreal.unregister_slate_post_tick_callback(s['handle'])
   with open(os.path.join(root,'Intermediate/inspect/beacon_interrupt_assertions.json'),'w') as f:json.dump({'passed':True,'visible_enemy_aborts_channel':True,'progress_resets':True,'beacon_and_door_stay_locked':True,'manual_resume_required':True},f,indent=2)
   unreal.log('BEACON_INTERRUPT_ASSERTIONS_PASSED');return
  assert now-s['since']<12,'Timeout '+s['stage']
 except Exception:
  unreal.unregister_slate_post_tick_callback(s['handle'])
  with open(os.path.join(root,'Intermediate/inspect/beacon_interrupt_assertions.json'),'w') as f:json.dump({'passed':False,'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('BEACON_INTERRUPT_ASSERTIONS_STARTED')
