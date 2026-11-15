"""Local: Blueprint clipboard sources for the hostage's Behavior Tree implementation."""
from generate_delivery_graphs import Graph, ACTOR, PAWN, OBJECT, ref, q

ROOT='/Game/ThirdPerson/Blueprints/Aliado'
ENEMY='/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C'
BB='/Script/AIModule.BlackboardComponent'
CONTROLLER='/Script/AIModule.AIController'
VECTOR='/Script/CoreUObject.Vector'

class HostageGraph(Graph):
    def blackboard(self,owner,pin,x=0,y=0):
        n=self.call('/Script/AIModule.AIBlueprintHelperLibrary','GetBlackboard',pure=True,static=True,x=x,y=y).pin('Target','object',obj=ACTOR).pin('ReturnValue','object',obj=BB,out=True)
        self.wire(owner,pin,n,'Target');return n
    def bbget(self,bb,key,kind='Bool',x=0,y=0):
        cat,obj,sub={'Bool':('bool',None,''),'Int':('int',None,''),'Float':('real',None,'float'),'Object':('object',OBJECT,''),'Vector':('struct',VECTOR,'')}[kind]
        n=self.call(BB,'GetValueAs'+kind,pure=True,x=x,y=y).pin('KeyName','name').pin('ReturnValue',cat,obj=obj,sub=sub,out=True)
        literal=self.call('/Script/Engine.KismetSystemLibrary','MakeLiteralName',pure=True,static=True,x=x-150,y=y+170).pin('Value','name',default=key).pin('ReturnValue','name',out=True)
        self.wire(literal,'ReturnValue',n,'KeyName')
        self.wire(bb,'ReturnValue',n,'self');return n
    def bbset(self,bb,key,kind,value=None,x=0,y=0):
        cat,obj,sub={'Bool':('bool',None,''),'Int':('int',None,''),'Float':('real',None,'float'),'Object':('object',OBJECT,''),'Vector':('struct',VECTOR,'')}[kind]
        n=self.call(BB,'SetValueAs'+kind,x=x,y=y).pin('KeyName','name').pin(kind+'Value',cat,obj=obj,sub=sub,default=value)
        literal=self.call('/Script/Engine.KismetSystemLibrary','MakeLiteralName',pure=True,static=True,x=x-150,y=y+170).pin('Value','name',default=key).pin('ReturnValue','name',out=True)
        self.wire(literal,'ReturnValue',n,'KeyName')
        self.wire(bb,'ReturnValue',n,'self');return n
    def chain(self,prev,next,prevpin='then',nextpin='execute'):
        self.wire(prev,prevpin,next,nextpin);return next
    def valid(self,owner,pin,x=0,y=0):
        n=self.call('/Script/Engine.KismetSystemLibrary','IsValid',pure=True,static=True,x=x,y=y).pin('Object','object',obj=OBJECT).pin('ReturnValue','bool',out=True)
        self.wire(owner,pin,n,'Object');return n
    def boolean(self,fn,a,ap,b=None,bp=None,x=0,y=0):
        n=self.call('/Script/Engine.KismetMathLibrary',fn,pure=True,static=True,x=x,y=y).pin('A','bool').pin('ReturnValue','bool',out=True)
        self.wire(a,ap,n,'A')
        if b:n.pin('B','bool');self.wire(b,bp,n,'B')
        return n
    def location(self,node,pin,x=0,y=0):
        n=self.call(ACTOR,'K2_GetActorLocation',pure=True,x=x,y=y).pin('ReturnValue','struct',obj=VECTOR,out=True)
        self.wire(node,pin,n,'self');return n
    def dist(self,a,ap,b,bp,x=0,y=0):
        n=self.call(ACTOR,'GetDistanceTo',pure=True,x=x,y=y).pin('OtherActor','object',obj=ACTOR).pin('ReturnValue','real',sub='float',out=True)
        self.wire(a,ap,n,'self');self.wire(b,bp,n,'OtherActor');return n
    def foreach(self,node,pin,typ=ACTOR,x=0,y=0):
        n=self.node('K2Node_MacroInstance',['MacroGraphReference=(MacroGraph="/Script/Engine.EdGraph\'/Engine/EditorBlueprintResources/StandardMacros.StandardMacros:ForEachLoop\'",GraphBlueprint="/Script/Engine.Blueprint\'/Engine/EditorBlueprintResources/StandardMacros.StandardMacros\'")'],x=x,y=y).pin('Exec').pin('Array','object',obj=typ).pin('LoopBody',out=True).pin('Array Element','object',obj=typ,out=True).pin('Array Index','int',out=True).pin('Completed',out=True)
        n.pins['Array']['container']='Array';self.wire(node,pin,n,'Array');return n
    def state(self,bb,index,**pos):return self.bbset(bb,'Estado','Int',str(index),**pos)

def controller():
    g=HostageGraph()
    e=g.event(ACTOR,'ReceiveBeginPlay',x=0,y=0)
    run=g.call(CONTROLLER,'RunBehaviorTree',x=300,y=0).pin('BTAsset','object',obj='/Script/AIModule.BehaviorTree',default_obj=ROOT+'/BT_Hostage.BT_Hostage').pin('ReturnValue','bool',out=True)
    g.chain(e,run)
    # GetBlackboard defaults its Target to self on a controller.
    selfnode=g.node('K2Node_Self',x=0,y=300).pin('self','object',obj=CONTROLLER,out=True)
    bb=g.blackboard(selfnode,'self',x=300,y=300)
    waiting=g.bbset(bb,'bWaiting','Bool','true',x=650,y=0);g.chain(run,waiting)
    g.write('BP_HostageController')

def hostage():
    g=HostageGraph()
    pawn=g.node('K2Node_Self',x=0,y=500).pin('self','object',obj=PAWN,out=True)
    ctrl=g.call(PAWN,'GetController',pure=True,x=250,y=500).pin('ReturnValue','object',obj='/Script/Engine.Controller',out=True)
    g.wire(pawn,'self',ctrl,'self')
    bb=g.blackboard(ctrl,'ReturnValue',x=550,y=500)
    flee=g.bbget(bb,'bMustFlee',x=850,y=600);enemy=g.bbget(bb,'bEnemyNear',x=850,y=800)
    unsafe=g.boolean('BooleanOR',flee,'ReturnValue',enemy,'ReturnValue',x=1100,y=700)
    safe=g.boolean('Not_PreBool',unsafe,'ReturnValue',x=1350,y=700)
    player=g.player(x=0,y=850)
    dist=g.dist(pawn,'self',player,'ReturnValue',x=250,y=850)
    near=g.compare('LessEqual_DoubleDouble','real','400',sub='double',x=550,y=900);g.wire(dist,'ReturnValue',near,'A')
    allowed=g.boolean('BooleanAND',safe,'ReturnValue',near,'ReturnValue',x=1650,y=800)
    branch=g.branch(x=1950,y=0);g.wire(allowed,'ReturnValue',branch,'Condition')
    interact=g.node('K2Node_CustomEvent',['CustomFunctionName="Interactuar"'],x=0,y=0).pin('then',out=True)
    g.wire(interact,'then',branch,'execute')
    prev=branch
    for i,(key,value) in enumerate([('bRescued','true'),('bWaiting','false'),('bAccompanying','true')]):
        n=g.bbset(bb,key,'Bool',value,x=2250+i*300,y=0);g.chain(prev,n,'then');prev=n
    state=g.state(bb,1,x=3200,y=0);g.chain(prev,state)
    g.write('BP_Hostage')

def arrive():
    g=HostageGraph()
    e=g.event('/Script/AIModule.BTTask_BlueprintBase','ReceiveExecuteAI',x=0,y=0).pin('OwnerController','object',obj=CONTROLLER,out=True).pin('ControlledPawn','object',obj=PAWN,out=True)
    bb=g.blackboard(e,'OwnerController',x=0,y=300)
    prev=e
    for i,(key,value) in enumerate([('bMustFlee','false'),('bWaiting','true'),('bAccompanying','false')]):
        n=g.bbset(bb,key,'Bool',value,x=300+i*300,y=0);g.chain(prev,n);prev=n
    state=g.state(bb,3,x=1200,y=0);g.chain(prev,state)
    finish=g.call('/Script/AIModule.BTTask_BlueprintBase','FinishExecute',x=1500,y=0).pin('bSuccess','bool',default='true');g.chain(state,finish)
    g.write('BTTask_HostageArrive')

def sense():
    g=HostageGraph()
    e=g.event('/Script/AIModule.BTService_BlueprintBase','ReceiveTickAI',x=0,y=0).pin('OwnerController','object',obj=CONTROLLER,out=True).pin('ControlledPawn','object',obj=PAWN,out=True).pin('DeltaSeconds','real',sub='float',out=True)
    bb=g.blackboard(e,'OwnerController',x=0,y=300)
    player=g.player(x=0,y=600)
    pset=g.bbset(bb,'PlayerActor','Object',x=350,y=0);g.wire(player,'ReturnValue',pset,'ObjectValue');g.chain(e,pset)
    pdist=g.dist(e,'ControlledPawn',player,'ReturnValue',x=350,y=600)
    dset=g.bbset(bb,'DistanceToPlayer','Float',x=650,y=0);g.wire(pdist,'ReturnValue',dset,'FloatValue');g.chain(pset,dset)
    clear=g.set('ThreatActor','object',None,obj=ACTOR,x=950,y=0);g.chain(dset,clear)
    enemies=g.call('/Script/Engine.GameplayStatics','GetAllActorsOfClass',static=True,x=1250,y=0).pin('ActorClass','class',obj=ACTOR,default_obj=ENEMY).pin('OutActors','object',obj=ENEMY,out=True)
    enemies.pins['OutActors']['container']='Array';g.chain(clear,enemies)
    loop=g.foreach(enemies,'OutActors',typ=ENEMY,x=1600,y=0);g.chain(enemies,loop,nextpin='Exec')
    dead=g.get('bIsDead','bool',owner=ENEMY,x=1600,y=400);g.wire(loop,'Array Element',dead,'self')
    living=g.boolean('Not_PreBool',dead,'bIsDead',x=1850,y=400)
    distance=g.dist(loop,'Array Element',e,'ControlledPawn',x=1600,y=650)
    radius=g.get('ThreatRadius','real',sub='double',x=1600,y=850)
    close=g.compare('LessEqual_DoubleDouble','real','800',sub='double',x=1900,y=650);g.wire(distance,'ReturnValue',close,'A');g.wire(radius,'ThreatRadius',close,'B')
    danger=g.boolean('BooleanAND',living,'ReturnValue',close,'ReturnValue',x=2200,y=500)
    sight=g.call('/Script/Engine.Controller','LineOfSightTo',pure=True,x=2200,y=800).pin('Other','object',obj=ACTOR).pin('ViewPoint','struct',obj=VECTOR,default='0,0,0').pin('bAlternateChecks','bool',default='false').pin('ReturnValue','bool',out=True)
    g.wire(e,'OwnerController',sight,'self');g.wire(loop,'Array Element',sight,'Other')
    visible=g.boolean('BooleanAND',danger,'ReturnValue',sight,'ReturnValue',x=2450,y=600)
    b=g.branch(x=2750,y=0);g.chain(loop,b,'LoopBody');g.wire(visible,'ReturnValue',b,'Condition')
    threat=g.set('ThreatActor','object',None,obj=ACTOR,x=2800,y=0);g.chain(b,threat);g.wire(loop,'Array Element',threat,'ThreatActor')
    tget=g.get('ThreatActor','object',obj=ACTOR,x=1600,y=1250)
    valid=g.valid(tget,'ThreatActor',x=1850,y=1250)
    enemynear=g.bbset(bb,'bEnemyNear','Bool',x=2200,y=1100);g.chain(loop,enemynear,'Completed');g.wire(valid,'ReturnValue',enemynear,'BoolValue')
    rescued=g.bbget(bb,'bRescued',x=1850,y=1500)
    fleeing=g.bbget(bb,'bMustFlee',x=1850,y=1700)
    notfleeing=g.boolean('Not_PreBool',fleeing,'ReturnValue',x=2100,y=1700)
    seenrescued=g.boolean('BooleanAND',valid,'ReturnValue',rescued,'ReturnValue',x=2400,y=1450)
    request=g.boolean('BooleanAND',seenrescued,'ReturnValue',notfleeing,'ReturnValue',x=2650,y=1500)
    choose=g.branch(x=2950,y=1100);g.chain(enemynear,choose);g.wire(request,'ReturnValue',choose,'Condition')
    resetcandidate=g.set('SafeCandidate','object',None,obj=ACTOR,x=3250,y=1100);g.chain(choose,resetcandidate)
    resetbest=g.set('BestDistance','real','100000',sub='double',x=3550,y=1100);g.chain(resetcandidate,resetbest)
    points=g.call('/Script/Engine.GameplayStatics','GetAllActorsWithTag',static=True,x=3850,y=1100).pin('Tag','name',default='RefugioRehen').pin('OutActors','object',obj=ACTOR,out=True)
    points.pins['OutActors']['container']='Array';g.chain(resetbest,points)
    plo=g.foreach(points,'OutActors',x=4200,y=1100);g.chain(points,plo,nextpin='Exec')
    candidate=g.set('Candidate','object',None,obj=ACTOR,x=4500,y=1100);g.chain(plo,candidate,'LoopBody');g.wire(plo,'Array Element',candidate,'Candidate')
    resetmin=g.set('MinEnemyDistance','real','100000',sub='double',x=4800,y=1100);g.chain(candidate,resetmin)
    elo=g.foreach(enemies,'OutActors',typ=ENEMY,x=5100,y=1100);g.chain(resetmin,elo,nextpin='Exec')
    cget=g.get('Candidate','object',obj=ACTOR,x=4500,y=1800)
    edeath=g.get('bIsDead','bool',owner=ENEMY,x=5100,y=1500);g.wire(elo,'Array Element',edeath,'self')
    alive=g.boolean('Not_PreBool',edeath,'bIsDead',x=5350,y=1500)
    ab=g.branch(x=5650,y=1100);g.chain(elo,ab,'LoopBody');g.wire(alive,'ReturnValue',ab,'Condition')
    edist=g.dist(cget,'Candidate',elo,'Array Element',x=5100,y=1800)
    mind=g.get('MinEnemyDistance','real',sub='double',x=5100,y=2000)
    minimum=g.call('/Script/Engine.KismetMathLibrary','FMin',pure=True,static=True,x=5400,y=1850).pin('A','real',sub='double').pin('B','real',sub='double').pin('ReturnValue','real',sub='double',out=True)
    g.wire(edist,'ReturnValue',minimum,'A');g.wire(mind,'MinEnemyDistance',minimum,'B')
    savemin=g.set('MinEnemyDistance','real','100000',sub='double',x=5950,y=1100);g.chain(ab,savemin);g.wire(minimum,'ReturnValue',savemin,'MinEnemyDistance')
    dp=g.dist(cget,'Candidate',player,'ReturnValue',x=5100,y=2500)
    safeplayer=g.get('SafePlayerDistance','real',sub='double',x=5100,y=2700)
    cp=g.compare('GreaterEqual_DoubleDouble','real','1000',sub='double',x=5400,y=2500);g.wire(dp,'ReturnValue',cp,'A');g.wire(safeplayer,'SafePlayerDistance',cp,'B')
    safeenemy=g.get('SafeEnemyDistance','real',sub='double',x=5100,y=3000)
    ce=g.compare('GreaterEqual_DoubleDouble','real','1200',sub='double',x=5400,y=2900);g.wire(mind,'MinEnemyDistance',ce,'A');g.wire(safeenemy,'SafeEnemyDistance',ce,'B')
    safe=g.boolean('BooleanAND',cp,'ReturnValue',ce,'ReturnValue',x=5700,y=2700)
    fromself=g.dist(cget,'Candidate',e,'ControlledPawn',x=5100,y=3300)
    best=g.get('BestDistance','real',sub='double',x=5100,y=3500)
    nearer=g.compare('Less_DoubleDouble','real','100000',sub='double',x=5400,y=3300);g.wire(fromself,'ReturnValue',nearer,'A');g.wire(best,'BestDistance',nearer,'B')
    test=g.boolean('BooleanAND',safe,'ReturnValue',nearer,'ReturnValue',x=6000,y=3000)
    candidatebranch=g.branch(x=6300,y=2300);g.chain(elo,candidatebranch,'Completed');g.wire(test,'ReturnValue',candidatebranch,'Condition')
    source=g.location(e,'ControlledPawn',x=6000,y=3600);dest=g.location(cget,'Candidate',x=6300,y=3600)
    path=g.call('/Script/NavigationSystem.NavigationSystemV1','FindPathToLocationSynchronously',static=True,x=6650,y=2300).pin('WorldContextObject','object',obj=OBJECT,hidden=True).pin('PathStart','struct',obj=VECTOR).pin('PathEnd','struct',obj=VECTOR).pin('PathfindingContext','object',obj=ACTOR).pin('FilterClass','class',obj='/Script/NavigationSystem.NavigationQueryFilter').pin('ReturnValue','object',obj='/Script/NavigationSystem.NavigationPath',out=True)
    g.chain(candidatebranch,path);g.wire(source,'ReturnValue',path,'PathStart');g.wire(dest,'ReturnValue',path,'PathEnd');g.wire(e,'ControlledPawn',path,'PathfindingContext')
    pvalid=g.call('/Script/NavigationSystem.NavigationPath','IsValid',pure=True,x=7000,y=2800).pin('ReturnValue','bool',out=True);g.wire(path,'ReturnValue',pvalid,'self')
    partial=g.call('/Script/NavigationSystem.NavigationPath','IsPartial',pure=True,x=7000,y=3000).pin('ReturnValue','bool',out=True);g.wire(path,'ReturnValue',partial,'self')
    full=g.boolean('Not_PreBool',partial,'ReturnValue',x=7300,y=3000)
    reachable=g.boolean('BooleanAND',pvalid,'ReturnValue',full,'ReturnValue',x=7600,y=2850)
    pb=g.branch(x=7900,y=2300);g.chain(path,pb);g.wire(reachable,'ReturnValue',pb,'Condition')
    save=g.set('SafeCandidate','object',None,obj=ACTOR,x=8200,y=2300);g.chain(pb,save);g.wire(cget,'Candidate',save,'SafeCandidate')
    score=g.set('BestDistance','real','100000',sub='double',x=8500,y=2300);g.chain(save,score);g.wire(fromself,'ReturnValue',score,'BestDistance')
    chosen=g.get('SafeCandidate','object',obj=ACTOR,x=4500,y=4200)
    has=g.valid(chosen,'SafeCandidate',x=4800,y=4200)
    fb=g.branch(x=5100,y=4100);g.chain(plo,fb,'Completed');g.wire(has,'ReturnValue',fb,'Condition')
    pos=g.location(chosen,'SafeCandidate',x=5100,y=4500)
    loc=g.bbset(bb,'FleeLocation','Vector',x=5400,y=4100);g.chain(fb,loc);g.wire(pos,'ReturnValue',loc,'VectorValue')
    prev=loc
    for i,(key,value) in enumerate([('bWaiting','false'),('bAccompanying','false'),('bMustFlee','true')]):
        n=g.bbset(bb,key,'Bool',value,x=5700+i*300,y=4100);g.chain(prev,n);prev=n
    state=g.state(bb,2,x=6600,y=4100);g.chain(prev,state)
    # If there is temporarily no safe route, hold and wait for another sense tick.
    hold=g.bbset(bb,'bAccompanying','Bool','false',x=5400,y=4900);g.chain(fb,hold,'else')
    wait=g.bbset(bb,'bWaiting','Bool','true',x=5700,y=4900);g.chain(hold,wait)
    statewait=g.state(bb,3,x=6000,y=4900);g.chain(wait,statewait)
    g.write('BTService_HostageSense')

if __name__=='__main__':
    controller();hostage();arrive();sense()
