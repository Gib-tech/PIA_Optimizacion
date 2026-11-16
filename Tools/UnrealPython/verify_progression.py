"""PIE integration: both hordes, three hostage channels, hammer impact guards and dynamic routes."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
R='/Game/ThirdPerson/Blueprints/Entrega/'
p=unreal.GameplayStatics.get_player_pawn(w,0)
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,R+'BP_DirectorEntrega.BP_DirectorEntrega_C'))
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
beacons=[d.get_editor_property('Baliza'+str(i)) for i in [1,2,3]]
doors=[b.get_editor_property('Door') for b in beacons]
zones=[d.get_editor_property('Zona'+str(i)) for i in [1,2]]
assert all(z.get_editor_property('Phase')==0 for z in zones),'Fresh PIE required'
closed=unreal.NavigationSystemV1.find_path_to_location_synchronously(w,unreal.Vector(0,-3620,0),unreal.Vector(-3200,-5320,0),h,None)
assert not closed or not closed.is_valid() or closed.is_partial(),'First closed gate can be bypassed'
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
lib.call_method('SetBoolPropertyByName',(p,'bCanBeDamaged',False))
def flags(obj,**values):
 for key,value in values.items():lib.call_method('SetBoolPropertyByName',(obj,key,value))
def prop(obj,key):return obj.get_editor_property(key)
def attack(door):
 p.call_method('BndEvt__BP_PlayerEntrega_HeavyOverlap__DelegateSignature',(prop(p,'WeaponHitbox'),door,door.static_mesh_component,0,False,unreal.HitResult()))
def swing_reset():
 flags(p,IsAttacking=False,bLightAttackActive=False);p.call_method('ReceiveTick',(.016,));flags(p,IsAttacking=True,bLightAttackActive=False)
flags(p,IsAttacking=True,bLightAttackActive=False,bIsHammerEquipped=True,bHammerUpgraded=True)
unreal.GameplayStatics.apply_damage(doors[0],25,None,p,None)
assert prop(doors[0],'Health')==50,'Locked gate took damage'
flags(p,bHammerUpgraded=False)
flags(doors[0],bUnlocked=True);unreal.GameplayStatics.apply_damage(doors[0],25,None,p,None)
assert prop(doors[0],'Health')==50,'Unpowered hammer took damage'
flags(p,bHammerUpgraded=True,bLightAttackActive=True);unreal.GameplayStatics.apply_damage(doors[0],25,None,p,None)
assert prop(doors[0],'Health')==50,'Light hit damaged door'
flags(doors[0],bUnlocked=False);flags(p,IsAttacking=False,bLightAttackActive=False,bHammerUpgraded=False)
assert prop(h,'Health')==100
unreal.GameplayStatics.apply_damage(h,10,None,p,None);assert prop(h,'Health')==100,'Friendly fire damaged hostage'
state={'index':0,'stage':'enter','since':unreal.GameplayStatics.get_time_seconds(w),'handle':None,'results':[]}
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())

def observe(delta,world=w,player=p,hostage=h,mission=d,board=bb,bs=beacons,ds=doors,zs=zones,s=state,root=project,flags=flags,prop=prop,attack=attack,swing_reset=swing_reset):
 try:
  now=unreal.GameplayStatics.get_time_seconds(world);i=s['index'];stage=s['stage'];gate=ds[i];b=bs[i];zone=zs[min(i,1)]
  if stage=='enter':
   if i<2:
    center=zone.get_actor_location();player.set_actor_location(center+unreal.Vector(0,500,-50),False,True)
    board.set_value_as_bool('bAccompanying',False);board.set_value_as_bool('bWaiting',True);board.set_value_as_bool('bMustFlee',False)
    s.update(stage='alone',since=now)
   else:s.update(stage='escort',since=now)
  elif stage=='alone' and now-s['since']>.7:
   assert prop(zone,'SpawnedCount')==0,'Entered alone and spawned enemies'
   hostage.set_actor_location(player.get_actor_location()+unreal.Vector(150,150,0),False,True)
   hostage.call_method('Interactuar');s.update(stage='first',since=now)
  elif stage in ['first','second'] and prop(zone,'Phase')==1:
   wave=1 if stage=='first' else 2
   assert prop(zone,'CurrentWave')==wave and prop(zone,'SpawnedCount')==wave*2
   assert gate.get_actor_enable_collision() and not prop(gate,'bUnlocked')
   enemies=prop(zone,'EncounterEnemies');assert len(enemies)==2
   for enemy in enemies:
    eh=next(c for c in enemy.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_E_Health_C');eh.call_method('E_Decrease_Health',(100.0,))
    assert prop(enemy,'bIsDead') and not enemy.get_actor_enable_collision()
   s.update(stage='intermission' if wave==1 else 'clear',since=now)
  elif stage=='intermission' and prop(zone,'Phase')==2:s.update(stage='second',since=now)
  elif stage=='clear' and prop(zone,'bCleared'):
   assert prop(zone,'SpawnedCount')==4 and gate.get_actor_enable_collision() and not prop(b,'bActivated')
   s.update(stage='wait_refuge',since=now)
  elif stage=='wait_refuge' and not board.get_value_as_bool('bMustFlee'):s.update(stage='escort',since=now)
  elif stage=='escort':
   target=b.get_actor_location();player.set_actor_location(target+unreal.Vector(0,360,35),False,True);hostage.set_actor_location(target+unreal.Vector(140,420,35),False,True)
   for key,value in [('bMustFlee',False),('bEnemyNear',False),('bWaiting',True),('bAccompanying',False)]:board.set_value_as_bool(key,value)
   hostage.call_method('Interactuar');assert board.get_value_as_bool('bAccompanying')
   s.update(stage='channel',since=now,saw_progress=False)
  elif stage=='channel':
   if prop(hostage,'bUsingBeacon') and prop(hostage,'ActivationProgress')>0:s['saw_progress']=True
   if prop(mission,'Paso')==i+1:
    assert s['saw_progress'],'No visible channel progress'
    assert prop(b,'bActivated') and prop(gate,'bUnlocked') and not prop(gate,'bDestroyed')
    assert prop(player,'bHammerUpgraded') and prop(player,'bIsHammerEquipped')
    assert not prop(player,'bIsSwordEquipped')
    assert prop(player,'hammer').is_visible() and not prop(player,'Weapon').is_visible()
    assert not prop(hostage,'bUsingBeacon')
    swing_reset();attack(gate);attack(gate);assert prop(gate,'Health')==25,'Overlap cache failed'
    swing_reset();attack(gate);assert prop(gate,'bDestroyed') and not gate.get_actor_enable_collision()
    flags(player,IsAttacking=False);s.update(stage='route',since=now)
  elif stage=='route' and now-s['since']>2:
   target=unreal.Vector(-3200,-4800,0) if i==0 else (unreal.Vector(3200,-9620,0) if i==1 else unreal.Vector(0,-11220,0))
   path=unreal.NavigationSystemV1.find_path_to_location_synchronously(world,hostage.get_actor_location(),target,hostage,None)
   if not path or not path.is_valid() or path.is_partial():
    assert now-s['since']<12,'Broken door did not reopen navigation'
    return
   if i<2:
    assert not prop(ds[i+1],'bUnlocked') and ds[i+1].get_actor_enable_collision(),'Upgrade skipped next gate'
    blocked_goal=unreal.Vector(3200,-9620,0) if i==0 else unreal.Vector(0,-11220,0)
    blocked=unreal.NavigationSystemV1.find_path_to_location_synchronously(world,target,blocked_goal,hostage,None)
    assert not blocked or not blocked.is_valid() or blocked.is_partial(),'Next closed gate can be bypassed'
   s['results'].append({'beacon':i+1,'hostage_channel':True,'automatic_hammer':True,'two_heavy_hits':True,'dynamic_route':True,'route_seconds':round(now-s['since'],2),'horde_enemies':4 if i<2 else 0})
   if i<2:s.update(index=i+1,stage='enter',since=now)
   else:
    exit=prop(mission,'Salida').get_actor_location();player.set_actor_location(exit+unreal.Vector(0,0,95),False,True);hostage.set_actor_location(exit+unreal.Vector(150,150,95),False,True);s.update(stage='win',since=now)
  elif stage=='win' and prop(mission,'Paso')==4:
   unreal.unregister_slate_post_tick_callback(s['handle'])
   with open(os.path.join(root,'Intermediate/inspect/progression_assertions.json'),'w') as f:json.dump({'passed':True,'locked_light_unpowered_damage':0,'friendly_fire':0,'zones':s['results'],'escort_extraction':True},f,indent=2)
   unreal.log('PROGRESSION_ASSERTIONS_PASSED');return
  assert now-s['since']<35,'Timeout '+stage+' beacon '+str(i+1)
 except Exception:
  unreal.unregister_slate_post_tick_callback(s['handle'])
  with open(os.path.join(root,'Intermediate/inspect/progression_assertions.json'),'w') as f:json.dump({'passed':False,'stage':s['stage'],'index':s['index'],'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('PROGRESSION_ASSERTIONS_STARTED')
