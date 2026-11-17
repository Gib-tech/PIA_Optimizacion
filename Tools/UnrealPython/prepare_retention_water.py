"""Captación pluvial con conducto de retorno, cubeta transitable y ondas en el contacto."""
import unreal

world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
bridge=unreal.DeliveryBlueprintBuilder
assert world.get_name()=='Nivel_Entrega' and not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bridge.load_editor_region(world,unreal.Vector(-6500,-12500,-1000),unreal.Vector(6500,1500,7000))
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
surface=placed['Lago_Retencion_Agua'];rim=placed['Lago_Retencion_Borde']
origin=surface.get_actor_location()
cx,cy=origin.x,origin.y
for a,z in [(surface,23.),(rim,20.)]:
    a.modify();a.set_actor_location(unreal.Vector(cx,cy,z),False,True)
# La colisión convexa del FBX tapaba toda la boca. Usar el borde y el fondo reales.
rim_mesh=rim.static_mesh_component.static_mesh
body=rim_mesh.get_editor_property('body_setup');body.modify()
body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
unreal.EditorAssetLibrary.save_loaded_asset(rim_mesh,False)

folder='/Game/ThirdPerson/Environment/Complementos/Materials'
assets=unreal.EditorAssetLibrary
material=unreal.load_asset(folder+'/M_AguaRetencion')
edit=unreal.MaterialEditingLibrary
edit.delete_all_material_expressions(material)
material.modify();material.set_editor_property('two_sided',False)
# Iluminación de superficie por volumen, sin coste de luces locales por píxel.
material.set_editor_property('translucency_lighting_mode',unreal.TranslucencyLightingMode.TLM_SURFACE)
def node(cls,x,y):return edit.create_material_expression(material,cls,x,y)
def wire(a,out,b,pin):assert edit.connect_material_expressions(a,out,b,pin),pin
def connect(a,out,prop):assert edit.connect_material_property(a,out,prop)
for prop,value,y in [(unreal.MaterialProperty.MP_ROUGHNESS,.19,0),(unreal.MaterialProperty.MP_SPECULAR,.58,140),(unreal.MaterialProperty.MP_OPACITY,.78,280)]:
    n=node(unreal.MaterialExpressionConstant,-230,y);n.r=value;connect(n,'',prop)
panner=node(unreal.MaterialExpressionPanner,-980,-350)
for key,v in [('SpeedX','.018'),('SpeedY','.012')]:assert bridge.set_property_text(panner,key,v)
sample=node(unreal.MaterialExpressionTextureSample,-720,-350)
sample.texture=unreal.load_asset('/Game/ParagonKallari/FX/Textures/Water/T_Water_N');sample.sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL
wire(panner,'',sample,'UVs');connect(sample,'RGB',unreal.MaterialProperty.MP_NORMAL)
inputs=[
 ('PositionWS',unreal.MaterialExpressionWorldPosition,'XYZ'),('Center',unreal.MaterialExpressionObjectPositionWS,''),
 ('Foot',unreal.MaterialExpressionVectorParameter,''),('GameTime',unreal.MaterialExpressionTime,''),
 ('StartTime',unreal.MaterialExpressionScalarParameter,'')]
wave=node(unreal.MaterialExpressionCustom,-360,550)
assert bridge.set_property_text(wave,'Inputs','('+','.join('(InputName="'+name+'")' for name,_,_ in inputs)+')')
assert bridge.set_property_text(wave,'OutputType','CMOT_Float3')
wave.set_editor_property('description','Ondas del retorno y del último paso, en centímetros y segundos')
wave.set_editor_property('code',"""
float age = max(0, GameTime - StartTime);
float r = distance(PositionWS.xy, Foot.xy);
float front = r - 115 * age;
float stepWave = exp(-0.003 * front * front) * (0.5 + 0.5*cos(front*.48)) * saturate(1-age/1.7);
float inletDist = distance(PositionWS.xy, Center.xy + float2(225,0));
float inlet = exp(-inletDist*.025) * pow(.5 + .5*cos(inletDist*.27-GameTime*5), 3);
return lerp(float3(.014,.095,.112), float3(.25,.55,.53), saturate(stepWave + .65*inlet));
""")
for i,(name,cls,out) in enumerate(inputs):
    n=node(cls,-910,330+i*160)
    if name in ['Foot','StartTime']:
        assert bridge.set_property_text(n,'ParameterName','Origen' if name=='Foot' else 'Inicio')
        if name=='StartTime':assert bridge.set_property_text(n,'DefaultValue','-10')
    wire(n,out,wave,name)
connect(wave,'',unreal.MaterialProperty.MP_BASE_COLOR);edit.recompile_material(material)
assert assets.save_loaded_asset(material,False)
cylinder=unreal.load_asset('/Engine/BasicShapes/Cylinder')
metal=unreal.load_asset(folder+'/M_Apoyo_Metal')
def pipe(label,x,z,length,diameter,horizontal=False,mat=metal):
    label='Estanque_'+label
    a=placed.get(label) or actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(cx+x,cy,z))
    a.modify();a.set_actor_label(label);a.set_folder_path('Entrega/Complementos/Estanque')
    a.set_editor_property('is_spatially_loaded',False);a.set_actor_location(unreal.Vector(cx+x,cy,z),False,True)
    a.set_actor_rotation(unreal.Rotator(pitch=90 if horizontal else 0),False)
    a.set_actor_scale3d(unreal.Vector(diameter/100,diameter/100,length/100))
    c=a.static_mesh_component;c.modify();c.set_static_mesh(cylinder);c.set_material(0,mat)
    c.set_collision_profile_name('NoCollision');c.set_editor_property('can_ever_affect_navigation',False)
    c.set_editor_property('ld_max_draw_distance',5000.);c.set_cast_shadow(mat==metal)
pipe('Bajante',725,292,450,16)
pipe('Colector',475,74,500,16,True)
pipe('Boquilla',225,63,23,18)
# Material independiente para que el chorro no repita las ondas horizontales.
stream=unreal.load_asset(folder+'/M_Retorno')
if not stream:
    stream=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_Retorno',folder,unreal.Material,unreal.MaterialFactoryNew())
    stream.set_editor_property('blend_mode',unreal.BlendMode.BLEND_TRANSLUCENT)
    color=edit.create_material_expression(stream,unreal.MaterialExpressionConstant3Vector,-240,0);color.constant=unreal.LinearColor(.12,.30,.32,1)
    edit.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR)
    alpha=edit.create_material_expression(stream,unreal.MaterialExpressionConstant,-240,130);alpha.r=.43
    edit.connect_material_property(alpha,'',unreal.MaterialProperty.MP_OPACITY)
    edit.recompile_material(stream);assert assets.save_loaded_asset(stream,False)
pipe('Retorno',225,38,32,8,mat=stream)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
if dirty:assert unreal.EditorLoadingAndSavingUtils.save_packages(dirty,True)
