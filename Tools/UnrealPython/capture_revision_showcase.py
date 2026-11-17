"""Capturas de presentación en PIE, con cámara/recursos preparados.

No se usan como evidencia del recorrido natural ni del saldo de una partida.
"""
import unreal,os,math,json,traceback
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
gs=unreal.GameplayStatics;pc=gs.get_player_controller(world,0);p=gs.get_player_character(world,0)
get=lambda cls:gs.get_actor_of_class(world,unreal.load_class(None,cls+'.'+cls.rsplit('/',1)[-1]+'_C'))
cinema=get('/Game/ThirdPerson/Cinematics/BP_CinematicDirector')
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
extra=get('/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios');host=get('/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage')
native=unreal.get_default_object(gs);tr=unreal.Transform(location=unreal.Vector(0,0,180))
cam=native.call_method('BeginDeferredActorSpawnFromClass',(world,unreal.CameraActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));native.call_method('FinishSpawningActor',(cam,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
cam.get_component_by_class(unreal.CameraComponent).set_field_of_view(65)
folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/revision-2026-11-17');os.makedirs(folder,exist_ok=True)
lib=unreal.get_default_object(unreal.SystemLibrary)
def field(obj,key,value):lib.call_method(('SetBool' if isinstance(value,bool) else 'SetInt' if isinstance(value,int) else 'SetDouble')+'PropertyByName',(obj,key,value))
def view(pos,target):
 cam.set_actor_location(unreal.Vector(*pos),False,True);cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(unreal.Vector(*pos),unreal.Vector(*target)),True);pc.set_view_target_with_blend(cam,0)
def host_view():
 q=host.get_actor_location();view((q.x-260,q.y+200,q.z+65),(q.x,q.y,q.z+25))
def tech_view():view((-660,-520,175),(-430,-880,85))
def console_view():view((-720,-740,170),(-520,-960,80))
def water_view():view((2400,-1180,285),(3000,-1850,3))
def night_view():field(extra,'WorldSeconds',245.0);view((700,-400,280),(-1000,-1700,80))
def day_view():field(extra,'WorldSeconds',0.0);view((700,-400,280),(-1000,-1700,80))
def inventory_view():
 pc.set_view_target_with_blend(p,0);p.set_actor_location(unreal.Vector(-150,-1000,100),False,True);pc.set_control_rotation(unreal.Rotator(pitch=-8,yaw=-90))
 field(extra,'Botiquines',2);field(extra,'Cargas',6);field(extra,'Creditos',3);field(extra,'InventoryOpen',True)
shots=[('rehen',host_view),('bruno',tech_view),('consola',console_view),('agua',water_view),('noche',night_view),('dia',day_view),('inventario',inventory_view)]
s={'index':0,'phase':0,'at':0,'handle':None}
def tick(dt,state=s):
 try:
  now=gs.get_time_seconds(world)
  if now-state['at']<1.4:return
  name,prepare=shots[state['index']]
  if state['phase']==0:
   field(extra,'InventoryOpen',False);pc.get_hud().set_editor_property('show_hud',name=='inventario');p.get_editor_property('Health_Widget').set_visibility(unreal.SlateVisibility.VISIBLE if name=='inventario' else unreal.SlateVisibility.HIDDEN);prepare();state['phase']=1
  else:
   unreal.SystemLibrary.execute_console_command(world,'HighResShot 1280x720 filename="'+os.path.join(folder,name+'.png').replace('\\','/')+'"');state['index']+=1;state['phase']=0
   if state['index']==len(shots):
    unreal.unregister_slate_post_tick_callback(state['handle']);pc.get_hud().set_actor_hidden_in_game(False)
    with open(os.path.join(folder,'metodo.json'),'w',encoding='utf-8') as f:json.dump({'method':'Cámaras y recursos preparados sólo para presentación; no es partida natural','shots':[n for n,_ in shots]},f,ensure_ascii=False,indent=2)
    unreal.log('SHOWCASE_CAPTURED');return
  state['at']=now
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle']);unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
