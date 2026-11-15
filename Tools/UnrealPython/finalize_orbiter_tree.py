"""Allow hit stun to interrupt attacks and restore the documented combat cooldowns."""
import unreal
tree=unreal.load_asset('/Game/ThirdPerson/Blueprints/EnemigoIA/BT_EnemyIA')
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world(),'Stop PIE before changing its tree.'
tree.modify()
hit=unreal.find_object(None,tree.get_path_name()+':BTDecorator_Blackboard_1')
hit.set_editor_property('FlowAbortMode',unreal.BTFlowAbortMode.BOTH)
for name,seconds in [('BTDecorator_Cooldown_0',3.0),('BTDecorator_Cooldown_1',6.0)]:
    node=unreal.find_object(None,tree.get_path_name()+':'+name)
    value=node.get_editor_property('CoolDownTime');value.set_editor_property('DefaultValue',seconds);node.set_editor_property('CoolDownTime',value)
unreal.EditorAssetLibrary.save_loaded_asset(tree,only_if_is_dirty=False)
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(tree)
unreal.log('ORBITER_INTERRUPTION_AND_COOLDOWNS_SAVED')
