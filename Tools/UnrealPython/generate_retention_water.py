"""La detección se acopla a la superficie colocada y respeta altura y movimiento."""
from generate_progression_graphs import ACTOR, MATH, VEC


def add_water_contact(g, seq, hero, now):
    mesh_actor = '/Script/Engine.StaticMeshActor'
    mid_type = '/Script/Engine.MaterialInstanceDynamic'
    water = g.local('AguaRetencion', mesh_actor)
    mid = g.local('AguaMID', mid_type)
    ready = g.br(seq, (g.valid(*water), 'ReturnValue'), 'then_7')
    ready = g.br(ready, (g.valid(*hero), 'ReturnValue'))
    initialized = g.br(ready, (g.valid(*mid), 'ReturnValue'))
    surface = g.v('StaticMeshComponent', 'object', owner=mesh_actor, target=water,
                  obj='/Script/Engine.StaticMeshComponent', native=True)
    make = g.call('/Script/Engine.PrimitiveComponent', 'CreateDynamicMaterialInstance').pin('ElementIndex','int',default='0').pin('ReturnValue','object',obj=mid_type,out=True)
    g.w(surface, make, 'self')
    g.chain(initialized, make, 'else')
    g.s(make, 'AguaMID', (make,'ReturnValue'), 'object', obj=mid_type)
    position = (g.location(*hero), 'ReturnValue')
    center = (g.location(*water), 'ReturnValue')
    feet = g.c(MATH,'Add_VectorVector',[('A','struct',position),('B','struct','0,0,-90')],cat='struct',obj=VEC)
    feet[0].pins['A']['obj'] = feet[0].pins['B']['obj'] = VEC
    radius = g.c(MATH,'Vector_Distance2D',[('V1','struct',feet),('V2','struct',center)])
    radius[0].pins['V1']['obj'] = radius[0].pins['V2']['obj'] = VEC
    def z(value):
        n=g.call(MATH,'BreakVector',pure=True,static=True).pin('InVec','struct',obj=VEC).pin('Z','real',sub='double',out=True)
        g.w(value,n,'InVec')
        return n,'Z'
    depth = g.op('Subtract_DoubleDouble', z(center), z(feet))
    inside = g.both(g.cmp('LessEqual_DoubleDouble',radius,285),g.both(g.cmp('GreaterEqual_DoubleDouble',depth,-3),g.cmp('Less_DoubleDouble',depth,65)))
    wet = g.br(initialized,inside)
    left = g.br(wet,g.v('PiesEnAgua','bool'),'else')
    g.s(left,'PiesEnAgua',False,'bool')
    velocity = g.c(ACTOR,'GetVelocity',cat='struct',obj=VEC,static=False)
    g.w(hero,velocity[0],'self')
    speed = g.c(MATH,'VSizeXY',[('A','struct',velocity)])
    speed[0].pins['A']['obj']=VEC
    step = g.both(g.cmp('Greater_DoubleDouble',speed,15),g.cmp('GreaterEqual_DoubleDouble',now,g.v('ProximaOnda')))
    trigger = g.br(wet,g.c('/Script/Engine.KismetMathLibrary','BooleanOR',[('A','bool',g.neg(g.v('PiesEnAgua','bool'))),('B','bool',step)],cat='bool'))
    prev = g.s(trigger,'PiesEnAgua',True,'bool')
    prev = g.s(prev,'ProximaOnda',g.op('Add_DoubleDouble',now,.65))
    color = g.c(MATH,'Conv_VectorToLinearColor',[('InVec','struct',feet)],cat='struct',obj='/Script/CoreUObject.LinearColor')
    color[0].pins['InVec']['obj']=VEC
    prev = g.action_on(prev,mid_type,'SetVectorParameterValue',mid,[('ParameterName','name','Origen',None),('Value','struct',color,'/Script/CoreUObject.LinearColor')])
    g.action_on(prev,mid_type,'SetScalarParameterValue',mid,[('ParameterName','name','Inicio',None),('Value','real',now,None)])
