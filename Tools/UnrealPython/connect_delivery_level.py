"""Editor-side: connect saved gameplay Blueprints to the delivery map only."""
import unreal
ROOT='/Game/ThirdPerson/Blueprints/Entrega'
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Nivel_Entrega'
for name in ['BP_DirectorEntrega','BP_HUD_Entrega']:
    unreal.EditorAssetLibrary.save_asset(ROOT+'/'+name)
mode=unreal.load_asset(ROOT+'/BP_GameMode_Entrega') if unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/BP_GameMode_Entrega') else unreal.EditorAssetLibrary.duplicate_asset('/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode',ROOT+'/BP_GameMode_Entrega')
assert mode, 'Delivery mode duplicate failed'
unreal.BlueprintEditorLibrary.compile_blueprint(mode)
cdo=unreal.get_default_object(mode.generated_class())
cdo.set_editor_property('hud_class',unreal.load_class(None,ROOT+'/BP_HUD_Entrega.BP_HUD_Entrega_C'))
unreal.EditorAssetLibrary.save_loaded_asset(mode)
world.get_world_settings().set_editor_property('default_game_mode',mode.generated_class())
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
director=placed.get('Director_Entrega') or actors.spawn_actor_from_class(unreal.load_class(None,ROOT+'/BP_DirectorEntrega.BP_DirectorEntrega_C'),unreal.Vector(0,-500,100))
director.set_actor_label('Director_Entrega')
director.set_folder_path('Objetivos')
for key,label in [('Baliza1','Baliza_01'),('Baliza2','Baliza_02'),('Baliza3','Baliza_03'),('Salida','Salida_Extraccion')]:
    director.set_editor_property(key,placed[label])
unreal.SystemLibrary.execute_console_command(world,'ShowFlag.Navigation 0')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('DELIVERY_CONNECTED director_input=%s mode=%s' % (director.get_editor_property('auto_receive_input'),mode.get_path_name()))
