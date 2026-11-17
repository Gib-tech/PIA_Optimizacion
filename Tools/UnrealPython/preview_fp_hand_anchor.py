import unreal,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_character(w,0);a=p.get_editor_property('BrazosFP');pc=p.get_controller()
for name in ['hand_r','WeaponSocket','index_01_r','lowerarm_r']:
 q=a.get_socket_location(name);unreal.log('FP_HAND_SCREEN '+name+' '+str(pc.project_world_location_to_screen(q,False))+' '+str(q))
unreal.get_default_object(unreal.SystemLibrary).call_method('SetDoublePropertyByName',(p,'FPHeight',-17.0))
sword=p.get_editor_property('EspadaFP');sword.set_relative_rotation(unreal.Rotator(roll=60),False,True);sword.set_relative_scale3d(unreal.Vector(.65,.65,.65))
light=p.get_editor_property('LuzFP');light.set_intensity(1500)
s={'handle':None,'at':unreal.GameplayStatics.get_time_seconds(w)}
def cb(dt,state=s):
 if unreal.GameplayStatics.get_time_seconds(w)-state['at']<1:return
 unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/fp_polish/hand-raised.png').replace('\\','/')+'"');unreal.unregister_slate_post_tick_callback(state['handle'])
s['handle']=unreal.register_slate_post_tick_callback(cb)
