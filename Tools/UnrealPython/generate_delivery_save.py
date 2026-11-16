"""Author Blueprint checkpoint graphs; all runtime behavior stays in Blueprints."""
from generate_progression_graphs import ProgressGraph, ACTOR, OBJECT, MATH, GS, HERO, HOSTAGE, DOOR, BEACON, ZONE, DIRECTOR, SMC, PRIM, SM
from generate_delivery_graphs import HEALTH, q, ref
from delivery_save_schema import SAVE, MANAGER, GI, SLOT, VERSION, ROT, VEC

class SaveGraph(ProgressGraph):
    def node(self, kind, props=(), **pos):
        n = super().node(kind, props, **pos)
        n.name = 'SV_' + n.name
        return n

    def action_on(self, prev, owner, name, target=None, inputs=(), pin='then'):
        n = self.action(name, owner=owner) if owner.startswith('/Game/') else self.call(owner, name)
        for p, kind, value, obj in inputs:
            n.pin(p, kind, obj=obj, sub='double' if kind == 'real' else '')
            self.w(value, n, p)
        if target:
            self.w(target, n, 'self')
        self.chain(prev, n, pin)
        if owner == MANAGER:
            self.__dict__.setdefault('local_calls', []).append((n, name))
        return n

    def local(self, name, cls):
        return self.v(name, 'object', obj=cls)

    def slot(self, name, pure=False):
        n = self.call(GS, name, static=True, pure=pure)
        n.pin('SlotName', 'string', default=SLOT).pin('UserIndex', 'int', default='0')
        return n

def manager():
    g = SaveGraph()
    hero = g.local('Hero', HERO)
    host = g.local('Hostage', HOSTAGE)
    director = g.local('Director', DIRECTOR)
    instance = g.local('Instance', GI)
    data = g.local('SaveData', SAVE)
    pc = g.c(GS, 'GetPlayerController', [('PlayerIndex', 'int', 0)], cat='object', obj='/Script/Engine.PlayerController')
    health = g.v('BPC_Health', 'object', owner=HERO, target=hero, obj=HEALTH)
    bb = g.blackboard(*host)
    zones = [g.v('Zona'+str(i), 'object', owner=DIRECTOR, target=director, obj=ZONE) for i in (1,2)]
    beacons = [g.local('Beacon'+str(i), BEACON) for i in (1,2,3)]
    doors = [g.v('Door', 'object', owner=BEACON, target=b, obj=DOOR) for b in beacons]
    live = lambda name, kind='real', obj=HERO, target=hero: g.v(name, kind, owner=obj, target=target)
    saved = lambda name, kind='real', obj=None: g.v(name, kind, owner=SAVE, target=data, obj=obj)
    bindings = [
        ('OrderCode', 'int', DIRECTOR, director, 'OrderCode'),
        ('MissionElapsed', 'real', DIRECTOR, director, 'MissionElapsed'),
        ('Paso', 'int', DIRECTOR, director, 'Paso'),
        ('PlayerHealth', 'real', HEALTH, health, 'Health'),
        ('HammerUpgraded', 'bool', HERO, hero, 'bHammerUpgraded'),
        ('HammerEquipped', 'bool', HERO, hero, 'bIsHammerEquipped'),
        ('HostageHealth', 'real', HOSTAGE, host, 'Health'),
    ]
    for i, z in enumerate(zones,1):
        for key, kind, prop in [('Cleared','bool','bCleared'),('Wave','int','CurrentWave'),('Phase','int','Phase'),('Spawned','int','SpawnedCount')]:
            bindings.append(('Zone%d%s'%(i,key),kind,ZONE,z,prop))
    for i,(b,d) in enumerate(zip(beacons,doors),1):
        bindings.append(('Beacon%dActivated'%i,'bool',BEACON,b,'bActivated'))
        for key,kind,prop in [('Health','real','Health'),('Unlocked','bool','bUnlocked'),('Destroyed','bool','bDestroyed'),('Cracked','bool','bCracked')]:
            bindings.append(('Door%d%s'%(i,key),kind,DOOR,d,prop))

    # Initialization happens on the first world Tick, after all BeginPlay events.
    tick = g.event(ACTOR,'ReceiveTick').pin('DeltaSeconds','real',sub='float',out=True)
    initialized = g.br(tick, g.v('bInitialized','bool'))
    init = g.custom('InitializeCheckpoint')
    g.action_on(initialized,MANAGER,'InitializeCheckpoint',pin='else')
    f = g.find(init,HERO); c = g.cast(HERO); g.chain(f,c); g.wire(f,'ReturnValue',c,'Object')
    prev = g.s(c,'Hero',(c,'AsBP_PlayerEntrega'),'object',obj=HERO)
    for name,cls in [('Hostage',HOSTAGE),('Director',DIRECTOR)]:
        f = g.find(prev,cls); c=g.cast(cls); g.chain(f,c); g.wire(f,'ReturnValue',c,'Object')
        prev=g.s(c,name,(c,'As'+cls.rsplit('.',1)[-1].removesuffix('_C')),'object',obj=cls)
    gi=g.c(GS,'GetGameInstance',cat='object',obj='/Script/Engine.GameInstance')
    c=g.cast(GI);g.chain(prev,c);g.w(gi,c,'Object');prev=g.s(c,'Instance',(c,'AsBP_GameInstance'),'object',obj=GI)
    for i in (1,2,3):
        b=g.v('Baliza'+str(i),'object',owner=DIRECTOR,target=director,obj=SM)
        c=g.cast(BEACON);g.chain(prev,c);g.w(b,c,'Object');prev=g.s(c,'Beacon'+str(i),(c,'AsBP_BeaconEntrega'),'object',obj=BEACON)
    prev=g.s(prev,'bInitialized',True,'bool')
    enable=g.call(ACTOR,'EnableInput').pin('PlayerController','object',obj='/Script/Engine.PlayerController');g.w(pc,enable,'PlayerController');g.chain(prev,enable)
    resume=g.br(enable,live('bDeliveryContinue','bool',GI,instance))
    clear=g.s(resume,'bDeliveryContinue',False,'bool',owner=GI,target=instance)
    g.action_on(clear,MANAGER,'RestoreCheckpoint')
    g.action_on(resume,MANAGER,'SaveCheckpoint',pin='else')

    # Checkpoint writes are forbidden during either wave/intermission or transient actions.
    def safe():
        good=g.cmp('Less_IntInt',live('Paso','int',DIRECTOR,director),4,'int')
        for value in [live('Health','real',HEALTH,health),live('Health','real',HOSTAGE,host)]:
            good=g.both(good,g.cmp('Greater_DoubleDouble',value,0))
        for z in zones:
            phase=live('Phase','int',ZONE,z)
            idle=g.cmp('EqualEqual_IntInt',phase,0,'int');done=g.cmp('EqualEqual_IntInt',phase,3,'int')
            good=g.both(good,g.c(MATH,'BooleanOR',[('A','bool',idle),('B','bool',done)],cat='bool'))
        for value in [live('IsAttacking','bool'),live('bUsingBeacon','bool',HOSTAGE,host),(g.bbget(bb,'bMustFlee'),'ReturnValue'),(g.bbget(bb,'bEnemyNear'),'ReturnValue')]:
            good=g.both(good,g.neg(value))
        movement=g.v('CharacterMovement','object',owner='/Script/Engine.Character',target=hero,obj='/Script/Engine.CharacterMovementComponent',native=True)
        ground=g.call('/Script/Engine.CharacterMovementComponent','IsMovingOnGround',pure=True).pin('ReturnValue','bool',out=True);g.w(movement,ground,'self')
        return g.both(good,(ground,'ReturnValue'))

    # A changed milestone is retried each Tick until it is safe, without timed polling.
    changed=g.neg(g.v('bHasCheckpoint','bool'))
    tracked=[b for b in bindings if b[0]=='Paso' or 'Cleared' in b[0] or ('Door' in b[0] and 'Health' in b[0])]
    for name,kind,owner,target,prop in tracked:
        fn={'bool':'NotEqual_BoolBool','int':'NotEqual_IntInt','real':'NotEqual_DoubleDouble'}[kind]
        diff=g.cmp(fn,live(prop,kind,owner,target),saved(name,kind),kind)
        changed=g.c(MATH,'BooleanOR',[('A','bool',changed),('B','bool',diff)],cat='bool')
    diff=g.cmp('NotEqual_BoolBool',(g.bbget(bb,'bRescued'),'ReturnValue'),saved('Rescued','bool'),'bool')
    changed=g.c(MATH,'BooleanOR',[('A','bool',changed),('B','bool',diff)],cat='bool')
    # Avoid dereferencing a missing SaveData object on the first checkpoint.
    has=g.br(initialized,g.v('bHasCheckpoint','bool'))
    change=g.br(has,changed);g.action_on(change,MANAGER,'SaveCheckpoint')
    g.action_on(has,MANAGER,'SaveCheckpoint',pin='else')
    key=g.key('F5');g.action_on(key,MANAGER,'SaveCheckpoint',pin='Pressed')

    event=g.custom('SaveCheckpoint');clear_success=g.s(event,'bSaveSucceeded',False,'bool');gate=g.br(clear_success,safe())
    g.s(gate,'StatusText','Guardado pendiente: espera a estar a salvo.','string',pin='else')
    make=g.call(GS,'CreateSaveGameObject',static=True).pin('SaveGameClass','class',obj='/Script/Engine.SaveGame',default_obj=SAVE).pin('ReturnValue','object',obj='/Script/Engine.SaveGame',out=True);g.chain(gate,make)
    cast=g.cast(SAVE);g.chain(make,cast);g.wire(make,'ReturnValue',cast,'Object')
    prev=g.s(cast,'SaveData',(cast,'AsBP_DeliverySave'),'object',obj=SAVE)
    prev=g.s(prev,'Version',VERSION,'int',owner=SAVE,target=data)
    for name,kind,owner,target,prop in bindings:
        prev=g.s(prev,name,live(prop,kind,owner,target),kind,owner=SAVE,target=data)
    for label,target in [('Player',hero),('Hostage',host)]:
        prev=g.s(prev,label+'Location',(g.location(*target),'ReturnValue'),'struct',owner=SAVE,target=data,obj=VEC)
        rot=g.call(ACTOR,'K2_GetActorRotation',pure=True).pin('ReturnValue','struct',obj=ROT,out=True);g.w(target,rot,'self')
        prev=g.s(prev,label+'Rotation',(rot,'ReturnValue'),'struct',owner=SAVE,target=data,obj=ROT)
    rot=g.call('/Script/Engine.Controller','GetControlRotation',pure=True).pin('ReturnValue','struct',obj=ROT,out=True);g.w(pc,rot,'self')
    prev=g.s(prev,'ControlRotation',(rot,'ReturnValue'),'struct',owner=SAVE,target=data,obj=ROT)
    for field,keyname in [('Rescued','bRescued'),('Accompanying','bAccompanying'),('Waiting','bWaiting')]:
        prev=g.s(prev,field,(g.bbget(bb,keyname),'ReturnValue'),'bool',owner=SAVE,target=data)
    write=g.slot('SaveGameToSlot').pin('SaveGameObject','object',obj='/Script/Engine.SaveGame').pin('ReturnValue','bool',out=True);g.w(data,write,'SaveGameObject');g.chain(prev,write)
    prev=g.s(write,'bSaveSucceeded',(write,'ReturnValue'),'bool')
    prev=g.s(prev,'bHasCheckpoint',(write,'ReturnValue'),'bool');ok=g.br(prev,g.v('bSaveSucceeded','bool'))
    prev=g.s(ok,'bHasCheckpoint',True,'bool');g.s(prev,'StatusText','Punto de control guardado. F5 guarda cuando estes a salvo.','string')
    g.s(ok,'StatusText','No se pudo guardar la partida. Intenta F5 de nuevo.','string',pin='else')

    # Load is gated by schema and health before any live-world values are changed.
    event=g.custom('RestoreCheckpoint');load=g.slot('LoadGameFromSlot').pin('ReturnValue','object',obj='/Script/Engine.SaveGame',out=True);g.chain(event,load)
    cast=g.cast(SAVE);g.chain(load,cast);g.wire(load,'ReturnValue',cast,'Object')
    g.action_on(cast,MANAGER,'SaveCheckpoint',pin='CastFailed')
    prev=g.s(cast,'SaveData',(cast,'AsBP_DeliverySave'),'object',obj=SAVE)
    valid=g.cmp('EqualEqual_IntInt',saved('Version','int'),VERSION,'int')
    for field in ['PlayerHealth','HostageHealth']:valid=g.both(valid,g.cmp('Greater_DoubleDouble',saved(field),0))
    valid=g.both(valid,g.cmp('Less_IntInt',saved('Paso','int'),4,'int'))
    valid=g.both(valid,g.both(g.cmp('GreaterEqual_IntInt',saved('OrderCode','int'),0,'int'),g.cmp('Less_IntInt',saved('OrderCode','int'),6,'int')))
    checked=g.br(prev,valid);g.s(checked,'StatusText','Guardado incompatible. Inicia una partida nueva.','string',pin='else')
    prev=checked
    for name,kind,owner,target,prop in bindings:
        prev=g.s(prev,prop,saved(name,kind),kind,owner=owner,target=target)
    prev=g.s(prev,'LastBeaconOrder',saved('OrderCode','int'),'int',owner=GI,target=instance)
    for label,target in [('Player',hero),('Hostage',host)]:
        n=g.call(ACTOR,'K2_SetActorLocationAndRotation').pin('NewLocation','struct',obj=VEC).pin('NewRotation','struct',obj=ROT).pin('bSweep','bool',default='false').pin('SweepHitResult','struct',obj='/Script/Engine.HitResult',out=True).pin('bTeleport','bool',default='true').pin('ReturnValue','bool',out=True)
        g.w(target,n,'self');g.w(saved(label+'Location','struct',VEC),n,'NewLocation');g.w(saved(label+'Rotation','struct',ROT),n,'NewRotation');g.chain(prev,n);prev=n
    prev=g.action_on(prev,'/Script/Engine.Controller','SetControlRotation',pc,[('NewRotation','struct',saved('ControlRotation','struct',ROT),ROT)])
    # Refresh the existing health widget through its original multicast path.
    prev=g.action_on(prev,HEALTH,'Increase_Health',health,[('Amount','real',0,None)])
    for field,keyname in [('Rescued','bRescued'),('Accompanying','bAccompanying'),('Waiting','bWaiting')]:
        n=g.bbset(bb,keyname,'Bool');g.w(saved(field,'bool'),n,'BoolValue');g.chain(prev,n);prev=n
    for keyname in ['bMustFlee','bEnemyNear','bActivateBeacon']:
        n=g.bbset(bb,keyname,'Bool','false');g.chain(prev,n);prev=n
    # Weapon flags and visibility are restored; the existing player Tick aligns its hitbox.
    prev=g.s(prev,'bIsSwordEquipped',g.neg(saved('HammerEquipped','bool')),'bool',owner=HERO,target=hero)
    for field,visible,cls in [('hammer',saved('HammerEquipped','bool'),'/Script/Engine.SkeletalMeshComponent'),('Weapon',g.neg(saved('HammerEquipped','bool')),SMC)]:
        component=g.v(field,'object',owner=HERO,target=hero,obj=cls)
        prev=g.action_on(prev,'/Script/Engine.SceneComponent','SetVisibility',component,[('bNewVisibility','bool',visible,None),('bPropagateToChildren','bool',True,None)])
    pending=None;required=None
    for i,(b,d) in enumerate(zip(beacons,doors),1):
        activated=saved('Beacon%dActivated'%i,'bool');destroyed=saved('Door%dDestroyed'%i,'bool')
        # Visuals are reapplied without executing activation rewards or spawning shards.
        for target,value in []:  # Beacon Tick refreshes its light; preserve all three material regions.
            comp=g.v('StaticMeshComponent','object',owner=SM,target=target,obj=SMC,native=True)
            branch=g.br(prev,value)
            a=g.call(PRIM,'SetMaterial').pin('ElementIndex','int',default='0').pin('Material','object',obj='/Script/Engine.MaterialInterface',default_obj='/Game/ThirdPerson/Environment/EscenarioIan/M_Baliza_Activa.M_Baliza_Activa');g.w(comp,a,'self');g.chain(branch,a)
            # The initial inactive material is already correct on a fresh map.
            prev=g.s(a,'bRestoring',True,'bool');g.chain(branch,prev,'else')
        mesh=g.v('StaticMeshComponent','object',owner=SM,target=d,obj=SMC,native=True)
        cracked=g.br(prev,saved('Door%dCracked'%i,'bool'))
        setmesh=g.call(SMC,'SetStaticMesh').pin('NewMesh','object',obj='/Script/Engine.StaticMesh').pin('ReturnValue','bool',out=True);g.w(mesh,setmesh,'self');g.w(g.v('CrackedMesh','object',owner=DOOR,target=d,obj='/Script/Engine.StaticMesh'),setmesh,'NewMesh');g.chain(cracked,setmesh)
        prev=g.s(setmesh,'bRestoring',True,'bool');g.chain(cracked,prev,'else')
        # Collision changes update the existing dynamic NavMesh just as real destruction does.
        prev=g.action_on(prev,ACTOR,'SetActorHiddenInGame',d,[('bNewHidden','bool',destroyed,None)])
        prev=g.action_on(prev,ACTOR,'SetActorEnableCollision',d,[('bNewActorEnableCollision','bool',g.neg(destroyed),None)])
        unlocked=saved('Door%dUnlocked'%i,'bool');need=g.both(unlocked,g.neg(destroyed))
        powered=g.br(prev,unlocked)
        mat=g.call(PRIM,'SetMaterial').pin('ElementIndex','int',default='2').pin('Material','object',obj='/Script/Engine.MaterialInterface',default_obj='/Game/ThirdPerson/Environment/Progression/M_DoorPowered.M_DoorPowered')
        g.w(mesh,mat,'self');g.chain(powered,mat)
        prev=g.s(mat,'bRestoring',True,'bool');g.chain(powered,prev,'else')
        pending=need if pending is None else g.c(MATH,'BooleanOR',[('A','bool',pending),('B','bool',need)],cat='bool')
        branch=g.br(prev,need);setdoor=g.s(branch,'RequiredDoor',d,'object',owner=HERO,target=hero,obj=DOOR)
        prev=g.s(setdoor,'bRestoring',True,'bool');g.chain(branch,prev,'else')
    prev=g.s(prev,'bDoorPending',pending,'bool',owner=HERO,target=hero)
    prev=g.s(prev,'bRestoring',False,'bool');prev=g.s(prev,'bHasCheckpoint',True,'bool')
    g.s(prev,'StatusText','Partida restaurada. F5 guarda cuando estes a salvo.','string')
    # Importing a new custom event and its call in one clipboard pass can drop
    # the call before the event signature exists. Share the action's exec entry
    # directly; keep the named events available for diagnostics and F5.
    for call, name in g.local_calls:
        event=next(n for n in g.nodes if 'CustomFunctionName='+q(name) in n.props)
        for source_name,source_id in list(call.pins['execute']['links']):
            source=next(n for n in g.nodes if n.name==source_name)
            source_pin=next(p for p in source.pins.values() if p['id']==source_id)
            source_pin['links'].remove((call.name,call.pins['execute']['id']))
            for target_name,target_id in event.pins['then']['links']:
                target=next(n for n in g.nodes if n.name==target_name)
                target_pin=next(p for p in target.pins.values() if p['id']==target_id)
                g.wire(source,source_pin['name'],target,target_pin['name'])
        for node in g.nodes:
            for pin in node.pins.values():
                pin['links']=[link for link in pin['links'] if link[0]!=call.name]
        g.nodes.remove(call)
    g.write('BP_DeliverySaveManager')

def menu():
    g=SaveGraph();WIDGET='/Script/UMG.UserWidget';BUTTON='/Script/UMG.Button'
    gi=g.c(GS,'GetGameInstance',cat='object',obj='/Script/Engine.GameInstance')
    def clicked(field,index):
        return g.node('K2Node_ComponentBoundEvent',[
            'DelegatePropertyName="OnClicked"','DelegateOwnerClass='+ref(BUTTON),
            'ComponentPropertyName='+q(field),
            'EventReference=(MemberParent="/Script/CoreUObject.Package\'/Script/UMG\'",MemberName="OnButtonClickedEvent__DelegateSignature")',
            'bInternalEvent=True','CustomFunctionName='+q('BndEvt__Menu_Inicio_'+field+'_K2Node_ComponentBoundEvent_'+str(index)+'_OnButtonClickedEvent__DelegateSignature')
        ]).pin('then',out=True)
    button=g.v('btn_continuar_menu','object',obj=BUTTON)
    construct=g.event(WIDGET,'Construct')
    disabled=g.action_on(construct,'/Script/UMG.Widget','SetIsEnabled',button,[('bInIsEnabled','bool',False,None)])
    exists=g.slot('DoesSaveGameExist').pin('ReturnValue','bool',out=True)
    g.chain(disabled,exists)
    test=g.br(exists,(exists,'ReturnValue'))
    load=g.slot('LoadGameFromSlot').pin('ReturnValue','object',obj='/Script/Engine.SaveGame',out=True);g.chain(test,load)
    cast=g.cast(SAVE);g.chain(load,cast);g.wire(load,'ReturnValue',cast,'Object');data=(cast,'AsBP_DeliverySave')
    valid=g.cmp('EqualEqual_IntInt',g.v('Version','int',owner=SAVE,target=data),VERSION,'int')
    for field in ['PlayerHealth','HostageHealth']:valid=g.both(valid,g.cmp('Greater_DoubleDouble',g.v(field,owner=SAVE,target=data),0))
    valid=g.both(valid,g.cmp('Less_IntInt',g.v('Paso','int',owner=SAVE,target=data),4,'int'))
    code=g.v('OrderCode','int',owner=SAVE,target=data)
    valid=g.both(valid,g.both(g.cmp('GreaterEqual_IntInt',code,0,'int'),g.cmp('Less_IntInt',code,6,'int')))
    g.action_on(cast,'/Script/UMG.Widget','SetIsEnabled',button,[('bInIsEnabled','bool',valid,None)])
    for field,index,resume in [('btn_nuevojuego_menu',0,False),('btn_continuar_menu',3,True)]:
        e=clicked(field,index);cast=g.cast(GI);g.chain(e,cast);g.w(gi,cast,'Object')
        prev=g.s(cast,'bDeliveryContinue',resume,'bool',owner=GI,target=(cast,'AsBP_GameInstance'))
        level=g.call(GS,'OpenLevel',static=True).pin('LevelName','name',default='/Game/ThirdPerson/Maps/Nivel_Entrega').pin('bAbsolute','bool',default='true').pin('Options','string');g.chain(prev,level)
    e=clicked('btn_salir_menu',1)
    quit=g.call('/Script/Engine.KismetSystemLibrary','QuitGame',static=True).pin('SpecificPlayer','object',obj='/Script/Engine.PlayerController').pin('QuitPreference','byte',obj='/Script/Engine.EQuitPreference',default='Quit').pin('bIgnorePlatformRestrictions','bool',default='false');g.chain(e,quit)
    e=clicked('btn_opciones_menu',2)
    remove=g.call(WIDGET,'RemoveFromParent');g.chain(e,remove)
    create=g.node('K2Node_CreateWidget').pin('execute').pin('then',out=True).pin('Class','class',obj=WIDGET,default_obj='/Game/Menu/Menu_Opciones.Menu_Opciones_C').pin('OwningPlayer','object',obj='/Script/Engine.PlayerController').pin('ReturnValue','object',obj='/Game/Menu/Menu_Opciones.Menu_Opciones_C',out=True)
    g.chain(remove,create);g.action_on(create,WIDGET,'AddToViewport',(create,'ReturnValue'),[('ZOrder','int',0,None)])
    g.write('Menu_Inicio')

if __name__=='__main__':
    from generate_progression_graphs import director
    director()
    manager()
    menu()
