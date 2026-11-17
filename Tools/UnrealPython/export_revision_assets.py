"""Actualiza sólo las fichas cuyas fuentes cambiaron desde la auditoría completa."""
import unreal,os,json
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());folder=os.path.join(root,'Intermediate/inspect/project_audit');inventory=json.load(open(os.path.join(folder,'inventory.json'),encoding='utf-8'))
for row in inventory['blueprints']:
 if row['path'].rsplit('/',1)[-1] not in ['BP_SistemasComplementarios','BP_TecnicoTemporal','BP_HUD_Entrega','BP_DeliverySaveManager','BP_DeliverySave','BP_CinematicDirector']:continue
 bp=unreal.load_asset(row['path']);t=unreal.AssetExportTask();t.object=bp;t.filename=row['export'];t.automated=True;t.prompt=False;t.replace_identical=True;assert unreal.Exporter.run_asset_export_task(t)
unreal.log('REVISION_ASSETS_EXPORTED')
