import unreal,os,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_character(w,0);a=p.get_editor_property('BrazosFP');sword=p.get_editor_property('EspadaFP');pc=p.get_controller()
sword.set_relative_location(unreal.Vector(),False,True)
sword.set_relative_scale3d(unreal.Vector(.5,.5,.5))
t=sword.get_world_transform()
for x in [-516,-400,-300,-200,-100,0,100,200,366]:
 point=unreal.MathLibrary.transform_location(t,unreal.Vector(x,0,0));unreal.log('SWORD_X '+str(x)+' '+str(pc.project_world_location_to_screen(point,False)))
unreal.log('SWORD_LOCAL_SOCKET '+str(a.get_socket_transform('WeaponSocket',unreal.RelativeTransformSpace.RTS_PARENT_BONE_SPACE)))
# El pivote del asset no está en el mango: se alinea el tercio de empuñadura.
grip=unreal.MathLibrary.transform_location(t,unreal.Vector(285,0,0));palm=a.get_socket_location('middle_02_r')
correction=unreal.MathLibrary.inverse_transform_direction(t,palm-grip)/t.scale3d.x
sword.set_world_location(sword.get_world_location()+palm-grip,False,True)
p.get_editor_property('LuzFP').set_intensity(400)
s={'handle':None,'at':unreal.GameplayStatics.get_time_seconds(w)}
def cb(dt,state=s):
 if unreal.GameplayStatics.get_time_seconds(w)-state['at']<1:return
 unreal.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/fp_polish/grip-aligned.png').replace('\\','/')+'"');unreal.unregister_slate_post_tick_callback(state['handle'])
s['handle']=unreal.register_slate_post_tick_callback(cb)
unreal.log('SWORD_CORRECTION '+str(correction)+' RELATIVE '+str(sword.relative_location))
