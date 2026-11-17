"""Final encounter prerequisites and last-enemy dying dialogue, Blueprint only."""
from generate_delivery_controls import ControlsGraph
from generate_progression_graphs import ACTOR,OBJECT,GS,MATH,DIRECTOR,HERO,HOSTAGE,ZONE
from generate_combat_graphs import BASE,CHAR
from generate_delivery_graphs import HEALTH as PLAYER_HEALTH,q
from generate_cinematic_graphs import CINEMA,select

DEATH='/Game/ThirdPerson/Blueprints/EnemigoIA/AM_EnemyDeath_Entrega.AM_EnemyDeath_Entrega'
ANIM='/Script/Engine.AnimInstance'

def zone_prerequisite(g,ready):
    g.__class__=ControlsGraph
    source_name,pid=ready.pins['execute']['links'][0]
    source=next(n for n in g.nodes if n.name==source_name)
    pin=next(p for p in source.pins.values() if p['id']==pid)
    pin['links'].remove((ready.name,ready.pins['execute']['id']));ready.pins['execute']['links']=[]
    required=g.v('RequiredZone','object',obj=ZONE)
    valid=g.br(source,(g.valid(*required),'ReturnValue'),pin['name'])
    clear=g.br(valid,g.v('bCleared','bool',owner=ZONE,target=required))
    g.chain(clear,ready);g.chain(valid,ready,'else')

def mixed_enemy_class(g,original):
    index=g.c(MATH,'Conv_BoolToInt',[('InBool','bool',g.v('bMixedEnemies','bool'))],cat='int')
    return select(g,index,[original,g.v('AlternateEnemyClass','class',obj=BASE)],'class',BASE)

def enemy_final_words(g):
    from generate_combat_feedback import detach,reconnect
    g.__class__=ControlsGraph;own=(g.selfnode(typ=BASE),'self')
    deathplay=next(n for n in g.nodes if 'AnimMontage' in n.pins and n.pins['AnimMontage'].get('default_obj')==DEATH)
    name,pid=deathplay.pins['execute']['links'][0];before=next(n for n in g.nodes if n.name==name)
    pin=next(p for p in before.pins.values() if p['id']==pid)
    pin['links'].remove((deathplay.name,deathplay.pins['execute']['id']));deathplay.pins['execute']['links']=[]
    fresh=g.br(before,g.neg(g.v('bFinalWordsPending','bool')),pin['name'])
    # Possession changes Pawn.Owner to the AI controller; keep an explicit zone.
    zone=g.v('EncounterZone','object',obj=ZONE)
    cast=g.br(fresh,(g.valid(*zone),'ReturnValue'));g.chain(cast,deathplay,'else')
    eligible=g.both(g.v('bFinalStand','bool',owner=ZONE,target=zone),g.neg(g.v('bRevelationStarted','bool',owner=ZONE,target=zone)))
    eligible=g.both(eligible,g.cmp('EqualEqual_IntInt',g.v('CurrentWave','int',owner=ZONE,target=zone),g.v('WaveCount','int',owner=ZONE,target=zone),'int'))
    finalwave=g.br(cast,eligible);g.chain(finalwave,deathplay,'else')
    reset=g.s(finalwave,'FinalPeersAlive',0,'int')
    enemies=g.v('EncounterEnemies','object',owner=ZONE,target=zone,obj=ACTOR);enemies[0].pins[enemies[1]]['container']='Array'
    loop=g.foreach(*enemies);g.chain(reset,loop,nextpin='Exec')
    exists=g.br(loop,(g.valid(loop,'Array Element'),'ReturnValue'),'LoopBody')
    ec,enemy=g.cast_after(exists,(loop,'Array Element'),BASE)
    alive=g.br(ec,g.neg(g.v('bIsDead','bool',owner=BASE,target=enemy)))
    g.s(alive,'FinalPeersAlive',g.op('Add_IntInt',g.v('FinalPeersAlive','int'),1,'int'),'int')
    last=g.br(loop,g.cmp('EqualEqual_IntInt',g.v('FinalPeersAlive','int'),0,'int'),'Completed');g.chain(last,deathplay,'else')
    found=g.find(last,CINEMA);c=(found,'ReturnValue')
    valid=g.br(found,(g.valid(*c),'ReturnValue'));g.chain(valid,deathplay,'else')
    initialized=g.br(valid,g.v('bInitialized','bool',owner=CINEMA,target=c));g.chain(initialized,deathplay,'else')
    director=g.v('Director','object',owner=CINEMA,target=c,obj=DIRECTOR)
    hero=g.v('Hero','object',owner=CINEMA,target=c,obj=HERO);host=g.v('Hostage','object',owner=CINEMA,target=c,obj=HOSTAGE)
    health=g.v('BPC_Health','object',owner=HERO,target=hero,obj=PLAYER_HEALTH)
    good=g.both(g.neg(g.v('bActive','bool',owner=CINEMA,target=c)),g.neg(g.v('bOrderRevealed','bool',owner=DIRECTOR,target=director)))
    good=g.both(good,g.cmp('Less_IntInt',g.v('Paso','int',owner=DIRECTOR,target=director),4,'int'))
    good=g.both(good,g.cmp('Greater_DoubleDouble',g.v('Health',owner=PLAYER_HEALTH,target=health),0))
    good=g.both(good,g.cmp('Greater_DoubleDouble',g.v('Health',owner=HOSTAGE,target=host),0))
    begin=g.br(initialized,good);g.chain(begin,deathplay,'else')
    prev=g.s(begin,'bRevelationStarted',True,'bool',owner=ZONE,target=zone)
    prev=g.s(prev,'bFinalWordsPending',True,'bool')
    prev=g.action_on(prev,ACTOR,'SetLifeSpan',own,[('InLifespan','real',0,None)])
    play=g.montage(*own,'AM_EnemyDeath_Entrega');g.chain(prev,play)
    mesh=g.v('Mesh','object',owner=CHAR,target=own,obj='/Script/Engine.SkeletalMeshComponent',native=True)
    anim=g.c('/Script/Engine.SkeletalMeshComponent','GetAnimInstance',cat='object',obj=ANIM,pure=True,static=False);g.w(mesh,anim[0],'self')
    position=g.action_on(play,ANIM,'Montage_SetPosition',anim,[('Montage','object',None,'/Script/Engine.AnimMontage'),('NewPosition','real',.28,None)])
    position.pins['Montage']['default_obj']=DEATH
    pause=g.action_on(position,ANIM,'Montage_Pause',anim,[('Montage','object',None,'/Script/Engine.AnimMontage')]);pause.pins['Montage']['default_obj']=DEATH
    g.action_on(pause,CINEMA,'StartRevelation',c,[('Enemy','object',own,BASE)])
    # Resume the original full death/cleanup only after the line has finished.
    event=g.custom('FinishFinalWords');pending=g.br(event,g.v('bFinalWordsPending','bool'))
    clear=g.s(pending,'bFinalWordsPending',False,'bool');g.chain(clear,deathplay)

def order_text(g,code):
    from generate_beacon_sequence import ORDERS
    return select(g,code,[' > '.join('ABC'[i] for i in p) for p in ORDERS])

def reveal_event(g,own,hero,host,director,now):
    e=g.custom('StartRevelation').pin('Enemy','object',obj=BASE,out=True)
    e.props.append('CustomProperties UserDefinedPin (PinName="Enemy",PinType=(PinCategory="object",PinSubCategoryObject='+q("/Script/Engine.BlueprintGeneratedClass'"+BASE+"'")+'),DesiredPinDirection=EGPD_Output)')
    gate=g.br(e,g.neg(g.v('bActive','bool')))
    valid=g.br(gate,(g.valid(e,'Enemy'),'ReturnValue'))
    prev=g.s(valid,'RevealEnemy',(e,'Enemy'),'object',obj=BASE)
    prev=g.s(prev,'RevealedSequence',order_text(g,g.v('OrderCode','int',owner=DIRECTOR,target=director)),'string')
    prev=g.s(prev,'Kind',4,'int')
    prev=g.s(prev,'bNarrativePaused',True,'bool',owner=DIRECTOR,target=director)
    # Nonterminal cinema pauses the escort tree but preserves walking and health.
    ctrl=g.c('/Script/Engine.Pawn','GetController',cat='object',obj='/Script/Engine.Controller',pure=True,static=False);g.w(host,ctrl[0],'self')
    prev=g.action_on(prev,'/Script/Engine.Controller','StopMovement',ctrl)
    nc=g.nativecast('/Script/AIModule.AIController');g.chain(prev,nc);g.w(ctrl,nc,'Object')
    brain=g.v('BrainComponent','object',owner='/Script/AIModule.AIController',target=(nc,'AsAIController'),obj='/Script/AIModule.BrainComponent',native=True)
    check=g.br(nc,(g.valid(*brain),'ReturnValue'))
    paused=g.action_on(check,'/Script/AIModule.BrainComponent','StopLogic',brain,[('Reason','string','Last guardian reveals the beacon order',None)])
    move=g.v('CharacterMovement','object',owner=CHAR,target=hero,obj='/Script/Engine.CharacterMovementComponent',native=True)
    stop=g.action_on(paused,'/Script/Engine.CharacterMovementComponent','StopMovementImmediately',move);g.chain(nc,stop,'CastFailed');g.chain(check,stop,'else')
    stop=g.action_on(stop,CHAR,'StopAnimMontage',hero,[('AnimMontage','object',None,'/Script/Engine.AnimMontage')])
    prev=g.s(stop,'IsAttacking',False,'bool',owner=HERO,target=hero)
    prev=g.s(prev,'bLightAttackActive',False,'bool',owner=HERO,target=hero)
    prev=g.action_on(prev,HERO,'ResetState',hero)
    g.action_on(prev,CINEMA,'PlayCinema')

def complete_revelation(g,prev,host,director):
    prev=g.s(prev,'bOrderRevealed',True,'bool',owner=DIRECTOR,target=director)
    prev=g.s(prev,'bNarrativePaused',False,'bool',owner=DIRECTOR,target=director)
    enemy=g.local('RevealEnemy',BASE);valid=g.br(prev,(g.valid(*enemy),'ReturnValue'))
    finished=g.action_on(valid,BASE,'FinishFinalWords',enemy)
    ctrl=g.c('/Script/Engine.Pawn','GetController',cat='object',obj='/Script/Engine.Controller',pure=True,static=False);g.w(host,ctrl[0],'self')
    cast=g.nativecast('/Script/AIModule.AIController');g.chain(finished,cast);g.chain(valid,cast,'else');g.w(ctrl,cast,'Object')
    brain=g.v('BrainComponent','object',owner='/Script/AIModule.AIController',target=(cast,'AsAIController'),obj='/Script/AIModule.BrainComponent',native=True)
    okay=g.br(cast,(g.valid(*brain),'ReturnValue'))
    resume=g.action_on(okay,'/Script/AIModule.BrainComponent','RestartLogic',brain)
    return resume,[(cast,'CastFailed'),(okay,'else')]
