"""Nearby refuge candidates. The sensing service still validates safety and full path length."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
specs=[('Refugio_Local_01_Izq',(-1000,-1500,0)),('Refugio_Local_01_Der',(1000,-1500,0)),('Refugio_Local_02_Norte',(-4300,-4322,0)),('Refugio_Local_02_Oeste',(-4600,-4500,0)),('Refugio_Local_02_Sur',(-4300,-5700,0))]
for name,pos in specs:
 a=placed.get(name)
 if not a:a=actors.spawn_actor_from_class(unreal.TargetPoint,unreal.Vector(*pos))
 a.set_actor_label(name);a.set_actor_location(unreal.Vector(*pos),False,True);a.set_editor_property('tags',['RefugioRehen']);a.set_folder_path('Combate/RefugiosLocales')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('LOCAL_REFUGES_PLACED')
