"""Read-only audit of the deliverable, not an inference from asset names."""
import unreal,os,json,collections
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
report={'map':w.get_path_name(),'builder':hasattr(unreal,'DeliveryBlueprintBuilder'),'classes':dict(collections.Counter(a.get_class().get_name() for a in actors)),'actors':[],'meshes':{},'particles':[],'lights':[],'landscapes':[]}
def value(obj,key):
 try:return str(obj.get_editor_property(key))
 except Exception:return None
for a in actors:
 item={'label':a.get_actor_label(),'class':a.get_class().get_name(),'location':[a.get_actor_location().x,a.get_actor_location().y,a.get_actor_location().z]}
 item['meshes']=[]
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  mesh=c.static_mesh
  if not mesh:continue
  path=mesh.get_path_name();item['meshes'].append(path)
  if path not in report['meshes']:
   n=mesh.get_editor_property('nanite_settings')
   report['meshes'][path]={'instances':0,'lod_count':sm.get_lod_count(mesh),'nanite':n.enabled,'materials':[str(s.material_interface.get_path_name()) if s.material_interface else None for s in mesh.static_materials]}
  report['meshes'][path]['instances']+=1
 for c in a.get_components_by_class(unreal.NiagaraComponent):report['particles'].append({'actor':a.get_actor_label(),'system':value(c,'asset'),'auto_activate':value(c,'auto_activate')})
 for c in a.get_components_by_class(unreal.LightComponent):report['lights'].append({'actor':a.get_actor_label(),'class':c.get_class().get_name(),'mobility':value(c,'mobility'),'intensity':value(c,'intensity'),'attenuation':value(c,'attenuation_radius'),'cast_shadows':value(c,'cast_shadows')})
 if isinstance(a,unreal.LandscapeProxy):report['landscapes'].append(item)
 if item['meshes'] or a.get_class().get_name().startswith(('BP_','GC_')):report['actors'].append(item)
ws=w.get_world_settings();report['world_composition']=value(ws,'enable_world_composition')
try:report['partitioned']=w.is_partitioned_world()
except Exception:report['partitioned']=value(ws,'world_partition')
registry=unreal.AssetRegistryHelpers.get_asset_registry()
owned=registry.get_assets_by_path('/Game/ThirdPerson/RecursosPropios',recursive=True)
report['owned_assets']=[{'path':str(a.package_name),'class':str(a.asset_class_path.asset_name)} for a in owned]
out=os.path.join(root,'Intermediate/inspect/evaluation_audit.json')
with open(out,'w',encoding='utf-8') as f:json.dump(report,f,indent=2,ensure_ascii=False)
unreal.log('EVALUATION_AUDIT '+json.dumps({k:len(report[k]) for k in ['actors','meshes','particles','lights','landscapes']}))
unreal.log('WORLD_COMPOSITION '+str(report['world_composition'])+' PARTITIONED '+str(report['partitioned']))
