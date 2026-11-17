import unreal,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
pc=unreal.GameplayStatics.get_player_controller(w,0);cam=pc.get_view_target();assert isinstance(cam,unreal.CameraActor)
cam.get_component_by_class(unreal.CameraComponent).set_field_of_view(70);cam.set_actor_location(unreal.Vector(3500,-3770,240),False,True);cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(unreal.Vector(3500,-3770,240),unreal.Vector(3850,-3350,90)),True)
unreal.SystemLibrary.execute_console_command(w,'viewmode unlit')
unreal.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/team-models/wreck-unlit.png'))
