"""Restore local progress/preferences after stopped PIE, without saving QA state."""
import unreal,os,json,shutil
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
folder=os.path.join(root,'Intermediate/inspect/cinematics/save-backup');saves=os.path.join(root,'Saved/SaveGames')
with open(os.path.join(folder,'inventory.json')) as f:names=json.load(f)
os.makedirs(saves,exist_ok=True)
for name in names:
    source=os.path.join(folder,name)
    if os.path.isfile(source):shutil.copy2(source,os.path.join(saves,name))
for name in ['TimeOut_Delivery_v1.sav','TimeOut_Options_v1.sav']:
    path=os.path.abspath(os.path.join(saves,name));assert os.path.dirname(path)==os.path.abspath(saves)
    if name not in names and os.path.isfile(path):os.remove(path)
unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground',True)
unreal.SystemLibrary.execute_console_command(None,'t.MaxFPS 0')
unreal.log('CINEMA_QA_RESTORED_SAVES_AND_PREFERENCES')
