"""Guarda sólo los recursos propios sucios y cierra para cargar el helper editor-only."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
if dirty:assert unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
unreal.SystemLibrary.quit_editor()
