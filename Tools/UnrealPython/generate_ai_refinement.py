"""Localized charger recovery. Emits normal Blueprint nodes; no runtime Python."""
from generate_progression_graphs import ProgressGraph, MATH, ACTOR, VEC
from generate_combat_graphs import CombatGraph, BASE, CONTROLLER


def face_target():
    g=CombatGraph();e=g.task_event('ReceiveExecuteAI');abort=g.task_event('ReceiveAbortAI')
    target=g.target_actor();valid=g.valid(target,'CombatTarget');b=g.branch();g.wire(valid,'ReturnValue',b,'Condition');g.chain(e,b)
    face=g.face_target(b,e,target,'CombatTarget');g.finish(face)
    g.finish(b,'else',success=False);g.finish(abort,abort=True)
    g.write('BTTask_FaceCombatTarget')

def retreat():
    g=ProgressGraph()
    e=g.task_event('ReceiveExecuteAI');tick=g.task_event('ReceiveTickAI');abort=g.task_event('ReceiveAbortAI')
    pawn=g.v('CachedPawn','object',obj=BASE)
    # Retreat remains local to the player, including the first service interval
    # before CombatTarget has been populated.
    player=g.player();target=(player,'ReturnValue')
    start=(g.location(e,'ControlledPawn'),'ReturnValue')
    end=(g.location(*target),'ReturnValue')
    def vector(fn,a,b):
        v=g.c(MATH,fn,[('A','struct',a),('B','struct',b)],cat='struct',obj=VEC)
        v[0].pins['A']['obj']=VEC;v[0].pins['B']['obj']=VEC;return v
    away=vector('Subtract_VectorVector',start,end)
    direction=g.c(MATH,'Vector_Normal2D',[('A','struct',away),('Tolerance','real',.0001)],cat='struct',obj=VEC);direction[0].pins['A']['obj']=VEC
    prev=g.s(e,'Elapsed',0)
    # Focus from windup must not make the recovery walk run backwards.
    clear=g.call(CONTROLLER,'K2_ClearFocus');g.wire(e,'OwnerController',clear,'self');g.chain(prev,clear)
    prev=g.speed(e,'400');g.chain(clear,prev)
    prev=g.s(prev,'BestDistance',100000)
    prev=g.s(prev,'RetreatGoal',start,'struct',obj=VEC)
    # A small local fan, full paths <=650 cm, never remote hostage refuge actors.
    for angle in [0,45,-45,90,-90]:
        rotated=g.c(MATH,'RotateAngleAxis',[('InVect','struct',direction),('AngleDeg','real',angle),('Axis','struct','0,0,1')],cat='struct',obj=VEC)
        for p in ['InVect','Axis']:rotated[0].pins[p]['obj']=VEC
        offset=g.c(MATH,'Multiply_VectorFloat',[('A','struct',rotated),('B','real',420)],cat='struct',obj=VEC);offset[0].pins['A']['obj']=VEC
        goal=vector('Add_VectorVector',start,offset)
        path=g.call('/Script/NavigationSystem.NavigationSystemV1','FindPathToLocationSynchronously',static=True).pin('WorldContextObject','object',obj='/Script/CoreUObject.Object',hidden=True).pin('PathStart','struct',obj=VEC).pin('PathEnd','struct',obj=VEC).pin('PathfindingContext','object',obj=ACTOR).pin('FilterClass','class',obj='/Script/NavigationSystem.NavigationQueryFilter').pin('ReturnValue','object',obj='/Script/NavigationSystem.NavigationPath',out=True)
        g.wire(e,'OwnerController',path,'WorldContextObject')
        g.w(start,path,'PathStart');g.w(goal,path,'PathEnd');g.wire(e,'ControlledPawn',path,'PathfindingContext');g.chain(prev,path)
        valid=g.call('/Script/NavigationSystem.NavigationPath','IsValid',pure=True).pin('ReturnValue','bool',out=True);g.wire(path,'ReturnValue',valid,'self')
        partial=g.call('/Script/NavigationSystem.NavigationPath','IsPartial',pure=True).pin('ReturnValue','bool',out=True);g.wire(path,'ReturnValue',partial,'self')
        length=g.call('/Script/NavigationSystem.NavigationPath','GetPathLength',pure=True).pin('ReturnValue','real',sub='float',out=True);g.wire(path,'ReturnValue',length,'self')
        distance=g.c(MATH,'Vector_Distance2D',[('V1','struct',goal),('V2','struct',end)])
        for p in ['V1','V2']:distance[0].pins[p]['obj']=VEC
        score=g.c(MATH,'Abs',[('A','real',g.op('Subtract_DoubleDouble',distance,550))])
        ok=g.both((valid,'ReturnValue'),g.neg((partial,'ReturnValue')))
        ok=g.both(ok,g.cmp('LessEqual_DoubleDouble',(length,'ReturnValue'),650))
        ok=g.both(ok,g.both(g.cmp('GreaterEqual_DoubleDouble',distance,300),g.cmp('Less_DoubleDouble',score,g.v('BestDistance'))))
        b=g.br(path,ok);save=g.s(b,'RetreatGoal',goal,'struct',obj=VEC);save=g.s(save,'BestDistance',score)
        merge=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True)
        g.chain(save,merge);g.chain(b,merge,'else');prev=merge
        # Uniform continuation pin for the next candidate.
        merge.pins['then']=merge.pins.pop('then_0');merge.pins['then']['name']='then_0'
    goal=g.v('RetreatGoal','struct',obj=VEC)
    move=g.move_to(e,goal[0],goal[1],radius='55');g.chain(prev,move)
    elapsed=g.elapsed(tick)
    distance=g.c(MATH,'Vector_Distance2D',[('V1','struct',(g.location(tick,'ControlledPawn'),'ReturnValue')),('V2','struct',goal)])
    for p in ['V1','V2']:distance[0].pins[p]['obj']=VEC
    finish=g.br(elapsed,g.both(g.cmp('GreaterEqual_DoubleDouble',(elapsed,'Output_Get'),.2),g.both(g.cmp('LessEqual_DoubleDouble',distance,90),g.cmp('Less_DoubleDouble',g.v('BestDistance'),100000))))
    expired=g.br(finish,g.cmp('GreaterEqual_DoubleDouble',(elapsed,'Output_Get'),1.4),'else')
    stop=g.stop_move(tick);g.chain(finish,stop);g.chain(expired,stop)
    normal=g.speed(tick,'600');g.chain(stop,normal);g.finish(normal)
    stop=g.stop_move(abort);g.chain(abort,stop);normal=g.speed(abort,'600');g.chain(stop,normal);g.finish(normal,abort=True)
    CombatGraph.write(g,'BTTask_ChargerRetreat')

if __name__=='__main__':retreat();face_target()
