"""Editor-side: finish walkable geometry and place the initial gameplay route."""
import json
import os
import unreal

MAP = '/Game/ThirdPerson/Maps/Nivel_Entrega'
ROOT = '/Game/ThirdPerson/Environment/EscenarioIan'
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name() == 'Nivel_Entrega'
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not any(a.get_actor_label() == 'Suelo_Entrega' for a in actors.get_all_level_actors()), 'Already populated.'
tools = unreal.AssetToolsHelpers.get_asset_tools()

def color_material(name, color, emission=False):
    material = tools.create_asset(name, ROOT, unreal.Material, unreal.MaterialFactoryNew())
    vector = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionConstant3Vector, -350, 0)
    vector.set_editor_property('constant', unreal.LinearColor(*color))
    unreal.MaterialEditingLibrary.connect_material_property(vector, '', unreal.MaterialProperty.MP_BASE_COLOR)
    if emission:
        unreal.MaterialEditingLibrary.connect_material_property(vector, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material)
    return material

active = color_material('M_Baliza_Activa', (0.05, 1.0, 0.22, 1.0), True)
inactive = color_material('M_Baliza_Pendiente', (1.0, 0.24, 0.02, 1.0), True)
exitmat = color_material('M_Extraccion', (0.04, 0.5, 1.0, 1.0), True)
ground = tools.create_asset('M_Suelo', ROOT, unreal.Material, unreal.MaterialFactoryNew())
sample = unreal.MaterialEditingLibrary.create_material_expression(ground, unreal.MaterialExpressionTextureSample, -400, 0)
sample.texture = unreal.load_asset(ROOT + '/Textures/rock_boulder_dry_diff_2k')
uv = unreal.MaterialEditingLibrary.create_material_expression(ground, unreal.MaterialExpressionTextureCoordinate, -650, 0)
uv.set_editor_property('u_tiling', 24.0)
uv.set_editor_property('v_tiling', 28.0)
unreal.MaterialEditingLibrary.connect_material_expressions(uv, '', sample, 'Coordinates')
unreal.MaterialEditingLibrary.connect_material_property(sample, 'RGB', unreal.MaterialProperty.MP_BASE_COLOR)
rough = unreal.MaterialEditingLibrary.create_material_expression(ground, unreal.MaterialExpressionConstant, -400, 200)
rough.r = 0.9
unreal.MaterialEditingLibrary.connect_material_property(rough, '', unreal.MaterialProperty.MP_ROUGHNESS)
unreal.MaterialEditingLibrary.recompile_material(ground)
unreal.EditorAssetLibrary.save_loaded_asset(ground)

def mesh_actor(label, mesh, pos, scale, material=None, folder='Escenario/Soporte'):
    actor = actors.spawn_actor_from_object(unreal.load_asset(mesh), unreal.Vector(*pos))
    actor.set_actor_label(label)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    actor.set_folder_path(folder)
    if material:
        actor.static_mesh_component.set_material(0, material)
    return actor

mesh_actor('Suelo_Entrega', '/Engine/BasicShapes/Cube', (0, -3000, -16), (54, 66, 0.3), ground)
for label, pos, scale in [
    ('Limite_Norte', (0, 350, 160), (55, 1, 3.5)),
    ('Limite_Sur', (0, -6350, 160), (55, 1, 3.5)),
    ('Limite_Este', (2750, -3000, 160), (1, 68, 3.5)),
    ('Limite_Oeste', (-2750, -3000, 160), (1, 68, 3.5)),
]:
    mesh_actor(label, '/Engine/BasicShapes/Cube', pos, scale, unreal.load_asset(ROOT + '/Sector1'))

nav = next(a for a in actors.get_all_level_actors() if isinstance(a, unreal.NavMeshBoundsVolume))
nav.set_actor_scale3d(unreal.Vector(28, 35, 5))
nav.set_folder_path('Navegacion')
unreal.NavigationSystemV1.get_navigation_system(world).on_navigation_bounds_updated(nav)
start = next(a for a in actors.get_all_level_actors() if isinstance(a, unreal.PlayerStart))
start.set_actor_location(unreal.Vector(0, -280, 110), False, True)
start.set_actor_rotation(unreal.Rotator(0, -90, 0), False)

# Positions are initial layout choices. Path tests must approve them before delivery.
route = [(0, -1900, 65), (-1600, -2750, 65), (1600, -4900, 65)]
for i, pos in enumerate(route, 1):
    mesh_actor('Baliza_%02d' % i, '/Engine/BasicShapes/Cylinder', pos, (0.6, 0.6, 1.3), inactive, 'Objetivos/Balizas')
    text = actors.spawn_actor_from_class(unreal.TextRenderActor, unreal.Vector(pos[0], pos[1], 185), unreal.Rotator(0, 90, 0))
    text.set_actor_label('Rotulo_Baliza_%02d' % i)
    text.set_folder_path('Objetivos/Rotulos')
    text.text_render.set_text('BALIZA %d' % i)
    text.text_render.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
    text.text_render.set_world_size(40)
mesh_actor('Salida_Extraccion', '/Engine/BasicShapes/Cylinder', (0,-5700,5), (3.5,3.5,0.08), exitmat, 'Objetivos/Salida')

enemy_class = unreal.load_class(None, '/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
for i, pos in enumerate([(400,-1600,110), (-400,-2100,110), (-1700,-2650,110), (1600,-4700,110)], 1):
    enemy = actors.spawn_actor_from_class(enemy_class, unreal.Vector(*pos))
    enemy.set_actor_label('Enemigo_Entrega_%02d' % i)
    enemy.set_folder_path('Enemigos')
unreal.SystemLibrary.execute_console_command(world, 'RebuildNavigation')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('DELIVERY_POPULATED actors=%d' % len(actors.get_all_level_actors()))
