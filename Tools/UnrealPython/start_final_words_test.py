"""Start isolated PIE; current user SaveGames were backed up before this slice."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
os.makedirs(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/final-words'),exist_ok=True)
unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground',False)
unreal.SystemLibrary.execute_console_command(None,'t.MaxFPS 30')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
unreal.log('FINAL_WORDS_TEST_PIE_STARTED')
