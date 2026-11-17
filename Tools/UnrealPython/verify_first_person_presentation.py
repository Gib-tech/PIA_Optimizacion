"""Prueba aislada en PIE: cámara, montajes reales y brazos sin daño duplicado."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=gs.get_player_controller(w,0)
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());folder=os.path.join(root,'docs/validation/primera-persona');os.makedirs(folder,exist_ok=True)
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
def flag(name,v):lib.call_method('SetBoolPropertyByName',(p,name,v))
def attack(heavy=False):
 name='IA_Heavy_Attack' if heavy else 'IA_Light_Attack';idx='6' if heavy else '7'
 p.call_method('InpActEvt_'+name+'_K2Node_EnhancedInputActionEvent_'+idx,(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/'+name)))
def capture(name):
 unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+os.path.join(folder,name+'.png').replace('\\','/')+'"')
def clean():
 p.stop_anim_montage(p.get_current_montage());flag('IsAttacking',False);flag('bLightAttackActive',False);flag('bSaveLightAttack',False);p.call_method('ResetState')
 p.get_editor_property('WeaponHitbox').set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
s={'stage':-1,'at':gs.get_time_seconds(w),'handle':None,'checks':[],'samples':[]}
def observe(dt,state=s):
 try:
  now=gs.get_time_seconds(w);age=now-state['at'];stage=state['stage'];arms=p.get_editor_property('BrazosFP')
  if age<.30:return
  if stage==-1:
   p.set_actor_location(unreal.Vector(0,-1800,100),False,True);pc.set_control_rotation(unreal.Rotator(pitch=-8,yaw=-90))
   clean();flag('bIsSwordEquipped',True);flag('bIsHammerEquipped',False)
   extra=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
   lib.call_method('SetBoolPropertyByName',(extra,'InventoryOpen',False))
  elif stage==0:
   assert arms.leader_pose_component is None and arms.get_attach_parent()==p.get_editor_property('FPC')
   assert arms.global_anim_rate_scale==0 and arms.get_animation_mode()==unreal.AnimationMode.ANIMATION_SINGLE_NODE
   assert arms.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
   hud=pc.get_hud();lib.call_method('SetIntPropertyByName',(hud,'DismissedDialog',hud.get_editor_property('CurrentDialog')))
   state['checks'].append('brazos_sin_colision_animacion_muestreada_sin_notifies');clean();flag('bIsSwordEquipped',True);flag('bIsHammerEquipped',False);capture('espada-reposo')
  elif stage==1:attack();state['started']=now
  elif stage==2:
   assert p.get_current_montage();capture('espada-ligero');state['checks'].append('montaje_ligero_espada')
  elif stage==3:
   if p.get_editor_property('IsAttacking'):return
   clean();attack(True)
  elif stage==4:
   assert p.get_current_montage();capture('espada-pesado');state['checks'].append('montaje_pesado_espada')
  elif stage==5:
   clean();flag('bIsSwordEquipped',False);flag('bIsHammerEquipped',True);attack()
  elif stage==6:
   assert p.get_current_montage();capture('martillo-ligero');state['checks'].append('montaje_ligero_martillo')
  elif stage==7:
   if p.get_editor_property('IsAttacking'):return
   clean();attack(True)
  elif stage==8:
   assert p.get_current_montage();capture('martillo-pesado');state['checks'].append('montaje_pesado_martillo')
  elif stage==9:
   clean();flag('CamaraPrimera',False);p.get_editor_property('TPC').activate();p.get_editor_property('FPC').deactivate()
  elif stage==10:
   assert not arms.is_visible() and not p.mesh.get_editor_property('owner_no_see');capture('tercera-persona');state['checks'].append('tercera_persona_restaura_cuerpo_y_oculta_brazos')
   flag('CamaraPrimera',True);p.get_editor_property('FPC').activate();p.get_editor_property('TPC').deactivate();pc.set_control_rotation(unreal.Rotator(pitch=45,yaw=-90))
  elif stage==11:
   assert arms.is_visible();capture('mirada-arriba');pc.set_control_rotation(unreal.Rotator(pitch=-55,yaw=-90));state['checks'].append('vista_sigue_pitch_sin_cabeza')
  elif stage==12:
   capture('mirada-abajo');pc.set_control_rotation(unreal.Rotator(pitch=-8,yaw=-90));clean()
   state['checks'].append('interrupcion_limpia_hitbox_y_estado')
   unreal.unregister_slate_post_tick_callback(state['handle'])
   with open(os.path.join(folder,'resultado.json'),'w',encoding='utf-8') as f:json.dump({'passed':True,'method':'PIE con llamadas a entradas reales; fixture visual, no partida natural ni mando físico','checks':state['checks'],'samples':state['samples']},f,indent=2,ensure_ascii=False)
   unreal.log('FIRST_PERSON_QA_PASSED');return
  state['samples'].append({'stage':stage,'montage':p.get_current_montage().get_name() if p.get_current_montage() else None,'arms_location':str(arms.relative_location),'hand':str(arms.get_socket_location('hand_r')),'sword_visible':p.get_editor_property('EspadaFP').is_visible(),'hammer_visible':p.get_editor_property('MartilloFP').is_visible()})
  state['stage']+=1;state['at']=now
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(os.path.join(folder,'resultado.json'),'w') as f:json.dump({'passed':False,'stage':state['stage'],'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
