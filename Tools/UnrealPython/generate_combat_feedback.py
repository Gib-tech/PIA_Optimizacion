"""Arrival-first enemy strikes and feedback from actual health loss. Blueprint only."""
from generate_progression_graphs import ProgressGraph, capture, MATH, GS, VEC
from generate_combat_graphs import BASE, ACTOR, CHAR, CONTROLLER, HEALTH

HUD='/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega.BP_HUD_Entrega_C'
ANIM='/Script/Engine.AnimInstance'

def detach(g,node,pin='then'):
    links=[]
    for name,pid in list(node.pins[pin]['links']):
        other=next(n for n in g.nodes if n.name==name)
        otherpin=next(p for p in other.pins.values() if p['id']==pid)
        otherpin['links'].remove((node.name,node.pins[pin]['id']))
        links.append((other,otherpin['name']))
    node.pins[pin]['links']=[]
    return links

def reconnect(g,prev,links,pin='then'):
    for node,destination in links:g.chain(prev,node,pin,destination)

def base_enemy():
    from generate_combat_graphs import legacy_base_enemy
    g=capture(legacy_base_enemy);g.__class__=ProgressGraph
    own=(g.selfnode(),'self');hp=g.v('E_Health',owner=HEALTH,target=g.v('BPC_E_Health','object',obj=HEALTH))
    begin=next(n for n in g.nodes if any('MemberName="ReceiveBeginPlay"' in p for p in n.props))
    links=detach(g,begin);reconnect(g,g.s(begin,'LastFeedbackHealth',hp),links)
    # Reject distant requests even if called directly, independently of the tree.
    attack=next(n for n in g.nodes if any('MemberName="Attack"' in p for p in n.props))
    gate=next(n for n in g.nodes if n.name==attack.pins['then']['links'][0][0])
    source_name,source_id=gate.pins['Condition']['links'][0]
    source=next(n for n in g.nodes if n.name==source_name)
    source_pin=next(p for p in source.pins.values() if p['id']==source_id)
    source_pin['links'].remove((gate.name,gate.pins['Condition']['id']));gate.pins['Condition']['links']=[]
    target=(attack,'TargetActor');ctrl=(g.ctrl(*own),'ReturnValue')
    near=g.cmp('LessEqual_DoubleDouble',(g.dist(*own,*target),'ReturnValue'),220)
    allowed=g.both((source,source_pin['name']),g.both((g.valid(*target),'ReturnValue'),g.both(near,(g.sight(*ctrl,*target),'ReturnValue'))))
    g.w(allowed,gate,'Condition')
    flag=next(n for n in g.nodes if n.kind.endswith('K2Node_VariableSet') and 'bAttackInProgress' in n.pins and n.pins['bAttackInProgress']['default']=='true')
    links=detach(g,flag);prev=g.s(flag,'bAttackResolved',False,'bool')
    stop=g.call('/Script/Engine.Controller','StopMovement');g.w(ctrl,stop,'self');g.chain(prev,stop);reconnect(g,stop,links)
    # Consume exactly one attempt, including a dodge/miss. Never defer a hit until approach.
    resolve=next(n for n in g.nodes if any('CustomFunctionName="ResolveAttack"' in p for p in n.props))
    links=detach(g,resolve)
    mesh=g.v('Mesh','object',owner=CHAR,obj='/Script/Engine.SkeletalMeshComponent',target=own,native=True)
    anim=g.call('/Script/Engine.SkeletalMeshComponent','GetAnimInstance',pure=True).pin('ReturnValue','object',obj=ANIM,out=True);g.w(mesh,anim,'self')
    montage='/Game/ThirdPerson/Blueprints/EnemigoIA/AM_EnemyAttack_Entrega.AM_EnemyAttack_Entrega'
    position=g.call(ANIM,'Montage_GetPosition',pure=True).pin('Montage','object',obj='/Script/Engine.AnimMontage',default_obj=montage).pin('ReturnValue','real',sub='float',out=True);g.w((anim,'ReturnValue'),position,'self')
    playing=g.call(ANIM,'Montage_IsPlaying',pure=True).pin('Montage','object',obj='/Script/Engine.AnimMontage',default_obj=montage).pin('ReturnValue','bool',out=True);g.w((anim,'ReturnValue'),playing,'self')
    window=g.both(g.cmp('GreaterEqual_DoubleDouble',(position,'ReturnValue'),.30),g.cmp('LessEqual_DoubleDouble',(position,'ReturnValue'),.70))
    check=g.br(resolve,g.both(g.neg(g.v('bAttackResolved','bool')),g.both((playing,'ReturnValue'),window)))
    used=g.s(check,'bAttackResolved',True,'bool');reconnect(g,used,links)
    # OnHealthChanged runs for both damage and healing; confirm only actual loss.
    changed=next(n for n in g.nodes if any('CustomFunctionName="OnHealthChanged"' in p for p in n.props))
    links=detach(g,changed)
    lost=g.br(changed,g.cmp('Less_DoubleDouble',hp,g.v('LastFeedbackHealth')))
    pc=g.call(GS,'GetPlayerController',pure=True,static=True).pin('PlayerIndex','int',default='0').pin('ReturnValue','object',obj='/Script/Engine.PlayerController',out=True)
    hud=g.call('/Script/Engine.PlayerController','GetHUD',pure=True).pin('ReturnValue','object',obj='/Script/Engine.HUD',out=True);g.w((pc,'ReturnValue'),hud,'self')
    cast=g.cast(HUD);g.chain(lost,cast);g.w((hud,'ReturnValue'),cast,'Object');hudtarget=(cast,'AsBP_HUD_Entrega')
    now=g.c(GS,'GetRealTimeSeconds')
    prev=g.s(cast,'EnemyHitUntil',g.op('Add_DoubleDouble',now,.18),owner=HUD,target=hudtarget)
    prev=g.s(prev,'LastEnemyDamage',g.op('Subtract_DoubleDouble',g.v('LastFeedbackHealth'),hp),owner=HUD,target=hudtarget)
    impact=g.sound(prev,'DoorHit');impact.pins['VolumeMultiplier']['default']='.3';impact.pins['PitchMultiplier']['default']='1.3'
    saved=g.s(impact,'LastFeedbackHealth',hp);g.chain(lost,saved,'else');g.chain(cast,saved,'CastFailed');reconnect(g,saved,links)
    g.write('BP_BaseEnemy')

def windup():
    g=ProgressGraph();e=g.task_event('ReceiveExecuteAI');tick=g.task_event('ReceiveTickAI');abort=g.task_event('ReceiveAbortAI')
    bb=g.blackboard(e,'OwnerController');target=g.target_actor()
    stop=g.stop_move(e);g.chain(e,stop);prev=g.s(stop,'Elapsed',0)
    focus=g.call(CONTROLLER,'K2_SetFocus').pin('NewFocus','object',obj=ACTOR);g.wire(e,'OwnerController',focus,'self');g.wire(target,'CombatTarget',focus,'NewFocus');g.chain(prev,focus)
    face=g.face_target(focus,e,target,'CombatTarget')
    # Hold facing for the telegraph. Locomotion remains idle; no remote punch montage.
    cue=g.sound(face,'Alert');cue.pins['VolumeMultiplier']['default']='.12'
    elapsed=g.elapsed(tick);ready=g.br(elapsed,g.cmp('GreaterEqual_DoubleDouble',(elapsed,'Output_Get'),.8))
    valid=g.br(ready,(g.valid(target,'CombatTarget'),'ReturnValue'));g.finish(valid,'else',success=False)
    goal=g.bbset(bb,'ChargeGoal','Vector');g.w((g.location(target,'CombatTarget'),'ReturnValue'),goal,'VectorValue');g.chain(valid,goal)
    prev=g.s(goal,'ChargeVictim',(target,'CombatTarget'),'object',owner=BASE,target=g.v('CachedPawn','object',obj=BASE),obj=ACTOR)
    charging=g.bbset(bb,'bCharging','Bool','true');g.chain(prev,charging);g.finish(charging)
    g.finish(abort,abort=True);g.write('BTTask_ChargerWindup')

def charge():
    g=ProgressGraph();e=g.task_event('ReceiveExecuteAI');tick=g.task_event('ReceiveTickAI');abort=g.task_event('ReceiveAbortAI')
    pawn=g.v('CachedPawn','object',obj=BASE);target=g.v('ChargeVictim','object',owner=BASE,obj=ACTOR,target=pawn)
    bb=g.blackboard(e,'OwnerController');goal=g.bbget(bb,'ChargeGoal','Vector')
    prev=g.s(e,'Elapsed',0);prev=g.s(prev,'bHit',False,'bool');prev=g.s(prev,'bAttackStarted',False,'bool')
    speed=g.speed(e,'900');g.chain(prev,speed)
    clear=g.call(CONTROLLER,'K2_ClearFocus');g.wire(e,'OwnerController',clear,'self');g.chain(speed,clear)
    move=g.move_to(e,goal,'ReturnValue',path=False,radius='40');g.chain(clear,move)
    elapsed=g.elapsed(tick);started=g.br(elapsed,g.v('bAttackStarted','bool'))
    live=g.both((g.valid(*target),'ReturnValue'),g.neg(g.v('bIsDead','bool',owner=BASE,target=pawn)))
    distance=(g.dist(*pawn,*target),'ReturnValue')
    contact=g.both(live,g.both(g.cmp('LessEqual_DoubleDouble',distance,180),(g.sight(tick,'OwnerController',*target),'ReturnValue')))
    arrival=g.br(started,contact,'else')
    stop=g.stop_move(tick);g.chain(arrival,stop)
    face=g.face_target(stop,tick,target[0],target[1])
    attack=g.action('Attack').pin('TargetActor','object',obj=ACTOR);g.w(pawn,attack,'self');g.w(target,attack,'TargetActor');g.chain(face,attack)
    prev=g.s(attack,'bAttackStarted',True,'bool');g.s(prev,'Elapsed',0)
    timeout=g.br(arrival,g.cmp('GreaterEqual_DoubleDouble',(elapsed,'Output_Get'),1.0),'else')
    strike=g.br(started,g.both(g.neg(g.v('bHit','bool')),g.cmp('GreaterEqual_DoubleDouble',(elapsed,'Output_Get'),.45)))
    used=g.s(strike,'bHit',True,'bool');resolve=g.action('ResolveAttack');g.w(pawn,resolve,'self');g.chain(used,resolve)
    finished=g.br(resolve,g.cmp('GreaterEqual_DoubleDouble',(elapsed,'Output_Get'),1.3));g.chain(strike,finished,'else')
    for start,event,isabort in [(finished,tick,False),(timeout,tick,False),(abort,abort,True)]:
        stop=g.stop_move(event);g.chain(start,stop)
        end=g.action('EndAttack');g.w(pawn,end,'self');g.chain(stop,end)
        speed=g.speed(event,'600');g.chain(end,speed)
        clear=g.bbset(bb,'bCharging','Bool','false');g.chain(speed,clear)
        retreat=g.bbset(bb,'bRetreat','Bool','true');g.chain(clear,retreat);g.finish(retreat,abort=isabort)
    g.write('BTTask_ChargerCharge')

if __name__=='__main__':base_enemy();windup();charge()
