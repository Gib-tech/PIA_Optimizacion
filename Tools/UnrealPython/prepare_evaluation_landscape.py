"""Keep Ian's architecture and replace its ground with the team's layered Landscape."""
import unreal,os,sys
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
sys.path.insert(0,os.path.join(root,'Tools/UnrealPython'))
ART='/Game/ThirdPerson/Environment/Evaluation'
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert hasattr(unreal.DeliveryBlueprintBuilder,'create_evaluation_landscape')
tools=unreal.AssetToolsHelpers.get_asset_tools();sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
for i in range(1,5):
 name='SM_IanWalls_%02d'%i;path=ART+'/'+name
 if not unreal.EditorAssetLibrary.does_asset_exist(path):
  options=unreal.FbxImportUI();options.automated_import_should_detect_type=False;options.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
  options.import_materials=False;options.import_textures=False;options.static_mesh_import_data.combine_meshes=True;options.static_mesh_import_data.auto_generate_collision=False
  options.static_mesh_import_data.transform_vertex_to_absolute=True
  task=unreal.AssetImportTask();task.filename=os.path.join(root,'Tools/ArtSource/EvaluationWalls',name+'.fbx');task.destination_path=ART;task.destination_name=name;task.automated=True;task.save=True;task.options=options;tools.import_asset_tasks([task])
 new=unreal.load_asset(path);old=unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/Escenario_Sector'+str(i))
 assert (new.get_bounds().box_extent-old.get_bounds().box_extent).length()<10,(name,str(new.get_bounds()),str(old.get_bounds()))
 for j,slot in enumerate(old.static_materials):new.set_material(j,slot.material_interface)
 for a in sub.get_all_level_actors():
  if a.get_actor_label()=='Ian_Sector_%02d'%i:a.static_mesh_component.set_static_mesh(new)
 # Rebuild simple convex walls from their exact remaining faces, not a solid box.
 # The existing helper's prisms function can be loaded without running its editor tail.
 source=open(os.path.join(root,'Tools/UnrealPython/build_precise_wall_collision.py'),encoding='utf-8').read().split('world=')[0]
 scope={};exec(source,scope);objpath=os.path.join(root,'Intermediate/inspect/evaluation_wall_%d.obj'%i)
 export=unreal.AssetExportTask();export.object=new;export.filename=objpath;export.automated=True;export.prompt=False;export.replace_identical=True;assert unreal.Exporter.run_asset_export_task(export)
 shapes=[]
 for j,points in enumerate(scope['prisms'](objpath)):
  def vec(p):return '(X=%.6f,Y=%.6f,Z=%.6f)'%p
  bounds=[tuple(fn(p[k] for p in points) for k in range(3)) for fn in [min,max]]
  text='(VertexData=('+','.join(vec(p) for p in points)+'),ElemBox=(Min='+vec(bounds[0])+',Max='+vec(bounds[1])+',IsValid=True),Name="WallFace'+str(j)+'")'
  shape=unreal.KConvexElem();assert shape.import_text(text);shapes.append(shape)
 body=unreal.new_object(unreal.BodySetup,outer=new);body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AND_COMPLEX);body.set_editor_property('double_sided_geometry',True)
 agg=unreal.KAggregateGeom();agg.set_editor_property('convex_elems',shapes);body.set_editor_property('agg_geom',agg);new.modify();new.set_editor_property('body_setup',body)
 nanite=sm.get_nanite_settings(new);nanite.enabled=True;sm.set_nanite_settings(new,nanite)
 unreal.EditorAssetLibrary.save_loaded_asset(new,only_if_is_dirty=False)
 unreal.log('EVALUATION_WALL '+name+' shapes '+str(len(shapes)))

lands=[a for a in sub.get_all_level_actors() if isinstance(a,unreal.Landscape)]
if not lands:
 layers=[]
 # Five genuine painted target layers from the team's existing material.
 for name in ['SueloLadrilloOscuro','SueloLadrillos','SueloCuadros','Pasto','Tierra']:
  path=ART+'/LI_'+name;info=unreal.load_asset(path)
  if not info:
   info=tools.create_asset('LI_'+name,ART,unreal.LandscapeLayerInfoObject,None)
  assert unreal.DeliveryBlueprintBuilder.set_property_text(info,'LayerName',name)
  unreal.EditorAssetLibrary.save_loaded_asset(info)
  layers.append(info)
 land=unreal.DeliveryBlueprintBuilder.create_evaluation_landscape(world,unreal.load_asset('/Game/Landscape'),layers)
 assert land,'Landscape import failed'
for a in sub.get_all_level_actors():
 if a.get_actor_label()=='Suelo_Entrega':sub.destroy_actor(a)
unreal.SystemLibrary.execute_console_command(world,'RebuildNavigation')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('EVALUATION_LANDSCAPE_PREPARED')
