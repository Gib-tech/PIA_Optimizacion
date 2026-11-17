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
 # La autoridad de contacto está en el jugador y la del pulso en su traza.
 # IsAttacking sólo describe melee y rechazaba el pulso legítimo del héroe.
 e.props.append('NodeComment='+q('Acepta daño positivo del protagonista: espada/martillo ligero o pesado y pulso. Las ventanas y deduplicación pertenecen al jugador; el pulso valida carga, alcance y visibilidad. bBroken evita fracturas repetidas. docs/CICLO_LUCES_Y_ATAQUES.md'))
 gate=g.br(cast,valid);prev=g.s(gate,'Health',g.c(MATH,'FMax',[('A','real',g.op('Subtract_DoubleDouble',g.v('Health'),(e,'Damage'))),('B','real',0)]))
 broken=g.br(prev,g.cmp('LessEqual_DoubleDouble',g.v('Health'),0));prev=g.s(broken,'bBroken',True,'bool')
 collection=g.v('Destruible','object',obj=GC)
 display=g.local('ModeloIntacto','/Script/Engine.StaticMeshActor');has_display=g.br(prev,(g.valid(*display),'ReturnValue'))
 hidden=g.action_on(has_display,ACTOR,'SetActorHiddenInGame',display,[('bNewHidden','bool',True,None)])
 show=g.action_on(hidden,'/Script/Engine.SceneComponent','SetVisibility',collection,[('bNewVisibility','bool',True,None),('bPropagateToChildren','bool',False,None)])
 prev=g.action_on(show,PRIM,'SetCollisionEnabled',box,[('NewType','byte','NoCollision','/Script/Engine.ECollisionEnabled')])
 g.chain(has_display,prev,'else')
 prev=g.action_on(prev,PRIM,'SetCollisionEnabled',collection,[('NewType','byte','QueryAndPhysics','/Script/Engine.ECollisionEnabled')])
 prev=g.action_on(prev,PRIM,'SetSimulatePhysics',collection,[('bSimulate','bool',True,None)])
 prev=g.action_on(prev,GC,'CrumbleActiveClusters',collection)
 pos=g.call('/Script/Engine.SceneComponent','K2_GetComponentLocation',pure=True).pin('ReturnValue','struct',obj=VEC,out=True);g.w(box,pos,'self')
 prev=g.action_on(prev,PRIM,'AddRadialImpulse',collection,[('Origin','struct',(pos,'ReturnValue'),VEC),('Radius','real',500,None),('Strength','real',180,None),('Falloff','byte','RIF_Linear','/Script/Engine.ERadialImpulseFalloff'),('bVelChange','bool',True,None)])
 for channel in ['ECC_Pawn','ECC_Camera']:
  prev=g.action_on(prev,PRIM,'SetCollisionResponseToChannel',collection,[('Channel','byte',channel,'/Script/Engine.ECollisionChannel'),('NewResponse','byte','ECR_Ignore','/Script/Engine.ECollisionResponse')])
 fx=g.call('/Script/Niagara.NiagaraFunctionLibrary','SpawnSystemAtLocation',static=True).pin('SystemTemplate','object',obj='/Script/Niagara.NiagaraSystem').pin('Location','struct',obj=VEC).pin('Rotation','struct',obj='/Script/CoreUObject.Rotator',default='0,0,0').pin('Scale','struct',obj=VEC,default='.4,.4,.4').pin('bAutoDestroy','bool',default='true').pin('bAutoActivate','bool',default='true').pin('PoolingMethod','byte',obj='/Script/Niagara.ENCPoolMethod',default='AutoRelease').pin('bPreCullCheck','bool',default='true')
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
 allow.props.append('NodeComment='+q('Cualquier arma cuerpo a cuerpo, sin exigir mejora: 15 ligero / 25 pesado. Sólo contacto de WeaponHitbox durante su ventana; HeavyHitActors impide daño duplicado por swing. Las puertas mantienen sus reglas de misión.'))
 add=g.array('HeavyHitActors','Array_AddUnique',item=overlap,ip='OtherActor');g.chain(allow,add)
 value=g.c(MATH,'SelectFloat',[('A','real',15),('B','real',25),('bPickA','bool',g.v('bLightAttackActive','bool'))])
 n=g.call(GS,'ApplyDamage',static=True).pin('DamagedActor','object',obj=ACTOR).pin('BaseDamage','real',sub='float').pin('EventInstigator','object',obj='/Script/Engine.Controller').pin('DamageCauser','object',obj=ACTOR).pin('DamageTypeClass','class',obj='/Script/Engine.DamageType').pin('ReturnValue','real',sub='float',out=True)
 g.w(target,n,'DamagedActor');g.w(value,n,'BaseDamage');g.w((g.selfnode(typ=HERO),'self'),n,'DamageCauser');g.chain(add,n)
 # El arco de espada puede pasar sobre caja/banca sin solapar su proxy bajo.
 # Barrer un volumen corto frente al personaje durante la misma ventana activa
 # hace alcanzables los props bajos; la primera pared bloqueante corta el golpe.
 from generate_delivery_controls import split_exec
 tick=next(n for n in g.nodes if any('MemberName="ReceiveTick"' in p for p in n.props))
 seq=split_exec(g,tick)
 previous=g.nodes[:];old=list(seq.pins['then_0']['links']);seq.pins['then_0']['links']=[]
 gate=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True).pin('then_1',out=True);g.chain(seq,gate,'then_0')
 for name,pid in old:
  node=next(x for x in previous if x.name==name);pin=next(x for x in node.pins.values() if x['id']==pid)
  pin['links'].remove((seq.name,seq.pins['then_0']['id']));g.chain(gate,node,'then_0',pin['name'])
 box=g.v('WeaponHitbox','object',obj='/Script/Engine.BoxComponent')
 collision=g.c(PRIM,'GetCollisionEnabled',cat='byte',obj='/Script/Engine.ECollisionEnabled',static=False);g.w(box,collision[0],'self')
 # EqualEqual_ByteByte takes a raw byte; QueryOnly is ECollisionEnabled=1.
 open_window=g.cmp('EqualEqual_ByteByte',collision,1,'byte')
 ready=g.br(gate,g.both(g.v('IsAttacking','bool'),open_window),'then_1')
 origin=g.c(ACTOR,'K2_GetActorLocation',cat='struct',obj=VEC,static=False)
 start=g.c(MATH,'Add_VectorVector',[('A','struct',origin),('B','struct','0,0,-20')],cat='struct',obj=VEC)
 for pin in ['A','B']:start[0].pins[pin]['obj']=VEC
 forward=g.c(ACTOR,'GetActorForwardVector',cat='struct',obj=VEC,static=False)
 reach=g.c(MATH,'Multiply_VectorFloat',[('A','struct',forward),('B','real',220)],cat='struct',obj=VEC);reach[0].pins['A']['obj']=VEC
 end=g.c(MATH,'Add_VectorVector',[('A','struct',start),('B','struct',reach)],cat='struct',obj=VEC)
 for pin in ['A','B']:end[0].pins[pin]['obj']=VEC
 trace=g.call('/Script/Engine.KismetSystemLibrary','SphereTraceSingle',static=True).pin('Start','struct',obj=VEC).pin('End','struct',obj=VEC).pin('Radius','real',sub='float',default='52').pin('TraceChannel','byte',obj='/Script/Engine.ETraceTypeQuery',default='TraceTypeQuery1').pin('bTraceComplex','bool',default='false').pin('ActorsToIgnore','object',obj=ACTOR).pin('DrawDebugType','byte',obj='/Script/Engine.EDrawDebugTrace',default='None').pin('bIgnoreSelf','bool',default='true').pin('OutHit','struct',obj='/Script/Engine.HitResult',out=True).pin('ReturnValue','bool',out=True)
 trace.pins['ActorsToIgnore']['container']='Array';g.w(start,trace,'Start');g.w(end,trace,'End');g.chain(ready,trace)
 trace.props.append('NodeComment='+q('Barrido de props bajos: 220 cm, radio 52, altura 75 cm aprox. Sólo durante WeaponHitbox QueryOnly + IsAttacking. Primer bloqueo Visibility; no atraviesa muros. Comparte HeavyHitActors con el overlap para aplicar un daño por swing.'))
 hit=g.call(GS,'BreakHitResult',pure=True,static=True).pin('Hit','struct',obj='/Script/Engine.HitResult').pin('HitActor','object',obj=ACTOR,out=True);g.w((trace,'OutHit'),hit,'Hit')
 cast2,target2=g.cast_after(trace,(hit,'HitActor'),DESTRUCTIBLE)
 contains=g.array('HeavyHitActors','Array_Contains',item=hit,ip='HitActor');fresh2=g.br(cast2,g.neg((contains,'ReturnValue')))
 cache=g.array('HeavyHitActors','Array_AddUnique',item=hit,ip='HitActor');g.chain(fresh2,cache)
 damage=g.call(GS,'ApplyDamage',static=True).pin('DamagedActor','object',obj=ACTOR).pin('BaseDamage','real',sub='float').pin('EventInstigator','object',obj='/Script/Engine.Controller').pin('DamageCauser','object',obj=ACTOR).pin('DamageTypeClass','class',obj='/Script/Engine.DamageType').pin('ReturnValue','real',sub='float',out=True)
 g.w(target2,damage,'DamagedActor');g.w(value,damage,'BaseDamage');g.w((g.selfnode(typ=HERO),'self'),damage,'DamageCauser');g.chain(cache,damage)

if __name__=='__main__':destructible()
