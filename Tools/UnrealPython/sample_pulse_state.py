import unreal,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs=unreal.GameplayStatics
extras=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
p=gs.get_player_character(w,0);pc=gs.get_player_controller(w,0)
enemies=gs.get_all_actors_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C'))
unreal.log('PULSE_SAMPLE '+json.dumps({'charges':extras.get_editor_property('Cargas'),'last':extras.get_editor_property('LastPulseAt'),'player_attack':p.get_editor_property('IsAttacking'),'camera':str(pc.player_camera_manager.get_camera_location()),'camera_rot':str(pc.player_camera_manager.get_camera_rotation()),'player':str(p.get_actor_location()),'enemies':[{'position':str(e.get_actor_location()),'hp':e.get_editor_property('BPC_E_Health').get_editor_property('E_Health')} for e in enemies]}))
