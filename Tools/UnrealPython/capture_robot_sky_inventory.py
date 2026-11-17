"""Muestras visuales preparadas de la revisión, con varios segundos de adaptación."""
import unreal,os,time,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;pc=gs.get_player_controller(w,0);p=gs.get_player_character(w,0);R='/Game/ThirdPerson/Blueprints/Entrega/'
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
native=unreal.get_default_object(gs);tr=unreal.Transform(location=unreal.Vector(0,0,180));cam=native.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.CameraActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));native.call_method('FinishSpawningActor',(cam,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));cam.camera_component.set_field_of_view(68)
folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/robot-cielo-inventario');os.makedirs(folder,exist_ok=True)
lib=unreal.get_default_object(unreal.SystemLibrary)
def field(key,value,kind='Double'):lib.call_method('Set'+kind+'PropertyByName',(extra,key,value))
def view(pos,target):
 cam.set_actor_location(unreal.Vector(*pos),False,True);cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(unreal.Vector(*pos),unreal.Vector(*target)),False);pc.set_view_target_with_blend(cam,0)
def prepare(name,age):
 field('WorldSeconds',age);field('InventoryOpen',name=='inventario','Bool');pc.get_hud().set_editor_property('show_hud',name=='inventario');p.get_editor_property('Health_Widget').set_visibility(unreal.SlateVisibility.VISIBLE if name=='inventario' else unreal.SlateVisibility.HIDDEN)
 if name=='robot':view((-175,-655,153),(-400,-850,92))
 elif name=='inventario':
  for k,v in [('Botiquines',2),('Cargas',6),('Creditos',3)]:field(k,v,'Int')
  view((100,-600,220),(-600,-1200,70))
 else:view((1000,-1300,300),(-1500,-2400,1400))
shots=[('inventario',0.),('robot',0.),('dia',0.),('atardecer',176.),('noche',300.)]
s={'i':0,'phase':0,'at':time.monotonic(),'handle':None,'samples':[]}
def tick(dt,state=s):
 try:
  if state['i']==len(shots):
   if time.monotonic()-state['at']<1:return
   unreal.unregister_slate_post_tick_callback(state['handle']);pc.get_hud().set_editor_property('show_hud',True);p.get_editor_property('Health_Widget').set_visibility(unreal.SlateVisibility.HIT_TEST_INVISIBLE);pc.set_view_target_with_blend(p,0);field('WorldSeconds',0.);field('InventoryOpen',True,'Bool')
   with open(os.path.join(folder,'muestras.json'),'w',encoding='utf-8') as f:json.dump({'method':'PIE, cámaras, inventario y fase preparados; 4 s de adaptación por captura. No partida natural.','samples':state['samples']},f,ensure_ascii=False,indent=2)
   unreal.log('ROBOT_SKY_INVENTORY_CAPTURED');return
  if time.monotonic()-state['at']<4:return
  name,age=shots[state['i']]
  if state['phase']==0:prepare(name,age);state['phase']=1
  else:
   sun=extra.get_editor_property('Sun').get_component_by_class(unreal.DirectionalLightComponent);moon=extra.get_editor_property('Moon').get_component_by_class(unreal.DirectionalLightComponent)
   state['samples'].append({'name':name,'clock':extra.get_editor_property('WorldSeconds'),'sun_lux':sun.intensity,'moon_lux':moon.intensity,'realtime_sky':extra.get_editor_property('Sky').light_component.real_time_capture,'sky_mid':str(extra.get_editor_property('SkyMID'))})
   unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+os.path.join(folder,name+'.png').replace('\\','/')+'"');state['i']+=1;state['phase']=0
  state['at']=time.monotonic()
 except Exception:unreal.unregister_slate_post_tick_callback(state['handle']);unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
