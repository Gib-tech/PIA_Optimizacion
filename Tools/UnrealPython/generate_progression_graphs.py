"""Blueprint clipboard sources for hostage beacon channeling and hammer-gated doors."""
from generate_combat_graphs import CombatGraph,ACTOR,OBJECT,BASE,CHAR,MOVE,ref,q
from generate_wave_graphs import HOSTAGE,ZONE,PLAYER,TRANSFORM
from generate_delivery_graphs import DIRECTOR,HEALTH
R='/Game/ThirdPerson/Blueprints/Entrega/'
DOOR=R+'BP_DestructibleDoor.BP_DestructibleDoor_C'
BEACON=R+'BP_BeaconEntrega.BP_BeaconEntrega_C'
HERO=R+'BP_PlayerEntrega.BP_PlayerEntrega_C'
FRAGMENT=R+'BP_DoorFragment.BP_DoorFragment_C'
MATH='/Script/Engine.KismetMathLibrary';GS='/Script/Engine.GameplayStatics'
PRIM='/Script/Engine.PrimitiveComponent';SCENE='/Script/Engine.SceneComponent'
VEC='/Script/CoreUObject.Vector';SM='/Script/Engine.StaticMeshActor';SMC='/Script/Engine.StaticMeshComponent'

class ProgressGraph(CombatGraph):
 def node(self,kind,props=(),**pos):
  i=len(self.nodes);pos.setdefault('x',(i%9)*390);pos.setdefault('y',(i//9)*350)
  return super().node(kind,props,**pos)
 def w(self,value,n,p):
  if isinstance(value,tuple):
   if value[0].pins[value[1]]['cat']=='int' and n.pins[p]['cat']=='real':value=self.c(MATH,'Conv_IntToDouble',[('InInt','int',value)])
   self.wire(*value,n,p)
  elif value is not None:n.pins[p]['default']=str(value).lower() if isinstance(value,bool) else str(value)
 def c(self,owner,name,inputs=(),cat='real',obj=None,pure=True,static=True,output='ReturnValue'):
  n=self.call(owner,name,pure=pure,static=static)
  for p,t,v in inputs:n.pin(p,t,sub='double' if t=='real' else '');self.w(v,n,p)
  n.pin(output,cat,obj=obj,sub='double' if cat=='real' else '',out=True);return n,output
 def v(self,name,cat='real',owner=None,obj=None,target=None,native=False):
  n=(self.nativeget if native else self.get)(owner,name,cat,obj=obj,sub='double' if cat=='real' else '') if native else self.get(name,cat,owner=owner,obj=obj,sub='double' if cat=='real' else '')
  if target:self.w(target,n,'self')
  return n,name
 def s(self,prev,name,value,cat='real',owner=None,target=None,obj=None,pin='then'):
  n=self.set(name,cat,None,obj=obj,sub='double' if cat=='real' else '')
  if owner:
   n.props=['VariableReference=(MemberParent='+ref(owner) if owner.startswith('/Script/') else 'VariableReference=(MemberParent='+q("/Script/Engine.BlueprintGeneratedClass'"+owner+"'")]
   n.props[0]+= ',MemberName='+q(name)+')';n.pin('self','object',obj=owner);self.w(target,n,'self')
  self.w(value,n,name);self.chain(prev,n,pin);return n
 def op(self,fn,a,b,cat='real'):return self.c(MATH,fn,[('A',cat,a),('B',cat,b)],cat=cat)
 def cmp(self,fn,a,b,cat='real'):return self.c(MATH,fn,[('A',cat,a),('B',cat,b)],cat='bool')
 def both(self,a,b):return self.c(MATH,'BooleanAND',[('A','bool',a),('B','bool',b)],cat='bool')
 def neg(self,a):return self.c(MATH,'Not_PreBool',[('A','bool',a)],cat='bool')
 def br(self,prev,value,pin='then'):
  n=self.branch();self.chain(prev,n,pin);self.w(value,n,'Condition');return n
 def find(self,prev,cls):
  n=self.call(GS,'GetActorOfClass',static=True).pin('ActorClass','class',obj=ACTOR,default_obj=cls).pin('ReturnValue','object',obj=cls,out=True);self.chain(prev,n);return n
 def fx(self,prev,name,component=None):
  n=self.call('/Script/Niagara.NiagaraFunctionLibrary','SpawnSystemAttached' if component else 'SpawnSystemAtLocation',static=True).pin('SystemTemplate','object',obj='/Script/Niagara.NiagaraSystem',default_obj=R+'FX/'+name+'.'+name).pin('bAutoDestroy','bool',default='true').pin('bAutoActivate','bool',default='true').pin('PoolingMethod','byte',obj='/Script/Niagara.ENCPoolMethod',default='None').pin('bPreCullCheck','bool',default='false').pin('Scale','struct',obj=VEC,default='.4,.4,.4').pin('ReturnValue','object',obj='/Script/Niagara.NiagaraComponent',out=True)
  if component:
   n.pin('AttachToComponent','object',obj=SCENE).pin('AttachPointName','name',default='None').pin('Location','struct',obj=VEC,default='0,0,0').pin('Rotation','struct',obj='/Script/CoreUObject.Rotator',default='0,0,0').pin('LocationType','byte',obj='/Script/Engine.EAttachLocation',default='KeepRelativeOffset');self.w(component,n,'AttachToComponent')
  else:
   n.pin('WorldContextObject','object',obj=OBJECT,hidden=True).pin('Location','struct',obj=VEC).pin('Rotation','struct',obj='/Script/CoreUObject.Rotator',default='0,0,0');pos=self.location(self.selfnode(typ=ACTOR),'self');self.wire(pos,'ReturnValue',n,'Location')
  self.chain(prev,n);return n
 def sound(self,prev,name):
  n=self.call(GS,'PlaySound2D',static=True).pin('Sound','object',obj='/Script/Engine.SoundBase',default_obj='/Game/ThirdPerson/Audio/SW_'+name+'.SW_'+name).pin('VolumeMultiplier','real',sub='float',default='.5').pin('PitchMultiplier','real',sub='float',default='1').pin('StartTime','real',sub='float',default='0').pin('ConcurrencySettings','object',obj='/Script/Engine.SoundConcurrency').pin('OwningActor','object',obj=ACTOR).pin('bIsUISound','bool',default='false');self.chain(prev,n);return n

def capture(fn):
 from generate_delivery_graphs import Graph
 result=[];old=CombatGraph.write;baseold=Graph.write;CombatGraph.write=lambda g,n:result.append(g);Graph.write=lambda g,n:result.append(g)
 try:fn()
 finally:CombatGraph.write=old;Graph.write=baseold
 g=result[0];g.__class__=ProgressGraph;return g

def player():
 from generate_wave_graphs import heavy_player
 g=capture(heavy_player)
 overlap=next(n for n in g.nodes if 'SweepResult' in n.pins)
 charger=next(n for n in g.nodes if n.kind.endswith('K2Node_DynamicCast'))
 door=g.cast(DOOR);g.chain(charger,door,'CastFailed');g.wire(overlap,'OtherActor',door,'Object')
 fresh=g.neg((g.array('HeavyHitActors','Array_Contains',item=overlap,ip='OtherActor'),'ReturnValue'))
 allowed=g.both(g.neg(g.v('bLightAttackActive','bool')),g.both(g.v('bHammerUpgraded','bool'),g.v('bIsHammerEquipped','bool')))
 b=g.br(door,g.both(allowed,fresh));cache=g.array('HeavyHitActors','Array_AddUnique',item=overlap,ip='OtherActor');g.chain(b,cache)
 dmg=g.call(GS,'ApplyDamage',static=True).pin('DamagedActor','object',obj=ACTOR).pin('BaseDamage','real',sub='float',default='25').pin('EventInstigator','object',obj='/Script/Engine.Controller').pin('DamageCauser','object',obj=ACTOR).pin('DamageTypeClass','class',obj='/Script/Engine.DamageType').pin('ReturnValue','real',sub='float',out=True);g.chain(cache,dmg);g.wire(overlap,'OtherActor',dmg,'DamagedActor');g.wire(g.selfnode(typ=HERO),'self',dmg,'DamageCauser')
 begin=next(n for n in g.nodes if n.kind.endswith('K2Node_Event') and any('ReceiveBeginPlay' in p for p in n.props));tail=next(n for n in g.nodes if any('K2_SetRelativeLocation' in p for p in n.props))
 hitbox=g.v('WeaponHitbox','object',obj='/Script/Engine.BoxComponent')
 collision=g.call(PRIM,'SetCollisionResponseToChannel').pin('Channel','byte',obj='/Script/Engine.ECollisionChannel',default='ECC_WorldDynamic').pin('NewResponse','byte',obj='/Script/Engine.ECollisionResponse',default='ECR_Overlap');g.w(hitbox,collision,'self');g.chain(tail,collision)
 relative=g.call(SCENE,'GetRelativeTransform',pure=True).pin('ReturnValue','struct',obj=TRANSFORM,out=True);g.w(hitbox,relative,'self')
 sword_transform_saved=g.s(collision,'SwordHitboxRelativeTransform',(relative,'ReturnValue'),'struct',obj=TRANSFORM)
 def attach_hitbox(prev,hammer,prevpin='then'):
  disable=g.call(PRIM,'SetCollisionEnabled').pin('NewType','byte',obj='/Script/Engine.ECollisionEnabled',default='NoCollision');g.w(hitbox,disable,'self');g.chain(prev,disable,prevpin)
  attach=g.call(SCENE,'K2_AttachToComponent').pin('Parent','object',obj=SCENE).pin('SocketName','name',default='None').pin('bWeldSimulatedBodies','bool',default='false').pin('ReturnValue','bool',out=True)
  for pin in ['LocationRule','RotationRule','ScaleRule']:attach.pin(pin,'byte',obj='/Script/Engine.EAttachmentRule',default='SnapToTarget')
  g.w(hitbox,attach,'self');g.w(g.v('hammer' if hammer else 'Weapon','object',obj='/Script/Engine.SkeletalMeshComponent' if hammer else SMC),attach,'Parent');g.chain(disable,attach)
  transform=g.call(SCENE,'K2_SetRelativeTransform').pin('NewTransform','struct',obj=TRANSFORM,default='(Rotation=(X=0,Y=0,Z=0,W=1),Translation=(X=0,Y=10,Z=145),Scale3D=(X=1,Y=1,Z=1))').pin('bSweep','bool',default='false').pin('SweepHitResult','struct',obj='/Script/Engine.HitResult',out=True).pin('bTeleport','bool',default='true');g.w(hitbox,transform,'self');g.chain(attach,transform)
  if not hammer:g.w(g.v('SwordHitboxRelativeTransform','struct',obj=TRANSFORM),transform,'NewTransform')
  else:
   make=g.call(MATH,'MakeTransform',pure=True,static=True).pin('Location','struct',obj=VEC,default='0,10,145').pin('Rotation','struct',obj='/Script/CoreUObject.Rotator',default='0,0,0').pin('Scale','struct',obj=VEC,default='1,1,1').pin('ReturnValue','struct',obj=TRANSFORM,out=True);g.wire(make,'ReturnValue',transform,'NewTransform')
  extent=g.call('/Script/Engine.BoxComponent','SetBoxExtent').pin('InBoxExtent','struct',obj=VEC,default='35,45,145' if hammer else '45,45,90').pin('bUpdateOverlaps','bool',default='false');g.w(hitbox,extent,'self');g.chain(transform,extent)
  return g.s(extent,'bHitboxOnHammer',hammer,'bool')
 attach_hitbox(sword_transform_saved,False)
 cacheclear=next(n for n in g.nodes if any('Array_Clear' in p for p in n.props))
 idle=g.br(cacheclear,g.neg(g.v('IsAttacking','bool')))
 changed=g.cmp('NotEqual_BoolBool',g.v('bIsHammerEquipped','bool'),g.v('bHitboxOnHammer','bool'),'bool');update=g.br(idle,changed);which=g.br(update,g.v('bIsHammerEquipped','bool'));attach_hitbox(which,True)
 attach_hitbox(which,False,'else')
 upgrade=g.custom('GrantHammerUpgrade').pin('Door','object',obj=DOOR,out=True)
 upgrade.props.append('CustomProperties UserDefinedPin (PinName="Door",PinType=(PinCategory="object",PinSubCategoryObject='+q("/Script/Engine.BlueprintGeneratedClass'"+DOOR+"'")+'),DesiredPinDirection=EGPD_Output)')
 prev=g.s(upgrade,'bHammerUpgraded',True,'bool');prev=g.s(prev,'bDoorPending',True,'bool');prev=g.s(prev,'RequiredDoor',(upgrade,'Door'),'object',obj=DOOR)
 now=g.c(GS,'GetTimeSeconds');prev=g.s(prev,'UpgradeUntil',g.op('Add_DoubleDouble',now,6))
 prev=g.s(prev,'IsAttacking',False,'bool');prev=g.s(prev,'bLightAttackActive',False,'bool')
 stop=g.call(CHAR,'StopAnimMontage').pin('AnimMontage','object',obj='/Script/Engine.AnimMontage');g.chain(prev,stop);prev=stop
 disable=g.call(PRIM,'SetCollisionEnabled').pin('NewType','byte',obj='/Script/Engine.ECollisionEnabled',default='NoCollision');g.w(hitbox,disable,'self');g.chain(prev,disable);prev=disable
 for field,visible in [('hammer',True),('Weapon',False)]:
  component=g.v(field,'object',obj='/Script/Engine.SkeletalMeshComponent' if field=='hammer' else SMC)
  n=g.call(SCENE,'SetVisibility').pin('bNewVisibility','bool',default=str(visible).lower()).pin('bPropagateToChildren','bool',default='true');g.w(component,n,'self');g.chain(prev,n);prev=n
 prev=g.s(prev,'bIsHammerEquipped',True,'bool');prev=g.s(prev,'bIsSwordEquipped',False,'bool');prev=attach_hitbox(prev,True);prev=g.fx(prev,'NS_HammerUpgrade',g.v('hammer','object',obj='/Script/Engine.SkeletalMeshComponent'));g.sound(prev,'Upgrade')
 # Heavy sword and hammer montage callbacks are disconnected in the parent.
 # Manage their authored hit windows in this child, with interruption cleanup.
 tick=next(n for n in g.nodes if n.kind.endswith('K2Node_Event') and any('ReceiveTick' in p for p in n.props))
 old=list(tick.pins['then']['links']);tick.pins['then']['links']=[]
 seq=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True).pin('then_1',out=True).pin('then_2',out=True).pin('then_3',out=True);g.chain(tick,seq)
 for name,pid in old:
  n=next(n for n in g.nodes if n.name==name);p=next(p for p in n.pins.values() if p['id']==pid);p['links'].remove((tick.name,tick.pins['then']['id']));g.chain(seq,n,'then_0',p['name'])
 current=g.call(CHAR,'GetCurrentMontage',pure=True).pin('ReturnValue','object',obj='/Script/Engine.AnimMontage',out=True)
 anim=g.call('/Script/Engine.SkeletalMeshComponent','GetAnimInstance',pure=True).pin('ReturnValue','object',obj='/Script/Engine.AnimInstance',out=True);g.w(g.v('Mesh','object',obj='/Script/Engine.SkeletalMeshComponent'),anim,'self')
 pos=g.call('/Script/Engine.AnimInstance','Montage_GetPosition',pure=True).pin('Montage','object',obj='/Script/Engine.AnimMontage').pin('ReturnValue','real',sub='float',out=True);g.wire(anim,'ReturnValue',pos,'self');g.wire(current,'ReturnValue',pos,'Montage')
 changed=g.cmp('NotEqual_ObjectObject',(current,'ReturnValue'),g.v('LastAttackMontage','object',obj='/Script/Engine.AnimMontage'),'object')
 rewound=g.cmp('Less_DoubleDouble',g.op('Add_DoubleDouble',(pos,'ReturnValue'),.01),g.v('LastAttackPosition'))
 reset=g.br(seq,g.c(MATH,'BooleanOR',[('A','bool',changed),('B','bool',rewound)],cat='bool'),'then_1')
 fresh=g.array('HeavyHitActors','Array_Clear');g.chain(reset,fresh)
 saved=g.s(fresh,'LastAttackMontage',(current,'ReturnValue'),'object',obj='/Script/Engine.AnimMontage');tail=g.s(saved,'LastAttackPosition',(pos,'ReturnValue'));g.chain(reset,tail,'else')
 managedmatch=None;inwindow=None
 # The original assets are preserved. Missing hit windows are defined here.
 specs=[('Attack_3_Montage',.252330,1.183353),('Heavy_attacks/Sword/H_attack_1_Montage',.82,1.05),('Heavy_attacks/Sword/H_attack_2_Montage',.28,.75),('Heavy_attacks/Sword/H_attack_3_Montage',.50,1.25),('Fast_attacks/sword/L_FA_4_Montage',.18,.65),('Fast_attacks/Hammer/HA_1_Montage',.55,.90),('Fast_attacks/Hammer/HA_2_Montage',.16,.50)]
 for path,a,b in specs:
  same=g.call(MATH,'EqualEqual_ObjectObject',pure=True,static=True).pin('A','object',obj=OBJECT).pin('B','object',obj=OBJECT,default_obj='/Game/ThirdPerson/Animations/'+path+'.'+path.rsplit('/',1)[-1]).pin('ReturnValue','bool',out=True);g.wire(current,'ReturnValue',same,'A');match=(same,'ReturnValue')
  bounds=g.both(g.cmp('GreaterEqual_DoubleDouble',(pos,'ReturnValue'),a),g.cmp('Less_DoubleDouble',(pos,'ReturnValue'),b));bounds=g.both(match,bounds)
  managedmatch=match if managedmatch is None else g.c(MATH,'BooleanOR',[('A','bool',managedmatch),('B','bool',match)],cat='bool')
  inwindow=bounds if inwindow is None else g.c(MATH,'BooleanOR',[('A','bool',inwindow),('B','bool',bounds)],cat='bool')
 managed=g.br(seq,g.both(g.v('IsAttacking','bool'),managedmatch),'then_2');mark=g.s(managed,'bHeavyWindowManaged',True,'bool')
 window=g.br(mark,inwindow)
 for pin,enabled in [('then','QueryOnly'),('else','NoCollision')]:
  collision=g.call(PRIM,'SetCollisionEnabled').pin('NewType','byte',obj='/Script/Engine.ECollisionEnabled',default=enabled);g.w(hitbox,collision,'self');g.chain(window,collision,pin)
 ended=g.br(managed,g.v('bHeavyWindowManaged','bool'),'else');clear=g.s(ended,'bHeavyWindowManaged',False,'bool')
 disable=g.call(PRIM,'SetCollisionEnabled').pin('NewType','byte',obj='/Script/Engine.ECollisionEnabled',default='NoCollision');g.w(hitbox,disable,'self');g.chain(clear,disable)
 interrupted=g.br(disable,g.neg(g.v('bLightAttackActive','bool')));g.s(interrupted,'IsAttacking',False,'bool')
 # The parent's canAttack notify releases movement while the full-body heavy
 # montage still owns the pose. End its recovery cleanly before locomotion resumes.
 sword_ready=None
 for path,cut in [('H_attack_1_Montage',1.18),('H_attack_2_Montage',1.05),('H_attack_3_Montage',1.70)]:
  same=g.call(MATH,'EqualEqual_ObjectObject',pure=True,static=True).pin('A','object',obj=OBJECT).pin('B','object',obj=OBJECT,default_obj='/Game/ThirdPerson/Animations/Heavy_attacks/Sword/'+path+'.'+path).pin('ReturnValue','bool',out=True);g.wire(current,'ReturnValue',same,'A')
  ready=g.c(MATH,'BooleanOR',[('A','bool',g.neg(g.v('IsAttacking','bool'))),('B','bool',g.cmp('GreaterEqual_DoubleDouble',(pos,'ReturnValue'),cut))],cat='bool')
  ready=g.both((same,'ReturnValue'),ready)
  sword_ready=ready if sword_ready is None else g.c(MATH,'BooleanOR',[('A','bool',sword_ready),('B','bool',ready)],cat='bool')
 recover=g.br(seq,sword_ready,'then_3')
 stop=g.call('/Script/Engine.AnimInstance','Montage_Stop').pin('InBlendOutTime','real',sub='float',default='.12').pin('Montage','object',obj='/Script/Engine.AnimMontage');g.wire(anim,'ReturnValue',stop,'self');g.wire(current,'ReturnValue',stop,'Montage');g.chain(recover,stop)
 clean=g.s(stop,'IsAttacking',False,'bool');clean=g.s(clean,'bLightAttackActive',False,'bool');clean=g.s(clean,'bHeavyWindowManaged',False,'bool');clean=g.s(clean,'AttackIndex',0,'int')
 off=g.call(PRIM,'SetCollisionEnabled').pin('NewType','byte',obj='/Script/Engine.ECollisionEnabled',default='NoCollision');g.w(hitbox,off,'self');g.chain(clean,off)
 reset=g.action('ResetState',owner=PLAYER);g.chain(off,reset)
 sheath=g.action('WeaponToBack',owner=PLAYER);g.chain(reset,sheath)
 g.write('BP_PlayerEntrega')

def door():
 g=ProgressGraph();e=g.event(ACTOR,'ReceiveAnyDamage').pin('Damage','real',sub='float',out=True).pin('DamageType','object',obj='/Script/Engine.DamageType',out=True).pin('InstigatedBy','object',obj='/Script/Engine.Controller',out=True).pin('DamageCauser','object',obj=ACTOR,out=True)
 cast=g.cast(HERO);g.chain(e,cast);g.wire(e,'DamageCauser',cast,'Object');hero=(cast,'AsBP_PlayerEntrega')
 valid=g.both(g.v('bUnlocked','bool'),g.neg(g.v('bDestroyed','bool')))
 for name,invert in [('bHammerUpgraded',False),('bIsHammerEquipped',False),('IsAttacking',False),('bLightAttackActive',True)]:
  value=g.v(name,'bool',owner=HERO,target=hero);valid=g.both(valid,g.neg(value) if invert else value)
 valid=g.both(valid,g.cmp('Greater_DoubleDouble',(e,'Damage'),0));b=g.br(cast,valid)
 amount=g.c(MATH,'FMin',[('A','real',(e,'Damage')),('B','real',25)])
 hp=g.s(b,'Health',g.c(MATH,'FMax',[('A','real',g.op('Subtract_DoubleDouble',g.v('Health'),amount)),('B','real',0)]))
 impact=g.sound(hp,'DoorHit')
 damaged=g.both(g.cmp('Greater_DoubleDouble',g.v('Health'),0),g.cmp('Less_DoubleDouble',g.v('Health'),50))
 first=g.br(impact,g.both(damaged,g.neg(g.v('bCracked','bool'))));mark=g.s(first,'bCracked',True,'bool')
 comp=g.v('StaticMeshComponent','object',owner=SM,obj=SMC,native=True,target=(g.selfnode(typ=DOOR),'self'))
 mesh=g.call(SMC,'SetStaticMesh').pin('NewMesh','object',obj='/Script/Engine.StaticMesh').pin('ReturnValue','bool',out=True);g.w(comp,mesh,'self');g.w(g.v('CrackedMesh','object',obj='/Script/Engine.StaticMesh'),mesh,'NewMesh');g.chain(mark,mesh);mark=mesh
 broken=g.br(mark,g.cmp('LessEqual_DoubleDouble',g.v('Health'),0));g.chain(first,broken,'else')
 prev=g.s(broken,'bDestroyed',True,'bool');prev=g.s(prev,'bDoorPending',False,'bool',owner=HERO,target=hero)
 c=g.call(ACTOR,'SetActorEnableCollision').pin('bNewActorEnableCollision','bool',default='false');g.chain(prev,c)
 hide=g.call(ACTOR,'SetActorHiddenInGame').pin('bNewHidden','bool',default='true');g.chain(c,hide)
 prev=g.fx(hide,'NS_DoorBreak');prev=g.sound(prev,'DoorBreak')
 from generate_fracture_graphs import spawn_shards
 spawn_shards(g,prev,hero)
 g.write('BP_DestructibleDoor')

def fragment():
 from generate_fracture_graphs import fragment as build
 build()

def beacon():
 g=ProgressGraph();e=g.custom('CompleteActivation').pin('Hostage','object',obj=HOSTAGE,out=True)
 e.props.append('CustomProperties UserDefinedPin (PinName="Hostage",PinType=(PinCategory="object",PinSubCategoryObject='+q("/Script/Engine.BlueprintGeneratedClass'"+HOSTAGE+"'")+'),DesiredPinDirection=EGPD_Output)')
 bb=g.blackboard(e,'Hostage');rescued=(g.bbget(bb,'bRescued'),'ReturnValue')
 director=g.find(e,DIRECTOR);step=g.v('Paso','int',owner=DIRECTOR,target=(director,'ReturnValue'))
 required=g.v('RequiredZone','object',obj=ZONE);cleared=g.v('bCleared','bool',owner=ZONE,target=required)
 ok=g.both(g.neg(g.v('bActivated','bool')),g.both(cleared,rescued));ok=g.both(ok,g.cmp('EqualEqual_IntInt',step,g.op('Subtract_IntInt',g.v('Index','int'),1,'int'),'int'))
 ok=g.both(ok,g.cmp('Greater_DoubleDouble',g.v('Health',owner=HOSTAGE,target=(e,'Hostage')),0))
 ok=g.both(ok,g.v('bUsingBeacon','bool',owner=HOSTAGE,target=(e,'Hostage')))
 ok=g.both(ok,g.cmp('GreaterEqual_DoubleDouble',g.v('ActivationProgress',owner=HOSTAGE,target=(e,'Hostage')),1))
 ok=g.both(ok,g.cmp('LessEqual_DoubleDouble',(g.dist(e,'Hostage',g.selfnode(typ=BEACON),'self'),'ReturnValue'),220))
 b=g.br(director,ok);prev=g.s(b,'bActivated',True,'bool');door=g.v('Door','object',obj=DOOR)
 prev=g.s(prev,'bUnlocked',True,'bool',owner=DOOR,target=door)
 component=g.v('StaticMeshComponent','object',owner=SM,obj=SMC,native=True,target=door)
 mat=g.call(PRIM,'SetMaterial').pin('ElementIndex','int',default='2').pin('Material','object',obj='/Script/Engine.MaterialInterface',default_obj='/Game/ThirdPerson/Environment/Progression/M_DoorPowered.M_DoorPowered');g.w(component,mat,'self');g.chain(prev,mat)
 pc=g.cast(HERO);g.chain(mat,pc);g.wire(g.player(),'ReturnValue',pc,'Object')
 grant=g.action('GrantHammerUpgrade',owner=HERO).pin('Door','object',obj=DOOR);g.wire(pc,'AsBP_PlayerEntrega',grant,'self');g.w(door,grant,'Door');g.chain(pc,grant)
 prev=g.s(grant,'Paso',g.v('Index','int'),'int',owner=DIRECTOR,target=(director,'ReturnValue'))
 own=g.v('StaticMeshComponent','object',owner=SM,obj=SMC,native=True,target=(g.selfnode(typ=SM),'self'))
 m=g.call(PRIM,'SetMaterial').pin('ElementIndex','int',default='0').pin('Material','object',obj='/Script/Engine.MaterialInterface',default_obj='/Game/ThirdPerson/Environment/EscenarioIan/M_Baliza_Activa.M_Baliza_Activa');g.w(own,m,'self');g.chain(prev,m)
 g.write('BP_BeaconEntrega')

def hostage():
 from generate_hostage_graphs import hostage as original
 g=capture(original);interact=next(n for n in g.nodes if n.kind.endswith('K2Node_CustomEvent'));b=next(n for n in g.nodes if n.kind.endswith('K2Node_IfThenElse'))
 src,pid=b.pins['Condition']['links'][0];source=next(n for n in g.nodes if n.name==src);pin=next(p['name'] for p in source.pins.values() if p['id']==pid)
 source.pins[pin]['links'].remove((b.name,b.pins['Condition']['id']));b.pins['Condition']['links']=[]
 g.w(g.both((source,pin),g.both(g.neg(g.v('bIsDead','bool')),g.neg(g.v('bUsingBeacon','bool')))),b,'Condition')
 e=g.event(ACTOR,'ReceiveAnyDamage').pin('Damage','real',sub='float',out=True).pin('DamageType','object',obj='/Script/Engine.DamageType',out=True).pin('InstigatedBy','object',obj='/Script/Engine.Controller',out=True).pin('DamageCauser','object',obj=ACTOR,out=True)
 cast=g.cast(BASE);g.chain(e,cast);g.wire(e,'DamageCauser',cast,'Object');now=g.c(GS,'GetTimeSeconds')
 ok=g.both(g.neg(g.v('bIsDead','bool')),g.both(g.cmp('Greater_DoubleDouble',(e,'Damage'),0),g.cmp('GreaterEqual_DoubleDouble',now,g.v('InvulnerableUntil'))))
 bb=g.blackboard(g.selfnode(typ=HOSTAGE),'self');ok=g.both(ok,(g.bbget(bb,'bRescued'),'ReturnValue'));hit=g.br(cast,ok)
 prev=g.s(hit,'Health',g.c(MATH,'FMax',[('A','real',g.op('Subtract_DoubleDouble',g.v('Health'),(e,'Damage'))),('B','real',0)]));prev=g.s(prev,'InvulnerableUntil',g.op('Add_DoubleDouble',now,.8))
 dead=g.br(prev,g.cmp('LessEqual_DoubleDouble',g.v('Health'),0));prev=g.s(dead,'bIsDead',True,'bool');prev=g.s(prev,'bUsingBeacon',False,'bool')
 move=g.v('CharacterMovement','object',owner=CHAR,obj=MOVE,native=True,target=(g.selfnode(typ=HOSTAGE),'self'));stop=g.call(MOVE,'DisableMovement');g.w(move,stop,'self');g.chain(prev,stop)
 director=g.find(stop,DIRECTOR);prev=g.s(director,'Paso',6,'int',owner=DIRECTOR,target=(director,'ReturnValue'));g.chain(prev,g.pause());g.write('BP_Hostage')

def activate_task():
 g=ProgressGraph();TASK='/Script/AIModule.BTTask_BlueprintBase'
 e=g.task_event('ReceiveExecuteAI');tick=g.task_event('ReceiveTickAI');abort=g.task_event('ReceiveAbortAI')
 cast=g.cast(HOSTAGE);g.chain(e,cast);g.wire(e,'ControlledPawn',cast,'Object');g.finish(cast,'CastFailed',success=False)
 prev=g.s(cast,'CachedPawn',(cast,'AsBP_Hostage'),'object',obj=HOSTAGE);pawn=g.v('CachedPawn','object',obj=HOSTAGE);bb=g.blackboard(e,'OwnerController');target=g.bbget(bb,'ActiveBeacon','Object')
 bc=g.cast(BEACON);g.chain(prev,bc);g.wire(target,'ReturnValue',bc,'Object');g.finish(bc,'CastFailed',success=False)
 prev=g.s(bc,'Beacon',(bc,'AsBP_BeaconEntrega'),'object',obj=BEACON);prev=g.s(prev,'Elapsed',0);g.s(prev,'bUsingBeacon',True,'bool',owner=HOSTAGE,target=pawn)
 elapsed=g.s(tick,'Elapsed',g.op('Add_DoubleDouble',g.v('Elapsed'),(tick,'DeltaSeconds')))
 prev=g.s(elapsed,'ActivationProgress',g.c(MATH,'FMin',[('A','real',g.op('Divide_DoubleDouble',g.v('Elapsed'),3)),('B','real',1)]),owner=HOSTAGE,target=pawn)
 b=g.br(prev,g.cmp('GreaterEqual_DoubleDouble',g.v('Elapsed'),3));beac=g.v('Beacon','object',obj=BEACON)
 complete=g.action('CompleteActivation',owner=BEACON).pin('Hostage','object',obj=HOSTAGE);g.w(beac,complete,'self');g.w(pawn,complete,'Hostage');g.chain(b,complete)
 for start,isabort in [(complete,False),(abort,True)]:
  prev=g.s(start,'bUsingBeacon',False,'bool',owner=HOSTAGE,target=pawn);prev=g.s(prev,'ActivationProgress',0,owner=HOSTAGE,target=pawn)
  clear=g.bbset(bb,'bActivateBeacon','Bool','false');g.chain(prev,clear)
  # Clear readiness before FinishAbort/FinishExecute; the director can retry once safe.
  finish=g.call(TASK,'FinishAbort' if isabort else 'FinishExecute')
  if not isabort:finish.pin('bSuccess','bool',default='true')
  g.chain(clear,finish)
 from generate_delivery_graphs import Graph
 Graph.write(g,'BTTask_ActivateBeacon')

def director():
 from generate_delivery_graphs import legacy_director as original
 g=capture(original)
 # Remove direct player activation completely, leaving E / RB solely for escort commands.
 switch=next(n for n in g.nodes if n.kind.endswith('K2Node_SwitchInteger'))
 for n in g.nodes:
  for p in n.pins.values():p['links']=[link for link in p['links'] if link[0]!=switch.name]
 switch.pins['execute']['links']=[]
 # The now unreachable old activation subgraph is stripped rather than retained as misleading source.
 start=next(i for i,n in enumerate(g.nodes) if n.kind.endswith('K2Node_VariableGet') and any('Baliza1' in p for p in n.props))
 end=next(i for i,n in enumerate(g.nodes) if n.kind.endswith('K2Node_Event') and any('ReceiveTick' in p for p in n.props))
 removed={n.name for n in g.nodes[start:end]}|{switch.name};g.nodes=[n for n in g.nodes if n.name not in removed]
 for n in g.nodes:
  for p in n.pins.values():p['links']=[link for link in p['links'] if link[0] not in removed]
 # New nodes must use fresh names after removal (Graph.node names by list length).
 for i,n in enumerate(g.nodes):pass
 # Move readiness to a second Tick execution branch, after the existing outcome checks.
 tick=next(n for n in g.nodes if n.kind.endswith('K2Node_Event') and any('ReceiveTick' in p for p in n.props))
 oldlinks=list(tick.pins['then']['links']);tick.pins['then']['links']=[]
 for name,pid in oldlinks:
  n=next(n for n in g.nodes if n.name==name);p=next(p for p in n.pins.values() if p['id']==pid);p['links'].remove((tick.name,tick.pins['then']['id']))
 # Fresh node allocation must avoid surviving generated IDs.
 original_node=g.node
 def unique(kind,props=(),**pos):
  n=original_node(kind,props,**pos)
  while sum(x.name==n.name for x in g.nodes)>1:n.name+='P'
  return n
 g.node=unique
 seq=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True).pin('then_1',out=True);g.chain(tick,seq)
 for name,pid in oldlinks:
  n=next(n for n in g.nodes if n.name==name);p=next(p for p in n.pins.values() if p['id']==pid);g.chain(seq,n,'then_0',p['name'])
 current=g.v('Paso','int');active=g.br(seq,g.cmp('Less_IntInt',current,3,'int'),'then_1');host=g.find(active,HOSTAGE);bb=g.blackboard(host,'ReturnValue')
 safe=g.neg(g.c(MATH,'BooleanOR',[('A','bool',(g.bbget(bb,'bMustFlee'),'ReturnValue')),('B','bool',(g.bbget(bb,'bEnemyNear'),'ReturnValue'))],cat='bool'))
 following=(g.bbget(bb,'bAccompanying'),'ReturnValue');ready=g.br(host,g.both(following,safe))
 sw=g.node('K2Node_SwitchInteger',['PinNames(0)="0"','PinNames(1)="1"','PinNames(2)="2"']).pin('execute').pin('Selection','int').pin('Default',out=True)
 for i in range(3):sw.pin(str(i),out=True)
 g.w(current,sw,'Selection');g.chain(ready,sw)
 for i in range(3):
  beacon=g.v('Baliza'+str(i+1),'object',obj=SM);cast=g.cast(BEACON);g.chain(sw,cast,str(i));g.w(beacon,cast,'Object');target=(cast,'AsBP_BeaconEntrega')
  zone=g.v('RequiredZone','object',owner=BEACON,obj=ZONE,target=target);clear=g.v('bCleared','bool',owner=ZONE,target=zone)
  distance=g.dist(host,'ReturnValue',cast,'AsBP_BeaconEntrega');near=g.cmp('LessEqual_DoubleDouble',(distance,'ReturnValue'),650)
  b=g.br(cast,g.both(clear,near));setactive=g.bbset(bb,'ActiveBeacon','Object');g.w(target,setactive,'ObjectValue');g.chain(b,setactive)
  approach=g.v('ApproachPoint','object',owner=BEACON,obj=ACTOR,target=target)
  settarget=g.bbset(bb,'BeaconTarget','Object');g.w(approach,settarget,'ObjectValue');g.chain(setactive,settarget);setready=g.bbset(bb,'bActivateBeacon','Bool','true');g.chain(settarget,setready)
 g.write('BP_DirectorEntrega')

def enemy_sense(charger=False):
 g=ProgressGraph();e=g.event('/Script/AIModule.BTService_BlueprintBase','ReceiveTickAI').pin('OwnerController','object',obj='/Script/AIModule.AIController',out=True).pin('ControlledPawn','object',obj='/Script/Engine.Pawn',out=True).pin('DeltaSeconds','real',sub='float',out=True)
 cast=g.cast(BASE);g.chain(e,cast);g.wire(e,'ControlledPawn',cast,'Object');pawn=(cast,'AsBP_BaseEnemy');p=g.player();player=(p,'ReturnValue');bb=g.blackboard(e,'OwnerController')
 prev=g.s(cast,'ChosenTarget',player,'object',obj=ACTOR);host=g.find(prev,HOSTAGE);h=(host,'ReturnValue');hbb=g.blackboard(host,'ReturnValue')
 hd=(g.dist(*pawn,*h),'ReturnValue');pd=(g.dist(*pawn,*player),'ReturnValue')
 alive=g.both((g.bbget(hbb,'bRescued'),'ReturnValue'),g.neg(g.v('bIsDead','bool',owner=HOSTAGE,target=h)))
 detected=g.both(g.cmp('LessEqual_DoubleDouble',hd,650),(g.sight(e,'OwnerController',host,'ReturnValue'),'ReturnValue'))
 retained=g.both((g.bbget(bb,'bHostageLocked'),'ReturnValue'),g.cmp('LessEqual_DoubleDouble',hd,1800))
 locked=g.both(alive,g.c(MATH,'BooleanOR',[('A','bool',detected),('B','bool',retained)],cat='bool'))
 setlock=g.bbset(bb,'bHostageLocked','Bool');g.w(locked,setlock,'BoolValue');g.chain(host,setlock)
 choose=g.br(setlock,(g.bbget(bb,'bHostageLocked'),'ReturnValue'))
 use=g.s(choose,'ChosenTarget',h,'object',obj=ACTOR)
 chosen=g.v('ChosenTarget','object',obj=ACTOR);target=g.s(use,'CombatTarget',chosen,'object',owner=BASE,target=pawn,obj=ACTOR);g.chain(choose,target,'else')
 distance=(g.dist(*pawn,*chosen),'ReturnValue');setdist=g.bbset(bb,'DistanceToTarget','Float');g.w(distance,setdist,'FloatValue');g.chain(target,setdist)
 enabled=g.br(setdist,g.cmp('LessEqual_DoubleDouble',distance,1800 if charger else 1500));setp=g.bbset(bb,'TargetActor','Object');g.w(chosen,setp,'ObjectValue');g.chain(enabled,setp);clear=g.bbset(bb,'TargetActor','Object');g.chain(enabled,clear,'else')
 if not charger:
  own=g.location(*pawn);goal=g.location(*chosen)
  delta=g.c(MATH,'Subtract_VectorVector',[('A','struct',(own,'ReturnValue')),('B','struct',(goal,'ReturnValue'))],cat='struct',obj=VEC)
  for pin in ['A','B']:delta[0].pins[pin]['obj']=VEC
  norm=g.c(MATH,'Normal',[('A','struct',delta),('Tolerance','real',.0001)],cat='struct',obj=VEC);norm[0].pins['A']['obj']=VEC
  rotate=g.c(MATH,'RotateAngleAxis',[('InVect','struct',norm),('AngleDeg','real',40),('Axis','struct','0,0,1')],cat='struct',obj=VEC)
  for pin in ['InVect','Axis']:rotate[0].pins[pin]['obj']=VEC
  band=g.both(g.cmp('GreaterEqual_DoubleDouble',distance,150),g.cmp('LessEqual_DoubleDouble',distance,210))
  direction=g.call(MATH,'SelectVector',pure=True,static=True).pin('A','struct',obj=VEC).pin('B','struct',obj=VEC).pin('bPickA','bool').pin('ReturnValue','struct',obj=VEC,out=True);g.w(rotate,direction,'A');g.w(norm,direction,'B');g.w(band,direction,'bPickA')
  radius=g.c(MATH,'Multiply_VectorFloat',[('A','struct',(direction,'ReturnValue')),('B','real',180)],cat='struct',obj=VEC);radius[0].pins['A']['obj']=VEC
  point=g.c(MATH,'Add_VectorVector',[('A','struct',(goal,'ReturnValue')),('B','struct',radius)],cat='struct',obj=VEC)
  for pin in ['A','B']:point[0].pins[pin]['obj']=VEC
  orbit=g.bbset(bb,'OrbitLocation','Vector');g.w(point,orbit,'VectorValue');g.chain(setp,orbit)
 g.write('BTService_ChargerSense' if charger else 'BTService_LocatePlayer')

def enemy_actions():
 from generate_combat_graphs import attack_task,windup,charge,controller
 from generate_ai_refinement import retreat
 controller();attack_task();charge();retreat();g=capture(windup)
 goal=next(n for n in g.nodes if any('SetValueAsVector' in p for p in n.props))
 links=list(goal.pins['then']['links']);goal.pins['then']['links']=[]
 for name,pid in links:
  n=next(n for n in g.nodes if n.name==name);p=next(p for p in n.pins.values() if p['id']==pid);p['links'].remove((goal.name,goal.pins['then']['id']))
 prev=g.s(goal,'ChargeVictim',g.v('CombatTarget','object',owner=BASE,obj=ACTOR,target=g.v('CachedPawn','object',obj=BASE)),'object',owner=BASE,target=g.v('CachedPawn','object',obj=BASE),obj=ACTOR)
 for name,pid in links:
  n=next(n for n in g.nodes if n.name==name);p=next(p for p in n.pins.values() if p['id']==pid);g.chain(prev,n,nextpin=p['name'])
 CombatGraph.write(g,'BTTask_ChargerWindup')

def combat_zone():
 import generate_wave_graphs as waves
 old=waves.gate;waves.gate=lambda g,prev,*args,**kwargs:prev
 try:waves.zone()
 finally:waves.gate=old

if __name__=='__main__':door();fragment();player();beacon();hostage();activate_task();director();enemy_sense();enemy_sense(True);enemy_actions();combat_zone()
