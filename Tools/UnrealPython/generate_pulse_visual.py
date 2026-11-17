"""Frente de energía que recorre el trazo y se abre al llegar a su extremo."""
from generate_delivery_controls import ControlsGraph
from generate_progression_graphs import ACTOR, GS, VEC

BEAM = '/Script/Engine.StaticMeshActor'
SPRITE = '/Script/Engine.MaterialBillboardComponent'


def build():
    g = ControlsGraph()
    begin = g.event(ACTOR, 'ReceiveBeginPlay')
    mesh = g.v('StaticMeshComponent', 'object', owner=BEAM, native=True,
               target=(g.selfnode(typ=BEAM), 'self'), obj='/Script/Engine.StaticMeshComponent')
    front = g.v('Frente', 'object', obj=SPRITE)
    time = g.c(GS, 'GetTimeSeconds')
    previous = begin
    for component in (mesh, front):
        previous = g.action_on(previous, '/Script/Engine.PrimitiveComponent',
                               'SetCustomPrimitiveDataFloat', component,
                               [('DataIndex', 'int', 0, None), ('Value', 'real', time, None)])
    # El cubo mide 100 cm en espacio local. Termina justo delante de la superficie.
    move = g.call('/Script/Engine.KismetSystemLibrary', 'MoveComponentTo', static=True)
    move.pin('Component', 'object', obj='/Script/Engine.SceneComponent')
    move.pin('TargetRelativeLocation', 'struct', obj=VEC, default='49,0,0')
    move.pin('TargetRelativeRotation', 'struct', obj='/Script/CoreUObject.Rotator', default='0,0,0')
    move.pin('OverTime', 'real', sub='float', default='.18')
    del move.pins['execute']
    move.pin('Move')
    g.w(front, move, 'Component')
    g.chain(previous, move, nextpin='Move')
    g.write('BP_PulsoTemporalVisual')


if __name__ == '__main__':
    build()
