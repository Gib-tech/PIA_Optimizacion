"""Editor-side: create an isolated playable scene from Ian's imported meshes."""
import json
import os
import unreal

ROOT = '/Game/ThirdPerson/Environment/EscenarioIan'
MAP = '/Game/ThirdPerson/Maps/Nivel_Entrega'
project = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not unreal.EditorAssetLibrary.does_asset_exist(MAP), 'Level already exists; do not overwrite.'
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages(), 'Save the current map before switching.'

# Import original textures individually: the FBX references paths on Ian's computer.
tasks = []
for filename in sorted(os.listdir(os.path.join(project, 'Intermediate', 'DeliverySource', 'Escenario'))):
    if filename.lower().endswith(('.jpg', '.png')):
        task = unreal.AssetImportTask()
        task.filename = os.path.join(project, 'Intermediate', 'DeliverySource', 'Escenario', filename)
        task.destination_path = ROOT + '/Textures'
        task.automated = True
        task.save = True
        task.replace_existing = False
        tasks.append(task)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
textures = [unreal.load_asset(t.imported_object_paths[0]) for t in tasks if t.imported_object_paths]
diffuse = {t.get_name(): t for t in textures if '_diff_' in t.get_name()}
assignments = {'Sector1': 'wood_inlaid_stone_wall_diff_2k', 'Sector2': 'rock_boulder_dry_diff_2k',
               'Sector3': 'wood_inlaid_stone_wall_diff_2k', 'Sector4': 'rock_wall_16_diff_2k'}
for name, texname in assignments.items():
    material = unreal.load_asset(ROOT + '/' + name)
    # Imported materials only; no marketplace materials are touched.
    unreal.MaterialEditingLibrary.delete_all_material_expressions(material)
    sample = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionTextureSample, -400, 0)
    sample.texture = diffuse[texname]
    unreal.MaterialEditingLibrary.connect_material_property(sample, 'RGB', unreal.MaterialProperty.MP_BASE_COLOR)
    roughness = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionConstant, -400, 200)
    roughness.set_editor_property('r', 0.85)
    unreal.MaterialEditingLibrary.connect_material_property(roughness, '', unreal.MaterialProperty.MP_ROUGHNESS)
    material.set_editor_property('two_sided', True)
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material)

assert level.new_level(MAP), 'Could not create delivery level'
for n in range(1, 5):
    mesh = unreal.load_asset(ROOT + '/Escenario_Sector%d' % n)
    body = mesh.get_editor_property('body_setup')
    body.set_editor_property('collision_trace_flag', unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
    mesh.modify()
    unreal.EditorAssetLibrary.save_loaded_asset(mesh)
    actor = actors.spawn_actor_from_object(mesh, unreal.Vector())
    actor.set_actor_label('Ian_Sector_%02d' % n)
    actor.set_folder_path('Escenario/Ian')
    actor.static_mesh_component.set_collision_profile_name('BlockAll')

sun = actors.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 2500), unreal.Rotator(-55, -35, 0))
sun.set_actor_label('Luz_Sol')
sun.light_component.set_editor_property('intensity', 3.0)
sky = actors.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, -3000, 2000))
sky.set_actor_label('Luz_Ambiente')
sky.light_component.set_editor_property('real_time_capture', True)
actors.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector())
start = actors.spawn_actor_from_class(unreal.PlayerStart, unreal.Vector(700, -500, 120), unreal.Rotator(0, -90, 0))
start.set_actor_label('Inicio_Jugador')
settings = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_world_settings()
settings.set_editor_property('default_game_mode', unreal.load_class(None, '/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C'))
level.save_current_level()
unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(0, -3000, 6500), unreal.Rotator(-90, -90, 0))
unreal.log('DELIVERY_LEVEL_CREATED ' + MAP)
