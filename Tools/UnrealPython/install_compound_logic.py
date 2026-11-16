import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_DestruibleEntrega')
assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/delivery_graphs/BP_DestruibleEntrega.t3d'))
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('COMPOUND_DESTRUCTION_PHYSICS_ON_DEMAND')
