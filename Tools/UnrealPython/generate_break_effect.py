"""Un actor por ráfaga. Su destrucción retira también los emisores en bucle."""
from generate_progression_graphs import ACTOR, GS, MATH, VEC

BURST='/Game/ThirdPerson/Blueprints/Entrega/FX/BP_RafagaRotura.BP_RafagaRotura_C'

def build_burst():
    from generate_delivery_controls import ControlsGraph
    g=ControlsGraph()
    begin=g.event(ACTOR,'ReceiveBeginPlay')
    sprite=g.v('Destellos','object',obj='/Script/Engine.MaterialBillboardComponent')
    g.action_on(begin,'/Script/Engine.PrimitiveComponent','SetCustomPrimitiveDataFloat',sprite,
                [('DataIndex','int',0,None),('Value','real',g.c(GS,'GetTimeSeconds'),None)])
    g.write('BP_RafagaRotura')

def burst(g, previous, position, system):
    actor_type='/Script/Niagara.NiagaraActor'
    component_type='/Script/Niagara.NiagaraComponent'
    transform_type='/Script/CoreUObject.Transform'
    transform=g.c(MATH,'MakeTransform',[('Location','struct',position),('Scale','struct','.55,.55,.55')],cat='struct',obj=transform_type)
    for pin in ['Location','Scale']:
        transform[0].pins[pin]['obj']=VEC
    spawn=g.node('K2Node_SpawnActorFromClass').pin('execute').pin('then',out=True)
    spawn.pin('Class','class',obj=ACTOR,default_obj=BURST).pin('SpawnTransform','struct',obj=transform_type)
    spawn.pin('CollisionHandlingOverride','byte',obj='/Script/Engine.ESpawnActorCollisionHandlingMethod',default='AlwaysSpawn')
    spawn.pin('ReturnValue','object',obj=BURST,out=True)
    g.w(transform,spawn,'SpawnTransform');g.chain(previous,spawn)
    lifetime=g.call(ACTOR,'SetLifeSpan').pin('InLifespan','real',sub='float',default='.65')
    g.w((spawn,'ReturnValue'),lifetime,'self');g.chain(spawn,lifetime)
    component=g.v('NiagaraComponent','object',owner=actor_type,target=(spawn,'ReturnValue'),native=True,obj=component_type)
    apply=g.call(component_type,'SetAsset').pin('InAsset','object',obj='/Script/Niagara.NiagaraSystem')
    if isinstance(system,str):
        apply.pins['InAsset']['default_obj']=system
    else:
        g.w(system,apply,'InAsset')
    g.w(component,apply,'self');g.chain(lifetime,apply)
    return apply
