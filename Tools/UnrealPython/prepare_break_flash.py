"""Ráfaga con un plano orientado a cámara y chispas de material emisivo."""
from pathlib import Path
import unreal

folder='/Game/ThirdPerson/Blueprints/Entrega/FX'
tools=unreal.AssetToolsHelpers.get_asset_tools()
assets=unreal.EditorAssetLibrary
edit=unreal.MaterialEditingLibrary
bridge=unreal.DeliveryBlueprintBuilder
name='M_DestellosRotura'
material=unreal.load_asset(folder+'/'+name) if assets.does_asset_exist(folder+'/'+name) else tools.create_asset(name,folder,unreal.Material,unreal.MaterialFactoryNew())
edit.delete_all_material_expressions(material)
material.set_editor_properties({'blend_mode':unreal.BlendMode.BLEND_ADDITIVE,'shading_model':unreal.MaterialShadingModel.MSM_UNLIT,'two_sided':True})
uv=edit.create_material_expression(material,unreal.MaterialExpressionTextureCoordinate,-760,-120)
clock=edit.create_material_expression(material,unreal.MaterialExpressionTime,-760,50)
start=edit.create_material_expression(material,unreal.MaterialExpressionScalarParameter,-760,220)
assert bridge.set_property_text(start,'ParameterName','Inicio')
assert bridge.set_property_text(start,'bUseCustomPrimitiveData','True')
shader=edit.create_material_expression(material,unreal.MaterialExpressionCustom,-280,0)
assert bridge.set_property_text(shader,'Inputs','((InputName="UV"),(InputName="Clock"),(InputName="Start"))')
assert bridge.set_property_text(shader,'OutputType','CMOT_Float3')
shader.set_editor_property('description','Nueve motas incandescentes que se separan y se apagan al romper')
shader.set_editor_property('code',"""
float age = clamp(Clock - Start,0,.65);
float2 pixel = UV*2-1;
float light = 0;
[unroll] for (int i=0;i<9;++i) {
    float seed = frac(sin(i*17.13 + floor(Start*31)) * 15731.7);
    float angle = 6.283185*frac(.618*i + .29*seed);
    float2 dir = float2(cos(angle),sin(angle));
    float2 tip = dir*(.025+age*(.75+1.4*seed)) + float2(0,-age*.8+age*age*2.2);
    float2 d = pixel-tip;
    float along = clamp(dot(d,dir),-(.024+.062*seed),0);
    float dist = length(d-dir*along);
    light += (1-smoothstep(.002,.011,dist))*(1-smoothstep(.09+.16*seed,.39+.18*seed,age));
}
return float3(10,3.9,.8)*light;
""")
for n,key in [(uv,'UV'),(clock,'Clock'),(start,'Start')]:
    assert edit.connect_material_expressions(n,'',shader,key)
assert edit.connect_material_property(shader,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
edit.recompile_material(material);assets.save_loaded_asset(material,False)
factory=unreal.BlueprintFactory();factory.set_editor_property('parent_class',unreal.NiagaraActor)
name='BP_RafagaRotura'
bp=unreal.load_asset(folder+'/'+name) if assets.does_asset_exist(folder+'/'+name) else tools.create_asset(name,folder,unreal.Blueprint,factory)
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lookup=unreal.SubobjectDataBlueprintFunctionLibrary
items=[(h,lookup.get_object(lookup.get_data(h))) for h in sub.k2_gather_subobject_data_for_blueprint(bp)]
sprite=next((c for _,c in items if isinstance(c,unreal.MaterialBillboardComponent)),None)
if not sprite:
    root=next(h for h,c in items if isinstance(c,unreal.NiagaraComponent))
    handle,error=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root,new_class=unreal.MaterialBillboardComponent,blueprint_context=bp))
    assert not str(error) and sub.rename_subobject(handle,unreal.Text('Destellos')),error
    sprite=lookup.get_object(lookup.get_data(handle))
sprite.set_editor_property('relative_location',unreal.Vector(0,0,95))
sprite.set_editor_property('can_ever_affect_navigation',False)
sprite.set_collision_profile_name('NoCollision');sprite.set_cast_shadow(False)
sprite.set_elements([])
sprite.add_element(material,None,False,178.,178.,None)
path=Path(unreal.Paths.project_dir()).resolve()/'Intermediate/inspect/delivery_graphs'
assert bridge.install_graph(bp,str(path/(name+'.t3d')))
assert assets.save_loaded_asset(bp,False)
