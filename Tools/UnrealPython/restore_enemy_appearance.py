"""Restore the team's original warrior mesh/materials, preserving the delivery animation graph."""
import unreal
root='/Game/ThirdPerson/Blueprints/EnemigoIA/'
mesh=unreal.load_asset('/Game/SciFiWarrior02/Meshes/SK_SciFiWarrior02')
anim=unreal.load_class(None,root+'ABP_EnemyEntrega.ABP_EnemyEntrega_C')
for name in ['BP_BaseEnemy','BP_ChargerEnemy']:
    bp=unreal.load_asset(root+name);bp.modify()
    cdo=unreal.get_default_object(bp.generated_class())
    cdo.mesh.set_skeletal_mesh_asset(mesh)
    cdo.mesh.set_anim_instance_class(anim)
    cdo.mesh.set_editor_property('override_materials',[])
    cdo.mesh.set_relative_scale3d(unreal.Vector(1,1,1))
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
    unreal.log('RESTORED_ENEMY_APPEARANCE '+name+' '+mesh.get_path_name())
