"""Compile and save delivery assets while preserving original enemy appearance."""
import unreal
AI='/Game/ThirdPerson/Blueprints/EnemigoIA/'
DELIVERY='/Game/ThirdPerson/Blueprints/Entrega/'
animation=unreal.load_asset(AI+'ABP_EnemyEntrega')
animation.modify()
unreal.get_default_object(animation.generated_class()).set_editor_property('root_motion_mode',unreal.RootMotionMode.IGNORE_ROOT_MOTION)
unreal.EditorAssetLibrary.save_loaded_asset(animation,only_if_is_dirty=False)
names=['BP_BaseEnemy','BTTask_Attack','BTTask_HitSun','ABP_EnemyEntrega','BP_ChargerEnemy','BP_ChargerController','BTService_ChargerSense','BTTask_ChargerWindup','BTTask_ChargerCharge','BTTask_ChargerRetreat','BTTask_ChargerRecover']
sub=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
for folder,items in [(AI,names),(DELIVERY,['BP_PlayerEntrega','BP_CombatZone','BP_DirectorEntrega','BP_HUD_Entrega','BP_GameMode_Entrega'])]:
    for name in items:
        bp=unreal.load_asset(folder+name)
        if name.startswith(('BTTask_Charger','BP_PlayerEntrega','BP_CombatZone')):unreal.BlueprintEditorLibrary.remove_unused_variables(bp)
        unreal.BlueprintEditorLibrary.compile_blueprint(bp)
        unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
        sub.close_all_editors_for_asset(bp)
sub.close_all_editors_for_asset(unreal.load_asset(AI+'BT_Charger'))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('COMBAT_DELIVERY_SAVED')
