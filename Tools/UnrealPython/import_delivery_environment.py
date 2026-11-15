"""Editor-side: import Ian's scene into an isolated project folder, without replacing assets."""
import json
import os
import unreal

project = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
source = os.path.join(project, 'Intermediate', 'DeliverySource', 'Escenario', 'Escenario.fbx')
destination = '/Game/ThirdPerson/Environment/EscenarioIan'
assert os.path.isfile(source), source
assert not unreal.EditorAssetLibrary.does_directory_exist(destination), 'Already imported; inspect existing assets instead.'
unreal.SystemLibrary.execute_console_command(None, 'Interchange.FeatureFlags.Import.FBX 0')
options = unreal.FbxImportUI()
options.set_editor_property('automated_import_should_detect_type', False)
options.set_editor_property('mesh_type_to_import', unreal.FBXImportType.FBXIT_STATIC_MESH)
options.set_editor_property('import_mesh', True)
options.set_editor_property('import_as_skeletal', False)
options.set_editor_property('import_animations', False)
options.set_editor_property('import_materials', True)
options.set_editor_property('import_textures', True)
data = options.get_editor_property('static_mesh_import_data')
data.set_editor_property('combine_meshes', False)
data.set_editor_property('transform_vertex_to_absolute', True)
data.set_editor_property('auto_generate_collision', False)
data.set_editor_property('generate_lightmap_u_vs', True)
task = unreal.AssetImportTask()
task.filename = source
task.destination_path = destination
task.automated = True
task.replace_existing = False
task.save = True
task.options = options
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
report = []
for path in unreal.EditorAssetLibrary.list_assets(destination, recursive=True):
    asset = unreal.load_asset(path)
    item = {'path': path, 'class': asset.get_class().get_name()}
    if isinstance(asset, unreal.StaticMesh):
        bounds = asset.get_bounds()
        item['origin'] = [bounds.origin.x, bounds.origin.y, bounds.origin.z]
        item['extent'] = [bounds.box_extent.x, bounds.box_extent.y, bounds.box_extent.z]
        item['materials'] = [str(s.material_slot_name) for s in asset.static_materials]
    report.append(item)
out = os.path.join(project, 'Intermediate', 'inspect', 'environment_import.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)
unreal.log('DELIVERY_IMPORT ' + json.dumps(report))
