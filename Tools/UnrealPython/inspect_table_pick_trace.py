import unreal,json,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller();cm=gs.get_player_camera_manager(w,0);start=cm.get_camera_location();end=start+unreal.MathLibrary.get_forward_vector(cm.get_camera_rotation())*350
lib=unreal.get_default_object(unreal.SystemLibrary);hit=lib.call_method('LineTraceSingle',(w,start,end,unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[p],unreal.DrawDebugTrace.NONE,True,unreal.LinearColor(1,0,0,1),unreal.LinearColor(0,1,0,1),0.))
unreal.log('PICK_TRACE_RAW '+str(hit))
for h in (hit if isinstance(hit,tuple) else [hit]):
 if isinstance(h,unreal.HitResult):unreal.log('PICK_TRACE_BREAK '+str(unreal.get_default_object(gs).call_method('BreakHitResult',(h,))))
extra=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
item=extra.get_editor_property('ItemMesa3');unreal.log('CREDIT_PHYSICS '+str({'camera':str(start),'rotation':str(cm.get_camera_rotation()),'component':str(unreal.SystemLibrary.get_component_bounds(item.static_mesh_component)),'pos':str(item.get_actor_location()),'profile':str(item.static_mesh_component.get_collision_profile_name()),'enabled':str(item.static_mesh_component.get_collision_enabled())}))
