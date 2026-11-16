"""Persist real collision query overlaps on all six placed Geometry Collections."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
actors=[a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name()=='BP_DestruibleEntrega_C']
assert len(actors)==6,'Load the compound editor region first'
for a in actors:
 a.modify();c=a.get_component_by_class(unreal.GeometryCollectionComponent);c.modify();c.set_editor_property('generate_overlap_events',True)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=[p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() if p.get_path_name().startswith('/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/')]
unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
unreal.log('COMPOUND_REAL_WEAPON_OVERLAPS_ENABLED')
