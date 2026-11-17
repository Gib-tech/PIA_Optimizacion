"""Start a fresh PIE for isolated cinematic checks, preserving local save files."""
import unreal,os,shutil,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
folder=os.path.join(root,'Intermediate/inspect/cinematics/save-backup');os.makedirs(folder,exist_ok=True)
marker=os.path.join(folder,'inventory.json')
if not os.path.exists(marker):
    saves=os.path.join(root,'Saved/SaveGames');names=os.listdir(saves) if os.path.isdir(saves) else []
    for name in names:
        if os.path.isfile(os.path.join(saves,name)):shutil.copy2(os.path.join(saves,name),os.path.join(folder,name))
    with open(marker,'w') as f:json.dump(names,f)
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'));settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
unreal.SystemLibrary.execute_console_command(None,'t.MaxFPS 30')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
unreal.log('CINEMA_QA_PIE_STARTED')
