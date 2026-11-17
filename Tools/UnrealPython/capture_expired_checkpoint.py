import unreal,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
hud=unreal.GameplayStatics.get_player_controller(w,0).get_hud()
assert not hud.get_editor_property('StatusNoticeVisible')
unreal.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/final-words/notice-expired.png'))
unreal.log('FINAL_WORDS_EXPIRED_NOTICE_CAPTURED')
