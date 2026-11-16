"""Replace rotation waits with a single explicit facing action, preserving the existing tree."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
E='/Game/ThirdPerson/Blueprints/EnemigoIA/'
builder=unreal.DeliveryBlueprintBuilder;lib=unreal.BlueprintEditorLibrary
bp=unreal.load_asset(E+'BTTask_FaceCombatTarget')
if not bp:
 f=unreal.BlueprintFactory();f.set_editor_property('parent_class',unreal.BTTask_BlueprintBase)
 bp=unreal.AssetToolsHelpers.get_asset_tools().create_asset('BTTask_FaceCombatTarget',E,unreal.Blueprint,f)
 lib.add_member_variable(bp,'CachedPawn',lib.get_object_reference_type(unreal.load_class(None,E+'BP_BaseEnemy.BP_BaseEnemy_C')));lib.compile_blueprint(bp)
assert builder.install_graph(bp,os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()),'Intermediate/inspect/delivery_graphs/BTTask_FaceCombatTarget.t3d'))
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
tree=unreal.load_asset(E+'BT_EnemyIA')
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(tree)
for i in [11,3]:
 node=unreal.find_object(None,tree.get_path_name()+':Behavior Tree.BehaviorTreeGraphNode_Task_'+str(i))
 assert node,i
 new=unreal.find_object(None,tree.get_path_name()+':FaceCombatTarget_'+str(i)) or unreal.new_object(bp.generated_class(),outer=tree,name='FaceCombatTarget_'+str(i))
 ref=new.get_class().get_path_name()+"'"+new.get_path_name()+"'"
 assert builder.set_property_text(node,'NodeInstance',ref)
 assert builder.set_property_text(node,'ClassData','(AssetName="BTTask_FaceCombatTarget",GeneratedClassPackage="'+E+'BTTask_FaceCombatTarget",ClassName="BTTask_FaceCombatTarget_C")')
builder.connect_tree_root(tree)
for seq,face,tail,tailclass in [('BTComposite_Sequence_1',3,'BTTask_Defend_C_0',E+'BTTask_Defend.BTTask_Defend_C'),('BTComposite_Sequence_3',11,'BTTask_MoveTo_0','/Script/AIModule.BTTask_MoveTo')]:
 parent=unreal.find_object(None,tree.get_path_name()+':'+seq)
 first=unreal.find_object(None,tree.get_path_name()+':FaceCombatTarget_'+str(face))
 last=unreal.find_object(None,tree.get_path_name()+':'+tail)
 value='((ChildTask='+bp.generated_class().get_path_name()+"'"+first.get_path_name()+"'),(ChildTask="+tailclass+"'"+last.get_path_name()+"'))"
 assert builder.set_property_text(parent,'Children',value),(seq,value)
move=unreal.find_object(None,tree.get_path_name()+':BTTask_MoveTo_0');v=move.get_editor_property('bAllowStrafe');v.set_editor_property('DefaultValue',False);move.set_editor_property('bAllowStrafe',v)
unreal.EditorAssetLibrary.save_loaded_asset(tree,only_if_is_dirty=False)
for asset in [tree,bp]:
 t=unreal.AssetExportTask();t.object=asset;t.filename=os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()),'Intermediate/inspect/live',asset.get_name()+'.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;unreal.Exporter.run_asset_export_task(t)
unreal.log('ORBITER_FACING_REFINED')
