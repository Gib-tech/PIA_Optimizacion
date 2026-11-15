from generate_delivery_graphs import Graph,Node,q
g=Graph()
pose='/Script/Engine.PoseLink'
linked=Node(g,'AnimGraph.AnimGraphNode_LinkedAnimGraph',['Node=(InstanceClass='+q("/Script/Engine.AnimBlueprintGeneratedClass'/Game/SciFITrooper_Man_03/Blueprints/AnimBP/ABP_SciFiTrooperManV3.ABP_SciFiTrooperManV3_C'")+')'],x=-600,y=0).pin('Pose','struct',obj=pose,out=True)
slot=Node(g,'AnimGraph.AnimGraphNode_Slot',['Node=(SlotName="DefaultSlot")'],x=-250,y=0).pin('Source','struct',obj=pose).pin('Pose','struct',obj=pose,out=True)
g.wire(linked,'Pose',slot,'Source')
g.write('ABP_EnemyEntrega_AnimGraph')
