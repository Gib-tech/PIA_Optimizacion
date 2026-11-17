import unreal,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller()
c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if c.get_editor_property('bActive'):c.call_method('FinishCinema')
sub_lib=unreal.get_default_object(unreal.load_class(None,'/Script/Engine.SubsystemBlueprintLibrary'))
input_sub=sub_lib.call_method('GetLocalPlayerSubSystemFromPlayerController',(pc,unreal.EnhancedInputLocalPlayerSubsystem.static_class()))
if not p.get_editor_property('CamaraPrimera'):input_sub.inject_input_vector_for_action(unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_Camera'),unreal.Vector(1,0,0),[],[])
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
script=os.path.join(root,'Tools/UnrealPython/playthrough_current_mission.py')
ns={'__name__':'mission_test','__file__':script};exec(compile(open(script,encoding='utf-8').read(),script,'exec'),ns)
