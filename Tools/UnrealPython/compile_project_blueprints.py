"""Recompila dependencias propias y comprueba el estado exportado de cada BP."""
import unreal,os,json,re
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
registry=unreal.AssetRegistryHelpers.get_asset_registry();items=[]
for path in ['/Game/ThirdPerson','/Game/Menu','/Game/LevelMenu','/Game/Characters/Mannequins/Animations']:
 for row in registry.get_assets_by_path(path,recursive=True):
  if str(row.asset_class_path.asset_name) in ['Blueprint','AnimBlueprint','WidgetBlueprint']:
   bp=row.get_asset();items.append(bp)
for _ in range(2):
 for bp in items:unreal.BlueprintEditorLibrary.compile_blueprint(bp)
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());out=os.path.join(root,'Intermediate/inspect/compile');os.makedirs(out,exist_ok=True)
report=[]
for bp in items:
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 task=unreal.AssetExportTask();task.object=bp;task.filename=os.path.join(out,bp.get_name()+'.t3d');task.automated=True;task.prompt=False;task.replace_identical=True
 assert unreal.Exporter.run_asset_export_task(task)
 data=open(task.filename,'rb').read();source=data.decode('utf-16' if data.startswith(b'\xff\xfe') else 'utf-8-sig')
 status=re.search(r'^   Status=(.*)',source,re.M)
 report.append({'path':bp.get_path_name(),'status':status.group(1).strip() if status else 'sin campo serializado','errors':re.findall(r'ErrorMsg="([^"]+)"',source)})
with open(os.path.join(root,'docs/validation/blueprints-compilacion.json'),'w',encoding='utf-8') as f:json.dump(report,f,indent=2,ensure_ascii=False)
failed=[r for r in report if r['status']=='BS_Error']
assert not failed,failed
unreal.log('BLUEPRINTS_COMPILED '+str(len(report)))
