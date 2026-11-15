"""PIE integration: progressive text, reveal/dismiss, escort prompts, real-time hide and ambient audio."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);hud=p.get_controller().get_hud()
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
assert not bb.get_value_as_bool('bRescued'),'Run in fresh PIE'
assert not unreal.GameplayStatics.get_all_actors_of_class(w,unreal.TextRenderActor)
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
lib.call_method('SetIntPropertyByName',(hud,'LastDialog',-1))
s={'stage':'start','at':unreal.GameplayStatics.get_real_time_seconds(w),'handle':None,'result':{'no_world_text':True}}
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
def verify_dialogue_tick(delta,world=w,player=p,ui=hud,hostage=h,board=bb,state=s,root=project):
    try:
        now=unreal.GameplayStatics.get_real_time_seconds(world);age=now-state['at']
        if state['stage']=='start' and age>=.35:
            length=len(ui.get_editor_property('FullText'));count=ui.get_editor_property('VisibleCharacters')
            assert ui.get_editor_property('CurrentDialog')==2 and 0<count<length,(count,length,ui.get_editor_property('CurrentDialog'))
            assert ui.get_editor_property('DialogueVisible')
            assert ui.get_editor_property('AmbientAudio').is_playing()
            assert not unreal.GameplayStatics.is_game_paused(world)
            ui.call_method('InpActEvt_Enter_K2Node_InputKeyEvent_0',(unreal.Key(),))
            state.update(stage='revealed',at=now);state['result'].update(progressive_text=True,ambient_playing=True,does_not_pause=True)
        elif state['stage']=='revealed' and age>=.1:
            assert ui.get_editor_property('VisibleText')==ui.get_editor_property('FullText')
            ui.call_method('InpActEvt_Enter_K2Node_InputKeyEvent_0',(unreal.Key(),));state.update(stage='dismissed',at=now);state['result']['enter_reveals']=True
        elif state['stage']=='dismissed' and age>=.1:
            assert not ui.get_editor_property('DialogueVisible')
            hostage.call_method('Interactuar',());state.update(stage='following',at=now);state['result']['enter_dismisses']=True
        elif state['stage']=='following' and age>=.25:
            assert board.get_value_as_bool('bAccompanying') and ui.get_editor_property('CurrentDialog')==3
            assert ui.get_editor_property('DialogueVisible')
            assert ui.get_editor_property('LastBeepAt')>ui.get_editor_property('DialogStarted')
            state.update(stage='auto_hide',at=now);state['result'].update(rescue_changes_dialogue=True,type_audio_ticks=True)
        elif state['stage']=='auto_hide' and age>=8:
            assert not ui.get_editor_property('DialogueVisible'),'Nonessential dialogue did not auto hide'
            board.set_value_as_bool('bAccompanying',False);board.set_value_as_bool('bWaiting',True);board.set_value_as_int('Estado',3)
            state.update(stage='resume',at=now);state['result']['auto_hides']=True
        elif state['stage']=='resume' and age>=.25:
            assert ui.get_editor_property('CurrentDialog')==6
            assert 'Volver a seguir' in ui.get_editor_property('ActionHint')
            state['result'].update(manual_resume_prompt=True,passed=True)
            unreal.unregister_slate_post_tick_callback(state['handle'])
            with open(os.path.join(root,'Intermediate/inspect/dialogue_assertions.json'),'w',encoding='utf-8') as f:json.dump(state['result'],f,indent=2)
            unreal.log('DIALOGUE_ASSERTIONS_PASSED '+json.dumps(state['result']));return
        assert age<12,'Dialogue test timed out: '+state['stage']
    except Exception:
        unreal.unregister_slate_post_tick_callback(state['handle'])
        with open(os.path.join(root,'Intermediate/inspect/dialogue_assertions.json'),'w',encoding='utf-8') as f:json.dump({'passed':False,'stage':state['stage'],'error':traceback.format_exc()},f,indent=2)
        unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(verify_dialogue_tick)
unreal.log('DIALOGUE_ASSERTIONS_STARTED')
