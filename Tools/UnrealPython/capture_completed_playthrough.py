import unreal,os,json
cw=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert cw
cd=unreal.GameplayStatics.get_actor_of_class(cw,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'));assert cd.get_editor_property('Paso')==4
unreal.SystemLibrary.execute_console_command(cw,'HighResShot 1280x720 filename="'+os.path.join(unreal.Paths.project_dir(),'docs/validation/partida-completa/victoria.png').replace('\\','/')+'"')
unreal.log('NATURAL_PLAYTHROUGH_VICTORY_CAPTURE')
