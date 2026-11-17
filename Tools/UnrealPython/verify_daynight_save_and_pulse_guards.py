"""Checkpoint solar y negativos del pulso contra un prop real, con fixture declarado."""
import unreal,os,json,time,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;R='/Game/ThirdPerson/Blueprints/Entrega/';p=gs.get_player_character(w,0);pc=p.get_controller()
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'));manager=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
target=next(a for a in gs.get_all_actors_of_class(w,unreal.load_class(None,R+'BP_DestruibleEntrega.BP_DestruibleEntrega_C')) if a.get_editor_property('NombreDestruible')=='Caja')
lib=unreal.get_default_object(unreal.SystemLibrary)
def field(obj,key,value,kind):lib.call_method('Set'+kind+'PropertyByName',(obj,key,value))
def aim(y):
 p.set_actor_location(unreal.Vector(520,y,95),False,True);p.set_actor_rotation(unreal.Rotator(yaw=90),False)
 pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(p.get_editor_property('FPC').get_world_location(),unreal.Vector(520,-900,45)))
field(p,'CamaraPrimera',True,'Bool');p.get_editor_property('TPC').deactivate();p.get_editor_property('FPC').activate()
native=unreal.get_default_object(gs);tr=unreal.Transform(location=unreal.Vector(520,-1110,150))
wall=native.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.StaticMeshActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));native.call_method('FinishSpawningActor',(wall,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
wall.static_mesh_component.set_mobility(unreal.ComponentMobility.MOVABLE);wall.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));wall.static_mesh_component.set_collision_profile_name('BlockAll');wall.set_actor_scale3d(unreal.Vector(3,.3,3))
folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/ciclo-luces-ataques');s={'stage':0,'at':time.monotonic(),'handle':None,'checks':[]}
def finish(error=None):
 unreal.unregister_slate_post_tick_callback(s['handle'])
 if unreal.SystemLibrary.is_valid(wall):wall.destroy_actor()
 with open(os.path.join(folder,'guardado-y-guardas.json'),'w',encoding='utf-8') as f:json.dump({'passed':error is None,'method':'PIE; posición, cámara, munición, hora y pared preparados. Pulso normal, guardado nativo y restauración por SaveManager.','checks':s['checks'],**({'error':error} if error else {})},f,ensure_ascii=False,indent=2)
 unreal.log('DAYNIGHT_SAVE_PULSE_GUARDS '+str(error is None))
def tick(dt):
 try:
  now=time.monotonic()
  if now-s['at']<.5:return
  stage=s['stage']
  if stage==0:
   field(extra,'WorldSeconds',783.,'Double');manager.call_method('SaveCheckpoint');assert manager.get_editor_property('bSaveSucceeded')
   data=gs.load_game_from_slot('TimeOut_Delivery_v1',0);s['clock']=data.get_editor_property('WorldSeconds');assert 782.9<s['clock']<783.2
   field(extra,'WorldSeconds',1.,'Double');manager.call_method('RestoreCheckpoint');assert abs(extra.get_editor_property('WorldSeconds')-s['clock'])<.001
   assert extra.get_editor_property('DayCycleDuration')==1200.;s['checks'].append('checkpoint_nativo_restaura_fase_nocturna_con_periodo_1200')
   aim(-1300);field(extra,'Cargas',3,'Int');field(extra,'LastPulseAt',-10.,'Double')
  elif stage==1:extra.call_method('DispararPulso')
  elif stage==2:
   assert extra.get_editor_property('Cargas')==2 and target.get_editor_property('Health')==50;s['checks'].append('pared_bloquea_prop_y_consume_una_carga');wall.destroy_actor();aim(-2000);field(extra,'LastPulseAt',-10.,'Double')
  elif stage==3:extra.call_method('DispararPulso')
  elif stage==4:
   assert extra.get_editor_property('Cargas')==1 and target.get_editor_property('Health')==50;s['checks'].append('fuera_de_ocho_metros_no_dana');aim(-1300);field(extra,'Cargas',0,'Int');field(extra,'LastPulseAt',-10.,'Double')
  elif stage==5:
   extra.call_method('DispararPulso');assert extra.get_editor_property('Cargas')==0 and extra.get_editor_property('LastPulseAt')==-10.;s['checks'].append('sin_cargas_no_dispara');field(extra,'Cargas',3,'Int')
  elif stage==6:
   extra.call_method('DispararPulso');extra.call_method('DispararPulso');assert extra.get_editor_property('Cargas')==2 and target.get_editor_property('Health')==30;s['checks'].append('un_impacto_20_y_recuperacion_impide_duplicado');finish();return
  s.update(stage=stage+1,at=now)
 except Exception:finish(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
