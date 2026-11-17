"""Isolated PIE fixtures: natural/skip cleanup, terminal hooks and authored shots.

These prepare terminal conditions for verification and are not a normal victory.
Register after PIE starts; wait for CINEMA_FIXTURE_COMPLETE before stopping PIE.
"""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
out=os.path.join(root,'Intermediate/inspect/cinematics');os.makedirs(out,exist_ok=True)
mode=open(os.path.join(out,'mode.txt'),encoding='utf-8-sig').read().strip()
c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
p=gs.get_player_character(w,0);pc=gs.get_player_controller(w,0)
h=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
d=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
s={'stage':0,'handle':None,'busy':False,'photos':[],'samples':[],'mode':mode,'passed':False}
def finish(error=None,state=s):
    unreal.unregister_slate_post_tick_callback(state['handle'])
    state['passed']=error is None
    if error:state['error']=error
    row={k:v for k,v in state.items() if k not in ['handle','busy']}
    with open(os.path.join(out,mode+'.json'),'w',encoding='utf-8') as f:json.dump(row,f,indent=2,ensure_ascii=False)
    unreal.log('CINEMA_FIXTURE_COMPLETE '+json.dumps(row,ensure_ascii=False))
def photograph(name,state=s):
    unreal.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(out,name+'.png'))
    state['photos'].append(name)
def run(dt,state=s,gs=gs,w=w,c=c,p=p,pc=pc,h=h,d=d,out=out,photograph=photograph,finish=finish):
    if state['busy']:return
    state['busy']=True
    try:
        now=gs.get_time_seconds(w);active=c.get_editor_property('bActive');kind=c.get_editor_property('Kind');age=now-c.get_editor_property('StartedAt')
        if not c.get_editor_property('bInitialized'):state['busy']=False;return
        if state['stage']==0:
            state['initial_position']=[p.get_actor_location().x,p.get_actor_location().y,p.get_actor_location().z]
            state['initial_camera_mode']=p.get_editor_property('CamaraPrimera')
            state['stage']=1
        if mode=='intro':
            if active:
                assert kind==0 and pc.is_move_input_ignored() and pc.is_look_input_ignored()
                assert pc.get_hud().get_editor_property('show_hud')
                assert p.get_editor_property('Health_Widget').get_visibility()==unreal.SlateVisibility.HIDDEN
                for at,name in [(3,'intro-01'),(9,'intro-02'),(15,'intro-03')]:
                    if age>=at and name not in state['photos']:
                        photograph(name);state['samples'].append({'at':age,'camera':str(pc.player_camera_manager.get_camera_location()),'rotation':str(pc.player_camera_manager.get_camera_rotation()),'view_target':pc.get_view_target().get_name()})
            else:
                assert not gs.is_game_paused(w) and not pc.is_move_input_ignored() and not pc.is_look_input_ignored()
                assert pc.get_view_target()==p
                assert p.get_editor_property('Health_Widget').get_visibility()==unreal.SlateVisibility.HIT_TEST_INVISIBLE
                assert d.get_editor_property('MissionElapsed')==0
                assert not c.get_editor_property('SequencePlayer').is_playing()
                state['final_position']=[p.get_actor_location().x,p.get_actor_location().y,p.get_actor_location().z]
                photograph('intro-gameplay');finish();return
        else:
            if state['stage']==1:
                if active:c.call_method('FinishCinema')
                assert not pc.is_move_input_ignored()
                if mode in ['defeat-player','defeat-hostage']:
                    if mode=='defeat-player':gs.apply_damage(p,1000,None,None,None)
                    else:
                        h.call_method('Interactuar')
                        enemy=unreal.get_default_object(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C'))
                        gs.apply_damage(h,1000,None,enemy,None)
                elif mode=='victory':
                    # Arrange the existing extraction condition; do not call the film directly.
                    p.set_actor_location(unreal.Vector(0,-11300,100),False,True)
                    unreal.get_default_object(unreal.SystemLibrary).call_method('SetIntPropertyByName',(d,'Paso',3))
                    state['stage']=11;state['waiting_since']=now;state['busy']=False;return
                state['stage']=2;state['waiting_since']=now
            elif state['stage']==11:
                if now-state['waiting_since']<.6:state['busy']=False;return
                assert not active and d.get_editor_property('Paso')==3,'Solo extraction incorrectly won'
                state['solo_extraction_rejected']=True
                h.set_actor_location(unreal.Vector(160,-11480,100),False,True)
                bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
                bb.set_value_as_bool('bRescued',True);bb.set_value_as_bool('bAccompanying',True)
                sys=unreal.get_default_object(unreal.SystemLibrary)
                sys.call_method('SetDoublePropertyByName',(d,'MissionElapsed',137.25))
                for i in (1,2,3):sys.call_method('SetBoolPropertyByName',(d.get_editor_property('Baliza'+str(i)),'bActivated',True))
                state['stage']=2;state['waiting_since']=now
            elif state['stage']==2:
                if not active:
                    assert now-state['waiting_since']<3,'Film did not start from terminal hook'
                    state['busy']=False;return
                assert kind=={'defeat-player':1,'defeat-hostage':2,'victory':3}[mode]
                assert not gs.is_game_paused(w)
                state['stage']=3
            elif state['stage']==3:
                if active:
                    for at,name in ([(2,mode+'-01'),(6.5,mode+'-02')] if mode!='victory' else [(2,'victory-01'),(7,'victory-02'),(11,'victory-03')]):
                        if age>=at and name not in state['photos']:
                            photograph(name);state['samples'].append({'at':age,'camera':str(pc.player_camera_manager.get_camera_location()),'rotation':str(pc.player_camera_manager.get_camera_rotation())})
                else:
                    assert gs.is_game_paused(w)
                    assert not c.get_editor_property('SequencePlayer').is_playing()
                    assert d.get_editor_property('Paso')=={'defeat-player':5,'defeat-hostage':6,'victory':4}[mode]
                    if mode=='victory':assert d.get_editor_property('MissionElapsed')==137.25;state['timer_frozen']=True
                    photograph(mode+'-result');finish();return
        state['busy']=False
    except Exception:
        finish(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(run)
unreal.log('CINEMA_FIXTURE_STARTED '+mode)
