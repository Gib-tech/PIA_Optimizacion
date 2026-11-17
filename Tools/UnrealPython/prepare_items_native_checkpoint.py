"""Prueba el reenvío al rehén y prepara un save aislado para teclas reales."""
import unreal,os,time,shutil,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller();R='/Game/ThirdPerson/Blueprints/Entrega/'
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'));manager=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
host=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'));bb=host.get_controller().get_component_by_class(unreal.BlackboardComponent);lib=unreal.get_default_object(unreal.SystemLibrary)
def field(obj,key,val):lib.call_method('Set'+('Bool' if isinstance(val,bool) else 'Int')+'PropertyByName',(obj,key,val))
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());folder=os.path.join(root,'docs/validation/items-colisiones');original=host.get_actor_location()
bb.set_value_as_bool('bRescued',False);p.set_actor_location(original+unreal.Vector(130,0,0),False,True);pc.set_control_rotation(unreal.Rotator(yaw=0))
s={'stage':0,'at':time.monotonic(),'handle':None}
def tick(dt,state=s):
 try:
  if time.monotonic()-state['at']<.6:return
  if state['stage']==0:
   assert not bb.get_value_as_bool('bRescued');extra.call_method('HablarConTecnico');assert bb.get_value_as_bool('bRescued') and bb.get_value_as_bool('bAccompanying')
   for key in ['bRescued','bAccompanying','bWaiting']:bb.set_value_as_bool(key,False)
   host.set_actor_location(original,False,True)
   for key,val in [('Botiquines',1),('Cargas',3),('Creditos',3)]:field(extra,key,val)
   for i in range(1,4):field(extra,'MesaRecogido'+str(i),False)
   p.set_actor_location(unreal.Vector(-563,-740,95),False,True);p.set_actor_rotation(unreal.Rotator(yaw=-90),False)
   field(p,'CamaraPrimera',True);p.get_editor_property('TPC').deactivate();p.get_editor_property('FPC').activate()
   health=p.get_editor_property('BPC_Health');health.call_method('Increase_Health',(100.,));gs.apply_damage(p,40,pc,None,None)
  elif state['stage']==1:
   center,_,_=unreal.SystemLibrary.get_component_bounds(extra.get_editor_property('ItemMesa1').static_mesh_component);pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(p.get_editor_property('FPC').get_world_location(),center))
  else:
   assert extra.get_editor_property('ObjetoEnMira')==1
   assert p.get_editor_property('BPC_Health').get_editor_property('Health')==60
   manager.call_method('SaveCheckpoint');assert manager.get_editor_property('bSaveSucceeded')
   target=os.path.join(root,'Intermediate/inspect/items-native-user/Saved/SaveGames');os.makedirs(target,exist_ok=True);shutil.copy2(os.path.join(root,'Saved/SaveGames/TimeOut_Delivery_v1.sav'),os.path.join(target,'TimeOut_Delivery_v1.sav'))
   result={'passed':True,'hostage_fallback_rescues':True,'fixture_not_natural_playthrough':True,'health':60,'resources':[1,3,3],'mesa_collected':[False]*3,'first_person':True,'native_user_dir':'Intermediate/inspect/items-native-user'}
   with open(os.path.join(folder,'preparacion-paquete.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
   unreal.unregister_slate_post_tick_callback(state['handle']);unreal.log('ITEMS_NATIVE_FIXTURE_READY');return
  state['stage']+=1;state['at']=time.monotonic()
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle']);unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
