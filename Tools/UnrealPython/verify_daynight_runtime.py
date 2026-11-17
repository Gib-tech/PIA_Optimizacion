"""Muestrea el Blueprint solar real, pausa y retorno de fase, con tiempo preparado."""
import unreal,os,json,time,math,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;R='/Game/ThirdPerson/Blueprints/Entrega/'
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
sun=extra.get_editor_property('Sun').get_component_by_class(unreal.DirectionalLightComponent)
moon=extra.get_editor_property('Moon').get_component_by_class(unreal.DirectionalLightComponent)
sky=extra.get_editor_property('Sky').light_component
lib=unreal.get_default_object(unreal.SystemLibrary)
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());folder=os.path.join(root,'docs/validation/ciclo-luces-ataques')
def settime(v):lib.call_method('SetDoublePropertyByName',(extra,'WorldSeconds',v))
def smooth(a,b,x):t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
duration=extra.get_editor_property('DayCycleDuration');assert duration==1200,duration
original=extra.get_editor_property('WorldSeconds');samples=[]
state={'index':0,'stage':'set','at':time.monotonic(),'handle':None,'rows':samples,'checks':[]}
def finish(s,error=None):
 gs.set_game_paused(w,False);settime(original);unreal.unregister_slate_post_tick_callback(s['handle'])
 report={'passed':error is None,'method':'PIE real. Fase preparada cada 5 segundos de un ciclo completo; se leen luces del Blueprint. Incluye avance natural, pausa y reanudación. No se acelera globalmente la simulación.','cycle_seconds':duration,'checks':s['checks'],'samples':s['rows']}
 if error:report['error']=error
 with open(os.path.join(folder,'ciclo-runtime.json'),'w',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
 unreal.log('DAYNIGHT_RUNTIME_FINISHED '+str(error is None))
def tick(dt,s=state):
 try:
  now=time.monotonic()
  if s['stage']=='set':
   if s['index']>240:
    s['checks'].append('241_fases_sin_saltos_de_formula_y_periodo_1200_s')
    s.update(stage='natural',at=now,clock=extra.get_editor_property('WorldSeconds'));return
   settime(s['index']*5.);s.update(stage='read',at=now);return
  if s['stage']=='read':
   clock=extra.get_editor_property('WorldSeconds');elev=math.sin(math.radians(35+clock*360/duration))
   expected_sun=26000*smooth(-.06,.59,elev);night=1-smooth(-.2,.2,elev)
   assert abs(sun.intensity-expected_sun)<2,(clock,sun.intensity,expected_sun)
   assert abs(moon.intensity-1.2*night)<.001
   assert abs(sky.intensity-(.65+.10*night))<.001
   s['rows'].append({'clock':clock,'sun_lux':sun.intensity,'moon_lux':moon.intensity,'sky_intensity':sky.intensity})
   s['index']+=1;s['stage']='set';return
  if s['stage']=='natural' and now-s['at']>2:
   elapsed=extra.get_editor_property('WorldSeconds')-s['clock'];assert 1.5<elapsed<3,elapsed
   s['checks'].append('reloj_avanza_en_segundos_de_juego');gs.set_game_paused(w,True)
   s.update(stage='paused',at=now,clock=extra.get_editor_property('WorldSeconds'),sun=sun.intensity);return
  if s['stage']=='paused' and now-s['at']>1:
   assert extra.get_editor_property('WorldSeconds')==s['clock'] and sun.intensity==s['sun']
   s['checks'].append('pausa_congela_fase_y_luces');gs.set_game_paused(w,False);s.update(stage='resumed',at=now);return
  if s['stage']=='resumed' and now-s['at']>1:
   assert extra.get_editor_property('WorldSeconds')>s['clock']+.7
   s['checks'].append('reanudar_continua_sin_reiniciar');finish(s)
 except Exception:finish(s,traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(tick)
