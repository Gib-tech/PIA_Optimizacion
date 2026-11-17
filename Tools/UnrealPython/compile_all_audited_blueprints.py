"""Compila los 101 BP auditados, también dependencias de packs y el nivel."""
import unreal,os,json,re,sys
from pathlib import Path
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=Path(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()));sys.path.insert(0,str(root/'Tools'))
from document_blueprints_es import parse,read
inventory=json.loads((root/'Intermediate/inspect/project_audit/inventory.json').read_text(encoding='utf-8'))
items=[]
for row in inventory['blueprints']:
 bp=unreal.find_object(None,row['path']) if row['class']=='LevelScriptBlueprint' else unreal.load_asset(row['path']);assert bp,row['path'];items.append((row,bp))
for _ in range(2):
 for row,bp in items:unreal.BlueprintEditorLibrary.compile_blueprint(bp)
out=root/'Intermediate/inspect/compile_all';out.mkdir(parents=True,exist_ok=True);report=[]
for i,(row,bp) in enumerate(items):
 try:status=str(bp.get_editor_property('status'))
 except Exception:status='Estado no expuesto; se revisan errores de nodos y cook.'
 if row['class']=='LevelScriptBlueprint':unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
 elif row['path'].startswith(('/Game/ThirdPerson/','/Game/Menu/','/Game/LevelMenu/')):unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=True)
 task=unreal.AssetExportTask();task.object=bp;task.filename=str(out/(str(i)+'.t3d'));task.automated=True;task.prompt=False;task.replace_identical=True;assert unreal.Exporter.run_asset_export_task(task)
 nodes=parse(read(Path(task.filename)));errors=[];warnings=[]
 for n in nodes:
  if 'bHasCompilerMessage=True' not in n['lines']:continue
  msg=next((l for l in n['lines'] if l.startswith('ErrorMsg=')),None)
  if not msg:continue
  (errors if 'ErrorType=1' in n['lines'] else warnings).append({'node':n['path'],'message':msg})
 report.append({'asset':bp.get_path_name(),'status':status,'errors':errors,'warnings':warnings})
result={'count':len(report),'passed':not any(x['errors'] for x in report),'blueprints':report,'scope':'Compilación en editor de todos los BP exportados; el cook del paquete es una comprobación adicional.'}
(root/'docs/validation/compilacion-completa-2026-11-17.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
assert result['passed'],[x['asset'] for x in report if x['errors']]
unreal.log('ALL_AUDITED_BLUEPRINTS_COMPILED '+str(len(report)))
