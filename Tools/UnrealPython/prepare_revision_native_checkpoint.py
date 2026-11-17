"""Fixture de paquete: recoger caja real y guardar junto a Bruno, sin combate."""
import unreal,os,shutil,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller();R='/Game/ThirdPerson/Blueprints/Entrega/'
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'));m=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if c.get_editor_property('bActive'):c.call_method('FinishCinema')
p.set_actor_location(extra.get_editor_property('Suministro1').get_actor_location()+unreal.Vector(0,0,90),False,True)
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());s={'stage':0,'at':gs.get_time_seconds(w),'handle':None}
def tick(dt,state=s):
 try:
  now=gs.get_time_seconds(w)
  if now-state['at']<.5:return
  if state['stage']==0:
   assert extra.get_editor_property('Recogido1') and extra.get_editor_property('Botiquines')==1 and extra.get_editor_property('Cargas')==3 and extra.get_editor_property('Creditos')==3
   p.set_actor_location(unreal.Vector(-150,-850,100),False,True);pc.set_control_rotation(unreal.Rotator(pitch=-8,yaw=180))
   sub=unreal.get_default_object(unreal.load_class(None,'/Script/Engine.SubsystemBlueprintLibrary')).call_method('GetLocalPlayerSubSystemFromPlayerController',(pc,unreal.EnhancedInputLocalPlayerSubsystem.static_class()))
   sub.inject_input_vector_for_action(unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_Camera'),unreal.Vector(1,0,0),[],[])
  else:
   assert p.get_editor_property('CamaraPrimera');m.call_method('SaveCheckpoint');assert m.get_editor_property('bSaveSucceeded')
   folder=os.path.join(root,'Intermediate/inspect/revision-native-user/Saved/SaveGames');os.makedirs(folder,exist_ok=True);shutil.copy2(os.path.join(root,'Saved/SaveGames/TimeOut_Delivery_v1.sav'),os.path.join(folder,'TimeOut_Delivery_v1.sav'))
   with open(os.path.join(root,'Intermediate/inspect/revision-native-prepared.json'),'w',encoding='utf-8') as f:json.dump({'fixture_not_natural_playthrough':True,'method':'Posiciones preparadas; recogida real de caja y SaveCheckpoint, cámara por Enhanced Input. Sin enemigos ni edición de salud/daño.','resources':[1,3,3],'first_person':True,'position':[-150,-850]},f,ensure_ascii=False,indent=2)
   unreal.unregister_slate_post_tick_callback(state['handle']);unreal.log('REVISION_NATIVE_CHECKPOINT_READY');return
  state['stage']+=1;state['at']=now
 except Exception:unreal.unregister_slate_post_tick_callback(state['handle']);unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
