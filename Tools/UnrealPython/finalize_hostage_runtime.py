"""Editor-side: save escort assets and disable Pawn input (director owns interaction)."""
import unreal
root='/Game/ThirdPerson/Blueprints/Aliado/'
bb=unreal.load_asset(root+'BB_Hostage')
for entry in bb.get_editor_property('keys'):
    if str(entry.get_editor_property('entry_name'))=='PlayerActor':
        entry.get_editor_property('key_type').set_editor_property('BaseClass',unreal.Actor)
unreal.EditorAssetLibrary.save_loaded_asset(bb)
tree=unreal.load_asset(root+'BT_Hostage')
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(tree)
move=unreal.find_object(None,tree.get_path_name()+':Instance_7')
key=move.get_editor_property('BlackboardKey')
key.set_editor_property('SelectedKeyName','PlayerActor')
key.set_editor_property('SelectedKeyType',unreal.load_class(None,'/Script/AIModule.BlackboardKeyType_Object'))
key.set_editor_property('SelectedKeyID',0)
move.set_editor_property('BlackboardKey',key)
unreal.log('FOLLOW_KEY_BEFORE_SAVE '+str(move.get_editor_property('BlackboardKey').export_text()))
decorator=unreal.find_object(None,tree.get_path_name()+':BTDecorator_Blackboard_3')
decorator.set_editor_property('FlowAbortMode',unreal.BTFlowAbortMode.LOWER_PRIORITY)
unreal.EditorAssetLibrary.save_loaded_asset(tree)
unreal.log('FOLLOW_KEY_AFTER_SAVE '+str(move.get_editor_property('BlackboardKey').export_text()))
bp=unreal.load_asset(root+'BP_Hostage')
unreal.get_default_object(bp.generated_class()).set_editor_property('auto_receive_input',unreal.AutoReceiveInput.DISABLED)
for name in ['BP_Hostage','BP_HostageController','BTService_HostageSense','BTTask_HostageArrive','ABP_Hostage']:
    asset=unreal.load_asset(root+name)
    unreal.BlueprintEditorLibrary.compile_blueprint(asset)
    unreal.EditorAssetLibrary.save_loaded_asset(asset)
unreal.log('HOSTAGE_RUNTIME_SAVED')
