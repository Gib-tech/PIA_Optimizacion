"""Regresión de pausa/opciones mediante sus delegados, con reloj real."""
import unreal,os,time,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;R='/Game/ThirdPerson/Blueprints/Entrega/'
ui=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliveryInterface.BP_DeliveryInterface_C'));p=gs.get_player_character(w,0);pc=p.get_controller()
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
ui.call_method('OpenPause');assert gs.is_game_paused(w) and pc.is_move_input_ignored() and pc.is_look_input_ignored()
pause=ui.get_editor_property('PauseWidget');pause.call_method('BndEvt__Menu_Pausa_btn_salvarjuego_pausa_Control_3_OnButtonClickedEvent__DelegateSignature')
manager=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'));assert manager.get_editor_property('bSaveSucceeded')
pause.call_method('BndEvt__Menu_Pausa_btn_opciones_pausa_Control_1_OnButtonClickedEvent__DelegateSignature');assert ui.get_editor_property('bOptionsOpen')
state={'at':time.monotonic(),'world':gs.get_time_seconds(w),'clock':extra.get_editor_property('WorldSeconds'),'handle':None}
def tick(dt,s=state):
 if time.monotonic()-s['at']<1:return
 unreal.unregister_slate_post_tick_callback(s['handle'])
 try:
  assert gs.get_time_seconds(w)==s['world'] and extra.get_editor_property('WorldSeconds')==s['clock']
  ui.call_method('CloseOptions');assert gs.is_game_paused(w) and not ui.get_editor_property('bOptionsOpen') and pause.get_visibility()==unreal.SlateVisibility.VISIBLE
  ui.call_method('ClosePause');assert not gs.is_game_paused(w) and not pc.is_move_input_ignored() and not pc.is_look_input_ignored()
  result={'passed':True,'method':'Eventos reales de UMG y reloj real de 1 s. No pulsación física de mando.','world_and_day_cycle_frozen':True,'save_from_pause':True,'options_return_to_same_pause':True,'move_and_look_restored':True}
 except Exception:result={'passed':False,'error':traceback.format_exc()};gs.set_game_paused(w,False)
 with open(os.path.join(unreal.Paths.project_dir(),'docs/validation/pausa-opciones-revision.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
 unreal.log('REVISION_PAUSE_RESULT '+str(result['passed']))
state['handle']=unreal.register_slate_post_tick_callback(tick)
