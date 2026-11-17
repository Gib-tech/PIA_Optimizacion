"""El canal de visibilidad de la cápsula enemiga recibe el pulso, con oclusión."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
for name in ['BP_BaseEnemy','BP_ChargerEnemy']:
 bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/EnemigoIA/'+name);bp.modify()
 cdo=unreal.get_default_object(bp.generated_class());cdo.capsule_component.modify()
 cdo.capsule_component.set_collision_response_to_channel(unreal.CollisionChannel.ECC_VISIBILITY,unreal.CollisionResponseType.ECR_BLOCK)
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.log('PULSE_ENEMY_VISIBILITY_READY')
