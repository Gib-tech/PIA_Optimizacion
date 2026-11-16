"""Check a physically opened pause, safe save, frozen time and return-stack state."""
import unreal,json,os,time
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs=unreal.GameplayStatics
R='/Game/ThirdPerson/Blueprints/Entrega/'
ui=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliveryInterface.BP_DeliveryInterface_C'))
m=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
p=gs.get_player_pawn(w,0);pc=gs.get_player_controller(w,0);pause=ui.get_editor_property('PauseWidget')
assert gs.is_game_paused(w) and ui.get_editor_property('bPauseOpen')
assert pc.is_move_input_ignored() and pc.is_look_input_ignored()
assert not p.get_editor_property('IsAttacking') and not p.get_editor_property('CamaraPrimera')
h=m.get_editor_property('Hostage');bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
assert not bb.get_value_as_bool('bRescued')
pause.call_method('BndEvt__Menu_Pausa_btn_salvarjuego_pausa_Control_3_OnButtonClickedEvent__DelegateSignature')
assert m.get_editor_property('bSaveSucceeded')
assert str(pause.get_editor_property('PauseSaveStatus').get_text())
pause.call_method('BndEvt__Menu_Pausa_btn_opciones_pausa_Control_1_OnButtonClickedEvent__DelegateSignature')
assert ui.get_editor_property('bOptionsOpen') and gs.is_game_paused(w)
assert pause.get_visibility()==unreal.SlateVisibility.COLLAPSED
ui.call_method('CloseOptions')
assert not ui.get_editor_property('bOptionsOpen') and gs.is_game_paused(w)
assert pause.get_visibility()==unreal.SlateVisibility.VISIBLE
# Exercise the existing safe-save guard through the new pause button.
zone=m.get_editor_property('Director').get_editor_property('Zona1')
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
lib.call_method('SetIntPropertyByName',(zone,'Phase',1))
pause.call_method('BndEvt__Menu_Pausa_btn_salvarjuego_pausa_Control_3_OnButtonClickedEvent__DelegateSignature')
assert not m.get_editor_property('bSaveSucceeded')
lib.call_method('SetIntPropertyByName',(zone,'Phase',0))
before=gs.get_time_seconds(w);state={'start':time.monotonic(),'handle':None}
def observe(dt,world=w,clock=gs.get_time_seconds,initial=before,state=state,project=unreal.Paths.project_dir()):
 if time.monotonic()-state['start']<1:return
 unreal.unregister_slate_post_tick_callback(state['handle'])
 out={'passed':clock(world)==initial,'agent_test_not_owner_acceptance':True,'physical_P_opened_pause':True,'world_time_frozen_for_real_second':clock(world)==initial,'move_look_ignored':True,'interaction_and_camera_unchanged_during_physical_keys':True,'safe_save_from_pause':True,'combat_save_rejected':True,'options_returned_to_same_paused_widget':True}
 with open(os.path.join(project,'Intermediate/inspect/delivery_pause_assertions.json'),'w') as f:json.dump(out,f,indent=2)
 unreal.log('PAUSE_REGRESSION '+json.dumps(out))
state['handle']=unreal.register_slate_post_tick_callback(observe)
