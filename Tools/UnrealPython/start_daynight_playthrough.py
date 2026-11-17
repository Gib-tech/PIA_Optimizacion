"""Recorrido nocturno mediante movimiento/combate normal; sólo se prepara la hora inicial."""
import unreal,os
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
source=open(os.path.join(root,'Tools/UnrealPython/playthrough_current_mission.py'),encoding='utf-8').read()
# El script existente reemplaza rutas dentro de su generador. Cambiar sólo el
# destino de evidencia conserva todos los controles de una partida normal.
source=source.replace('docs/validation/partida-completa-2026-11-17.json','docs/validation/ciclo-luces-ataques/partida-nocturna.json').replace('docs/validation/partida-completa','docs/validation/ciclo-luces-ataques/partida-nocturna')
namespace={'__name__':'daynight_playthrough','__file__':os.path.join(root,'Tools/UnrealPython/playthrough_current_mission.py')}
exec(compile(source,'daynight_playthrough','exec'),namespace)
inner=namespace['namespace'];original_finish=inner['finish']
def finish_night_walk(passed,reason,state=inner['state'],finish_original=original_finish,report_path=inner['out']):
 import json
 finish_original(passed,reason,state)
 with open(report_path,encoding='utf-8') as f:result=json.load(f)
 result.update(initial_world_seconds=783.,prepared_time_only=True,expected_wall_lights=41)
 with open(report_path,'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
inner['finish']=finish_night_walk
w=namespace['w'];gs=unreal.GameplayStatics
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
extra=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
unreal.get_default_object(unreal.SystemLibrary).call_method('SetDoublePropertyByName',(extra,'WorldSeconds',783.))
unreal.log('NIGHT_PLAYTHROUGH_STARTED_NORMAL_MOVEMENT_ONLY')
