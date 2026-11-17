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
    near=g.cmp('LessEqual_DoubleDouble',(g.dist(*own,*target),'ReturnValue'),160)
    now=g.c(GS,'GetTimeSeconds')
    recovered=g.cmp('GreaterEqual_DoubleDouble',now,g.v('NextAttackAt'))
    allowed=g.both(recovered,g.both((source,source_pin['name']),g.both((g.valid(*target),'ReturnValue'),g.both(near,(g.sight(*ctrl,*target),'ReturnValue')))))
    g.w(allowed,gate,'Condition')
    flag=next(n for n in g.nodes if n.kind.endswith('K2Node_VariableSet') and 'bAttackInProgress' in n.pins and n.pins['bAttackInProgress']['default']=='true')
    links=detach(g,flag);prev=g.s(flag,'bAttackResolved',False,'bool')
    prev=g.s(prev,'NextAttackAt',g.op('Add_DoubleDouble',now,3.0))
    stop=g.call('/Script/Engine.Controller','StopMovement');g.w(ctrl,stop,'self');g.chain(prev,stop);reconnect(g,stop,links)
    # Contact is possible only inside the active portion of this montage.
    resolve=next(n for n in g.nodes if any('CustomFunctionName="ResolveAttack"' in p for p in n.props))
    links=detach(g,resolve)
    mesh=g.v('Mesh','object',owner=CHAR,obj='/Script/Engine.SkeletalMeshComponent',target=own,native=True)
    anim=g.call('/Script/Engine.SkeletalMeshComponent','GetAnimInstance',pure=True).pin('ReturnValue','object',obj=ANIM,out=True);g.w(mesh,anim,'self')
    montage='/Game/ThirdPerson/Blueprints/EnemigoIA/AM_EnemyAttack_Entrega.AM_EnemyAttack_Entrega'
    position=g.call(ANIM,'Montage_GetPosition',pure=True).pin('Montage','object',obj='/Script/Engine.AnimMontage',default_obj=montage).pin('ReturnValue','real',sub='float',out=True);g.w((anim,'ReturnValue'),position,'self')
    playing=g.call(ANIM,'Montage_IsPlaying',pure=True).pin('Montage','object',obj='/Script/Engine.AnimMontage',default_obj=montage).pin('ReturnValue','bool',out=True);g.w((anim,'ReturnValue'),playing,'self')
    window=g.both(g.cmp('GreaterEqual_DoubleDouble',(position,'ReturnValue'),.28),g.cmp('LessEqual_DoubleDouble',(position,'ReturnValue'),.64))
    check=g.br(resolve,g.both(g.neg(g.v('bAttackResolved','bool')),g.both((playing,'ReturnValue'),window)))
    reconnect(g,check,links)
    # Mark a real contact, not the first empty frame of the active punch.
    from generate_combat_motion import facing_dot, turn_toward
    contact_gate=next(n for n in g.nodes if n.kind.endswith('K2Node_IfThenElse') and n.x==2100 and n.y==4200)
    condition_name,condition_id=contact_gate.pins['Condition']['links'][0]
    condition_node=next(n for n in g.nodes if n.name==condition_name)
    condition_pin=next(p for p in condition_node.pins.values() if p['id']==condition_id)
    condition_pin['links'].remove((contact_gate.name,contact_gate.pins['Condition']['id']));contact_gate.pins['Condition']['links']=[]
    victim=g.v('AttackVictim','object',obj=ACTOR)
    cone=g.cmp('GreaterEqual_DoubleDouble',facing_dot(g,own,victim),.4)
    g.w(g.both((condition_node,condition_pin['name']),cone),contact_gate,'Condition')
    links=detach(g,contact_gate);reconnect(g,g.s(contact_gate,'bAttackResolved',True,'bool'),links)
    # Animation owns timing; movement remains planted. Tracking ends before contact.
    for node in g.nodes:
        if 'InPlayRate' in node.pins and 'AnimMontage' in node.pins and 'AM_EnemyAttack_' in str(node.pins['AnimMontage'].get('default_obj')):node.pins['InPlayRate']['default']='1.25'
    legacy_range=next(n for n in g.nodes if n.x==1500 and n.y==4800 and 'B' in n.pins);legacy_range.pins['B']['default']='210'
    # Enemy Actor Tick stays disabled. The active behavior task owns this update.
    tick=g.custom('UpdateStrike').pin('DeltaSeconds','real',sub='float',out=True)
    tick.props.append('CustomProperties UserDefinedPin (PinName="DeltaSeconds",PinType=(PinCategory="real",PinSubCategory="float"),DesiredPinDirection=EGPD_Output)')
    active=g.br(tick,g.v('bAttackInProgress','bool'))
    track=g.br(active,g.cmp('Less_DoubleDouble',(position,'ReturnValue'),.26))
    turned=turn_toward(g,track,own,victim,(tick,'DeltaSeconds'),480)
    # Reuse the resolve branch directly: importing a self-call to another event in
    # the same cleared graph can silently discard that call before skeleton rebuild.
    g.chain(turned,check);g.chain(track,check,'else')
    # OnHealthChanged runs for both damage and healing; confirm only actual loss.
    changed=next(n for n in g.nodes if any('CustomFunctionName="OnHealthChanged"' in p for p in n.props))
    links=detach(g,changed)
    delta=g.s(changed,'LastDamageAmount',g.op('Subtract_DoubleDouble',g.v('LastFeedbackHealth'),hp))
    lost=g.br(delta,g.cmp('Greater_DoubleDouble',g.v('LastDamageAmount'),0))
    pc=g.call(GS,'GetPlayerController',pure=True,static=True).pin('PlayerIndex','int',default='0').pin('ReturnValue','object',obj='/Script/Engine.PlayerController',out=True)
    hud=g.call('/Script/Engine.PlayerController','GetHUD',pure=True).pin('ReturnValue','object',obj='/Script/Engine.HUD',out=True);g.w((pc,'ReturnValue'),hud,'self')
    cast=g.cast(HUD);g.chain(lost,cast);g.w((hud,'ReturnValue'),cast,'Object');hudtarget=(cast,'AsBP_HUD_Entrega')
    now=g.c(GS,'GetRealTimeSeconds')
    prev=g.s(cast,'EnemyHitUntil',g.op('Add_DoubleDouble',now,.18),owner=HUD,target=hudtarget)
    prev=g.s(prev,'LastEnemyDamage',g.op('Subtract_DoubleDouble',g.v('LastFeedbackHealth'),hp),owner=HUD,target=hudtarget)
    impact=g.sound(prev,'DoorHit');impact.pins['VolumeMultiplier']['default']='.3';impact.pins['PitchMultiplier']['default']='1.3'
    saved=g.s(impact,'LastFeedbackHealth',hp);g.chain(lost,saved,'else');g.chain(cast,saved,'CastFailed');reconnect(g,saved,links)
    # Light hits retain damage/feedback but cannot restart a perpetual stun loop.
    react=next(n for n in g.nodes if any('SetValueAsBool' in p for p in n.props) and n.x==1250 and n.y==2100)
    previous_name,previous_id=react.pins['execute']['links'][0]
    previous=next(n for n in g.nodes if n.name==previous_name);previous_pin=next(p for p in previous.pins.values() if p['id']==previous_id)
    previous_pin['links'].remove((react.name,react.pins['execute']['id']));react.pins['execute']['links']=[]
    time=g.c(GS,'GetTimeSeconds')
    poise=g.c(MATH,'BooleanOR',[('A','bool',g.cmp('GreaterEqual_DoubleDouble',time,g.v('NextStaggerAt'))),('B','bool',g.cmp('GreaterEqual_DoubleDouble',g.v('LastDamageAmount'),25))],cat='bool')
    stagger=g.br(previous,g.both(g.cmp('Greater_DoubleDouble',g.v('LastDamageAmount'),0),poise),previous_pin['name'])
    recovery=g.s(stagger,'NextStaggerAt',g.op('Add_DoubleDouble',time,g.v('StaggerCooldown')));g.chain(recovery,react)
    from generate_final_words import enemy_final_words
    enemy_final_words(g)
    g.write('BP_BaseEnemy')

def windup():
    from generate_combat_motion import windup_task
    windup_task()

def charge():
    from generate_combat_motion import charge_task
    charge_task()

if __name__=='__main__':base_enemy();windup();charge()
