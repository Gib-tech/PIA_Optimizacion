import os
import unreal
project = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
for name in ['BP_DirectorEntrega','BP_HUD_Entrega']:
    bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/'+name)
    unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    task=unreal.AssetExportTask()
    task.object=bp
    task.filename=os.path.join(project,'Intermediate','inspect','live',name+'.t3d')
    task.automated=True
    task.prompt=False
    task.replace_identical=True
    unreal.Exporter.run_asset_export_task(task)
    unreal.log('DELIVERY_COMPILE_EXPORTED %s' % name)
