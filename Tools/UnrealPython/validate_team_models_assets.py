"""Saved-asset audit after visual/nav QA; preserves the established systems."""
import unreal,os,json
ues=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not ues.get_game_world()
root=unreal.Paths.project_dir();ART='/Game/ThirdPerson/Environment/TeamModels';sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);rows=[]
for name in ['Edificio','Farol','Escombros','AutoDestruido','ArbolFab']:
 mesh=unreal.load_asset(ART+'/SM_'+name);assert mesh
 geo=[{'vertices':p.x,'triangles':p.y} for p in unreal.DeliveryBlueprintBuilder.get_lod_geometry(mesh)]
 nanite=sm.get_nanite_settings(mesh).enabled
 assert nanite if name=='AutoDestruido' else len(geo)==4 and len({p['triangles'] for p in geo})==4
 assert sm.get_convex_collision_count(mesh)==1
 for slot in mesh.static_materials:assert slot.material_interface and 'DefaultMaterial' not in slot.material_interface.get_name()
 rows.append({'name':name,'geometry':geo,'nanite':nanite,'one_simple_collision':True,'materials_assigned':True})
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
new=[a for a in actors if a.get_actor_label().startswith('Equipo_')];assert len(new)==8
for a in new:
 assert not a.get_editor_property('is_spatially_loaded') and a.static_mesh_component.forced_lod_model==0
 assert a.static_mesh_component.get_editor_property('never_distance_cull')
 assert a.static_mesh_component.get_editor_property('ld_max_draw_distance')==0
for name in ['Banco','Car','Tree1','Light_Pole','fuente']:assert sm.get_lod_count(unreal.load_asset('/Game/ThirdPerson/Environment/Evaluation/SM_LOD_'+name))==4
architecture=[a for a in actors if a.get_actor_label().startswith('Compound_SM_Walls_')];assert len(architecture)==10 and all(sm.get_nanite_settings(a.static_mesh_component.static_mesh).enabled for a in architecture)
assert any(isinstance(a,unreal.LandscapeProxy) for a in actors)
assert unreal.DeliveryBlueprintBuilder.is_partitioned(ues.get_editor_world())
director=next(a for a in actors if a.get_class().get_name()=='BP_DirectorEntrega_C')
assert all(director.get_editor_property('Zona'+str(i)) for i in [1,2,3])
for name in ['BP_BaseEnemy','BP_ChargerEnemy']:
 cdo=unreal.get_default_object(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/'+name+'.'+name+'_C'));assert abs(cdo.get_editor_property('ContactDamage')-13.2)<.001 and not cdo.is_actor_tick_enabled()
for name in ['LS_Intro','LS_Derrota','LS_Victoria','LS_Revelacion']:assert unreal.load_asset('/Game/ThirdPerson/Cinematics/'+name)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not dirty,[p.get_path_name() for p in dirty]
result={'passed':True,'meshes':rows,'four_lod_designs_total':9,'architecture_nanite_preserved':10,'new_nanite_wreck':True,'landscape_world_partition_preserved':True,'three_encounters_four_cinematics_and_damage_preserved':True,'dirty':[]}
with open(os.path.join(root,'Intermediate/inspect/team-models/assets.json'),'w') as f:json.dump(result,f,indent=2)
unreal.log('TEAM_MODELS_ASSETS_VALIDATED '+json.dumps(result))
