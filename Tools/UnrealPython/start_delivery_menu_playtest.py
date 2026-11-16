import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert level.load_level('/Game/LevelMenu/MainMenuLevel')
level.editor_request_begin_play()
unreal.log('SAVE_MENU_PLAYTEST_STARTED')
