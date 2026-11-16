"""Blueprint sources for pause, persistent options, and keyboard camera refinement."""
import re
from generate_delivery_save import SaveGraph
from generate_progression_graphs import capture, player as original_player, ACTOR, OBJECT, GS, MATH, HERO, DIRECTOR, PRIM
from generate_delivery_graphs import q, ref
from delivery_save_schema import MANAGER as SAVE_MANAGER

R='/Game/ThirdPerson/Blueprints/Entrega/'
UI=R+'BP_DeliveryInterface.BP_DeliveryInterface_C'
OPTIONS_DATA=R+'BP_DeliveryOptions.BP_DeliveryOptions_C'
PAUSE='/Game/Menu/Menu_Pausa.Menu_Pausa_C'
OPTIONS='/Game/Menu/Menu_Opciones.Menu_Opciones_C'
WIDGET='/Script/UMG.UserWidget'; W='/Script/UMG.Widget'; BUTTON='/Script/UMG.Button'
PC='/Script/Engine.PlayerController'; SETTINGS='/Script/Engine.GameUserSettings'
MIX='/Game/ThirdPerson/Audio/SM_TimeOutSettings.SM_TimeOutSettings'
VEC='/Script/CoreUObject.Vector'

class ControlsGraph(SaveGraph):
    def pc(self):return self.c(GS,'GetPlayerController',[('PlayerIndex','int',0)],cat='object',obj=PC)
    def cast_after(self,prev,value,cls,pin='then'):
        n=self.cast(cls);self.chain(prev,n,pin);self.w(value,n,'Object')
        return n,(n,'As'+cls.rsplit('.',1)[-1].removesuffix('_C'))
    def ui(self,prev):
        find=self.find(prev,UI)
        return self.cast_after(find,(find,'ReturnValue'),UI)
    def widget(self,prev,cls):
        n=self.node('K2Node_CreateWidget');n.kind='UMGEditor.K2Node_CreateWidget'
        n.pin('execute').pin('then',out=True).pin('Class','class',obj=WIDGET,default_obj=cls)
        n.pin('OwningPlayer','object',obj=PC).pin('ReturnValue','object',obj=cls,out=True)
        self.w(self.pc(),n,'OwningPlayer');self.chain(prev,n)
        return n,(n,'ReturnValue')
    def clicked(self,asset,field,index):
        return self.node('K2Node_ComponentBoundEvent',[
            'DelegatePropertyName="OnClicked"','DelegateOwnerClass='+ref(BUTTON),
            'ComponentPropertyName='+q(field),
            'EventReference=(MemberParent="/Script/CoreUObject.Package\'/Script/UMG\'",MemberName="OnButtonClickedEvent__DelegateSignature")',
            'bInternalEvent=True','CustomFunctionName='+q('BndEvt__'+asset+'_'+field+'_Control_'+str(index)+'_OnButtonClickedEvent__DelegateSignature')
        ]).pin('then',out=True)
    def mode(self,prev,focus=None,game=False):
        n=self.call('/Script/UMG.WidgetBlueprintLibrary','SetInputMode_GameOnly' if game else 'SetInputMode_GameAndUIEx',static=True)
        n.pin('PlayerController','object',obj=PC).pin('bFlushInput','bool',default='true');self.w(self.pc(),n,'PlayerController')
        if not game:
            n.pin('InWidgetToFocus','object',obj=W).pin('InMouseLockMode','byte',obj='/Script/Engine.EMouseLockMode',default='DoNotLock').pin('bHideCursorDuringCapture','bool',default='false')
            if focus:self.w(focus,n,'InWidgetToFocus')
        self.chain(prev,n)
        if game:
            focus=self.call('/Script/UMG.WidgetBlueprintLibrary','SetFocusToGameViewport',static=True)
            self.chain(n,focus)
            capture=self.call(GS,'SetViewportMouseCaptureMode',static=True).pin('MouseCaptureMode','byte',obj='/Script/Engine.EMouseCaptureMode',default='CapturePermanently_IncludingInitialMouseDown')
            self.chain(focus,capture);return capture
        return n
    def cursor(self,prev,visible):
        return self.s(prev,'bShowMouseCursor',visible,'bool',owner=PC,target=self.pc())
    def text(self,prev,field,value):
        n=self.call('/Script/UMG.TextBlock','SetText').pin('InText','text');self.w(self.v(field,'object',obj='/Script/UMG.TextBlock'),n,'self')
        convert=self.c('/Script/Engine.KismetTextLibrary','Conv_StringToText',[('InString','string',value)],cat='text');self.w(convert,n,'InText')
        self.chain(prev,n);return n
    def getter_settings(self,prev):
        n=self.call(SETTINGS,'GetGameUserSettings',static=True).pin('ReturnValue','object',obj=SETTINGS,out=True);self.chain(prev,n)
        return n,(n,'ReturnValue')
    def audio_slot(self,name):
        return self.call(GS,name,static=True).pin('SlotName','string',default='TimeOut_Options_v1').pin('UserIndex','int',default='0')

def flatten(g,owner):
    """Share exec entries for local events before their reflected signatures exist."""
    calls=[n for n in g.nodes if n.kind.endswith('K2Node_CallFunction') and any(owner in p for p in n.props)]
    for call in calls:
        text=' '.join(call.props);match=re.search(r'MemberName="([^"]+)"',text)
        if not match:continue
        event=next((n for n in g.nodes if 'CustomFunctionName='+q(match[1]) in n.props),None)
        if not event:continue
        for name,pid in list(call.pins['execute']['links']):
            source=next(n for n in g.nodes if n.name==name);pin=next(p for p in source.pins.values() if p['id']==pid)
            pin['links'].remove((call.name,call.pins['execute']['id']))
            for target_name,target_id in event.pins['then']['links']:
                target=next(n for n in g.nodes if n.name==target_name);target_pin=next(p for p in target.pins.values() if p['id']==target_id)
                g.wire(source,pin['name'],target,target_pin['name'])
        for n in g.nodes:
            for p in n.pins.values():p['links']=[l for l in p['links'] if l[0]!=call.name]
        g.nodes.remove(call)

def interface():
    g=ControlsGraph();self=g.selfnode(typ=UI);pc=g.pc()
    pause=g.local('PauseWidget',WIDGET);options=g.local('OptionsWidget',WIDGET)
    ret=g.local('ReturnWidget',WIDGET);focus=g.local('ReturnFocus',W)
    def own(prev,name,pin='then'):return g.action_on(prev,UI,name,pin=pin)
    def show(prev,target,visibility):
        return g.action_on(prev,W,'SetVisibility',target,[('InVisibility','byte',visibility,'/Script/UMG.ESlateVisibility')])
    def ignore(prev,value):
        prev=g.action_on(prev,'/Script/Engine.Controller','SetIgnoreMoveInput',pc,[('bNewMoveInput','bool',value,None)])
        return g.action_on(prev,'/Script/Engine.Controller','SetIgnoreLookInput',pc,[('bNewLookInput','bool',value,None)])
    # Load only the audio preference. GameUserSettings owns graphics persistence.
    begin=g.event(ACTOR,'ReceiveBeginPlay')
    exists=g.audio_slot('DoesSaveGameExist').pin('ReturnValue','bool',out=True);g.chain(begin,exists)
    test=g.br(exists,(exists,'ReturnValue'))
    load=g.audio_slot('LoadGameFromSlot').pin('ReturnValue','object',obj='/Script/Engine.SaveGame',out=True);g.chain(test,load)
    cast,data=g.cast_after(load,(load,'ReturnValue'),OPTIONS_DATA)
    version=g.v('Version','int',owner=OPTIONS_DATA,target=data)
    good=g.br(cast,g.cmp('EqualEqual_IntInt',version,1,'int'))
    value=g.c(MATH,'FClamp',[('Value','real',g.v('MasterVolume',owner=OPTIONS_DATA,target=data)),('Min','real',0),('Max','real',1)])
    prev=g.s(good,'MasterVolume',value)
    apply=own(prev,'ApplyVolume')
    g.chain(test,apply,'else');g.chain(cast,apply,'CastFailed');g.chain(good,apply,'else')
    e=g.custom('ApplyVolume')
    base=g.call(GS,'SetBaseSoundMix',static=True).pin('InSoundMix','object',obj='/Script/Engine.SoundMix',default_obj=MIX);g.chain(e,base)
    mix=g.call(GS,'SetSoundMixClassOverride',static=True).pin('InSoundMixModifier','object',obj='/Script/Engine.SoundMix',default_obj=MIX).pin('InSoundClass','object',obj='/Script/Engine.SoundClass',default_obj='/Engine/EngineSounds/Master.Master').pin('Volume','real',sub='float').pin('Pitch','real',sub='float',default='1').pin('FadeInTime','real',sub='float',default='0').pin('bApplyToChildren','bool',default='true');g.w(g.v('MasterVolume'),mix,'Volume');g.chain(base,mix)
    e=g.custom('SaveVolume');make=g.call(GS,'CreateSaveGameObject',static=True).pin('SaveGameClass','class',obj='/Script/Engine.SaveGame',default_obj=OPTIONS_DATA).pin('ReturnValue','object',obj='/Script/Engine.SaveGame',out=True);g.chain(e,make)
    cast,data=g.cast_after(make,(make,'ReturnValue'),OPTIONS_DATA)
    prev=g.s(cast,'Version',1,'int',owner=OPTIONS_DATA,target=data)
    prev=g.s(prev,'MasterVolume',g.v('MasterVolume'),owner=OPTIONS_DATA,target=data)
    save=g.audio_slot('SaveGameToSlot').pin('SaveGameObject','object',obj='/Script/Engine.SaveGame').pin('ReturnValue','bool',out=True);g.w(data,save,'SaveGameObject');g.chain(prev,save)
    # Pause input is handled above the inherited character P binding.
    for key in ['P','Escape']:
        k=g.key(key);k.props=[p.replace('bConsumeInput=False','bConsumeInput=True') for p in k.props]
        own(k,'TogglePause','Pressed')
    e=g.custom('TogglePause');choice=g.br(e,g.v('bOptionsOpen','bool'));own(choice,'CloseOptions')
    openchoice=g.br(choice,g.v('bPauseOpen','bool'),'else');own(openchoice,'ClosePause');own(openchoice,'OpenPause','else')
    e=g.custom('OpenPause');found=g.find(e,DIRECTOR);valid=g.br(found,(g.valid(found,'ReturnValue'),'ReturnValue'))
    cast,director=g.cast_after(valid,(found,'ReturnValue'),DIRECTOR)
    alive=g.br(cast,g.cmp('Less_IntInt',g.v('Paso','int',owner=DIRECTOR,target=director),4,'int'))
    paused=g.call(GS,'SetGamePaused',static=True).pin('bPaused','bool',default='true').pin('ReturnValue','bool',out=True);g.chain(alive,paused)
    created,widget=g.widget(paused,PAUSE);prev=g.s(created,'PauseWidget',widget,'object',obj=WIDGET)
    prev=g.action_on(prev,WIDGET,'AddToViewport',widget,[('ZOrder','int',100,None)])
    prev=g.s(prev,'bPauseOpen',True,'bool');prev=ignore(prev,True);prev=g.cursor(prev,True)
    pcast,pw=g.cast_after(prev,widget,PAUSE);resume=g.v('btn_reanudar_pausa','object',owner=PAUSE,target=pw,obj=BUTTON)
    g.mode(pcast,resume)
    e=g.custom('ClosePause');guard=g.br(e,g.v('bPauseOpen','bool'))
    prev=g.action_on(guard,W,'RemoveFromParent',pause)
    paused=g.call(GS,'SetGamePaused',static=True).pin('bPaused','bool',default='false').pin('ReturnValue','bool',out=True);g.chain(prev,paused)
    prev=g.s(paused,'bPauseOpen',False,'bool');prev=ignore(prev,False);prev=g.cursor(prev,False);g.mode(prev,game=True)
    # Options always return to the exact originating menu instance.
    e=g.custom('OpenOptions').pin('PreviousWidget','object',obj=WIDGET,out=True).pin('PreviousFocus','object',obj=W,out=True)
    for pin,cls in [('PreviousWidget',WIDGET),('PreviousFocus',W)]:
        e.props.append('CustomProperties UserDefinedPin (PinName='+q(pin)+',PinType=(PinCategory="object",PinSubCategoryObject='+ref(cls)+'),DesiredPinDirection=EGPD_Output)')
    prev=g.s(e,'ReturnWidget',(e,'PreviousWidget'),'object',obj=WIDGET)
    prev=g.s(prev,'ReturnFocus',(e,'PreviousFocus'),'object',obj=W)
    prev=show(prev,ret,'Collapsed')
    created,widget=g.widget(prev,OPTIONS);prev=g.s(created,'OptionsWidget',widget,'object',obj=WIDGET)
    prev=g.action_on(prev,WIDGET,'AddToViewport',widget,[('ZOrder','int',110,None)])
    prev=g.s(prev,'bOptionsOpen',True,'bool')
    cast,ow=g.cast_after(prev,widget,OPTIONS);first=g.v('btn_resolucion1_O','object',owner=OPTIONS,target=ow,obj=BUTTON)
    g.mode(cast,first)
    e=g.custom('CloseOptions');guard=g.br(e,g.v('bOptionsOpen','bool'))
    prev=g.action_on(guard,W,'RemoveFromParent',options);prev=show(prev,ret,'Visible')
    prev=g.s(prev,'bOptionsOpen',False,'bool');g.mode(prev,focus)
    flatten(g,UI);g.write('BP_DeliveryInterface')

def pause_menu():
    g=ControlsGraph()
    for i,(field,action) in enumerate([('btn_reanudar_pausa','ClosePause'),('btn_opciones_pausa','OpenOptions'),('btn_irmenu_pausa','ClosePause'),('btn_salvarjuego_pausa','SaveCheckpoint')]):
        e=g.clicked('Menu_Pausa',field,i)
        if action=='SaveCheckpoint':
            f=g.find(e,SAVE_MANAGER);cast,target=g.cast_after(f,(f,'ReturnValue'),SAVE_MANAGER)
            tail=g.action_on(cast,SAVE_MANAGER,action,target)
            text=g.v('StatusText','string',owner=SAVE_MANAGER,target=target);g.text(tail,'PauseSaveStatus',text)
            continue
        cast,target=g.ui(e)
        call=g.action_on(cast,UI,action,target)
        if action=='OpenOptions':
            call.pin('PreviousWidget','object',obj=WIDGET).pin('PreviousFocus','object',obj=W)
            g.w((g.selfnode(typ=WIDGET),'self'),call,'PreviousWidget');g.w(g.v(field,'object',obj=BUTTON),call,'PreviousFocus')
        if field=='btn_irmenu_pausa':
            level=g.call(GS,'OpenLevel',static=True).pin('LevelName','name',default='/Game/LevelMenu/MainMenuLevel').pin('bAbsolute','bool',default='true').pin('Options','string');g.chain(call,level)
    g.write('Menu_Pausa')

def options_menu():
    g=ControlsGraph()
    def status(prev,message):return g.text(prev,'SettingsStatus',message)
    def apply(prev,target,message):
        n=g.action_on(prev,SETTINGS,'ApplySettings',target,[('bCheckForCommandLineOverrides','bool',False,None)])
        n=g.action_on(n,SETTINGS,'ConfirmVideoMode',target)
        n=g.action_on(n,SETTINGS,'SaveSettings',target)
        return status(n,message)
    def label(index,values):
        n=g.node('K2Node_Select',['NumOptionPins='+str(len(values)),'IndexPinType=(PinCategory="int")']).pin('Index','int').pin('ReturnValue','string',out=True);g.w(index,n,'Index')
        for i,s in enumerate(values):n.pin('Option '+str(i),'string',default=s)
        return n,'ReturnValue'
    # Show actual saved scalability values rather than implying every button is selected.
    construct=g.event(WIDGET,'Construct');entry,settings=g.getter_settings(construct)
    summary=('','')
    string=None
    for heading,getter in [('Distancia','GetViewDistanceQuality'),('Suavizado','GetAntiAliasingQuality'),('Sombras','GetShadowQuality'),('Texturas','GetTextureQuality')]:
        n=g.call(SETTINGS,getter,pure=True).pin('ReturnValue','int',out=True);g.w(settings,n,'self')
        value=label((n,'ReturnValue'),['Baja','Media','Alta','Epica','Cine'])
        part=g.c('/Script/Engine.KismetStringLibrary','Concat_StrStr',[('A','string',heading+': '),('B','string',value)],cat='string')
        if string is None:string=part
        else:
            string=g.c('/Script/Engine.KismetStringLibrary','Concat_StrStr',[('A','string',string),('B','string',' | ')],cat='string')
            string=g.c('/Script/Engine.KismetStringLibrary','Concat_StrStr',[('A','string',string),('B','string',part)],cat='string')
    status(entry,string)
    groups=[('viewdistance',3,'SetViewDistanceQuality',[0,1,3]),('antialiasing',4,'SetAntiAliasingQuality',[0,1,2,3]),('shadow',4,'SetShadowQuality',[0,1,2,3]),('texture',4,'SetTextureQuality',[0,1,2,3])]
    counter=0
    for group,count,method,values in groups:
        for i in range(count):
            e=g.clicked('Menu_Opciones','btn_'+group+str(i+1)+'_O',counter);counter+=1
            prev,s=g.getter_settings(e)
            prev=g.action_on(prev,SETTINGS,method,s,[('Value','int',values[i],None)])
            apply(prev,s,'Ajuste aplicado y guardado. ESC vuelve al menu anterior.')
    for i,(x,y) in enumerate([(1280,720),(1600,900),(1920,1080),(2560,1440)],1):
        e=g.clicked('Menu_Opciones','btn_resolucion'+str(i)+'_O',counter);counter+=1
        prev,s=g.getter_settings(e)
        prev=g.action_on(prev,SETTINGS,'SetScreenResolution',s,[('Resolution','struct','(X='+str(x)+',Y='+str(y)+')','/Script/CoreUObject.IntPoint')])
        apply(prev,s,'Resolucion '+str(x)+'x'+str(y)+' guardada.')
    for i,mode in enumerate(['Windowed','WindowedFullscreen','Fullscreen']):
        e=g.clicked('Menu_Opciones','btn_display'+str(i),counter);counter+=1
        prev,s=g.getter_settings(e)
        prev=g.action_on(prev,SETTINGS,'SetFullscreenMode',s,[('InFullscreenMode','byte',mode,'/Script/Engine.EWindowMode')])
        apply(prev,s,'Modo de pantalla aplicado y guardado.')
    for i,volume in enumerate([0,.25,.5,1]):
        e=g.clicked('Menu_Opciones','btn_volume'+str(i),counter);counter+=1
        prev,ui=g.ui(e);prev=g.s(prev,'MasterVolume',volume,owner=UI,target=ui)
        prev=g.action_on(prev,UI,'ApplyVolume',ui);prev=g.action_on(prev,UI,'SaveVolume',ui)
        status(prev,'Volumen '+str(round(volume*100))+' % guardado.')
    # The original Back button kept a copied main-menu variable name.
    e=g.clicked('Menu_Opciones','btn_volver_opciones',counter);prev,ui=g.ui(e);g.action_on(prev,UI,'CloseOptions',ui)
    g.write('Menu_Opciones')

def main_menu():
    from generate_delivery_save import menu as base
    g=capture(base);g.__class__=ControlsGraph
    e=next(n for n in g.nodes if any('ComponentPropertyName="btn_opciones_menu"'==p for p in n.props))
    # Replace the failed widget creation path while keeping the art and save checks.
    obsolete=set();pending=[name for name,pid in e.pins['then']['links']]
    while pending:
        name=pending.pop()
        if name in obsolete:continue
        obsolete.add(name);node=next(n for n in g.nodes if n.name==name)
        pending.extend(t for p in node.pins.values() if p['out'] and p['cat']=='exec' for t,pid in p['links'])
    g.nodes=[n for n in g.nodes if n.name not in obsolete]
    for node in g.nodes:
        for pin in node.pins.values():pin['links']=[link for link in pin['links'] if link[0] not in obsolete]
    e.pins['then']['links']=[]
    prev,ui=g.ui(e)
    n=g.action_on(prev,UI,'OpenOptions',ui).pin('PreviousWidget','object',obj=WIDGET).pin('PreviousFocus','object',obj=W)
    g.w((g.selfnode(typ=WIDGET),'self'),n,'PreviousWidget');g.w(g.v('btn_opciones_menu','object',obj=BUTTON),n,'PreviousFocus')
    construct=next(n for n in g.nodes if any('MemberName="Construct"' in p for p in n.props))
    split_exec(g,construct)
    focus=g.v('btn_nuevojuego_menu','object',obj=BUTTON)
    cursor=g.s(g._split,'bShowMouseCursor',True,'bool',owner=PC,target=g.pc(),pin='then_1')
    g.mode(cursor,focus)
    g.write('Menu_Inicio')

def split_exec(g,event):
    old=list(event.pins['then']['links']);event.pins['then']['links']=[]
    n=g.node('K2Node_ExecutionSequence').pin('execute').pin('then_0',out=True).pin('then_1',out=True);g.chain(event,n)
    for name,pid in old:
        target=next(x for x in g.nodes if x.name==name);pin=next(p for p in target.pins.values() if p['id']==pid)
        pin['links'].remove((event.name,event.pins['then']['id']));g.chain(n,target,'then_0',pin['name'])
    g._split=n;return n

def player_camera():
    g=capture(original_player);g.__class__=ControlsGraph
    first=g.v('FPC','object',obj='/Script/Engine.CameraComponent')
    capsule=g.v('CapsuleComponent','object',owner='/Script/Engine.Character',target=(g.selfnode(typ=HERO),'self'),obj='/Script/Engine.CapsuleComponent',native=True)
    begin=next(n for n in g.nodes if n.kind.endswith('K2Node_Event') and any('ReceiveBeginPlay' in p for p in n.props))
    seq=split_exec(g,begin)
    # The menu used GameAndUI in a different world. Explicitly take the mouse
    # after possession and camera setup in the new gameplay world.
    attach=g.call('/Script/Engine.SceneComponent','K2_AttachToComponent').pin('Parent','object',obj='/Script/Engine.SceneComponent').pin('SocketName','name',default='None').pin('bWeldSimulatedBodies','bool',default='false').pin('ReturnValue','bool',out=True)
    for key in ['LocationRule','RotationRule','ScaleRule']:attach.pin(key,'byte',obj='/Script/Engine.EAttachmentRule',default='SnapToTarget')
    g.w(first,attach,'self');g.w(capsule,attach,'Parent');g.chain(seq,attach,'then_1')
    position=g.call('/Script/Engine.SceneComponent','K2_SetRelativeLocation').pin('NewLocation','struct',obj=VEC,default='0,0,64').pin('bSweep','bool',default='false').pin('SweepHitResult','struct',obj='/Script/Engine.HitResult',out=True).pin('bTeleport','bool',default='true');g.w(first,position,'self');g.chain(attach,position)
    prev=g.s(position,'bUsePawnControlRotation',True,'bool',owner='/Script/Engine.CameraComponent',target=first)
    prev=g.action_on(prev,'/Script/Engine.CameraComponent','SetFieldOfView',first,[('InFieldOfView','real',90,None)])
    prev=g.cursor(prev,False);prev=g.mode(prev,game=True)
    hitbox=g.v('WeaponHitbox','object',obj='/Script/Engine.BoxComponent')
    g.action_on(prev,PRIM,'SetCollisionResponseToChannel',hitbox,[('Channel','byte','ECC_Destructible','/Script/Engine.ECollisionChannel'),('NewResponse','byte','ECR_Overlap','/Script/Engine.ECollisionResponse')])
    tick=next(n for n in g.nodes if n.kind.endswith('K2Node_Event') and any('ReceiveTick' in p for p in n.props));seq=split_exec(g,tick)
    mode=g.v('CamaraPrimera','bool');changed=g.cmp('NotEqual_BoolBool',mode,g.v('LastFirstPerson','bool'),'bool')
    b=g.br(seq,changed,'then_1');prev=g.s(b,'LastFirstPerson',mode,'bool')
    mesh=g.v('Mesh','object',obj='/Script/Engine.SkeletalMeshComponent')
    g.action_on(prev,PRIM,'SetOwnerNoSee',mesh,[('bNewOwnerNoSee','bool',mode,None)])
    from generate_evaluation_graphs import add_destructible_combat
    add_destructible_combat(g)
    g.write('BP_PlayerEntrega')

if __name__=='__main__':
    from generate_progression_graphs import director
    director()
    interface();pause_menu();options_menu();main_menu();player_camera()
