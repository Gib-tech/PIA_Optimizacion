import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios');cdo=unreal.get_default_object(bp.generated_class())
for obj in [cdo]+[a for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors() if a.get_class()==bp.generated_class()]:
 obj.modify();obj.set_editor_property('auto_receive_input',unreal.AutoReceiveInput.PLAYER0);obj.set_editor_property('input_priority',5)
assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/delivery_graphs/BP_SistemasComplementarios.t3d'))
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False);unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('PLACED_SYSTEM_INPUT_FIXED')
