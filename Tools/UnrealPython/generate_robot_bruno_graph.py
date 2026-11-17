"""Animación de presentación del robot fijo; no decide ni concede recursos."""
from generate_delivery_controls import ControlsGraph
from generate_progression_graphs import ACTOR,MATH,GS,VEC,SCENE
from generate_rubric_systems import EXTRAS
ROBOT='/Game/ThirdPerson/Blueprints/Entrega/BP_TecnicoTemporal.BP_TecnicoTemporal_C'
SMC='/Script/Engine.StaticMeshComponent';ROT='/Script/CoreUObject.Rotator'
def robot():
 g=ControlsGraph();tick=g.event(ACTOR,'ReceiveTick').pin('DeltaSeconds','real',sub='float',out=True)
 prev=g.s(tick,'TiempoVisual',g.op('Add_DoubleDouble',g.v('TiempoVisual'),(tick,'DeltaSeconds')))
 seq=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True).pin('then_1',out=True);g.chain(prev,seq)
 cached=g.v('Sistema','object',obj=EXTRAS);missing=g.br(seq,g.neg((g.valid(*cached),'ReturnValue')),'then_0')
 found=g.find(missing,EXTRAS);g.s(found,'Sistema',(found,'ReturnValue'),'object',obj=EXTRAS)
 good=g.br(seq,(g.valid(*cached),'ReturnValue'),'then_1')
 busy=g.v('bFabricating','bool',owner=EXTRAS,target=cached)
 rate=g.c(MATH,'SelectFloat',[('A','real',180),('B','real',16),('bPickA','bool',busy)])
 angle=g.op('Multiply_DoubleDouble',g.v('TiempoVisual'),rate)
 ring=g.v('AroConversion','object',obj=SMC)
 rot=g.c(MATH,'MakeRotator',[('Roll','real',0),('Pitch','real',0),('Yaw','real',angle)],cat='struct',obj=ROT)
 prev=g.action_on(good,SCENE,'K2_SetRelativeRotation',ring,[('NewRotation','struct',rot,ROT),('bSweep','bool',False,None),('bTeleport','bool',True,None)])
 head=g.v('CabezaRobot','object',obj=SMC)
 yaw=g.op('Multiply_DoubleDouble',g.c(MATH,'Sin',[('A','real',g.op('Multiply_DoubleDouble',g.v('TiempoVisual'),.45))]),12)
 head_rot=g.c(MATH,'MakeRotator',[('Roll','real',0),('Pitch','real',0),('Yaw','real',g.op('Add_DoubleDouble',90,yaw))],cat='struct',obj=ROT)
 prev=g.action_on(prev,SCENE,'K2_SetRelativeRotation',head,[('NewRotation','struct',head_rot,ROT),('bSweep','bool',False,None),('bTeleport','bool',True,None)])
 light=g.v('LuzConversion','object',obj='/Script/Engine.PointLightComponent')
 intensity=g.c(MATH,'SelectFloat',[('A','real',45),('B','real',3),('bPickA','bool',busy)])
 g.action_on(prev,'/Script/Engine.LightComponent','SetIntensity',light,[('NewIntensity','real',intensity,None)])
 g.write('BP_TecnicoTemporal')
if __name__=='__main__':robot()
