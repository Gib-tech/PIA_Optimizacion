import unreal,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();p=unreal.GameplayStatics.get_player_character(w,0)
rows={}
for field in ['Mesh','BrazosFP','Weapon','EspadaFP','hammer','MartilloFP']:
 c=p.mesh if field=='Mesh' else p.get_editor_property(field)
 row={'relative':str(c.get_relative_transform()),'bounds':str(unreal.SystemLibrary.get_component_bounds(c)),'parent':str(c.get_attach_parent()),'socket':str(c.get_attach_socket_name())}
 if isinstance(c,unreal.SkeletalMeshComponent):
  row['sockets']={name:str(c.get_socket_transform(name,unreal.RelativeTransformSpace.RTS_COMPONENT)) for name in ['hand_r','WeaponSocket','HammerSocket','root']}
  row['socket_bones']={name:str(c.get_socket_bone_name(name)) for name in ['WeaponSocket','HammerSocket']}
 rows[field]=row
unreal.log('FP_ALIGNMENT '+json.dumps(rows))
