"""Cheap intact query colliders; Chaos collision/simulation starts only at fracture."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
actors=[a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name()=='BP_DestruibleEntrega_C']
assert len(actors)==6
for a in actors:
 a.modify();gc=a.get_component_by_class(unreal.GeometryCollectionComponent);gc.modify()
 center,extent,r=unreal.SystemLibrary.get_component_bounds(gc)
 box=a.get_editor_property('Colision');box.modify();box.set_world_location(center,False,False)
 box.set_world_scale3d(unreal.Vector(1,1,1));box.set_box_extent(extent,False)
 box.set_collision_profile_name('BlockAllDynamic');box.set_collision_object_type(unreal.CollisionChannel.ECC_DESTRUCTIBLE)
 box.set_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA,unreal.CollisionResponseType.ECR_IGNORE)
 box.set_editor_property('generate_overlap_events',True);box.set_collision_enabled(unreal.CollisionEnabled.QUERY_ONLY)
 gc.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=[p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() if p.get_path_name().startswith('/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/')]
unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
unreal.log('COMPOUND_SIX_CHEAP_QUERY_COLLIDERS_FITTED')
