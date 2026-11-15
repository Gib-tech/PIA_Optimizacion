import unreal
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/EnemigoIA/ABP_EnemyEntrega')
library=unreal.get_default_object(unreal.SystemLibrary.static_class())
for name,x in [('AnimGraphNode_LinkedAnimGraph_0',-400),('AnimGraphNode_Slot_1',-100),('AnimGraphNode_Root_0',200)]:
    node=unreal.find_object(None,bp.get_path_name()+':AnimGraph.'+name)
    library.call_method('SetIntPropertyByName',(node,'NodePosX',x))
    library.call_method('SetIntPropertyByName',(node,'NodePosY',0))
unreal.log('ANIM_LAYOUT_READY')
