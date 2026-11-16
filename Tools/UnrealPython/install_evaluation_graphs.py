import unreal,os
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/'
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
for path in [R+'BP_DestruibleEntrega',R+'BP_PlayerEntrega',R+'BP_DirectorEntrega',R+'BP_DeliveryInterface','/Game/Menu/Menu_Pausa','/Game/Menu/Menu_Opciones','/Game/Menu/Menu_Inicio']:
 bp=unreal.load_asset(path)
 unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
 assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs',bp.get_name()+'.t3d')),path
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 unreal.log('EVALUATION_INSTALLED '+path)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
