"""Integra el sobreviviente existente; el paquete original permanece intacto."""
import unreal, os, json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
folder='/Game/ThirdPerson/Blueprints/Aliado/'
target='/Game/ThirdPerson/Characters/Rehen/'
src='/Game/Survival_Character/Meshes/SK_Survival_Character'
mesh=unreal.load_asset(target+'SK_RehenSuperviviente') or unreal.EditorAssetLibrary.duplicate_asset(src,target+'SK_RehenSuperviviente')
skeleton=unreal.load_asset(target+'SKEL_RehenSuperviviente') or unreal.EditorAssetLibrary.duplicate_asset('/Game/Survival_Character/Meshes/SKEL_Survival_Character',target+'SKEL_RehenSuperviviente')
assert unreal.DeliveryBlueprintBuilder.set_property_text(mesh,'Skeleton',skeleton.get_path_name())
# El pack contiene el mismo rig Manny. Compatibilidad explícita en la copia del
# proyecto, sin cambiar el esqueleto ni las animaciones del proveedor.
skeleton.add_compatible_skeleton(unreal.load_asset('/Game/Characters/Mannequins/Meshes/SK_Mannequin'))
anim=unreal.load_asset(folder+'ABP_RehenSuperviviente') or unreal.EditorAssetLibrary.duplicate_asset(folder+'ABP_Hostage',folder+'ABP_RehenSuperviviente')
assert unreal.DeliveryBlueprintBuilder.set_property_text(anim,'TargetSkeleton',skeleton.get_path_name())
unreal.BlueprintEditorLibrary.compile_blueprint(anim)
bp=unreal.load_asset(folder+'BP_Hostage');bp.modify()
cdo=unreal.get_default_object(bp.generated_class())
cdo.mesh.set_skeletal_mesh_asset(mesh)
cdo.mesh.set_anim_instance_class(anim.generated_class())
cdo.mesh.set_editor_property('relative_location',unreal.Vector(0,0,-88))
cdo.mesh.set_editor_property('relative_rotation',unreal.Rotator(yaw=-90))
for asset in [skeleton,mesh,anim,bp]:unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
 if a.get_class()==bp.generated_class():
  a.modify();a.mesh.set_skeletal_mesh_asset(mesh);a.mesh.set_anim_instance_class(cdo.mesh.anim_class)
  a.mesh.set_editor_property('relative_location',unreal.Vector(0,0,-88))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('SURVIVOR_HOSTAGE_READY '+mesh.get_path_name())
