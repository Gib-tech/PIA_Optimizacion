"""PIE integration: cancel an attack with hit stun, then observe a full attack and death cleanup."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);p.set_actor_location(unreal.Vector(0,-2000,100),False,True)
lib=unreal.get_default_object(unreal.SystemLibrary.static_class());lib.call_method('SetBoolPropertyByName',(p,'bCanBeDamaged',True))
hp=next(c for c in p.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_Health_C');lib.call_method('SetDoublePropertyByName',(hp,'Health',100.0))
cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
t=unreal.Transform(location=unreal.Vector(0,-2170,100));statics=unreal.get_default_object(unreal.GameplayStatics.static_class())
enemy=statics.call_method('BeginDeferredActorSpawnFromClass',(w,cls,t,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));statics.call_method('FinishSpawningActor',(enemy,t,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
health=next(c for c in enemy.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_E_Health_C')
state={'stage':'first','start':unreal.GameplayStatics.get_time_seconds(w),'handle':None,'result':{}}
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
def observe_lifecycle(delta,world=w,player=p,e=enemy,eh=health,ph=hp,s=state,project=root):
    try:
        now=unreal.GameplayStatics.get_time_seconds(world);elapsed=now-s['start'];value=ph.get_editor_property('Health')
        busy=e.get_editor_property('bAttackInProgress') if unreal.SystemLibrary.is_valid(e) else False
        if s['stage']=='first' and busy:s.update(stage='interrupt',attack_at=now)
        elif s['stage']=='interrupt' and now-s['attack_at']>=.2:
            assert value==100.0,'Attack applied damage before the impact frame'
            eh.call_method('E_Decrease_Health',(1.0,));s.update(stage='cancelled',cancel_at=now)
        elif s['stage']=='cancelled' and now-s['cancel_at']>=1.4:
            assert value==100.0,'Interrupted attack still hit'
            s['result']['interrupted_damage']=0;s.update(stage='second')
        elif s['stage']=='second' and busy:s.update(stage='impact',attack_at=now)
        elif s['stage']=='impact' and value<100:
            delay=now-s['attack_at'];assert .35<=delay<=.65,delay
            assert value==94.0,value
            s['result'].update(impact_seconds=round(delay,3),attack_damage=6);s.update(stage='finish')
        elif s['stage']=='finish' and not busy:
            duration=now-s['attack_at'];assert 1.2<=duration<=1.6,duration
            assert value==94.0,'One attack applied damage more than once'
            s['result']['attack_seconds']=round(duration,3)
            eh.call_method('E_Decrease_Health',(100.0,));s.update(stage='death',death_at=now)
        elif s['stage']=='death' and now-s['death_at']>=.3:
            assert e.get_editor_property('bIsDead') and not e.get_actor_enable_collision()
            assert not e.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).is_running()
            assert e.get_current_montage().get_name()=='AM_EnemyDeath_Entrega'
            s['result']['death_stops_tree_and_collision']=True;s.update(stage='cleanup')
        elif s['stage']=='cleanup' and now-s['death_at']>=3.3:
            assert not unreal.SystemLibrary.is_valid(e),'Corpse did not clean up'
            s['result'].update(passed=True,death_cleanup=True)
            unreal.unregister_slate_post_tick_callback(s['handle'])
            with open(os.path.join(project,'Intermediate/inspect/animation_assertions.json'),'w') as f:json.dump(s['result'],f,indent=2)
            unreal.log('ENEMY_ANIMATION_ASSERTIONS_PASSED '+json.dumps(s['result']));return
        assert elapsed<25,'Lifecycle test timed out at '+s['stage']
    except Exception:
        unreal.unregister_slate_post_tick_callback(s['handle'])
        with open(os.path.join(project,'Intermediate/inspect/animation_assertions.json'),'w') as f:json.dump({'passed':False,'stage':s['stage'],'error':traceback.format_exc()},f,indent=2)
        unreal.log_error(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(observe_lifecycle)
unreal.log('ENEMY_ANIMATION_ASSERTIONS_STARTED')
