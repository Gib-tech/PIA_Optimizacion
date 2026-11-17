"""Sitúa suministros en las antesalas, sin atraer al jugador lejos de su escolta."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
es=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors={a.get_actor_label():a for a in es.get_all_level_actors()}
placements={'Suministro_Temporal_2':(-2300,-3750,2),'Suministro_Temporal_3':(0,-6250,2)}
for name,loc in placements.items():
 a=actors[name];a.modify();a.set_actor_location(unreal.Vector(*loc),False,True)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('SUPPLIES_IN_ANTECHAMBERS '+json.dumps(placements))
