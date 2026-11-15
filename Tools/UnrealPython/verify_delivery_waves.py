"""PIE assertions for both complete encounters. Teleports and lethal test damage are isolated to PIE."""
import unreal,json,os,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0)
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
director=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
hud=unreal.GameplayStatics.get_player_controller(w,0).get_hud()
b=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
zs=sorted(unreal.GameplayStatics.get_all_actors_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C')),key=lambda a:a.get_actor_label())
assert all(z.get_editor_property('Phase')==0 for z in zs),'Run in a fresh PIE session.'
unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetBoolPropertyByName',(p,'bCanBeDamaged',False))
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
state={'index':0,'stage':'enter','since':unreal.GameplayStatics.get_time_seconds(w),'handle':None,'results':[]}
def verify_waves_tick(delta,world=w,player=p,hostage=h,bb=b,zones=zs,s=state,root=project,mission=director,ui=hud):
    try:
        now=unreal.GameplayStatics.get_time_seconds(world);zone=zones[s['index']];phase=zone.get_editor_property('Phase');wave=zone.get_editor_property('CurrentWave');count=zone.get_editor_property('SpawnedCount')
        if s['stage']=='enter':
            unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetIntPropertyByName',(mission,'Paso',s['index']))
            center=zone.get_actor_location();player.set_actor_location(unreal.Vector(center.x,center.y+600,100),False,True)
            bb.set_value_as_bool('bAccompanying',False);bb.set_value_as_bool('bWaiting',True);bb.set_value_as_bool('bMustFlee',False)
            s.update(stage='alone',since=now)
        elif s['stage']=='alone' and now-s['since']>1:
            assert count==0 and phase==0,'Entering alone spawned enemies'
            assert ui.get_editor_property('CurrentDialog')==9,ui.get_editor_property('CurrentDialog')
            hostage.set_actor_location(player.get_actor_location()+unreal.Vector(150,150,0),False,True)
            for key,value in [('bWaiting',False),('bMustFlee',False),('bRescued',True),('bAccompanying',True)]:bb.set_value_as_bool(key,value)
            bb.set_value_as_int('Estado',1);s.update(stage='first',since=now)
        elif s['stage'] in ['first','second'] and phase==1:
            expected=1 if s['stage']=='first' else 2
            assert wave==expected and count==expected*2,(wave,count,expected)
            assert zone.get_editor_property('Blocker').get_actor_enable_collision()
            enemies=zone.get_editor_property('EncounterEnemies');assert len(enemies)==2
            expected_class='BP_BaseEnemy_C' if s['index']==0 else 'BP_ChargerEnemy_C'
            assert all(e.get_class().get_name()==expected_class for e in enemies)
            if expected==2:
                interval=now-s['intermission_at'];assert 2.9<=interval<=3.7,interval
                s['interval']=interval
            for e in enemies:
                health=next(c for c in e.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_E_Health_C')
                health.call_method('E_Decrease_Health',(100.0,))
                assert e.get_editor_property('bIsDead') and not e.get_actor_enable_collision()
                assert not e.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).is_running()
            s.update(stage='intermission' if expected==1 else 'clearing',since=now)
        elif s['stage']=='intermission' and phase==2:
            assert zone.get_editor_property('LivingCount')==0
            assert zone.get_editor_property('Blocker').get_actor_enable_collision()
            s.update(stage='second',since=now,intermission_at=now)
        elif s['stage']=='clearing' and phase==3:
            assert zone.get_editor_property('bCleared') and not zone.get_editor_property('Blocker').get_actor_enable_collision()
            assert count==4 and wave==2
            s['results'].append({'zone':zone.get_actor_label(),'enter_alone':0,'waves':2,'total_enemies':4,'intermission_seconds':round(s['interval'],3),'death_stops_tree':True,'gate_opens':True})
            s.update(stage='reentry',since=now)
            player.set_actor_location(zone.get_actor_location()+unreal.Vector(0,1500,0),False,True)
        elif s['stage']=='reentry' and now-s['since']>.4:
            player.set_actor_location(zone.get_actor_location()+unreal.Vector(0,500,0),False,True)
            s.update(stage='check_once',since=now)
        elif s['stage']=='check_once' and now-s['since']>.5:
            assert count==4 and phase==3,'Completed zone respawned'
            assert ui.get_editor_property('CurrentDialog')==15+s['index'],ui.get_editor_property('CurrentDialog')
            s['results'][-1]['dialogue_prompts_updated']=True
            s['results'][-1]['reentry_respawn']=0
            if s['index']==0:s.update(index=1,stage='enter',since=now)
            else:
                unreal.unregister_slate_post_tick_callback(s['handle'])
                with open(os.path.join(root,'Intermediate/inspect/wave_assertions.json'),'w') as f:json.dump({'passed':True,'zones':s['results']},f,indent=2)
                unreal.log('DELIVERY_WAVE_ASSERTIONS_PASSED '+json.dumps(s['results']));return
        assert now-s['since']<12,'Wave test timed out at '+s['stage']
    except Exception:
        unreal.unregister_slate_post_tick_callback(s['handle'])
        with open(os.path.join(root,'Intermediate/inspect/wave_assertions.json'),'w') as f:json.dump({'passed':False,'stage':s['stage'],'error':traceback.format_exc()},f,indent=2)
        unreal.log_error(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(verify_waves_tick)
unreal.log('DELIVERY_WAVE_ASSERTIONS_STARTED')
