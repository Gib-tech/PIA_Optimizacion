"""Observe the actual second-zone trees: local escort escape and repeated charger cycles."""
import unreal,json,os,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0)
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
z=d.get_editor_property('Zona2');bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
for a in [p,h]:lib.call_method('SetBoolPropertyByName',(a,'bCanBeDamaged',False))
lib.call_method('SetIntPropertyByName',(d,'Paso',1))
p.set_actor_location(unreal.Vector(-3200,-4500,100),False,True)
h.set_actor_location(unreal.Vector(-3200,-4400,100),False,True)
for key,value in [('bRescued',True),('bAccompanying',True),('bWaiting',False),('bMustFlee',False)]:bb.set_value_as_bool(key,value)
unreal.SystemLibrary.execute_console_command(w,'t.IdleWhenNotForeground 0')
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
s={'start':unreal.GameplayStatics.get_time_seconds(w),'last':-1,'samples':[],'handle':None,'flee_goal':None,'prev':{},'charge_ends':0,'max_path':0}
def observe(dt,world=w,player=p,hostage=h,zone=z,board=bb,state=s,project=root):
 try:
  now=unreal.GameplayStatics.get_time_seconds(world);t=now-state['start']
  if t-state['last']>=.1:
   state['last']=t;enemies=list(zone.get_editor_property('EncounterEnemies'));rows=[]
   for e in enemies:
    ctrl=e.get_controller();b=ctrl.get_component_by_class(unreal.BlackboardComponent);v=e.get_velocity();f=e.get_actor_forward_vector();speed=v.length();dot=f.dot(v/speed) if speed>50 else None
    charging=b.get_value_as_bool('bCharging');previous=state['prev'].get(e.get_name(),False)
    if previous and not charging:state['charge_ends']+=1
    state['prev'][e.get_name()]=charging
    pos=e.get_actor_location();rows.append({'distance':round(e.get_distance_to(player),1),'speed':round(speed,1),'facing_motion':round(dot,3) if dot is not None else None,'charging':charging,'retreat':b.get_value_as_bool('bRetreat'),'location':[round(n,1) for n in [pos.x,pos.y,pos.z]]})
   fleeing=board.get_value_as_bool('bMustFlee');goal=board.get_value_as_vector('FleeLocation')
   if fleeing and state['flee_goal'] is None:
    state['flee_goal']=[goal.x,goal.y,goal.z]
    path=unreal.NavigationSystemV1.find_path_to_location_synchronously(world,hostage.get_actor_location(),goal,hostage,None)
    assert path and path.is_valid() and not path.is_partial(),'Flee route is incomplete'
    state['max_path']=path.get_path_length();assert state['max_path']<=1801,state['max_path']
   state['samples'].append({'t':round(t,2),'hostage_distance':round(hostage.get_distance_to(player),1),'hostage_fleeing':fleeing,'hostage_waiting':board.get_value_as_bool('bWaiting'),'hostage_goal_distance':round(hostage.get_actor_location().distance(goal),1),'enemies':rows})
  if t>=22:
   unreal.unregister_slate_post_tick_callback(state['handle']);data=state['samples'];rows=[e for x in data for e in x['enemies']]
   settled=[x for x in data if x['hostage_waiting'] and not x['hostage_fleeing'] and x['hostage_goal_distance']<130]
   moving=[e for e in rows if e['facing_motion'] is not None and e['speed']>200]
   result={'passed':bool(settled) and state['charge_ends']>=4 and max(e['distance'] for e in rows)<1200,'flee_goal':state['flee_goal'],'flee_path_cm':round(state['max_path'],1),'hostage_reached_local_refuge':bool(settled),'max_hostage_distance_cm':max(x['hostage_distance'] for x in data),'charge_cycles':state['charge_ends'],'max_enemy_distance_cm':max(e['distance'] for e in rows),'forward_motion_fraction':round(sum(e['facing_motion']>0 for e in moving)/max(1,len(moving)),3),'samples':data}
   with open(os.path.join(project,'Intermediate/inspect/ai_refinement_assertions.json'),'w') as f:json.dump(result,f,indent=2)
   unreal.log('AI_REFINEMENT_RESULT '+json.dumps({k:v for k,v in result.items() if k!='samples'}))
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(os.path.join(project,'Intermediate/inspect/ai_refinement_assertions.json'),'w') as f:json.dump({'passed':False,'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('AI_REFINEMENT_OBSERVER_STARTED')
