"""Prueba negativa: pared, fuera de alcance y bloqueo por escena/pausa."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller();R='/Game/ThirdPerson/Blueprints/Entrega/'
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
lib=unreal.get_default_object(unreal.SystemLibrary);native=unreal.get_default_object(gs)
def field(obj,key,value):lib.call_method(('SetBool' if isinstance(value,bool) else 'SetInt' if isinstance(value,int) else 'SetDouble')+'PropertyByName',(obj,key,value))
def spawn(cls,loc):
 tr=unreal.Transform(location=unreal.Vector(*loc));a=native.call_method('BeginDeferredActorSpawnFromClass',(w,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));native.call_method('FinishSpawningActor',(a,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));return a
p.set_actor_location(unreal.Vector(0,-1800,100),False,True);pc.set_control_rotation(unreal.Rotator(yaw=-90));field(p,'CamaraPrimera',True);p.get_editor_property('FPC').activate();p.get_editor_property('TPC').deactivate()
enemy=spawn(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C'),(0,-2250,100));enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Fixture de oclusión')
health=enemy.get_editor_property('BPC_E_Health')
wall=spawn(unreal.StaticMeshActor.static_class(),(0,-2050,150));wall.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE);wall.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));wall.static_mesh_component.set_collision_profile_name('BlockAll');wall.set_actor_scale3d(unreal.Vector(2,.3,3))
s={'stage':0,'at':gs.get_real_time_seconds(w),'handle':None,'checks':[]}
def tick(dt,state=s):
 try:
  now=gs.get_real_time_seconds(w)
  if now-state['at']<.4:return
  stage=state['stage']
  if stage==0:field(extra,'Cargas',3);field(extra,'LastPulseAt',-10.0);extra.call_method('DispararPulso')
  elif stage==1:
   assert extra.get_editor_property('Cargas')==2 and health.get_editor_property('E_Health')==100
   state['checks'].append('pared_bloquea_dano_y_disparo_consume_una_carga');wall.destroy_actor();enemy.set_actor_location(unreal.Vector(0,-2800,100),False,True);field(extra,'LastPulseAt',-10.0);extra.call_method('DispararPulso')
  elif stage==2:
   assert extra.get_editor_property('Cargas')==1 and health.get_editor_property('E_Health')==100
   state['checks'].append('objetivo_a_diez_metros_no_recibe_dano');field(extra,'Cargas',0);field(extra,'LastPulseAt',-10.0);extra.call_method('DispararPulso');assert extra.get_editor_property('Cargas')==0 and extra.get_editor_property('LastPulseAt')==-10
   state['checks'].append('sin_municion_no_dispara');cinema.call_method('StartIntro')
  elif stage==3:
   assert pc.is_move_input_ignored();field(extra,'InventoryOpen',False);extra.call_method('AlternarInventario');extra.call_method('DispararPulso');assert not extra.get_editor_property('InventoryOpen')
   state['checks'].append('escena_bloquea_acciones_complementarias');cinema.call_method('FinishCinema')
  elif stage==4:
   ui=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliveryInterface.BP_DeliveryInterface_C'));ui.call_method('OpenPause');assert gs.is_game_paused(w);field(extra,'InventoryOpen',False);extra.call_method('AlternarInventario');assert not extra.get_editor_property('InventoryOpen');ui.call_method('ClosePause')
   state['checks'].append('pausa_bloquea_inventario_y_recupera_control');enemy.destroy_actor();unreal.unregister_slate_post_tick_callback(state['handle'])
   with open(os.path.join(unreal.Paths.project_dir(),'docs/validation/pulso-controles-negativos.json'),'w',encoding='utf-8') as f:json.dump({'passed':True,'method':'PIE; pared/enemigo/cámara/munición preparados para controles negativos','checks':state['checks']},f,ensure_ascii=False,indent=2)
   unreal.log('PULSE_GUARDS_PASSED');return
  state['stage']+=1;state['at']=now
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle']);gs.set_game_paused(w,False)
  with open(os.path.join(unreal.Paths.project_dir(),'docs/validation/pulso-controles-negativos.json'),'w') as f:json.dump({'passed':False,'stage':state['stage'],'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
