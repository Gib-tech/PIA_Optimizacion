"""Smooth approach/alignment and short repositioning, emitted as ordinary Blueprint nodes."""
from generate_progression_graphs import ProgressGraph,MATH,GS,VEC
from generate_combat_graphs import BASE,ACTOR,CONTROLLER,CHAR
ROT='/Script/CoreUObject.Rotator'

def facing_dot(g,pawn,target):
    delta=g.c(MATH,'Subtract_VectorVector',[('A','struct',(g.location(*target),'ReturnValue')),('B','struct',(g.location(*pawn),'ReturnValue'))],cat='struct',obj=VEC)
    for pin in ['A','B']:delta[0].pins[pin]['obj']=VEC
    direction=g.c(MATH,'Vector_Normal2D',[('A','struct',delta),('Tolerance','real',.0001)],cat='struct',obj=VEC);direction[0].pins['A']['obj']=VEC
    forward=g.call(ACTOR,'GetActorForwardVector',pure=True).pin('ReturnValue','struct',obj=VEC,out=True);g.w(pawn,forward,'self')
    dot=g.c(MATH,'Dot_VectorVector',[('A','struct',(forward,'ReturnValue')),('B','struct',direction)])
    for pin in ['A','B']:dot[0].pins[pin]['obj']=VEC
    return dot

def turn_toward(g,prev,pawn,target,dt,rate=420):
    current=g.call(ACTOR,'K2_GetActorRotation',pure=True).pin('ReturnValue','struct',obj=ROT,out=True);g.w(pawn,current,'self')
    wanted=g.c(MATH,'FindLookAtRotation',[('Start','struct',(g.location(*pawn),'ReturnValue')),('Target','struct',(g.location(*target),'ReturnValue'))],cat='struct',obj=ROT)
    for pin in ['Start','Target']:wanted[0].pins[pin]['obj']=VEC
    split=g.call(MATH,'BreakRotator',pure=True,static=True).pin('InRot','struct',obj=ROT).pin('Yaw','real',sub='double',out=True);g.w(wanted,split,'InRot')
    wanted=g.c(MATH,'MakeRotator',[('Roll','real',0),('Pitch','real',0),('Yaw','real',(split,'Yaw'))],cat='struct',obj=ROT)
    # BT tasks can receive an accumulated first delta after being inactive.
    # Bound that step so entering a task never snaps the capsule around.
    step=g.op('FMin',dt,.033)
    rotation=g.c(MATH,'RInterpTo_Constant',[('Current','struct',(current,'ReturnValue')),('Target','struct',wanted),('DeltaTime','real',step),('InterpSpeed','real',rate)],cat='struct',obj=ROT)
    for pin in ['Current','Target']:rotation[0].pins[pin]['obj']=ROT
    setrot=g.call(ACTOR,'K2_SetActorRotation').pin('NewRotation','struct',obj=ROT).pin('bTeleportPhysics','bool',default='false').pin('ReturnValue','bool',out=True)
    g.w(pawn,setrot,'self');g.w(rotation,setrot,'NewRotation');g.chain(prev,setrot);return setrot

def focus(g,prev,event,target):
    node=g.call(CONTROLLER,'K2_SetFocus').pin('NewFocus','object',obj=ACTOR);g.wire(event,'OwnerController',node,'self');g.w(target,node,'NewFocus');g.chain(prev,node);return node

def melee_task():
    g=ProgressGraph();e=g.task_event('ReceiveExecuteAI');tick=g.task_event('ReceiveTickAI');abort=g.task_event('ReceiveAbortAI')
    pawn=g.v('CachedPawn','object',obj=BASE)
    prev=g.s(e,'StrikeTarget',(g.target_actor(),'CombatTarget'),'object',obj=ACTOR)
    target=g.v('StrikeTarget','object',obj=ACTOR)
    prev=g.s(prev,'Elapsed',0);prev=g.s(prev,'RepathAt',0);prev=g.s(prev,'bAttackStarted',False,'bool');focus(g,prev,e,target)
    age=g.elapsed(tick);started=g.br(age,g.v('bAttackStarted','bool'))
    timeout=g.br(started,g.cmp('GreaterEqual_DoubleDouble',(age,'Output_Get'),1.5),'else')
    near=g.br(timeout,g.cmp('LessEqual_DoubleDouble',(g.dist(*pawn,*target),'ReturnValue'),150),'else')
    stop=g.stop_move(tick);g.chain(near,stop)
    turned=turn_toward(g,stop,pawn,target,(tick,'DeltaSeconds'))
    aligned=g.br(turned,g.cmp('GreaterEqual_DoubleDouble',facing_dot(g,pawn,target),.6))
    attack=g.action('Attack').pin('TargetActor','object',obj=ACTOR);g.w(pawn,attack,'self');g.w(target,attack,'TargetActor');g.chain(aligned,attack)
    accepted=g.br(attack,g.v('bAttackInProgress','bool',owner=BASE,target=pawn))
    mark=g.s(accepted,'bAttackStarted',True,'bool');g.s(mark,'Elapsed',0)
    replan=g.br(near,g.cmp('GreaterEqual_DoubleDouble',(age,'Output_Get'),g.v('RepathAt')),'else')
    speed=g.speed(tick,'520');g.chain(replan,speed)
    location=g.location(*target);move=g.move_to(tick,location,'ReturnValue',radius='35');g.chain(speed,move)
    g.s(move,'RepathAt',g.op('Add_DoubleDouble',(age,'Output_Get'),.18))
    update=g.action('UpdateStrike').pin('DeltaSeconds','real',sub='float');g.w(pawn,update,'self');g.wire(tick,'DeltaSeconds',update,'DeltaSeconds');g.chain(started,update)
    finished=g.br(update,g.cmp('GreaterEqual_DoubleDouble',(age,'Output_Get'),1.12))
    for prev,event,isabort,success in [(finished,tick,False,True),(timeout,tick,False,False),(abort,abort,True,False)]:
        stop=g.stop_move(event);g.chain(prev,stop)
        end=g.action('EndAttack');g.w(pawn,end,'self');g.chain(stop,end);g.finish(end,abort=isabort,success=success)
    g.write('BTTask_Attack')

def defend():
    g=ProgressGraph();e=g.task_event('ReceiveExecuteAI');tick=g.task_event('ReceiveTickAI');abort=g.task_event('ReceiveAbortAI')
    target=(g.target_actor(),'CombatTarget');bb=g.blackboard(e,'OwnerController')
    prev=g.s(e,'Elapsed',0);focused=focus(g,prev,e,target)
    speed=g.speed(e,'230');g.chain(focused,speed)
    goal=g.bbget(bb,'OrbitLocation','Vector');move=g.move_to(e,goal,'ReturnValue',radius='30');g.chain(speed,move)
    age=g.elapsed(tick);end=g.br(age,g.cmp('GreaterEqual_DoubleDouble',(age,'Output_Get'),.65))
    for prev,event,isabort in [(end,tick,False),(abort,abort,True)]:
        stop=g.stop_move(event);g.chain(prev,stop);g.finish(stop,abort=isabort)
    g.write('BTTask_Defend')

def face_target():
    g=ProgressGraph();e=g.task_event('ReceiveExecuteAI');abort=g.task_event('ReceiveAbortAI')
    target=(g.target_actor(),'CombatTarget');valid=g.br(e,(g.valid(*target),'ReturnValue'))
    focused=focus(g,valid,e,target);g.finish(focused);g.finish(valid,'else',success=False);g.finish(abort,abort=True)
    g.write('BTTask_FaceCombatTarget')

def predicted_position(g,target):
    velocity=g.call(ACTOR,'GetVelocity',pure=True).pin('ReturnValue','struct',obj=VEC,out=True);g.w(target,velocity,'self')
    lead=g.c(MATH,'Multiply_VectorFloat',[('A','struct',(velocity,'ReturnValue')),('B','real',.18)],cat='struct',obj=VEC);lead[0].pins['A']['obj']=VEC
    point=g.c(MATH,'Add_VectorVector',[('A','struct',(g.location(*target),'ReturnValue')),('B','struct',lead)],cat='struct',obj=VEC)
    for pin in ['A','B']:point[0].pins[pin]['obj']=VEC
    return point

def windup_task():
    g=ProgressGraph();e=g.task_event('ReceiveExecuteAI');tick=g.task_event('ReceiveTickAI');abort=g.task_event('ReceiveAbortAI')
    pawn=g.v('CachedPawn','object',obj=BASE);target=(g.target_actor(),'CombatTarget');bb=g.blackboard(e,'OwnerController')
    stop=g.stop_move(e);g.chain(e,stop);prev=g.s(stop,'Elapsed',0);focus(g,prev,e,target)
    age=g.elapsed(tick);turn=turn_toward(g,age,pawn,target,(tick,'DeltaSeconds'),360)
    ready=g.br(turn,g.cmp('GreaterEqual_DoubleDouble',(age,'Output_Get'),.65))
    valid=g.br(ready,g.both((g.valid(*target),'ReturnValue'),(g.sight(e,'OwnerController',*target),'ReturnValue')))
    g.finish(valid,'else',success=False)
    goal=g.bbset(bb,'ChargeGoal','Vector');g.w(predicted_position(g,target),goal,'VectorValue');g.chain(valid,goal)
    prev=g.s(goal,'ChargeVictim',target,'object',owner=BASE,target=pawn,obj=ACTOR)
    charging=g.bbset(bb,'bCharging','Bool','true');g.chain(prev,charging);g.finish(charging);g.finish(abort,abort=True)
    g.write('BTTask_ChargerWindup')

def charge_task():
    g=ProgressGraph();e=g.task_event('ReceiveExecuteAI');tick=g.task_event('ReceiveTickAI');abort=g.task_event('ReceiveAbortAI')
    pawn=g.v('CachedPawn','object',obj=BASE);target=g.v('ChargeVictim','object',owner=BASE,target=pawn,obj=ACTOR);bb=g.blackboard(e,'OwnerController')
    mesh=g.v('Mesh','object',owner=CHAR,obj='/Script/Engine.SkeletalMeshComponent',target=pawn,native=True)
    prev=g.s(e,'Elapsed',0);prev=g.s(prev,'RepathAt',.18);prev=g.s(prev,'bAttackStarted',False,'bool')
    prev=g.s(prev,'GlobalAnimRateScale',1.35,owner='/Script/Engine.SkeletalMeshComponent',target=mesh)
    speed=g.speed(e,'900');g.chain(prev,speed)
    goal=g.bbget(bb,'ChargeGoal','Vector');move=g.move_to(e,goal,'ReturnValue',path=True,radius='60');g.chain(speed,move)
    age=g.elapsed(tick);started=g.br(age,g.v('bAttackStarted','bool'))
    timeout=g.br(started,g.cmp('GreaterEqual_DoubleDouble',(age,'Output_Get'),1.5),'else')
    near=g.br(timeout,g.both(g.cmp('LessEqual_DoubleDouble',(g.dist(*pawn,*target),'ReturnValue'),150),(g.sight(tick,'OwnerController',*target),'ReturnValue')),'else')
    stop=g.stop_move(tick);g.chain(near,stop)
    rate=g.s(stop,'GlobalAnimRateScale',1,owner='/Script/Engine.SkeletalMeshComponent',target=mesh)
    turn=turn_toward(g,rate,pawn,target,(tick,'DeltaSeconds'),480)
    aligned=g.br(turn,g.cmp('GreaterEqual_DoubleDouble',facing_dot(g,pawn,target),.6))
    attack=g.action('Attack').pin('TargetActor','object',obj=ACTOR);g.w(pawn,attack,'self');g.w(target,attack,'TargetActor');g.chain(aligned,attack)
    accepted=g.br(attack,g.v('bAttackInProgress','bool',owner=BASE,target=pawn));prev=g.s(accepted,'bAttackStarted',True,'bool');g.s(prev,'Elapsed',0)
    can_repath=g.both(g.cmp('LessEqual_DoubleDouble',(age,'Output_Get'),.45),g.cmp('GreaterEqual_DoubleDouble',(age,'Output_Get'),g.v('RepathAt')))
    replan=g.br(near,can_repath,'else');point=predicted_position(g,target)
    move=g.move_to(tick,*point,path=True,radius='60');g.chain(replan,move);g.s(move,'RepathAt',g.op('Add_DoubleDouble',(age,'Output_Get'),.18))
    update=g.action('UpdateStrike').pin('DeltaSeconds','real',sub='float');g.w(pawn,update,'self');g.wire(tick,'DeltaSeconds',update,'DeltaSeconds');g.chain(started,update)
    finished=g.br(update,g.cmp('GreaterEqual_DoubleDouble',(age,'Output_Get'),1.18))
    for prev,event,isabort in [(timeout,tick,False),(finished,tick,False),(abort,abort,True)]:
        stop=g.stop_move(event);g.chain(prev,stop)
        rate=g.s(stop,'GlobalAnimRateScale',1,owner='/Script/Engine.SkeletalMeshComponent',target=mesh)
        end=g.action('EndAttack');g.w(pawn,end,'self');g.chain(rate,end)
        speed=g.speed(event,'600');g.chain(end,speed)
        clear=g.bbset(bb,'bCharging','Bool','false');g.chain(speed,clear)
        retreat=g.bbset(bb,'bRetreat','Bool','true');g.chain(clear,retreat);g.finish(retreat,abort=isabort)
    g.write('BTTask_ChargerCharge')

if __name__=='__main__':melee_task();defend();face_target();windup_task();charge_task()
