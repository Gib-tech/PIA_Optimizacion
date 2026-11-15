"""Compile, save, export and open the asset named in Intermediate/inspect/edit_asset.txt."""
import os
import unreal

root = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
path = open(os.path.join(root, 'Intermediate/inspect/edit_asset.txt'), encoding='utf-8-sig').read().strip()
asset = unreal.load_asset(path)
assert asset, path
if isinstance(asset, unreal.Blueprint):
    unreal.BlueprintEditorLibrary.compile_blueprint(asset)
unreal.EditorAssetLibrary.save_loaded_asset(asset)
task = unreal.AssetExportTask()
task.object = asset
task.filename = os.path.join(root, 'Intermediate/inspect/live', asset.get_name()+'.t3d')
task.automated = True
task.prompt = False
task.replace_identical = True
unreal.Exporter.run_asset_export_task(task)
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([asset])
unreal.log('DELIVERY_ASSET ' + path)
