import unreal,os,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics
c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
m=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
assert c.get_editor_property('bInitialized')
assert not c.get_editor_property('bShouldIntro') and not c.get_editor_property('bActive')
assert not c.get_editor_property('SequencePlayer')
assert m.get_editor_property('bInitialized') and m.get_editor_property('bHasCheckpoint')
pc=gs.get_player_controller(w,0);assert not pc.is_move_input_ignored() and not pc.is_look_input_ignored()
result={'passed':True,'continue_omits_intro':True,'checkpoint_restored':m.get_editor_property('StatusText'),'input_restored':True}
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/cinematics/continue.json'),'w',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
unreal.log('CINEMA_CONTINUE_PASSED '+json.dumps(result,ensure_ascii=False))
unreal.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/cinematics/continue-gameplay.png'))
