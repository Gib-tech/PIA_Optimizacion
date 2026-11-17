"""Instalar con los cuatro grafos generados, Nivel_Entrega cargado y PIE detenido."""
from pathlib import Path
import unreal

root=Path(unreal.Paths.project_dir()).resolve()
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Nivel_Entrega' and not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bridge=unreal.DeliveryBlueprintBuilder
assert bridge.load_editor_region(world,unreal.Vector(-6500,-12500,-1200),unreal.Vector(6500,1500,7000))
base='/Game/ThirdPerson/Blueprints/Entrega/'
lib=unreal.BlueprintEditorLibrary
assets=unreal.EditorAssetLibrary
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
def blueprint(name):return unreal.load_asset(base+name)
def fields(bp,types):
    for name,kind in types.items():
        try:unreal.get_default_object(bp.generated_class()).get_editor_property(name);continue
        except Exception:pass
        pin=lib.get_object_reference_type(unreal.load_class(None,kind)) if kind.startswith('/') else lib.get_basic_type_by_name(kind)
        assert lib.add_member_variable(bp,name,pin),name
        if kind.startswith('/'):lib.set_blueprint_variable_instance_editable(bp,name,True)
    lib.compile_blueprint(bp)
extra=blueprint('BP_SistemasComplementarios')
prop=blueprint('BP_DestruibleEntrega')
fields(extra,{'SiguienteLuz':'real','FaseSolar':'int','AguaRetencion':'/Script/Engine.StaticMeshActor','AguaMID':'/Script/Engine.MaterialInstanceDynamic','PiesEnAgua':'bool','ProximaOnda':'real'})
fields(prop,{'ModeloIntacto':'/Script/Engine.StaticMeshActor'})
notes={
 'BP_SistemasComplementarios':'Ciclo de 480 s desde la tarde. Reloj por frame, luz cada 0,12 s. BRUNO usa proximidad y visibilidad; la mesa tiene prioridad. El pulso consume una celda, usa la mira y confirma el impacto. El estanque genera ondas en los pies al entrar y caminar.',
 'BP_PlayerEntrega':'La ventana de ataque abre un barrido de 220 cm con radio de 52 cm, además del contacto del arma. Ambos comparten la lista de impactos del swing. Sólo las puertas filtran por mejora y tipo de golpe.',
 'BP_DestruibleEntrega':'Daño positivo del protagonista rompe el objeto común en un golpe (vida 15). En copias con LOD, se oculta el modelo intacto y se revela Chaos en el mismo lugar. La colisión de los restos ignora al jugador.',
 'BP_DeliverySaveManager':'Guardado manual y automático con confirmación silenciosa. Los errores de escritura o lectura conservan su aviso.',
 'BP_HUD_Entrega':'Alerta de daño al rehén a la derecha. Las tres tarjetas horizontales leen las cantidades del inventario y comparten sus iconos. Mira para ambas cámaras. El contexto de BRUNO usa la misma condición que la interacción. La fase solar procede del reloj del mundo.'}
for name,note in notes.items():
    bp=blueprint(name)
    assert bridge.install_graph(bp,str(root/'Intermediate/inspect/delivery_graphs'/(name+'.t3d'))),name
    assert bridge.add_layout_comment(bp,'RevisionJugable','JUGABILIDAD · '+note+'\nVer docs/REVISION_JUGABLE.md',unreal.Vector2D(-1000,-550),unreal.Vector2D(900,440),unreal.LinearColor(.07,.2,.24,1))
    assert bridge.set_property_text(bp,'BlueprintDescription',note)
for name in [*notes,'BP_DirectorEntrega','BP_BeaconEntrega','BP_DeliverySaveManager']:
    bp=blueprint(name);lib.compile_blueprint(bp);assert assets.save_loaded_asset(bp,False)
unreal.get_default_object(extra.generated_class()).set_editor_property('DayCycleDuration',480.)
unreal.get_default_object(prop.generated_class()).set_editor_property('Health',15.)
assets.save_loaded_asset(extra,False);assets.save_loaded_asset(prop,False)
system=placed['Sistemas_Complementarios'];system.modify()
system.set_editor_property('DayCycleDuration',480.);system.set_editor_property('AguaRetencion',placed['Lago_Retencion_Agua'])
# La malla intacta conserva sus materiales, LOD y encuadre originales.
for label,kind in [('LOD_Banco','Banca'),('LOD_Car','Auto'),('LOD_fuente','Fuente'),('Equipo_Auto_Abandonado','Auto')]:
    model=placed[label];display=model.static_mesh_component
    name='Impacto_'+label
    twin=placed.get(name) or actors.duplicate_actor(placed['Destruible_'+kind])
    assert twin
    twin.modify();twin.set_actor_label(name);twin.set_editor_property('is_spatially_loaded',False)
    gc=twin.get_component_by_class(unreal.GeometryCollectionComponent);gc.modify()
    center,extent,_=unreal.SystemLibrary.get_component_bounds(display)
    pos,size,_=unreal.SystemLibrary.get_component_bounds(gc)
    scale=twin.get_actor_scale3d()
    twin.set_actor_scale3d(unreal.Vector(scale.x*extent.x/size.x,scale.y*extent.y/size.y,scale.z*extent.z/size.z))
    pos,_,_=unreal.SystemLibrary.get_component_bounds(gc)
    twin.set_actor_location(twin.get_actor_location()+center-pos,False,True)
    twin.set_editor_property('ModeloIntacto',model)
    box=twin.get_editor_property('Colision');box.modify();box.set_world_location(center,False,True);box.set_world_scale3d(unreal.Vector(1,1,1));box.set_box_extent(extent,False)
    gc.set_visibility(False);gc.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    model.modify();display.modify();display.set_collision_profile_name('NoCollision')
    placed[name]=twin
stone=unreal.load_asset('/Game/ThirdPerson/Environment/Atmosphere/MI_FuenteChaos')
placed['LOD_fuente'].static_mesh_component.set_material(0,stone)
for a in placed.values():
    if a.get_class()!=prop.generated_class():continue
    a.modify();a.set_editor_property('Health',15.)
    kind=a.get_editor_property('NombreDestruible').lower()
    effect=('/Game/NS/Chispas_impacto/NS_ChispaImpacto' if any(w in kind for w in ['auto','barril','basurero']) else base+'FX/NS_DoorBreak')
    a.set_editor_property('BreakFX',unreal.load_asset(effect))
# Reducir el trabajo de sombras conservando el cono que ilumina el camino.
lamp=blueprint('BP_LuminariaPared')
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);fn=unreal.SubobjectDataBlueprintFunctionLibrary
for h in sub.k2_gather_subobject_data_for_blueprint(lamp):
    c=fn.get_object(fn.get_data(h))
    if isinstance(c,unreal.SpotLightComponent):
        c.modify();c.set_editor_properties({'max_draw_distance':2300.,'max_distance_fade_range':500.,'shadow_resolution_scale':.35,'volumetric_scattering_intensity':0.})
assert bridge.set_property_text(lamp,'BlueprintDescription','Foco cálido de 3200 lm y radio 1450 cm. Se desvanece hasta 2300 cm, con sombras a escala 0,35 y sin dispersión volumétrica.')
lib.compile_blueprint(lamp);assets.save_loaded_asset(lamp,False)
# Los objetos pequeños salen antes del presupuesto de dibujo; los edificios conservan su silueta.
for label in ['Equipo_Escombros_Jardin','Equipo_Escombros_Servicio','Equipo_Farol_Jardin','Equipo_Farol_Deposito']:
    a=placed[label];a.modify();c=a.static_mesh_component;c.modify();c.set_editor_properties({'ld_max_draw_distance':6500.,'never_distance_cull':False})
for label,limit in [('FX_NS_Hojas',1800.),('FX_NS_Polvo',1400.)]:
    a=placed[label];a.modify();c=a.get_component_by_class(unreal.NiagaraComponent);c.modify();c.set_editor_property('ld_max_draw_distance',limit)
for path,cap in [('/Game/ThirdPerson/RecursosPropios/Modelos/ConcreteBench',1024),('/Game/ThirdPerson/Environment/TeamModels/Textures/T_Escombros_0_BaseColor',512)]:
    tex=unreal.load_asset(path);assert tex
    tex.modify();tex.set_editor_properties({'max_texture_size':cap,'never_stream':False,'mip_gen_settings':unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP})
    assets.save_loaded_asset(tex,False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
if dirty:assert unreal.EditorLoadingAndSavingUtils.save_packages(dirty,True)
