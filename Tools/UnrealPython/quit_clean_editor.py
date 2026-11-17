"""Libera proxies de QA antes del cierre del intérprete del editor.

Usar sólo después de finalizar y desregistrar todos los callbacks de pruebas.
No forma parte del juego ni se distribuye como dependencia del ejecutable.
"""
import unreal,gc
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
if dirty:assert unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
for qa_global_name in list(globals()):
 if qa_global_name not in ('unreal','gc','__builtins__','__name__','__doc__','__package__','__loader__','__spec__','__file__'):
  globals().pop(qa_global_name,None)
gc.collect();unreal.SystemLibrary.collect_garbage()
unreal.log('QA_PYTHON_REFERENCES_RELEASED')
unreal.SystemLibrary.quit_editor()
