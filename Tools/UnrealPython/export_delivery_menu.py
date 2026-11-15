import os
import unreal
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
for path in ['/Game/Menu/Menu_Inicio','/Game/LevelMenu/Menu/Menu_Inicio']:
    asset=unreal.load_asset(path)
    if not asset:continue
    task=unreal.AssetExportTask();task.object=asset
    task.filename=os.path.join(root,'Intermediate/inspect/live',path.split('/')[2]+'_Menu_Inicio.t3d')
    task.automated=True;task.prompt=False;task.replace_identical=True
    unreal.Exporter.run_asset_export_task(task)
unreal.log('MENU_EXPORT_DONE')
