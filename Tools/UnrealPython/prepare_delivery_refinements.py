"""Editable balance and world-space guidance shells for the delivery map."""
import unreal
AI='/Game/ThirdPerson/Blueprints/EnemigoIA/'
ROOT='/Game/ThirdPerson/Blueprints/Entrega/'
lib=unreal.BlueprintEditorLibrary
bp=unreal.load_asset(AI+'BP_BaseEnemy')
cdo=unreal.get_default_object(bp.generated_class())
try:cdo.get_editor_property('ContactDamage')
except Exception:lib.add_member_variable(bp,'ContactDamage',lib.get_basic_type_by_name('real'))
lib.set_blueprint_variable_instance_editable(bp,'ContactDamage',True)
lib.compile_blueprint(bp)
unreal.get_default_object(bp.generated_class()).set_editor_property('ContactDamage',6.0)
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
for folder,name in [(AI,'BP_BaseEnemy'),(AI,'BP_ChargerEnemy'),('/Game/ThirdPerson/Blueprints/Aliado/','BP_Hostage')]:
    asset=unreal.load_asset(folder+name);cdo=unreal.get_default_object(asset.generated_class())
    cdo.capsule_component.set_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA,unreal.CollisionResponseType.ECR_IGNORE)
    cdo.mesh.set_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA,unreal.CollisionResponseType.ECR_IGNORE)
    unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
tools=unreal.AssetToolsHelpers.get_asset_tools()
for name,variable,typ in [('BP_RehenIndicador','Rehen',unreal.Actor),('BP_ZonaIndicador','Zona',unreal.load_class(None,ROOT+'BP_CombatZone.BP_CombatZone_C'))]:
    if unreal.EditorAssetLibrary.does_asset_exist(ROOT+name):
        asset=unreal.load_asset(ROOT+name)
        text=unreal.get_default_object(asset.generated_class()).get_component_by_class(unreal.TextRenderComponent)
        text.set_world_size(27);text.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
        unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
        continue
    factory=unreal.BlueprintFactory();factory.set_editor_property('parent_class',unreal.TextRenderActor)
    asset=tools.create_asset(name,ROOT,unreal.Blueprint,factory)
    lib.add_member_variable(asset,variable,lib.get_object_reference_type(typ));lib.set_blueprint_variable_instance_editable(asset,variable,True);lib.compile_blueprint(asset)
    cdo=unreal.get_default_object(asset.generated_class());text=cdo.get_component_by_class(unreal.TextRenderComponent)
    text.set_world_size(27);text.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER);text.set_vertical_alignment(unreal.VerticalTextAligment.EVRTA_TEXT_CENTER)
    text.set_text_render_color(unreal.Color(90,220,255,255));text.set_cast_shadow(False)
    tick=cdo.get_editor_property('primary_actor_tick');tick.set_editor_property('tick_interval',.1);cdo.set_editor_property('primary_actor_tick',tick)
    unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
unreal.log('DELIVERY_REFINEMENTS_PREPARED')
