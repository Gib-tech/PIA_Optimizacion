"""Evaluation rework traversal with gameplay movement/attacks, no teleport/health edits.

This is an automated regression, not the owner's manual FIN-01 acceptance.
Run on a fresh Nivel_Entrega PIE. Stop with Intermediate/inspect/stop_fluid_walk.flag.
"""
import unreal, math, json, os, traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_character(w,0)
R='/Game/ThirdPerson/Blueprints/Entrega/'
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,R+'BP_DirectorEntrega.BP_DirectorEntrega_C'))
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
zones=[d.get_editor_property('Zona'+str(i)) for i in (1,2)]
beacons=[d.get_editor_property('Baliza'+str(i)) for i in (1,2,3)]
doors=[b.get_editor_property('Door') for b in beacons]
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
resume_path=os.path.join(root,'Intermediate/inspect/resume_fluid_walk.flag')
resume=os.path.exists(resume_path)
if not resume:assert d.get_editor_property('Paso')==0 and all(z.get_editor_property('Phase')==0 for z in zones),'Fresh new game required'
out=os.path.join(root,'Intermediate/inspect/fluid_mission_playthrough.json')
stop=os.path.join(root,'Intermediate/inspect/stop_fluid_walk.flag')
assert not os.path.exists(stop),'Remove the previous stop flag before starting'
if resume:
    assert state['stage']=='beacon','Resume only supports correcting the bot beacon approach'
    unreal.unregister_slate_post_tick_callback(state['handle'])
    state.update(path=[],path_time=-10,goal=None)
    state['events'].append({'stage':'bot_beacon_approach_adjusted_without_teleport','time':round(unreal.GameplayStatics.get_time_seconds(w)-state['started'],2)})
    os.remove(resume_path)
else:
    state={'stage':'rescue','index':0,'started':unreal.GameplayStatics.get_time_seconds(w),'since':0,'last_attack':-10,'last_log':-10,'events':[],'handle':None,'path':[],'path_time':-10,'goal':None,'samples':[]}

def prop(o,k):return o.get_editor_property(k)
def horizontal(v):return math.hypot(v.x,v.y)
def finish(passed,reason,s=state):
    result={'agent_tests_not_owner_acceptance':True,'no_teleports':True,'no_health_or_damage_overrides':True,'input_transport':'Pawn movement input with combat guards, real Enhanced Input attack handlers, normal interaction in range; no transform edits','passed':passed,'reason':reason,'stage':s['stage'],'events':s['events'],'samples':s['samples']}
    with open(out,'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
    unreal.unregister_slate_post_tick_callback(s['handle']);unreal.log('FLUID_WALK_FINISHED '+str(passed)+' '+reason)

def direction_input(dv):
    # Same pawn movement input consumed by CharacterMovement, with normal combat locks.
    length=horizontal(dv)
    if length<1 or p.get_editor_property('IsAttacking'):return
    if p.get_editor_property('CurrentState').value!=0:return
    p.add_movement_input(unreal.Vector(dv.x/length,dv.y/length,0),1,False)

def move(goal,now,s=state):
    here=p.get_actor_location();delta=goal-here
    if horizontal(delta)<65:return True
    if s['goal'] is None or horizontal(goal-s['goal'])>100 or now-s['path_time']>1:
        path=unreal.NavigationSystemV1.find_path_to_location_synchronously(w,here,goal,p,None)
        if not path or not path.is_valid() or path.is_partial():
            s['path']=[]
        else:s['path']=list(path.path_points)[1:]
        s['goal']=goal;s['path_time']=now
    while len(s['path'])>1 and horizontal(s['path'][0]-here)<35:s['path'].pop(0)
    target=s['path'][0] if s['path'] else goal
    dv=target-here;length=horizontal(dv)
    if length>1:direction_input(dv)
    return False

def face(target):
    delta=target-p.get_actor_location()
    p.get_controller().set_control_rotation(unreal.Rotator(pitch=0,yaw=math.degrees(math.atan2(delta.y,delta.x)),roll=0))

def attack(heavy,now,s=state):
    # A deliberate press after recovery, rather than buffering attacks while
    # the target has already retreated or crossed to another side.
    if now-s['last_attack']<.18 or p.get_editor_property('IsAttacking'):return
    name='Heavy_Attack' if heavy else 'Light_Attack'
    fn='InpActEvt_IA_'+name+'_K2Node_EnhancedInputActionEvent_'+('6' if heavy else '7')
    p.call_method(fn,(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_'+name)))
    s['last_attack']=now

def stage(name,now,s=state):
    s['events'].append({'stage':name,'time':round(now-s['started'],2)})
    s.update(stage=name,since=now,path=[],goal=None)

def observe(delta,s=state):
    try:
        now=unreal.GameplayStatics.get_time_seconds(w);age=now-s['since'];i=s['index']
        if os.path.exists(stop):finish(False,'Stopped by operator');return
        step=prop(d,'Paso')
        if step==4:finish(True,'Complete mission through gameplay movement and attacks');return
        if step>=5:finish(False,'Defeat: '+('hostage' if step==6 else 'player'));return
        if now-s['started']>420:finish(False,'Traversal exceeded seven minutes');return
        if now-s['last_log']>3:
            position=p.get_actor_location()
            sample={'t':round(now-s['started'],1),'stage':s['stage'],'player':[round(position.x),round(position.y)],'player_health':prop(prop(p,'BPC_Health'),'Health'),'hostage_health':prop(h,'Health'),'zones':[prop(z,'Phase') for z in zones]}
            s['samples'].append(sample);s['last_log']=now
            unreal.log('FLUID_WALK '+json.dumps(sample))
            with open(out,'w',encoding='utf-8') as f:json.dump({'running':True,'latest':sample,'events':s['events']},f,ensure_ascii=False,indent=2)
        current=s['stage']
        if current in ('rescue','recover'):
            point=h.get_actor_location()
            if horizontal(point-p.get_actor_location())>230:move(point,now)
            else:
                h.call_method('Interactuar')
                if bb.get_value_as_bool('bAccompanying'):stage('enter' if current=='rescue' else 'door',now)
        elif current=='enter':
            zone=zones[i]
            move(zone.get_actor_location(),now)
            if prop(zone,'Phase')>0:stage('combat',now)
        elif current=='combat':
            zone=zones[i]
            enemies=[e for e in prop(zone,'EncounterEnemies') if unreal.SystemLibrary.is_valid(e) and not prop(e,'bIsDead')]
            if enemies:
                target=min(enemies,key=lambda e:.7*h.get_distance_to(e)+.3*p.get_distance_to(e));point=target.get_actor_location();face(point)
                distance=p.get_distance_to(target)
                delta=point-p.get_actor_location()
                yaw=math.degrees(math.atan2(delta.y,delta.x))
                facing=abs((yaw-p.get_actor_rotation().yaw+180)%360-180)
                # Looking with the controller does not rotate a root-motion attack.
                # Let locomotion face the next enemy before queuing another combo.
                if distance>110 or facing>15:move(point,now)
                if distance<125 and facing<15:
                    # Close, deliberate sword hits avoid queuing a long attack after
                    # the target has already retreated. Heavy hits open doors.
                    attack(False,now)
            elif prop(zone,'bCleared'):stage('recover',now)
        elif current=='beacon':
            # Walk clear of the pedestal before taking a new cross-courtyard path.
            # A shortest nav path from its capsule edge can point back into the mesh.
            departure=s.get('departure')
            if departure is None:
                for completed in beacons:
                    center=completed.get_actor_location();here=p.get_actor_location()
                    if prop(completed,'bActivated') and horizontal(here-center)<330:
                        sign=1 if here.x>=center.x else -1
                        departure=unreal.Vector(center.x+sign*400,center.y+500,here.z)
                        s['departure']=departure
                        break
            if departure is not None:
                delta=departure-p.get_actor_location();length=horizontal(delta)
                if length>80:
                    direction_input(delta)
                    return
                s['departure']=None;s.update(path=[],goal=None)
            beacon=prop(d,'CurrentBeacon');point=prop(beacon,'ApproachPoint').get_actor_location()+unreal.Vector(180,-60,0)
            if horizontal(point-p.get_actor_location())>65:move(point,now)
            if prop(d,'Paso')==3:stage('door',now)
            elif bb.get_value_as_bool('bWaiting') and not bb.get_value_as_bool('bMustFlee') and p.get_distance_to(h)<380:h.call_method('Interactuar')
        elif current=='door':
            door=doors[i];point=door.get_actor_location();delta=point-p.get_actor_location();distance=horizontal(delta)
            face(point)
            if distance>180:
                goal=point-unreal.Vector(delta.x/distance*150,delta.y/distance*150,0);goal.z=p.get_actor_location().z
                move(goal,now)
            else:
                yaw=math.degrees(math.atan2(delta.y,delta.x))
                facing=abs((yaw-p.get_actor_rotation().yaw+180)%360-180)
                if facing>30:move(point,now)
                else:attack(True,now)
            if prop(door,'bDestroyed'):
                s['index']+=1
                stage('enter' if s['index']==1 else 'beacon' if s['index']==2 else 'extract',now)
        elif current=='extract':
            point=prop(d,'Salida').get_actor_location();move(point,now)
            if bb.get_value_as_bool('bWaiting') and p.get_distance_to(h)<380:h.call_method('Interactuar')
    except Exception:finish(False,traceback.format_exc())

state['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('FLUID_WALK_STARTED')
