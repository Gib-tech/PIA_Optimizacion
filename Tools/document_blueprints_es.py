"""Genera fichas españolas a partir de las exportaciones reales de Unreal.

La descripción editorial explica la responsabilidad. Los eventos, variables,
referencias y recorridos se extraen del grafo, nunca del nombre del archivo.
"""
from pathlib import Path
import re,json,hashlib,collections
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'Intermediate/inspect/project_audit'
DEST=ROOT/'docs/blueprints';DEST.mkdir(parents=True,exist_ok=True)
PURPOSE={
 'BP_ThirdPersonCharacter':'Personaje base del equipo. Procesa Enhanced Input, locomoción, salto, cámaras, equipamiento y combos con montajes y AnimNotifies. BP_PlayerEntrega lo especializa para el nivel final. No duplicar aquí lógica de misión.',
 'BP_PlayerEntrega':'Personaje jugable de la entrega. Añade ventanas de impacto, control de recuperación, daño a puertas/Chaos y brazos de primera persona. BrazosFP muestrea copias de animación sin notifies: postura preparada en reposo y posición sincronizada del ataque real. EspadaFP y MartilloFP son sólo presentación; la malla y las armas originales conservan el daño real.',
 'BP_DirectorEntrega':'Coordina rescate, tres encuentros, orden aleatorio de balizas y extracción conjunta. Paso 0–3 representa avance de balizas; 4 victoria, 5 derrota del jugador y 6 derrota del rehén. El cronómetro y las señales se suspenden durante la revelación. No decide las acciones de los enemigos.',
 'BP_CombatZone':'Encuentro con dos oleadas de dos enemigos. Requiere rehén siguiendo y requisitos de progresión; mantiene lista de enemigos, fase e intermedio. La tercera instancia combina ambos tipos y solicita la revelación del último guardián. Phase 0 espera, 1 combate, 2 intermedio y 3 despejado.',
 'BP_BaseEnemy':'Enemigo orbitador y base común de combate. Expone acciones que invocan las tareas del Behavior Tree: ataque, orientación, defensa, interrupción y muerte. Valida objetivo, distancia, cono, montaje y línea de visión antes de aplicar daño. El árbol decide; el actor ejecuta.',
 'BP_ChargerEnemy':'Especialización del enemigo base para el embestidor. Usa su propio controlador, Blackboard y Behavior Tree. Cambia preparación, carrera, ataque cercano y retirada; conserva salud y sistema común de impacto.',
 'BP_IAController':'Posee al orbitador, inicializa BB_EnemyIA y ejecuta BT_EnemyIA. DetectionRadius y CombatTarget alimentan decisiones de árbol, no una cadena de decisiones en Actor Tick.',
 'BP_ChargerController':'Posee al embestidor e inicia BT_Charger con su Blackboard. Mantiene separada la arquitectura de decisiones de la del orbitador.',
 'BTService_LocatePlayer':'Servicio de percepción del orbitador. Escribe objetivo, distancias, visión y fijación del rehén en el Blackboard. El rehén rescatado puede tener prioridad; no aplica daño ni mueve al enemigo.',
 'BTService_ChargerSense':'Servicio de percepción del embestidor. Actualiza Blackboard, objetivo y condiciones de carga. Conserva la víctima comprometida mientras dura una carga para no cambiarla a mitad.',
 'BTTask_Roam':'Una acción de patrulla. Escoge destino navegable y termina o aborta para devolver el control al Behavior Tree.',
 'BTTask_Defend':'Acción corta de defensa/reposición orbital alrededor del objetivo. Usa movimiento de navegación y termina; no mantiene un bucle de decisiones fuera del árbol.',
 'BTTask_Attack':'Acerca y alinea al orbitador antes de solicitar Attack. Durante la ejecución actualiza la ventana del golpe mediante UpdateStrike. Finalización y aborto detienen movimiento y cancelan el ataque.',
 'BTTask_FaceCombatTarget':'Fija el foco del controlador en el objetivo de combate y devuelve el control al árbol. Centraliza la orientación previa sin duplicar percepción.',
 'BTTask_HitSun':'Acción de aturdimiento; el nombre histórico HitSun se conserva para no romper referencias. Interrumpe el ataque y permite recuperación temporal antes de volver al árbol.',
 'BTTask_ChargerWindup':'Anticipación visible de la embestida. Orienta al rival, comprueba visión y calcula ChargeGoal con predicción breve. Todavía no produce el golpe cercano.',
 'BTTask_ChargerCharge':'Desplazamiento rápido hacia el punto comprometido. Al llegar se detiene y solicita el montaje cercano; UpdateStrike comprueba contacto durante la animación. Abortar cancela daño pendiente y recupera velocidad.',
 'BTTask_ChargerRetreat':'Retirada local navegable respecto al objetivo de combate real. Limita longitud y duración para mantener al rival en el encuentro y evitar recorridos lejanos.',
 'BTTask_ChargerRecover':'Pausa breve de recuperación de la embestida. Finaliza/aborta para ceder la siguiente decisión al árbol.',
 'BP_Hostage':'Aliado escoltado con salud propia. Interactuar rescata o reanuda seguimiento sólo si está a salvo; percepción y movimiento pertenecen a BT_Hostage. Recibir daño actualiza salud/aviso; morir termina la misión. La apariencia usa el sobreviviente existente, con copia propia de malla/esqueleto/AnimBlueprint.',
 'BP_HostageController':'Posee al aliado e inicia BT_Hostage/BB_Hostage. El jugador nunca posee al rehén; E/RB comunica intención y el árbol decide la acción.',
 'BTService_HostageSense':'Evalúa amenazas, seguimiento y refugios locales con ruta completa. Escribe bMustFlee, bWaiting, bAccompanying, FleeLocation y Estado en el Blackboard. No sustituye el árbol con decisiones de movimiento por Tick.',
 'BTTask_HostageArrive':'Marca llegada al refugio y espera segura. El aliado requiere una nueva interacción para volver a seguir; acercarse por sí solo no lo reactiva.',
 'BTTask_ActivateBeacon':'Canalización de tres segundos mediante el árbol del aliado. Sólo continúa con baliza correcta, cercana y sin amenaza. Interrupción cancela la canalización sin conceder avance.',
 'ABP_Aliado':'AnimBlueprint de referencia del aliado original. Se conserva como fuente histórica; la entrega utiliza la especialización del rehén.',
 'ABP_Hostage':'AnimBlueprint original de la escolta con locomoción por velocidad y presentación de muerte. Se conserva para reproducir la integración; la apariencia actual usa ABP_RehenSuperviviente.',
 'ABP_RehenSuperviviente':'Copia propia del AnimBlueprint de escolta compatible con el esqueleto del sobreviviente. Lee el Pawn válido, mezcla reposo/caminar/correr y conserva muerte. Las animaciones compatibles se reutilizan sin modificar el pack original.',
 'ABP_EnemyEntrega':'Envuelve la locomoción original del pack y añade DefaultSlot para montajes de combate. Ignora root motion en las acciones de enemigo para que la navegación controle el desplazamiento.',
 'ABP_Manny':'AnimBlueprint del protagonista usado con la malla del viajero. Mezcla locomoción, salto/caída y slots de montajes. Las notificaciones gobiernan buffer de combo y recuperación; no deben volver a dispararse desde los brazos de cámara.',
 'BP_BeaconEntrega':'Baliza A/B/C con identidad fija, aproximación y estado activado. Sólo acepta el siguiente elemento de la permutación revelada y la canalización válida del rehén. Actualiza luces y comunica avance al director.',
 'BP_DestructibleDoor':'Puerta de misión. Bloqueada hasta recibir carga de progresión. Dos golpes pesados de martillo mejorado reducen 50→25→0: primero grietas geométricas, después fragmentos correspondientes y actualización de navegación.',
 'BP_DoorFragment':'Fragmento visual/físico de puerta. Aplica movimiento/rotación de rotura, ignora peones/cámara y expira para limitar coste. No cuenta como tipo distinto de destruible por cada fragmento.',
 'BP_DestruibleEntrega':'Copia funcional del destruible del equipo para caja, basurero, banca, barril, auto y fuente. Recibe impactos válidos, activa Chaos bajo demanda, dispara efecto y limpia restos. La decoración se restablece al cargar; las puertas de misión sí se guardan.',
 'BP_DestruiblePick':'Prototipo de destruible del equipo conservado como fuente. El mapa entregable usa BP_DestruibleEntrega para evitar mezclar lógica de ejemplo y daño final.',
 'BP_DeliverySave':'Datos locales de checkpoint, esquema 2 con extensiones aditivas. Sólo escalares y transforms; no guarda referencias a actores del mapa. Incluye aliados, encuentros, balizas/puertas, secuencia/tiempo e inventario.',
 'BP_DeliverySaveManager':'Valida momentos seguros, serializa checkpoint y restaura mundo/aliados/cámara. Reintenta hitos pendientes cuando termina el peligro. No sobrescribe un checkpoint seguro en mitad de una oleada, ataque, huida, canalización o desenlace.',
 'BP_DeliveryOptions':'Datos independientes de volumen. GameUserSettings conserva gráficos/pantalla; el progreso y Nuevo juego no borran esta preferencia.',
 'BP_DeliveryInterface':'Orquesta menú de pausa y opciones en ambos mapas. Conserva widget/foco de origen, detiene mundo y restaura modo de entrada/captura del ratón. P/Esc/START alternan pausa; las acciones se consumen antes del P heredado.',
 'Menu_Inicio':'Menú de entrada con Nuevo juego, Continuar validado, opciones y salida. Nuevo juego sustituye el intento; Continuar restaura un checkpoint compatible sin repetir introducción.',
 'Menu_Pausa':'Interfaz de pausa con reanudar, guardar, opciones y regreso al menú. Los botones delegan en BP_DeliveryInterface y BP_DeliverySaveManager; no crean una segunda implementación del guardado.',
 'Menu_Opciones':'Interfaz de calidad, resolución, modo de pantalla y volumen. Aplica y guarda cada selección. Vuelve a la instancia de menú/pausa de origen y mantiene la partida detenida cuando corresponde.',
 'BP_HUD_Entrega':'Presentación de misión: salud, objetivos, orden/tiempo, diálogo progresivo, señales del rehén, daño real e inventario. Lee datos de actores; no concede objetivos ni aplica daño por dibujar.',
 'BP_CinematicDirector':'Director de introducción, derrota, victoria y revelación final. Reproduce Level Sequence/audio, bloquea/restaura entrada y cámara, permite omisión y muestra la permutación real. No cambia las condiciones de victoria ni el daño.',
 'BP_GameMode_Entrega':'Selecciona Pawn y HUD de la misión entregable. El mapa tiene esta configuración propia aunque DefaultEngine conserve otro modo global como respaldo.',
 'BP_GameMode_Menu':'Modo del menú, sin generar un personaje de combate. La interfaz ofrece navegación y viaje al mapa entregable.',
 'BP_ThirdPersonGameMode':'Modo base/histórico del equipo. El nivel final usa BP_GameMode_Entrega como override; no asumir que el modo global describe la partida final.',
 'BP_GameInstance':'Persiste intención de Nuevo juego/Continuar y datos entre cambios de mapa. El disco lo gestiona el SaveManager de entrega; conserva las interfaces de guardado originales como historia.',
 'BP_SaveGame':'Esquema de guardado original del menú. Se conserva por compatibilidad de recursos antiguos; no es la fuente autoritativa del checkpoint de Nivel_Entrega.',
 'BP_SaveInterface':'Contrato del guardado original. Revisar referencias antes de retirarlo; el flujo final de misión está en los Blueprints DeliverySave.',
 'BP_Saveable':'Interfaz original para objetos guardables. No confundir su presencia con que todos los actores estén serializados; las propiedades finales se enumeran en BP_DeliverySave.',
 'BPC_Health':'Componente de salud del jugador. Disminuye la vida con el daño recibido y comunica muerte. Botiquines limitan restauración a 100; el SaveManager restaura el valor del checkpoint.',
 'BPC_E_Health':'Componente de salud enemiga. Descuenta el daño aceptado, emite E_Dead al llegar a cero y sirve como fuente de confirmación de impacto real.',
 'SaveLightAttack_AN':'Notify del montage que habilita/consume buffer del siguiente golpe ligero. Se ejecuta únicamente en la malla real del jugador.',
 'ResetState_AN':'Notify de recuperación que devuelve el estado de ataque a Nothing. Debe coordinarse con interrupción y limpieza de hitbox del personaje especializado.',
 'BPI_Enemy':'Contrato de acciones de enemigo utilizado desde tareas del árbol. Permite solicitar ataque/defensa/interrupción sin trasladar la decisión al actor.',
 'BP_SenalExtraccion':'Señal del área de extracción. Colabora con funciones/macros del Level Blueprint para mostrar si la secuencia está resuelta y ambos aliados siguen vivos.',
 'BP_BeaconLabel':'Identificación visual estable de baliza. Su letra representa lugar, no turno de la secuencia.',
 'BP_RehenIndicador':'Indicador histórico de texto flotante. El HUD actual dibuja la placa E/RB; conservarlo no implica que esté activo en el nivel final.',
 'BP_ZonaIndicador':'Indicador histórico de zona. Las alertas finales son recuadros contextuales del HUD; comprobar instancias antes de reutilizar este prototipo.',
 'BP_SistemasComplementarios':'Inventario, suministros únicos, curación, pulso y ciclo solar. BRUNO convierte tres créditos de energía durante tres segundos en un botiquín; valida alcance, saldo y trabajo activo para no consumir ni entregar dos veces. WorldSeconds, FabricationProgress y la animación del robot usan tiempo de juego y se detienen con pausa. El SaveManager conserva energía/proceso y fase; Sun en lux, Moon, Sky con captura continua y SkyMID mantienen día y noche.',
 'BP_TecnicoTemporal':'BRUNO es un robot de apoyo original fijado al suelo y a la red del recinto: no puede salir con los viajeros. ChasisRobot, CabezaRobot y AroConversion sustituyen por completo la malla humana heredada; el nombre de clase se conserva para compatibilidad. Tick sólo anima cabeza/aro/luz según bFabricating. BP_SistemasComplementarios decide conversación, energía y fabricación; este actor nunca concede recursos.',
 'DañoDes':'Campo Chaos del equipo que apoya destrucción física. Deriva de un recurso de campo del motor; no es un modelo artístico propio.',
 'BP_TargetDummy':'Actor de práctica original. Útil para depurar contactos; no sustituye pruebas contra enemigos con controlador y Behavior Tree activos.',
 'Health':'Widget original de salud del jugador. Se conserva la integración base; la misión muestra también la salud independiente del rehén desde el HUD.',
 'HealthBar':'Barra de salud de interfaz original. La ruta distingue copias del menú y recursos propios; no confundir cantidad de widgets con sistemas diferentes.',
 'Interfaz':'Interfaz de referencia del equipo, conservada bajo RecursosPropios. Las pantallas activas del nivel están en /Game/Menu y BP_HUD_Entrega.',
 'Menu_GameOver':'Pantalla original de fin de partida. El desenlace de entrega usa director, cinemática y HUD con R/Enter; esta pantalla permanece como recurso histórico.',
 'Bp_PosteLuz':'Prop del equipo que agrupa poste y luz. Revisar radio/sombras/culling al colocarlo para no duplicar luces de faroles ya integrados.',
 'Bp_Carro':'Prop de automóvil del equipo. Distinguir su malla de los otros coches/escaneos al contar diseños y documentar LOD.',
}

def read(path):
 data=path.read_bytes();return data.decode('utf-16' if data.startswith(b'\xff\xfe') else 'utf-8-sig')
def parse(source):
 lines=source.splitlines();stack=[];nodes=[];declared={};live_by_graph={}
 for line in lines:
  if 'Begin Object Class=' not in line:continue
  klass=re.search(r'Class=([^ ]+)',line);ep=re.search(r'ExportPath="[^\']*\'([^\']+)\'',line)
  if klass and ep:declared[ep.group(1)]=klass.group(1)
 for i,line in enumerate(lines):
  stripped=line.strip()
  if stripped.startswith('Begin Object'):stack.append((i,stripped))
  elif stripped=='End Object' and stack:
   start,header=stack.pop();depth=0;own=[]
   for l in lines[start+1:i]:
    s=l.strip()
    if s.startswith('Begin Object'):depth+=1
    elif s=='End Object':depth-=1
    elif depth==0:own.append(s)
   ep=re.search(r'ExportPath="[^\']*\'([^\']+)\'',header)
   references=[re.search(r'^Nodes\(\d+\)="[^\']*\'([^\']+)\'',l) for l in own if l.startswith('Nodes(')]
   if ep and references:live_by_graph[ep.group(1)]={m.group(1).rsplit('.',1)[-1] for m in references if m}
   if not any('CustomProperties Pin' in l for l in own):continue
   name=re.search(r'Name="([^"]+)"',header)
   ep=re.search(r'ExportPath="[^\']*\'([^\']+)\'',header)
   klass=re.search(r'Class=([^ ]+)',header)
   fn=next((re.search(r'MemberName="([^"]+)"',l).group(1) for l in own if l.startswith(('FunctionReference=','EventReference=')) and 'MemberName=' in l),None)
   custom=next((re.search(r'CustomFunctionName="([^"]+)"',l).group(1) for l in own if l.startswith('CustomFunctionName=')),None)
   key=next((l.split('=',1)[1] for l in own if l.startswith('InputKey=')),None)
   component=next((l.split('=',1)[1].strip('"') for l in own if l.startswith('ComponentPropertyName=')),None)
   action=next((re.search(r'/Game/[^\']*/([^/\.\']+)\.',l).group(1) for l in own if l.startswith('InputAction=') and re.search(r'/Game/[^\']*/([^/\.\']+)\.',l)),None)
   label=('Tecla '+key) if key else ('Botón '+component) if component else ('Acción '+action) if action else None
   nodes.append({'name':name.group(1),'path':ep.group(1) if ep else '', 'class':klass.group(1) if klass else declared.get(ep.group(1),'') if ep else '', 'function':custom or fn,'label':label,'lines':own})
 # ExportText puede incluir objetos huérfanos que ya no figuran en Graph.Nodes.
 # No se presentan como entradas activas ni como errores de compilación vivos.
 return [n for n in nodes if n['path'].rsplit('.',1)[0] not in live_by_graph or n['name'] in live_by_graph[n['path'].rsplit('.',1)[0]]]
def role(path):
 if path.endswith('/KallariPlayerCharacter'):
  return 'Personaje de demostración del pack Paragon Kallari, sin uso como protagonista de la misión. La revisión de UE5.6 retiró únicamente la acción ResetVR y su llamada obsoleta ResetOrientationAndPosition que impedían compilar al cargar el ejemplo. Los demás controles originales requieren sus mappings históricos y generan avisos si no están configurados; no se agregan a la misión para ocultar esos avisos.'
 if 'Nivel_Entrega' in path and ':PersistentLevel.' in path:
  return 'Blueprint del nivel entregable. Inicializa referencias de jugador, rehén, director y señal; consulta vida y secuencia mediante funciones propias y combina sus condiciones con macros antes de sincronizar la extracción. InicializarSenales y SincronizarExtraccion son eventos reales del nivel; los contadores permiten comprobar su ejecución.'
 name=path.rsplit('/',1)[-1]
 if not path.startswith(('/Game/ThirdPerson/','/Game/Menu/','/Game/LevelMenu/','/Game/Characters/')):
  return 'Recurso del proveedor o ejemplo del pack. Se documentan sus grafos y referencias para poder rastrear dependencias; su presencia no acredita uso en la misión ni autoría propia. Mantener su implementación original y especializar en carpetas del proyecto.'
 return PURPOSE.get(name,'Recurso de animación/rig del personaje. Sus grafos forman parte de la cadena de pose; consultar las entradas y dependencias extraídas abajo antes de modificarlo. No contiene por sí solo condiciones de misión.')

def main():
 data=json.loads((AUDIT/'inventory.json').read_text(encoding='utf-8'))
 index=['# Catálogo de Blueprints en español','','Fuente: exportación de todos los Blueprints de `/Game` mediante el editor. Las fichas describen responsabilidades y muestran evidencia de conexiones; no sustituyen las pruebas de juego. Los assets de ejemplo/proveedor se distinguen por ruta.','',f"Cobertura: **{len(data['blueprints'])} Blueprints**, incluidos AnimBlueprints, widgets, interfaces y Control Rigs. Los Behavior Trees/Blackboards se explican en la guía de flujo.",'']
 manifest=[]
 for row in sorted(data['blueprints'],key=lambda x:x['path']):
  path=row['path'];name=path.rsplit('/',1)[-1];filename=re.sub(r'[:<>"|?*]','__',path.removeprefix('/Game/').replace('/','__'))+'.md'
  source=read(Path(row['export']));nodes=parse(source);description=role(path)
  contents=[f'# {name}','','[Volver al catálogo](../CATALOGO_BLUEPRINTS.md)','',f'**Ruta de Unreal:** `{path}`. **Tipo:** {row["class"]}.',f'**Clase padre:** `{row["parent"]}`.','',description,'','## Entradas y responsabilidades del grafo','']
  entries=[n for n in nodes if any(t in n['class'] for t in ['K2Node_Event','K2Node_CustomEvent','K2Node_FunctionEntry','K2Node_ComponentBoundEvent','K2Node_InputKey','K2Node_InputAction','K2Node_InputAxisEvent','K2Node_EnhancedInputAction']) and 'PersistentFrame' not in n['class']]
  seen=set()
  for n in entries:
   graph=n['path'].split(':')[-1].rsplit('.',1)[0]
   label=n.get('label') or n['function'] or graph
   if label.startswith(('ExecuteUbergraph','BndEvt__','InpActEvt_')):continue
   key=(graph,label)
   if key in seen:continue
   seen.add(key)
   outputs=[]
   for line in n['lines']:
    if 'PinType.PinCategory="exec"' in line and 'Direction="EGPD_Output"' in line:
     m=re.search(r'LinkedTo=\(([^)]*)\)',line)
     if m:outputs.append((re.search(r'PinName="([^"]+)"',line).group(1),re.findall(r'(\w+) [A-F0-9]{32}',m.group(1))))
   byname={x['name']:x for x in nodes if x['path'].rsplit('.',1)[0]==n['path'].rsplit('.',1)[0]}
   routes=[]
   for output,links in outputs:
    steps=[];queue=links[:];visited=set()
    while queue and len(steps)<12:
     nextname=queue.pop(0)
     if nextname in visited:continue
     visited.add(nextname);target=byname.get(nextname)
     if not target:continue
     variable=next((re.search(r'MemberName="([^"]+)"',l).group(1) for l in target['lines'] if l.startswith('VariableReference=') and 'MemberName=' in l),None)
     op=target['function'] or ('Asignar '+variable if variable and 'VariableSet' in target['class'] else 'Condición' if 'IfThenElse' in target['class'] else 'Secuencia' if 'ExecutionSequence' in target['class'] else target['class'].rsplit('.',1)[-1])
     steps.append(op)
     for line in target['lines']:
      if 'PinType.PinCategory="exec"' in line and 'Direction="EGPD_Output"' in line:
       m=re.search(r'LinkedTo=\(([^)]*)\)',line)
       if m:queue+=re.findall(r'(\w+) [A-F0-9]{32}',m.group(1))
    if steps:routes.append('desde `'+output+'`: '+', '.join('`'+s+'`' for s in steps))
   contents.append(f'- **`{label}`** en `{graph}`. '+('Operaciones alcanzables '+ '; '.join(routes)+'. Las condiciones del grafo deciden qué rama se ejecuta.' if routes else 'Entrada/contrato sin una continuación de ejecución serializada en esta exportación; puede ser un grafo de pose, herencia o configuración.'))
  if not seen:contents.append('Este Blueprint contiene datos, configuración o un rig. No presenta una entrada de ejecución K2 propia que describir como lógica de gameplay.')
  variables=[]
  for match in re.finditer(r'NewVariables\(\d+\)=\(VarName="([^"]+)"([^\r\n]+)',source):
   kind=re.search(r'PinCategory="([^"]+)"',match.group(2))
   variables.append((match.group(1),kind.group(1) if kind else 'según tipo del editor'))
  if variables:
   contents+=['','## Campos propios declarados','', 'Los identificadores se conservan como aparecen en Unreal para que el equipo pueda buscarlos. El padre puede aportar otros campos heredados; no renombrar contratos sin actualizar consumidores y archivos guardados.','']
   for variable,kind in variables:contents.append(f'- `{variable}` — tipo `{kind}`.')
  operations=collections.Counter(n['function'] for n in nodes if n['function'] and not n['function'].startswith(('ExecuteUbergraph','InpActEvt_','BndEvt__')))
  contents+=['','## Operaciones y dependencias verificadas','',f'La exportación contiene {len(nodes)} nodos con pines. Funciones referenciadas: '+', '.join('`'+k+'`' for k in sorted(operations))+'.','']
  game_refs=sorted({p.split(':')[0] for p in re.findall(r"/Game/[^\s\"'\),]+",source) if not p.startswith(path)})
  contents.extend('- `'+p+'`' for p in game_refs)
  contents+=['','## Cómo modificarlo sin romper el flujo','','1. Revisar primero el padre y los consumidores de sus eventos/variables. Los nombres usados por notifies, Blackboard y guardado son contratos.','2. Cambiar en la copia propia del proyecto; no sobrescribir packs externos. Si existe un generador en `Tools/UnrealPython`, actualizarlo junto con el asset para conservar reproducibilidad.','3. Compilar el Blueprint y sus dependencias, guardar y ejecutar el escenario correspondiente de la guía de pruebas. Un grafo compilado no acredita por sí solo comportamiento correcto.','4. Registrar evidencia en `docs/validation` y regenerar este catálogo después de exportar.','',f'**Huella de exportación:** `{hashlib.sha256(source.encode()).hexdigest()}`.']
  (DEST/filename).write_text('\n'.join(contents)+'\n',encoding='utf-8')
  index.append(f'- [{path}](blueprints/{filename}) — {description.split(". ")[0]}.')
  manifest.append({'path':path,'doc':filename,'description':description,'export_sha256':hashlib.sha256(source.encode()).hexdigest(),'nodes':len(nodes)})
 (ROOT/'docs/CATALOGO_BLUEPRINTS.md').write_text('\n'.join(index)+'\n',encoding='utf-8')
 (AUDIT/'documentation_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print('FICHAS_BLUEPRINTS',len(manifest))
if __name__=='__main__':main()
