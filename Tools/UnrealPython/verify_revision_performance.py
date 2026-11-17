"""Muestra reproducible de render; no comparación antes/después ni benchmark."""
import unreal,os,json,time,statistics,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;pc=gs.get_player_controller(w,0);p=gs.get_player_character(w,0)
c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if c.get_editor_property('bActive'):c.call_method('FinishCinema')
p.set_actor_location(unreal.Vector(0,-1800,100),False,True);pc.set_control_rotation(unreal.Rotator(pitch=-8,yaw=-90));pc.set_view_target_with_blend(p,0)
unreal.SystemLibrary.execute_console_command(w,'t.MaxFPS 0')
unreal.SystemLibrary.execute_console_command(w,'stat RHI');unreal.SystemLibrary.execute_console_command(w,'stat SceneRendering')
folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/rendimiento-2026-11-17');os.makedirs(folder,exist_ok=True)
state={'at':time.monotonic(),'last':time.monotonic(),'frames':[],'handle':None}
def tick(dt,s=state):
 now=time.monotonic();elapsed=now-s['at'];step=now-s['last'];s['last']=now
 if elapsed>3:s['frames'].append(step)
 if elapsed<8:return
 unreal.unregister_slate_post_tick_callback(s['handle'])
 settings=unreal.GameUserSettings.get_game_user_settings()
 result={'method':'PIE, cámara quieta preparada, 3 s calentamiento y 5 s de Slate tick sin límite t.MaxFPS. No es benchmark del paquete ni comparación antes/después. Captura RHI adjunta para draw calls.','hardware':'AMD Ryzen 5 3600 / NVIDIA GeForce RTX 3060 Ti, Windows 11 25H2; fuente LogInit de Terreno.log','sample_frames':len(s['frames']),'editor_tick_mean_ms':1000*statistics.mean(s['frames']),'editor_tick_p95_ms':1000*sorted(s['frames'])[int(.95*(len(s['frames'])-1))],'qualities':{'distance':settings.get_view_distance_quality(),'aa':settings.get_anti_aliasing_quality(),'shadow':settings.get_shadow_quality(),'texture':settings.get_texture_quality()},'camera':str(p.get_actor_location()),'rotation':str(pc.get_control_rotation()),'viewport':str(pc.get_viewport_size())}
 with open(os.path.join(folder,'muestra.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
 unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+os.path.join(folder,'rhi.png').replace('\\','/')+'"')
 unreal.SystemLibrary.execute_console_command(w,'t.MaxFPS 30');unreal.log('PERFORMANCE_SAMPLE_COMPLETE')
state['handle']=unreal.register_slate_post_tick_callback(tick)
