"""Isolated actual-health callbacks, HUD/audio output and negative feedback cases."""
import unreal,os,json,time,traceback
fb_world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert fb_world
fb_gs=unreal.GameplayStatics;fb_native=unreal.get_default_object(fb_gs.static_class());fb_system=unreal.get_default_object(unreal.SystemLibrary.static_class())
fb_player=fb_gs.get_player_character(fb_world,0);fb_hud=fb_gs.get_player_controller(fb_world,0).get_hud()
fb_hostage=fb_gs.get_actor_of_class(fb_world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
fb_hostage.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Feedback isolation')
fb_hostage.get_controller().get_component_by_class(unreal.BlackboardComponent).set_value_as_bool('bRescued',True)
fb_system.call_method('SetBoolPropertyByName',(fb_hud,'ForceReveal',True))
fb_ambient=fb_hud.get_editor_property('AmbientAudio')
if fb_ambient:fb_ambient.stop()
fb_audio=unreal.get_default_object(unreal.load_class(None,'/Script/AudioMixer.AudioMixerBlueprintLibrary'))
fb_root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());fb_audio_dir=os.path.join(fb_root,'Intermediate/inspect/combat-audio');os.makedirs(fb_audio_dir,exist_ok=True)
fb_state={'stage':'settle','at':time.monotonic(),'handle':None,'results':{},'enemy':None,'busy':False}

def fb_spawn(name):
    cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/'+name+'.'+name+'_C')
    tr=unreal.Transform(location=fb_player.get_actor_location()+unreal.Vector(0,-160,0))
    enemy=fb_native.call_method('BeginDeferredActorSpawnFromClass',(fb_world,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));fb_native.call_method('FinishSpawningActor',(enemy,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
    enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Feedback isolation');return enemy

def fb_damage(enemy,amount):
    health=enemy.get_component_by_class(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health.BPC_E_Health_C'))
    health.call_method('E_Decrease_Health',(amount,));return health

def fb_tick(dt,s=fb_state):
    if s['busy']:return
    try:
        age=time.monotonic()-s['at']
        if s['stage']=='settle' and age>1.2:
            fb_system.call_method('SetBoolPropertyByName',(fb_hud,'ForceReveal',True))
            fb_audio.call_method('StartRecordingOutput',(fb_world,1.,None))
            enemy=fb_spawn('BP_BaseEnemy');s['enemy']=enemy
            fb_damage(enemy,15)
            assert fb_hud.get_editor_property('LastEnemyDamage')==15
            assert fb_hud.get_editor_property('EnemyHitUntil')>fb_gs.get_real_time_seconds(fb_world)
            s['results']['orbiter_damage_marker']=True;s.update(stage='impact_audio',at=time.monotonic())
        elif s['stage']=='impact_audio' and age>.6:
            fb_audio.call_method('StopRecordingOutput',(fb_world,unreal.AudioRecordingExportType.WAV_FILE,'enemy_impact',fb_audio_dir,None,None))
            enemy=s['enemy'];previous=fb_hud.get_editor_property('EnemyHitUntil')
            health=enemy.get_component_by_class(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health.BPC_E_Health_C'))
            fb_system.call_method('SetDoublePropertyByName',(health,'E_Health',95.));enemy.call_method('OnHealthChanged')
            assert fb_hud.get_editor_property('EnemyHitUntil')==previous,'Healing triggered damage feedback'
            s['results']['healing_does_not_confirm_hit']=True
            fb_damage(enemy,200)
            assert fb_hud.get_editor_property('EnemyHitUntil')>previous,'Lethal hit missing feedback'
            assert enemy.get_editor_property('bIsDead')
            s['results']['lethal_hit_confirmed']=True;enemy.destroy_actor()
            s['enemy']=fb_spawn('BP_ChargerEnemy');fb_damage(s['enemy'],25)
            assert fb_hud.get_editor_property('LastEnemyDamage')==25
            s['results']['charger_damage_marker']=True
            # Health restoration must not appear as an accepted hostile hit.
            previous=fb_hostage.get_editor_property('DamageNoticeSerial')
            fb_system.call_method('SetDoublePropertyByName',(fb_hostage,'Health',80.))
            assert fb_hostage.get_editor_property('DamageNoticeSerial')==previous
            fb_gs.apply_damage(fb_hostage,13.2,None,s['enemy'],None)
            assert fb_hostage.get_editor_property('DamageNoticeSerial')==previous+1
            fb_gs.apply_damage(fb_hostage,13.2,None,s['enemy'],None)
            assert fb_hostage.get_editor_property('DamageNoticeSerial')==previous+1
            s.update(stage='capture',at=time.monotonic())
        elif s['stage']=='capture' and age>.05:
            assert fb_hud.get_editor_property('HostageHurtUntil')>fb_gs.get_real_time_seconds(fb_world)
            s['results'].update(hostage_warning=True,restore_does_not_increment_hit_notice=True,invulnerable_hit_does_not_repeat_notice=True)
            # Refresh an enemy impact for a capture of both distinct signals.
            fb_damage(s['enemy'],15)
            s['busy']=True
            unreal.SystemLibrary.execute_console_command(fb_world,'Shot filename="'+os.path.join(fb_root,'Intermediate/inspect/combat-feedback.png')+'"')
            s['busy']=False;s.update(stage='finish',at=time.monotonic())
        elif s['stage']=='finish' and age>1:
            unreal.unregister_slate_post_tick_callback(s['handle']);s['enemy'].destroy_actor()
            with open(os.path.join(fb_root,'Intermediate/inspect/combat_feedback.json'),'w') as f:json.dump({'passed':True,'isolated_callbacks_not_physical_input':True,**s['results']},f,indent=2)
            unreal.log('COMBAT_FEEDBACK_ASSERTIONS_PASSED')
    except Exception:
        unreal.unregister_slate_post_tick_callback(s['handle'])
        if s['enemy']:s['enemy'].destroy_actor()
        with open(os.path.join(fb_root,'Intermediate/inspect/combat_feedback.json'),'w') as f:json.dump({'passed':False,'stage':s['stage'],'error':traceback.format_exc()},f,indent=2)
        unreal.log_error(traceback.format_exc())

fb_state['handle']=unreal.register_slate_post_tick_callback(fb_tick)
