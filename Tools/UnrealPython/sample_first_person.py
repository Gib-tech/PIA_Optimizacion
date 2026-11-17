import unreal,json,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_character(w,0);pc=unreal.GameplayStatics.get_player_controller(w,0)
cinema=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
lib.call_method('SetBoolPropertyByName',(p,'CamaraPrimera',True))
# Activar mediante la misma acción del jugador permite que el padre actualice
# ambas cámaras y conserve su orientación de control.
pc.set_control_rotation(unreal.Rotator(pitch=-8,yaw=-90))
p.get_editor_property('FPC').activate();p.get_editor_property('TPC').deactivate()
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
unreal.log('PRESENTATION_RUNTIME '+json.dumps({'host_anim':str(h.mesh.anim_class),'host_mesh':h.mesh.get_skeletal_mesh_asset().get_path_name(),'host_valid_anim':h.mesh.has_valid_animation_instance(),'fp_mesh':p.get_editor_property('BrazosFP').get_skeletal_mesh_asset().get_path_name(),'arms_parent':str(p.get_editor_property('BrazosFP').get_attach_parent()),'leader':str(p.get_editor_property('BrazosFP').leader_pose_component)}))
