"""Instalar la revisión de presentación en Nivel_Entrega con el helper de editor."""
from pathlib import Path
import re
import unreal

root=Path(unreal.Paths.project_dir()).resolve()
es=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
world=es.get_editor_world()
assert world.get_name()=='Nivel_Entrega' and not es.get_game_world()
bridge=unreal.DeliveryBlueprintBuilder
assert bridge.load_editor_region(world,unreal.Vector(-6500,-12500,-1200),unreal.Vector(6500,1500,7000))
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assets=unreal.EditorAssetLibrary
lib=unreal.BlueprintEditorLibrary
tools=unreal.AssetToolsHelpers.get_asset_tools()
edit=unreal.MaterialEditingLibrary
base='/Game/ThirdPerson/Blueprints/Entrega/'
art='/Game/ThirdPerson/Environment/Evaluation'
def save(obj):assert assets.save_loaded_asset(obj,False),obj.get_name()
def load_or_create(name,folder,cls,factory):
    return unreal.load_asset(folder+'/'+name) if assets.does_asset_exist(folder+'/'+name) else tools.create_asset(name,folder,cls,factory)
def import_file(path,folder):
    t=unreal.AssetImportTask();t.filename=str(path);t.destination_path=folder
    t.automated=True;t.replace_existing=True;t.save=True;tools.import_asset_tasks([t])
    assert t.imported_object_paths,str(path)
    return unreal.load_asset(t.imported_object_paths[0])
for name in ['SW_HostageAlarm','SW_PasoAgua']:
    import_file(root/'Tools/AudioSource'/(name+'.wav'),'/Game/ThirdPerson/Audio')
tree=unreal.load_asset(art+'/SM_LOD_Tree1')
fn=unreal.load_asset('/Engine/Functions/Engine_MaterialFunctions01/Texturing/WorldAlignedTexture')
for slot,name,size in [(0,'FollajeAcceso',95.),(1,'CortezaAcceso',62.)]:
    texture=import_file(root/'Tools/ArtSource/ArbolAcceso'/('T_'+name+'.png'),art)
    material=load_or_create('M_'+name,art,unreal.Material,unreal.MaterialFactoryNew())
    edit.delete_all_material_expressions(material)
    sample=edit.create_material_expression(material,unreal.MaterialExpressionTextureObject,-500,0);sample.texture=texture
    metric=edit.create_material_expression(material,unreal.MaterialExpressionConstant3Vector,-500,180)
    metric.constant=unreal.LinearColor(size,size,size,1)
    mapping=edit.create_material_expression(material,unreal.MaterialExpressionMaterialFunctionCall,-200,0);mapping.set_editor_property('material_function',fn)
    assert edit.connect_material_expressions(sample,'',mapping,'TextureObject') and edit.connect_material_expressions(metric,'',mapping,'TextureSize')
    assert edit.connect_material_property(mapping,'XYZ Texture',unreal.MaterialProperty.MP_BASE_COLOR)
    rough=edit.create_material_expression(material,unreal.MaterialExpressionConstant,-200,200);rough.r=.87
    edit.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
    material.set_editor_property('two_sided',slot==0);edit.recompile_material(material);save(material)
    tree.modify();tree.set_material(slot,material)
save(tree)

# Quitar únicamente la cadena del daño de prueba en el EventGraph heredado.
parent=unreal.load_asset('/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter')
out=root/'Intermediate/inspect/parent-polish.t3d'
task=unreal.AssetExportTask();task.object=parent;task.filename=str(out);task.automated=True;task.prompt=False;task.replace_identical=True
assert unreal.Exporter.run_asset_export_task(task)
raw=out.read_bytes();source=raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig')
# La exportación puede conservar objetos huérfanos. Sólo Nodes(...) contiene
# las entradas vivas. Comprobar la tecla y el destino antes de retirar la cadena.
if re.search(r'''Nodes\(\d+\)="[^"]*'K2Node_InputDebugKey_0'"''',source):
    def graph_node(name):
        match=re.search(r'Begin Object Name="'+name+r'" [^\n]*:EventGraph\.'+name+r"""'".*?End Object""",source,re.S)
        assert match,name
        return match.group()
    key=graph_node('K2Node_InputDebugKey_0')
    damage=graph_node('K2Node_CallFunction_47')
    assert 'InputKey=One' in key and 'LinkedTo=(K2Node_CallFunction_47 ' in key
    assert 'MemberName="Decrease_Health"' in damage and 'LinkedTo=(K2Node_VariableGet_20 ' in damage
    assert bridge.remove_graph_nodes(parent,['K2Node_InputDebugKey_0','K2Node_CallFunction_47','K2Node_VariableGet_20'])==3
    save(parent)
label=unreal.load_asset(base+'BP_BeaconLabel')
cinema=unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C')
try:unreal.get_default_object(label.generated_class()).get_editor_property('DirectorDeCine')
except Exception:assert lib.add_member_variable(label,'DirectorDeCine',lib.get_object_reference_type(cinema))
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);lookup=unreal.SubobjectDataBlueprintFunctionLibrary
def components(bp):
    return [(h,lookup.get_object(lookup.get_data(h))) for h in sub.k2_gather_subobject_data_for_blueprint(bp)]
items=components(label)
board=next((obj for _,obj in items if obj.get_name().startswith('FondoRotulo')),None)
if not board:
    h=next(h for h,obj in items if isinstance(obj,unreal.TextRenderComponent))
    new,error=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=h,new_class=unreal.StaticMeshComponent,blueprint_context=label))
    assert not str(error) and sub.rename_subobject(new,unreal.Text('FondoRotulo')),error
    board=lookup.get_object(lookup.get_data(new))
board.set_mobility(unreal.ComponentMobility.MOVABLE);board.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'))
board.set_material(0,unreal.load_asset('/Game/ThirdPerson/Environment/Complementos/Materials/M_Apoyo_Goma'))
board.set_editor_properties({'relative_location':unreal.Vector(-2,0,22),'relative_scale3d':unreal.Vector(.025,1.85,.53),'can_ever_affect_navigation':False})
board.set_cast_shadow(False);board.set_collision_profile_name('NoCollision')

exec(compile((root/'Tools/UnrealPython/prepare_break_flash.py').read_text(encoding='utf8'),'prepare_break_flash.py','exec'),{})
paths={'BP_Hostage':'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage'}
notes={'BP_Hostage':'La cápsula bloquea el paso del jugador. El árbol gobierna seguimiento, espera y refugio.',
       'BP_HUD_Entrega':'El control de cine envuelve toda la interfaz jugable. Recursos en columna y acciones contextuales sobre fondo oscuro.',
       'BP_DestruibleEntrega':'La caja de impacto desaparece al romper. Chaos sólo interactúa con el escenario estático. La ráfaga dura como máximo 0,65 s.',
       'BP_DestructibleDoor':'Dos golpes cargados abren la puerta. El efecto se retira a los 0,65 s y los fragmentos físicos ignoran a los personajes.',
       'BP_SistemasComplementarios':'El aljibe está junto al alero del refugio. El contacto con agua genera una onda y un paso audible.',
       'BP_BeaconLabel':'Placa orientada hacia la cámara. Se oculta con el director durante las secuencias.'}
for name,note in notes.items():
    bp=unreal.load_asset(paths.get(name,base+name))
    assert bridge.install_graph(bp,str(root/'Intermediate/inspect/delivery_graphs'/(name+'.t3d'))),name
    assert bridge.add_layout_comment(bp,'Presentacion','PRESENTACIÓN · '+note,unreal.Vector2D(-900,-700),unreal.Vector2D(800,300),unreal.LinearColor(.08,.20,.24,1))
    lib.compile_blueprint(bp);save(bp)

# El helper vacía el EventGraph antes de importar y recompila sus dependencias.
# Resolver de nuevo los llamadores de Interactuar tras restaurar el evento.
for name in ['BP_DirectorEntrega','BP_DeliverySaveManager']:
    bp=unreal.load_asset(base+name);lib.compile_blueprint(bp)

lamp=unreal.load_asset(base+'BP_LuminariaPared')
for _,obj in components(lamp):
    if isinstance(obj,unreal.SpotLightComponent):
        obj.modify();obj.set_editor_properties({'max_draw_distance':6500.,'max_distance_fade_range':1400.})
    if isinstance(obj,unreal.StaticMeshComponent):
        obj.modify();obj.set_editor_property('ld_max_draw_distance',7000.)
assert bridge.set_property_text(lamp,'BlueprintDescription','Foco de pared de 3200 lm. Radio 14,5 m y alcance de dibujo 65 m con transición de 14 m.')
assert bridge.add_layout_comment(lamp,'DocumentacionLuminaria','LUMINARIA DE PARED · 3200 lm / radio 14,5 m\nDistancia de dibujo 65 m con transición de 14 m.',unreal.Vector2D(-400,-400),unreal.Vector2D(750,350),unreal.LinearColor(.12,.20,.28,1))
lib.compile_blueprint(lamp);save(lamp)
fragment=unreal.load_asset(base+'BP_DoorFragment')
fc=unreal.get_default_object(fragment.generated_class()).static_mesh_component
fc.modify();fc.set_collision_profile_name('RestosEscenario');fc.set_editor_property('can_character_step_up_on',unreal.CanBeCharacterBase.ECB_NO)
assert fc.get_collision_enabled()==unreal.CollisionEnabled.PHYSICS_ONLY
save(fragment)
prop=unreal.load_asset(base+'BP_DestruibleEntrega')
def configure_gc(c):
    c.modify();c.set_editor_property('collision_profile_per_level',['RestosEscenario'])
    c.set_editor_properties({'can_ever_affect_navigation':False,'can_character_step_up_on':unreal.CanBeCharacterBase.ECB_NO,'generate_overlap_events':False})
for _,obj in components(prop):
    if isinstance(obj,unreal.GeometryCollectionComponent):configure_gc(obj)
lib.compile_blueprint(prop);save(prop)
for a in actors.get_all_level_actors():
    key=a.get_actor_label()
    if key in ['Luz_Compound_Rescate','Luz_Compound_Deposito','Luz_Compound_AccesoPatio','Luz_Equipo_Farol_Deposito','Luz_Equipo_Farol_Jardin']:
        a.modify();c=a.get_component_by_class(unreal.LocalLightComponent);c.modify()
        room=key in ['Luz_Compound_Rescate','Luz_Compound_Deposito']
        c.set_editor_properties({'max_draw_distance':0. if room else 6000.,'max_distance_fade_range':0. if room else 1200.})
        if room:a.set_editor_property('is_spatially_loaded',False)
    if a.get_class()==prop.generated_class():
        gc=a.get_component_by_class(unreal.GeometryCollectionComponent)
        if list(map(str,gc.get_editor_property('collision_profile_per_level'))) != ['RestosEscenario'] or gc.get_editor_property('can_ever_affect_navigation'):
            a.modify();configure_gc(gc)

exec(compile((root/'Tools/UnrealPython/prepare_retention_water.py').read_text(encoding='utf8'),'prepare_retention_water.py','exec'),{})
