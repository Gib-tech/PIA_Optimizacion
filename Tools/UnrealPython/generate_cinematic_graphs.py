"""Blueprint presentation controller and small hooks into existing mission sources."""
from generate_delivery_controls import ControlsGraph, flatten, split_exec, PC
from generate_progression_graphs import ACTOR, OBJECT, GS, MATH, HERO, HOSTAGE, DIRECTOR, PRIM, VEC
from generate_combat_graphs import CHAR, MOVE, BASE
from generate_delivery_graphs import q
from delivery_save_schema import GI

ROOT='/Game/ThirdPerson/Cinematics/'
CINEMA=ROOT+'BP_CinematicDirector.BP_CinematicDirector_C'
LSPLAYER='/Script/LevelSequence.LevelSequencePlayer'
MSPLAYER='/Script/MovieScene.MovieSceneSequencePlayer'
LSACTOR='/Script/LevelSequence.LevelSequenceActor'
INSTANCE='/Script/LevelSequence.DefaultLevelSequenceInstanceData'
HUD='/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega.BP_HUD_Entrega_C'
UI='/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C'

def select(g,index,values,cat='string',obj=None):
    n=g.node('K2Node_Select',['NumOptionPins='+str(len(values)),'IndexPinType=(PinCategory="int")']).pin('Index','int').pin('ReturnValue',cat,obj=obj,sub='double' if cat=='real' else '',out=True)
    g.w(index,n,'Index')
    for i,value in enumerate(values):
        p='Option '+str(i);n.pin(p,cat,obj=obj,sub='double' if cat=='real' else '')
        if cat=='object' and isinstance(value,str):n.pins[p]['default_obj']=value
        else:g.w(value,n,p)
    return n,'ReturnValue'

def terminal_hooks(g):
    """Keep the existing outcome conditions; start a film instead of pausing early."""
    g.__class__=ControlsGraph
    for pause in list(g.nodes):
        if not any('MemberName="SetGamePaused"' in p for p in pause.props):continue
        if pause.pins['bPaused'].get('default')!='true':continue
        # Only pauses after a terminal Paso assignment belong to this hook.
        incoming=list(pause.pins['execute']['links'])
        if not incoming:continue
        sources=[next(n for n in g.nodes if n.name==name) for name,pid in incoming]
        if not all('Paso' in n.pins and n.pins['Paso'].get('default') in ['4','5','6'] for n in sources):continue
        pause.pins['execute']['links']=[]
        for src in sources:
            p=next(p for p in src.pins.values() if (pause.name,pause.pins['execute']['id']) in p['links'])
            p['links'].remove((pause.name,pause.pins['execute']['id']))
            f=g.find(src,CINEMA)
            valid=g.br(f,(g.valid(f,'ReturnValue'),'ReturnValue'))
            g.action_on(valid,CINEMA,'StartOutcome',(f,'ReturnValue'))
            # Old maps without the presentation actor retain a usable result.
            g.chain(valid,pause,'else')
    return g

def controller():
    g=ControlsGraph();own=(g.selfnode(typ=CINEMA),'self');pc=g.pc()
    kind=g.v('Kind','int');active=g.v('bActive','bool')
    hero=g.local('Hero',HERO);host=g.local('Hostage',HOSTAGE)
    director=g.local('Director',DIRECTOR);ui=g.local('Interface',UI);hud=g.local('GameHUD',HUD)
    player=g.local('SequencePlayer',LSPLAYER);actor=g.local('SequenceActor',LSACTOR)
    now=g.c(GS,'GetTimeSeconds')
    camera_manager=g.c(GS,'GetPlayerCameraManager',[('PlayerIndex','int',0)],cat='object',obj='/Script/Engine.PlayerCameraManager')
    def clear_loading_fade(prev,pin='then'):return g.action_on(prev,'/Script/Engine.PlayerCameraManager','StopCameraFade',camera_manager,pin=pin)
    def owncall(prev,name,pin='then'):return g.action_on(prev,CINEMA,name,pin=pin)
    def input_to(prev,target,enabled):return g.action_on(prev,ACTOR,'EnableInput' if enabled else 'DisableInput',target,[('PlayerController','object',pc,PC)])
    def cinematic(prev,enabled):
        false=g.c('/Script/Engine.KismetSystemLibrary','MakeLiteralBool',[('Value','bool',False)],cat='bool')
        return g.action_on(prev,PC,'SetCinematicMode',pc,[('bInCinematicMode','bool',enabled,None),('bHidePlayer','bool',false,None),('bAffectsHUD','bool',false,None),('bAffectsMovement','bool',True,None),('bAffectsTurning','bool',True,None)])
    def mesh_owner(prev,value):
        mesh=g.v('Mesh','object',owner=CHAR,target=hero,obj='/Script/Engine.SkeletalMeshComponent',native=True)
        return g.action_on(prev,PRIM,'SetOwnerNoSee',mesh,[('bNewOwnerNoSee','bool',value,None)])
    def health_widget(prev,hidden):
        widget=g.v('Health_Widget','object',owner='/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C',target=hero,obj='/Script/UMG.UserWidget')
        return g.action_on(prev,'/Script/UMG.Widget','SetVisibility',widget,[('InVisibility','byte','Hidden' if hidden else 'HitTestInvisible','/Script/UMG.ESlateVisibility')])
    begin=g.event(ACTOR,'ReceiveBeginPlay')
    # Mask the first native streaming frame before the HUD/player caches exist.
    black=g.action_on(begin,'/Script/Engine.PlayerCameraManager','SetManualCameraFade',camera_manager,[('InFadeAmount','real',1,None),('Color','struct','(R=0,G=0,B=0,A=1)','/Script/CoreUObject.LinearColor'),('bInFadeAudio','bool',False,None)])
    gi=g.c(GS,'GetGameInstance',cat='object',obj='/Script/Engine.GameInstance')
    cast,instance=g.cast_after(black,gi,GI)
    g.s(cast,'bShouldIntro',g.neg(g.v('bDeliveryContinue','bool',owner=GI,target=instance)),'bool')
    tick=g.event(ACTOR,'ReceiveTick').pin('DeltaSeconds','real',sub='float',out=True)
    ready=g.br(tick,g.v('bInitialized','bool'))
    available=g.br(ready,(g.valid(g.player(),'ReturnValue'),'ReturnValue'),'else')
    prev=available
    for name,cls in [('Hero',HERO),('Hostage',HOSTAGE),('Director',DIRECTOR),('Interface',UI)]:
        f=g.find(prev,cls);prev=g.s(f,name,(f,'ReturnValue'),'object',obj=cls)
    gethud=g.call(PC,'GetHUD',pure=True).pin('ReturnValue','object',obj='/Script/Engine.HUD',out=True);g.w(pc,gethud,'self')
    c,val=g.cast_after(prev,(gethud,'ReturnValue'),HUD);prev=g.s(c,'GameHUD',val,'object',obj=HUD)
    prev=g.s(prev,'bInitialized',True,'bool')
    first=g.br(prev,g.v('bShouldIntro','bool'));owncall(first,'StartIntro')
    clear_loading_fade(first,'else')
    running=g.br(ready,active)
    over=g.br(running,g.cmp('GreaterEqual_DoubleDouble',now,g.v('EndsAt')));owncall(over,'FinishCinema')
    e=g.custom('StartIntro');guard=g.br(e,g.neg(active));prev=g.s(guard,'Kind',0,'int');owncall(prev,'PlayCinema')
    from generate_final_words import reveal_event,complete_revelation
    reveal_event(g,own,hero,host,director,now)
    e=g.custom('StartOutcome');guard=g.br(e,g.neg(g.v('bOutcomeStarted','bool')))
    # Terminal outcomes take priority if damage races the nonterminal dialogue.
    interrupt=g.br(guard,active)
    stopped=g.action_on(interrupt,MSPLAYER,'Stop',player)
    stopped=cinematic(stopped,False)
    old_enemy=g.local('RevealEnemy',BASE);enemy_valid=g.br(stopped,(g.valid(*old_enemy),'ReturnValue'))
    released=g.action_on(enemy_valid,BASE,'FinishFinalWords',old_enemy)
    prev=g.s(released,'bNarrativePaused',False,'bool',owner=DIRECTOR,target=director)
    g.chain(enemy_valid,prev,'else');g.chain(interrupt,prev,'else')
    prev=g.s(prev,'bOutcomeStarted',True,'bool')
    step=g.v('Paso','int',owner=DIRECTOR,target=director)
    choice=g.c(MATH,'SelectInt',[('A','int',3),('B','int',g.c(MATH,'SelectInt',[('A','int',2),('B','int',1),('bPickA','bool',g.cmp('EqualEqual_IntInt',step,6,'int'))],cat='int')),('bPickA','bool',g.cmp('EqualEqual_IntInt',step,4,'int'))],cat='int')
    prev=g.s(prev,'Kind',choice,'int')
    # The existing death montage places its final pose partly below the floor.
    # Raise only the rendered mesh after terminal defeat to keep it in the shot.
    fallen=g.br(prev,g.cmp('EqualEqual_IntInt',kind,1,'int'))
    mesh=g.v('Mesh','object',owner=CHAR,target=hero,obj='/Script/Engine.SkeletalMeshComponent',native=True)
    lift=g.action_on(fallen,'/Script/Engine.SceneComponent','K2_AddLocalOffset',mesh,[('DeltaLocation','struct','0,0,42',VEC),('bSweep','bool',False,None),('bTeleport','bool',True,None)])
    hostage_fell=g.br(lift,g.cmp('EqualEqual_IntInt',kind,2,'int'));g.chain(fallen,hostage_fell,'else')
    hostmesh=g.v('Mesh','object',owner=CHAR,target=host,obj='/Script/Engine.SkeletalMeshComponent',native=True)
    ragdoll=g.action_on(hostage_fell,PRIM,'SetCollisionProfileName',hostmesh,[('InCollisionProfileName','name','Ragdoll',None),('bUpdateOverlaps','bool',True,None)])
    ragdoll=g.action_on(ragdoll,PRIM,'SetSimulatePhysics',hostmesh,[('bSimulate','bool',True,None)])
    # Terminal presentation stops outstanding AI actions while Sequencer keeps time.
    allai=g.call(GS,'GetAllActorsOfClass',static=True).pin('ActorClass','class',obj=ACTOR,default_obj='/Script/AIModule.AIController').pin('OutActors','object',obj='/Script/AIModule.AIController',out=True)
    allai.pins['OutActors']['container']='Array';g.chain(ragdoll,allai);g.chain(hostage_fell,allai,'else')
    loop=g.foreach(allai,'OutActors',typ='/Script/AIModule.AIController');g.chain(allai,loop,nextpin='Exec')
    brain=g.v('BrainComponent','object',owner='/Script/AIModule.AIController',target=(loop,'Array Element'),obj='/Script/AIModule.BrainComponent',native=True)
    good=g.br(loop,(g.valid(*brain),'ReturnValue'),'LoopBody')
    g.action_on(good,'/Script/AIModule.BrainComponent','StopLogic',brain,[('Reason','string','Cinematic: mission finished',None)])
    prev=loop
    # Stop movement/late damage only after the existing mission has ended.
    allchars=g.call(GS,'GetAllActorsOfClass',static=True).pin('ActorClass','class',obj=ACTOR,default_obj=CHAR).pin('OutActors','object',obj=CHAR,out=True);allchars.pins['OutActors']['container']='Array';g.chain(prev,allchars,'Completed')
    chars=g.foreach(allchars,'OutActors',typ=CHAR);g.chain(allchars,chars,nextpin='Exec')
    char=(chars,'Array Element');move=g.v('CharacterMovement','object',owner=CHAR,target=char,obj=MOVE,native=True)
    stop=g.action_on(chars,MOVE,'StopMovementImmediately',move,pin='LoopBody')
    stop=g.action_on(stop,MOVE,'DisableMovement',move)
    g.s(stop,'bCanBeDamaged',False,'bool',owner=ACTOR,target=char)
    owncall(chars,'PlayCinema','Completed')
    e=g.custom('PlayCinema');prev=g.s(e,'bActive',True,'bool')
    prev=g.s(prev,'StartedAt',now);duration=select(g,kind,[18,8,8,14,12],'real');prev=g.s(prev,'Duration',duration)
    prev=g.s(prev,'EndsAt',g.op('Add_DoubleDouble',now,duration))
    target=g.call(PC,'GetViewTarget',pure=True).pin('ReturnValue','object',obj=ACTOR,out=True);g.w(pc,target,'self')
    prev=g.s(prev,'SavedViewTarget',(target,'ReturnValue'),'object',obj=ACTOR)
    prev=cinematic(prev,True);prev=mesh_owner(prev,False);prev=health_widget(prev,True)
    for value in [hero,director,ui,hud]:prev=input_to(prev,value,False)
    prev=input_to(prev,own,True);prev=g.cursor(prev,False);prev=g.mode(prev,game=True)
    make=g.call(LSPLAYER,'CreateLevelSequencePlayer',static=True).pin('WorldContextObject','object',obj=OBJECT,hidden=True).pin('LevelSequence','object',obj='/Script/LevelSequence.LevelSequence').pin('Settings','struct',obj='/Script/MovieScene.MovieSceneSequencePlaybackSettings',default='(bAutoPlay=False,PlayRate=1.000000,bHidePlayer=False,bHideHud=False,bDisableMovementInput=False,bDisableLookAtInput=False,bDisableCameraCuts=False,bPauseAtEnd=False,FinishCompletionStateOverride=ForceRestoreState)').pin('OutActor','object',obj=LSACTOR,out=True).pin('ReturnValue','object',obj=LSPLAYER,out=True)
    sequence=select(g,kind,[ROOT+'LS_Intro.LS_Intro',ROOT+'LS_Derrota.LS_Derrota',ROOT+'LS_Derrota.LS_Derrota',ROOT+'LS_Victoria.LS_Victoria',ROOT+'LS_Revelacion.LS_Revelacion'],'object','/Script/LevelSequence.LevelSequence');g.w(sequence,make,'LevelSequence');g.chain(prev,make)
    prev=g.s(make,'SequencePlayer',(make,'ReturnValue'),'object',obj=LSPLAYER)
    prev=g.s(prev,'SequenceActor',(make,'OutActor'),'object',obj=LSACTOR)
    reveal=g.cmp('EqualEqual_IntInt',kind,4,'int')
    death=g.c(MATH,'BooleanOR',[('A','bool',g.both(g.cmp('Greater_IntInt',kind,0,'int'),g.cmp('Less_IntInt',kind,3,'int'))),('B','bool',reveal)],cat='bool')
    prev=g.s(prev,'bOverrideInstanceData',death,'bool',owner=LSACTOR,target=actor)
    victim=select(g,kind,[hero,hero,host,hero,g.local('RevealEnemy',BASE)],'object',ACTOR)
    pos=g.location(*victim)
    prev=g.action_on(prev,ACTOR,'K2_SetActorLocation',own,[('NewLocation','struct',(pos,'ReturnValue'),VEC),('bSweep','bool',False,None),('bTeleport','bool',True,None)])
    rot=g.c(ACTOR,'K2_GetActorRotation',cat='struct',obj='/Script/CoreUObject.Rotator',pure=True,static=False);g.w(victim,rot[0],'self')
    chosen_rot=g.c(MATH,'SelectRotator',[('A','struct',rot),('B','struct','0,0,0'),('bPickA','bool',reveal)],cat='struct',obj='/Script/CoreUObject.Rotator')
    for pin in ['A','B']:chosen_rot[0].pins[pin]['obj']='/Script/CoreUObject.Rotator'
    prev=g.action_on(prev,ACTOR,'K2_SetActorRotation',own,[('NewRotation','struct',chosen_rot,'/Script/CoreUObject.Rotator'),('bTeleportPhysics','bool',False,None)])
    data=g.v('DefaultInstanceData','object',owner=LSACTOR,target=actor,obj=OBJECT,native=True)
    cast=g.nativecast(INSTANCE);g.chain(prev,cast);g.w(data,cast,'Object')
    prev=g.s(cast,'TransformOriginActor',own,'object',owner=INSTANCE,target=(cast,'AsDefaultLevelSequenceInstanceData'),obj=ACTOR)
    clear=clear_loading_fade(prev);g.chain(cast,clear,'CastFailed')
    play=g.action_on(clear,MSPLAYER,'Play',player)
    for key in ['SpaceBar','Gamepad_FaceButton_Bottom']:
        e=g.key(key);e.props=[p.replace('bConsumeInput=False','bConsumeInput=True') for p in e.props]
        guard=g.br(e,active,'Pressed');owncall(guard,'FinishCinema')
    e=g.custom('FinishCinema');guard=g.br(e,active);prev=g.s(guard,'bActive',False,'bool')
    valid=g.br(prev,(g.valid(*player),'ReturnValue'));stop=g.action_on(valid,MSPLAYER,'Stop',player)
    # Both natural completion and skip use this exact camera/input cleanup.
    prev=cinematic(stop,False);g.chain(valid,prev,'else')
    firstperson=g.v('CamaraPrimera','bool',owner=HERO,target=hero)
    prev=mesh_owner(prev,firstperson);prev=health_widget(prev,False)
    view=g.action_on(prev,PC,'SetViewTargetWithBlend',pc,[('NewViewTarget','object',g.local('SavedViewTarget',ACTOR),ACTOR),('BlendTime','real',0,None),('BlendFunc','byte','VTBlend_Linear','/Script/Engine.EViewTargetBlendFunction'),('BlendExp','real',0,None),('bLockOutgoing','bool',False,None)])
    prev=input_to(view,director,True);prev=input_to(prev,hud,True);prev=input_to(prev,own,False)
    story=g.br(prev,reveal)
    complete,extra=complete_revelation(g,story,host,director)
    intro=g.br(story,g.cmp('EqualEqual_IntInt',kind,0,'int'),'else')
    prev=input_to(intro,hero,True);g.chain(complete,prev)
    for node,pin in extra:g.chain(node,prev,pin)
    prev=input_to(prev,ui,True);g.mode(prev,game=True)
    paused=g.call(GS,'SetGamePaused',static=True).pin('bPaused','bool',default='true').pin('ReturnValue','bool',out=True);g.chain(intro,paused,'else')
    flatten(g,CINEMA);g.write('BP_CinematicDirector')

def hud_hook(g):
    """Draw only the film frame/captions while active; normal HUD resumes afterward."""
    g.__class__=ControlsGraph
    begin=next(n for n in g.nodes if n.kind.endswith('K2Node_Event') and any('ReceiveBeginPlay' in p for p in n.props))
    seq=split_exec(g,begin)
    found=g.call(GS,'GetActorOfClass',static=True).pin('ActorClass','class',obj=ACTOR,default_obj=CINEMA).pin('ReturnValue','object',obj=CINEMA,out=True)
    g.chain(seq,found,'then_1')
    g.s(found,'CachedCinema',(found,'ReturnValue'),'object',obj=CINEMA)
    draw=next(n for n in g.nodes if n.kind.endswith('K2Node_Event') and any('ReceiveDrawHUD' in p for p in n.props))
    old=list(draw.pins['then']['links']);draw.pins['then']['links']=[]
    for name,pid in old:
        n=next(n for n in g.nodes if n.name==name);p=next(p for p in n.pins.values() if p['id']==pid);p['links'].remove((draw.name,draw.pins['then']['id']))
    movie=g.local('CachedCinema',CINEMA);valid=g.br(draw,(g.valid(*movie),'ReturnValue'))
    active=g.br(valid,g.v('bActive','bool',owner=CINEMA,target=movie))
    for name,pid in old:
        n=next(n for n in g.nodes if n.name==name);p=next(p for p in n.pins.values() if p['id']==pid)
        g.chain(valid,n,'else',p['name']);g.chain(active,n,'else',p['name'])
    width=(draw,'SizeX');height=(draw,'SizeY')
    ratio=g.op('Divide_DoubleDouble',width,1280)
    scale=g.c(MATH,'FClamp',[('Value','real',ratio),('Min','real',.5),('Max','real',1.8)])
    mul=lambda a,b:g.op('Multiply_DoubleDouble',a,b)
    add=lambda a,b:g.op('Add_DoubleDouble',a,b)
    sub=lambda a,b:g.op('Subtract_DoubleDouble',a,b)
    bar=g.c(MATH,'FMax',[('A','real',mul(sub(height,g.op('Divide_DoubleDouble',width,2.39)),.5)),('B','real',mul(90,scale))])
    black='(R=.003,G=.006,B=.012,A=1)';white='(R=.91,G=.96,B=1,A=1)';cyan='(R=.24,G=.82,B=1,A=1)'
    def rect(prev,x,y,w,h,color):
        n=g.call('/Script/Engine.HUD','DrawRect').pin('RectColor','struct',obj='/Script/CoreUObject.LinearColor',default=color)
        for p,v in [('ScreenX',x),('ScreenY',y),('ScreenW',w),('ScreenH',h)]:n.pin(p,'real',sub='float');g.w(v,n,p)
        g.chain(prev,n);return n
    def text(prev,value,x,y,size=1,color=white):
        n=g.call('/Script/Engine.HUD','DrawText').pin('Text','string').pin('TextColor','struct',obj='/Script/CoreUObject.LinearColor',default=color).pin('Font','object',obj='/Script/Engine.Font',default_obj='/Game/ThirdPerson/Blueprints/Entrega/F_DialogueMono.F_DialogueMono').pin('bScalePosition','bool',default='false')
        g.w(value,n,'Text')
        for p,v in [('ScreenX',x),('ScreenY',y),('Scale',mul(size,scale))]:n.pin(p,'real',sub='float');g.w(v,n,p)
        g.chain(prev,n);return n
    kind=g.v('Kind','int',owner=CINEMA,target=movie)
    age=sub(g.c(GS,'GetTimeSeconds'),g.v('StartedAt',owner=CINEMA,target=movie))
    def segment(first,second):return g.c(MATH,'SelectInt',[('A','int',2),('B','int',g.c(MATH,'SelectInt',[('A','int',1),('B','int',0),('bPickA','bool',g.cmp('GreaterEqual_DoubleDouble',age,first))],cat='int')),('bPickA','bool',g.cmp('GreaterEqual_DoubleDouble',age,second))],cat='int')
    part=select(g,kind,[segment(6,12),segment(3,6),segment(3,6),segment(5,10),segment(4,9)],'int')
    def line(sets):return select(g,kind,[select(g,part,lines) for lines in sets])
    speaker=line([['CONTROL','REHÉN','CONTROL'],['CONTROL','CONTROL','TIME OUT'],['CONTROL','CONTROL','TIME OUT'],['REHÉN','REHÉN','CONTROL'],['GUARDIÁN','GUARDIÁN','GUARDIÁN']])
    spoken_order=g.c('/Script/Engine.KismetStringLibrary','Concat_StrStr',[('A','string','El orden es: '),('B','string',g.v('RevealedSequence','string',owner=CINEMA,target=movie))],cat='string')
    first=line([
      ['El salto te ha dejado en un recinto fuera del tiempo.','Sólo yo puedo sincronizar las balizas.','Despeja las zonas. Carga el martillo.'],
      ['Hemos perdido tu señal.','El salto quedó incompleto.','El tiempo permite otro intento.'],
      ['Su señal se ha apagado.','Sin él, no hay camino de vuelta.','El tiempo permite otro intento.'],
      ['Las tres señales coinciden.','Esta vez volvemos juntos.','Extracción confirmada. Dos viajeros.'],
      ['Espera... aún queda una salida de este bucle.',spoken_order,'Rompe el sello... y saca al cautivo de aquí.']])
    second=line([
      ['Encuentra al cautivo. Su señal es nuestra salida.','Ayúdame a salir. No puedo hacerlo solo.','Escolta su señal hasta la salida.'],
      ['','Protege al rehén y vuelve a intentarlo.',''],['','No dejes que lo alcancen.',''],
      ['Ya no tenemos que huir.','','Una misma línea temporal.'],
      ['Las balizas sólo responden a una secuencia.','No lo olvides. Es la clave del último sello.','']])
    chapter=select(g,kind,['UNA SEÑAL ENTRE ÉPOCAS','LA SEÑAL SE APAGA','LA SEÑAL SE APAGA','VOLVER JUNTOS','EL ÚLTIMO GUARDIÁN'])
    prev=rect(active,0,0,width,bar,black);prev=rect(prev,0,sub(height,bar),width,bar,black)
    prev=rect(prev,mul(46,scale),sub(bar,mul(13,scale)),mul(80,scale),mul(2,scale),cyan)
    prev=text(prev,'TIME OUT',mul(46,scale),mul(19,scale),1.55)
    prev=text(prev,chapter,mul(46,scale),mul(49,scale),.78,cyan)
    y=sub(height,bar);prev=text(prev,speaker,mul(46,scale),add(y,mul(8,scale)),.72,cyan)
    prev=text(prev,first,mul(46,scale),add(y,mul(27,scale)),1.12)
    prev=text(prev,second,mul(46,scale),add(y,mul(51,scale)),1.12)
    prev=text(prev,'ESPACIO  /  Omitir',sub(width,mul(255,scale)),sub(height,mul(22,scale)),.72)
    progress=g.c(MATH,'FClamp',[('Value','real',g.op('Divide_DoubleDouble',age,g.v('Duration',owner=CINEMA,target=movie))),('Min','real',0),('Max','real',1)])
    rect(prev,0,sub(height,2),mul(width,progress),2,cyan)

if __name__=='__main__':controller()
