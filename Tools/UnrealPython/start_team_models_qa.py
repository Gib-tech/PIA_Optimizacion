import unreal,os,json,shutil
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.project_dir();backup=os.path.join(root,'Intermediate/inspect/team-models/save-backup');saves=os.path.join(root,'Saved/SaveGames')
if not os.path.exists(os.path.join(backup,'inventory.json')):
 os.makedirs(backup,exist_ok=True);names=os.listdir(saves) if os.path.isdir(saves) else []
 for name in names:
  if os.path.isfile(os.path.join(saves,name)):shutil.copy2(os.path.join(saves,name),os.path.join(backup,name))
 with open(os.path.join(backup,'inventory.json'),'w') as f:json.dump(names,f)
unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground',False)
unreal.SystemLibrary.execute_console_command(None,'t.MaxFPS 30')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
unreal.log('TEAM_MODELS_QA_PIE_REQUESTED')
