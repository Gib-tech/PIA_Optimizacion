"""Current rubric evidence: runtime models, real LODs, partition, lights and level logic.

Groups count visual designs, not duplicate instances, LOD copies or fracture variants.
An isolated stopped enemy is spawned to inspect its actual rendered character model.
"""
import unreal,os,json
assert hasattr(unreal,'DeliveryBlueprintBuilder'),'Run this audit with the editor-only BPB3 helper loaded'
rubric_world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert rubric_world
rubric_gs=unreal.GameplayStatics;rubric_native=unreal.get_default_object(rubric_gs.static_class())
rubric_player=rubric_gs.get_player_character(rubric_world,0)
rubric_class=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
rubric_tr=unreal.Transform(location=rubric_player.get_actor_location()+unreal.Vector(350,0,0))
rubric_enemy=rubric_native.call_method('BeginDeferredActorSpawnFromClass',(rubric_world,rubric_class,rubric_tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));rubric_native.call_method('FinishSpawningActor',(rubric_enemy,rubric_tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
rubric_enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Read-only inventory fixture')
rubric_meshes=set();rubric_lights=[];rubric_collections=[];rubric_landscapes=[]
rubric_actors=rubric_gs.get_all_actors_of_class(rubric_world,unreal.Actor)
for rubric_actor in rubric_actors:
    for c in rubric_actor.get_components_by_class(unreal.StaticMeshComponent):
        if c.static_mesh and c.static_mesh.get_path_name().startswith('/Game/'):rubric_meshes.add(c.static_mesh.get_path_name())
    for c in rubric_actor.get_components_by_class(unreal.SkeletalMeshComponent):
        if c.get_skeletal_mesh_asset():rubric_meshes.add(c.get_skeletal_mesh_asset().get_path_name())
    for c in rubric_actor.get_components_by_class(unreal.GeometryCollectionComponent):
        asset=c.get_editor_property('rest_collection')
        if asset:rubric_meshes.add(asset.get_path_name())
        if rubric_actor.get_class().get_name()=='BP_DestruibleEntrega_C':rubric_collections.append(asset.get_path_name())
    if isinstance(rubric_actor,unreal.LandscapeProxy):rubric_landscapes.append(rubric_actor.get_name())
    for c in rubric_actor.get_components_by_class(unreal.LightComponent):
        row={'type':c.get_class().get_name()}
        if isinstance(c,unreal.LocalLightComponent):row.update(radius=c.get_editor_property('attenuation_radius'),max_draw_distance=c.get_editor_property('max_draw_distance'))
        rubric_lights.append(row)
rubric_groups={
 'Banca':['SM_LOD_Banco','GC_Banco'],'Automóvil':['SM_LOD_Car','GC_Car2'],
 'Árbol':['SM_LOD_Tree1'],'Poste':['SM_LOD_Light_Pole'],'Fuente':['SM_LOD_fuente','GC_fuente'],
 'Caja':['GC_box'],'Basurero':['GC_Trash'],'Barril':['GC_Barril'],
 'Protagonista':['SK_SciFITrooper_Man_03'],'Rehén sobreviviente':['SK_RehenSuperviviente'],'Rival':['SK_SciFiWarrior02'],
 'Espada':['longsword'],'Martillo':['Decahammer'],'Baliza':['SM_Baliza'],
 'Puerta':['SM_DoorPanel_01','SM_DoorPanel_02','SM_DoorPanel_03'],
 'Arquitectura de Ian':['SM_Walls_Rescate','SM_Walls_Arena','SM_Walls_Deposito'],
 'Botiquín temporal':['SM_BotiquinTemporal'],'Celda temporal':['SM_CeldaTemporal'],'Crédito cronal':['SM_CreditoCronal'],
 'Caja de suministros':['SM_CajaSuministros'],'Consola del técnico':['SM_ConsolaTecnico'],'Cubeta de estanque':['SM_EstanqueRetencion']}
rubric_designs={name:sorted(p for p in rubric_meshes if p.rsplit('.',1)[-1] in variants) for name,variants in rubric_groups.items()}
assert all(rubric_designs.values()),[k for k,v in rubric_designs.items() if not v]
rubric_sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);rubric_lods=[]
for name in ['Banco','Car','Tree1','Light_Pole','fuente']:
    mesh=unreal.load_asset('/Game/ThirdPerson/Environment/Evaluation/SM_LOD_'+name)
    geometry=unreal.DeliveryBlueprintBuilder.get_lod_geometry(mesh)
    row={'model':name,'lod_count':len(geometry),'triangles':[p.y for p in geometry],'nanite':rubric_sm.get_nanite_settings(mesh).enabled}
    assert row['lod_count']==4 and not row['nanite'] and len(set(row['triangles']))==4,row
    rubric_lods.append(row)
rubric_level=next(a for a in rubric_actors if isinstance(a,unreal.LevelScriptActor))
assert rubric_level.get_editor_property('Inicializado') and rubric_level.get_editor_property('Sincronizaciones')>0
assert rubric_level.call_method('ConsultarAliados') and not rubric_level.call_method('ConsultarSecuencia')
assert len(set(rubric_collections))==6 and rubric_landscapes
assert unreal.DeliveryBlueprintBuilder.is_partitioned(rubric_world)
rubric_enemy.destroy_actor()
rubric_report={'passed':True,'date':'2026-11-16','isolated_stopped_enemy_inventory_fixture':True,'partitioned_runtime':True,'landscape':rubric_landscapes,'loaded_geometry_paths':sorted(rubric_meshes),'conservative_visual_design_count':len(rubric_designs),'visual_designs':rubric_designs,'authorship_not_proven_by_asset_names':True,'five_four_lod_models':rubric_lods,'six_different_chaos_collections':sorted(set(rubric_collections)),'lights':rubric_lights,'level_logic_executed':True,'owner_professor_acceptance_not_claimed':True}
rubric_report['date']='2026-11-17'
with open(os.path.join(unreal.Paths.project_dir(),'docs/validation/inventario-runtime-2026-11-17.json'),'w',encoding='utf-8') as f:json.dump(rubric_report,f,ensure_ascii=False,indent=2)
unreal.log('CURRENT_RUBRIC_INVENTORY_PASSED '+str(len(rubric_designs))+' visual designs')
