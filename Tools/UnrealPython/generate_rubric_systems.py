"""Blueprints de inventario, segundo NPC, pulso consumible y luz solar."""
from generate_delivery_controls import ControlsGraph, flatten
from generate_progression_graphs import ACTOR,HERO,DIRECTOR,MATH,GS,VEC,PRIM,SCENE,HOSTAGE
from generate_combat_graphs import BASE,CHAR
from generate_delivery_graphs import q
R='/Game/ThirdPerson/Blueprints/Entrega/'
EXTRAS=R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'
HEALTH='/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C'
SM='/Script/Engine.StaticMeshActor';ROT='/Script/CoreUObject.Rotator'

def systems():
 g=ControlsGraph();hero=g.local('Hero',HERO);director=g.local('Director',DIRECTOR);tech=g.local('Tecnico',R+'BP_TecnicoTemporal.BP_TecnicoTemporal_C')
 now=g.c(GS,'GetTimeSeconds');health=g.v('BPC_Health','object',owner=HERO,target=hero,obj=HEALTH)
 hp=g.v('Health',owner=HEALTH,target=health)
 def notice(prev,text,pin='then'):
  prev=g.s(prev,'Notice',text,'string',pin=pin);return g.s(prev,'NoticeUntil',g.op('Add_DoubleDouble',now,3))
 def allowed():
  valid=g.both((g.valid(*hero),'ReturnValue'),(g.valid(*director),'ReturnValue'))
  valid=g.both(valid,g.cmp('Less_IntInt',g.v('Paso','int',owner=DIRECTOR,target=director),4,'int'))
  ignored=g.c('/Script/Engine.Controller','IsMoveInputIgnored',cat='bool',static=False);g.w(g.pc(),ignored[0],'self')
  return g.both(g.both(valid,g.neg(ignored)),g.neg(g.v('bNarrativePaused','bool',owner=DIRECTOR,target=director)))
 def key(name,consume=True,paused=False):
  n=g.key(name);n.props=['InputKey='+name,'bConsumeInput='+str(consume),'bExecuteWhenPaused='+str(paused)];return n
 def entry(keys,name,consume=True):
  for k in keys:g.action_on(key(k,consume),EXTRAS,name,pin='Pressed')
  return g.custom(name)
 tick=g.event(ACTOR,'ReceiveTick').pin('DeltaSeconds','real',sub='float',out=True)
 seq=g.node('K2Node_ExecutionSequence').pin('execute')
 for i in range(6):seq.pin('then_'+str(i),out=True)
 g.chain(tick,seq)
 start=g.br(seq,g.neg(g.v('bInitialized','bool')),'then_0')
 prev=start
 for field,cls in [('Hero',HERO),('Director',DIRECTOR)]:
  f=g.find(prev,cls);cast,val=g.cast_after(f,(f,'ReturnValue'),cls);prev=g.s(cast,field,val,'object',obj=cls)
 prev=g.s(prev,'bInitialized',True,'bool')
 # Las instancias antiguas pueden conservar AutoReceiveInput=Disabled aunque
 # cambie el CDO. Registrar aquí, cuando Player0 y Hero ya existen, evita que
 # sólo funcionen llamadas directas a eventos durante una prueba preparada.
 enabled=g.action_on(prev,ACTOR,'EnableInput',(g.selfnode(typ=EXTRAS),'self'),[('PlayerController','object',g.pc(),'/Script/Engine.PlayerController')])
 # La cúpula conserva la atmósfera física y añade cielo nocturno procedural.
 dome=g.local('SkyDome',SM);dome_mesh=g.v('StaticMeshComponent','object',owner=SM,target=dome,obj='/Script/Engine.StaticMeshComponent',native=True)
 valid_dome=g.br(enabled,(g.valid(*dome),'ReturnValue'))
 mid=g.call('/Script/Engine.PrimitiveComponent','CreateDynamicMaterialInstance').pin('ElementIndex','int',default='0').pin('SourceMaterial','object',obj='/Script/Engine.MaterialInterface').pin('OptionalName','name',default='CieloDinamico').pin('ReturnValue','object',obj='/Script/Engine.MaterialInstanceDynamic',out=True)
 g.w(dome_mesh,mid,'self');g.chain(valid_dome,mid);g.s(mid,'SkyMID',(mid,'ReturnValue'),'object',obj='/Script/Engine.MaterialInstanceDynamic')
 ready=g.br(seq,g.v('bInitialized','bool'),'then_1');ready=g.br(ready,allowed())
 updates=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True).pin('then_1',out=True);g.chain(ready,updates)
 age=g.s(updates,'WorldSeconds',g.op('Add_DoubleDouble',g.v('WorldSeconds'),(tick,'DeltaSeconds')),pin='then_0')
 # Ocho minutos reales por vuelta. Arranque matinal y pausa real del reloj.
 phase=g.op('Multiply_DoubleDouble',g.v('WorldSeconds'),.75)
 angle=g.op('Add_DoubleDouble',phase,35)
 elevation=g.c(MATH,'DegSin',[('A','real',angle)])
 daylight=g.c(MATH,'FMax',[('A','real',elevation),('B','real',0)])
 night=g.c(MATH,'FClamp',[('Value','real',g.op('Divide_DoubleDouble',g.op('Subtract_DoubleDouble',.03,elevation),.23)),('Min','real',0),('Max','real',1)])
 rot=g.c(MATH,'MakeRotator',[('Pitch','real',g.op('Multiply_DoubleDouble',angle,-1)),('Yaw','real',-35),('Roll','real',0)],cat='struct',obj=ROT)
 sun=g.local('Sun','/Script/Engine.DirectionalLight');valid=g.br(age,(g.valid(*sun),'ReturnValue'))
 prev=g.action_on(valid,ACTOR,'K2_SetActorRotation',sun,[('NewRotation','struct',rot,ROT),('bTeleportPhysics','bool',False,None)])
 light=g.v('LightComponent','object',owner='/Script/Engine.Light',target=sun,obj='/Script/Engine.LightComponent',native=True)
 intensity=g.op('Multiply_DoubleDouble',daylight,26000)
 prev=g.action_on(prev,'/Script/Engine.LightComponent','SetIntensity',light,[('NewIntensity','real',intensity,None)])
 moon=g.local('Moon','/Script/Engine.DirectionalLight');moon_ok=g.br(prev,(g.valid(*moon),'ReturnValue'))
 moon_rot=g.c(MATH,'MakeRotator',[('Pitch','real',g.op('Subtract_DoubleDouble',180,angle)),('Yaw','real',-35),('Roll','real',0)],cat='struct',obj=ROT)
 prev=g.action_on(moon_ok,ACTOR,'K2_SetActorRotation',moon,[('NewRotation','struct',moon_rot,ROT),('bTeleportPhysics','bool',False,None)])
 moon_light=g.v('LightComponent','object',owner='/Script/Engine.Light',target=moon,obj='/Script/Engine.LightComponent',native=True)
 prev=g.action_on(prev,'/Script/Engine.LightComponent','SetIntensity',moon_light,[('NewIntensity','real',g.op('Multiply_DoubleDouble',night,.12),None)])
 sky=g.local('Sky','/Script/Engine.SkyLight');sky_ok=g.br(prev,(g.valid(*sky),'ReturnValue'));g.chain(moon_ok,sky_ok,'else')
 sky_component=g.v('LightComponent','object',owner='/Script/Engine.SkyLight',target=sky,obj='/Script/Engine.SkyLightComponent',native=True)
 ambience=g.op('Subtract_DoubleDouble',.65,g.op('Multiply_DoubleDouble',night,.35))
 prev=g.action_on(sky_ok,'/Script/Engine.SkyLightComponent','SetIntensity',sky_component,[('NewIntensity','real',ambience,None)])
 sky_mid=g.local('SkyMID','/Script/Engine.MaterialInstanceDynamic');mid_ok=g.br(prev,(g.valid(*sky_mid),'ReturnValue'));g.chain(sky_ok,mid_ok,'else')
 g.action_on(mid_ok,'/Script/Engine.MaterialInstanceDynamic','SetScalarParameterValue',sky_mid,[('ParameterName','name','NightAmount',None),('Value','real',night,None)])
 # Proceso real de conversión, en tiempo de juego. Una orden produce un kit.
 working=g.br(updates,g.v('bFabricating','bool'),'then_1')
 prev=g.s(working,'FabricationProgress',g.op('Add_DoubleDouble',g.v('FabricationProgress'),(tick,'DeltaSeconds')))
 completed=g.br(prev,g.cmp('GreaterEqual_DoubleDouble',g.v('FabricationProgress'),3))
 prev=g.s(completed,'bFabricating',False,'bool');prev=g.s(prev,'RobotEnergy',0,'int');prev=g.s(prev,'FabricationProgress',0)
 prev=g.s(prev,'Botiquines',g.op('Add_IntInt',g.v('Botiquines','int'),1,'int'),'int')
 notice(g.sound(prev,'Rescue'),'BRUNO: conversión completada. Botiquín fabricado (+1).')
 for i in range(1,5):
  item=g.local('Suministro'+str(i),SM)
  branch=g.br(seq,g.both(g.v('bInitialized','bool'),(g.valid(*hero),'ReturnValue')),'then_'+str(i+1))
  branch=g.br(branch,(g.valid(*item),'ReturnValue'))
  # Ocultar a partir del estado persistido también al reabrir el nivel.
  prev=g.action_on(branch,ACTOR,'SetActorHiddenInGame',item,[('bNewHidden','bool',g.v('Recogido'+str(i),'bool'),None)])
  near=g.cmp('LessEqual_DoubleDouble',(g.dist(*hero,*item),'ReturnValue'),165)
  pickup=g.br(prev,g.both(g.neg(g.v('Recogido'+str(i),'bool')),g.both(allowed(),near)))
  prev=g.s(pickup,'Recogido'+str(i),True,'bool')
  for field,amount in [('Botiquines',1),('Cargas',3),('Creditos',3)]:prev=g.s(prev,field,g.op('Add_IntInt',g.v(field,'int'),amount,'int'),'int')
  notice(g.sound(prev,'Rescue'),'Suministros: +1 botiquín, +3 cargas, +3 créditos.')
 for e in [entry(['I','Gamepad_Special_Left'],'AlternarInventario')]:
  guard=g.br(e,g.v('bInitialized','bool'));guard=g.br(guard,allowed());g.s(guard,'InventoryOpen',g.neg(g.v('InventoryOpen','bool')),'bool')
 for e in [entry(['H','Gamepad_LeftShoulder'],'UsarBotiquin')]:
  guard=g.br(e,g.v('bInitialized','bool'));guard=g.br(guard,allowed())
  condition=g.both(g.cmp('Greater_IntInt',g.v('Botiquines','int'),0,'int'),g.both(g.cmp('Greater_DoubleDouble',hp,0),g.cmp('Less_DoubleDouble',hp,100)))
  use=g.br(guard,condition);prev=g.s(use,'Botiquines',g.op('Subtract_IntInt',g.v('Botiquines','int'),1,'int'),'int')
  prev=g.s(prev,'Health',g.c(MATH,'FMin',[('A','real',g.op('Add_DoubleDouble',hp,35)),('B','real',100)]),owner=HEALTH,target=health)
  notice(g.sound(prev,'Rescue'),'Botiquín utilizado: +35 de vida.');notice(use,'No necesitas curarte o no tienes botiquines.',pin='else')
 # BRUNO no cobra: convierte celdas recuperadas en energía de fabricación.
 for e in [entry(['E','Gamepad_RightShoulder'],'HablarConTecnico',False)]:
  guard=g.br(e,g.v('bInitialized','bool'));guard=g.br(guard,allowed())
  guard=g.br(guard,(g.valid(*tech),'ReturnValue'));guard=g.br(guard,g.cmp('LessEqual_DoubleDouble',(g.dist(*hero,*tech),'ReturnValue'),270))
  busy=g.br(guard,g.v('bFabricating','bool'))
  notice(busy,'BRUNO: estoy convirtiendo energía. No se consumen más créditos.')
  shopping=g.br(busy,g.cmp('Greater_DoubleDouble',g.v('DialogUntil'),now),'else')
  afford=g.br(shopping,g.cmp('GreaterEqual_IntInt',g.v('Creditos','int'),3,'int'))
  prev=g.s(afford,'Creditos',g.op('Subtract_IntInt',g.v('Creditos','int'),3,'int'),'int');prev=g.s(prev,'RobotEnergy',3,'int');prev=g.s(prev,'FabricationProgress',0);prev=g.s(prev,'bFabricating',True,'bool');notice(prev,'BRUNO: 3 créditos convertidos en energía. Fabricando botiquín (3 s).')
  notice(afford,'BRUNO: faltan 3 créditos de energía. Recupera celdas de los suministros.',pin='else')
  prev=g.s(shopping,'DialogSpeaker','BRUNO · UNIDAD DE RECICLAJE','string',pin='else')
  prev=g.s(prev,'DialogText','Soy BRUNO, robot de apoyo anclado a esta red. No puedo cruzar la extracción. Los créditos son celdas recuperadas: convierto 3 en energía para fabricar un botiquín. No es un pago. Tú y el sobreviviente deben salir. E / RB de nuevo inicia la conversión.','string')
  g.s(prev,'DialogUntil',g.op('Add_DoubleDouble',now,22))
 # Tercer ataque opcional: munición real y traza de visibilidad con alcance 8m.
 for e in [entry(['MiddleMouseButton','Gamepad_RightTrigger'],'DispararPulso')]:
  guard=g.br(e,g.v('bInitialized','bool'));guard=g.br(guard,allowed())
  can=g.both(g.cmp('Greater_IntInt',g.v('Cargas','int'),0,'int'),g.cmp('Greater_DoubleDouble',g.op('Subtract_DoubleDouble',now,g.v('LastPulseAt')),.8))
  can=g.both(can,g.neg(g.v('IsAttacking','bool',owner=HERO,target=hero)))
  prev=g.s(g.br(guard,can),'LastPulseAt',now);prev=g.s(prev,'Cargas',g.op('Subtract_IntInt',g.v('Cargas','int'),1,'int'),'int')
  pc=g.pc();cm=g.c(GS,'GetPlayerCameraManager',[('PlayerIndex','int',0)],cat='object',obj='/Script/Engine.PlayerCameraManager')
  loc=g.c('/Script/Engine.PlayerCameraManager','GetCameraLocation',cat='struct',obj=VEC,static=False);g.w(cm,loc[0],'self')
  rotation=g.c('/Script/Engine.PlayerCameraManager','GetCameraRotation',cat='struct',obj=ROT,static=False);g.w(cm,rotation[0],'self')
  forward=g.c(MATH,'GetForwardVector',[('InRot','struct',rotation)],cat='struct',obj=VEC);forward[0].pins['InRot']['obj']=ROT
  reach=g.c(MATH,'Multiply_VectorFloat',[('A','struct',forward),('B','real',800)],cat='struct',obj=VEC);reach[0].pins['A']['obj']=VEC
  end=g.c(MATH,'Add_VectorVector',[('A','struct',loc),('B','struct',reach)],cat='struct',obj=VEC)
  for p in ['A','B']:end[0].pins[p]['obj']=VEC
  trace=g.call('/Script/Engine.KismetSystemLibrary','SphereTraceSingle',static=True).pin('Start','struct',obj=VEC).pin('End','struct',obj=VEC).pin('Radius','real',sub='float',default='18').pin('TraceChannel','byte',obj='/Script/Engine.ETraceTypeQuery',default='TraceTypeQuery1').pin('bTraceComplex','bool',default='false').pin('ActorsToIgnore','object',obj=ACTOR).pin('DrawDebugType','byte',obj='/Script/Engine.EDrawDebugTrace',default='None').pin('bIgnoreSelf','bool',default='true').pin('OutHit','struct',obj='/Script/Engine.HitResult',out=True).pin('ReturnValue','bool',out=True)
  trace.pins['ActorsToIgnore']['container']='Array'
  array=g.node('K2Node_MakeArray',['NumInputs=1']).pin('[0]','object',obj=ACTOR).pin('Array','object',obj=ACTOR,out=True);array.pins['Array']['container']='Array';g.w(hero,array,'[0]');g.w((array,'Array'),trace,'ActorsToIgnore')
  g.w(loc,trace,'Start');g.w(end,trace,'End');g.chain(prev,trace)
  hit=g.call(GS,'BreakHitResult',pure=True,static=True).pin('Hit','struct',obj='/Script/Engine.HitResult').pin('HitActor','object',obj=ACTOR,out=True);g.w((trace,'OutHit'),hit,'Hit')
  post=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True).pin('then_1',out=True);g.chain(trace,post)
  cast,val=g.cast_after(post,(hit,'HitActor'),BASE,pin='then_0')
  living=g.br(cast,g.neg(g.v('bIsDead','bool',owner=BASE,target=val)))
  enemy_health_class='/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health.BPC_E_Health_C'
  enemy_health=g.v('BPC_E_Health','object',owner=BASE,target=val,obj=enemy_health_class)
  prev=g.action_on(living,enemy_health_class,'E_Decrease_Health',enemy_health,[('Damage','real',20,None)])
  g.sound(notice(post,'Pulso temporal: -1 carga.',pin='then_1'),'Upgrade')
 flatten(g,EXTRAS);g.write('BP_SistemasComplementarios')

if __name__=='__main__':systems()
