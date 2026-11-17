"""Isolated PIE regression: all 6 real channel orders, guards, timer and persistence.

Sets completed encounters/positions for isolation; this is not a manual playthrough.
"""
import unreal,os,json,traceback,time,itertools
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;R='/Game/ThirdPerson/Blueprints/Entrega/'
d=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DirectorEntrega.BP_DirectorEntrega_C'))
m=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
p=m.get_editor_property('Hero');h=m.get_editor_property('Hostage')
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
bs=[d.get_editor_property('Baliza'+str(i)) for i in (1,2,3)]
ds=[b.get_editor_property('Door') for b in bs]
zs=[d.get_editor_property('Zona'+str(i)) for i in (1,2,3)]
sys=unreal.get_default_object(unreal.SystemLibrary.static_class())
prop=lambda o,k:o.get_editor_property(k)
def put(o,k,v):
 kind='Bool' if isinstance(v,bool) else 'Int' if isinstance(v,int) else 'Double'
 sys.call_method('Set'+kind+'PropertyByName',(o,k,v))

assert prop(d,'MissionElapsed')==0,'Timer ran before rescue'
assert all(not prop(b,'bActivated') for b in bs)
assert all(not prop(door,'bUnlocked') for door in ds)
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if prop(cinema,'bActive'):cinema.call_method('FinishCinema')
# All six directed paths must be reachable without opening the final bulkhead.
paths=[]
for a in bs:
 for b in bs:
  if a==b:continue
  path=unreal.NavigationSystemV1.find_path_to_location_synchronously(w,prop(a,'ApproachPoint').get_actor_location(),prop(b,'ApproachPoint').get_actor_location(),h,None)
  assert path and path.is_valid() and not path.is_partial(),(prop(a,'Index'),prop(b,'Index'))
  paths.append([prop(a,'Index'),prop(b,'Index')])

for z in zs:put(z,'bCleared',True);put(z,'Phase',3)
bb.set_value_as_bool('bRescued',True)
state={'stage':'gates','code':0,'index':0,'since':gs.get_time_seconds(w),'handle':None,'orders':[],
       'result':{'agent_test_not_owner_acceptance':True,'isolated_state_setup':True,'all_six_directed_paths':paths}}
orders=list(itertools.permutations(range(3)))
out=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/beacon_sequence_assertions.json')

def observe(dt,world=w,mission=d,manager=m,player=p,hostage=h,board=bb,beacons=bs,doors=ds,zones=zs,s=state,orders=orders,put=put,prop=prop,out=out):
 try:
  now=gs.get_time_seconds(world);stage=s['stage']
  if stage=='gates':
   if not all(prop(door,'bUnlocked') for door in doors[:2]):return
   assert not prop(doors[2],'bUnlocked'),'Final door opened before sequence'
   assert prop(player,'bHammerUpgraded') and prop(player,'bIsHammerEquipped')
   # Retain actual two-hit damage guards while making navigation available.
   put(player,'IsAttacking',True);put(player,'bLightAttackActive',False)
   for door in doors[:2]:
    gs.apply_damage(door,25,None,player,None);assert prop(door,'Health')==25
    gs.apply_damage(door,25,None,player,None);assert prop(door,'bDestroyed')
   put(player,'IsAttacking',False)
   s['result']['encounters_unlock_first_two_doors_and_two_hits']=True
   # Even a complete valid channel cannot bypass the final guardian revelation.
   correct=beacons[orders[prop(mission,'OrderCode')][0]]
   hostage.set_actor_location(prop(correct,'ApproachPoint').get_actor_location()+unreal.Vector(0,-30,100),False,True)
   put(hostage,'bUsingBeacon',True);put(hostage,'ActivationProgress',1.0)
   correct.call_method('CompleteActivation',(hostage,))
   assert not prop(correct,'bActivated') and prop(mission,'Paso')==0
   s['result']['complete_channel_rejected_before_revelation']=True
   put(mission,'bOrderRevealed',True)
   s.update(stage='reset',since=now)
  elif stage=='reset':
   hostage.get_controller().get_component_by_class(unreal.BrainComponent).stop_logic('Isolated permutation setup')
   for b in beacons:put(b,'bActivated',False)
   put(doors[2],'bUnlocked',False);put(mission,'Paso',0);put(mission,'OrderCode',s['code'])
   put(hostage,'bUsingBeacon',False);put(hostage,'ActivationProgress',0.0)
   board.set_value_as_bool('bActivateBeacon',False)
   for key,val in [('bRescued',True),('bAccompanying',True),('bWaiting',False),('bMustFlee',False),('bEnemyNear',False)]:board.set_value_as_bool(key,val)
   # Exercise rejection at the wrong beacon with otherwise complete channel state.
   wrong=beacons[(orders[s['code']][0]+1)%3]
   hostage.set_actor_location(prop(wrong,'ApproachPoint').get_actor_location()+unreal.Vector(0,-30,100),False,True)
   put(hostage,'bUsingBeacon',True);put(hostage,'ActivationProgress',1.0)
   wrong.call_method('CompleteActivation',(hostage,))
   assert not prop(wrong,'bActivated') and prop(mission,'Paso')==0,'Out-of-order beacon accepted'
   put(hostage,'bUsingBeacon',False);put(hostage,'ActivationProgress',0.0)
   s.update(stage='approach',index=0,since=now)
  elif stage=='approach':
   b=beacons[orders[s['code']][s['index']]];pos=prop(b,'ApproachPoint').get_actor_location()
   player.set_actor_location(pos+unreal.Vector(0,200,100),False,True)
   hostage.set_actor_location(pos+unreal.Vector(0,-30,100),False,True)
   for key,val in [('bAccompanying',True),('bWaiting',False),('bMustFlee',False),('bEnemyNear',False),('bActivateBeacon',False)]:board.set_value_as_bool(key,val)
   hostage.get_controller().get_component_by_class(unreal.BrainComponent).restart_logic()
   s.update(stage='channel',since=now,saw_progress=False)
  elif stage=='channel':
   if prop(hostage,'bUsingBeacon') and prop(hostage,'ActivationProgress')>.05:s['saw_progress']=True
   if prop(mission,'Paso')==s['index']+1:
    b=beacons[orders[s['code']][s['index']]]
    assert prop(b,'bActivated') and s['saw_progress'],'Channel did not run through Behavior Tree'
    assert sum(prop(b,'bActivated') for b in beacons)==s['index']+1
    assert prop(doors[2],'bUnlocked')==(s['index']==2),'Final door unlocked at wrong count'
    if s['index']<2:s.update(stage='approach',index=s['index']+1,since=now)
    else:
     s['orders'].append({'code':s['code'],'order':['ABC'[i] for i in orders[s['code']]],'three_real_channels':True})
     if s['code']<5:s.update(stage='reset',code=s['code']+1,since=now)
     else:
      s.update(stage='pause',since=now,elapsed=prop(mission,'MissionElapsed'),real=time.monotonic())
      gs.set_game_paused(world,True)
  elif stage=='pause':
   if time.monotonic()-s['real']<1:return
   assert prop(mission,'MissionElapsed')==s['elapsed'],'Mission clock advanced while paused'
   gs.set_game_paused(world,False)
   s['result']['pause_freezes_mission_clock']=True
   s.update(stage='save',since=now)
  elif stage=='save' and now-s['since']>1:
   assert prop(mission,'MissionElapsed')>s['elapsed'],'Clock did not resume'
   board.set_value_as_bool('bActivateBeacon',False);put(hostage,'bUsingBeacon',False);put(hostage,'ActivationProgress',0.0)
   manager.call_method('SaveCheckpoint')
   assert prop(manager,'bSaveSucceeded'),'Safe save rejected'
   data=gs.load_game_from_slot('TimeOut_Delivery_v1',0)
   elapsed=prop(data,'MissionElapsed');assert elapsed>0 and prop(data,'OrderCode')==5 and prop(data,'Version')==2
   put(mission,'OrderCode',0);put(mission,'MissionElapsed',0.0)
   manager.call_method('RestoreCheckpoint')
   assert prop(mission,'OrderCode')==5 and prop(mission,'MissionElapsed')==elapsed
   assert prop(mission,'Paso')==3 and all(prop(b,'bActivated') for b in beacons)
   s['result']['checkpoint_restores_order_time_and_activations']=True
   previous=prop(gs.get_game_instance(world),'LastBeaconOrder');draws=[]
   for _ in range(24):
    mission.call_method('ReceiveBeginPlay')
    drawn=prop(mission,'OrderCode');assert 0<=drawn<6 and drawn!=previous
    draws.append(drawn);previous=drawn
   s['result']['new_attempt_initialization_24_draws_no_adjacent_repeat']=draws
   manager.call_method('RestoreCheckpoint')
   put(player,'IsAttacking',True);put(player,'bLightAttackActive',False)
   gs.apply_damage(doors[2],25,None,player,None);assert prop(doors[2],'Health')==25
   gs.apply_damage(doors[2],25,None,player,None);assert prop(doors[2],'bDestroyed')
   put(player,'IsAttacking',False)
   end=prop(mission,'Salida').get_actor_location()
   player.set_actor_location(end+unreal.Vector(0,0,100),False,True)
   hostage.set_actor_location(end+unreal.Vector(150,0,100),False,True)
   board.set_value_as_bool('bAccompanying',True)
   finaltime=prop(mission,'MissionElapsed');mission.call_method('ReceiveTick',(.016,))
   assert prop(mission,'Paso')==4
   assert prop(mission,'MissionElapsed')==finaltime
   s.update(stage='cinematic',since=now,finaltime=finaltime)
  elif stage=='cinematic':
   if not gs.is_game_paused(world):return
   assert prop(mission,'MissionElapsed')==s['finaltime']
   s['result']['final_door_two_hits_extraction_and_clock_stop']=True
   s['result']['orders']=s['orders'];s['result']['out_of_order_rejected_all_six']=True
   s['result']['passed']=True
   with open(out,'w') as f:json.dump(s['result'],f,indent=2)
   unreal.unregister_slate_post_tick_callback(s['handle']);unreal.log('BEACON_SEQUENCE_PASSED');return
  if s['stage'] not in ['pause','save']:assert now-s['since']<25,'Timeout '+s['stage']+' '+str(s['code'])+' '+str(s['index'])
 except Exception:
  unreal.unregister_slate_post_tick_callback(s['handle'])
  s['result'].update(passed=False,error=traceback.format_exc(),stage=s['stage'],code=s['code'],index=s['index'])
  with open(out,'w') as f:json.dump(s['result'],f,indent=2)
  unreal.log_error(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('BEACON_SEQUENCE_TEST_STARTED')
