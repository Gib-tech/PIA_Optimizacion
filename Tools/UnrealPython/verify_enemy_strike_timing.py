"""Isolated PIE encounter: real trees/locomotion/montages, no direct damage for hits."""
import unreal,os,json,traceback
timing_world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert timing_world
timing_gs=unreal.GameplayStatics;timing_native=unreal.get_default_object(timing_gs.static_class())
timing_system=unreal.get_default_object(unreal.SystemLibrary.static_class())
timing_player=timing_gs.get_player_character(timing_world,0)
timing_hostage=timing_gs.get_actor_of_class(timing_world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
timing_hud=timing_gs.get_player_controller(timing_world,0).get_hud()
timing_hostage.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Isolated strike timing')
timing_hbb=timing_hostage.get_controller().get_component_by_class(unreal.BlackboardComponent)
timing_hbb.set_value_as_bool('bRescued',False)
timing_hostage.set_actor_location(unreal.Vector(0,-10000,100),False,True)
timing_player.set_actor_location(unreal.Vector(0,-2000,100),False,True)
timing_montage=unreal.load_asset('/Game/ThirdPerson/Blueprints/EnemigoIA/AM_EnemyAttack_Entrega')
timing_root=unreal.Paths.project_dir()
timing_cases=[('BP_BaseEnemy','player'),('BP_ChargerEnemy','player'),('BP_BaseEnemy','hostage'),('BP_ChargerEnemy','hostage')]
timing_state={'case':-1,'enemy':None,'samples':[],'results':[],'at':0,'handle':None,'impact_seen_at':None}

def timing_hp(victim):
    if victim==timing_hostage:return victim.get_editor_property('Health')
    return victim.get_component_by_class(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C')).get_editor_property('Health')

def timing_next(s):
    if s['enemy']:s['enemy'].destroy_actor()
    s['case']+=1;s['samples']=[];s['impact_seen_at']=None
    if s['case']==len(timing_cases):return False
    name,victim_name=timing_cases[s['case']]
    victim=timing_player if victim_name=='player' else timing_hostage
    if victim==timing_hostage:
        timing_player.set_actor_location(unreal.Vector(2400,-2000,100),False,True)
        timing_hostage.set_actor_location(unreal.Vector(0,-2000,100),False,True)
        timing_hbb.set_value_as_bool('bRescued',True)
        timing_system.call_method('SetDoublePropertyByName',(timing_hostage,'Health',100.))
        timing_system.call_method('SetDoublePropertyByName',(timing_hostage,'InvulnerableUntil',0.))
    else:timing_player.set_actor_location(unreal.Vector(0,-2000,100),False,True)
    cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/'+name+'.'+name+'_C')
    tr=unreal.Transform(location=unreal.Vector(0,-2500,100))
    enemy=timing_native.call_method('BeginDeferredActorSpawnFromClass',(timing_world,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));timing_native.call_method('FinishSpawningActor',(enemy,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
    brain=enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent);brain.stop_logic('Test distant request first')
    enemy.call_method('Attack',(victim,));assert not enemy.get_editor_property('bAttackInProgress'),'Distant attack was accepted'
    assert not enemy.mesh.get_anim_instance().montage_is_playing(timing_montage)
    s.update(enemy=enemy,victim=victim,start_hp=timing_hp(victim),at=timing_gs.get_time_seconds(timing_world))
    brain.restart_logic();return True

def timing_tick(dt,s=timing_state):
    try:
        now=timing_gs.get_time_seconds(timing_world);age=now-s['at'];enemy=s['enemy'];victim=s['victim']
        anim=enemy.mesh.get_anim_instance();playing=anim.montage_is_playing(timing_montage)
        sample={'t':round(age,3),'distance':round(enemy.get_distance_to(victim),2),'attacking':enemy.get_editor_property('bAttackInProgress'),'montage':playing,'position':round(anim.montage_get_position(timing_montage),3),'speed':round(enemy.get_velocity().length(),2),'hp':timing_hp(victim),'charging':enemy.get_controller().get_component_by_class(unreal.BlackboardComponent).get_value_as_bool('bCharging')}
        s['samples'].append(sample)
        if playing:assert sample['distance']<=225,('Remote attack montage',sample)
        if sample['hp']<s['start_hp'] and s['impact_seen_at'] is None:
            assert abs(s['start_hp']-sample['hp']-13.2)<.001,sample
            assert playing and .30<=sample['position']<=.73,('Damage outside montage impact',sample)
            assert sample['speed']<10,('Sliding strike',sample)
            s['impact_seen_at']=now
            if victim==timing_hostage:
                assert victim.get_editor_property('DamageNoticeSerial')>0
                s['serial']=victim.get_editor_property('DamageNoticeSerial')
                timing_gs.apply_damage(victim,13.2,None,enemy,None)
                assert victim.get_editor_property('DamageNoticeSerial')==s['serial'],'Invulnerability produced a false alert'
        if s['impact_seen_at'] is not None and now-s['impact_seen_at']>.15:
            if victim==timing_hostage:assert timing_hud.get_editor_property('HostageHurtUntil')>timing_gs.get_real_time_seconds(timing_world),'Missing hostage warning'
            s['results'].append({'enemy':timing_cases[s['case']][0],'victim':timing_cases[s['case']][1],'distant_request_rejected':True,'damage':13.2,'samples':s['samples']})
            if not timing_next(s):
                unreal.unregister_slate_post_tick_callback(s['handle'])
                with open(os.path.join(timing_root,'Intermediate/inspect/enemy_strike_timing.json'),'w') as f:json.dump({'passed':True,'isolated_real_tree_test':True,'cases':s['results']},f,indent=2)
                unreal.log('ENEMY_STRIKE_TIMING_ALL_FOUR_CASES_PASSED')
        assert age<22,('Timed out',timing_cases[s['case']],s['samples'][-1])
    except Exception:
        unreal.unregister_slate_post_tick_callback(s['handle'])
        if s['enemy']:s['enemy'].destroy_actor()
        with open(os.path.join(timing_root,'Intermediate/inspect/enemy_strike_timing.json'),'w') as f:json.dump({'passed':False,'case':s['case'],'error':traceback.format_exc(),'samples':s['samples'],'previous':s['results']},f,indent=2)
        unreal.log_error(traceback.format_exc())

timing_next(timing_state);timing_state['handle']=unreal.register_slate_post_tick_callback(timing_tick)
