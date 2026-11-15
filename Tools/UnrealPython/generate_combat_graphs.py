"""Reviewable Blueprint clipboard sources: combat actions and charger tasks."""
from generate_hostage_graphs import HostageGraph,ACTOR,PAWN,OBJECT,VECTOR,CONTROLLER,BB
from generate_delivery_graphs import ref,q
ROOT='/Game/ThirdPerson/Blueprints/EnemigoIA'
BASE=ROOT+'/BP_BaseEnemy.BP_BaseEnemy_C'
CHARGER=ROOT+'/BP_ChargerEnemy.BP_ChargerEnemy_C'
HEALTH='/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health.BPC_E_Health_C'
TASK='/Script/AIModule.BTTask_BlueprintBase'
CHAR='/Script/Engine.Character'
MOVE='/Script/Engine.CharacterMovementComponent'
MONTAGE='/Script/Engine.AnimMontage'

class CombatGraph(HostageGraph):
    def write(self,name):
        if name.startswith('BTTask_'):
            events=[n for n in self.nodes if n.kind.endswith('K2Node_Event')]
            execute=next((n for n in events if any('ReceiveExecuteAI' in p for p in n.props)),None)
            if execute:
                cached=self.get('CachedPawn','object',obj=BASE,x=-800,y=600)
                for n in list(self.nodes):
                    if 'self' not in n.pins or n.pins['self']['obj']!=CHAR:continue
                    for source_name,source_id in list(n.pins['self']['links']):
                        source=next(x for x in self.nodes if x.name==source_name)
                        if source not in events:continue
                        pin=source.pins['ControlledPawn']
                        pin['links'].remove((n.name,n.pins['self']['id']))
                        n.pins['self']['links'].remove((source_name,source_id))
                        self.wire(cached,'CachedPawn',n,'self')
                outgoing=list(execute.pins['then']['links']);execute.pins['then']['links']=[]
                for target_name,pin_id in outgoing:
                    target=next(x for x in self.nodes if x.name==target_name)
                    targetpin=next(p for p in target.pins.values() if p['id']==pin_id)
                    targetpin['links'].remove((execute.name,execute.pins['then']['id']))
                cast=self.cast(BASE,x=-650,y=-500);self.wire(execute,'ControlledPawn',cast,'Object');self.chain(execute,cast)
                save=self.set('CachedPawn','object',None,obj=BASE,x=-350,y=-500);self.chain(cast,save);self.wire(cast,'AsBP_BaseEnemy',save,'CachedPawn')
                for target_name,pin_id in outgoing:
                    target=next(x for x in self.nodes if x.name==target_name)
                    targetpin=next(p for p in target.pins.values() if p['id']==pin_id)
                    self.chain(save,target,nextpin=targetpin['name'])
                self.finish(cast,'CastFailed',success=False,x=-300,y=-800)
        super().write(name)
    def custom(self,name,**pos):return self.node('K2Node_CustomEvent',['CustomFunctionName='+q(name)],**pos).pin('then',out=True)
    def action(self,name,owner=BASE,**pos):
        n=self.call(ACTOR,name,**pos)
        n.props=['FunctionReference=(MemberParent='+q("/Script/Engine.BlueprintGeneratedClass'"+owner+"'")+',MemberName='+q(name)+')']
        n.pins['self']['obj']=owner
        return n
    def nativeget(self,owner,name,cat,obj=None,**pos):
        n=self.get(name,cat,owner=owner,obj=obj,**pos)
        n.props=['VariableReference=(MemberParent='+ref(owner)+',MemberName='+q(name)+')']
        return n
    def selfnode(self,typ=BASE,**pos):return self.node('K2Node_Self',**pos).pin('self','object',obj=typ,out=True)
    def ctrl(self,pawn,pin,**pos):
        n=self.call(PAWN,'GetController',pure=True,**pos).pin('ReturnValue','object',obj='/Script/Engine.Controller',out=True)
        self.wire(pawn,pin,n,'self');return n
    def nativecast(self,typ,**pos):
        return self.node('K2Node_DynamicCast',['TargetType='+ref(typ)],**pos).pin('execute').pin('then',out=True).pin('CastFailed',out=True).pin('Object','object',obj=OBJECT).pin('As'+typ.rsplit('.',1)[-1],'object',obj=typ,out=True)
    def finish(self,prev,pin='then',abort=False,success=True,**pos):
        n=self.call(TASK,'FinishAbort' if abort else 'FinishExecute',**pos)
        if not abort:n.pin('bSuccess','bool',default=str(success).lower())
        self.chain(prev,n,pin);return n
    def task_event(self,name,**pos):
        n=self.event(TASK,name,**pos).pin('OwnerController','object',obj=CONTROLLER,out=True).pin('ControlledPawn','object',obj=PAWN,out=True)
        if name=='ReceiveTickAI':n.pin('DeltaSeconds','real',sub='float',out=True)
        return n
    def montage(self,pawn,pin,name,rate='1.0',**pos):
        n=self.call(CHAR,'PlayAnimMontage',**pos).pin('AnimMontage','object',obj=MONTAGE,default_obj=ROOT+'/'+name+'.'+name).pin('InPlayRate','real',sub='float',default=rate).pin('StartSectionName','name',default='None').pin('ReturnValue','real',sub='float',out=True)
        self.wire(pawn,pin,n,'self');return n
    def stop_montage(self,pawn,pin,name,**pos):
        n=self.call(CHAR,'StopAnimMontage',**pos).pin('AnimMontage','object',obj=MONTAGE,default_obj=ROOT+'/'+name+'.'+name)
        self.wire(pawn,pin,n,'self');return n
    def stop_move(self,event,**pos):
        n=self.call('/Script/Engine.Controller','StopMovement',**pos);self.wire(event,'OwnerController',n,'self');return n
    def speed(self,event,value,**pos):
        movement=self.nativeget(CHAR,'CharacterMovement','object',obj=MOVE,x=pos.get('x',0),y=pos.get('y',0)+230)
        self.wire(event,'ControlledPawn',movement,'self')
        n=self.set('MaxWalkSpeed','real',value,sub='float',**pos)
        n.props=['VariableReference=(MemberParent='+ref(MOVE)+',MemberName="MaxWalkSpeed")']
        n.pin('self','object',obj=MOVE);self.wire(movement,'CharacterMovement',n,'self');return n
    def elapsed(self,tick,**pos):
        old=self.get('Elapsed','real',sub='double',x=pos.get('x',0),y=pos.get('y',0)+220)
        add=self.call('/Script/Engine.KismetMathLibrary','Add_DoubleDouble',pure=True,static=True,x=pos.get('x',0)+250,y=pos.get('y',0)+220).pin('A','real',sub='double').pin('B','real',sub='double').pin('ReturnValue','real',sub='double',out=True)
        self.wire(old,'Elapsed',add,'A');self.wire(tick,'DeltaSeconds',add,'B')
        n=self.set('Elapsed','real','0',sub='double',x=pos.get('x',0)+550,y=pos.get('y',0));self.wire(add,'ReturnValue',n,'Elapsed');self.chain(tick,n)
        return n
    def sight(self,controller,cp,target,tp,**pos):
        n=self.call('/Script/Engine.Controller','LineOfSightTo',pure=True,**pos).pin('Other','object',obj=ACTOR).pin('ViewPoint','struct',obj=VECTOR,default='0,0,0').pin('bAlternateChecks','bool',default='false').pin('ReturnValue','bool',out=True)
        self.wire(controller,cp,n,'self');self.wire(target,tp,n,'Other');return n
    def move_to(self,event,goal,pin,path=True,radius='80',**pos):
        n=self.call(CONTROLLER,'MoveToLocation',**pos).pin('Dest','struct',obj=VECTOR).pin('AcceptanceRadius','real',sub='float',default=radius).pin('bStopOnOverlap','bool',default='false').pin('bUsePathfinding','bool',default=str(path).lower()).pin('bProjectDestinationToNavigation','bool',default='true').pin('bCanStrafe','bool',default='false').pin('FilterClass','class',obj='/Script/NavigationSystem.NavigationQueryFilter').pin('bAllowPartialPath','bool',default='false').pin('ReturnValue','byte',obj='/Script/AIModule.EPathFollowingRequestResult',out=True)
        self.wire(event,'OwnerController',n,'self');self.wire(goal,pin,n,'Dest');return n
    def array(self,name,fn,*,item=None,ip=None,**pos):
        var=self.get(name,'object',obj=ACTOR,x=pos.get('x',0),y=pos.get('y',0)+200);var.pins[name]['container']='Array'
        pure=fn in ('Array_Contains','Array_Length')
        n=self.call('/Script/Engine.KismetArrayLibrary',fn,pure=pure,static=True,**pos).pin('TargetArray','object',obj=ACTOR)
        n.kind='BlueprintGraph.K2Node_CallArrayFunction'
        n.pins['TargetArray']['container']='Array';self.wire(var,name,n,'TargetArray')
        if item:
            n.pin('ItemToFind' if fn=='Array_Contains' else 'NewItem','object',obj=ACTOR);self.wire(item,ip,n,'ItemToFind' if fn=='Array_Contains' else 'NewItem')
        if fn=='Array_Contains':n.pin('ReturnValue','bool',out=True)
        if fn in ('Array_AddUnique','Array_Length'):n.pin('ReturnValue','int',out=True)
        return n

def base_enemy():
    g=CombatGraph();self=g.selfnode(x=0,y=500);bb=g.blackboard(self,'self',x=300,y=500)
    health=g.get('BPC_E_Health','object',obj=HEALTH,x=0,y=750)
    begin=g.event(ACTOR,'ReceiveBeginPlay',x=0,y=0)
    death=g.custom('Enemy_Death',x=0,y=3000).pin('OutputDelegate','delegate',out=True)
    changed=g.custom('OnHealthChanged',x=0,y=2100).pin('OutputDelegate','delegate',out=True)
    previous=begin
    for i,(name,event) in enumerate([('E_Dead',death),('E_Updated_Heatlh',changed)]):
        bind=g.node('K2Node_AddDelegate',['DelegateReference=(MemberParent='+q("/Script/Engine.BlueprintGeneratedClass'"+HEALTH+"'")+',MemberName='+q(name)+')'],x=350+i*350,y=0).pin('execute').pin('then',out=True).pin('self','object',obj=HEALTH).pin('Delegate','delegate')
        g.wire(health,'BPC_E_Health',bind,'self');g.wire(event,'OutputDelegate',bind,'Delegate');g.chain(previous,bind);previous=bind
    attack=g.event(ROOT+'/BPI_Enemy.BPI_Enemy_C','Attack',x=0,y=1000).pin('TargetActor','object',obj=ACTOR,out=True)
    dead=g.get('bIsDead','bool',x=0,y=1350);busy=g.get('bAttackInProgress','bool',x=0,y=1550)
    either=g.boolean('BooleanOR',dead,'bIsDead',busy,'bAttackInProgress',x=350,y=1350)
    allowed=g.boolean('Not_PreBool',either,'ReturnValue',x=650,y=1350)
    b=g.branch(x=950,y=1000);g.chain(attack,b);g.wire(allowed,'ReturnValue',b,'Condition')
    victim=g.set('AttackVictim','object',None,obj=ACTOR,x=1250,y=1000);g.chain(b,victim);g.wire(attack,'TargetActor',victim,'AttackVictim')
    flag=g.set('bAttackInProgress','bool','true',x=1550,y=1000);g.chain(victim,flag)
    play=g.montage(self,'self','AM_EnemyAttack_Entrega',x=1850,y=1000);g.chain(flag,play)
    strike=g.custom('ResolveAttack',x=0,y=4200)
    victimget=g.get('AttackVictim','object',obj=ACTOR,x=0,y=4500)
    valid=g.valid(victimget,'AttackVictim',x=300,y=4500)
    live=g.boolean('Not_PreBool',dead,'bIsDead',x=300,y=4700)
    active=g.boolean('BooleanAND',busy,'bAttackInProgress',live,'ReturnValue',x=600,y=4700)
    ready=g.boolean('BooleanAND',active,'ReturnValue',valid,'ReturnValue',x=900,y=4600)
    check=g.branch(x=1200,y=4200);g.chain(strike,check);g.wire(ready,'ReturnValue',check,'Condition')
    distance=g.dist(self,'self',victimget,'AttackVictim',x=1200,y=4800)
    near=g.compare('LessEqual_DoubleDouble','real','220',sub='double',x=1500,y=4800);g.wire(distance,'ReturnValue',near,'A')
    ctrl=g.ctrl(self,'self',x=1200,y=5100)
    sight=g.sight(ctrl,'ReturnValue',victimget,'AttackVictim',x=1500,y=5100)
    hittable=g.boolean('BooleanAND',near,'ReturnValue',sight,'ReturnValue',x=1800,y=4800)
    hit=g.branch(x=2100,y=4200);g.chain(check,hit);g.wire(hittable,'ReturnValue',hit,'Condition')
    damage=g.call('/Script/Engine.GameplayStatics','ApplyDamage',static=True,x=2400,y=4200).pin('DamagedActor','object',obj=ACTOR).pin('BaseDamage','real',sub='float',default='6').pin('EventInstigator','object',obj='/Script/Engine.Controller').pin('DamageCauser','object',obj=ACTOR).pin('DamageTypeClass','class',obj='/Script/Engine.DamageType').pin('ReturnValue','real',sub='float',out=True)
    g.chain(hit,damage);g.wire(victimget,'AttackVictim',damage,'DamagedActor');g.wire(ctrl,'ReturnValue',damage,'EventInstigator');g.wire(self,'self',damage,'DamageCauser')
    end=g.custom('EndAttack',x=0,y=5700)
    reset=g.set('bAttackInProgress','bool','false',x=350,y=5700);g.chain(end,reset)
    stop=g.stop_montage(self,'self','AM_EnemyAttack_Entrega',x=700,y=5700);g.chain(reset,stop)
    hp=g.get('E_Health','real',owner=HEALTH,sub='double',x=350,y=2450);g.wire(health,'BPC_E_Health',hp,'self')
    positive=g.compare('Greater_DoubleDouble','real','0',sub='double',x=650,y=2450);g.wire(hp,'E_Health',positive,'A')
    alive=g.branch(x=950,y=2100);g.chain(changed,alive);g.wire(positive,'ReturnValue',alive,'Condition')
    react=g.bbset(bb,'bReceivingDamage','Bool','true',x=1250,y=2100);g.chain(alive,react)
    setdead=g.set('bIsDead','bool','true',x=350,y=3000);g.chain(death,setdead)
    cancel=g.set('bAttackInProgress','bool','false',x=700,y=3000);g.chain(setdead,cancel)
    stopattack=g.stop_montage(self,'self','AM_EnemyAttack_Entrega',x=700,y=3200);g.chain(cancel,stopattack)
    controller=g.ctrl(self,'self',x=350,y=3350)
    cast=g.nativecast(CONTROLLER,x=1050,y=3000);g.chain(stopattack,cast);g.wire(controller,'ReturnValue',cast,'Object')
    brain=g.nativeget(CONTROLLER,'BrainComponent','object',obj='/Script/AIModule.BrainComponent',x=1050,y=3400);g.wire(cast,'AsAIController',brain,'self')
    stopbrain=g.call('/Script/AIModule.BrainComponent','StopLogic',x=1400,y=3000).pin('Reason','string',default='Enemy dead');g.chain(cast,stopbrain);g.wire(brain,'BrainComponent',stopbrain,'self')
    movement=g.nativeget(CHAR,'CharacterMovement','object',obj=MOVE,x=1400,y=3400)
    g.wire(self,'self',movement,'self')
    disable=g.call(MOVE,'DisableMovement',x=1750,y=3000);g.wire(movement,'CharacterMovement',disable,'self');g.chain(stopbrain,disable);g.chain(cast,disable,'CastFailed')
    collision=g.call(ACTOR,'SetActorEnableCollision',x=2100,y=3000).pin('bNewActorEnableCollision','bool',default='false');g.chain(disable,collision)
    deathplay=g.montage(self,'self','AM_EnemyDeath_Entrega',x=2450,y=3000);g.chain(collision,deathplay)
    lifespan=g.call(ACTOR,'SetLifeSpan',x=2800,y=3000).pin('InLifespan','real',sub='float',default='3.0');g.chain(deathplay,lifespan)
    amount=g.get('ContactDamage','real',sub='double',x=2100,y=5400);g.wire(amount,'ContactDamage',damage,'BaseDamage')
    g.write('BP_BaseEnemy')

def attack_task():
    g=CombatGraph();e=g.task_event('ReceiveExecuteAI',x=0,y=0);tick=g.task_event('ReceiveTickAI',x=0,y=1200);abort=g.task_event('ReceiveAbortAI',x=0,y=3000)
    bb=g.blackboard(e,'OwnerController',x=0,y=500);target=g.player(x=300,y=500)
    cast=g.cast(BASE,x=300,y=0);g.chain(e,cast);g.wire(e,'ControlledPawn',cast,'Object');g.finish(cast,'CastFailed',success=False,x=650,y=-200)
    cache=g.set('Enemy','object',None,obj=BASE,x=650,y=0);g.chain(cast,cache);g.wire(cast,'AsBP_BaseEnemy',cache,'Enemy')
    reset=g.set('Elapsed','real','0',sub='double',x=950,y=0);g.chain(cache,reset)
    hit=g.set('bHit','bool','false',x=1250,y=0);g.chain(reset,hit)
    stop=g.stop_move(e,x=1550,y=0);g.chain(hit,stop)
    out=g.call('/Script/Engine.KismetSystemLibrary','PrintString',static=True,x=1800,y=-200).pin('InString','string',default='Enemigo: va a atacar').pin('bPrintToScreen','bool',default='true').pin('bPrintToLog','bool',default='true').pin('Duration','real',sub='float',default='1.5');g.chain(stop,out)
    call=g.action('Attack',x=2100,y=0).pin('TargetActor','object',obj=ACTOR);g.chain(out,call);g.wire(cache,'Output_Get',call,'self');g.wire(target,'ReturnValue',call,'TargetActor')
    enemy=g.get('Enemy','object',obj=BASE,x=0,y=1800)
    elapsed=g.elapsed(tick,x=0,y=1200)
    crossed=g.compare('GreaterEqual_DoubleDouble','real','0.45',sub='double',x=900,y=1550);g.wire(elapsed,'Output_Get',crossed,'A')
    was=g.get('bHit','bool',x=900,y=1800);notyet=g.boolean('Not_PreBool',was,'bHit',x=1150,y=1800)
    impact=g.boolean('BooleanAND',crossed,'ReturnValue',notyet,'ReturnValue',x=1450,y=1550)
    b=g.branch(x=1750,y=1200);g.chain(elapsed,b);g.wire(impact,'ReturnValue',b,'Condition')
    mark=g.set('bHit','bool','true',x=2050,y=1100);g.chain(b,mark)
    strike=g.action('ResolveAttack',x=2350,y=1100);g.chain(mark,strike);g.wire(enemy,'Enemy',strike,'self')
    expired=g.compare('GreaterEqual_DoubleDouble','real','1.3',sub='double',x=2050,y=2000);g.wire(elapsed,'Output_Get',expired,'A')
    done=g.branch(x=2650,y=1600);g.chain(strike,done);g.chain(b,done,'else');g.wire(expired,'ReturnValue',done,'Condition')
    end=g.action('EndAttack',x=2950,y=1600);g.chain(done,end);g.wire(enemy,'Enemy',end,'self');g.finish(end,x=3250,y=1600)
    cancel=g.action('EndAttack',x=650,y=3000);g.chain(abort,cancel);g.wire(enemy,'Enemy',cancel,'self');g.finish(cancel,abort=True,x=950,y=3000)
    g.write('BTTask_Attack')

def hit_task():
    g=CombatGraph();e=g.task_event('ReceiveExecuteAI',x=0,y=0);abort=g.task_event('ReceiveAbortAI',x=0,y=800)
    play=g.montage(e,'ControlledPawn','AM_EnemyHit_Entrega',rate='3.0',x=300,y=0);g.chain(e,play)
    delay=g.call('/Script/Engine.KismetSystemLibrary','Delay',static=True,x=650,y=0).pin('Duration','real',sub='float',default='0.6');g.chain(play,delay)
    bb=g.blackboard(e,'OwnerController',x=650,y=400)
    clear=g.bbset(bb,'bReceivingDamage','Bool','false',x=1000,y=0);g.chain(delay,clear)
    out=g.call('/Script/Engine.KismetSystemLibrary','PrintString',static=True,x=1350,y=0).pin('InString','string',default='Enemigo: ya no recibe daño').pin('bPrintToScreen','bool',default='true').pin('bPrintToLog','bool',default='true').pin('Duration','real',sub='float',default='1.5');g.chain(clear,out);g.finish(out,x=1650,y=0)
    tag=g.call(ACTOR,'ActorHasTag',pure=True,x=1000,y=650).pin('Tag','name',default='Enemy.Charger').pin('ReturnValue','bool',out=True);g.wire(e,'ControlledPawn',tag,'self')
    orbiter=g.boolean('Not_PreBool',tag,'ReturnValue',x=1350,y=650);g.wire(orbiter,'ReturnValue',out,'bPrintToScreen');g.wire(orbiter,'ReturnValue',out,'bPrintToLog')
    stop=g.stop_montage(abort,'ControlledPawn','AM_EnemyHit_Entrega',x=350,y=800);g.chain(abort,stop);g.finish(stop,abort=True,x=700,y=800)
    g.write('BTTask_HitSun')

def controller():
    g=CombatGraph();e=g.event('/Script/Engine.Controller','ReceivePossess',x=0,y=0).pin('PossessedPawn','object',obj=PAWN,out=True)
    run=g.call(CONTROLLER,'RunBehaviorTree',x=350,y=0).pin('BTAsset','object',obj='/Script/AIModule.BehaviorTree',default_obj=ROOT+'/BT_Charger.BT_Charger').pin('ReturnValue','bool',out=True);g.chain(e,run)
    g.write('BP_ChargerController')

def sense():
    g=CombatGraph();e=g.event('/Script/AIModule.BTService_BlueprintBase','ReceiveTickAI',x=0,y=0).pin('OwnerController','object',obj=CONTROLLER,out=True).pin('ControlledPawn','object',obj=PAWN,out=True).pin('DeltaSeconds','real',sub='float',out=True)
    bb=g.blackboard(e,'OwnerController',x=0,y=400);player=g.player(x=0,y=650)
    distance=g.dist(e,'ControlledPawn',player,'ReturnValue',x=350,y=650)
    d=g.bbset(bb,'DistanceToTarget','Float',x=350,y=0);g.chain(e,d);g.wire(distance,'ReturnValue',d,'FloatValue')
    near=g.compare('LessEqual_DoubleDouble','real','1800',sub='double',x=650,y=650);g.wire(distance,'ReturnValue',near,'A')
    b=g.branch(x=950,y=0);g.chain(d,b);g.wire(near,'ReturnValue',b,'Condition')
    setp=g.bbset(bb,'TargetActor','Object',x=1250,y=0);g.chain(b,setp);g.wire(player,'ReturnValue',setp,'ObjectValue')
    clear=g.bbset(bb,'TargetActor','Object',x=1250,y=350);g.chain(b,clear,'else')
    g.write('BTService_ChargerSense')

def windup():
    g=CombatGraph();e=g.task_event('ReceiveExecuteAI',x=0,y=0);tick=g.task_event('ReceiveTickAI',x=0,y=900);abort=g.task_event('ReceiveAbortAI',x=0,y=2200)
    bb=g.blackboard(e,'OwnerController',x=0,y=400);target=g.player(x=300,y=400)
    stop=g.stop_move(e,x=300,y=0);g.chain(e,stop)
    reset=g.set('Elapsed','real','0',sub='double',x=600,y=0);g.chain(stop,reset)
    focus=g.call(CONTROLLER,'K2_SetFocus',x=900,y=0).pin('NewFocus','object',obj=ACTOR);g.chain(reset,focus);g.wire(e,'OwnerController',focus,'self');g.wire(target,'ReturnValue',focus,'NewFocus')
    play=g.montage(e,'ControlledPawn','AM_EnemyAttack_Entrega',rate='1.625',x=1200,y=0);g.chain(focus,play)
    elapsed=g.elapsed(tick,x=0,y=900)
    compare=g.compare('GreaterEqual_DoubleDouble','real','0.8',sub='double',x=900,y=1300);g.wire(elapsed,'Output_Get',compare,'A')
    b=g.branch(x=1200,y=900);g.chain(elapsed,b);g.wire(compare,'ReturnValue',b,'Condition')
    pos=g.location(target,'ReturnValue',x=1200,y=1500)
    goal=g.bbset(bb,'ChargeGoal','Vector',x=1500,y=900);g.chain(b,goal);g.wire(pos,'ReturnValue',goal,'VectorValue')
    charging=g.bbset(bb,'bCharging','Bool','true',x=1800,y=900);g.chain(goal,charging);g.finish(charging,x=2100,y=900)
    stopanim=g.stop_montage(abort,'ControlledPawn','AM_EnemyAttack_Entrega',x=350,y=2200);g.chain(abort,stopanim);g.finish(stopanim,abort=True,x=700,y=2200)
    g.write('BTTask_ChargerWindup')

def charge():
    g=CombatGraph();e=g.task_event('ReceiveExecuteAI',x=0,y=0);tick=g.task_event('ReceiveTickAI',x=0,y=1000);abort=g.task_event('ReceiveAbortAI',x=0,y=3000)
    bb=g.blackboard(e,'OwnerController',x=0,y=450);target=g.player(x=350,y=450);goal=g.bbget(bb,'ChargeGoal','Vector',x=650,y=450)
    reset=g.set('Elapsed','real','0',sub='double',x=350,y=0);g.chain(e,reset)
    mark=g.set('bHit','bool','false',x=650,y=0);g.chain(reset,mark)
    speed=g.speed(e,'900',x=950,y=0);g.chain(mark,speed)
    move=g.move_to(e,goal,'ReturnValue',path=False,radius='40',x=1250,y=0);g.chain(speed,move)
    elapsed=g.elapsed(tick,x=0,y=1000)
    distance=g.dist(tick,'ControlledPawn',target,'ReturnValue',x=350,y=1600)
    near=g.compare('LessEqual_DoubleDouble','real','180',sub='double',x=650,y=1600);g.wire(distance,'ReturnValue',near,'A')
    hit=g.get('bHit','bool',x=650,y=1900);notyet=g.boolean('Not_PreBool',hit,'bHit',x=950,y=1900)
    fresh=g.boolean('BooleanAND',near,'ReturnValue',notyet,'ReturnValue',x=1250,y=1800)
    sight=g.sight(tick,'OwnerController',target,'ReturnValue',x=1250,y=2100)
    valid=g.boolean('BooleanAND',fresh,'ReturnValue',sight,'ReturnValue',x=1550,y=1800)
    b=g.branch(x=1850,y=1000);g.chain(elapsed,b);g.wire(valid,'ReturnValue',b,'Condition')
    flag=g.set('bHit','bool','true',x=2150,y=1000);g.chain(b,flag)
    damage=g.call('/Script/Engine.GameplayStatics','ApplyDamage',static=True,x=2450,y=1000).pin('DamagedActor','object',obj=ACTOR).pin('BaseDamage','real',sub='float',default='6').pin('EventInstigator','object',obj='/Script/Engine.Controller').pin('DamageCauser','object',obj=ACTOR).pin('DamageTypeClass','class',obj='/Script/Engine.DamageType').pin('ReturnValue','real',sub='float',out=True)
    g.chain(flag,damage);g.wire(target,'ReturnValue',damage,'DamagedActor');g.wire(tick,'OwnerController',damage,'EventInstigator');g.wire(tick,'ControlledPawn',damage,'DamageCauser')
    expired=g.compare('GreaterEqual_DoubleDouble','real','1.0',sub='double',x=2150,y=2300);g.wire(elapsed,'Output_Get',expired,'A')
    donecond=g.boolean('BooleanOR',near,'ReturnValue',expired,'ReturnValue',x=2450,y=2300)
    done=g.branch(x=2800,y=1700);g.chain(damage,done);g.chain(b,done,'else');g.wire(donecond,'ReturnValue',done,'Condition')
    for previous,prevpin,event,y,isabort in [(done,'then',tick,1700,False),(abort,'then',abort,3000,True)]:
        stop=g.stop_move(event,x=3150 if not isabort else 350,y=y);g.chain(previous,stop,prevpin)
        speed=g.speed(event,'600',x=3500 if not isabort else 700,y=y);g.chain(stop,speed)
        clear=g.bbset(bb,'bCharging','Bool','false',x=3850 if not isabort else 1050,y=y);g.chain(speed,clear)
        retreat=g.bbset(bb,'bRetreat','Bool','true',x=4200 if not isabort else 1400,y=y);g.chain(clear,retreat)
        g.finish(retreat,abort=isabort,x=4550 if not isabort else 1750,y=y)
    pawn=g.get('CachedPawn','object',obj=BASE,x=2150,y=2700)
    amount=g.get('ContactDamage','real',owner=BASE,sub='double',x=2450,y=2700);g.wire(pawn,'CachedPawn',amount,'self');g.wire(amount,'ContactDamage',damage,'BaseDamage')
    g.write('BTTask_ChargerCharge')

def retreat():
    g=CombatGraph();e=g.task_event('ReceiveExecuteAI',x=0,y=0);tick=g.task_event('ReceiveTickAI',x=0,y=3500);abort=g.task_event('ReceiveAbortAI',x=0,y=4700)
    reset=g.set('Elapsed','real','0',sub='double',x=350,y=0);g.chain(e,reset)
    best=g.set('BestDistance','real','100000',sub='double',x=650,y=0);g.chain(reset,best)
    clear=g.set('SafeCandidate','object',None,obj=ACTOR,x=950,y=0);g.chain(best,clear)
    points=g.call('/Script/Engine.GameplayStatics','GetAllActorsWithTag',static=True,x=1250,y=0).pin('Tag','name',default='RefugioRehen').pin('OutActors','object',obj=ACTOR,out=True)
    points.pins['OutActors']['container']='Array';g.chain(clear,points)
    loop=g.foreach(points,'OutActors',x=1550,y=0);g.chain(points,loop,nextpin='Exec')
    player=g.player(x=1550,y=700)
    far=g.dist(loop,'Array Element',player,'ReturnValue',x=1850,y=700)
    enough=g.compare('GreaterEqual_DoubleDouble','real','1100',sub='double',x=2150,y=700);g.wire(far,'ReturnValue',enough,'A')
    distance=g.dist(loop,'Array Element',e,'ControlledPawn',x=1850,y=1000)
    bestget=g.get('BestDistance','real',sub='double',x=1850,y=1200)
    closer=g.compare('Less_DoubleDouble','real','100000',sub='double',x=2150,y=1000);g.wire(distance,'ReturnValue',closer,'A');g.wire(bestget,'BestDistance',closer,'B')
    candidate=g.boolean('BooleanAND',enough,'ReturnValue',closer,'ReturnValue',x=2450,y=800)
    b=g.branch(x=2750,y=0);g.chain(loop,b,'LoopBody');g.wire(candidate,'ReturnValue',b,'Condition')
    start=g.location(e,'ControlledPawn',x=2450,y=1200);end=g.location(loop,'Array Element',x=2750,y=1200)
    playerpos=g.location(player,'ReturnValue',x=2450,y=1550)
    def difference(a,ap,b,bp,x,y):
        n=g.call('/Script/Engine.KismetMathLibrary','Subtract_VectorVector',pure=True,static=True,x=x,y=y).pin('A','struct',obj=VECTOR).pin('B','struct',obj=VECTOR).pin('ReturnValue','struct',obj=VECTOR,out=True);g.wire(a,ap,n,'A');g.wire(b,bp,n,'B');return n
    away=difference(start,'ReturnValue',playerpos,'ReturnValue',2750,1550)
    direction=difference(end,'ReturnValue',start,'ReturnValue',3050,1550)
    dot=g.call('/Script/Engine.KismetMathLibrary','Dot_VectorVector',pure=True,static=True,x=3350,y=1550).pin('A','struct',obj=VECTOR).pin('B','struct',obj=VECTOR).pin('ReturnValue','real',sub='double',out=True);g.wire(away,'ReturnValue',dot,'A');g.wire(direction,'ReturnValue',dot,'B')
    outward=g.compare('Greater_DoubleDouble','real','0',sub='double',x=3650,y=1550);g.wire(dot,'ReturnValue',outward,'A')
    path=g.call('/Script/NavigationSystem.NavigationSystemV1','FindPathToLocationSynchronously',static=True,x=3050,y=0).pin('WorldContextObject','object',obj=OBJECT,hidden=True).pin('PathStart','struct',obj=VECTOR).pin('PathEnd','struct',obj=VECTOR).pin('PathfindingContext','object',obj=ACTOR).pin('FilterClass','class',obj='/Script/NavigationSystem.NavigationQueryFilter').pin('ReturnValue','object',obj='/Script/NavigationSystem.NavigationPath',out=True)
    g.chain(b,path);g.wire(start,'ReturnValue',path,'PathStart');g.wire(end,'ReturnValue',path,'PathEnd');g.wire(e,'ControlledPawn',path,'PathfindingContext')
    valid=g.call('/Script/NavigationSystem.NavigationPath','IsValid',pure=True,x=3350,y=700).pin('ReturnValue','bool',out=True);g.wire(path,'ReturnValue',valid,'self')
    partial=g.call('/Script/NavigationSystem.NavigationPath','IsPartial',pure=True,x=3350,y=1000).pin('ReturnValue','bool',out=True);g.wire(path,'ReturnValue',partial,'self')
    full=g.boolean('Not_PreBool',partial,'ReturnValue',x=3650,y=1000)
    pathok=g.boolean('BooleanAND',valid,'ReturnValue',full,'ReturnValue',x=3950,y=800)
    reachable=g.boolean('BooleanAND',pathok,'ReturnValue',outward,'ReturnValue',x=3950,y=1200)
    pb=g.branch(x=4250,y=0);g.chain(path,pb);g.wire(reachable,'ReturnValue',pb,'Condition')
    save=g.set('SafeCandidate','object',None,obj=ACTOR,x=4550,y=0);g.chain(pb,save);g.wire(loop,'Array Element',save,'SafeCandidate')
    score=g.set('BestDistance','real','100000',sub='double',x=4850,y=0);g.chain(save,score);g.wire(distance,'ReturnValue',score,'BestDistance')
    chosen=g.get('SafeCandidate','object',obj=ACTOR,x=1850,y=2200)
    has=g.valid(chosen,'SafeCandidate',x=2150,y=2200)
    choose=g.branch(x=2450,y=1800);g.chain(loop,choose,'Completed');g.wire(has,'ReturnValue',choose,'Condition')
    goal=g.location(chosen,'SafeCandidate',x=2750,y=2200)
    move=g.move_to(e,goal,'ReturnValue',radius='80',x=3050,y=1800);g.chain(choose,move)
    g.finish(choose,'else',x=2750,y=2700)
    elapsed=g.elapsed(tick,x=0,y=3500)
    currentdist=g.dist(tick,'ControlledPawn',player,'ReturnValue',x=650,y=4000)
    safe=g.compare('GreaterEqual_DoubleDouble','real','1000',sub='double',x=950,y=4000);g.wire(currentdist,'ReturnValue',safe,'A')
    expired=g.compare('GreaterEqual_DoubleDouble','real','4.0',sub='double',x=950,y=4300);g.wire(elapsed,'Output_Get',expired,'A')
    done=g.boolean('BooleanOR',safe,'ReturnValue',expired,'ReturnValue',x=1250,y=4100)
    finish=g.branch(x=1550,y=3500);g.chain(elapsed,finish);g.wire(done,'ReturnValue',finish,'Condition')
    stop=g.stop_move(tick,x=1850,y=3500);g.chain(finish,stop);g.finish(stop,x=2150,y=3500)
    cancel=g.stop_move(abort,x=350,y=4700);g.chain(abort,cancel);g.finish(cancel,abort=True,x=700,y=4700)
    g.write('BTTask_ChargerRetreat')

def recover():
    g=CombatGraph();e=g.task_event('ReceiveExecuteAI',x=0,y=0);bb=g.blackboard(e,'OwnerController',x=0,y=350)
    clear=g.bbset(bb,'bRetreat','Bool','false',x=350,y=0);g.chain(e,clear);g.finish(clear,x=700,y=0)
    g.write('BTTask_ChargerRecover')

if __name__=='__main__':
    base_enemy();attack_task();hit_task();controller();sense();windup();charge();retreat();recover()
