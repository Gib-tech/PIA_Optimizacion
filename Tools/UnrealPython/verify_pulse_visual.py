"""Prueba el disparo por entrada real en ambas cámaras y registra el movimiento en PIE."""
from pathlib import Path
import json
import time
import traceback
import unreal

root = Path(unreal.Paths.project_dir()).resolve()
out = root/'docs/validation/pulso'
frames = root/'Intermediate/inspect/pulso-fotogramas'
out.mkdir(exist_ok=True, parents=True)
frames.mkdir(exist_ok=True, parents=True)
es = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert not es.get_game_world()
gs = unreal.GameplayStatics
folder = '/Game/ThirdPerson/Blueprints/Entrega/'
beam_class = unreal.load_class(None, folder+'BP_PulsoTemporalVisual.BP_PulsoTemporalVisual_C')
settings = unreal.get_default_object(unreal.load_class(None, '/Script/UnrealEd.EditorPerformanceSettings'))
throttle = settings.get_editor_property('bThrottleCPUWhenNotForeground')
settings.set_editor_property('bThrottleCPUWhenNotForeground', False)
checkpoint = Path(unreal.Paths.project_saved_dir()).resolve()/'SaveGames/TimeOut_Delivery_v1.sav'
original = checkpoint.read_bytes() if checkpoint.exists() else None
s = {'stage': 'start', 'deadline': time.monotonic()+120, 'shots': [], 'camera': 'tercera'}


def finish(error=None):
    unreal.unregister_slate_post_tick_callback(s['handle'])
    settings.set_editor_property('bThrottleCPUWhenNotForeground', throttle)
    result = {'passed': not error, 'metodo': 'PIE con munición, posiciones e IA inmóvil preparadas. Se inyectan botones de Unreal y se ralentiza el mundo para muestrear la animación en tiempo de juego.', 'shots': s['shots']}
    if error:
        result['error'] = error

    def restore(dt):
        if es.get_game_world():
            return
        unreal.unregister_slate_post_tick_callback(s['restore'])
        if original is None:
            checkpoint.unlink(missing_ok=True)
        elif not checkpoint.exists() or checkpoint.read_bytes()!=original:
            checkpoint.write_bytes(original)
        (out/'prueba.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf8')
    s['restore'] = unreal.register_slate_post_tick_callback(restore)
    level.editor_request_end_play()


def check(dt):
    try:
        assert time.monotonic() < s['deadline'], ('Tiempo agotado', s['stage'])
        w = es.get_game_world()
        if not w:
            return
        now = gs.get_time_seconds(w)
        hero = gs.get_player_character(w, 0)
        if not hero:
            return
        pc = hero.get_controller()
        def actor(path, name):
            return gs.get_actor_of_class(w, unreal.load_class(None, path+name+'.'+name+'_C'))
        def key(pressed):
            name = 'MiddleMouseButton' if s['camera']=='tercera' else 'Gamepad_RightTrigger'
            unreal.SystemLibrary.execute_console_command(w, 'Input.'+('+' if pressed else '-')+'key '+name, pc)
        def shot(index):
            path = frames/(s['camera']+f'-{index:02d}.png')
            unreal.SystemLibrary.execute_console_command(w, 'Shot filename="'+path.as_posix()+'" -nosuffix', pc)
        def field(obj, name, value, kind):
            unreal.get_default_object(unreal.SystemLibrary).call_method('Set'+kind+'PropertyByName', (obj,name,value))

        extra = actor(folder, 'BP_SistemasComplementarios')
        stage = s['stage']
        if stage == 'start':
            cinema = actor('/Game/ThirdPerson/Cinematics/', 'BP_CinematicDirector')
            if now<2 or not cinema or not extra or not extra.get_editor_property('bInitialized'):
                return
            if cinema.get_editor_property('bActive'):
                cinema.call_method('FinishCinema')
            field(extra,'Cargas',2,'Int')
            hero.set_actor_location(unreal.Vector(0,-1800,95),False,True)
            hero.set_actor_rotation(unreal.Rotator(yaw=-90),False)
            pc.set_control_rotation(unreal.Rotator(yaw=-90))
            enemy_class = unreal.load_class(None, '/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
            native = unreal.get_default_object(gs)
            tr = unreal.Transform(location=unreal.Vector(0,-2290,95))
            mode = unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT
            enemy = native.call_method('BeginDeferredActorSpawnFromClass',(w, enemy_class, tr, unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,mode))
            native.call_method('FinishSpawningActor',(enemy,tr,mode))
            enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Prueba de puntería')
            enemy.character_movement.disable_movement()
            s.update(enemy=enemy, stage='aim', at=now)
        elif stage == 'aim':
            cam = gs.get_player_camera_manager(w,0)
            first = s['camera']=='primera'
            if bool(hero.get_editor_property('CamaraPrimera'))!=first:
                field(hero,'CamaraPrimera',first,'Bool')
                hero.get_editor_property('FPC' if first else 'TPC').activate()
                hero.get_editor_property('TPC' if first else 'FPC').deactivate()
            rot = unreal.Rotator(yaw=-90, pitch=48) if first else unreal.MathLibrary.find_look_at_rotation(cam.get_camera_location(),s['enemy'].get_actor_location()+unreal.Vector(0,0,26))
            pc.set_control_rotation(rot)
            if now-s['at']<1.4:
                return
            gs.set_global_time_dilation(w,.18)
            shot(0)
            s.update(stage='press', at=now)
        elif stage == 'press' and now-s['at']>.075:
            key(True)
            s.update(stage='flight', index=1, flight=[])
        elif stage == 'flight':
            beams = gs.get_all_actors_of_class(w,beam_class)
            if not beams:
                return
            assert len(beams)==1
            beam = beams[0]
            front = beam.get_component_by_class(unreal.MaterialBillboardComponent)
            age = beam.get_game_time_since_creation()
            if s['index']==1:
                key(False)
                assert beam.static_mesh_component.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
                assert front.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION
                endpoint = beam.get_actor_transform().transform_location(unreal.Vector(50,0,0))
                s['range_cm'] = (endpoint-hero.get_actor_location()).length()
                assert s['range_cm'] <= 800.1, s['range_cm']
                start = extra.get_editor_property('LastPulseAt')
                extra.call_method('DispararPulso')
                assert extra.get_editor_property('LastPulseAt')==start
            if age >= (s['index']-1)*.045:
                s['flight'].append([round(age,3),round(front.get_editor_property('relative_location').x,2)])
                shot(s['index'])
                s['index']+=1
            if age>.46:
                s.update(stage='cleanup', at=now)
        elif stage == 'cleanup' and now-s['at']>.16:
            assert not gs.get_all_actors_of_class(w,beam_class)
            flight = s['flight']
            assert min(x for _,x in flight)<0 and max(x for _,x in flight)>48, flight
            first = s['camera']=='primera'
            charges = extra.get_editor_property('Cargas')
            hp = s['enemy'].get_editor_property('BPC_E_Health').get_editor_property('E_Health')
            assert charges==(0 if first else 1) and hp==80, (charges,hp)
            shot(s['index'])
            s['shots'].append({'camara':s['camera'],'entrada':'Gamepad_RightTrigger' if first else 'MiddleMouseButton','objetivo':'cielo' if first else 'enemigo','vida_enemigo':hp,'cargas_restantes':charges,'distancia_final_cm':round(s['range_cm'],2),'frente_tiempo_s_y_x_local_cm':flight,'efecto_retirado':True})
            gs.set_global_time_dilation(w,1)
            if first:
                s.update(stage='empty',at=now)
            else:
                s.update(stage='aim',at=now,camera='primera')
        elif stage == 'empty' and now-s['at']>1:
            key(True)
            s.update(stage='denied',at=now)
        elif stage == 'denied' and now-s['at']>.12:
            key(False)
            assert not gs.get_all_actors_of_class(w,beam_class) and 'Sin celdas' in extra.get_editor_property('Notice')
            finish()
    except Exception:
        finish(traceback.format_exc())


s['handle'] = unreal.register_slate_post_tick_callback(check)
level.editor_request_begin_play()
