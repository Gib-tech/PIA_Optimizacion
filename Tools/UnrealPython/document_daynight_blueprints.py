"""Actualiza comentarios y exportaciones de los cinco BP de la revisión, sin reinstalar grafos."""
import unreal,os,json,re,sys
from pathlib import Path
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());R='/Game/ThirdPerson/Blueprints/Entrega/'
audit=os.path.join(root,'Intermediate/inspect/project_audit');inventory_file=os.path.join(audit,'inventory.json')
inventory=json.load(open(inventory_file,encoding='utf-8'));names=['BP_SistemasComplementarios','BP_DestruibleEntrega','BP_PlayerEntrega','BP_HUD_Entrega','BP_LuminariaPared']
sys.path.insert(0,os.path.join(root,'Tools'));from document_blueprints_es import role
def export_current(name):
 path=R+name;bp=unreal.load_asset(path);destination=os.path.join(audit,path.removeprefix('/Game/').replace('/','__')+'.t3d')
 task=unreal.AssetExportTask();task.object=bp;task.filename=destination;task.automated=True;task.prompt=False;task.replace_identical=True;assert unreal.Exporter.run_asset_export_task(task)
 data=Path(destination).read_bytes();source=data.decode('utf-16' if data.startswith(b'\xff\xfe') else 'utf-8-sig');parent=re.search(r'ParentClass=(.*)',source)
 row={'path':path,'class':'Blueprint','parent':parent.group(1).strip() if parent else None,'export':destination,'exported':True,'nodes':len(re.findall(r'Begin Object Class=.*?(?:K2Node|AnimGraphNode)',source)),'events':sorted(set(re.findall(r'(?:CustomFunctionName|MemberName)="([^"]+)"',source))),'references':sorted(set(re.findall(r'/Game/[^\s"\'\),]+',source)))}
 inventory['blueprints']=[r for r in inventory['blueprints'] if r['path']!=path]+[row]
for name in names:
 bp=unreal.load_asset(R+name);assert unreal.DeliveryBlueprintBuilder.set_property_text(bp,'BlueprintDescription',role(R+name));unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False);export_current(name)
with open(inventory_file,'w',encoding='utf-8') as f:json.dump(inventory,f,ensure_ascii=False,indent=2)
BLUEPRINT_DOCUMENTATION_FILTER={R+name for name in names}
exec(compile(Path(root,'Tools/UnrealPython/install_spanish_blueprint_comments.py').read_text(encoding='utf-8'),'install_spanish_blueprint_comments.py','exec'),globals())
# El instalador documental usa nombres globales genéricos: recargar inventario
# y lista antes de exportar los comentarios recién guardados.
inventory=json.load(open(inventory_file,encoding='utf-8'))
for name in names:export_current(name)
with open(inventory_file,'w',encoding='utf-8') as f:json.dump(inventory,f,ensure_ascii=False,indent=2)
unreal.log('DAYNIGHT_BLUEPRINT_DOCUMENTATION_EXPORTED')
