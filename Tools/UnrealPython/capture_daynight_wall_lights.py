"""Capturas PIE con cámara/hora preparadas y comparación de luminarias apagadas/encendidas."""
import unreal,os,time,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;pc=gs.get_player_controller(w,0);p=gs.get_player_character(w,0);R='/Game/ThirdPerson/Blueprints/Entrega/'
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
lamps=gs.get_all_actors_of_class(w,unreal.load_class(None,R+'BP_LuminariaPared.BP_LuminariaPared_C'));assert len(lamps)==41
for lamp in lamps:
 light=lamp.get_component_by_class(unreal.SpotLightComponent)
 assert light.get_attach_parent()==lamp.root_component,lamp.get_actor_label()
 assert light.get_world_location().distance(lamp.get_actor_location())<50,(lamp.get_actor_label(),str(light.get_world_location()))
 assert all(c.get_world_location().distance(lamp.get_actor_location())<50 for c in lamp.get_components_by_class(unreal.StaticMeshComponent)),lamp.get_actor_label()
native=unreal.get_default_object(gs);tr=unreal.Transform(location=unreal.Vector(0,0,180))
cam=native.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.CameraActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));native.call_method('FinishSpawningActor',(cam,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));cam.camera_component.set_field_of_view(80)
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());folder=os.path.join(root,'docs/validation/ciclo-luces-ataques')
lib=unreal.get_default_object(unreal.SystemLibrary);original=extra.get_editor_property('WorldSeconds')
pc.get_hud().set_editor_property('show_hud',False);p.get_editor_property('Health_Widget').set_visibility(unreal.SlateVisibility.HIDDEN)
shots=[('rescate-sin-luminarias',783,(0,-1050,170),(500,-600,160),False),('rescate-noche',783,(0,-1050,170),(500,-600,160),True),('arena-noche',783,(550,-3850,170),(-300,-3000,160),True),('jardin-noche',783,(2800,-3500,170),(3300,-3500,180),True),('atrio-noche',783,(0,-8250,170),(0,-7300,155),True),('patio-noche',783,(0,-10350,170),(700,-11100,160),True),('dia',0,(550,-3850,170),(-300,-3000,160),True),('atardecer',475,(550,-3850,170),(-300,-3000,160),True),('amanecer',1075,(550,-3850,170),(-300,-3000,160),True)]
s={'i':0,'stage':0,'at':time.monotonic(),'handle':None,'rows':[]}
def reset():
 for a in lamps:a.get_component_by_class(unreal.SpotLightComponent).set_visibility(True)
 pc.get_hud().set_editor_property('show_hud',True);p.get_editor_property('Health_Widget').set_visibility(unreal.SlateVisibility.HIT_TEST_INVISIBLE);pc.set_view_target_with_blend(p,0);lib.call_method('SetDoublePropertyByName',(extra,'WorldSeconds',original));cam.destroy_actor()
def tick(dt,state=s):
 try:
  now=time.monotonic()
  if state['i']==len(shots):
   if now-state['at']<1:return
   unreal.unregister_slate_post_tick_callback(state['handle']);reset()
   with open(os.path.join(folder,'capturas.json'),'w',encoding='utf-8') as f:json.dump({'method':'PIE; cámaras/hora preparadas. 5 s de adaptación por captura. Comparación sin/con focos nuevos en el mismo punto; no es una partida natural.','verified_light_count':len(lamps),'all_meshes_and_lights_follow_actor':True,'samples':state['rows']},f,ensure_ascii=False,indent=2)
   unreal.log('DAYNIGHT_CAPTURES_FINISHED');return
  name,age,pos,target,lights=shots[state['i']]
  if state['stage']==0:
   lib.call_method('SetDoublePropertyByName',(extra,'WorldSeconds',float(age)))
   position=unreal.Vector(*pos)
   ground=unreal.NavigationSystemV1.project_point_to_navigation(w,unreal.Vector(pos[0],pos[1],20),None,None,unreal.Vector(180,180,200))
   if ground:position=ground+unreal.Vector(0,0,170)
   cam.set_actor_location(position,False,True);cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(position,unreal.Vector(*target)),False);pc.set_view_target_with_blend(cam,0)
   for a in lamps:a.get_component_by_class(unreal.SpotLightComponent).set_visibility(lights)
   state.update(stage=1,at=now);return
  if now-state['at']<5:return
  sun=extra.get_editor_property('Sun').light_component;moon=extra.get_editor_property('Moon').light_component
  state['rows'].append({'name':name,'clock':extra.get_editor_property('WorldSeconds'),'sun_lux':sun.intensity,'moon_lux':moon.intensity,'new_lights':lights})
  unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+os.path.join(folder,name+'.png').replace('\\','/')+'"')
  state.update(i=state['i']+1,stage=0,at=now)
 except Exception:unreal.unregister_slate_post_tick_callback(state['handle']);reset();unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
