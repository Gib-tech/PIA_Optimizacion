"""Resolve all escort Blackboard selectors before cooking (including the new beacon MoveTo)."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root='/Game/ThirdPerson/Blueprints/Aliado/'
tree=unreal.load_asset(root+'BT_Hostage');bb=unreal.load_asset(root+'BB_Hostage')
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(tree)
keys={str(e.get_editor_property('entry_name')):i for i,e in enumerate(bb.get_editor_property('keys'))}
for name,keyname,kind in [('Instance_3','FleeLocation','Vector'),('Instance_7','PlayerActor','Object'),('Instance_10','BeaconTarget','Object'),('BTDecorator_Blackboard_0','bMustFlee','Bool'),('BTDecorator_Blackboard_1','bWaiting','Bool'),('BTDecorator_Blackboard_2','bAccompanying','Bool'),('BTDecorator_Blackboard_3','DistanceToPlayer','Float'),('BTDecorator_Blackboard_4','bActivateBeacon','Bool')]:
 node=unreal.find_object(None,tree.get_path_name()+':'+name);assert node,name
 key=node.get_editor_property('BlackboardKey');key.set_editor_property('SelectedKeyName',keyname);key.set_editor_property('SelectedKeyType',unreal.load_class(None,'/Script/AIModule.BlackboardKeyType_'+kind));key.set_editor_property('SelectedKeyID',keys[keyname]);node.set_editor_property('BlackboardKey',key)
 unreal.log('ESCORT_KEY '+name+' '+str(key.export_text()))
unreal.EditorAssetLibrary.save_loaded_asset(tree,only_if_is_dirty=False)
move=unreal.find_object(None,tree.get_path_name()+':Instance_10');radius=move.get_editor_property('AcceptableRadius');radius.set_editor_property('DefaultValue',25.0);move.set_editor_property('AcceptableRadius',radius);unreal.EditorAssetLibrary.save_loaded_asset(tree,only_if_is_dirty=False)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
for i in [1,2,3]:
 beacon=placed['Progression_Baliza_'+str(i)];point=placed.get('Progression_Approach_'+str(i))
 if not point:
  pos=beacon.get_actor_location();point=actors.spawn_actor_from_class(unreal.TargetPoint,unreal.Vector(pos.x,pos.y+180,0));point.set_actor_label('Progression_Approach_'+str(i));point.set_folder_path('Mision/Balizas')
 beacon.set_editor_property('ApproachPoint',point)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
