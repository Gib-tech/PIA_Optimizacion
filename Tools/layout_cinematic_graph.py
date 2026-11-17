"""Calcula posiciones exclusivamente editoriales desde el grafo real exportado.

No genera nodos de ejecución, no reconecta pines y no usa el generador de lógica.
"""
from pathlib import Path
import re,json,hashlib,collections
from document_blueprints_es import parse,read
ROOT=Path(__file__).resolve().parents[1];FOLDER=ROOT/'Intermediate/inspect/robot-sky'
def logic(source):
 return {n['name']:{'class':n['class'],'lines':[l for l in n['lines'] if not l.startswith(('NodePosX=','NodePosY=','NodeComment=','bCommentBubble','AdvancedPinDisplay='))]} for n in parse(source) if ':EventGraph.' in n['path']}
def fingerprint(source):return hashlib.sha256(json.dumps(logic(source),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def plan():
 source=read(FOLDER/'cinema-before.t3d');nodes={n['name']:n for n in parse(source) if ':EventGraph.' in n['path']};pins={};out=collections.defaultdict(list);data=collections.defaultdict(list)
 for name,n in nodes.items():
  for line in n['lines']:
   if not line.startswith('CustomProperties Pin'):continue
   pid=re.search(r'PinId=([A-F0-9]+)',line).group(1);cat=re.search(r'PinType.PinCategory="([^"]+)"',line).group(1);links=re.search(r'LinkedTo=\(([^)]*)\)',line)
   pins[name,pid]={'cat':cat,'out':'Direction="EGPD_Output"' in line,'links':re.findall(r'(\w+) ([A-F0-9]{32})',links.group(1)) if links else []}
 for (name,pid),p in pins.items():
  if not p['out']:continue
  for target,_ in p['links']:
   if target in nodes:(out if p['cat']=='exec' else data)[name].append(target)
 roots=[n for n in nodes if any(x in nodes[n]['class'] for x in ['K2Node_Event','K2Node_CustomEvent','K2Node_InputKey'])]
 control={n for n,pid in pins if pins[n,pid]['cat']=='exec'}
 distances={}
 for root in roots:
  q=collections.deque([(root,0)]);seen=set()
  while q:
   n,d=q.popleft()
   if n in seen:continue
   seen.add(n);distances.setdefault(n,[]).append((d,roots.index(root),root))
   q.extend((t,d+1) for t in out[n])
 owner={n:min(ds)[2] for n,ds in distances.items()};pure_targets={}
 for name in nodes.keys()-control:
  q=collections.deque([(name,0)]);seen=set();cons=[]
  while q:
   n,d=q.popleft()
   if n in seen:continue
   seen.add(n)
   if n in control:
    if n in owner:cons.append((d,roots.index(owner[n]),int(n.rsplit('_',1)[-1]),n))
    continue
   q.extend((t,d+1) for t in data[n])
  if cons:
   target=min(cons)[3];owner[name]=owner[target];pure_targets[name]=target
  else:owner[name]=roots[0];pure_targets[name]=roots[0]
 titles={'ReceiveBeginPlay':'01 · ARRANQUE / intención de introducción','ReceiveTick':'02 · ACTUALIZACIÓN / referencias y fin por tiempo','StartIntro':'03 · SOLICITAR INTRODUCCIÓN','StartRevelation':'04 · REVELACIÓN / secuencia real del guardián','StartOutcome':'05 · DESENLACE / prioridad e interrupción','PlayCinema':'06 · REPRODUCCIÓN / bloquear, cámara, audio y secuencia','Tecla SpaceBar':'07 · OMITIR / teclado','Tecla Gamepad_FaceButton_Bottom':'08 · OMITIR / mando','FinishCinema':'09 · FINALIZAR / restaurar y continuar'}
 positions={};comments=[];base_y=0
 for root in roots:
  members=[n for n in nodes if owner.get(n)==root];execution=[n for n in members if n in control]
  # Recorrido por conexiones de ejecución; conserva las bifurcaciones contiguas.
  ordered=[];seen=set()
  def visit(n):
   if n in seen or n not in members:return
   seen.add(n);ordered.append(n)
   for child in out[n]:visit(child)
  visit(root)
  for n in execution:visit(n)
  pure_by=collections.defaultdict(list)
  for n in members:
   if n not in control:pure_by[pure_targets.get(n,root)].append(n)
  row_y=base_y+130;max_x=0
  for start in range(0,len(ordered),6):
   row=ordered[start:start+6];row_h=400
   for column,n in enumerate(row):
    x=160+column*650;positions[n]=[x,row_y];max_x=max(max_x,x+540)
    py=row_y+330
    # Datos propios debajo del nodo que los consume, separados del cable blanco.
    deps=pure_by[n]
    for dep in sorted(deps,key=lambda d:int(d.rsplit('_',1)[-1]),reverse=True):
     positions[dep]=[x-15,py]
     pin_count=sum(1 for line in nodes[dep]['lines'] if line.startswith('CustomProperties Pin') and 'bHidden=True' not in line)
     py+=max(100,70+pin_count*24)
    row_h=max(row_h,py-row_y+90)
   comments.append({'name':'LayoutFila_'+str(len(comments)),'title':'Lectura de izquierda a derecha · tramo '+str(start//6+1),'position':[90,row_y-60],'size':[max_x, row_h+70],'color':[.025,.045,.065,.5]})
   row_y+=row_h+160
  label=nodes[root]['function'] or nodes[root]['label'];comments.append({'name':'LayoutSeccion_'+str(roots.index(root)),'title':titles.get(label,label),'position':[0,base_y],'size':[max_x+200,row_y-base_y],'color':[.035,.12,.16,.45]})
  base_y=row_y+250
 assert positions.keys()==nodes.keys(),nodes.keys()-positions.keys()
 result={'before_sha256':fingerprint(source),'node_count':len(nodes),'positions':positions,'comments':comments}
 (FOLDER/'cinema-layout.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print('CINEMATIC_LAYOUT_PLAN',len(nodes),'nodes',len(comments),'comments')
if __name__=='__main__':plan()
