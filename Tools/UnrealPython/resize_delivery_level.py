"""Editor-side: widen Ian's layout so doorways fit the game's navigation agent."""
import unreal
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name() == 'Nivel_Entrega'
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
sectors=[a for a in actors.get_all_level_actors() if a.get_actor_label().startswith('Ian_Sector_')]
assert sectors and all(abs(a.get_actor_scale3d().x-1.0)<0.001 for a in sectors), 'Layout is already resized; do not apply twice.'
for actor in actors.get_all_level_actors():
    label = actor.get_actor_label()
    if label.startswith('Ian_Sector_') or label == 'Suelo_Entrega' or label.startswith('Limite_') or isinstance(actor, unreal.NavMeshBoundsVolume):
        scale = actor.get_actor_scale3d()
        actor.set_actor_scale3d(unreal.Vector(scale.x * 2, scale.y * 2, scale.z))
    if label.startswith(('Ian_Sector_', 'Luz_', 'Baliza_', 'Rotulo_', 'Salida_', 'Enemigo_', 'Limite_')) or label in ('Suelo_Entrega','Inicio_Jugador','Navegacion_Entrega'):
        p = actor.get_actor_location()
        actor.set_actor_location(unreal.Vector(p.x*2,p.y*2,p.z),False,True)
nav = unreal.NavigationSystemV1.get_navigation_system(world)
for actor in actors.get_all_level_actors():
    if isinstance(actor,unreal.NavMeshBoundsVolume):
        nav.on_navigation_bounds_updated(actor)
unreal.SystemLibrary.execute_console_command(world,'RebuildNavigation')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(0,-6000,14000),unreal.Rotator(pitch=-90,yaw=-90,roll=0))
unreal.log('DELIVERY_LAYOUT_XY_SCALE=2')
