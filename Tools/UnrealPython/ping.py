# Editor-side. Confirms the connection and lists unsaved packages. Changes nothing.
import unreal

ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
editor_world = ues.get_editor_world()
game_world = ues.get_game_world()
unreal.log("PING editor_world=%s game_world=%s" % (editor_world.get_name() if editor_world else None,
                                                    game_world.get_name() if game_world else None))
dirty = [p.get_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
unreal.log("DIRTY " + (", ".join(dirty) if dirty else "(none)"))
