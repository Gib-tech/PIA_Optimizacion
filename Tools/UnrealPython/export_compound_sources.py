"""Read-only geometry sources for the Blender split/cover recipe."""
import unreal,os
root=unreal.Paths.project_dir()
for i in range(1,5):
 task=unreal.AssetExportTask();task.object=unreal.load_asset('/Game/ThirdPerson/Environment/Evaluation/SM_IanWalls_%02d'%i)
 task.filename=os.path.join(root,'Intermediate/inspect/evaluation_wall_%d.obj'%i);task.automated=True;task.prompt=False;task.replace_identical=True
 assert task.object and unreal.Exporter.run_asset_export_task(task)
unreal.log('COMPOUND_ORIGINAL_WALL_SOURCES_EXPORTED')
