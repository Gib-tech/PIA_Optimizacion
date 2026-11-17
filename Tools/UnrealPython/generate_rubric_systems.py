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
 def item_trace(prev):
  cm=g.c(GS,'GetPlayerCameraManager',[('PlayerIndex','int',0)],cat='object',obj='/Script/Engine.PlayerCameraManager')
  start=g.c('/Script/Engine.PlayerCameraManager','GetCameraLocation',cat='struct',obj=VEC,static=False);g.w(cm,start[0],'self')
  rotation=g.c('/Script/Engine.PlayerCameraManager','GetCameraRotation',cat='struct',obj=ROT,static=False);g.w(cm,rotation[0],'self')
  forward=g.c(MATH,'GetForwardVector',[('InRot','struct',rotation)],cat='struct',obj=VEC);forward[0].pins['InRot']['obj']=ROT
  reach=g.c(MATH,'Multiply_VectorFloat',[('A','struct',forward),('B','real',350)],cat='struct',obj=VEC);reach[0].pins['A']['obj']=VEC
  end=g.c(MATH,'Add_VectorVector',[('A','struct',start),('B','struct',reach)],cat='struct',obj=VEC)
  for pin in ['A','B']:end[0].pins[pin]['obj']=VEC
  trace=g.call('/Script/Engine.KismetSystemLibrary','LineTraceSingle',static=True).pin('Start','struct',obj=VEC).pin('End','struct',obj=VEC).pin('TraceChannel','byte',obj='/Script/Engine.ETraceTypeQuery',default='TraceTypeQuery1').pin('bTraceComplex','bool',default='false').pin('ActorsToIgnore','object',obj=ACTOR).pin('DrawDebugType','byte',obj='/Script/Engine.EDrawDebugTrace',default='None').pin('bIgnoreSelf','bool',default='true').pin('OutHit','struct',obj='/Script/Engine.HitResult',out=True).pin('ReturnValue','bool',out=True)
  trace.pins['ActorsToIgnore']['container']='Array';array=g.node('K2Node_MakeArray',['NumInputs=1']).pin('[0]','object',obj=ACTOR).pin('Array','object',obj=ACTOR,out=True);array.pins['Array']['container']='Array';g.w(hero,array,'[0]');g.w((array,'Array'),trace,'ActorsToIgnore');g.w(start,trace,'Start');g.w(end,trace,'End');g.chain(prev,trace)
  hit=g.call(GS,'BreakHitResult',pure=True,static=True).pin('Hit','struct',obj='/Script/Engine.HitResult').pin('HitActor','object',obj=ACTOR,out=True);g.w((trace,'OutHit'),hit,'Hit')
  return trace,(hit,'HitActor')
 tick=g.event(ACTOR,'ReceiveTick').pin('DeltaSeconds','real',sub='float',out=True)
 seq=g.node('K2Node_ExecutionSequence').pin('execute')
 for i in range(7):seq.pin('then_'+str(i),out=True)
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
 # Los objetos de la mesa ya no son muestras decorativas. Sólo se ofrecen
 # cuando la traza de cámara los alcanza, sin atravesar robot/mesa/paredes.
 target=g.br(seq,g.v('bInitialized','bool'),'then_6');target=g.br(target,allowed());target=g.s(target,'ObjetoEnMira',0,'int');target=g.s(target,'DestruibleEnMira',None,'object',obj=R+'BP_DestruibleEntrega.BP_DestruibleEntrega_C');trace,hit_actor=item_trace(target)
 robot_look=g.s(trace,'bRobotEnMira',g.both((g.valid(*tech),'ReturnValue'),g.cmp('EqualEqual_ObjectObject',hit_actor,tech,'object')),'bool')
 cast,destructible=g.cast_after(robot_look,hit_actor,R+'BP_DestruibleEntrega.BP_DestruibleEntrega_C');selected_destructible=g.s(cast,'DestruibleEnMira',destructible,'object',obj=R+'BP_DestruibleEntrega.BP_DestruibleEntrega_C')
 items=g.node('K2Node_ExecutionSequence').pin('execute')
 for i in range(3):items.pin('then_'+str(i),out=True)
 g.chain(selected_destructible,items);g.chain(cast,items,'CastFailed')
 for i in range(1,4):
  obj=g.local('ItemMesa'+str(i),SM);ready_item=g.br(items,(g.valid(*obj),'ReturnValue'),'then_'+str(i-1))
  hidden=g.action_on(ready_item,ACTOR,'SetActorHiddenInGame',obj,[('bNewHidden','bool',g.v('MesaRecogido'+str(i),'bool'),None)])
  collision=g.action_on(hidden,ACTOR,'SetActorEnableCollision',obj,[('bNewActorEnableCollision','bool',g.neg(g.v('MesaRecogido'+str(i),'bool')),None)])
  selected=g.br(collision,g.both(g.neg(g.v('MesaRecogido'+str(i),'bool')),g.cmp('EqualEqual_ObjectObject',hit_actor,obj,'object')));g.s(selected,'ObjetoEnMira',i,'int')
 for e in [entry(['I','Gamepad_Special_Left'],'AlternarInventario')]:
  guard=g.br(e,g.v('bInitialized','bool'));guard=g.br(guard,allowed());g.s(guard,'InventoryOpen',g.neg(g.v('InventoryOpen','bool')),'bool')
 for e in [entry(['H','Gamepad_LeftShoulder'],'UsarBotiquin')]:
  guard=g.br(e,g.v('bInitialized','bool'));guard=g.br(guard,allowed())
  condition=g.both(g.cmp('Greater_IntInt',g.v('Botiquines','int'),0,'int'),g.both(g.cmp('Greater_DoubleDouble',hp,0),g.cmp('Less_DoubleDouble',hp,100)))
  use=g.br(guard,condition);prev=g.s(use,'Botiquines',g.op('Subtract_IntInt',g.v('Botiquines','int'),1,'int'),'int')
  # El componente limita a 100 y emite Updated_Heatlh, al que está enlazada
  # la barra. Asignar Health directamente curaba sin refrescar la interfaz.
  prev=g.action_on(prev,HEALTH,'Increase_Health',health,[('Amount','real',35,None)])
  current=g.c('/Script/Engine.KismetStringLibrary','Conv_IntToString',[('InInt','int',g.c(MATH,'FFloor',[('A','real',hp)],cat='int'))],cat='string')
  message=g.c('/Script/Engine.KismetStringLibrary','Concat_StrStr',[('A','string','Botiquín utilizado. Vida: '),('B','string',current)],cat='string')
  message=g.c('/Script/Engine.KismetStringLibrary','Concat_StrStr',[('A','string',message),('B','string',' / 100.')],cat='string')
  notice(g.sound(prev,'Rescue'),message);notice(use,'No necesitas curarte o no tienes botiquines.',pin='else')
 # BRUNO no cobra: convierte celdas recuperadas en energía de fabricación.
 for e in [entry(['E','Gamepad_RightShoulder'],'HablarConTecnico')]:
  guard=g.br(e,g.v('bInitialized','bool'));guard=g.br(guard,allowed())
  trace,hit_actor=item_trace(guard);fallthrough=trace;fallpin='then'
  for i,field,amount in [(1,'Botiquines',1),(2,'Cargas',3),(3,'Creditos',3)]:
   obj=g.local('ItemMesa'+str(i),SM);eligible=g.both((g.valid(*obj),'ReturnValue'),g.neg(g.v('MesaRecogido'+str(i),'bool')));eligible=g.both(eligible,g.cmp('EqualEqual_ObjectObject',hit_actor,obj,'object'))
   pick=g.br(fallthrough,eligible,fallpin);prev=g.s(pick,'MesaRecogido'+str(i),True,'bool');prev=g.s(prev,field,g.op('Add_IntInt',g.v(field,'int'),amount,'int'),'int')
   prev=g.action_on(prev,ACTOR,'SetActorHiddenInGame',obj,[('bNewHidden','bool',True,None)]);prev=g.action_on(prev,ACTOR,'SetActorEnableCollision',obj,[('bNewActorEnableCollision','bool',False,None)]);prev=g.s(prev,'ObjetoEnMira',0,'int')
   notice(g.sound(prev,'Rescue'),['','Botiquín recogido (+1). H / LB: curar.','Celdas de pulso recogidas (+3). Clic central / RT: disparar.','Créditos de energía recogidos (+3). E / RB con BRUNO: convertir.'][i])
   fallthrough=pick;fallpin='else'
  # Si no se apuntó a un objeto recogible, la interacción sigue con BRUNO.
  valid_tech=g.br(fallthrough,(g.valid(*tech),'ReturnValue'),fallpin)
  guard=g.br(valid_tech,g.both(g.cmp('LessEqual_DoubleDouble',(g.dist(*hero,*tech),'ReturnValue'),270),g.cmp('EqualEqual_ObjectObject',hit_actor,tech,'object')))
  # Una pulsación produce una sola acción. Sin objeto ni robot cercano,
  # reenviar la orden de escolta que antes atendía E/RB en el director.
  found_host=g.call(GS,'GetActorOfClass',static=True).pin('ActorClass','class',obj=ACTOR,default_obj=HOSTAGE).pin('ReturnValue','object',obj=HOSTAGE,out=True);g.chain(guard,found_host,'else');g.chain(valid_tech,found_host,'else')
  valid_host=g.br(found_host,(g.valid(found_host,'ReturnValue'),'ReturnValue'));g.action_on(valid_host,HOSTAGE,'Interactuar',(found_host,'ReturnValue'))
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
  hit=g.call(GS,'BreakHitResult',pure=True,static=True).pin('Hit','struct',obj='/Script/Engine.HitResult').pin('HitActor','object',obj=ACTOR,out=True).pin('bBlockingHit','bool',out=True).pin('ImpactPoint','struct',obj=VEC,out=True);g.w((trace,'OutHit'),hit,'Hit')
  post=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True).pin('then_1',out=True).pin('then_2',out=True);g.chain(trace,post)
  cast,val=g.cast_after(post,(hit,'HitActor'),BASE,pin='then_0')
  living=g.br(cast,g.neg(g.v('bIsDead','bool',owner=BASE,target=val)))
  enemy_health_class='/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health.BPC_E_Health_C'
  enemy_health=g.v('BPC_E_Health','object',owner=BASE,target=val,obj=enemy_health_class)
  prev=g.action_on(living,enemy_health_class,'E_Decrease_Health',enemy_health,[('Damage','real',20,None)])
  g.sound(notice(post,'Pulso temporal: -1 carga.',pin='then_1'),'Upgrade')
  # Rayo visible, sin colisión/daño: la única autoridad sigue siendo la traza.
  chosen=g.call(MATH,'SelectVector',pure=True,static=True).pin('A','struct',obj=VEC).pin('B','struct',obj=VEC).pin('bPickA','bool').pin('ReturnValue','struct',obj=VEC,out=True);g.w((hit,'bBlockingHit'),chosen,'bPickA');g.w(end,chosen,'B');g.w((hit,'ImpactPoint'),chosen,'A');endpoint=(chosen,'ReturnValue')
  midpoint=g.c(MATH,'Add_VectorVector',[('A','struct',loc),('B','struct',endpoint)],cat='struct',obj=VEC)
  for pin in ['A','B']:midpoint[0].pins[pin]['obj']=VEC
  midpoint=g.c(MATH,'Multiply_VectorFloat',[('A','struct',midpoint),('B','real',.5)],cat='struct',obj=VEC);midpoint[0].pins['A']['obj']=VEC
  look=g.c(MATH,'FindLookAtRotation',[('Start','struct',loc),('Target','struct',endpoint)],cat='struct',obj=ROT)
  for pin in ['Start','Target']:look[0].pins[pin]['obj']=VEC
  distance=g.c(MATH,'Vector_Distance',[('V1','struct',loc),('V2','struct',endpoint)])
  for pin in ['V1','V2']:distance[0].pins[pin]['obj']=VEC
  beam_scale=g.c(MATH,'MakeVector',[('X','real',g.op('Divide_DoubleDouble',distance,100)),('Y','real',.025),('Z','real',.025)],cat='struct',obj=VEC)
  transform=g.c(MATH,'MakeTransform',[('Location','struct',midpoint),('Rotation','struct',look),('Scale','struct',beam_scale)],cat='struct',obj='/Script/CoreUObject.Transform')
  for pin,obj in [('Location',VEC),('Rotation',ROT),('Scale',VEC)]:transform[0].pins[pin]['obj']=obj
  beam_cls=R+'BP_PulsoTemporalVisual.BP_PulsoTemporalVisual_C'
  spawn=g.node('K2Node_SpawnActorFromClass').pin('execute').pin('then',out=True).pin('Class','class',obj=ACTOR,default_obj=beam_cls).pin('SpawnTransform','struct',obj='/Script/CoreUObject.Transform').pin('CollisionHandlingOverride','byte',obj='/Script/Engine.ESpawnActorCollisionHandlingMethod',default='AlwaysSpawn').pin('Owner','object',obj=ACTOR).pin('TransformScaleMethod','byte',obj='/Script/Engine.ESpawnActorScaleMethod',default='MultiplyWithRoot').pin('ReturnValue','object',obj=beam_cls,out=True);g.w(transform,spawn,'SpawnTransform');g.chain(post,spawn,'then_2')
 flatten(g,EXTRAS);g.write('BP_SistemasComplementarios')

if __name__=='__main__':systems()
