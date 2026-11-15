import unreal
tree=unreal.load_asset('/Game/ThirdPerson/Blueprints/Aliado/BT_Hostage')
bb=unreal.load_asset('/Game/ThirdPerson/Blueprints/Aliado/BB_Hostage')
library=unreal.get_default_object(unreal.SystemLibrary.static_class())
library.call_method('SetObjectPropertyByName',(tree,'BlackboardAsset',bb))
graphroot=unreal.find_object(None,tree.get_path_name()+':Behavior Tree.BehaviorTreeGraphNode_Root_0')
assert graphroot,'Tree graph root was not found'
library.call_method('SetObjectPropertyByName',(graphroot,'BlackboardAsset',bb))
unreal.EditorAssetLibrary.save_loaded_asset(tree)
unreal.log('HOSTAGE_BLACKBOARD %s' % tree.get_blackboard_asset().get_path_name())
