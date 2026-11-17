"""Prepare a separate native smoke location; not a natural gameplay checkpoint."""
import unreal,os,shutil,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;data=gs.load_game_from_slot('TimeOut_Delivery_v1',0);assert data
sys=unreal.get_default_object(unreal.SystemLibrary)
sys.call_method('SetVectorPropertyByName',(data,'PlayerLocation',unreal.Vector(3500,-3770,100)))
for key in ['PlayerRotation','ControlRotation']:sys.call_method('SetRotatorPropertyByName',(data,key,unreal.Rotator(pitch=-5 if key=='ControlRotation' else 0,yaw=50,roll=0)))
assert gs.save_game_to_slot(data,'TeamModels_Native_QA',0)
root=unreal.Paths.project_dir();folder=os.path.join(root,'Intermediate/inspect/team-models/native-user/Saved/SaveGames');os.makedirs(folder,exist_ok=True)
shutil.copy2(os.path.join(root,'Saved/SaveGames/TeamModels_Native_QA.sav'),os.path.join(folder,'TimeOut_Delivery_v1.sav'))
assert gs.delete_game_in_slot('TeamModels_Native_QA',0)
with open(os.path.join(root,'Intermediate/inspect/team-models/native-prepared.json'),'w') as f:json.dump({'prepared_checkpoint_not_natural_playthrough':True,'position':[3500,-3770,100],'user_dir':'Intermediate/inspect/team-models/native-user','original_saves_restored_after_qa':True},f,indent=2)
unreal.log('TEAM_NATIVE_CHECKPOINT_PREPARED')
