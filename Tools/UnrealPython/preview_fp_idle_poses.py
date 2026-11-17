"""Muestrea posturas de reposo sin modificar daño ni montajes del juego."""
import unreal,os,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_character(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
lib=unreal.get_default_object(unreal.SystemLibrary.static_class());folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/primera-persona');os.makedirs(folder,exist_ok=True)
def setp(name,value,kind='Double'):lib.call_method('Set'+kind+'PropertyByName',(p,name,value))
p.set_actor_location(unreal.Vector(0,-1800,100),False,True);pc.set_control_rotation(unreal.Rotator(yaw=-90,pitch=-8));setp('CamaraPrimera',True,'Bool')
p.get_editor_property('FPC').activate();p.get_editor_property('TPC').deactivate();p.stop_anim_montage(p.get_current_montage());p.call_method('ResetState');setp('IsAttacking',False,'Bool')
fp_preview={'index':0,'at':unreal.GameplayStatics.get_time_seconds(w),'handle':None,'shots':[]}
cases=[('sword',x) for x in [.15,.3,.45,.6,.75]]+[('hammer',x) for x in [.25,.45,.65,.8]]
def tick(dt,state=fp_preview):
 now=unreal.GameplayStatics.get_time_seconds(w)
 if now-state['at']<.5:return
 if state['index']>=len(cases):unreal.unregister_slate_post_tick_callback(state['handle']);return
 weapon,pos=cases[state['index']]
 if not state.get('prepared'):
  setp('bIsSwordEquipped',weapon=='sword','Bool');setp('bIsHammerEquipped',weapon=='hammer','Bool');setp('FPIdleSwordPosition' if weapon=='sword' else 'FPIdleHammerPosition',pos)
  state.update(prepared=True,at=now);return
 hud=pc.get_hud();lib.call_method('SetIntPropertyByName',(hud,'DismissedDialog',hud.get_editor_property('CurrentDialog')))
 path=os.path.join(folder,'reposo-'+weapon+'-'+str(pos)+'.png').replace('\\','/')
 unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+path+'"')
 state['index']+=1;state.update(prepared=False,at=now)
fp_preview['handle']=unreal.register_slate_post_tick_callback(tick)
