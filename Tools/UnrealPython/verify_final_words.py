"""Real encounter/death event integration with prepared PIE state, not a playthrough."""
import unreal,os,json,traceback
def main():
    gs=unreal.GameplayStatics;w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
    R='/Game/ThirdPerson/Blueprints/Entrega/';E='/Game/ThirdPerson/Blueprints/EnemigoIA/'
    find=lambda path:gs.get_actor_of_class(w,unreal.load_class(None,path))
    c=find('/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C')
    d=find(R+'BP_DirectorEntrega.BP_DirectorEntrega_C');m=find(R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C')
    p=gs.get_player_character(w,0);pc=gs.get_player_controller(w,0)
    h=find('/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C');z=d.get_editor_property('Zona3')
    bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
    sys=unreal.get_default_object(unreal.SystemLibrary)
    def put(o,k,v):sys.call_method('Set'+('Bool' if isinstance(v,bool) else 'Int' if isinstance(v,int) else 'Double')+'PropertyByName',(o,k,v))
    def prop(o,k):return o.get_editor_property(k)
    def kill(enemy):prop(enemy,'BPC_E_Health').call_method('E_Decrease_Health',(1000.0,))
    def enemies():return list(prop(z,'EncounterEnemies'))
    out=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/final-words')
    s={'stage':0,'since':gs.get_time_seconds(w),'handle':None,'passed':False,'checks':[],'prepared_state_not_natural_playthrough':True,'orders':[]}
    def finish(error=None):
        unreal.unregister_slate_post_tick_callback(s['handle']);s['passed']=error is None
        if error:s['error']=error
        with open(os.path.join(out,'integration.json'),'w',encoding='utf-8') as f:json.dump({k:v for k,v in s.items() if k not in ['handle','speaker']},f,indent=2,ensure_ascii=False)
        unreal.log('FINAL_WORDS_FIXTURE_COMPLETE '+str(s.get('passed'))+' '+str(error))
    def advance(stage):s['stage']=stage;s['since']=gs.get_time_seconds(w)
    def shot(name):unreal.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(out,name+'.png'))
    def run(dt):
        try:
            now=gs.get_time_seconds(w);age=now-s['since'];stage=s['stage']
            if stage==0:
                if not prop(c,'bInitialized'):return
                if prop(c,'bActive'):c.call_method('FinishCinema')
                put(p,'bCanBeDamaged',False);put(h,'bCanBeDamaged',False)
                p.set_actor_location(unreal.Vector(0,-7450,100),False,True)
                h.set_actor_location(unreal.Vector(0,-7050,100),False,True)
                assert not prop(d,'bOrderRevealed')
                advance(1)
            elif stage==1:
                if age<.5:return
                assert prop(z,'SpawnedCount')==0,'Encounter started without rescue'
                s['checks'].append('no_spawn_without_escort')
                bb.set_value_as_bool('bRescued',True);bb.set_value_as_bool('bAccompanying',True)
                advance(2)
            elif stage==2:
                if age<.5:return
                assert prop(z,'SpawnedCount')==0,'Encounter ignored previous zone prerequisite'
                s['checks'].append('no_spawn_before_previous_horde')
                for i in [1,2]:
                    zone=prop(d,'Zona'+str(i));put(zone,'bCleared',True);put(zone,'Phase',3)
                advance(3)
            elif stage==3:
                if prop(z,'SpawnedCount')<2:
                    assert age<5,'Final horde failed to activate';return
                wave=enemies();assert len(wave)==2
                names=sorted(a.get_class().get_name() for a in wave)
                assert names==['BP_BaseEnemy_C','BP_ChargerEnemy_C'],names
                assert all(a.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).is_running() for a in wave)
                assert not prop(d,'bOrderRevealed')
                assert prop(pc.get_hud(),'DisplayedOrder')=='ORDEN: DESCONOCIDO'
                for i in [1,2,3]:assert 'Siguiente' not in prop(d,'Baliza'+str(i)).static_mesh_component.get_material(1).get_name()
                s['checks'].extend(['mixed_wave_two_distinct_running_trees','order_and_next_beacon_hidden'])
                for enemy in wave:kill(enemy)
                assert not prop(c,'bActive'),'First-wave death incorrectly revealed order'
                advance(4)
            elif stage==4:
                if prop(z,'CurrentWave')<2:
                    assert age<7,'Second wave did not spawn';return
                wave=enemies();assert len(wave)==2 and prop(z,'SpawnedCount')==4
                kill(wave[0]);assert not prop(c,'bActive')
                s['checks'].append('only_final_enemy_of_final_wave_starts_scene')
                s['speaker']=wave[1];kill(wave[1])
                assert prop(c,'bActive') and prop(c,'Kind')==4, str({'cinema':prop(c,'bActive'),'kind':prop(c,'Kind'),'pending':prop(wave[1],'bFinalWordsPending'),'dead':prop(wave[1],'bIsDead'),'peers':prop(wave[1],'FinalPeersAlive'),'owner':str(wave[1].get_owner()),'zone_started':prop(z,'bRevelationStarted'),'health':prop(prop(p,'BPC_Health'),'Health'),'hostage':prop(h,'Health')})
                assert prop(wave[1],'bFinalWordsPending') and prop(wave[1],'bIsDead')
                assert prop(m,'bHasCheckpoint')
                from itertools import permutations
                expected=' > '.join('ABC'[i] for i in list(permutations(range(3)))[prop(d,'OrderCode')])
                assert prop(c,'RevealedSequence')==expected
                s['spoken_sequence']=expected;s['clock']=prop(d,'MissionElapsed')
                s['checks'].append('spoken_order_matches_actual_attempt')
                m.call_method('SaveCheckpoint');assert not prop(m,'bSaveSucceeded')
                advance(5)
            elif stage==5:
                if prop(c,'bActive'):
                    assert prop(d,'MissionElapsed')==s['clock'],'Clock advanced during dialogue'
                    assert not prop(d,'bOrderRevealed')
                    assert not h.get_controller().get_component_by_class(unreal.BrainComponent).is_running()
                    if age>=5 and not s.get('photographed'):
                        assert unreal.SystemLibrary.is_valid(s['speaker']),'Speaker disappeared before final words'
                        shot('revelation');s['photographed']=True
                    return
                assert not gs.is_game_paused(w)
                assert prop(d,'bOrderRevealed') and not prop(d,'bNarrativePaused')
                assert not prop(s['speaker'],'bFinalWordsPending')
                assert h.get_controller().get_component_by_class(unreal.BrainComponent).is_running()
                assert pc.get_view_target()==p and not pc.is_move_input_ignored() and not pc.is_look_input_ignored()
                s['checks'].extend(['speaker_held_beyond_original_lifespan','clock_and_checkpoint_suspended','walking_tree_and_camera_restored'])
                # Arrange a safe checkpoint away from beacons after presentation.
                p.set_actor_location(unreal.Vector(0,-6550,100),False,True);h.set_actor_location(unreal.Vector(100,-6650,100),False,True)
                for key in ['bMustFlee','bEnemyNear','bActivateBeacon']:bb.set_value_as_bool(key,False)
                put(h,'bUsingBeacon',False);bb.set_value_as_bool('bAccompanying',True)
                advance(6)
            elif stage==6:
                if age<.8:return
                m.call_method('SaveCheckpoint')
                if not prop(m,'bSaveSucceeded'):
                    assert age<6,'Safe post-cinema checkpoint failed';return
                saved=gs.load_game_from_slot('TimeOut_Delivery_v1',0)
                assert prop(saved,'FinalStandRevision')==1 and prop(saved,'OrderRevealed') and prop(saved,'Zone3Cleared')
                assert prop(saved,'Zone3Phase')==3 and prop(saved,'Zone3Spawned')==4
                s['checks'].append('safe_checkpoint_persists_horde_and_revelation')
                advance(7)
            elif stage==7:
                if age<4.5:return
                assert not prop(pc.get_hud(),'StatusNoticeVisible'),'Checkpoint notice stayed on screen'
                m.call_method('SaveCheckpoint');advance(8)
            elif stage==8:
                if age<.3:return
                assert prop(pc.get_hud(),'StatusNoticeVisible'),'Same-text manual save did not refresh notice'
                s['checks'].append('four_second_notice_hides_and_same_text_save_refreshes')
                # Exercise all six reflected order selections and skip cleanup.
                s['order_index']=0;advance(9)
            elif stage==9:
                from itertools import permutations
                idx=s['order_index'];put(d,'OrderCode',idx)
                speaker=s['speaker']
                if not unreal.SystemLibrary.is_valid(speaker):
                    # Use a dead cue actor for isolated presentation selection.
                    lib=unreal.get_default_object(gs.static_class());tr=unreal.Transform(location=unreal.Vector(0,-7000,100))
                    speaker=lib.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.load_class(None,E+'BP_BaseEnemy.BP_BaseEnemy_C'),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,z,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
                    lib.call_method('FinishSpawningActor',(speaker,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));s['speaker']=speaker
                    put(speaker,'bIsDead',True)
                    speaker.get_controller().get_component_by_class(unreal.BrainComponent).stop_logic('Isolated presentation cue')
                put(speaker,'bFinalWordsPending',True);speaker.set_life_span(0)
                c.call_method('StartRevelation',(speaker,))
                expected=' > '.join('ABC'[i] for i in list(permutations(range(3)))[idx])
                assert prop(c,'RevealedSequence')==expected
                s['orders'].append(expected);advance(10)
            elif stage==10:
                if age<.3:return
                c.call_method('FinishCinema')
                assert not prop(c,'bActive') and prop(d,'bOrderRevealed') and not gs.is_game_paused(w)
                assert not pc.is_move_input_ignored() and not pc.is_look_input_ignored()
                if s['order_index']<5:s['order_index']+=1;advance(9)
                else:
                    s['checks'].append('six_order_variants_and_skip_cleanup')
                    advance(11)
            elif stage==11:
                if age<4.5:return
                assert not prop(pc.get_hud(),'StatusNoticeVisible')
                shot('notice-expired')
                s['checks'].append('notice_expires_after_repeated_dialogue_and_save')
                finish()
        except Exception:finish(traceback.format_exc())
    s['handle']=unreal.register_slate_post_tick_callback(run)
    unreal.log('FINAL_WORDS_FIXTURE_STARTED')
main()
