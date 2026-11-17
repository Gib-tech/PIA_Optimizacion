import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_character(w,0);a=p.get_editor_property('BrazosFP')
for key in ['Weapon','EspadaFP','hammer','MartilloFP']:
 c=p.get_editor_property(key);unreal.log('ALIGN '+key+' '+str(c.relative_location)+' '+str(c.relative_rotation)+' '+str(c.relative_scale3d)+' socket '+str(c.get_attach_socket_name())+' parent '+str(c.get_attach_parent()))
for name in ['hand_r','WeaponSocket','index_01_r','middle_01_r']:
 unreal.log('ALIGN '+name+' bone '+str(a.get_socket_bone_name(name))+' '+str(a.get_socket_transform(name,unreal.RelativeTransformSpace.RTS_COMPONENT)))
