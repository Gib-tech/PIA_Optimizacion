"""El inicio debe existir antes de crear la primera fuente de streaming de WP."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert unreal.DeliveryBlueprintBuilder.load_editor_region(w,unreal.Vector(-6500,-12500,-1000),unreal.Vector(6500,1000,3500))
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
starts=[a for a in actors.get_all_level_actors() if isinstance(a,unreal.PlayerStart)]
assert starts,'No crear otro PlayerStart hasta comprobar los actores de la región completa.'
for a in starts:
 a.modify();a.set_editor_property('is_spatially_loaded',False)
 unreal.log('RESIDENT_PLAYER_START '+a.get_actor_label()+' '+str(a.get_actor_location()))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
if dirty:unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
