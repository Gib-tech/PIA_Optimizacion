import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega')
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs/BP_PlayerEntrega.t3d'))
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('FIRST_PERSON_INSTALLED')
