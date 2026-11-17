"""Restore this slice's saved games and editor preferences after stopped PIE."""
import unreal,os,shutil,hashlib,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());out=os.path.join(root,'Intermediate/inspect/final-words')
backup=os.path.join(out,'save-backup/SaveGames');saves=os.path.join(root,'Saved/SaveGames')
assert os.path.isdir(backup);os.makedirs(saves,exist_ok=True)
names=os.listdir(backup)
for name in names:
 source=os.path.join(backup,name)
 if os.path.isfile(source):shutil.copy2(source,os.path.join(saves,name))
for name in ['TimeOut_Delivery_v1.sav','TimeOut_Options_v1.sav']:
 path=os.path.abspath(os.path.join(saves,name));assert os.path.dirname(path)==os.path.abspath(saves)
 if name not in names and os.path.isfile(path):os.remove(path)
hashes={}
for name in names:
 if not os.path.isfile(os.path.join(backup,name)):continue
 a=hashlib.sha256(open(os.path.join(backup,name),'rb').read()).hexdigest();b=hashlib.sha256(open(os.path.join(saves,name),'rb').read()).hexdigest();assert a==b
 hashes[name]=b
unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground',True)
unreal.SystemLibrary.execute_console_command(None,'t.MaxFPS 0')
with open(os.path.join(out,'qa-restored.json'),'w') as f:json.dump({'passed':True,'original_save_sha256':hashes,'preferences_restored':True},f,indent=2)
unreal.log('FINAL_WORDS_QA_RESTORED')
