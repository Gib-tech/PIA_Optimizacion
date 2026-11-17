import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());R='/Game/ThirdPerson/Blueprints/Entrega/'
for path in [R+n for n in ['BP_SistemasComplementarios','BP_DeliverySaveManager','BP_DeliveryInterface','BP_HUD_Entrega','BP_PlayerEntrega','BP_DirectorEntrega']]+['/Game/ThirdPerson/Cinematics/BP_CinematicDirector']:
 bp=unreal.load_asset(path);name=bp.get_name();unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
 assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs',name+'.t3d')),name
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
for path in ['/Game/Menu/Menu_Opciones','/Game/Menu/Menu_Pausa','/Game/Menu/Menu_Inicio']:
 bp=unreal.load_asset(path);unreal.BlueprintEditorLibrary.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('RUBRIC_SYSTEMS_INSTALLED')
