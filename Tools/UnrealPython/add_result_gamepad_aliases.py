"""Enlaces de resultado que comparten las mismas ramas de teclado."""
def add_result_aliases(g):
 for source_key,pad_key in [('R','Gamepad_FaceButton_Bottom'),('Enter','Gamepad_DPad_Down')]:
  source=next(n for n in g.nodes if 'InputKey='+source_key in n.props)
  alias=g.key(pad_key)
  for name,pid in list(source.pins['Pressed']['links']):
   node=next(n for n in g.nodes if n.name==name);pin=next(p for p in node.pins.values() if p['id']==pid)
   g.wire(alias,'Pressed',node,pin['name'])
