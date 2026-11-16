"""Two useful macros, two functions and two custom events in the Level Blueprint."""
import json,os
from generate_delivery_controls import ControlsGraph,flatten
from generate_beacon_sequence import table
from generate_progression_graphs import ACTOR,DIRECTOR,HOSTAGE,HERO,MATH,GS,HEALTH
from generate_delivery_graphs import q

spec=json.load(open('Intermediate/inspect/evaluation_level_blueprint.json'))
LEVEL=spec['class'];BP=spec['blueprint']
OUT='Intermediate/inspect/delivery_graphs'

def graphwrite(g,name):
 with open(os.path.join(OUT,name+'.t3d'),'w',encoding='utf-8') as f:f.write('\n'.join(n.render() for n in g.nodes))

def userpin(n,name,kind,out):
 n.pin(name,kind,sub='double' if kind=='real' else '',out=out)
 n.props.append('CustomProperties UserDefinedPin (PinName='+q(name)+',PinType=(PinCategory='+q(kind)+(',PinSubCategory="double"' if kind=='real' else '')+'),DesiredPinDirection='+('EGPD_Output' if out else 'EGPD_Input')+')')

def macro(name,inputs,build):
 g=ControlsGraph()
 entry=g.node('K2Node_Tunnel',['bCanHaveOutputs=True','bCanHaveInputs=False','bIsEditable=True'])
 for key,kind in inputs:userpin(entry,key,kind,True)
 output=g.node('K2Node_Tunnel',['bCanHaveOutputs=False','bCanHaveInputs=True','bIsEditable=True'])
 userpin(output,'Resultado','bool',False)
 g.w(build(g,entry),output,'Resultado');graphwrite(g,name)

macro('AmbosAliadosVivos',[('SaludJugador','real'),('SaludRehen','real')],lambda g,e:g.both(g.cmp('Greater_DoubleDouble',(e,'SaludJugador'),0),g.cmp('Greater_DoubleDouble',(e,'SaludRehen'),0)))
macro('SecuenciaResuelta',[('Paso','int')],lambda g,e:g.both(g.cmp('GreaterEqual_IntInt',(e,'Paso'),3,'int'),g.cmp('LessEqual_IntInt',(e,'Paso'),4,'int')))

def function(name,macroname,arguments):
 g=ControlsGraph()
 entry=g.node('K2Node_FunctionEntry',['FunctionReference=(MemberName='+q(name)+')','ExtraFlags=201457664']).pin('then',out=True)
 result=g.node('K2Node_FunctionResult',['FunctionReference=(MemberName='+q(name)+')']).pin('execute')
 userpin(result,'ReturnValue','bool',False)
 ref='MacroGraphReference=(MacroGraph='+q("/Script/Engine.EdGraph'"+BP+('.' if ':' in BP else ':')+macroname+"'")+',GraphBlueprint='+q("/Script/Engine.LevelScriptBlueprint'"+BP+"'")+')'
 node=g.node('K2Node_MacroInstance',[ref]).pin('Resultado','bool',out=True)
 for key,kind,value in arguments(g):node.pin(key,kind,sub='double' if kind=='real' else '');g.w(value,node,key)
 g.w((node,'Resultado'),result,'ReturnValue');g.chain(entry,result);graphwrite(g,name)

def life_arguments(g):
 player=g.v('Jugador','object',obj=HERO);host=g.v('Rehen','object',obj=HOSTAGE)
 hp=g.v('BPC_Health','object',owner=HERO,target=player,obj=HEALTH)
 return [('SaludJugador','real',g.v('Health',owner=HEALTH,target=hp)),('SaludRehen','real',g.v('Health',owner=HOSTAGE,target=host))]
function('ConsultarAliados', 'AmbosAliadosVivos',life_arguments)
function('ConsultarSecuencia','SecuenciaResuelta',lambda g:[('Paso','int',g.v('Paso','int',owner=DIRECTOR,target=g.v('Director','object',obj=DIRECTOR)))])

g=ControlsGraph();begin=g.event(ACTOR,'ReceiveBeginPlay')
init=g.custom('InicializarSenales').pin('OutputDelegate','delegate',out=True)
event=g.custom('SincronizarExtraccion').pin('OutputDelegate','delegate',out=True)
prev=begin
for ev,seconds,loop in [(init,.01,False),(event,.2,True)]:
 timer=g.call('/Script/Engine.KismetSystemLibrary','K2_SetTimerDelegate',static=True).pin('Delegate','delegate').pin('Time','real',sub='float',default=str(seconds)).pin('bLooping','bool',default=str(loop).lower()).pin('bMaxOncePerFrame','bool',default='true').pin('InitialStartDelay','real',sub='float',default='0').pin('InitialStartDelayVariance','real',sub='float',default='0')
 g.w((ev,'OutputDelegate'),timer,'Delegate');g.chain(prev,timer);prev=timer
prev=g.s(init,'Inicializaciones',g.op('Add_IntInt',g.v('Inicializaciones','int'),1,'int'),'int')
for field,cls in [('Jugador',HERO),('Rehen',HOSTAGE),('Director',DIRECTOR)]:
 f=g.find(prev,cls);c,value=g.cast_after(f,(f,'ReturnValue'),cls);prev=g.s(c,field,value,'object',obj=cls)
f=g.find(prev,'/Game/ThirdPerson/Blueprints/Entrega/BP_SenalExtraccion.BP_SenalExtraccion_C')
prev=g.s(f,'SenalExtraccion',(f,'ReturnValue'),'object',obj=ACTOR)
prev=g.s(prev,'Inicializado',True,'bool')
guard=g.br(event,g.v('Inicializado','bool'))
count=g.s(guard,'Sincronizaciones',g.op('Add_IntInt',g.v('Sincronizaciones','int'),1,'int'),'int')
life=g.action_on(count,LEVEL,'ConsultarAliados').pin('ReturnValue','bool',out=True)
sequence=g.action_on(life,LEVEL,'ConsultarSecuencia').pin('ReturnValue','bool',out=True)
active=g.both((life,'ReturnValue'),(sequence,'ReturnValue'))
signal=g.v('SenalExtraccion','object',obj=ACTOR)
valid=g.br(sequence,(g.valid(*signal),'ReturnValue'))
g.action_on(valid,ACTOR,'SetActorHiddenInGame',signal,[('bNewHidden','bool',g.neg(active),None)])
graphwrite(g,'Nivel_Entrega_Evaluation')
