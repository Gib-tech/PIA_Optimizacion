"""Random beacon challenge. Authoring only; packaged gameplay uses Blueprints/BTs."""
from generate_delivery_controls import ControlsGraph, split_exec
from generate_progression_graphs import (capture,legacy_progression_director,ACTOR,OBJECT,
    MATH,GS,BEACON,DOOR,DIRECTOR,HERO,HOSTAGE,ZONE,SM,SMC,PRIM)
from generate_delivery_graphs import q
from delivery_save_schema import GI
from itertools import permutations

ORDERS=list(permutations(range(3)))
ART='/Game/ThirdPerson/Environment/Baliza/'
LABEL='/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconLabel.BP_BeaconLabel_C'
POWERED='/Game/ThirdPerson/Environment/Progression/M_DoorPowered.M_DoorPowered'

def power_door(g,prev,door):
    comp=g.v('StaticMeshComponent','object',owner=SM,target=door,obj=SMC,native=True)
    return g.action_on(prev,PRIM,'SetMaterial',comp,[('ElementIndex','int',2,None),('Material','object',None,'/Script/Engine.MaterialInterface')])

def table(g,index,values,cat='int',obj=None):
    n=g.node('K2Node_Select',['NumOptionPins='+str(len(values)),'IndexPinType=(PinCategory="int")'])
    n.pin('Index','int').pin('ReturnValue',cat,obj=obj,out=True);g.w(index,n,'Index')
    for i,value in enumerate(values):
        n.pin('Option '+str(i),cat,obj=obj);g.w(value,n,'Option '+str(i))
    return n,'ReturnValue'

def identity(g,code,step):
    step=g.c(MATH,'Clamp',[('Value','int',step),('Min','int',0),('Max','int',2)],cat='int')
    return table(g,step,[table(g,code,[p[i] for p in ORDERS]) for i in range(3)])

def director():
    g=capture(legacy_progression_director);g.__class__=ControlsGraph
    # Keep generated node names distinct after removal in the original recipe.
    base=ControlsGraph.node.__get__(g)
    def unique(kind,props=(),**pos):
        n=base(kind,props,**pos)
        while sum(x.name==n.name for x in g.nodes)>1:n.name+='Q'
        return n
    g.node=unique
    code=g.v('OrderCode','int');step=g.v('Paso','int');target=identity(g,code,step)
    switch=next(n for n in g.nodes if n.kind.endswith('K2Node_SwitchInteger'))
    for name,pid in switch.pins['Selection']['links']:
        src=next(n for n in g.nodes if n.name==name)
        next(p for p in src.pins.values() if p['id']==pid)['links'].remove((switch.name,switch.pins['Selection']['id']))
    switch.pins['Selection']['links']=[];g.w(target,switch,'Selection')
    # R explicitly starts a new attempt; Continue restores the saved attempt.
    for n in g.nodes:
        if any('MemberName="bDeliveryContinue"' in p for p in n.props) and 'execute' in n.pins:
            for name,pid in n.pins['bDeliveryContinue']['links']:
                src=next(x for x in g.nodes if x.name==name)
                next(p for p in src.pins.values() if p['id']==pid)['links'].remove((n.name,n.pins['bDeliveryContinue']['id']))
            n.pins['bDeliveryContinue']['links']=[];n.pins['bDeliveryContinue']['default']='false'
    begin=g.event(ACTOR,'ReceiveBeginPlay')
    gi=g.c(GS,'GetGameInstance',cat='object',obj='/Script/Engine.GameInstance')
    cast,instance=g.cast_after(begin,gi,GI)
    last=g.v('LastBeaconOrder','int',owner=GI,target=instance)
    random=g.c(MATH,'RandomInteger',[('Max','int',6)],cat='int')
    prev=g.s(cast,'OrderCode',random,'int')
    repeat=g.br(prev,g.cmp('EqualEqual_IntInt',code,last,'int'))
    # Uniformly choose among the other five permutations when a draw repeats.
    alternative=g.op('Percent_IntInt',g.op('Add_IntInt',last,g.op('Add_IntInt',g.c(MATH,'RandomInteger',[('Max','int',5)],cat='int'),1,'int'),'int'),6,'int')
    reroll=g.s(repeat,'OrderCode',alternative,'int')
    remember=g.s(reroll,'LastBeaconOrder',code,'int',owner=GI,target=instance);g.chain(repeat,remember,'else')
    chosen=table(g,target,[g.v('Baliza'+str(i),'object',obj=SM) for i in (1,2,3)],'object',SM)
    g.s(remember,'CurrentBeacon',chosen,'object',obj=SM)
    tick=next(n for n in g.nodes if n.kind.endswith('K2Node_Event') and any('ReceiveTick' in p for p in n.props))
    seq=split_exec(g,tick)
    cache=g.s(seq,'CurrentBeacon',chosen,'object',obj=SM,pin='then_1')
    work=g.node('K2Node_ExecutionSequence').pin('execute')
    for i in range(3):work.pin('then_'+str(i),out=True)
    g.chain(cache,work)
    h=g.call(GS,'GetActorOfClass',static=True).pin('ActorClass','class',obj=ACTOR,default_obj=HOSTAGE).pin('ReturnValue','object',obj=HOSTAGE,out=True)
    g.chain(work,h,'then_0');bb=g.blackboard(h,'ReturnValue')
    running=g.both(g.both(g.cmp('Less_IntInt',step,4,'int'),(g.bbget(bb,'bRescued'),'ReturnValue')),g.neg(g.v('bNarrativePaused','bool')))
    timer=g.br(h,running)
    g.s(timer,'MissionElapsed',g.op('Add_DoubleDouble',g.v('MissionElapsed'),(tick,'DeltaSeconds')))
    # The first two doors now reward completed encounters, making the entire
    # beacon courtyard reachable before any randomly selected activation.
    for i in (1,2):
        zone=g.v('Zona'+str(i),'object',obj=ZONE)
        b=g.v('Baliza'+str(i),'object',obj=SM)
        cast,beacon=g.cast_after(work,b,BEACON,pin='then_'+str(i))
        door=g.v('Door','object',owner=BEACON,target=beacon,obj=DOOR)
        ready=g.both(g.v('bCleared','bool',owner=ZONE,target=zone),g.neg(g.v('bUnlocked','bool',owner=DOOR,target=door)))
        ready=g.both(ready,g.cmp('Less_IntInt',step,4,'int'))
        test=g.br(cast,ready);prev=g.s(test,'bUnlocked',True,'bool',owner=DOOR,target=door)
        prev=power_door(g,prev,door);prev.pins['Material']['default_obj']=POWERED
        hero=g.player();hc,hp=g.cast_after(prev,(hero,'ReturnValue'),HERO)
        g.action_on(hc,HERO,'GrantHammerUpgrade',hp,[('Door','object',door,DOOR)])
    from generate_cinematic_graphs import terminal_hooks
    terminal_hooks(g)
    from add_result_gamepad_aliases import add_result_aliases
    add_result_aliases(g)
    g.write('BP_DirectorEntrega')

def beacon():
    g=ControlsGraph();e=g.custom('CompleteActivation').pin('Hostage','object',obj=HOSTAGE,out=True)
    e.props.append('CustomProperties UserDefinedPin (PinName="Hostage",PinType=(PinCategory="object",PinSubCategoryObject='+q("/Script/Engine.BlueprintGeneratedClass'"+HOSTAGE+"'")+'),DesiredPinDirection=EGPD_Output)')
    found=g.find(e,DIRECTOR);cast,d=g.cast_after(found,(found,'ReturnValue'),DIRECTOR)
    step=g.v('Paso','int',owner=DIRECTOR,target=d);code=g.v('OrderCode','int',owner=DIRECTOR,target=d)
    h=(e,'Hostage');bb=g.blackboard(*h)
    okay=g.both(g.cmp('Less_IntInt',step,3,'int'),g.neg(g.v('bActivated','bool')))
    okay=g.both(okay,g.cmp('EqualEqual_IntInt',g.v('Index','int'),g.op('Add_IntInt',identity(g,code,step),1,'int'),'int'))
    for i in (1,2,3):
        z=g.v('Zona'+str(i),'object',owner=DIRECTOR,target=d,obj=ZONE)
        okay=g.both(okay,g.v('bCleared','bool',owner=ZONE,target=z))
    okay=g.both(okay,g.v('bOrderRevealed','bool',owner=DIRECTOR,target=d))
    for key in ['bRescued','bAccompanying']:
        okay=g.both(okay,(g.bbget(bb,key),'ReturnValue'))
    for key in ['bEnemyNear','bMustFlee']:
        okay=g.both(okay,g.neg((g.bbget(bb,key),'ReturnValue')))
    okay=g.both(okay,g.cmp('Greater_DoubleDouble',g.v('Health',owner=HOSTAGE,target=h),0))
    okay=g.both(okay,g.v('bUsingBeacon','bool',owner=HOSTAGE,target=h))
    okay=g.both(okay,g.cmp('GreaterEqual_DoubleDouble',g.v('ActivationProgress',owner=HOSTAGE,target=h),1))
    # The supplied prop's pivot is on the floor; the hostage origin is at the
    # capsule center. Measure reach on the ground so the BT's arrival tolerance
    # cannot turn a completed three-second channel into an endless retry.
    reach=g.call(ACTOR,'GetHorizontalDistanceTo',pure=True).pin('OtherActor','object',obj=ACTOR).pin('ReturnValue','real',sub='float',out=True)
    g.w(h,reach,'self');g.w((g.selfnode(typ=BEACON),'self'),reach,'OtherActor')
    okay=g.both(okay,g.cmp('LessEqual_DoubleDouble',(reach,'ReturnValue'),220))
    accept=g.br(cast,okay);prev=g.s(accept,'bActivated',True,'bool')
    prev=g.s(prev,'Paso',g.op('Add_IntInt',step,1,'int'),'int',owner=DIRECTOR,target=d)
    complete=g.br(prev,g.cmp('EqualEqual_IntInt',step,3,'int'))
    third=g.v('Baliza3','object',owner=DIRECTOR,target=d,obj=SM)
    bc,b=g.cast_after(complete,third,BEACON);door=g.v('Door','object',owner=BEACON,target=b,obj=DOOR)
    prev=g.s(bc,'bUnlocked',True,'bool',owner=DOOR,target=door)
    prev=power_door(g,prev,door);prev.pins['Material']['default_obj']=POWERED
    pc,hp=g.cast_after(prev,(g.player(),'ReturnValue'),HERO)
    reward=g.action_on(pc,HERO,'GrantHammerUpgrade',hp,[('Door','object',door,DOOR)])
    fireworks=g.fx(reward,'NS_DoorBreak')
    fireworks.pins['SystemTemplate']['default_obj']='/Game/ThirdPerson/RecursosPropios/Particulas/NS_FuegArtificiales.NS_FuegArtificiales'
    # Only the luminous inset changes; the team's metal body stays intact.
    tick=g.event(ACTOR,'ReceiveTick').pin('DeltaSeconds','real',sub='float',out=True)
    f=g.find(tick,DIRECTOR);dc,d=g.cast_after(f,(f,'ReturnValue'),DIRECTOR)
    current=g.v('CurrentBeacon','object',owner=DIRECTOR,target=d,obj=SM)
    nextone=g.both(g.v('bOrderRevealed','bool',owner=DIRECTOR,target=d),g.cmp('EqualEqual_ObjectObject',current,(g.selfnode(typ=BEACON),'self'),'object'))
    state=table(g,g.c(MATH,'SelectInt',[('A','int',2),('B','int',g.c(MATH,'SelectInt',[('A','int',1),('B','int',0),('bPickA','bool',nextone)],cat='int')),('bPickA','bool',g.v('bActivated','bool'))],cat='int'),[0,1,2])
    mats=g.node('K2Node_Select',['NumOptionPins=3','IndexPinType=(PinCategory="int")']).pin('Index','int').pin('ReturnValue','object',obj='/Script/Engine.MaterialInterface',out=True)
    g.w(state,mats,'Index')
    for i,name in enumerate(['M_Baliza_Espera','M_Baliza_Siguiente','M_Baliza_Activada']):mats.pin('Option '+str(i),'object',obj='/Script/Engine.MaterialInterface',default_obj=ART+name+'.'+name)
    comp=g.v('StaticMeshComponent','object',owner=SM,target=(g.selfnode(typ=BEACON),'self'),obj=SMC,native=True)
    g.action_on(dc,PRIM,'SetMaterial',comp,[('ElementIndex','int',1,None),('Material','object',(mats,'ReturnValue'),'/Script/Engine.MaterialInterface')])
    g.write('BP_BeaconEntrega')

def label():
    from generate_guidance_graphs import setup,message
    g,prev,component=setup();g.__class__=ControlsGraph
    b=g.v('Beacon','object',obj=BEACON)
    index=g.op('Subtract_IntInt',g.v('Index','int',owner=BEACON,target=b),1,'int')
    name=table(g,index,['BALIZA A','BALIZA B','BALIZA C'],'string')
    value=g.c('/Script/Engine.KismetTextLibrary','Conv_StringToText',[('InString','string',name)],cat='text')
    g.action_on(prev,'/Script/Engine.TextRenderComponent','K2_SetText',(component,'TextRender'),[('Value','text',value,None)])
    g.write('BP_BeaconLabel')

if __name__=='__main__':
    director();beacon();label()
