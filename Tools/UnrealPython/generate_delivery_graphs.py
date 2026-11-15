"""Local tool: generate reviewable Blueprint clipboard text for the delivery slice.

Paste each output into its matching Blueprint's empty EventGraph in Unreal, then
compile/export it. This is normal Blueprint code, not editor-only runtime Python.
"""
import json
import os
import uuid

OUT = os.path.abspath('Intermediate/inspect/delivery_graphs')
os.makedirs(OUT, exist_ok=True)
ACTOR = '/Script/Engine.Actor'
PAWN = '/Script/Engine.Pawn'
OBJECT = '/Script/CoreUObject.Object'
MESH_ACTOR = '/Script/Engine.StaticMeshActor'
MESH_COMP = '/Script/Engine.StaticMeshComponent'
DIRECTOR = '/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'
HEALTH = '/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C'

def q(s):
    return json.dumps(str(s),ensure_ascii=False)

def ref(path, kind='Class'):
    return q('/Script/CoreUObject.%s\'%s\'' % (kind,path))

class Node:
    def __init__(self, graph, kind, props=(), x=0, y=0):
        self.kind = kind
        self.name = '%s_%d' % (kind.rsplit('.',1)[-1],len(graph.nodes))
        self.props = list(props)
        self.pins = {}
        self.x,self.y = x,y
        graph.nodes.append(self)

    def pin(self,name,cat='exec',out=False,default=None,obj=None,sub='',hidden=False,default_obj=None):
        self.pins[name] = dict(name=name,cat=cat,out=out,default=default,obj=obj,sub=sub,hidden=hidden,
                               default_obj=default_obj,id=uuid.uuid4().hex.upper(),links=[])
        return self

    def render(self):
        lines = ['Begin Object Class=/Script/'+self.kind+' Name='+q(self.name)]
        lines += ['   '+p for p in self.props]
        lines += ['   NodePosX=%d'%self.x,'   NodePosY=%d'%self.y,'   NodeGuid='+uuid.uuid4().hex.upper()]
        for p in self.pins.values():
            f = ['PinId='+p['id'],'PinName='+q(p['name'])]
            if p['out']: f += ['Direction="EGPD_Output"']
            f += ['PinType.PinCategory='+q(p['cat']),'PinType.PinSubCategory='+q(p['sub'])]
            if p['obj']:
                kind = 'ScriptStruct' if p['cat']=='struct' else ('BlueprintGeneratedClass' if p['obj'].startswith('/Game/') else 'Class')
                prefix = '/Script/CoreUObject.' if kind in ('Class','ScriptStruct') else '/Script/Engine.'
                f += ['PinType.PinSubCategoryObject='+q(prefix+kind+"'"+p['obj']+"'")]
            else: f += ['PinType.PinSubCategoryObject=None']
            f += ['PinType.ContainerType='+p.get('container','None')]
            if p['default'] is not None: f += ['DefaultValue='+q(p['default'])]
            if p['default_obj'] is not None: f += ['DefaultObject='+q(p['default_obj'])]
            if p['links']: f += ['LinkedTo=('+''.join('%s %s,'%l for l in p['links'])+')']
            f += ['bHidden='+str(p['hidden']),'bOrphanedPin=False']
            lines += ['   CustomProperties Pin ('+','.join(f)+',)']
        return '\n'.join(lines+['End Object'])

class Graph:
    def __init__(self): self.nodes=[]
    def node(self,kind,props=(),x=0,y=0): return Node(self,'BlueprintGraph.'+kind,props,x,y)
    def wire(self,a,ap,b,bp):
        a.pins[ap]['links'].append((b.name,b.pins[bp]['id']))
        b.pins[bp]['links'].append((a.name,a.pins[ap]['id']))
    def event(self,owner,name,**pos):
        return self.node('K2Node_Event',['EventReference=(MemberParent='+ref(owner)+',MemberName='+q(name)+')','bOverrideFunction=True'],**pos).pin('then',out=True)
    def key(self,key,**pos):
        return self.node('K2Node_InputKey',['InputKey='+key,'bConsumeInput=False','bExecuteWhenPaused=True'],**pos).pin('Pressed',out=True).pin('Released',out=True).pin('Key','struct',out=True,obj='/Script/InputCore.Key')
    def call(self,owner,name,pure=False,static=False,**pos):
        props=['FunctionReference=(MemberParent='+ref(owner)+',MemberName='+q(name)+')']
        if pure: props += ['bDefaultsToPureFunc=True']
        n=self.node('K2Node_CallFunction',props,**pos)
        if not pure: n.pin('execute').pin('then',out=True)
        n.pin('self','object',obj=owner,hidden=static,default_obj=owner.rsplit('.',1)[0]+'.Default__'+owner.rsplit('.',1)[1] if static else None)
        if static and owner.endswith(('GameplayStatics','KismetSystemLibrary')):
            n.pin('WorldContextObject','object',obj=OBJECT,hidden=True)
        return n
    def get(self,name,cat,owner=None,obj=None,sub='',**pos):
        props=['VariableReference=(MemberName='+q(name)+(','+'MemberParent='+q('/Script/Engine.BlueprintGeneratedClass\''+owner+'\'') if owner else ',bSelfContext=True')+')']
        n=self.node('K2Node_VariableGet',props,**pos).pin(name,cat,out=True,obj=obj,sub=sub)
        if owner: n.pin('self','object',obj=owner)
        return n
    def set(self,name,cat,default,obj=None,sub='',**pos):
        return self.node('K2Node_VariableSet',['VariableReference=(MemberName='+q(name)+',bSelfContext=True)'],**pos).pin('execute').pin('then',out=True).pin(name,cat,default=default,obj=obj,sub=sub).pin('Output_Get',cat,out=True,obj=obj,sub=sub)
    def branch(self,**pos): return self.node('K2Node_IfThenElse',**pos).pin('execute').pin('Condition','bool',default='true').pin('then',out=True).pin('else',out=True)
    def compare(self,fn,cat,b,sub='',**pos):
        return self.call('/Script/Engine.KismetMathLibrary',fn,pure=True,static=True,**pos).pin('A',cat,sub=sub).pin('B',cat,sub=sub,default=b).pin('ReturnValue','bool',out=True)
    def player(self,**pos): return self.call('/Script/Engine.GameplayStatics','GetPlayerPawn',pure=True,static=True,**pos).pin('PlayerIndex','int',default='0').pin('ReturnValue','object',out=True,obj=PAWN)
    def distance(self,target,target_pin,player,x,y):
        n=self.call(ACTOR,'GetHorizontalDistanceTo',pure=True,x=x,y=y).pin('OtherActor','object',obj=ACTOR).pin('ReturnValue','real',sub='float',out=True)
        self.wire(target,target_pin,n,'self');self.wire(player,'ReturnValue',n,'OtherActor')
        return n
    def cast(self,cls,**pos):
        return self.node('K2Node_DynamicCast',['TargetType='+q('/Script/Engine.BlueprintGeneratedClass\''+cls+'\'')],**pos).pin('execute').pin('then',out=True).pin('CastFailed',out=True).pin('Object','object',obj=OBJECT).pin('As'+cls.rsplit('.',1)[-1].removesuffix('_C'),'object',obj=cls,out=True)
    def pause(self,**pos): return self.call('/Script/Engine.GameplayStatics','SetGamePaused',static=True,**pos).pin('bPaused','bool',default='true').pin('ReturnValue','bool',out=True)
    def write(self,name):
        path=os.path.join(OUT,name+'.t3d')
        with open(path,'w',encoding='utf-8') as f:f.write('\n'.join(n.render() for n in self.nodes))
        print(name,len(self.nodes),'nodes',path)

def director():
    from generate_hostage_graphs import HostageGraph
    g=HostageGraph()
    step=g.get('Paso','int',x=0,y=250)
    player=g.player(x=0,y=500)
    # One input press evaluates exactly one step. Repeated input cannot reactivate it.
    switch=g.node('K2Node_SwitchInteger',x=300,y=0).pin('execute').pin('Selection','int',default='0').pin('Default',out=True)
    for i in range(3):switch.pin(str(i),out=True)
    g.wire(step,'Paso',switch,'Selection')
    hostage_class='/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'
    hostage=g.call('/Script/Engine.GameplayStatics','GetActorOfClass',static=True,x=0,y=-650).pin('ActorClass','class',obj=ACTOR,default_obj=hostage_class).pin('ReturnValue','object',obj=hostage_class,out=True)
    interact=g.call(ACTOR,'Interactuar',x=350,y=-650)
    interact.props=['FunctionReference=(MemberParent='+q('/Script/Engine.BlueprintGeneratedClass\''+hostage_class+'\'')+',MemberName="Interactuar")']
    interact.pins['self']['obj']=hostage_class
    g.wire(hostage,'ReturnValue',interact,'self');g.wire(hostage,'then',interact,'execute');g.wire(interact,'then',switch,'execute')
    for key,y in [('E',0),('Gamepad_RightShoulder',-200)]:
        n=g.key(key,x=-350,y=y);g.wire(n,'Pressed',hostage,'execute')
    for i in range(3):
        y=i*550
        beacon=g.get('Baliza%d'%(i+1),'object',obj=MESH_ACTOR,x=600,y=y+200)
        distance=g.distance(beacon,'Baliza%d'%(i+1),player,850,y+200)
        near=g.compare('LessEqual_DoubleDouble','real','250',sub='double',x=1100,y=y+200)
        g.wire(distance,'ReturnValue',near,'A')
        branch=g.branch(x=1400,y=y);g.wire(switch,str(i),branch,'execute');g.wire(near,'ReturnValue',branch,'Condition')
        component=g.get('StaticMeshComponent','object',owner=MESH_ACTOR,obj=MESH_COMP,x=1450,y=y+200)
        # Native variables require a native member-parent reference.
        component.props=['VariableReference=(MemberParent='+ref(MESH_ACTOR)+',MemberName="StaticMeshComponent")']
        g.wire(beacon,'Baliza%d'%(i+1),component,'self')
        material=g.call('/Script/Engine.PrimitiveComponent','SetMaterial',x=1700,y=y).pin('ElementIndex','int',default='0').pin('Material','object',obj='/Script/Engine.MaterialInterface',default_obj='/Game/ThirdPerson/Environment/EscenarioIan/M_Baliza_Activa.M_Baliza_Activa')
        g.wire(branch,'then',material,'execute');g.wire(component,'StaticMeshComponent',material,'self')
        advance=g.set('Paso','int',str(i+1),x=2000,y=y);g.wire(material,'then',advance,'execute')
    # Watch only the delivery outcome. AI decisions stay in the existing trees.
    tick=g.event(ACTOR,'ReceiveTick',x=0,y=2100).pin('DeltaSeconds','real',sub='float',out=True)
    active=g.compare('Less_IntInt','int','4',x=0,y=2300);g.wire(step,'Paso',active,'A')
    alive_branch=g.branch(x=300,y=2100);g.wire(tick,'then',alive_branch,'execute');g.wire(active,'ReturnValue',alive_branch,'Condition')
    component=g.call(ACTOR,'GetComponentByClass',pure=True,x=300,y=2500).pin('ComponentClass','class',obj='/Script/Engine.ActorComponent',default_obj=HEALTH).pin('ReturnValue','object',obj='/Script/Engine.ActorComponent',out=True)
    g.wire(player,'ReturnValue',component,'self')
    health=g.get('Health','real',owner=HEALTH,sub='double',x=900,y=2500);g.wire(component,'ReturnValue',health,'self')
    dead=g.compare('LessEqual_DoubleDouble','real','0',sub='double',x=1150,y=2500);g.wire(health,'Health',dead,'A')
    dead_branch=g.branch(x=1400,y=2100);g.wire(alive_branch,'then',dead_branch,'execute');g.wire(dead,'ReturnValue',dead_branch,'Condition')
    lose=g.set('Paso','int','5',x=1650,y=2000);g.wire(dead_branch,'then',lose,'execute')
    losepause=g.pause(x=1900,y=2000);g.wire(lose,'then',losepause,'execute')
    ready=g.compare('EqualEqual_IntInt','int','3',x=650,y=2900);g.wire(step,'Paso',ready,'A')
    exit_branch=g.branch(x=1650,y=2800);g.wire(dead_branch,'else',exit_branch,'execute');g.wire(ready,'ReturnValue',exit_branch,'Condition')
    exit=g.get('Salida','object',obj=MESH_ACTOR,x=900,y=3100)
    distance=g.distance(exit,'Salida',player,1150,3100)
    near=g.compare('LessEqual_DoubleDouble','real','300',sub='double',x=1400,y=3100);g.wire(distance,'ReturnValue',near,'A')
    escort=g.call('/Script/Engine.GameplayStatics','GetActorOfClass',static=True,x=1900,y=2800).pin('ActorClass','class',obj=ACTOR,default_obj=hostage_class).pin('ReturnValue','object',obj=hostage_class,out=True)
    g.wire(exit_branch,'then',escort,'execute')
    bb=g.blackboard(escort,'ReturnValue',x=1900,y=3300)
    accompanying=g.bbget(bb,'bAccompanying',x=2200,y=3300)
    escortdist=g.dist(escort,'ReturnValue',exit,'Salida',x=1900,y=3600)
    escortnear=g.compare('LessEqual_DoubleDouble','real','600',sub='double',x=2200,y=3600);g.wire(escortdist,'ReturnValue',escortnear,'A')
    together=g.boolean('BooleanAND',near,'ReturnValue',escortnear,'ReturnValue',x=2500,y=3400)
    rescued=g.boolean('BooleanAND',together,'ReturnValue',accompanying,'ReturnValue',x=2800,y=3400)
    end=g.branch(x=2500,y=2800);g.wire(escort,'then',end,'execute');g.wire(rescued,'ReturnValue',end,'Condition')
    win=g.set('Paso','int','4',x=2150,y=2800);g.wire(end,'then',win,'execute')
    winpause=g.pause(x=2400,y=2800);g.wire(win,'then',winpause,'execute')
    for key,y,level in [('Enter',3600,'/Game/LevelMenu/MainMenuLevel'),('R',4100,'/Game/ThirdPerson/Maps/Nivel_Entrega')]:
        k=g.key(key,x=0,y=y)
        ended=g.compare('GreaterEqual_IntInt','int','4',x=0,y=y+200);g.wire(step,'Paso',ended,'A')
        b=g.branch(x=300,y=y);g.wire(k,'Pressed',b,'execute');g.wire(ended,'ReturnValue',b,'Condition')
        p=g.pause(x=550,y=y);p.pins['bPaused']['default']='false';g.wire(b,'then',p,'execute')
        op=g.call('/Script/Engine.GameplayStatics','OpenLevel',static=True,x=850,y=y).pin('LevelName','name',default=level).pin('bAbsolute','bool',default='true').pin('Options','string',default='')
        g.wire(p,'then',op,'execute')
    g.write('BP_DirectorEntrega')

def hud():
    from generate_hostage_graphs import HostageGraph
    g=HostageGraph()
    event=g.event('/Script/Engine.HUD','ReceiveDrawHUD',x=0,y=0).pin('SizeX','int',out=True).pin('SizeY','int',out=True)
    get=g.call('/Script/Engine.GameplayStatics','GetActorOfClass',static=True,x=0,y=400).pin('ActorClass','class',obj=ACTOR,default_obj=DIRECTOR).pin('ReturnValue','object',obj=ACTOR,out=True)
    step=g.get('Paso','int',owner=DIRECTOR,x=600,y=400);g.wire(get,'ReturnValue',step,'self')
    text=g.node('K2Node_Select',['NumOptionPins=6','IndexPinType=(PinCategory="int")'],x=900,y=400).pin('Index','int',default='0').pin('ReturnValue','string',out=True)
    messages=['OBJETIVO 1/4 | Activa la baliza 1','OBJETIVO 2/4 | Activa la baliza 2','OBJETIVO 3/4 | Activa la baliza 3','OBJETIVO 4/4 | Lleva al rehen a la zona azul','MISION COMPLETADA | REHEN A SALVO','HAS MUERTO']
    for i,msg in enumerate(messages):text.pin('Option %d'%i,'string',default=msg)
    g.wire(step,'Paso',text,'Index')
    # Fixed left margin; occupies the strip below the existing health widget.
    rect=g.call('/Script/Engine.HUD','DrawRect',x=300,y=0).pin('RectColor','struct',obj='/Script/CoreUObject.LinearColor',default='(R=0.008,G=0.018,B=0.035,A=0.88)').pin('ScreenX','real',sub='float',default='24').pin('ScreenY','real',sub='float',default='95').pin('ScreenW','real',sub='float',default='660').pin('ScreenH','real',sub='float',default='160')
    g.wire(event,'then',get,'execute');g.wire(get,'then',rect,'execute')
    def draw(value,y,prev,x=600,scale='1.2',color='(R=0.9,G=0.95,B=1,A=1)'):
        n=g.call('/Script/Engine.HUD','DrawText',x=x,y=y*4).pin('Text','string',default=value).pin('TextColor','struct',obj='/Script/CoreUObject.LinearColor',default=color).pin('ScreenX','real',sub='float',default='40').pin('ScreenY','real',sub='float',default=str(y)).pin('Font','object',obj='/Script/Engine.Font',default_obj='/Engine/EngineFonts/Roboto.Roboto').pin('Scale','real',sub='float',default=scale).pin('bScalePosition','bool',default='false')
        g.wire(prev,'then',n,'execute')
        return n
    title=draw('OBJETIVOS DE LA MISION',110,rect,scale='1.3',color='(R=0.1,G=0.8,B=1,A=1)')
    objective=draw('',145,title);g.wire(text,'ReturnValue',objective,'Text')
    controls=g.node('K2Node_Select',['NumOptionPins=6','IndexPinType=(PinCategory="int")'],x=1200,y=700).pin('Index','int',default='0').pin('ReturnValue','string',out=True)
    for i in range(6):controls.pin('Option %d'%i,'string',default='E / RB: interactuar cerca | Balizas en orden 1 > 2 > 3' if i<3 else ('Reunete con el rehen y escoltalo hasta la salida.' if i==3 else 'R: reintentar | Enter: volver al menu'))
    g.wire(step,'Paso',controls,'Index')
    hint=draw('',180,objective,scale='1.0');g.wire(controls,'ReturnValue',hint,'Text')
    escort=g.call('/Script/Engine.GameplayStatics','GetActorOfClass',static=True,x=1600,y=900).pin('ActorClass','class',obj=ACTOR,default_obj='/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C').pin('ReturnValue','object',obj=ACTOR,out=True)
    g.chain(hint,escort)
    bb=g.blackboard(escort,'ReturnValue',x=1900,y=1000)
    state=g.bbget(bb,'Estado','Int',x=2200,y=1000)
    status=g.node('K2Node_Select',['NumOptionPins=4','IndexPinType=(PinCategory="int")'],x=2500,y=1000).pin('Index','int',default='0').pin('ReturnValue','string',out=True)
    for i,msg in enumerate(['REHEN: esperando | Acercate y pulsa E / RB para rescatarlo','REHEN: siguiendote | Si detecta enemigos buscara un refugio','REHEN: huyendo | Reunete con el en su refugio','REHEN: refugiado | Despeja la zona y pulsa E / RB cerca']):status.pin('Option %d'%i,'string',default=msg)
    g.wire(state,'ReturnValue',status,'Index')
    statusline=draw('',215,escort,scale='1.0',color='(R=1,G=0.8,B=0.2,A=1)');g.wire(status,'ReturnValue',statusline,'Text')
    g.write('BP_HUD_Entrega')

if __name__=='__main__':
    director()
    hud()
