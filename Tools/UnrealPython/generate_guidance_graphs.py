"""Runtime world-space prompts; packaged Blueprint actors, no Python dependency."""
from generate_combat_graphs import CombatGraph,ACTOR,ref
from generate_wave_graphs import ZONE
VECTOR='/Script/CoreUObject.Vector'
TEXTACTOR='/Script/Engine.TextRenderActor'
TEXT='/Script/Engine.TextRenderComponent'

def setup():
    g=CombatGraph();tick=g.event(ACTOR,'ReceiveTick').pin('DeltaSeconds','real',sub='float',out=True)
    self=g.selfnode(typ=TEXTACTOR,x=0,y=400)
    component=g.nativeget(TEXTACTOR,'TextRender','object',obj=TEXT,x=300,y=400);g.wire(self,'self',component,'self')
    camera=g.call('/Script/Engine.GameplayStatics','GetPlayerCameraManager',pure=True,static=True,x=0,y=700).pin('PlayerIndex','int',default='0').pin('ReturnValue','object',obj='/Script/Engine.PlayerCameraManager',out=True)
    pos=g.call('/Script/Engine.PlayerCameraManager','GetCameraLocation',pure=True,x=300,y=700).pin('ReturnValue','struct',obj=VECTOR,out=True);g.wire(camera,'ReturnValue',pos,'self')
    own=g.location(self,'self',x=300,y=1000)
    look=g.call('/Script/Engine.KismetMathLibrary','FindLookAtRotation',pure=True,static=True,x=600,y=700).pin('Start','struct',obj=VECTOR).pin('Target','struct',obj=VECTOR).pin('ReturnValue','struct',obj='/Script/CoreUObject.Rotator',out=True);g.wire(own,'ReturnValue',look,'Start');g.wire(pos,'ReturnValue',look,'Target')
    rotate=g.call(ACTOR,'K2_SetActorRotation',x=650,y=0).pin('NewRotation','struct',obj='/Script/CoreUObject.Rotator').pin('bTeleportPhysics','bool',default='true').pin('ReturnValue','bool',out=True);g.chain(tick,rotate);g.wire(look,'ReturnValue',rotate,'NewRotation')
    return g,rotate,component

def message(g,prev,component,value,pin='then',x=1500,y=0):
    literal=g.call('/Script/Engine.KismetTextLibrary','Conv_StringToText',pure=True,static=True,x=x,y=y+180).pin('InString','string',default=value).pin('ReturnValue','text',out=True)
    text=g.call(TEXT,'K2_SetText',x=x,y=y).pin('Value','text');g.chain(prev,text,pin);g.wire(component,'TextRender',text,'self');g.wire(literal,'ReturnValue',text,'Value')
    return text

def hostage():
    g,prev,component=setup();rehen=g.get('Rehen','object',obj=ACTOR,x=0,y=1400)
    valid=g.valid(rehen,'Rehen',x=300,y=1400);b=g.branch(x=1000,y=0);g.chain(prev,b);g.wire(valid,'ReturnValue',b,'Condition')
    pos=g.location(rehen,'Rehen',x=600,y=1400)
    offset=g.call('/Script/Engine.KismetMathLibrary','Add_VectorVector',pure=True,static=True,x=900,y=1400).pin('A','struct',obj=VECTOR).pin('B','struct',obj=VECTOR,default='0,0,180').pin('ReturnValue','struct',obj=VECTOR,out=True);g.wire(pos,'ReturnValue',offset,'A')
    move=g.call(ACTOR,'K2_SetActorLocation',x=1300,y=0).pin('NewLocation','struct',obj=VECTOR).pin('bSweep','bool',default='false').pin('SweepHitResult','struct',obj='/Script/Engine.HitResult',out=True).pin('bTeleport','bool',default='true').pin('ReturnValue','bool',out=True);g.chain(b,move);g.wire(offset,'ReturnValue',move,'NewLocation')
    bb=g.blackboard(rehen,'Rehen',x=900,y=1800)
    flee=g.bbget(bb,'bMustFlee',x=1200,y=1800);enemy=g.bbget(bb,'bEnemyNear',x=1200,y=2100)
    unsafe=g.boolean('BooleanOR',flee,'ReturnValue',enemy,'ReturnValue',x=1500,y=1800)
    danger=g.branch(x=1700,y=0);g.chain(move,danger);g.wire(unsafe,'ReturnValue',danger,'Condition')
    message(g,danger,component,'REHEN<br>BUSCANDO REFUGIO',x=2000)
    following=g.bbget(bb,'bAccompanying',x=1700,y=2400);follow=g.branch(x=2000,y=600);g.chain(danger,follow,'else');g.wire(following,'ReturnValue',follow,'Condition')
    message(g,follow,component,'REHEN<br>SIGUIENDOTE',x=2300,y=600)
    player=g.player(x=2000,y=2400);distance=g.dist(rehen,'Rehen',player,'ReturnValue',x=2300,y=2400)
    near=g.compare('LessEqual_DoubleDouble','real','400',sub='double',x=2600,y=2400);g.wire(distance,'ReturnValue',near,'A')
    proximity=g.branch(x=2300,y=1100);g.chain(follow,proximity,'else');g.wire(near,'ReturnValue',proximity,'Condition')
    rescued=g.bbget(bb,'bRescued',x=2600,y=2800);again=g.branch(x=2600,y=1100);g.chain(proximity,again);g.wire(rescued,'ReturnValue',again,'Condition')
    message(g,again,component,'REHEN<br>[E / RB] VOLVER A SEGUIR',x=2900,y=1100)
    message(g,again,component,'REHEN<br>[E / RB] RESCATAR','else',x=2900,y=1500)
    message(g,proximity,component,'REHEN<br>ACERCATE PARA INTERACTUAR','else',x=2600,y=1900)
    g.write('BP_RehenIndicador')

def zone():
    g,prev,component=setup();zone=g.get('Zona','object',obj=ZONE,x=0,y=1400)
    phase=g.get('Phase','int',owner=ZONE,x=400,y=1400);g.wire(zone,'Zona',phase,'self')
    switch=g.node('K2Node_SwitchInteger',['PinNames(0)="0"','PinNames(1)="1"','PinNames(2)="2"','PinNames(3)="3"'],x=1000,y=0).pin('execute').pin('Selection','int').pin('Default',out=True)
    for i in range(4):switch.pin(str(i),out=True)
    g.chain(prev,switch);g.wire(phase,'Phase',switch,'Selection')
    for i,value in enumerate(['ZONA DE COMBATE<br>ENTRA CON EL REHEN CERCA<br>2 OLEADAS DE 2 ENEMIGOS','OLEADA EN CURSO<br>ELIMINA A LOS ENEMIGOS','PREPARATE<br>SIGUIENTE OLEADA','ZONA DESPEJADA<br>RECUPERA AL REHEN']):message(g,switch,component,value,str(i),y=i*400)
    g.write('BP_ZonaIndicador')

if __name__=='__main__':hostage();zone()
