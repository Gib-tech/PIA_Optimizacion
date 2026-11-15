"""Compile delivery assets and save the charger's distinct skeletal material."""
import unreal
AI='/Game/ThirdPerson/Blueprints/EnemigoIA/'
DELIVERY='/Game/ThirdPerson/Blueprints/Entrega/'
animation=unreal.load_asset(AI+'ABP_EnemyEntrega')
animation.modify()
unreal.get_default_object(animation.generated_class()).set_editor_property('root_motion_mode',unreal.RootMotionMode.IGNORE_ROOT_MOTION)
unreal.EditorAssetLibrary.save_loaded_asset(animation,only_if_is_dirty=False)
path=DELIVERY+'M_Armadura_Embestidor'
if unreal.EditorAssetLibrary.does_asset_exist(path):material=unreal.load_asset(path)
else:
    material=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_Armadura_Embestidor',DELIVERY,unreal.Material,unreal.MaterialFactoryNew())
    color=unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionConstant3Vector,-300,0)
    color.set_editor_property('constant',unreal.LinearColor(0.8,0.09,0.015,1))
    unreal.MaterialEditingLibrary.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR)
material.set_editor_property('used_with_skeletal_mesh',True)
unreal.MaterialEditingLibrary.recompile_material(material)
unreal.EditorAssetLibrary.save_loaded_asset(material,only_if_is_dirty=False)
charger=unreal.load_asset(AI+'BP_ChargerEnemy')
unreal.get_default_object(charger.generated_class()).mesh.set_material(0,material)
unreal.EditorAssetLibrary.save_loaded_asset(charger,only_if_is_dirty=False)
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
