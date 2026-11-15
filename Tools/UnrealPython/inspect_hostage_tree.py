import os
import unreal
tree=unreal.load_asset('/Game/ThirdPerson/Blueprints/Aliado/BT_Hostage')
task=unreal.AssetExportTask()
task.object=tree
task.filename=os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()),'Intermediate/inspect/live/BT_Hostage.t3d')
task.automated=True;task.prompt=False;task.replace_identical=True
unreal.Exporter.run_asset_export_task(task)
unreal.log('HOSTAGE_TREE_EXPORTED')
