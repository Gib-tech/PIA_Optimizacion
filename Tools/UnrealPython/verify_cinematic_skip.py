"""Arm first-person skip verification; press physical Space in the focused PIE."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=gs.get_player_controller(w,0)
c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
assert not gs.is_game_paused(w)
if c.get_editor_property('bActive'):c.call_method('FinishCinema')
lib=unreal.get_default_object(unreal.load_class(None,'/Script/Engine.SubsystemBlueprintLibrary'))
sub=lib.call_method('GetLocalPlayerSubSystemFromPlayerController',(pc,unreal.EnhancedInputLocalPlayerSubsystem.static_class()))
if not p.get_editor_property('CamaraPrimera'):
    sub.inject_input_vector_for_action(unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_Camera'),unreal.Vector(1,0,0),[],[])
s={'stage':0,'handle':None,'passed':False}
def watch(dt,state=s):
    try:
        if state['stage']==0:
            if not p.get_editor_property('CamaraPrimera'):return
            state['position']=str(p.get_actor_location());state['rotation']=str(pc.get_control_rotation())
            c.call_method('StartIntro');state['stage']=1;unreal.log('CINEMA_PHYSICAL_SKIP_ARMED');return
        if c.get_editor_property('bActive'):return
        elapsed=gs.get_time_seconds(w)-c.get_editor_property('StartedAt')
        assert elapsed<17,'Expected a physical Space skip before natural completion'
        assert p.get_editor_property('CamaraPrimera') and p.mesh.get_editor_property('owner_no_see')
        assert pc.get_view_target()==p and not pc.is_move_input_ignored() and not pc.is_look_input_ignored()
        assert str(pc.get_control_rotation())==state['rotation']
        assert not c.get_editor_property('SequencePlayer').is_playing()
        state['passed']=True;state['skip_age']=elapsed;unreal.unregister_slate_post_tick_callback(state['handle'])
        with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/cinematics/skip-first-person.json'),'w') as f:json.dump({k:v for k,v in state.items() if k!='handle'},f,indent=2)
        unreal.log('CINEMA_PHYSICAL_SKIP_PASSED '+str(elapsed))
    except Exception:
        unreal.unregister_slate_post_tick_callback(state['handle']);unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(watch)
