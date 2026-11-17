"""Comprueba efecto, interfaz, colisiones, recogida única, pulso y guardado."""
import unreal,os,json,time,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller();R='/Game/ThirdPerson/Blueprints/Entrega/'
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'));manager=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
lib=unreal.get_default_object(unreal.SystemLibrary);health=p.get_editor_property('BPC_Health');bar=p.get_editor_property('Health_Widget').get_editor_property('HealthBar')
folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/items-colisiones');os.makedirs(folder,exist_ok=True)
def field(obj,name,value):lib.call_method('Set'+('Bool' if isinstance(value,bool) else 'Int' if isinstance(value,int) else 'Double')+'PropertyByName',(obj,name,value))
def prop(key):return extra.get_editor_property(key)
def snap():return {'health':health.get_editor_property('Health'),'bar':bar.get_editor_property('percent'),'kits':prop('Botiquines')}
def aim_item(i):
 item=prop('ItemMesa'+str(i));pos=item.get_actor_location();p.set_actor_location(unreal.Vector(pos.x,-740,95),False,True);p.set_actor_rotation(unreal.Rotator(yaw=-90),False)
 eye=p.get_editor_property('FPC').get_world_location();origin,extent,_=unreal.SystemLibrary.get_component_bounds(item.static_mesh_component);pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(eye,origin))
field(p,'CamaraPrimera',True);p.get_editor_property('TPC').deactivate();p.get_editor_property('FPC').activate()
for k in ['Botiquines','Cargas','Creditos']:field(extra,k,0)
for i in range(1,4):field(extra,'MesaRecogido'+str(i),False)
field(extra,'Botiquines',2);health.call_method('Increase_Health',(100.,));gs.apply_damage(p,40,pc,None,None)
s={'stage':0,'at':time.monotonic(),'handle':None,'checks':[],'healing':[snap()],'enemy':None}
def tick(dt,state=s):
 try:
  if time.monotonic()-state['at']<.6:return
  stage=state['stage']
  if stage==0:
   assert abs(health.get_editor_property('Health')-60)<.001 and abs(bar.get_editor_property('percent')-.6)<.001
   extra.call_method('UsarBotiquin');state['healing'].append(snap());assert health.get_editor_property('Health')==95 and abs(bar.get_editor_property('percent')-.95)<.001 and prop('Botiquines')==1
   extra.call_method('UsarBotiquin');state['healing'].append(snap());assert health.get_editor_property('Health')==100 and bar.get_editor_property('percent')==1 and prop('Botiquines')==0
   extra.call_method('UsarBotiquin');assert prop('Botiquines')==0
   state['checks'].append('dano_40_cura_35_y_5_barra_sincronizada_no_sobrepasa_100')
   # El barrido de la cápsula del personaje debe detenerse ante ambos objetos.
   robot=prop('Tecnico');c=robot.get_actor_location();p.set_actor_location(c+unreal.Vector(220,0,92),False,True);p.set_actor_location(c+unreal.Vector(0,0,92),True,False);rp=p.get_actor_location();assert rp.x-c.x>60,(rp,c)
   table=next(a for a in gs.get_all_actors_of_class(w,unreal.StaticMeshActor) if a.get_actor_label()=='Consola_Bruno');c=table.get_actor_location();p.set_actor_location(c+unreal.Vector(0,-220,92),False,True);p.set_actor_location(c+unreal.Vector(0,0,92),True,False);tp=p.get_actor_location();assert c.y-tp.y>50,(tp,c)
   state['blocking']={'robot_stop':str(rp),'table_stop':str(tp)};state['checks'].append('capsula_jugador_bloqueada_por_robot_y_mesa')
   aim_item(1)
  elif stage in [1,3,5]:
   i=(stage+1)//2
   if state.get('aim_refreshed')!=i:
    # Esperar el ajuste al suelo de CharacterMovement antes de apuntar a
    # la moneda, cuya altura visible es sólo de unos centímetros.
    center,_,_=unreal.SystemLibrary.get_component_bounds(prop('ItemMesa'+str(i)).static_mesh_component);pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(p.get_editor_property('FPC').get_world_location(),center));state['aim_refreshed']=i;return
   if prop('ObjetoEnMira')!=i and time.monotonic()-state['at']<3:return
   assert prop('ObjetoEnMira')==i,('target',i,prop('ObjetoEnMira'),str(pc.get_control_rotation()))
   extra.call_method('HablarConTecnico');assert prop('MesaRecogido'+str(i))
   before=[prop(k) for k in ['Botiquines','Cargas','Creditos']];extra.call_method('HablarConTecnico');assert [prop(k) for k in ['Botiquines','Cargas','Creditos']]==before
  elif stage in [2,4,6]:
   i=stage//2;item=prop('ItemMesa'+str(i));assert item.get_editor_property('hidden') and not item.get_actor_enable_collision()
   state['checks'].append('mesa_objeto_'+str(i)+'_efecto_real_recogida_unica_oculta_y_sin_colision')
   if i<3:aim_item(i+1)
   else:
    assert [prop(k) for k in ['Botiquines','Cargas','Creditos']]==[1,3,3]
    manager.call_method('SaveCheckpoint');assert manager.get_editor_property('bSaveSucceeded');data=gs.load_game_from_slot('TimeOut_Delivery_v1',0)
    assert data.get_editor_property('ExtrasRevision')==3 and all(data.get_editor_property('MesaRecogido'+str(j)) for j in range(1,4))
    for j in range(1,4):field(extra,'MesaRecogido'+str(j),False)
    field(extra,'Botiquines',0);manager.call_method('RestoreCheckpoint')
  elif stage==7:
   assert prop('Botiquines')==1 and all(prop('MesaRecogido'+str(i)) and prop('ItemMesa'+str(i)).get_editor_property('hidden') for i in range(1,4));state['checks'].append('checkpoint_restaura_objetos_y_cantidades_sin_reaparicion')
   p.set_actor_location(unreal.Vector(0,-1800,95),False,True);p.set_actor_rotation(unreal.Rotator(yaw=-90),False);pc.set_control_rotation(unreal.Rotator(yaw=-90))
   cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C');tr=unreal.Transform(location=unreal.Vector(0,-2250,95));native=unreal.get_default_object(gs);enemy=native.call_method('BeginDeferredActorSpawnFromClass',(w,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));native.call_method('FinishSpawningActor',(enemy,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));state['enemy']=enemy
  elif stage==8:
   if health.get_editor_property('Health')==100:
    assert time.monotonic()-state['at']<12,'El enemigo no llega a atacar'
    return
   enemy=state['enemy'];enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Aislar la curación después del primer golpe real');enemy.character_movement.disable_movement();enemy.stop_anim_montage(enemy.get_current_montage())
   state['healing'].append(snap());extra.call_method('UsarBotiquin');state['healing'].append(snap());assert health.get_editor_property('Health')==100 and bar.get_editor_property('percent')==1 and prop('Botiquines')==0
   state['checks'].append('golpe_real_IA_reduce_vida_y_botiquin_restaura_vida_y_barra')
   pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(p.get_editor_property('FPC').get_world_location(),enemy.get_actor_location()+unreal.Vector(0,0,35)))
  elif stage==9:
   extra.call_method('DispararPulso');enemy_health=state['enemy'].get_editor_property('BPC_E_Health').get_editor_property('E_Health');assert enemy_health==80,enemy_health
   beams=gs.get_all_actors_of_class(w,unreal.load_class(None,R+'BP_PulsoTemporalVisual.BP_PulsoTemporalVisual_C'));assert len(beams)==1
   beam=beams[0];assert beam.static_mesh_component.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION;assert 0<beam.get_actor_scale3d().x<=8.001,beam.get_actor_scale3d();state['beam']={'scale':str(beam.get_actor_scale3d()),'enemy_health':enemy_health,'bounded_to_eight_meters':True};assert prop('Cargas')==2
   extra.call_method('DispararPulso');assert prop('Cargas')==2
   state['checks'].append('pulso_visible_sin_dano_duplicado_20_dano_una_carga_cooldown')
  elif stage==10:
   assert not gs.get_all_actors_of_class(w,unreal.load_class(None,R+'BP_PulsoTemporalVisual.BP_PulsoTemporalVisual_C'));state['enemy'].destroy_actor();unreal.unregister_slate_post_tick_callback(state['handle'])
   result={'passed':True,'method':'PIE. Daño por ApplyDamage, funciones reales de ítems, barrido físico de cápsula y recogida por traza de cámara. Posiciones y saldos iniciales preparados. No callbacks de solapamiento ni daño directo al enemigo.','checks':state['checks'],'healing':state['healing'],'blocking':state['blocking'],'beam':state['beam']}
   with open(os.path.join(folder,'efectos-runtime.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
   unreal.log('ITEMS_EFFECTS_RUNTIME_PASSED');return
  state['stage']+=1;state['at']=time.monotonic()
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(os.path.join(folder,'efectos-runtime.json'),'w',encoding='utf-8') as f:json.dump({'passed':False,'stage':state['stage'],'checks':state['checks'],'error':traceback.format_exc()},f,ensure_ascii=False,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
