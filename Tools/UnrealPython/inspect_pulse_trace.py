import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=gs.get_player_controller(w,0)
start=pc.player_camera_manager.get_camera_location();rot=pc.player_camera_manager.get_camera_rotation();end=start+unreal.MathLibrary.get_forward_vector(rot)*800
result=unreal.SystemLibrary.sphere_trace_single(w,start,end,18,unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[p],unreal.DrawDebugTrace.NONE,True)
unreal.log('PULSE_TRACE '+str(result))
for e in gs.get_all_actors_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')):
 unreal.log('PULSE_ENEMY '+str(e.get_actor_location())+' capsule='+str(e.capsule_component.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY))+' mesh='+str(e.mesh.get_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY)))
