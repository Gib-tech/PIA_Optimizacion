"""Tune the existing two trees, retaining their distinct decision structure."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
E='/Game/ThirdPerson/Blueprints/EnemigoIA/';builder=unreal.DeliveryBlueprintBuilder
tree=unreal.load_asset(E+'BT_Charger');tree.modify()
node=unreal.find_object(None,tree.get_path_name()+':Behavior Tree.BehaviorTreeGraphNode_Task_13');assert node
bp=unreal.load_asset(E+'BTTask_Attack');new=unreal.find_object(None,tree.get_path_name()+':CloseMelee_9') or unreal.new_object(bp.generated_class(),outer=tree,name='CloseMelee_9')
assert builder.set_property_text(node,'NodeInstance',bp.generated_class().get_path_name()+"'"+new.get_path_name()+"'")
assert builder.set_property_text(node,'ClassData','(AssetName="BTTask_Attack",GeneratedClassPackage="'+E+'BTTask_Attack",ClassName="BTTask_Attack_C")')
seq=unreal.find_object(None,tree.get_path_name()+':Instance_8');assert seq
assert builder.set_property_text(seq,'Children','((ChildTask='+bp.generated_class().get_path_name()+"'"+new.get_path_name()+"'),(ChildTask=/Script/AIModule.BTTask_Wait'"+tree.get_path_name()+":Instance_10'),(ChildTask="+E+"BTTask_ChargerRecover.BTTask_ChargerRecover_C'"+tree.get_path_name()+":Instance_11'))")
assert builder.set_property_text(seq,'NodeName','Golpe cercano y recuperacion')
for name in ['Instance_6','Instance_10']:
 wait=unreal.find_object(None,tree.get_path_name()+':'+name);v=wait.get_editor_property('WaitTime');v.set_editor_property('DefaultValue',.4);wait.set_editor_property('WaitTime',v)
move=unreal.find_object(None,tree.get_path_name()+':Instance_13');v=move.get_editor_property('AcceptableRadius');v.set_editor_property('DefaultValue',140);move.set_editor_property('AcceptableRadius',v)
unreal.EditorAssetLibrary.save_loaded_asset(tree,only_if_is_dirty=False)
orbiter=unreal.load_asset(E+'BT_EnemyIA');move=unreal.find_object(None,orbiter.get_path_name()+':BTTask_MoveTo_0')
if move:
 v=move.get_editor_property('AcceptableRadius');v.set_editor_property('DefaultValue',35);move.set_editor_property('AcceptableRadius',v)
 for key in ['bReachTestIncludesAgentRadius','bReachTestIncludesGoalRadius']:
  value=move.get_editor_property(key);value.set_editor_property('DefaultValue',False);move.set_editor_property(key,value)
 unreal.EditorAssetLibrary.save_loaded_asset(orbiter,only_if_is_dirty=False)
for asset in [tree,orbiter]:
 task=unreal.AssetExportTask();task.object=asset;task.filename=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/live',asset.get_name()+'.t3d');task.automated=True;task.prompt=False;task.replace_identical=True;unreal.Exporter.run_asset_export_task(task)
unreal.log('COMBAT_MOVEMENT_TREES_TUNED')
