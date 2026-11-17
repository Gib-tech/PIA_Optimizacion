"""Añade documentación a entradas/funciones de Blueprints propios, sin recablear."""
import unreal,os,json,sys,re
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());sys.path.insert(0,os.path.join(root,'Tools'))
from document_blueprints_es import parse,read,role
from pathlib import Path
inventory=json.load(open(os.path.join(root,'Intermediate/inspect/project_audit/inventory.json'),encoding='utf-8'))
translated={'ReceiveBeginPlay':'Inicio del actor: inicializa referencias y estado.',
 'ReceiveTick':'Actualización durante la partida. Respetar las guardas de estado y las responsabilidades del sistema.',
 'ReceiveAnyDamage':'Recepción de daño: validar origen/estado antes de modificar salud.',
 'ReceiveDrawHUD':'Dibuja información; no debe conceder progreso ni producir daño.',
 'BlueprintUpdateAnimation':'Actualiza parámetros de pose desde un Pawn válido.',
 'ReceiveExecuteAI':'Entrada de una acción decidida por el Behavior Tree.',
 'ReceiveTickAI':'Actualización de la tarea activa; no sustituye las decisiones del árbol.',
 'ReceiveAbortAI':'Interrupción: cancelar movimiento/impacto pendiente y devolver control al árbol.',
 'ReceiveTickAI':'Actualiza la acción o percepción del árbol según el tipo de Blueprint.',
 'Construct':'Construcción de la pantalla: estado y foco de entrada.',
 'UsarBotiquin':'Consume una unidad sólo si puede restaurar vida; máximo 100.',
 'DispararPulso':'Valida carga/recuperación y aplica daño sólo al enemigo visible alcanzado.',
 'HablarConTecnico':'Dentro del alcance: diálogo y conversión validada de 3 créditos en energía. Un trabajo activo no vuelve a consumir; entrega un kit al terminar 3 segundos.',
 'SaveCheckpoint':'Guardar únicamente en una situación segura; no sobrescribir con combate parcial.',
 'RestoreCheckpoint':'Validar esquema y reconstruir estado sin volver a conceder recompensas.',
 'FinishCinema':'Finalización común de escena y omisión: restituir cámara, visibilidad y entrada.'}
report=[]
for row in inventory['blueprints']:
 path=row['path']
 if globals().get('BLUEPRINT_DOCUMENTATION_FILTER') and path not in BLUEPRINT_DOCUMENTATION_FILTER:continue
 if not path.startswith(('/Game/ThirdPerson/','/Game/Menu/','/Game/LevelMenu/')):continue
 bp=unreal.find_object(None,path) if row['class']=='LevelScriptBlueprint' else unreal.load_asset(path);description=role(path)
 assert unreal.DeliveryBlueprintBuilder.set_property_text(bp,'BlueprintDescription',description)
 count=0
 for n in parse(read(Path(row['export']))):
  if not any(k in n['class'] for k in ['K2Node_Event','K2Node_CustomEvent','K2Node_FunctionEntry','K2Node_ComponentBoundEvent','K2Node_InputKey','K2Node_InputAction','K2Node_InputAxisEvent','K2Node_EnhancedInputAction']):continue
  if not n['path'] or any(k in n['path'] for k in ['ExecuteUbergraph','InpActEvt_','BndEvt__']):continue
  obj=unreal.find_object(None,n['path'])
  if not obj:continue
  label=n.get('label') or n['function'] or n['path'].split(':')[-1].split('.')[0]
  note=translated.get(label,'Entrada/función «'+label+'». Consultar su contrato y consumidores en la ficha del catálogo.')
  comment=note+'\n'+description[:380]+'\nDocumentación: docs/LEEME_EQUIPO.md y docs/CATALOGO_BLUEPRINTS.md.'
  assert unreal.DeliveryBlueprintBuilder.set_property_text(obj,'NodeComment',comment)
  # Disponible al inspeccionar el nodo; no cubre otros grafos con burbujas largas.
  unreal.DeliveryBlueprintBuilder.set_property_text(obj,'bCommentBubbleVisible','False');count+=1
 if row['class']=='LevelScriptBlueprint':unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
 else:unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 report.append({'blueprint':path,'entradas_comentadas':count,'descripcion_espanola':True})
report_file=os.path.join(root,'docs/validation/documentacion-blueprints.json')
if globals().get('BLUEPRINT_DOCUMENTATION_FILTER') and os.path.isfile(report_file):
 previous=json.load(open(report_file,encoding='utf-8'));changed={r['blueprint'] for r in report};report=[r for r in previous if r['blueprint'] not in changed]+report
with open(report_file,'w',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
unreal.log('SPANISH_BLUEPRINT_DOCUMENTATION '+str(len(report)))
