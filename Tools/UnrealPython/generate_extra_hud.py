"""Inventario y señales de suministros con el lenguaje visual del HUD existente."""
from generate_delivery_controls import ControlsGraph,split_exec
from generate_progression_graphs import MATH,GS,ACTOR,HERO
from generate_rubric_systems import EXTRAS

def add_extra_hud(g,draw,width,height,scale,rect,text):
 g.__class__=ControlsGraph
 extras=g.v('CachedExtras','object',obj=EXTRAS)
 def v(name,kind='int'):return g.v(name,kind,owner=EXTRAS,target=extras)
 def mul(a,b):return g.op('Multiply_DoubleDouble',a,b)
 def cat(a,b):return g.c('/Script/Engine.KismetStringLibrary','Concat_StrStr',[('A','string',a),('B','string',b)],cat='string')
 def count(title,name):return cat(title,g.c('/Script/Engine.KismetStringLibrary','Conv_IntToString',[('InInt','int',v(name))],cat='string'))
 seq=split_exec(g,draw);ready=g.br(seq,(g.valid(*extras),'ReturnValue'),'then_1')
 output=g.node('K2Node_ExecutionSequence').pin('execute')
 for i in range(8):output.pin('then_'+str(i),out=True)
 g.chain(ready,output)
 inventory=g.br(output,v('InventoryOpen','bool'),'then_0')
 ix=g.op('Subtract_DoubleDouble',mul(width,.5),mul(456,scale));iy=g.op('Subtract_DoubleDouble',mul(height,.5),mul(172,scale))
 def atx(x):return g.op('Add_DoubleDouble',ix,mul(x,scale))
 def aty(y):return g.op('Add_DoubleDouble',iy,mul(y,scale))
 def panel(prev,x,y,w,h,col):return rect(prev,atx(x),aty(y),mul(w,scale),mul(h,scale),col)
 def label(prev,value,x,y,size=1,col='(R=.88,G=.94,B=.97,A=1)'):
  font='F_InventarioNumero' if size>2 else 'F_InventarioTexto'
  n=g.call('/Script/Engine.HUD','DrawText').pin('Text','string').pin('TextColor','struct',obj='/Script/CoreUObject.LinearColor',default=col).pin('Font','object',obj='/Script/Engine.Font',default_obj='/Game/ThirdPerson/Blueprints/Entrega/Inventario/'+font+'.'+font).pin('bScalePosition','bool',default='false')
  g.w(value,n,'Text')
  for pin,val in [('ScreenX',atx(x)),('ScreenY',aty(y)),('Scale',mul(size*(.375 if size>2 else .75),scale))]:n.pin(pin,'real',sub='float');g.w(val,n,pin)
  g.chain(prev,n);return n
 def icon(prev,name,x,y,size=142,screen=False):
  n=g.call('/Script/Engine.HUD','DrawTexture').pin('Texture','object',obj='/Script/Engine.Texture',default_obj='/Game/ThirdPerson/Blueprints/Entrega/Inventario/T_Inv_'+name+'.T_Inv_'+name).pin('TintColor','struct',obj='/Script/CoreUObject.LinearColor',default='(R=1,G=1,B=1,A=1)').pin('BlendMode','byte',obj='/Script/Engine.EBlendMode',default='BLEND_Translucent').pin('bScalePosition','bool',default='false').pin('RotPivot','struct',obj='/Script/CoreUObject.Vector2D',default='(X=0,Y=0)')
  for pin,val in [('ScreenX',mul(x,scale) if screen else atx(x)),('ScreenY',mul(y,scale) if screen else aty(y)),('ScreenW',mul(size,scale)),('ScreenH',mul(size,scale)),('TextureU',0),('TextureV',0),('TextureUWidth',1),('TextureVHeight',1),('Scale',1),('Rotation',0)]:n.pin(pin,'real',sub='float');g.w(val,n,pin)
  g.chain(prev,n);return n
 # Panel de equipo: tres recursos reales, sin capacidades ni estadísticas ficticias.
 prev=rect(inventory,0,0,width,height,'(R=.002,G=.008,B=.013,A=.35)')
 prev=panel(prev,6,8,912,344,'(R=0,G=0,B=0,A=.6)')
 prev=panel(prev,0,0,912,344,'(R=.009,G=.022,B=.032,A=.985)')
 prev=panel(prev,0,0,912,3,'(R=.12,G=.78,B=.95,A=1)')
 prev=label(prev,'EQUIPO DE RESCATE',24,19,1.7)
 prev=label(prev,'INVENTARIO  /  VIAJERO TEMPORAL',25,49,.68,'(R=.3,G=.68,B=.78,A=1)')
 prev=panel(prev,758,21,130,29,'(R=.04,G=.11,B=.14,A=1)')
 prev=label(prev,'I / SELECT   CERRAR',768,29,.69)
 cards=[('BOTIQUINES','Botiquines','BotiquinTemporal','(R=.28,G=.82,B=.62,A=1)','Recupera hasta 35 de vida.','H / LB   UTILIZAR'),('CARGAS DE PULSO','Cargas','CeldaTemporal','(R=.16,G=.73,B=1,A=1)','Apunta a la mira · 8 m · 1 celda.','CLIC CENTRAL / RT   DISPARAR'),('CRÉDITOS DE ENERGÍA','Creditos','CreditoCronal','(R=1,G=.64,B=.22,A=1)','3 créditos → energía → 1 botiquín.','E / RB   CONVERTIR CON BRUNO')]
 for i,(title,field,img,color,desc,hint) in enumerate(cards):
  x=24+i*292
  prev=panel(prev,x,80,280,207,'(R=.025,G=.048,B=.06,A=1)')
  prev=panel(prev,x,80,280,2,color)
  prev=label(prev,title,x+14,94,.78,color)
  amount=g.c('/Script/Engine.KismetStringLibrary','Conv_IntToString',[('InInt','int',v(field))],cat='string')
  prev=label(prev,cat('x',amount),x+167,128,3.2)
  available=g.c(MATH,'SelectInt',[('A','int',1),('B','int',0),('bPickA','bool',g.cmp('Greater_IntInt',v(field),0,'int'))],cat='int')
  status=g.node('K2Node_Select',['NumOptionPins=2','IndexPinType=(PinCategory="int")']).pin('Index','int').pin('ReturnValue','string',out=True).pin('Option 0','string',default='AGOTADO').pin('Option 1','string',default='DISPONIBLE');g.w(available,status,'Index')
  prev=label(prev,(status,'ReturnValue'),x+161,205,.6,'(R=.45,G=.6,B=.66,A=1)')
  prev=label(prev,desc,x+14,236,.69)
  prev=panel(prev,x+12,261,256,1,'(R=.09,G=.16,B=.19,A=1)')
  prev=label(prev,hint,x+14,269,.68,color)
 prev=panel(prev,24,303,864,1,'(R=.07,G=.16,B=.19,A=1)')
 prev=label(prev,'MESA: APUNTAR + E / RB PARA RECOGER',25,317,.67,'(R=.8,G=.63,B=.35,A=1)')
 prev=label(prev,'EL MUNDO SIGUE ACTIVO · P / START: PAUSA',584,317,.61,'(R=.45,G=.6,B=.66,A=1)')
 # Dibujar iconos después de fondos/texto conserva sus capas en Canvas.
 for i,card in enumerate(cards):prev=icon(prev,card[2],31+i*292,113,136)
 now=g.c(GS,'GetTimeSeconds');notice=g.br(output,g.cmp('Greater_DoubleDouble',v('NoticeUntil','real'),now),'then_1')
 prev=rect(notice,mul(20,scale),mul(183,scale),mul(760,scale),mul(32,scale),'(R=.01,G=.05,B=.08,A=.92)')
 text(prev,v('Notice','string'),mul(30,scale),mul(192,scale),.92,'(R=.4,G=.9,B=1,A=1)')
 line=g.br(output,g.neg(v('InventoryOpen','bool')),'then_2')
 for i,(_,field,img,color,_,_) in enumerate(cards):
  row=220+i*36
  line=rect(line,mul(22,scale),mul(row,scale),mul(82,scale),mul(33,scale),'(R=.008,G=.022,B=.032,A=.94)')
  line=icon(line,img,24,row,32,screen=True)
  line=text(line,count('x',field),mul(59,scale),mul(row+6,scale),1.05,color)
 phase=g.node('K2Node_Select',['NumOptionPins=4','IndexPinType=(PinCategory="int")']).pin('Index','int').pin('ReturnValue','string',out=True)
 for i,name in enumerate(['Día','Atardecer','Noche','Amanecer']):phase.pin('Option '+str(i),'string',default=name)
 g.w(v('FaseSolar'),phase,'Index')
 line=rect(line,mul(22,scale),mul(330,scale),mul(116,scale),mul(49,scale),'(R=.008,G=.022,B=.032,A=.92)')
 line=text(line,(phase,'ReturnValue'),mul(29,scale),mul(334,scale),1.05,'(R=1,G=.85,B=.62,A=1)')
 text(line,'[I] Equipo',mul(29,scale),mul(355,scale),1.0)
 def prompt_label(prev,value):
  # Una sola posición para las acciones contextuales; el centro queda libre.
  bg=rect(prev,mul(116,scale),mul(220,scale),mul(510,scale),mul(35,scale),'(R=.008,G=.022,B=.032,A=.96)')
  return text(bg,value,mul(128,scale),mul(228,scale),1.15)
 tech=g.v('Tecnico','object',owner=EXTRAS,target=extras,obj=ACTOR)
 hero=g.v('Hero','object',owner=EXTRAS,target=extras,obj=HERO)
 hint=g.br(output,(g.valid(*tech),'ReturnValue'),'then_3')
 hint=g.br(hint,(g.valid(*hero),'ReturnValue'));hint=g.br(hint,g.neg(v('InventoryOpen','bool')));hint=g.br(hint,g.cmp('EqualEqual_IntInt',v('ObjetoEnMira'),0,'int'))
 near=g.br(hint,v('bRobotEnMira','bool'))
 prompt_label(near,'[E / RB]  Hablar con BRUNO')
 pickup=g.br(output,g.cmp('Greater_IntInt',v('ObjetoEnMira'),0,'int'),'then_6');pickup=g.br(pickup,g.neg(v('InventoryOpen','bool')))
 prompt=g.node('K2Node_Select',['NumOptionPins=4','IndexPinType=(PinCategory="int")']).pin('Index','int').pin('ReturnValue','string',out=True)
 for i,value in enumerate(['','BOTIQUÍN  [E / RB]  Recoger +1','CELDAS DE PULSO  [E / RB]  Recoger +3','CRÉDITOS DE ENERGÍA  [E / RB]  Recoger +3']):prompt.pin('Option '+str(i),'string',default=value)
 g.w(v('ObjetoEnMira'),prompt,'Index');prompt_label(pickup,(prompt,'ReturnValue'))
 cls='/Game/ThirdPerson/Blueprints/Entrega/BP_DestruibleEntrega.BP_DestruibleEntrega_C';obj=g.v('DestruibleEnMira','object',owner=EXTRAS,target=extras,obj=cls)
 destructible=g.br(output,(g.valid(*obj),'ReturnValue'),'then_7');destructible=g.br(destructible,g.neg(v('InventoryOpen','bool')));destructible=g.br(destructible,g.neg(g.v('bBroken','bool',owner=cls,target=obj)))
 message=cat(cat('DESTRUIBLE: ',g.v('NombreDestruible','string',owner=cls,target=obj)),'  ·  Ligero / pesado / pulso')
 destructible=g.br(destructible,g.neg(v('bRobotEnMira','bool')))
 destructible=g.br(destructible,g.cmp('EqualEqual_IntInt',v('ObjetoEnMira'),0,'int'))
 prompt_label(destructible,message)
 manufacturing=g.br(output,v('bFabricating','bool'),'then_5')
 progress=g.c(MATH,'FClamp',[('Value','real',g.op('Divide_DoubleDouble',v('FabricationProgress','real'),3)),('Min','real',0),('Max','real',1)])
 fab_x=g.op('Subtract_DoubleDouble',width,mul(440,scale))
 prev=rect(manufacturing,fab_x,mul(145,scale),mul(420,scale),mul(63,scale),'(R=.005,G=.02,B=.03,A=.97)')
 prev=text(prev,'BRUNO · FABRICANDO BOTIQUÍN',g.op('Add_DoubleDouble',fab_x,mul(12,scale)),mul(153,scale),.92,'(R=.25,G=.9,B=1,A=1)')
 prev=text(prev,cat(count('ENERGÍA ','RobotEnergy'),' / 3'),g.op('Add_DoubleDouble',fab_x,mul(12,scale)),mul(174,scale),.78)
 prev=rect(prev,g.op('Add_DoubleDouble',fab_x,mul(12,scale)),mul(197,scale),mul(396,scale),mul(5,scale),'(R=.04,G=.1,B=.13,A=1)')
 rect(prev,g.op('Add_DoubleDouble',fab_x,mul(12,scale)),mul(197,scale),mul(mul(396,progress),scale),mul(5,scale),'(R=.15,G=.8,B=1,A=1)')
 aim=g.br(output,(g.valid(*hero),'ReturnValue'),'then_4')
 aim=g.br(aim,g.neg(v('InventoryOpen','bool')))
 x=mul(width,.5);y=mul(height,.5)
 prev=rect(aim,g.op('Subtract_DoubleDouble',x,5),g.op('Subtract_DoubleDouble',y,1),10,2,'(R=.6,G=.9,B=1,A=.7)')
 rect(prev,g.op('Subtract_DoubleDouble',x,1),g.op('Subtract_DoubleDouble',y,5),2,10,'(R=.6,G=.9,B=1,A=.7)')
