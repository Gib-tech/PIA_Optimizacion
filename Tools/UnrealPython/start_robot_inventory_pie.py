import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
