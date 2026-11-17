"""Fixtures de integración: inventario, dinero, curación, pulso, diálogo y reloj."""
import unreal,json,os,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;R='/Game/ThirdPerson/Blueprints/Entrega/'
p=gs.get_player_character(w,0);pc=gs.get_player_controller(w,0)
extras=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
manager=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());out=os.path.join(root,'docs/validation/complementos-runtime.json')
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
def setp(obj,name,value,kind='Int'):lib.call_method('Set'+kind+'PropertyByName',(obj,name,value))
def prop(obj,name):return obj.get_editor_property(name)
s={'stage':0,'at':gs.get_time_seconds(w),'handle':None,'checks':[],'enemy':None}
def observe(dt,state=s):
 try:
  now=gs.get_time_seconds(w);age=now-state['at'];stage=state['stage']
  if stage!=7 and age<.35:return
  if stage==0:
   assert prop(extras,'bInitialized') and prop(extras,'Sun') and prop(extras,'Tecnico')
   item=prop(extras,'Suministro1');p.set_actor_location(item.get_actor_location()+unreal.Vector(0,0,90),False,True)
  elif stage==1:
   assert prop(extras,'Recogido1') and prop(extras,'Botiquines')==1 and prop(extras,'Cargas')==3 and prop(extras,'Creditos')==3
   state['checks'].append('recogida_unica_y_tres_recursos');extras.call_method('AlternarInventario')
   setp(prop(p,'BPC_Health'),'Health',70.,'Double');extras.call_method('UsarBotiquin')
  elif stage==2:
   assert prop(prop(p,'BPC_Health'),'Health')==100 and prop(extras,'Botiquines')==0
   extras.call_method('UsarBotiquin');assert prop(prop(p,'BPC_Health'),'Health')==100 and prop(extras,'Botiquines')==0
   assert prop(extras,'InventoryOpen');state['checks'].append('inventario_visible_curacion_limitada_sin_duplicacion')
   p.set_actor_location(prop(extras,'Tecnico').get_actor_location()+unreal.Vector(0,100,90),False,True);extras.call_method('HablarConTecnico')
  elif stage==3:
   assert prop(extras,'DialogUntil')>now and 'BRUNO' in prop(extras,'DialogSpeaker')
   assert pc.get_hud().get_editor_property('CurrentDialog')==34
   extras.call_method('HablarConTecnico')
  elif stage==4:
   assert prop(extras,'Creditos')==0 and prop(extras,'Botiquines')==1
   extras.call_method('HablarConTecnico');assert prop(extras,'Botiquines')==1
   state['checks'].append('segundo_npc_dialogo_y_compra_sin_saldo_negativo')
   # Objetivo aislado para comprobar la traza, sin alterar los encuentros.
   cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
   p.set_actor_location(unreal.Vector(0,-1800,100),False,True)
   loc=unreal.Vector(0,-2250,100)
   spawn=unreal.get_default_object(unreal.GameplayStatics.static_class());tr=unreal.Transform(location=loc)
   state['enemy']=spawn.call_method('BeginDeferredActorSpawnFromClass',(w,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
   spawn.call_method('FinishSpawningActor',(state['enemy'],tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
   enemy=state['enemy'];enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Fixture de pulso')
   enemy.character_movement.disable_movement();pc.set_control_rotation(unreal.Rotator(yaw=-90,pitch=0))
   p.get_editor_property('FPC').activate();p.get_editor_property('TPC').deactivate();setp(p,'CamaraPrimera',True,'Bool')
   state['before']=prop(prop(enemy,'BPC_E_Health'),'E_Health')
  elif stage==5:extras.call_method('DispararPulso')
  elif stage==6:
   assert prop(extras,'Cargas')==2
   assert prop(prop(state['enemy'],'BPC_E_Health'),'E_Health')==state['before']-20
   extras.call_method('DispararPulso');assert prop(extras,'Cargas')==2
   state['checks'].append('pulso_gasta_municion_y_dana_20_con_cooldown')
   state['enemy'].destroy_actor();state['clock']=prop(extras,'WorldSeconds');state['sun']=prop(extras,'Sun').get_actor_rotation().pitch
   gs.set_game_paused(w,True);state['real_at']=gs.get_real_time_seconds(w)
  elif stage==7:
   if gs.get_real_time_seconds(w)-state['real_at']<.5:return
   assert prop(extras,'WorldSeconds')==state['clock'];gs.set_game_paused(w,False)
   state['checks'].append('pausa_detiene_ciclo_horario')
  elif stage==8:
   assert prop(extras,'WorldSeconds')>state['clock'] and prop(extras,'Sun').get_actor_rotation().pitch!=state['sun']
   manager.call_method('SaveCheckpoint')
  elif stage==9:
   data=gs.load_game_from_slot('TimeOut_Delivery_v1',0);assert data
   for k in ['Botiquines','Cargas','Creditos','Recogido1']:assert prop(data,k)==prop(extras,k),(k,prop(data,k),prop(extras,k))
   assert prop(data,'FirstPerson') and prop(data,'ExtrasRevision')==1
   state['saved']={k:prop(data,k) for k in ['Botiquines','Cargas','Creditos','WorldSeconds','Recogido1']}
   setp(extras,'Cargas',0);setp(extras,'Botiquines',0);manager.call_method('RestoreCheckpoint')
  elif stage==10:
   assert prop(extras,'Cargas')==state['saved']['Cargas'] and prop(extras,'Botiquines')==state['saved']['Botiquines']
   assert prop(extras,'Recogido1') and prop(prop(extras,'Suministro1'),'hidden')
   state['checks'].append('checkpoint_restaura_inventario_municion_dinero_recogida_y_camara')
   unreal.unregister_slate_post_tick_callback(state['handle'])
   with open(out,'w',encoding='utf-8') as f:json.dump({'passed':True,'method':'PIE, fixtures con posiciones y salud preparadas; no partida natural','checks':state['checks'],'saved':state['saved']},f,ensure_ascii=False,indent=2)
   unreal.log('RUBRIC_RUNTIME_PASSED');return
  state['stage']+=1;state['at']=now
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  if gs.is_game_paused(w):gs.set_game_paused(w,False)
  with open(out,'w') as f:json.dump({'passed':False,'stage':state['stage'],'checks':state['checks'],'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
