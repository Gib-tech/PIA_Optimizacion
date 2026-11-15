"""Observe the real charger Behavior Tree over time in PIE, without blocking the editor."""
import unreal,os,json,traceback
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert world
player=unreal.GameplayStatics.get_player_pawn(world,0)
player.set_actor_location(unreal.Vector(0,-2000,100),False,True)
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
lib.call_method('SetBoolPropertyByName',(player,'bCanBeDamaged',True))
health=next(c for c in player.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_Health_C')
lib.call_method('SetDoublePropertyByName',(health,'Health',100.0))
cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_ChargerEnemy.BP_ChargerEnemy_C')
transform=unreal.Transform(location=unreal.Vector(0,-2600,100))
statics=unreal.get_default_object(unreal.GameplayStatics.static_class())
enemy=statics.call_method('BeginDeferredActorSpawnFromClass',(world,cls,transform,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
statics.call_method('FinishSpawningActor',(enemy,transform,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
controller=enemy.get_controller();bb=controller.get_component_by_class(unreal.BlackboardComponent);brain=controller.get_component_by_class(unreal.BehaviorTreeComponent)
unreal.log('CHARGER_OBSERVER_CONTROLLER '+controller.get_class().get_name()+' brain='+str(brain)+' bb='+str(bb))
state={'start':unreal.GameplayStatics.get_time_seconds(world),'samples':[],'handle':None,'last':-1}
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
def observe_charger(delta,w=world,p=player,e=enemy,board=bb,tree=brain,s=state,project=root,hp=health):
    try:
        t=unreal.GameplayStatics.get_time_seconds(w)-s['start']
        if t-s['last']>=0.05:
            s['last']=t;active=[]
            for name,ids in [('BTTask_ChargerWindup_C',[12]),('BTTask_ChargerCharge_C',[3]),('BTTask_ChargerRetreat_C',[5,9]),('BTTask_ChargerRecover_C',[7,11])]:
                for suffix in [name+'_'+str(i) for i in range(32)]+['Instance_'+str(i) for i in ids]:
                    obj=unreal.find_object(None,tree.get_path_name()+'.'+suffix)
                    if obj and obj.get_class().get_name()==name and obj.is_task_executing():active.append(name)
            hand=e.mesh.get_socket_transform('hand_r',unreal.RelativeTransformSpace.RTS_COMPONENT).translation
            s['samples'].append({'t':round(t,3),'distance':round(e.get_distance_to(p),1),'sensed_distance':board.get_value_as_float('DistanceToTarget'),'speed':round(e.get_velocity().length(),1),'charging':board.get_value_as_bool('bCharging'),'retreat':board.get_value_as_bool('bRetreat'),'tasks':active,'montage':e.get_current_montage().get_name() if e.get_current_montage() else None,'player_hp':hp.get_editor_property('Health'),'hand':[hand.x,hand.y,hand.z]})
        if t>=14:
            unreal.unregister_slate_post_tick_callback(s['handle'])
            data=s['samples'];seen={name for sample in data for name in sample['tasks']}
            result={'seen_tasks':sorted(seen),'max_speed':max(x['speed'] for x in data),'max_distance':max(x['distance'] for x in data),'samples':data}
            hits=[a['player_hp']-b['player_hp'] for a,b in zip(data,data[1:]) if a['player_hp']>b['player_hp']]
            motion=max(unreal.Vector(*x['hand']).distance(unreal.Vector(*data[0]['hand'])) for x in data)
            result.update(contact_damage_events=hits,original_mesh=e.mesh.get_skeletal_mesh_asset().get_name(),hand_motion_cm=round(motion,1))
            result['passed']=all(name in seen for name in ['BTTask_ChargerWindup_C','BTTask_ChargerCharge_C','BTTask_ChargerRetreat_C']) and result['max_speed']>=800 and bool(hits) and all(x==6 for x in hits) and motion>5
            with open(os.path.join(project,'Intermediate/inspect/charger_cycle_assertions.json'),'w') as f:json.dump(result,f,indent=2)
            e.destroy_actor();unreal.log('CHARGER_CYCLE_RESULT '+json.dumps({k:v for k,v in result.items() if k!='samples'}))
    except Exception:
        unreal.unregister_slate_post_tick_callback(s['handle']);unreal.log_error(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(observe_charger)
unreal.log('CHARGER_CYCLE_OBSERVER_STARTED')
