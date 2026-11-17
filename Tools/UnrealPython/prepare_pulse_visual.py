"""Construye los materiales emisivos, el frente móvil y la estela del pulso."""
from pathlib import Path
import sys
import unreal

root = Path(unreal.Paths.project_dir()).resolve()
sys.path.insert(0, str(root/'Tools/UnrealPython'))
from generate_pulse_visual import build

assets = unreal.EditorAssetLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()
edit = unreal.MaterialEditingLibrary
bridge = unreal.DeliveryBlueprintBuilder
folder = '/Game/ThirdPerson/Environment/Complementos/Materials'
bp_folder = '/Game/ThirdPerson/Blueprints/Entrega'


def material(name, description, shader_code):
    path = folder + '/' + name
    mat = unreal.load_asset(path) if assets.does_asset_exist(path) else tools.create_asset(
        name, folder, unreal.Material, unreal.MaterialFactoryNew())
    edit.delete_all_material_expressions(mat)
    mat.set_editor_properties({'blend_mode': unreal.BlendMode.BLEND_ADDITIVE,
                               'shading_model': unreal.MaterialShadingModel.MSM_UNLIT})
    uv = edit.create_material_expression(mat, unreal.MaterialExpressionTextureCoordinate, -650, -130)
    clock = edit.create_material_expression(mat, unreal.MaterialExpressionTime, -650, 50)
    start = edit.create_material_expression(mat, unreal.MaterialExpressionScalarParameter, -650, 220)
    assert bridge.set_property_text(start, 'ParameterName', 'InicioDisparo')
    assert bridge.set_property_text(start, 'bUseCustomPrimitiveData', 'True')
    shader = edit.create_material_expression(mat, unreal.MaterialExpressionCustom, -220, 0)
    assert bridge.set_property_text(shader, 'Inputs', '((InputName="UV"),(InputName="Clock"),(InputName="Start"))')
    assert bridge.set_property_text(shader, 'OutputType', 'CMOT_Float3')
    shader.set_editor_properties({'description': description, 'code': shader_code})
    for node, pin in ((uv, 'UV'), (clock, 'Clock'), (start, 'Start')):
        assert edit.connect_material_expressions(node, '', shader, pin)
    exposure = edit.create_material_expression(mat, unreal.MaterialExpressionEyeAdaptationInverse, 60, 0)
    light_pin = edit.get_material_expression_input_names(exposure)[0]
    assert edit.connect_material_expressions(shader, '', exposure, light_pin)
    assert edit.connect_material_property(exposure, '', unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    edit.recompile_material(mat)
    assert assets.save_loaded_asset(mat, False)
    return mat


def prepare():
    trail = material('M_PulsoEnergia', 'Estela breve de la descarga', """
float t = max(0, Clock - Start);
float edge = smoothstep(0, .12, UV.y) * (1 - smoothstep(.88, 1, UV.y));
return float3(.15, 3.0, 5.5) * (.22 + .78 * edge) * (1 - smoothstep(.045, .29, t));
""")
    wave = material('M_FrentePulso', 'Núcleo en vuelo y dos ondas de disipación', """
float age = max(0, Clock - Start);
float r = length(UV * 2 - 1);
float arrival = saturate((age - .18) / .32);
float core = (1 - smoothstep(.04, .21, r)) * (1 - smoothstep(.18, .32, age));
float glow = exp(-9 * r) * (1 - smoothstep(.18, .38, age));
float radius = lerp(.17, .93, 1 - (1-arrival)*(1-arrival));
float ring = 1 - smoothstep(.012, .065, abs(r - radius));
float echo = 1 - smoothstep(.008, .04, abs(r - radius*.71));
float envelope = smoothstep(.15, .20, age) * (1 - smoothstep(.28, .5, age));
return float3(6, 9, 11)*core + float3(.12, 3, 7)*(glow + (ring + .45*echo)*envelope);
""")
    name = 'BP_PulsoTemporalVisual'
    path = bp_folder + '/' + name
    if assets.does_asset_exist(path):
        bp = unreal.load_asset(path)
    else:
        factory = unreal.BlueprintFactory()
        factory.set_editor_property('parent_class', unreal.StaticMeshActor)
        bp = tools.create_asset(name, bp_folder, unreal.Blueprint, factory)
    sub = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    lookup = unreal.SubobjectDataBlueprintFunctionLibrary
    parts = [(h, lookup.get_object(lookup.get_data(h))) for h in sub.k2_gather_subobject_data_for_blueprint(bp)]
    front = next((c for _, c in parts if isinstance(c, unreal.MaterialBillboardComponent)), None)
    if front is None:
        parent = next(h for h, c in parts if isinstance(c, unreal.StaticMeshComponent))
        handle, error = sub.add_new_subobject(unreal.AddNewSubobjectParams(
            parent_handle=parent, new_class=unreal.MaterialBillboardComponent, blueprint_context=bp))
        assert not str(error) and sub.rename_subobject(handle, unreal.Text('Frente')), error
        front = lookup.get_object(lookup.get_data(handle))
    front.set_editor_properties({'relative_location': unreal.Vector(-48, 0, 0), 'absolute_scale': True,
                                 'can_ever_affect_navigation': False})
    front.set_mobility(unreal.ComponentMobility.MOVABLE)
    front.set_collision_profile_name('NoCollision')
    front.set_cast_shadow(False)
    front.set_elements([])
    front.add_element(wave, None, False, 43, 43, None)
    import generate_delivery_graphs
    generate_delivery_graphs.OUT = str(root/'Intermediate/inspect/delivery_graphs')
    Path(generate_delivery_graphs.OUT).mkdir(parents=True, exist_ok=True)
    build()
    assert bridge.install_graph(bp, str(root/'Intermediate/inspect/delivery_graphs'/f'{name}.t3d'))
    assert bridge.set_property_text(bp, 'BlueprintDescription',
        'Frente luminoso móvil y estela del pulso. A los 0,18 s el frente se abre en dos ondas. El actor expira a los 0,52 s.')
    cdo = unreal.get_default_object(bp.generated_class())
    cdo.set_editor_property('initial_life_span', .52)
    mesh = cdo.static_mesh_component
    mesh.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'))
    mesh.set_material(0, trail)
    mesh.set_collision_profile_name('NoCollision')
    mesh.set_cast_shadow(False)
    mesh.set_editor_property('can_ever_affect_navigation', False)
    assert assets.save_loaded_asset(bp, False)


if __name__ == '__main__':
    prepare()
