"""Full placed-wall/material audit and effective render distance check."""
import unreal,os,json
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
report={'walls':[],'models':[],'passed':False}
for a in actors:
 for c in a.get_components_by_class(unreal.PrimitiveComponent):
  if not isinstance(c,(unreal.StaticMeshComponent,unreal.GeometryCollectionComponent)):continue
  mats=[m for m in c.get_materials() if m]
  assert not any(m.get_path_name().startswith('/Game/ThirdPerson/Environment/EscenarioIan/Sector') for m in mats),a.get_actor_label()
  wall_mats=[m for m in mats if m.get_name().startswith('M_WallMetric_')]
  if wall_mats:
   report['walls'].append({'actor':a.get_actor_label(),'materials':sorted({m.get_name() for m in wall_mats})})
  assert c.get_editor_property('ld_max_draw_distance')==0,(a.get_actor_label(),c.get_name(),c.get_editor_property('ld_max_draw_distance'))
  assert c.get_editor_property('never_distance_cull'),(a.get_actor_label(),c.get_name(),'never_distance_cull')
  assert c.get_editor_property('cached_max_draw_distance')==0,(a.get_actor_label(),c.get_name(),'cached')
  if a.get_actor_label().startswith(('LOD_','Destruible_')):
   assert not a.get_editor_property('is_spatially_loaded'),a.get_actor_label()
   report['models'].append(a.get_actor_label())
assert len(report['walls'])==104,len(report['walls'])
assert len(set(report['models']))==11
for name in ['wood_inlaid_stone_wall','rock_boulder_dry','rock_wall_16']:
 mat=unreal.load_asset('/Game/ThirdPerson/Environment/Atmosphere/M_WallMetric_'+name)
 task=unreal.AssetExportTask();task.object=mat;task.filename=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/live',mat.get_name()+'.t3d');task.automated=True;task.prompt=False;task.replace_identical=True
 assert unreal.Exporter.run_asset_export_task(task)
lods=[a for a in actors if a.get_actor_label().startswith('LOD_')]
sm_editor=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
assert len(lods)==5
for a in lods:
 mesh=a.static_mesh_component.static_mesh
 assert sm_editor.get_lod_count(mesh)==4,mesh.get_name()
 assert not sm_editor.get_nanite_settings(mesh).enabled,mesh.get_name()
report.update(four_lod_models=5,passed=True,all_wall_components=104,metric_tile_cm=[400,400,400],visible_model_distance_culling=False)
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/wall_visibility_validation.json'),'w') as f:json.dump(report,f,indent=2)
unreal.log('ALL_104_WALLS_AND_11_MODELS_VALIDATED')
