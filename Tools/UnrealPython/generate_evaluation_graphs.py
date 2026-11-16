"""Team destructibles and combat integration; no runtime helper dependency."""
from generate_delivery_controls import ControlsGraph
from generate_progression_graphs import ACTOR,GS,MATH,HERO,DOOR,PRIM,SMC,VEC
from generate_delivery_graphs import ref,q
ROOT='/Game/ThirdPerson/Blueprints/Entrega/'
DESTRUCTIBLE=ROOT+'BP_DestruibleEntrega.BP_DestruibleEntrega_C'
GC='/Script/GeometryCollectionEngine.GeometryCollectionComponent'

def destructible():
 g=ControlsGraph();begin=g.event(ACTOR,'ReceiveBeginPlay')
 # The team Blueprint's component layout is retained. Its previous tutorial
 # widgets/overlaps are replaced in this owned copy by weapon damage events.
 box=g.v('Colision','object',obj='/Script/Engine.BoxComponent')
 prev=g.action_on(begin,PRIM,'SetCollisionEnabled',box,[('NewType','byte','QueryOnly','/Script/Engine.ECollisionEnabled')])
 collection=g.v('Destruible','object',obj=GC)
 g.action_on(prev,PRIM,'SetSimulatePhysics',collection,[('bSimulate','bool',False,None)])
 e=g.event(ACTOR,'ReceiveAnyDamage').pin('Damage','real',sub='float',out=True).pin('DamageType','object',obj='/Script/Engine.DamageType',out=True).pin('InstigatedBy','object',obj='/Script/Engine.Controller',out=True).pin('DamageCauser','object',obj=ACTOR,out=True)
 cast,p=g.cast_after(e,(e,'DamageCauser'),HERO)
 valid=g.both(g.neg(g.v('bBroken','bool')),g.cmp('Greater_DoubleDouble',(e,'Damage'),0))
 valid=g.both(valid,g.v('IsAttacking','bool',owner=HERO,target=p))
 gate=g.br(cast,valid);prev=g.s(gate,'Health',g.c(MATH,'FMax',[('A','real',g.op('Subtract_DoubleDouble',g.v('Health'),(e,'Damage'))),('B','real',0)]))
 broken=g.br(prev,g.cmp('LessEqual_DoubleDouble',g.v('Health'),0));prev=g.s(broken,'bBroken',True,'bool')
 collection=g.v('Destruible','object',obj=GC)
 prev=g.action_on(prev,PRIM,'SetCollisionEnabled',box,[('NewType','byte','NoCollision','/Script/Engine.ECollisionEnabled')])
 prev=g.action_on(prev,PRIM,'SetCollisionEnabled',collection,[('NewType','byte','QueryAndPhysics','/Script/Engine.ECollisionEnabled')])
 prev=g.action_on(prev,PRIM,'SetSimulatePhysics',collection,[('bSimulate','bool',True,None)])
 prev=g.action_on(prev,GC,'CrumbleActiveClusters',collection)
 pos=g.location(g.selfnode(typ=DESTRUCTIBLE),'self')
 prev=g.action_on(prev,PRIM,'AddRadialImpulse',collection,[('Origin','struct',(pos,'ReturnValue'),VEC),('Radius','real',500,None),('Strength','real',180,None),('Falloff','byte','RIF_Linear','/Script/Engine.ERadialImpulseFalloff'),('bVelChange','bool',True,None)])
 for channel in ['ECC_Pawn','ECC_Camera']:
  prev=g.action_on(prev,PRIM,'SetCollisionResponseToChannel',collection,[('Channel','byte',channel,'/Script/Engine.ECollisionChannel'),('NewResponse','byte','ECR_Ignore','/Script/Engine.ECollisionResponse')])
 fx=g.call('/Script/Niagara.NiagaraFunctionLibrary','SpawnSystemAtLocation',static=True).pin('SystemTemplate','object',obj='/Script/Niagara.NiagaraSystem').pin('Location','struct',obj=VEC).pin('Rotation','struct',obj='/Script/CoreUObject.Rotator',default='0,0,0').pin('Scale','struct',obj=VEC,default='1,1,1').pin('bAutoDestroy','bool',default='true').pin('bAutoActivate','bool',default='true').pin('PoolingMethod','byte',obj='/Script/Niagara.ENCPoolMethod',default='AutoRelease').pin('bPreCullCheck','bool',default='true')
 g.w(g.v('BreakFX','object',obj='/Script/Niagara.NiagaraSystem'),fx,'SystemTemplate');g.w((pos,'ReturnValue'),fx,'Location');g.chain(prev,fx)
 life=g.call(ACTOR,'SetLifeSpan').pin('InLifespan','real',sub='float',default='8');g.chain(fx,life)
 event=g.node('K2Node_ComponentBoundEvent',[
  'DelegatePropertyName="OnChaosBreakEvent"','DelegateOwnerClass='+ref(GC),'ComponentPropertyName="Destruible"',
  'EventReference=(MemberParent="/Script/CoreUObject.Package\'/Script/GeometryCollectionEngine\'",MemberName="OnChaosBreakEvent__DelegateSignature")',
  'bInternalEvent=True','CustomFunctionName="Evaluation_ChaosBreak"']).pin('then',out=True).pin('BreakEvent','struct',obj='/Script/PhysicsCore.ChaosBreakEvent',out=True)
 g.s(event,'ChaosBreakCount',g.op('Add_IntInt',g.v('ChaosBreakCount','int'),1,'int'),'int')
 g.write('BP_DestruibleEntrega')

def add_destructible_combat(g):
 overlap=next(n for n in g.nodes if 'SweepResult' in n.pins)
 door=next(n for n in g.nodes if n.kind.endswith('K2Node_DynamicCast') and any(DOOR in p for p in n.props))
 cast,target=g.cast_after(door,(overlap,'OtherActor'),DESTRUCTIBLE,pin='CastFailed')
 fresh=g.neg((g.array('HeavyHitActors','Array_Contains',item=overlap,ip='OtherActor'),'ReturnValue'))
 allow=g.br(cast,g.both(fresh,g.v('IsAttacking','bool')))
 add=g.array('HeavyHitActors','Array_AddUnique',item=overlap,ip='OtherActor');g.chain(allow,add)
 value=g.c(MATH,'SelectFloat',[('A','real',15),('B','real',25),('bPickA','bool',g.v('bLightAttackActive','bool'))])
 n=g.call(GS,'ApplyDamage',static=True).pin('DamagedActor','object',obj=ACTOR).pin('BaseDamage','real',sub='float').pin('EventInstigator','object',obj='/Script/Engine.Controller').pin('DamageCauser','object',obj=ACTOR).pin('DamageTypeClass','class',obj='/Script/Engine.DamageType').pin('ReturnValue','real',sub='float',out=True)
 g.w(target,n,'DamagedActor');g.w(value,n,'BaseDamage');g.w((g.selfnode(typ=HERO),'self'),n,'DamageCauser');g.chain(add,n)

if __name__=='__main__':destructible()
