"""PIE: sustained movement into three walls, escape, and spring-arm retraction/recovery."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);controller=p.get_controller()
arm=p.get_editor_property('CameraBoom');camera=p.get_editor_property('TPC')
assert arm.get_editor_property('probe_size')==24 and arm.get_editor_property('do_collision_test')
start=unreal.Vector(0,-560,100)
p.set_actor_location(start,False,True)
state={'stage':'push','index':0,'at':unreal.GameplayStatics.get_time_seconds(w),'handle':None,'results':[]}
directions=[unreal.Vector(0,1,0),unreal.Vector(1,0,0),unreal.Vector(-1,0,0)]
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
def observe_wall(delta,world=w,player=p,s=state,dirs=directions,origin=start,boom=arm,cam=camera,ctrl=controller,root=project):
    try:
        now=unreal.GameplayStatics.get_time_seconds(world);elapsed=now-s['at']
        if s['stage']=='push':
            player.character_movement.add_input_vector(dirs[s['index']],True)
            if elapsed>=3:
                pos=player.get_actor_location()
                assert pos.distance(origin)>200,'Movement did not execute'
                # Imported entry walls stand at y=-26 and x around +/-900.
                assert pos.y < -60 and abs(pos.x)<1000,'Player crossed the wall: '+str(pos)
                s['contact']=pos;s.update(stage='escape',at=now)
        elif s['stage']=='escape':
            player.character_movement.add_input_vector(dirs[s['index']]*-1,True)
            if elapsed>=1:
                distance=player.get_actor_location().distance(s['contact']);assert distance>200,'Player remained stuck'
                s['results'].append({'direction':s['index'],'escaped_cm':round(distance,1),'contact':[s['contact'].x,s['contact'].y,s['contact'].z]})
                s['index']+=1
                player.character_movement.stop_movement_immediately()
                if s['index']<len(dirs):player.set_actor_location(origin,False,True);s.update(stage='push',at=now)
                else:
                    player.set_actor_location(unreal.Vector(0,-90,100),False,True);ctrl.set_control_rotation(unreal.Rotator(pitch=0,yaw=-90,roll=0));s.update(stage='camera_wall',at=now)
        elif s['stage']=='camera_wall' and elapsed>=1:
            pos=cam.get_world_location();distance=pos.distance(boom.get_world_location())
            assert pos.y<-48 and distance<100,(str(pos),distance)
            s['retracted_cm']=round(distance,1);ctrl.set_control_rotation(unreal.Rotator(pitch=0,yaw=90,roll=0));s.update(stage='camera_clear',at=now)
        elif s['stage']=='camera_clear' and elapsed>=1:
            distance=cam.get_world_location().distance(boom.get_world_location());assert distance>340,distance
            result={'passed':True,'walls':s['results'],'retracted_cm':s['retracted_cm'],'recovered_cm':round(distance,1),'probe_cm':24}
            with open(os.path.join(root,'Intermediate/inspect/wall_camera_assertions.json'),'w') as f:json.dump(result,f,indent=2)
            unreal.unregister_slate_post_tick_callback(s['handle']);unreal.log('WALL_CAMERA_ASSERTIONS_PASSED '+json.dumps(result));return
    except Exception:
        unreal.unregister_slate_post_tick_callback(s['handle'])
        with open(os.path.join(root,'Intermediate/inspect/wall_camera_assertions.json'),'w') as f:json.dump({'passed':False,'stage':s['stage'],'error':traceback.format_exc()},f,indent=2)
        unreal.log_error(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(observe_wall)
unreal.log('WALL_CAMERA_ASSERTIONS_STARTED')
