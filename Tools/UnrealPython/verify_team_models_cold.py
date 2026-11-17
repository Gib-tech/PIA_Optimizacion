"""Read-only cold reopen, with the authoring helper absent."""
import unreal,os,json
ues=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not ues.get_game_world() and not hasattr(unreal,'DeliveryBlueprintBuilder')
assert ues.get_editor_world().get_name()=='Nivel_Entrega'
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
new=[a for a in actors if a.get_actor_label().startswith('Equipo_')];assert len(new)==8 and all(not a.get_editor_property('is_spatially_loaded') for a in new)
meshes={a.static_mesh_component.static_mesh.get_name():a.static_mesh_component.static_mesh for a in new};assert len(meshes)==5
for name,mesh in meshes.items():
 assert sm.get_nanite_settings(mesh).enabled if name=='SM_AutoDestruido' else sm.get_lod_count(mesh)==4
 assert sm.get_convex_collision_count(mesh)==1
assert any(a.get_actor_label()=='Horizonte_Terreno_Distante' for a in actors)
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not dirty
result={'passed':True,'normal_editor_without_helper':True,'no_pie':True,'five_new_designs_eight_resident_instances':True,'four_new_conventional_lod_designs_and_nanite_wreck':True,'dirty_packages':[]}
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/team-models/cold.json'),'w') as f:json.dump(result,f,indent=2)
unreal.log('TEAM_MODELS_COLD_RELOAD_PASSED')
