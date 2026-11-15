"""Editor-side: finish delivery lighting, startup maps and menu mode."""
import unreal
lib=unreal.BlueprintEditorLibrary
assets=unreal.AssetToolsHelpers.get_asset_tools()
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Nivel_Entrega'
for actor in actors.get_all_level_actors():
    if isinstance(actor,unreal.Light):
        actor.get_component_by_class(unreal.LightComponent).set_mobility(unreal.ComponentMobility.MOVABLE)
    elif isinstance(actor,unreal.SkyLight):
        actor.get_component_by_class(unreal.SkyLightComponent).set_mobility(unreal.ComponentMobility.MOVABLE)
world.get_world_settings().set_editor_property('force_no_precomputed_lighting',True)
levels.save_current_level()
path='/Game/ThirdPerson/Blueprints/Entrega/BP_GameMode_Menu'
mode=unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else lib.create_blueprint_asset_with_parent(path,unreal.GameModeBase)
lib.compile_blueprint(mode)
cdo=unreal.get_default_object(mode.generated_class())
cdo.set_editor_property('default_pawn_class',None)
cdo.set_editor_property('hud_class',None)
unreal.EditorAssetLibrary.save_loaded_asset(mode)
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(unreal.load_asset('/Game/Menu/Menu_Inicio'))
levels.load_level('/Game/LevelMenu/MainMenuLevel')
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
world.get_world_settings().set_editor_property('default_game_mode',mode.generated_class())
levels.save_current_level()
unreal.log('DELIVERY_LEVEL_FINALIZED')
