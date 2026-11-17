"""Remove only generated, unreferenced prototypes superseded by the baked atlas."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
base='/Game/ThirdPerson/Environment/TeamModels/'
paths=[base+'Materials/M_Escombros_'+str(i) for i in [1,2]]+[base+'Textures/T_Escombros_'+str(i)+'_BaseColor' for i in [1,2]]
for path in paths:
 if not unreal.EditorAssetLibrary.does_asset_exist(path):continue
 refs=list(unreal.EditorAssetLibrary.find_package_referencers_for_asset(path,True))
 assert all(str(ref) in paths for ref in refs),(path,refs)
for path in paths:
 if unreal.EditorAssetLibrary.does_asset_exist(path):assert unreal.EditorAssetLibrary.delete_asset(path),path
root=unreal.Paths.project_dir()
for name in ['SM_AutoDestruido.fbx','T_Escombros_1_BaseColor.png','T_Escombros_2_BaseColor.png']:
 path=os.path.abspath(os.path.join(root,'Tools/ArtSource/TeamModels',name));assert os.path.dirname(path)==os.path.abspath(os.path.join(root,'Tools/ArtSource/TeamModels'))
 if os.path.isfile(path):os.remove(path)
unreal.log('TEAM_GENERATED_PROTOTYPES_REMOVED')
