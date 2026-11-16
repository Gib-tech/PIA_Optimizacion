"""Blueprint source for matched irregular door fragments; no native game module."""
from generate_progression_graphs import ProgressGraph,ACTOR,OBJECT,VEC,SM,SMC,PRIM,MATH,FRAGMENT,HERO
from generate_wave_graphs import TRANSFORM

def spawn_shards(g,prev,hero):
 meshes=g.v('FragmentMeshes','object',obj='/Script/Engine.StaticMesh');meshes[0].pins[meshes[1]]['container']='Array'
 loop=g.foreach(meshes[0],meshes[1],typ='/Script/Engine.StaticMesh');g.chain(prev,loop,nextpin='Exec')
 offsets=g.v('FragmentOffsets','struct',obj=VEC);offsets[0].pins[offsets[1]]['container']='Array'
 item=g.node('K2Node_GetArrayItem',['bReturnByRefDesired=False']).pin('Array','struct',obj=VEC).pin('Dimension 1','int').pin('Output','struct',obj=VEC,out=True);item.pins['Array']['container']='Array';g.w(offsets,item,'Array');g.wire(loop,'Array Index',item,'Dimension 1')
 transform=g.call(ACTOR,'GetTransform',pure=True).pin('ReturnValue','struct',obj=TRANSFORM,out=True)
 world=g.c(MATH,'TransformLocation',[('T','struct',(transform,'ReturnValue')),('Location','struct',(item,'Output'))],cat='struct',obj=VEC);world[0].pins['T']['obj']=TRANSFORM;world[0].pins['Location']['obj']=VEC
 rotation=g.call(ACTOR,'K2_GetActorRotation',pure=True).pin('ReturnValue','struct',obj='/Script/CoreUObject.Rotator',out=True)
 tr=g.call(MATH,'MakeTransform',pure=True,static=True).pin('Location','struct',obj=VEC).pin('Rotation','struct',obj='/Script/CoreUObject.Rotator').pin('Scale','struct',obj=VEC,default='1,1,1').pin('ReturnValue','struct',obj=TRANSFORM,out=True);g.w(world,tr,'Location');g.wire(rotation,'ReturnValue',tr,'Rotation')
 own=g.location(g.selfnode(typ=ACTOR),'self');attacker=g.location(*hero)
 away=g.c(MATH,'Subtract_VectorVector',[('A','struct',(own,'ReturnValue')),('B','struct',(attacker,'ReturnValue'))],cat='struct',obj=VEC)
 for p in ['A','B']:away[0].pins[p]['obj']=VEC
 direction=g.c(MATH,'Vector_Normal2D',[('A','struct',away),('Tolerance','real',.0001)],cat='struct',obj=VEC);direction[0].pins['A']['obj']=VEC
 outward=g.c(MATH,'Multiply_VectorFloat',[('A','struct',direction),('B','real',420)],cat='struct',obj=VEC);outward[0].pins['A']['obj']=VEC
 split=g.call(MATH,'BreakVector',pure=True,static=True).pin('InVec','struct',obj=VEC).pin('X','real',sub='double',out=True).pin('Z','real',sub='double',out=True);g.wire(item,'Output',split,'InVec')
 radial=g.c(MATH,'MakeVector',[('X','real',g.op('Multiply_DoubleDouble',(split,'X'),1.25)),('Y','real',0),('Z','real',g.op('Add_DoubleDouble',g.op('Multiply_DoubleDouble',g.op('Subtract_DoubleDouble',(split,'Z'),g.op('Multiply_DoubleDouble',g.v('DoorHeight'),.5)),.7),220))],cat='struct',obj=VEC)
 turned=g.c(MATH,'TransformDirection',[('T','struct',(transform,'ReturnValue')),('Direction','struct',radial)],cat='struct',obj=VEC);turned[0].pins['T']['obj']=TRANSFORM;turned[0].pins['Direction']['obj']=VEC
 velocity=g.c(MATH,'Add_VectorVector',[('A','struct',outward),('B','struct',turned)],cat='struct',obj=VEC)
 for p in ['A','B']:velocity[0].pins[p]['obj']=VEC
 spawn=g.node('K2Node_SpawnActorFromClass').pin('execute').pin('then',out=True).pin('Class','class',obj=ACTOR,default_obj=FRAGMENT).pin('SpawnTransform','struct',obj=TRANSFORM).pin('CollisionHandlingOverride','byte',obj='/Script/Engine.ESpawnActorCollisionHandlingMethod',default='AlwaysSpawn').pin('Owner','object',obj=ACTOR).pin('TransformScaleMethod','byte',obj='/Script/Engine.ESpawnActorScaleMethod',default='MultiplyWithRoot').pin('ShardMesh','object',obj='/Script/Engine.StaticMesh').pin('BreakVelocity','struct',obj=VEC).pin('ReturnValue','object',obj=FRAGMENT,out=True)
 g.chain(loop,spawn,'LoopBody');g.wire(tr,'ReturnValue',spawn,'SpawnTransform');g.wire(loop,'Array Element',spawn,'ShardMesh');g.w(velocity,spawn,'BreakVelocity');g.wire(g.selfnode(typ=ACTOR),'self',spawn,'Owner')

def fragment():
 g=ProgressGraph();e=g.event(ACTOR,'ReceiveBeginPlay');comp=g.v('StaticMeshComponent','object',owner=SM,obj=SMC,native=True,target=(g.selfnode(typ=SM),'self'))
 mesh=g.call(SMC,'SetStaticMesh').pin('NewMesh','object',obj='/Script/Engine.StaticMesh').pin('ReturnValue','bool',out=True);g.w(comp,mesh,'self');g.w(g.v('ShardMesh','object',obj='/Script/Engine.StaticMesh'),mesh,'NewMesh');g.chain(e,mesh)
 n=g.call(PRIM,'SetSimulatePhysics').pin('bSimulate','bool',default='true');g.w(comp,n,'self');g.chain(mesh,n)
 impulse=g.call(PRIM,'AddImpulse').pin('Impulse','struct',obj=VEC).pin('BoneName','name',default='None').pin('bVelChange','bool',default='true');g.w(comp,impulse,'self');g.w(g.v('BreakVelocity','struct',obj=VEC),impulse,'Impulse');g.chain(n,impulse)
 random=g.c(MATH,'RandomUnitVector',cat='struct',obj=VEC);speed=g.c(MATH,'RandomFloatInRange',[('Min','real',180),('Max','real',420)]);spin=g.c(MATH,'Multiply_VectorFloat',[('A','struct',random),('B','real',speed)],cat='struct',obj=VEC);spin[0].pins['A']['obj']=VEC
 angular=g.call(PRIM,'SetPhysicsAngularVelocityInDegrees').pin('NewAngVel','struct',obj=VEC).pin('bAddToCurrent','bool',default='false').pin('BoneName','name',default='None');g.w(comp,angular,'self');g.w(spin,angular,'NewAngVel');g.chain(impulse,angular)
 life=g.call(ACTOR,'SetLifeSpan').pin('InLifespan','real',sub='float',default='4');g.chain(angular,life);g.write('BP_DoorFragment')

if __name__=='__main__':fragment()
