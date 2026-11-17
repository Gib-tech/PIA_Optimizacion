"""Read current film/camera/input state; no gameplay mutation."""
import unreal,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics
c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
p=gs.get_player_character(w,0);pc=gs.get_player_controller(w,0);sp=c.get_editor_property('SequencePlayer')
row={k:str(c.get_editor_property(k)) for k in ['bInitialized','bShouldIntro','bActive','bOutcomeStarted','Kind','StartedAt','EndsAt','Duration']}
row.update(now=gs.get_time_seconds(w),paused=gs.is_game_paused(w),view_target=pc.get_view_target().get_name(),location=str(p.get_actor_location()),move_ignored=pc.is_move_input_ignored(),look_ignored=pc.is_look_input_ignored(),sequence_playing=sp.is_playing() if sp else None,sequence_time=str(sp.get_current_time()) if sp else None,camera=str(pc.player_camera_manager.get_camera_location()),hostage_scale=str(c.get_editor_property('Hostage').mesh.get_world_scale()))
unreal.log('CINEMA_QA '+json.dumps(row))
