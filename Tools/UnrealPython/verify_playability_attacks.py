"""Matriz de impactos mediante entradas del motor y una colocación por objetivo."""
from pathlib import Path
import json, math, time, traceback
import unreal

root=Path(unreal.Paths.project_dir()).resolve()
folder=root/'docs/validation/revision-jugable';folder.mkdir(exist_ok=True,parents=True)
case=(root/'Intermediate/inspect/revision-jugable/mode').read_text().strip()
mode,_,group=case.partition('-')
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
gs=unreal.GameplayStatics
base='/Game/ThirdPerson/Blueprints/Entrega/'
def one(name):return gs.get_actor_of_class(w,unreal.load_class(None,base+name+'.'+name+'_C'))
hero=gs.get_player_character(w,0);pc=hero.get_controller();extra=one('BP_SistemasComplementarios')
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
objects=sorted(gs.get_all_actors_of_class(w,one('BP_DestruibleEntrega').get_class()),key=lambda a:a.get_actor_label())
assert len(objects)==10,[(a.get_actor_label()) for a in objects]
if group:objects=[a for a in objects if a.get_actor_label().startswith('Impacto_')==(group=='copias')]
def field(obj,key,value,kind):unreal.get_default_object(unreal.SystemLibrary).call_method('Set'+kind+'PropertyByName',(obj,key,value))
field(extra,'Cargas',25,'Int');field(hero,'bIsHammerEquipped',mode.startswith('martillo'),'Bool')
field(hero,'bIsSwordEquipped',not mode.startswith('martillo'),'Bool');field(hero,'bHammerUpgraded',False,'Bool')
field(hero,'CamaraPrimera',False,'Bool');hero.get_editor_property('TPC').activate();hero.get_editor_property('FPC').deactivate()
key='MiddleMouseButton' if mode=='pulso' else 'LeftMouseButton' if mode.endswith('ligero') else 'RightMouseButton'
def command(op):unreal.SystemLibrary.execute_console_command(w,'Input.'+op+'key '+key,pc)
def visible(start,end,actor):
    hit=unreal.SystemLibrary.line_trace_single(w,start,end,unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[hero],unreal.DrawDebugTrace.NONE)
    return hit and unreal.get_default_object(gs).call_method('BreakHitResult',(hit,))[9]==actor
state={'i':0,'stage':'approach','rows':[]}
def finish(error=None):
    command('-');unreal.unregister_slate_post_tick_callback(state['handle'])
    report={'passed':error is None,'attack':mode,'third_person':True,'hammer_upgrade':False,'input':key,'fixture':'Posición, equipo y munición preparados. Una pulsación por objetivo, sin aplicar daño ni invocar callbacks del arma.','objects':state['rows']}
    if error:report['error']=error
    (folder/(case+'.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
def tick(dt):
    try:
        now=time.monotonic()
        if state['i']>=len(objects):finish();return
        a=objects[state['i']];stage=state['stage']
        if stage=='approach':
            if hero.get_current_montage() or hero.get_editor_property('IsAttacking'):return
            center,extent,_=unreal.SystemLibrary.get_component_bounds(a.get_editor_property('Colision'))
            for dx,dy in [(0,-1),(-1,0),(0,1),(1,0)]:
                loc=unreal.Vector(center.x+dx*(extent.x+140),center.y+dy*(extent.y+140),95)
                if visible(loc+unreal.Vector(0,0,55),center,a):break
            else:raise AssertionError('Sin cara accesible '+a.get_actor_label())
            yaw=math.degrees(math.atan2(center.y-loc.y,center.x-loc.x))
            hero.set_actor_location(loc,False,True);hero.set_actor_rotation(unreal.Rotator(yaw=yaw),False)
            pc.set_control_rotation(unreal.Rotator(yaw=yaw));pc.set_view_target_with_blend(hero,0)
            state.update(stage='aim',at=now,center=center,label=a.get_actor_label(),hp=a.get_editor_property('Health'))
            return
        if stage=='aim':
            if mode=='pulso':
                cam=gs.get_player_camera_manager(w,0)
                pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(cam.get_camera_location(),state['center']))
            if now-state['at']<1.2 or hero.get_current_montage():return
            assert state['hp']==15,(a.get_actor_label(),state['hp'])
            command('+');state.update(stage='release',at=now);return
        if stage=='release' and now-state['at']>.14:
            command('-');state.update(stage='hit');return
        if stage=='hit':
            if a.get_editor_property('bBroken') and a.get_editor_property('ChaosBreakCount')>0:
                model=a.get_editor_property('ModeloIntacto')
                if model:assert model.get_editor_property('hidden'),model.get_actor_label()
                state['rows'].append({'actor':a.get_actor_label(),'modelo':model.get_actor_label() if model else None,'vida_inicial':state['hp'],'vida_final':a.get_editor_property('Health'),'fracturas':a.get_editor_property('ChaosBreakCount')})
                state.update(i=state['i']+1,stage='approach');return
            assert now-state['at']<5,(state['label'],a.get_editor_property('Health'),extra.get_editor_property('Notice'),str(hero.get_actor_location()))
    except Exception:finish(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(tick)
