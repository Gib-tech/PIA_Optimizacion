import unreal, os, json
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
report={}
for label,path in [('player','/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega'),('hostage','/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage')]:
 bp=unreal.load_asset(path); sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
 report[label]=[]
 for h in sub.k2_gather_subobject_data_for_blueprint(bp):
  data=unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h)
  obj=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
  row={'name':obj.get_name(),'class':obj.get_class().get_name()}
  if isinstance(obj,unreal.SceneComponent):
   row.update(location=str(obj.relative_location),rotation=str(obj.relative_rotation),socket=str(obj.get_attach_socket_name()))
  if isinstance(obj,unreal.SkeletalMeshComponent):
   mesh=obj.get_skeletal_mesh_asset();row.update(mesh=mesh.get_path_name() if mesh else None)
  if isinstance(obj,unreal.StaticMeshComponent):row['mesh']=obj.static_mesh.get_path_name() if obj.static_mesh else None
  report[label].append(row)
for name,cls in [('add',unreal.AddNewSubobjectParams),('fbx',unreal.FbxExportOption),('skel',unreal.Skeleton)]:report[name]=cls.__doc__
for meshpath in ['/Game/Survival_Character/Meshes/SK_Survival_Character','/Game/SciFITrooper_Man_03/SkeletalMesh/SK_SciFITrooper_Man_03']:
 mesh=unreal.load_asset(meshpath)
 task=unreal.AssetExportTask();task.object=mesh;task.filename=os.path.join(root,'Intermediate/inspect/project_audit',mesh.get_name()+'.fbx')
 task.automated=True;task.prompt=False;task.replace_identical=True
 task.options=unreal.FbxExportOption();task.options.set_editor_property('level_of_detail',False)
 assert unreal.Exporter.run_asset_export_task(task)
 report[mesh.get_name()]={'skeleton':mesh.skeleton.get_path_name(),'compatible':str(mesh.skeleton.compatible_skeletons),'export':task.filename}
with open(os.path.join(root,'Intermediate/inspect/project_audit/presentation.json'),'w',encoding='utf-8') as f:json.dump(report,f,indent=2)
unreal.log('PRESENTATION_ASSETS '+json.dumps(report))
