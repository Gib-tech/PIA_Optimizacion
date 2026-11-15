"""Editor-side: match Ian's door height to the player capsule; restore source materials."""
import unreal
ROOT='/Game/ThirdPerson/Environment/EscenarioIan'
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Nivel_Entrega'
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    if a.get_actor_label().startswith('Ian_Sector_'):
        a.set_actor_scale3d(unreal.Vector(2,2,2))
assignments={'Sector1':'wood_inlaid_stone_wall_diff_2k','Sector2':'rock_boulder_dry_diff_2k',
             'Sector3':'wood_inlaid_stone_wall_diff_2k','Sector4':'rock_wall_16_diff_2k'}
for material_name, texture_name in assignments.items():
    material=unreal.load_asset(ROOT+'/'+material_name)
    # The one texture sample was created by build_delivery_level.py.
    expression=unreal.find_object(None,material.get_path_name()+':MaterialExpressionTextureSample_0')
    if expression:
        expression.texture=unreal.load_asset(ROOT+'/Textures/'+texture_name)
    else:
        unreal.MaterialEditingLibrary.delete_all_material_expressions(material)
        expression=unreal.MaterialEditingLibrary.create_material_expression(material,unreal.MaterialExpressionTextureSample,-400,0)
        expression.texture=unreal.load_asset(ROOT+'/Textures/'+texture_name)
        unreal.MaterialEditingLibrary.connect_material_property(expression,'RGB',unreal.MaterialProperty.MP_BASE_COLOR)
    unreal.MaterialEditingLibrary.recompile_material(material)
    unreal.EditorAssetLibrary.save_loaded_asset(material)
unreal.SystemLibrary.execute_console_command(world,'RebuildNavigation')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('DELIVERY_CLEARANCE height scale=2; source doorway 1.289m becomes 2.578m')
