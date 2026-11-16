"""Keep mission references resident before official map conversion."""
import unreal,os
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Nivel_Entrega'
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if a.get_class().get_name().startswith('BP_') or isinstance(a,(unreal.TargetPoint,unreal.NavMeshBoundsVolume,unreal.RecastNavMesh,unreal.PlayerStart)):
  a.set_editor_property('is_spatially_loaded',False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('MISSION_ACTORS_ALWAYS_LOADED')
