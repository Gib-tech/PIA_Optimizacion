"""Blueprint sources for escort-gated, finite combat encounters and heavy hits."""
from generate_combat_graphs import CombatGraph,ACTOR,OBJECT,BASE,CHARGER,HEALTH,ref,q
ZONE='/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C'
PLAYER='/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C'
HOSTAGE='/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'
TRANSFORM='/Script/CoreUObject.Transform'

def seq(g,prev,items,x=0,y=0):
    for i,(name,cat,value) in enumerate(items):
        n=g.set(name,cat,value,sub='double' if cat=='real' else '',x=x+i*300,y=y);g.chain(prev,n);prev=n
    return prev

def gate(g,prev,enabled,x=0,y=0):
    blocker=g.get('Blocker','object',obj=ACTOR,x=x,y=y+400)
    valid=g.valid(blocker,'Blocker',x=x+250,y=y+400)
    b=g.branch(x=x,y=y);g.chain(prev,b);g.wire(valid,'ReturnValue',b,'Condition')
    collision=g.call(ACTOR,'SetActorEnableCollision',x=x+300,y=y).pin('bNewActorEnableCollision','bool',default=str(enabled).lower());g.chain(b,collision);g.wire(blocker,'Blocker',collision,'self')
    hide=g.call(ACTOR,'SetActorHiddenInGame',x=x+600,y=y).pin('bNewHidden','bool',default=str(not enabled).lower());g.chain(collision,hide);g.wire(blocker,'Blocker',hide,'self')
    return hide

def zone():
    g=CombatGraph();self=g.selfnode(typ=ZONE,x=0,y=700);player=g.player(x=0,y=1000)
    tick=g.event(ACTOR,'ReceiveTick',x=0,y=0).pin('DeltaSeconds','real',sub='float',out=True)
    phase=g.get('Phase','int',x=0,y=350)
    switch=g.node('K2Node_SwitchInteger',['PinNames(0)="0"','PinNames(1)="1"','PinNames(2)="2"'],x=300,y=0).pin('execute').pin('Selection','int').pin('0',out=True).pin('1',out=True).pin('2',out=True).pin('Default',out=True)
    g.chain(tick,switch);g.wire(phase,'Phase',switch,'Selection')
    overlap=g.call(ACTOR,'IsOverlappingActor',pure=True,x=650,y=700).pin('Other','object',obj=ACTOR).pin('ReturnValue','bool',out=True);g.wire(player,'ReturnValue',overlap,'Other')
    entered=g.branch(x=650,y=0);g.chain(switch,entered,'0');g.wire(overlap,'ReturnValue',entered,'Condition')
    escort=g.call('/Script/Engine.GameplayStatics','GetActorOfClass',static=True,x=950,y=0).pin('ActorClass','class',obj=ACTOR,default_obj=HOSTAGE).pin('ReturnValue','object',obj=ACTOR,out=True);g.chain(entered,escort)
    valid=g.valid(escort,'ReturnValue',x=1250,y=650)
    vb=g.branch(x=1250,y=0);g.chain(escort,vb);g.wire(valid,'ReturnValue',vb,'Condition')
    bb=g.blackboard(escort,'ReturnValue',x=1550,y=700);following=g.bbget(bb,'bAccompanying','Bool',x=1850,y=700)
    dist=g.dist(escort,'ReturnValue',player,'ReturnValue',x=1550,y=1000)
    near=g.compare('LessEqual_DoubleDouble','real','600',sub='double',x=1850,y=1000);g.wire(dist,'ReturnValue',near,'A')
    ready=g.boolean('BooleanAND',following,'ReturnValue',near,'ReturnValue',x=2150,y=700)
    eb=g.branch(x=2450,y=0);g.chain(vb,eb);g.wire(ready,'ReturnValue',eb,'Condition')
    # The hostage flees before the door closes; subsequent waves never require him to return.
    refuge=g.get('RefugePoint','object',obj=ACTOR,x=2750,y=700);pos=g.location(refuge,'RefugePoint',x=3050,y=700)
    flee=g.bbset(bb,'FleeLocation','Vector',x=3050,y=0);g.chain(eb,flee);g.wire(pos,'ReturnValue',flee,'VectorValue')
    previous=flee
    for i,(key,kind,value) in enumerate([('bAccompanying','Bool','false'),('bWaiting','Bool','false'),('Estado','Int','2'),('bMustFlee','Bool','true')]):
        n=g.bbset(bb,key,kind,value,x=3350+i*350,y=0);g.chain(previous,n);previous=n
    escort_ready=previous
    # Count living enemies, including corpses awaiting their death animation cleanup.
    reset=g.set('LivingCount','int','0',x=650,y=1800);g.chain(switch,reset,'1')
    enemies=g.get('EncounterEnemies','object',obj=ACTOR,x=650,y=2200);enemies.pins['EncounterEnemies']['container']='Array'
    loop=g.foreach(enemies,'EncounterEnemies',x=950,y=1800);g.chain(reset,loop,nextpin='Exec')
    exists=g.valid(loop,'Array Element',x=1250,y=2200);lb=g.branch(x=1250,y=1800);g.chain(loop,lb,'LoopBody');g.wire(exists,'ReturnValue',lb,'Condition')
    cast=g.cast(BASE,x=1550,y=1800);g.chain(lb,cast);g.wire(loop,'Array Element',cast,'Object')
    dead=g.get('bIsDead','bool',owner=BASE,x=1850,y=2200);g.wire(cast,'AsBP_BaseEnemy',dead,'self')
    alive=g.boolean('Not_PreBool',dead,'bIsDead',x=2150,y=2200);ab=g.branch(x=2450,y=1800);g.chain(cast,ab);g.wire(alive,'ReturnValue',ab,'Condition')
    count=g.get('LivingCount','int',x=2450,y=2400)
    add=g.call('/Script/Engine.KismetMathLibrary','Add_IntInt',pure=True,static=True,x=2750,y=2400).pin('A','int').pin('B','int',default='1').pin('ReturnValue','int',out=True);g.wire(count,'LivingCount',add,'A')
    inc=g.set('LivingCount','int','0',x=3050,y=1800);g.chain(ab,inc);g.wire(add,'ReturnValue',inc,'LivingCount')
    zero=g.compare('EqualEqual_IntInt','int','0',x=1250,y=3000);g.wire(count,'LivingCount',zero,'A')
    cleared=g.branch(x=1550,y=2800);g.chain(loop,cleared,'Completed');g.wire(zero,'ReturnValue',cleared,'Condition')
    wave=g.get('CurrentWave','int',x=1550,y=3300);total=g.get('WaveCount','int',x=1550,y=3500)
    more=g.compare('Less_IntInt','int','2',x=1850,y=3300);g.wire(wave,'CurrentWave',more,'A');g.wire(total,'WaveCount',more,'B')
    mb=g.branch(x=2150,y=2800);g.chain(cleared,mb);g.wire(more,'ReturnValue',mb,'Condition')
    inter=g.set('Phase','int','2',x=2450,y=2800);g.chain(mb,inter)
    now=g.call('/Script/Engine.GameplayStatics','GetTimeSeconds',pure=True,static=True,x=2450,y=3400).pin('ReturnValue','real',sub='float',out=True)
    later=g.call('/Script/Engine.KismetMathLibrary','Add_DoubleDouble',pure=True,static=True,x=2750,y=3400).pin('A','real',sub='double').pin('B','real',sub='double',default='3.0').pin('ReturnValue','real',sub='double',out=True);g.wire(now,'ReturnValue',later,'A')
    wait=g.set('NextWaveAt','real','0',sub='double',x=3050,y=2800);g.chain(inter,wait);g.wire(later,'ReturnValue',wait,'NextWaveAt')
    done=seq(g,mb,[('Phase','int','3'),('bCleared','bool','true')],x=2450,y=3900)
    # seq's default connection above is replaced to the false branch.
    mb.pins['then']['links'].remove((g.nodes[-2].name,g.nodes[-2].pins['execute']['id']))
    g.nodes[-2].pins['execute']['links'].remove((mb.name,mb.pins['then']['id']))
    g.chain(mb,g.nodes[-2],'else')
    gate(g,done,False,x=3050,y=3900)
    due=g.get('NextWaveAt','real',sub='double',x=650,y=4900)
    expired=g.compare('GreaterEqual_DoubleDouble','real','0',sub='double',x=950,y=4900);g.wire(now,'ReturnValue',expired,'A');g.wire(due,'NextWaveAt',expired,'B')
    wb=g.branch(x=1250,y=4600);g.chain(switch,wb,'2');g.wire(expired,'ReturnValue',wb,'Condition')
    # One custom event is shared by activation and the intermission timer.
    event=g.custom('StartWave',x=0,y=5700)
    clear=g.array('EncounterEnemies','Array_Clear',x=350,y=5700);g.chain(event,clear);g.chain(escort_ready,clear);g.chain(wb,clear)
    num=g.call('/Script/Engine.KismetMathLibrary','Add_IntInt',pure=True,static=True,x=350,y=6200).pin('A','int').pin('B','int',default='1').pin('ReturnValue','int',out=True);g.wire(wave,'CurrentWave',num,'A')
    save=g.set('CurrentWave','int','0',x=650,y=5700);g.chain(clear,save);g.wire(num,'ReturnValue',save,'CurrentWave')
    previous=save
    enemyclass=g.get('EnemyClass','class',obj=BASE,x=650,y=6600)
    for i in [1,2]:
        x=950+(i-1)*1500
        point=g.get('SpawnPoint'+str(i),'object',obj=ACTOR,x=x,y=6500)
        loc=g.location(point,'SpawnPoint'+str(i),x=x+200,y=6900)
        transform=g.call('/Script/Engine.KismetMathLibrary','MakeTransform',pure=True,static=True,x=x+300,y=6500).pin('Location','struct',obj='/Script/CoreUObject.Vector').pin('Rotation','struct',obj='/Script/CoreUObject.Rotator',default='0,0,0').pin('Scale','struct',obj='/Script/CoreUObject.Vector',default='1,1,1').pin('ReturnValue','struct',obj=TRANSFORM,out=True);g.wire(loc,'ReturnValue',transform,'Location')
        spawn=g.node('K2Node_SpawnActorFromClass',x=x,y=5700).pin('execute').pin('then',out=True).pin('Class','class',obj=ACTOR).pin('SpawnTransform','struct',obj=TRANSFORM).pin('CollisionHandlingOverride','byte',obj='/Script/Engine.ESpawnActorCollisionHandlingMethod',default='AdjustIfPossibleButAlwaysSpawn').pin('Owner','object',obj=ACTOR).pin('TransformScaleMethod','byte',obj='/Script/Engine.ESpawnActorScaleMethod',default='MultiplyWithRoot').pin('ReturnValue','object',obj=BASE,out=True)
        g.chain(previous,spawn);g.wire(enemyclass,'EnemyClass',spawn,'Class');g.wire(transform,'ReturnValue',spawn,'SpawnTransform');g.wire(self,'self',spawn,'Owner')
        append=g.array('EncounterEnemies','Array_AddUnique',item=spawn,ip='ReturnValue',x=x+900,y=5700);g.chain(spawn,append);previous=append
    previous=seq(g,previous,[('Phase','int','1'),('LivingCount','int','2')],x=3950,y=5700)
    spawned=g.get('SpawnedCount','int',x=3950,y=6400)
    plus=g.call('/Script/Engine.KismetMathLibrary','Add_IntInt',pure=True,static=True,x=4250,y=6400).pin('A','int').pin('B','int',default='2').pin('ReturnValue','int',out=True);g.wire(spawned,'SpawnedCount',plus,'A')
    savecount=g.set('SpawnedCount','int','0',x=4550,y=5700);g.chain(previous,savecount);g.wire(plus,'ReturnValue',savecount,'SpawnedCount')
    gate(g,savecount,True,x=4850,y=5700)
    g.write('BP_CombatZone')

def heavy_player():
    g=CombatGraph()
    props=['DelegatePropertyName="OnComponentBeginOverlap"','DelegateOwnerClass='+ref('/Script/Engine.PrimitiveComponent'),'ComponentPropertyName="WeaponHitbox"','EventReference=(MemberParent="/Script/CoreUObject.Package\'/Script/Engine\'",MemberName="ComponentBeginOverlapSignature__DelegateSignature")','bInternalEvent=True','CustomFunctionName="BndEvt__BP_PlayerEntrega_HeavyOverlap__DelegateSignature"']
    event=g.node('K2Node_ComponentBoundEvent',props,x=0,y=0).pin('then',out=True).pin('OverlappedComponent','object',obj='/Script/Engine.PrimitiveComponent',out=True).pin('OtherActor','object',obj=ACTOR,out=True).pin('OtherComp','object',obj='/Script/Engine.PrimitiveComponent',out=True).pin('OtherBodyIndex','int',out=True).pin('bFromSweep','bool',out=True).pin('SweepResult','struct',obj='/Script/Engine.HitResult',out=True)
    active=g.get('IsAttacking','bool',x=0,y=500)
    light=g.get('bLightAttackActive','bool',x=0,y=700)
    heavy=g.boolean('Not_PreBool',light,'bLightAttackActive',x=300,y=700)
    ok=g.boolean('BooleanAND',active,'IsAttacking',heavy,'ReturnValue',x=600,y=500)
    branch=g.branch(x=900,y=0);g.chain(event,branch);g.wire(ok,'ReturnValue',branch,'Condition')
    cast=g.cast(CHARGER,x=1200,y=0);g.chain(branch,cast);g.wire(event,'OtherActor',cast,'Object')
    contains=g.array('HeavyHitActors','Array_Contains',item=event,ip='OtherActor',x=1500,y=600)
    fresh=g.boolean('Not_PreBool',contains,'ReturnValue',x=1800,y=600)
    check=g.branch(x=2100,y=0);g.chain(cast,check);g.wire(fresh,'ReturnValue',check,'Condition')
    append=g.array('HeavyHitActors','Array_AddUnique',item=event,ip='OtherActor',x=2400,y=0);g.chain(check,append)
    health=g.get('BPC_E_Health','object',owner=BASE,obj=HEALTH,x=2400,y=700);g.wire(cast,'AsBP_ChargerEnemy',health,'self')
    amount=g.get('HeavyDamage','real',sub='double',x=2700,y=900)
    hit=g.action('E_Decrease_Health',owner=HEALTH,x=3000,y=0).pin('Damage','real',sub='double');g.chain(append,hit);g.wire(health,'BPC_E_Health',hit,'self');g.wire(amount,'HeavyDamage',hit,'Damage')
    tick=g.event(ACTOR,'ReceiveTick',x=0,y=1500).pin('DeltaSeconds','real',sub='float',out=True)
    stop=g.boolean('Not_PreBool',active,'IsAttacking',x=300,y=1800)
    reset=g.boolean('BooleanOR',stop,'ReturnValue',light,'bLightAttackActive',x=600,y=1800)
    b=g.branch(x=900,y=1500);g.chain(tick,b);g.wire(reset,'ReturnValue',b,'Condition')
    clear=g.array('HeavyHitActors','Array_Clear',x=1200,y=1500);g.chain(b,clear)
    g.write('BP_PlayerEntrega')

if __name__=='__main__':zone();heavy_player()
