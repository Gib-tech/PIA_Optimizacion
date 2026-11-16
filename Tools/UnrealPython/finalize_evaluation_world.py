import unreal,os,json
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert unreal.DeliveryBlueprintBuilder.is_partitioned(world),'Map must be truly converted'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
for a in actors:
 if isinstance(a,unreal.RecastNavMesh):
  try:a.set_editor_property('is_world_partitioned',False);a.set_editor_property('force_rebuild_on_load',True)
  except Exception:pass
lods=[]
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for name in ['Banco','Car','Tree1','Light_Pole','fuente']:
 mesh=unreal.load_asset('/Game/ThirdPerson/Environment/Evaluation/SM_LOD_'+name)
 settings=sm.get_nanite_settings(mesh)
 if settings.enabled:settings.enabled=False;sm.set_nanite_settings(mesh,settings);unreal.EditorAssetLibrary.save_loaded_asset(mesh)
 geometry=unreal.DeliveryBlueprintBuilder.get_lod_geometry(mesh)
 lods.append({'name':name,'geometry':[{'vertices':p.x,'triangles':p.y} for p in geometry],'screen_sizes':list(sm.get_lod_screen_sizes(mesh)),'nanite':sm.get_nanite_settings(mesh).enabled})
 assert len(geometry)==4 and all(p.y>0 for p in geometry),lods[-1]
unreal.SystemLibrary.execute_console_command(world,'RebuildNavigation')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/evaluation_world.json'),'w') as f:json.dump({'partitioned':True,'runtime_grid':'Default official converter configuration; no custom cell sizes claimed','lod_models':lods},f,indent=2)
unreal.log('EVALUATION_WORLD_READY')
