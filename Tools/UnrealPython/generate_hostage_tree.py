"""Local: Behavior Tree clipboard subtree. Connect the selector to ROOT after pasting."""
from generate_delivery_graphs import Graph,Node,q,ref
import os
ROOT='/Game/ThirdPerson/Blueprints/Aliado'

class TreeGraph(Graph):
    def tree_node(self,kind,runtime,settings=(),x=0,y=0,index=None):
        node=Node(self,'BehaviorTreeEditor.BehaviorTreeGraphNode_'+kind,(),x,y)
        index=len(self.nodes) if index is None else index
        name='Instance_'+str(index)
        cls=runtime if runtime.startswith('/Game/') else '/Script/AIModule.'+runtime
        props=['Begin Object Class='+cls+' Name='+q(name)]
        props += ['   '+s for s in settings]
        props += ['End Object']
        if runtime.startswith('/Game/'):
            asset=runtime.rsplit('.',1)[0]
            props += ['ClassData=(AssetName='+q(asset.rsplit('/',1)[-1])+',GeneratedClassPackage='+q(asset)+',ClassName='+q(runtime.rsplit('.',1)[-1])+')']
        else:props += ['ClassData=(ClassName='+q(runtime)+')']
        props += ['NodeInstance='+q(cls+"'"+name+"'"),'CopySubNodeIndex='+str(index)]
        node.props=props
        if kind in ('Composite','Task'):
            node.pin('In','MultipleNodes')
            if kind=='Composite':node.pin('Out','MultipleNodes',out=True)
        return node
    def decorator(self,parent,key,numeric=False):
        i=int(next(p.split('=')[1] for p in parent.props if p.startswith('CopySubNodeIndex=')))
        settings=['BlackboardKey=(SelectedKeyName='+q(key)+')','FlowAbortMode=Both']
        if numeric:
            settings[1]='FlowAbortMode=LowerPriority'
            settings+=['OperationType=4','ArithmeticOperation=Greater','FloatValue=500.0']
        node=self.tree_node('Decorator','BTDecorator_Blackboard',settings,index=i)
        node.props+=['bIsSubNode=True']
        return node

g=TreeGraph()
selector=g.tree_node('Composite','BTComposite_Selector',['NodeName="Prioridad: huir > baliza > esperar > seguir > idle"'],x=0,y=0,index=1)
service=g.tree_node('Service',ROOT+'/BTService_HostageSense.BTService_HostageSense_C',index=1)
service.props+=['bIsSubNode=True']
flee=g.tree_node('Composite','BTComposite_Sequence',['NodeName="Huir a refugio seguro"'],x=-700,y=300,index=2)
g.decorator(flee,'bMustFlee')
move=g.tree_node('Task','BTTask_MoveTo',['BlackboardKey=(SelectedKeyName="FleeLocation")','AcceptableRadius=(DefaultValue=80.0)','bAllowPartialPath=(DefaultValue=False)','bReachTestIncludesAgentRadius=(DefaultValue=False)','NodeName="Llegar al refugio"'],x=-850,y=650,index=3)
arrive=g.tree_node('Task',ROOT+'/BTTask_HostageArrive.BTTask_HostageArrive_C',x=-550,y=650,index=4)
wait=g.tree_node('Task','BTTask_Wait',['WaitTime=(DefaultValue=0.5)','RandomDeviation=(DefaultValue=0.0)','NodeName="Esperar interaccion del jugador"'],x=-150,y=300,index=5)
g.decorator(wait,'bWaiting')
follow=g.tree_node('Composite','BTComposite_Sequence',['NodeName="Seguir al jugador"'],x=400,y=300,index=6)
g.decorator(follow,'bAccompanying');g.decorator(follow,'DistanceToPlayer',True)
followmove=g.tree_node('Task','BTTask_MoveTo',['BlackboardKey=(SelectedKeyName="PlayerActor")','AcceptableRadius=(DefaultValue=300.0)','bObserveBlackboardValue=True','bReachTestIncludesAgentRadius=(DefaultValue=False)','bReachTestIncludesGoalRadius=(DefaultValue=False)','bAllowPartialPath=(DefaultValue=False)'],x=400,y=650,index=7)
idle=g.tree_node('Task','BTTask_Wait',['WaitTime=(DefaultValue=0.5)','RandomDeviation=(DefaultValue=0.0)','NodeName="Idle junto al jugador"'],x=950,y=300,index=8)
activate=g.tree_node('Composite','BTComposite_Sequence',['NodeName="Activar baliza segura (3 segundos)"'],x=-350,y=300,index=9)
g.decorator(activate,'bActivateBeacon')
beaconmove=g.tree_node('Task','BTTask_MoveTo',['BlackboardKey=(SelectedKeyName="BeaconTarget")','AcceptableRadius=(DefaultValue=25.0)','bAllowPartialPath=(DefaultValue=False)','bReachTestIncludesAgentRadius=(DefaultValue=False)'],x=-350,y=950,index=10)
channel=g.tree_node('Task',ROOT+'/BTTask_ActivateBeacon.BTTask_ActivateBeacon_C',x=0,y=950,index=11)
for child in [flee,activate,wait,follow,idle]:g.wire(selector,'Out',child,'In')
for child in [beaconmove,channel]:g.wire(activate,'Out',child,'In')
for child in [move,arrive]:g.wire(flee,'Out',child,'In')
g.wire(follow,'Out',followmove,'In')
g.write('BT_Hostage_Subtree')
