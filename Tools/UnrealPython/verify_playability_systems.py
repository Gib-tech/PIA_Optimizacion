"""Prueba de entrada, lectura de materiales y cambios solares a velocidad real en PIE."""
from pathlib import Path
import json,time,traceback
import unreal

root=Path(unreal.Paths.project_dir()).resolve()
folder=root/'docs/validation/revision-jugable'
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
gs=unreal.GameplayStatics
hero=gs.get_player_character(w,0);pc=hero.get_controller()
base='/Game/ThirdPerson/Blueprints/Entrega/'
def actor(name):return gs.get_actor_of_class(w,unreal.load_class(None,base+name+'.'+name+'_C'))
extra=actor('BP_SistemasComplementarios');robot=extra.get_editor_property('Tecnico');water=extra.get_editor_property('AguaRetencion')
manager=actor('BP_DeliverySaveManager')
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground',False)
def warp(x,y,z=95):hero.set_actor_location(unreal.Vector(x,y,z),False,True)
def field(obj,key,value,kind):unreal.get_default_object(unreal.SystemLibrary).call_method('Set'+kind+'PropertyByName',(obj,key,value))
def key(name,down):unreal.SystemLibrary.execute_console_command(w,'Input.'+('+' if down else '-')+'key '+name,pc)
def shot(name):unreal.SystemLibrary.execute_console_command(w,'Shot showui filename="'+str(folder/(name+'.png')).replace('\\','/')+'"')
clock=lambda:extra.get_editor_property('WorldSeconds')
# Sólo el comienzo del reloj se fija. La transición posterior tarda tiempo de juego real.
field(extra,'WorldSeconds',0.,'Double');field(extra,'Creditos',3,'Int')
pc.set_control_rotation(unreal.Rotator(yaw=0))
warp(-350,-680)
state={'stage':0,'at':time.monotonic(),'rows':[],'phases':[],'last':None,'begin':time.monotonic()}
def next_step(stage):state.update(stage=stage,at=time.monotonic())
def tick(dt):
    try:
        t=time.monotonic()-state['at'];stage=state['stage']
        phase=extra.get_editor_property('FaseSolar');sun=extra.get_editor_property('Sun').light_component.intensity
        if phase!=state['last']:
            state['phases'].append({'fase':phase,'segundos':round(clock(),2),'lux':round(sun,2)});state['last']=phase
        assert time.monotonic()-state['begin']<145,(stage,clock())
        if stage==0 and t>.8:
            assert extra.get_editor_property('bRobotEnMira'),(str(hero.get_actor_location()),str(robot.get_actor_location()))
            key('E',True);next_step(1)
        elif stage==1 and t>.18:key('E',False);next_step(2)
        elif stage==2 and t>.35:
            assert extra.get_editor_property('DialogUntil')>gs.get_time_seconds(w),extra.get_editor_property('Notice')
            key('E',True);next_step(3)
        elif stage==3 and t>.18:
            key('E',False);assert extra.get_editor_property('bFabricating') and extra.get_editor_property('Creditos')==0
            state['kits']=extra.get_editor_property('Botiquines');next_step(4)
        elif stage==4 and t>3.5:
            assert extra.get_editor_property('Botiquines')==state['kits']+1
            state['rows'].append('E en tercera persona con la cámara orientada fuera del robot: diálogo, segundo E y conversión de tres créditos en un botiquín.')
            field(extra,'DialogUntil',0.,'Double')
            waterpos=water.get_actor_location();warp(waterpos.x-160,waterpos.y);next_step(5)
        elif stage==5 and t>.5:
            mid=extra.get_editor_property('AguaMID')
            assert extra.get_editor_property('PiesEnAgua') and mid, str(hero.get_actor_location())
            state['onda']=mid.get_scalar_parameter_value('Inicio')
            assert state['onda']>0
            point=mid.get_vector_parameter_value('Origen')
            assert abs(point.r-hero.get_actor_location().x)<15
            key('W',True);next_step(6)
        elif stage==6 and t>.9:
            key('W',False)
            mid=extra.get_editor_property('AguaMID')
            assert mid.get_scalar_parameter_value('Inicio')>state['onda']
            state['rows'].append('La cubeta permite entrar y caminar. El MID renueva origen y tiempo de onda en los pies.')
            warp(3000,-2260);pc.set_control_rotation(unreal.Rotator(yaw=70,pitch=-8));next_step(7)
        elif stage==7 and t>.8:
            assert not extra.get_editor_property('PiesEnAgua')
            state['rows'].append('Fuera de la superficie cesan las pisadas de agua.')
            key('F5',True);next_step(8)
        elif stage==8 and t>.2:
            key('F5',False);assert manager.get_editor_property('bSaveSucceeded') and not manager.get_editor_property('StatusText')
            state['rows'].append('F5 escribe un checkpoint desde la entrada real y deja el aviso vacío.')
            shot('hud-estanque');next_step(9)
        elif stage==9 and t>1:
            # Fixture visual del aviso, independiente de la prueba del daño de combate.
            hud=pc.get_hud();field(hud,'HostageHurtUntil',gs.get_time_seconds(w)+3,'Double')
            next_step(10)
        elif stage==10 and phase==2 and clock()>65:
            shot('ocaso-natural');state['rows'].append('Día, atardecer y noche visibles durante los primeros 65 segundos sin mover el reloj ni acelerar el mundo.')
            state['passed']=True;finish()
    except Exception:state.update(passed=False,error=traceback.format_exc());finish()
def finish():
    unreal.unregister_slate_post_tick_callback(state['handle'])
    for name in ['E','W','F5']:key(name,False)
    data={k:v for k,v in state.items() if k in ['passed','error','phases','rows','stage']}
    (folder/'sistemas.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
state['handle']=unreal.register_slate_post_tick_callback(tick)
