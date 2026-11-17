"""Prueba PIE aislada: recogida, fabricación, pausa y guardado en proceso."""
import unreal,os,time,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;pc=gs.get_player_controller(w,0);p=gs.get_player_character(w,0);R='/Game/ThirdPerson/Blueprints/Entrega/'
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'));manager=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'));robot=extra.get_editor_property('Tecnico')
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
lib=unreal.get_default_object(unreal.SystemLibrary)
def setp(obj,key,val,kind=None):lib.call_method('Set'+(kind or ('Bool' if isinstance(val,bool) else 'Int' if isinstance(val,int) else 'Double'))+'PropertyByName',(obj,key,val))
def prop(key):return extra.get_editor_property(key)
for k in ['Botiquines','Cargas','Creditos']:setp(extra,k,0)
setp(extra,'Recogido1',False);setp(extra,'bFabricating',False);setp(extra,'RobotEnergy',0);setp(extra,'FabricationProgress',0.)
p.set_actor_location(prop('Suministro1').get_actor_location()+unreal.Vector(0,0,90),False,True)
folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/robot-cielo-inventario');os.makedirs(folder,exist_ok=True)
s={'stage':0,'at':time.monotonic(),'handle':None,'checks':[]}
def tick(dt,state=s):
 try:
  age=time.monotonic()-state['at'];stage=state['stage']
  if age<.35:return
  if stage==0:
   assert [prop(k) for k in ['Botiquines','Cargas','Creditos']]==[1,3,3] and prop('Recogido1')
   state['checks'].append('caja_real_recogida_una_vez_1_3_3')
   assert robot.skeletal_mesh_component.get_skeletal_mesh_asset() is None
   assert len(robot.get_components_by_class(unreal.StaticMeshComponent))==3
   state['checks'].append('robot_original_en_tres_piezas_sin_modelo_humano')
   p.set_actor_location(robot.get_actor_location()+unreal.Vector(150,100,95),False,True);extra.call_method('HablarConTecnico')
  elif stage==1:
   assert 'robot' in prop('DialogText') and prop('DialogUntil')>gs.get_time_seconds(w)
   assert pc.get_hud().get_editor_property('CurrentDialog')==34
   state['head']=str(robot.get_editor_property('CabezaRobot').relative_rotation)
   extra.call_method('HablarConTecnico')
   assert prop('Creditos')==0 and prop('RobotEnergy')==3 and prop('bFabricating') and prop('Botiquines')==1
   extra.call_method('HablarConTecnico');assert prop('Creditos')==0 and prop('Botiquines')==1
   state['checks'].append('dialogo_explica_anclaje_y_conversion_tres_creditos_una_orden')
  elif stage==2:
   assert 0<prop('FabricationProgress')<3 and prop('Botiquines')==1
   assert robot.get_editor_property('LuzConversion').intensity==45
   assert str(robot.get_editor_property('CabezaRobot').relative_rotation)!=state['head']
   manager.call_method('SaveCheckpoint');assert manager.get_editor_property('bSaveSucceeded')
   data=gs.load_game_from_slot('TimeOut_Delivery_v1',0);assert data.get_editor_property('bFabricating') and data.get_editor_property('RobotEnergy')==3 and 0<data.get_editor_property('FabricationProgress')<3
   state['saved_progress']=data.get_editor_property('FabricationProgress');state['saved_clock']=data.get_editor_property('WorldSeconds');state['clock']=prop('WorldSeconds');state['progress']=prop('FabricationProgress');state['robot_time']=robot.get_editor_property('TiempoVisual')
   gs.set_game_paused(w,True)
  elif stage==3:
   if age<1:return
   assert prop('WorldSeconds')==state['clock'] and prop('FabricationProgress')==state['progress'] and robot.get_editor_property('TiempoVisual')==state['robot_time']
   gs.set_game_paused(w,False);state['checks'].append('pausa_real_detiene_cielo_fabricacion_y_animacion')
   setp(extra,'bFabricating',False);setp(extra,'RobotEnergy',0);setp(extra,'FabricationProgress',0.);manager.call_method('RestoreCheckpoint')
   assert prop('bFabricating') and prop('RobotEnergy')==3 and abs(prop('FabricationProgress')-state['saved_progress'])<.001
   state['checks'].append('checkpoint_en_proceso_restaura_energia_progreso_y_fase_sin_duplicar')
  elif stage==4:
   if prop('bFabricating'):
    assert prop('Botiquines')==1
    if age>5:raise AssertionError('La fabricación no termina')
    return
   assert prop('Botiquines')==2 and prop('RobotEnergy')==0 and prop('FabricationProgress')==0 and prop('Creditos')==0
   state['checks'].append('finalizacion_despues_de_tres_segundos_un_solo_botiquin')
   extra.call_method('HablarConTecnico');assert not prop('bFabricating') and prop('Creditos')==0 and prop('Botiquines')==2
   state['checks'].append('sin_saldo_no_inicia_no_negativos_no_recompensa_extra')
  elif stage==5:
   assert prop('Botiquines')==2
   # Compatibilidad aditiva: una revisión anterior carece de energía en proceso.
   manager.call_method('SaveCheckpoint');data=gs.load_game_from_slot('TimeOut_Delivery_v1',0)
   setp(data,'ExtrasRevision',1);setp(data,'bFabricating',False);setp(data,'RobotEnergy',0);setp(data,'FabricationProgress',0.)
   assert gs.save_game_to_slot(data,'TimeOut_Delivery_v1',0)
   manager.call_method('RestoreCheckpoint');assert not prop('bFabricating') and prop('RobotEnergy')==0 and prop('Botiquines')==2 and prop('Cargas')==3
   state['checks'].append('guardado_revision_anterior_conserva_inventario_sin_trabajo_fantasma')
  elif stage==6:
   assert prop('Botiquines')==2 and robot.get_editor_property('LuzConversion').intensity==3
   unreal.unregister_slate_post_tick_callback(state['handle'])
   result={'passed':True,'method':'PIE en tiempo real. Posición y saldos iniciales preparados; recogida, diálogo, conversión y SaveCheckpoint/RestoreCheckpoint reales. No recorrido natural ni mando físico.','checks':state['checks'],'fabrication_seconds':3,'pause_wall_seconds':1,'saved_progress':state['saved_progress'],'saved_world_seconds':state['saved_clock']}
   with open(os.path.join(folder,'energia-runtime.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
   unreal.log('ROBOT_ENERGY_RUNTIME_PASSED');return
  state['stage']+=1;state['at']=time.monotonic()
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle']);gs.set_game_paused(w,False)
  with open(os.path.join(folder,'energia-runtime.json'),'w',encoding='utf-8') as f:json.dump({'passed':False,'stage':state['stage'],'checks':state['checks'],'error':traceback.format_exc()},f,ensure_ascii=False,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
