from generate_hostage_tree import TreeGraph
from generate_delivery_graphs import q
ROOT='/Game/ThirdPerson/Blueprints/EnemigoIA'
g=TreeGraph()
def task(name,x,y,index):return g.tree_node('Task',ROOT+'/'+name+'.'+name+'_C',x=x,y=y,index=index)
def numeric(parent,operation,value,abort='LowerPriority'):
    i=int(next(p.split('=')[1] for p in parent.props if p.startswith('CopySubNodeIndex=')))
    number={'Greater':4,'GreaterOrEqual':5,'LessOrEqual':3,'Less':2}[operation]
    n=g.tree_node('Decorator','BTDecorator_Blackboard',['BlackboardKey=(SelectedKeyName="DistanceToTarget")','FlowAbortMode='+abort,'OperationType='+str(number),'ArithmeticOperation='+operation,'FloatValue='+str(value)],index=i)
    n.props+=['bIsSubNode=True'];return n
root=g.tree_node('Composite','BTComposite_Selector',['NodeName="Dano > carga > retirada > preparar > perseguir > patrulla"'],x=0,y=0,index=1)
service=g.tree_node('Service',ROOT+'/BTService_ChargerSense.BTService_ChargerSense_C',index=1);service.props+=['bIsSubNode=True']
hit=task('BTTask_HitSun',-1600,350,2);g.decorator(hit,'bReceivingDamage')
charge=task('BTTask_ChargerCharge',-1100,350,3);g.decorator(charge,'bCharging')
retreat=g.tree_node('Composite','BTComposite_Sequence',['NodeName="Retirada y recuperacion"'],x=-450,y=350,index=4);g.decorator(retreat,'bRetreat')
close=g.tree_node('Composite','BTComposite_Sequence',['NodeName="Golpe cercano y recuperacion"'],x=400,y=350,index=8);numeric(close,'Less',250)
for seq,base,x in [(retreat,5,-650),(close,9,200)]:
    move=task('BTTask_Attack' if base==9 else 'BTTask_ChargerRetreat',x,700,base)
    wait=g.tree_node('Task','BTTask_Wait',['WaitTime=(DefaultValue=0.4)','RandomDeviation=(DefaultValue=0.0)'],x=x+250,y=700,index=base+1)
    recover=task('BTTask_ChargerRecover',x+500,700,base+2)
    for n in [move,wait,recover]:g.wire(seq,'Out',n,'In')
windup=task('BTTask_ChargerWindup',1250,350,12);g.decorator(windup,'TargetActor');numeric(windup,'GreaterOrEqual',250);numeric(windup,'LessOrEqual',700)
cd=g.tree_node('Decorator','BTDecorator_Cooldown',['CoolDownTime=(DefaultValue=2.0)'],index=12);cd.props+=['bIsSubNode=True']
chase=g.tree_node('Task','BTTask_MoveTo',['BlackboardKey=(SelectedKeyName="TargetActor")','AcceptableRadius=(DefaultValue=140.0)','bObserveBlackboardValue=True','bReachTestIncludesAgentRadius=(DefaultValue=False)','bReachTestIncludesGoalRadius=(DefaultValue=False)','bAllowPartialPath=(DefaultValue=False)','NodeName="Perseguir sin orbitar"'],x=1850,y=350,index=13)
g.decorator(chase,'TargetActor');numeric(chase,'Greater',0)
roam=g.tree_node('Composite','BTComposite_Sequence',['NodeName="Patrullar"'],x=2450,y=350,index=14)
r=task('BTTask_Roam',2300,700,15)
w=g.tree_node('Task','BTTask_Wait',['WaitTime=(DefaultValue=2.0)','RandomDeviation=(DefaultValue=0.0)'],x=2600,y=700,index=16)
g.wire(roam,'Out',r,'In');g.wire(roam,'Out',w,'In')
for n in [hit,charge,retreat,close,windup,chase,roam]:g.wire(root,'Out',n,'In')
g.write('BT_Charger_Subtree')
