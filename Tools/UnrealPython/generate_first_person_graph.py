"""Presentación de brazos/armas sin notifies duplicados ni colisión adicional."""
from generate_delivery_controls import split_exec
from generate_progression_graphs import ACTOR, HERO, VEC, MATH, GS, PRIM, SCENE
SK='/Script/Engine.SkeletalMeshComponent';SM='/Script/Engine.StaticMeshComponent'
ROT='/Script/CoreUObject.Rotator'

def add_first_person(g):
    arms=g.v('BrazosFP','object',obj=SK);sword=g.v('EspadaFP','object',obj=SM);hammer=g.v('MartilloFP','object',obj=SK)
    body=g.v('Mesh','object',obj=SK);cam=g.v('FPC','object',obj='/Script/Engine.CameraComponent')
    def attach(prev,component,parent,socket='None',pin='then'):
        n=g.call(SCENE,'K2_AttachToComponent').pin('Parent','object',obj=SCENE).pin('SocketName','name',default=socket).pin('bWeldSimulatedBodies','bool',default='false').pin('ReturnValue','bool',out=True)
        for p in ['LocationRule','RotationRule','ScaleRule']:n.pin(p,'byte',obj='/Script/Engine.EAttachmentRule',default='SnapToTarget')
        g.w(component,n,'self');g.w(parent,n,'Parent');g.chain(prev,n,pin);return n
    def transform(prev,component,location,rotation='0,0,0'):
        n=g.call(SCENE,'K2_SetRelativeLocationAndRotation').pin('NewLocation','struct',obj=VEC).pin('NewRotation','struct',obj=ROT).pin('bSweep','bool',default='false').pin('SweepHitResult','struct',obj='/Script/Engine.HitResult',out=True).pin('bTeleport','bool',default='true')
        g.w(component,n,'self');g.w(location,n,'NewLocation');g.w(rotation,n,'NewRotation');g.chain(prev,n);return n
    begin=next(n for n in g.nodes if any('MemberName="ReceiveBeginPlay"' in p for p in n.props))
    seq=split_exec(g,begin)
    prev=attach(seq,arms,cam,pin='then_1')
    # Rig en centímetros y mirando +X; origen visual bajo los ojos.
    prev=transform(prev,arms,'34,0,-108','0,-90,0')
    prev=g.action_on(prev,'/Script/Engine.SkinnedMeshComponent','SetLeaderPoseComponent',arms,[('NewLeaderBoneComponent','object',None,'/Script/Engine.SkinnedMeshComponent'),('bForceUpdate','bool',True,None),('bInFollowerShouldTickPose','bool',True,None)])
    prev=g.action_on(prev,SK,'SetAnimationMode',arms,[('InAnimationMode','byte','AnimationSingleNode','/Script/Engine.EAnimationMode'),('bForceInitAnimScriptInstance','bool',True,None)])
    prev=g.s(prev,'GlobalAnimRateScale',0,owner=SK,target=arms)
    prev=g.action_on(prev,SK,'HideBoneByName',arms,[('BoneName','name','clavicle_l',None),('PhysBodyOption','byte','PBO_None','/Script/Engine.EPhysBodyOp')])
    prev=attach(prev,sword,arms,'WeaponSocket')
    prev=g.action_on(prev,SCENE,'SetRelativeScale3D',sword,[('NewScale3D','struct','.5,.5,.5',VEC)])
    # El pivote de longsword está lejos de la empuñadura. Este ajuste sitúa
    # su mango en middle_02_r, sin reutilizar el offset de tercera persona.
    prev=transform(prev,sword,'129.535,-16.613,-29.542','0,0,60')
    prev=attach(prev,hammer,arms,'hand_r')
    prev=g.action_on(prev,SCENE,'SetRelativeScale3D',hammer,[('NewScale3D','struct','.55,.55,.55',VEC)])
    # El socket de martillo era específico de la malla de tercera persona.
    prev=transform(prev,hammer,'0,0,-20','0,0,0')
    light=g.v('LuzFP','object',obj='/Script/Engine.PointLightComponent')
    prev=attach(prev,light,cam);prev=transform(prev,light,'8,-12,10')
    tick=next(n for n in g.nodes if any('MemberName="ReceiveTick"' in p for p in n.props));seq=split_exec(g,tick)
    fp=g.v('CamaraPrimera','bool')
    # La visibilidad se sincroniza también al cargar un checkpoint o al salir de
    # una cinemática; no depende de haber pulsado C en esta sesión.
    hero=(g.selfnode(typ=HERO),'self')
    hidden=g.v('bHidden','bool',owner=ACTOR,target=hero,native=True)
    show=g.both(fp,g.neg(hidden))
    prev=g.action_on(seq,SCENE,'SetVisibility',arms,[('bNewVisibility','bool',show,None),('bPropagateToChildren','bool',False,None)],pin='then_1')
    prev=g.action_on(prev,SCENE,'SetVisibility',light,[('bNewVisibility','bool',show,None),('bPropagateToChildren','bool',False,None)])
    for component,value in [(sword,g.both(show,g.v('bIsSwordEquipped','bool'))),(hammer,g.both(show,g.v('bIsHammerEquipped','bool')))]:
        prev=g.action_on(prev,SCENE,'SetVisibility',component,[('bNewVisibility','bool',value,None),('bPropagateToChildren','bool',False,None)])
    for component in [g.v('Weapon','object',obj=SM),g.v('hammer','object',obj=SK)]:
        prev=g.action_on(prev,PRIM,'SetOwnerNoSee',component,[('bNewOwnerNoSee','bool',fp,None)])
    # Oscilación discreta por velocidad; el movimiento de cámara no sigue la
    # cabeza del montaje para que los giros de ataques no mareen al jugador.
    active=g.br(prev,fp)
    time=g.op('Add_DoubleDouble',g.v('FPBobTime'),(tick,'DeltaSeconds'))
    prev=g.s(active,'FPBobTime',time)
    # Vista propia: reposo preparado y muestreo sincronizado del ataque real.
    # Las copias carecen de notifies, no avanzan solas y SetPosition no los dispara.
    import json
    from pathlib import Path
    rows=json.loads((Path(__file__).resolve().parents[2]/'Tools/ArtSource/FirstPerson/animation_manifest.json').read_text())
    ANIMSEQ='/Script/Engine.AnimSequence';ANIMASSET='/Script/Engine.AnimationAsset'
    def asset_pick(condition,a,b):
        index=g.c(MATH,'SelectInt',[('A','int',1),('B','int',0),('bPickA','bool',condition)],cat='int')
        n=g.node('K2Node_Select',['NumOptionPins=2','IndexPinType=(PinCategory="int")']).pin('Index','int').pin('ReturnValue','object',obj=ANIMSEQ,out=True)
        g.w(index,n,'Index')
        for i,value in enumerate([b,a]):
            n.pin('Option '+str(i),'object',obj=ANIMSEQ)
            if isinstance(value,str):n.pins['Option '+str(i)]['default_obj']=value
            else:g.w(value,n,'Option '+str(i))
        return n,'ReturnValue'
    current=g.c('/Script/Engine.Character','GetCurrentMontage',cat='object',obj='/Script/Engine.AnimMontage',static=False)
    anim=g.c(SK,'GetAnimInstance',cat='object',obj='/Script/Engine.AnimInstance',static=False);g.w(body,anim[0],'self')
    pos=g.c('/Script/Engine.AnimInstance','Montage_GetPosition',[('Montage','object',current)],static=False)
    pos[0].pins['Montage']['obj']='/Script/Engine.AnimMontage';g.w(anim,pos[0],'self')
    idle_sword=next(r['sequence'] for r in rows if r['montage'].endswith('/FA_1_Montage.FA_1_Montage'))
    idle_hammer=next(r['sequence'] for r in rows if r['montage'].endswith('/HA_1_Montage.HA_1_Montage'))
    selected=asset_pick(g.v('bIsHammerEquipped','bool'),idle_hammer,idle_sword)
    for row in rows:
        same=g.call(MATH,'EqualEqual_ObjectObject',pure=True,static=True).pin('A','object',obj='/Script/CoreUObject.Object').pin('B','object',obj='/Script/CoreUObject.Object',default_obj=row['montage']).pin('ReturnValue','bool',out=True)
        g.w(current,same,'A');selected=asset_pick((same,'ReturnValue'),row['sequence'],selected)
    changed=g.br(prev,g.cmp('NotEqual_ObjectObject',selected,g.v('LastFPAnimation','object',obj=ANIMSEQ),'object'))
    prev=g.action_on(changed,SK,'SetAnimation',arms,[('NewAnimToPlay','object',selected,ANIMASSET)])
    prev=g.s(prev,'LastFPAnimation',selected,'object',obj=ANIMSEQ)
    held=g.c(MATH,'SelectFloat',[('A','real',g.v('FPIdleHammerPosition')),('B','real',g.v('FPIdleSwordPosition')),('bPickA','bool',g.v('bIsHammerEquipped','bool'))])
    position=g.c(MATH,'SelectFloat',[('A','real',pos),('B','real',held),('bPickA','bool',(g.valid(*current),'ReturnValue'))])
    sample=g.action_on(prev,SK,'SetPosition',arms,[('InPos','real',position,None),('bFireNotifies','bool',False,None)])
    g.chain(changed,sample,'else');prev=sample
    velocity=g.c(ACTOR,'GetVelocity',cat='struct',obj=VEC,static=False)
    speed=g.c(MATH,'VSizeXY',[('A','struct',velocity)]);speed[0].pins['A']['obj']=VEC
    weight=g.c(MATH,'FClamp',[('Value','real',g.op('Divide_DoubleDouble',speed,500)),('Min','real',0),('Max','real',1)])
    phase=g.op('Multiply_DoubleDouble',g.v('FPBobTime'),9)
    wave=g.c(MATH,'Sin',[('A','real',phase)])
    hand=g.c(SCENE,'GetSocketTransform',[('InSocketName','name','hand_r'),('TransformSpace','byte','RTS_Component')],cat='struct',obj='/Script/CoreUObject.Transform',static=False)
    hand[0].pins['TransformSpace']['obj']='/Script/Engine.ERelativeTransformSpace';g.w(arms,hand[0],'self')
    split=g.call(MATH,'BreakTransform',pure=True,static=True).pin('InTransform','struct',obj='/Script/CoreUObject.Transform').pin('Location','struct',obj=VEC,out=True)
    g.w(hand,split,'InTransform')
    xyz=g.call(MATH,'BreakVector',pure=True,static=True).pin('InVec','struct',obj=VEC)
    for p in ['X','Y','Z']:xyz.pin(p,'real',sub='double',out=True)
    g.w((split,'Location'),xyz,'InVec')
    roll=g.c(MATH,'SelectFloat',[('A','real',0),('B','real',g.v('FPRollSword')),('bPickA','bool',g.v('bIsHammerEquipped','bool'))])
    camera_roll=g.c(MATH,'MakeRotator',[('Roll','real',roll),('Pitch','real',0),('Yaw','real',0)],cat='struct',obj=ROT)
    rotation=g.c(MATH,'ComposeRotators',[('A','struct','0,-90,0'),('B','struct',camera_roll)],cat='struct',obj=ROT)
    for p in ['A','B']:rotation[0].pins[p]['obj']=ROT
    basis=g.c(MATH,'MakeTransform',[('Location','struct','0,0,0'),('Rotation','struct',rotation),('Scale','struct','1,1,1')],cat='struct',obj='/Script/CoreUObject.Transform')
    basis[0].pins['Location']['obj']=VEC;basis[0].pins['Rotation']['obj']=ROT;basis[0].pins['Scale']['obj']=VEC
    rotated=g.c(MATH,'TransformLocation',[('T','struct',basis),('Location','struct',(split,'Location'))],cat='struct',obj=VEC)
    rotated[0].pins['T']['obj']='/Script/CoreUObject.Transform';rotated[0].pins['Location']['obj']=VEC
    axes=g.call(MATH,'BreakVector',pure=True,static=True).pin('InVec','struct',obj=VEC)
    for p in ['X','Y','Z']:axes.pin(p,'real',sub='double',out=True)
    g.w(rotated,axes,'InVec')
    lift=g.op('Subtract_DoubleDouble',g.v('FPHeight'),(axes,'Z'))
    lift=g.op('Add_DoubleDouble',lift,g.op('Multiply_DoubleDouble',wave,g.op('Multiply_DoubleDouble',weight,.65)))
    loc=g.c(MATH,'MakeVector',[('X','real',g.op('Subtract_DoubleDouble',g.v('FPForward'),(axes,'X'))),('Y','real',g.op('Subtract_DoubleDouble',22,(axes,'Y'))),('Z','real',lift)],cat='struct',obj=VEC)
    transform(prev,arms,loc,rotation)

if __name__=='__main__':
    from generate_delivery_controls import player_camera
    player_camera()
