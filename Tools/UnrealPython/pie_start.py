# Editor-side. Starts Play In Editor on the open map. Wait 3-5 seconds before sampling.
# When the editor window is not focused, PIE ticks at about 3 FPS, so allow extra time.
import unreal

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
unreal.log("PIE requested")
