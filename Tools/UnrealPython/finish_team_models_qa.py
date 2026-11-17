import unreal,os,json,shutil,hashlib
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.project_dir();out=os.path.join(root,'Intermediate/inspect/team-models');backup=os.path.join(out,'save-backup');saves=os.path.join(root,'Saved/SaveGames');names=json.load(open(os.path.join(backup,'inventory.json')));os.makedirs(saves,exist_ok=True)
for name in names:
 if os.path.isfile(os.path.join(backup,name)):shutil.copy2(os.path.join(backup,name),os.path.join(saves,name))
for name in ['TimeOut_Delivery_v1.sav','TimeOut_Options_v1.sav']:
 path=os.path.abspath(os.path.join(saves,name));assert os.path.dirname(path)==os.path.abspath(saves)
 if name not in names and os.path.isfile(path):os.remove(path)
hashes={}
for name in names:
 if not os.path.isfile(os.path.join(backup,name)):continue
 a=hashlib.sha256(open(os.path.join(backup,name),'rb').read()).hexdigest();b=hashlib.sha256(open(os.path.join(saves,name),'rb').read()).hexdigest();assert a==b;hashes[name]=b
unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground',True);unreal.SystemLibrary.execute_console_command(None,'t.MaxFPS 0')
with open(os.path.join(out,'qa-restored.json'),'w') as f:json.dump({'passed':True,'save_sha256':hashes,'preferences_restored':True},f,indent=2)
unreal.log('TEAM_MODELS_QA_RESTORED')
