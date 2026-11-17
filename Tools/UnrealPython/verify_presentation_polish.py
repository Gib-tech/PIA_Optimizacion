"""Prueba preparada en PIE del HUD, colisiones, ráfaga nocturna, luces y agua."""
from pathlib import Path
import json, time, traceback
import unreal

root=Path(unreal.Paths.project_dir()).resolve()
out=root/'docs/validation/presentacion';out.mkdir(parents=True,exist_ok=True)
es=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert not es.get_game_world()
gs=unreal.GameplayStatics
settings=unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings'))
throttle=settings.get_editor_property('bThrottleCPUWhenNotForeground')
settings.set_editor_property('bThrottleCPUWhenNotForeground',False)
checkpoint=root/'Saved/SaveGames/TimeOut_Delivery_v1.sav'
original=checkpoint.read_bytes() if checkpoint.exists() else None
state={'stage':0,'rows':{},'deadline':time.monotonic()+100}
def next_stage(now):
    state['stage']+=1;state['at']=now
def finish(error=None):
    unreal.unregister_slate_post_tick_callback(state['handle'])
    settings.set_editor_property('bThrottleCPUWhenNotForeground',throttle)
    result={'passed':not error,'metodo':'PIE con posiciones, daño de prueba y fase nocturna preparados.',**state['rows']}
    if error:result['error']=error
    def restore(dt):
        if es.get_game_world():return
        unreal.unregister_slate_post_tick_callback(state['restore_handle'])
        if original is None:
            checkpoint.unlink(missing_ok=True)
        elif not checkpoint.exists() or checkpoint.read_bytes()!=original:
            temp=checkpoint.with_suffix('.presentacion.tmp')
            temp.write_bytes(original);temp.replace(checkpoint)
        (out/'pruebas.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    state['restore_handle']=unreal.register_slate_post_tick_callback(restore)
    level.editor_request_end_play()
def check(dt):
    try:
        assert time.monotonic()<state['deadline'],('Tiempo de prueba agotado',state['stage'])
        w=es.get_game_world()
        if not w:return
        now=gs.get_time_seconds(w);stage=state['stage']
        pc=gs.get_player_controller(w,0);hero=gs.get_player_character(w,0)
        if not pc or not hero:return
        def of(name,path='/Game/ThirdPerson/Blueprints/Entrega/'):
            return gs.get_actor_of_class(w,unreal.load_class(None,path+name+'.'+name+'_C'))
        cinema=of('BP_CinematicDirector','/Game/ThirdPerson/Cinematics/')
        if not cinema or not cinema.get_editor_property('bInitialized'):return
        def shot(name):unreal.SystemLibrary.execute_console_command(w,'Shot showui filename="'+(out/(name+'.png')).as_posix()+'" -nosuffix',pc)
        def key(k,on):unreal.SystemLibrary.execute_console_command(w,'Input.'+('+' if on else '-')+'key '+k,pc)
        def field(obj,k,value):unreal.get_default_object(unreal.SystemLibrary).call_method('SetDoublePropertyByName',(obj,k,value))
        extra=of('BP_SistemasComplementarios');host=of('BP_Hostage','/Game/ThirdPerson/Blueprints/Aliado/')
        hp=hero.get_editor_property('BPC_Health')
        if stage==0 and now>2:
            assert cinema.get_editor_property('bActive') and hero.get_editor_property('Health_Widget').get_visibility()==unreal.SlateVisibility.HIDDEN
            assert pc.get_hud().get_editor_property('CurrentDialog')==0
            shot('cinematica');next_stage(now)
        elif stage==1 and now-state['at']>.6:
            cinema.call_method('FinishCinema');next_stage(now)
        elif stage==2 and now-state['at']>.7:
            assert not cinema.get_editor_property('bActive') and pc.get_hud().get_editor_property('CurrentDialog')>0
            assert hero.get_editor_property('Health_Widget').get_visibility()==unreal.SlateVisibility.HIT_TEST_INVISIBLE
            shot('juego');state['rows']['hud']='Oculto en introducción, subtítulos y omisión visibles. La interfaz de juego vuelve al terminar.'
            state['hp']=hp.get_editor_property('Health');key('One',True);next_stage(now)
        elif stage==3 and now-state['at']>.18:
            key('One',False);assert hp.get_editor_property('Health')==state['hp']
            state['rows']['vida_antes_y_despues_de_1']=[state['hp'],hp.get_editor_property('Health')]
            center=host.get_actor_location()
            hero.set_actor_location(center+unreal.Vector(180,0,0),False,True)
            hero.set_actor_location(center-unreal.Vector(170,0,0),True,False)
            dist=hero.get_actor_location().x-center.x
            assert 60<dist<130,dist
            state['rows']['distancia_al_bloquear_capsulas_cm']=round(dist,2)
            field(extra,'WorldSeconds',175.)
            water=extra.get_editor_property('AguaRetencion');pos=water.get_actor_location()
            hero.set_actor_location(unreal.Vector(pos.x+85,pos.y,93),False,True);next_stage(now)
        elif stage==4 and now-state['at']>.85:
            assert extra.get_editor_property('PiesEnAgua') and extra.get_editor_property('AguaMID').get_scalar_parameter_value('Inicio')>0
            lights=gs.get_all_actors_of_class(w,of('BP_LuminariaPared').get_class())
            assert len(lights)==41 and all(a.get_component_by_class(unreal.SpotLightComponent).get_editor_property('max_draw_distance')==6500 for a in lights)
            other={a.get_actor_label():a for a in gs.get_all_actors_of_class(w,unreal.Actor)}
            for k in ('Luz_Compound_Rescate','Luz_Compound_Deposito'):
                assert other[k].get_component_by_class(unreal.LocalLightComponent).get_editor_property('max_draw_distance')==0
            assert [m.get_name() for m in other['LOD_Tree1'].static_mesh_component.get_materials()]==['M_FollajeAcceso','M_CortezaAcceso']
            state['rows']['luces']={'pared_a_65_m':len(lights),'interiores_sin_corte':2}
            state['rows']['texturas_y_agua']='Ambos materiales aplicados al árbol colocado. Contacto de pies en la cubeta y parámetro de onda actualizado.'
            gc_actor=other['Destruible_Caja'];box=gc_actor.get_editor_property('Colision')
            center,ext,_=unreal.SystemLibrary.get_component_bounds(box)
            hero.set_actor_location(unreal.Vector(center.x+200,center.y,94),False,True)
            unreal.get_default_object(unreal.SystemLibrary).call_method('SetBoolPropertyByName',(hero,'CamaraPrimera',True))
            hero.get_editor_property('TPC').deactivate();hero.get_editor_property('FPC').activate()
            hero.set_actor_rotation(unreal.Rotator(yaw=180),False)
            pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(hero.get_editor_property('FPC').get_world_location(),center))
            state.update(prop=gc_actor,center=center,prev_fx=set(a.get_path_name() for a in gs.get_all_actors_of_class(w,unreal.NiagaraActor)))
            next_stage(now)
        elif stage==5 and now-state['at']>1.5:
            assert not extra.get_editor_property('PiesEnAgua') and extra.get_editor_property('FaseSolar')==2
            hud=pc.get_hud()
            unreal.get_default_object(unreal.SystemLibrary).call_method('SetIntPropertyByName',(hud,'DismissedDialog',hud.get_editor_property('CurrentDialog')))
            a=state['prop'];gs.apply_damage(a,15,pc,hero,None)
            assert a.get_editor_property('bBroken')
            bursts=[n for n in gs.get_all_actors_of_class(w,unreal.NiagaraActor) if n.get_path_name() not in state['prev_fx']]
            assert len(bursts)==1,([n.get_name() for n in bursts],state['prev_fx'],a.get_life_span(),a.get_editor_property('Colision').get_collision_enabled(),a.get_component_by_class(unreal.GeometryCollectionComponent).get_collision_profile_name())
            fx=bursts[0];assert fx.niagara_component.is_active() and 0<fx.get_life_span()<=.66
            state['fx_name']=fx.get_path_name();state['rows']['limite_rafaga_s']=round(fx.get_life_span(),2)
            next_stage(now)
        elif stage==6 and now-state['at']>.12:
            shot('rotura-nocturna')
            c=state['prop'].get_component_by_class(unreal.GeometryCollectionComponent)
            assert c.get_collision_enabled()==unreal.CollisionEnabled.PHYSICS_ONLY and str(c.get_collision_profile_name())=='RestosEscenario'
            assert c.get_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN)==unreal.CollisionResponseType.ECR_IGNORE
            assert list(map(str,c.get_editor_property('collision_profile_per_level')))==['RestosEscenario']
            assert not c.get_editor_property('can_ever_affect_navigation')
            next_stage(now)
        elif stage==7 and now-state['at']>.8:
            assert all(a.get_path_name()!=state['fx_name'] for a in gs.get_all_actors_of_class(w,unreal.NiagaraActor))
            assert state['prop'].get_editor_property('ChaosBreakCount')>0
            center=state['center']
            hero.set_actor_location(unreal.Vector(center.x+130,center.y,95),False,True)
            hero.set_actor_location(unreal.Vector(center.x-85,center.y,95),True,False)
            assert hero.get_actor_location().x<center.x-70,(center,hero.get_actor_location())
            state['rows']['fractura']={'eventos':state['prop'].get_editor_property('ChaosBreakCount'),'atraveso_restos':True,'efecto_retirado':True}
            state['rows']['perfil_puertas']=str(unreal.get_default_object(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DoorFragment.BP_DoorFragment_C')).static_mesh_component.get_collision_profile_name())
            assert state['rows']['perfil_puertas']=='RestosEscenario'
            bb=host.get_controller().get_component_by_class(unreal.BlackboardComponent)
            bb.set_value_as_bool('bRescued',True)
            tr=unreal.Transform(location=hero.get_actor_location()+unreal.Vector(2200,0,0))
            enemy_cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
            native=unreal.get_default_object(gs)
            enemy=native.call_method('BeginDeferredActorSpawnFromClass',(w,enemy_cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
            native.call_method('FinishSpawningActor',(enemy,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
            state['host_hp']=host.get_editor_property('Health')
            gs.apply_damage(host,13.2,None,enemy,None)
            next_stage(now)
        elif stage==8 and now-state['at']>.12:
            hud=pc.get_hud()
            assert abs(state['host_hp']-host.get_editor_property('Health')-13.2)<.01
            assert hud.get_editor_property('HostageAlertCooldown')>gs.get_real_time_seconds(w)
            assert hud.get_editor_property('HostageHurtUntil')>gs.get_real_time_seconds(w)
            state['rows']['alerta_rehen']='Daño de enemigo de 13,2 aceptado. Se ejecutaron la rama de sonido y el aviso visual.'
            field(extra,'WorldSeconds',5.)
            cam_transform=unreal.Transform(location=unreal.Vector(2020,-1290,360))
            native=unreal.get_default_object(gs)
            cam=native.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.CameraActor,cam_transform,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
            native.call_method('FinishSpawningActor',(cam,cam_transform,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
            cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(cam.get_actor_location(),unreal.Vector(1190,-620,134)),False)
            pc.set_view_target_with_blend(cam,0)
            hud.set_editor_property('show_hud',False);hero.get_editor_property('Health_Widget').set_visibility(unreal.SlateVisibility.HIDDEN)
            state['camera']=cam;next_stage(now)
        elif stage==9 and now-state['at']>2.5:
            shot('estanque');next_stage(now)
        elif stage==10 and now-state['at']>.4:
            cam=state['camera'];cam.set_actor_location(unreal.Vector(1750,-2130,220),False,True)
            cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(cam.get_actor_location(),unreal.Vector(1450,-1750,225)),False)
            next_stage(now)
        elif stage==11 and now-state['at']>1.5:
            shot('arbol');next_stage(now)
        elif stage==12 and now-state['at']>.4:
            finish()
    except Exception:finish(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(check)
level.editor_request_begin_play()
