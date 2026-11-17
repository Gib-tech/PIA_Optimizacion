import unreal,os,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
root=unreal.Paths.project_dir();out=os.path.join(root,'Intermediate/inspect/final-words');mode=open(os.path.join(out,'checkpoint-mode.txt')).read().strip()
gs=unreal.GameplayStatics;R='/Game/ThirdPerson/Blueprints/Entrega/'
find=lambda path:gs.get_actor_of_class(w,unreal.load_class(None,path))
c=find('/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C');d=find(R+'BP_DirectorEntrega.BP_DirectorEntrega_C');m=find(R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C')
p=lambda o,k:o.get_editor_property(k)
assert p(c,'bInitialized') and not p(c,'bActive') and not p(c,'bShouldIntro') and not p(c,'SequencePlayer')
assert p(m,'bInitialized') and p(m,'bHasCheckpoint')
z=p(d,'Zona3');expected=mode!='legacy-unstarted'
assert p(d,'bOrderRevealed')==expected and p(z,'bCleared')==expected
assert p(z,'Phase')==(3 if expected else 0) and p(z,'SpawnedCount')==(4 if expected else 0)
assert p(z,'bRevelationStarted')==expected and not p(d,'bNarrativePaused')
assert not p(z,'EncounterEnemies'),'Continue respawned a completed encounter'
pc=gs.get_player_controller(w,0);assert not pc.is_move_input_ignored() and not pc.is_look_input_ignored()
assert pc.get_view_target()==gs.get_player_character(w,0)
data=gs.load_game_from_slot('TimeOut_Delivery_v1',0);assert p(data,'OrderCode')==p(d,'OrderCode')
result={'passed':True,'case':mode,'prepared_state_not_natural_playthrough':True,'order_revealed':expected,'zone3_phase':p(z,'Phase'),'zone3_spawned':p(z,'SpawnedCount'),'same_order_restored':True,'continue_omits_intro_and_revelation':True,'input_restored':True}
with open(os.path.join(out,mode+'.json'),'w',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
unreal.log('FINAL_WORDS_CHECKPOINT_PASSED '+json.dumps(result))
