"""Import shared fracture geometry, exact convex shard collision and instance bindings; raise contact damage."""
import unreal,os,json,math
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());root=os.path.join(project,'Tools/ArtSource/Fracture')
manifest=json.load(open(os.path.join(root,'fracture_manifest.json')))
R='/Game/ThirdPerson/Blueprints/Entrega/';E='/Game/ThirdPerson/Blueprints/EnemigoIA/';ART='/Game/ThirdPerson/Environment/Progression';DEST=ART+'/Fracture'
lib=unreal.BlueprintEditorLibrary;tools=unreal.AssetToolsHelpers.get_asset_tools()
mesh_type=lib.get_object_reference_type(unreal.StaticMesh);vector_type=lib.get_struct_type(unreal.load_object(None,'/Script/CoreUObject.Vector'))
for path,fields in {R+'BP_DestructibleDoor':{'CrackedMesh':mesh_type,'FragmentMeshes':lib.get_array_type(mesh_type),'FragmentOffsets':lib.get_array_type(vector_type),'DoorHeight':lib.get_basic_type_by_name('real')},R+'BP_DoorFragment':{'ShardMesh':mesh_type,'BreakVelocity':vector_type}}.items():
 bp=unreal.load_asset(path);cdo=unreal.get_default_object(bp.generated_class())
 for name,typ in fields.items():
  try:cdo.get_editor_property(name)
  except Exception:assert lib.add_member_variable(bp,name,typ)
  lib.set_blueprint_variable_instance_editable(bp,name,True)
  if path.endswith('BP_DoorFragment'):lib.set_blueprint_variable_expose_on_spawn(bp,name,True)
 lib.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
tasks=[]
for door in manifest['doors']:
 for name in [door['cracked_mesh']]+[p['mesh'] for p in door['pieces']]:
  if unreal.EditorAssetLibrary.does_asset_exist(DEST+'/'+name):continue
  options=unreal.FbxImportUI();options.automated_import_should_detect_type=False;options.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH;options.import_materials=False;options.import_textures=False
  data=options.static_mesh_import_data;data.combine_meshes=True;data.auto_generate_collision=False;data.generate_lightmap_u_vs=False
  t=unreal.AssetImportTask();t.filename=os.path.join(root,name+'.fbx');t.destination_path=DEST;t.destination_name=name;t.automated=True;t.save=True;t.options=options;tasks.append(t)
tools.import_asset_tasks(tasks)
interior=unreal.load_asset(ART+'/M_FractureInterior')
if not interior:
 interior=tools.create_asset('M_FractureInterior',ART,unreal.Material,unreal.MaterialFactoryNew())
 ml=unreal.MaterialEditingLibrary;c=ml.create_material_expression(interior,unreal.MaterialExpressionConstant3Vector,-400,0);c.constant=unreal.LinearColor(.018,.013,.009,1);ml.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
 for value,prop in [(.65,unreal.MaterialProperty.MP_METALLIC),(.9,unreal.MaterialProperty.MP_ROUGHNESS)]:
  n=ml.create_material_expression(interior,unreal.MaterialExpressionConstant,-400,200);n.r=value;ml.connect_material_property(n,'',prop)
 ml.recompile_material(interior);unreal.EditorAssetLibrary.save_loaded_asset(interior)
materials={name:unreal.load_asset(ART+'/M_'+name) for name in ['DoorRust','DoorSteel','DoorLight']};materials['FractureInterior']=interior
sub=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
def assign(mesh):
 for i,slot in enumerate(mesh.static_materials):
  key=str(slot.material_slot_name).split('.')[0];assert key in materials,(mesh.get_name(),key);mesh.set_material(i,materials[key])
def clip(poly,n,c):
 result=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=a[0]*n[0]+a[1]*n[1]-c;db=b[0]*n[0]+b[1]*n[1]-c
  if da<=1e-7:result.append(a)
  if (da<0)!=(db<0):
   t=da/(da-db);result.append([a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])])
 return result
for door in manifest['doors']:
 mesh=unreal.load_asset(DEST+'/'+door['cracked_mesh']);assign(mesh);sub.remove_collisions(mesh);sub.add_simple_collisions(mesh,unreal.ScriptingCollisionShapeType.BOX);unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
 for piece in door['pieces']:
  mesh=unreal.load_asset(DEST+'/'+piece['mesh']);assign(mesh);poly=piece['outline'];inner=list(poly)
  for a,b in zip(poly,poly[1:]+poly[:1]):
   n=(b[1]-a[1],a[0]-b[0]);size=math.hypot(*n);n=(n[0]/size,n[1]/size);inner=clip(inner,n,n[0]*a[0]+n[1]*a[1]-.35)
  bounds=mesh.get_bounds();ymin=bounds.origin.y-bounds.box_extent.y;ymax=bounds.origin.y+bounds.box_extent.y
  vertices=[(x,y,z) for y in [ymin,ymax] for x,z in inner]
  def vec(v):return '(X=%.6f,Y=%.6f,Z=%.6f)'%v
  low=tuple(min(v[i] for v in vertices) for i in range(3));high=tuple(max(v[i] for v in vertices) for i in range(3))
  shape=unreal.KConvexElem();assert shape.import_text('(VertexData=('+','.join(vec(v) for v in vertices)+'),ElemBox=(Min='+vec(low)+',Max='+vec(high)+',IsValid=True),Name="FractureHull")')
  body=unreal.new_object(unreal.BodySetup,outer=mesh);body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AND_COMPLEX);agg=unreal.KAggregateGeom();agg.set_editor_property('convex_elems',[shape]);body.set_editor_property('agg_geom',agg);mesh.modify();mesh.set_editor_property('body_setup',body);unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
 unreal.log('FRACTURE_IMPORTED '+str(door['index'])+' pieces='+str(door['count']))
placed=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
for actor in placed:
 if actor.get_class().get_name()!='BP_DestructibleDoor_C':continue
 door=manifest['doors'][actor.get_editor_property('BeaconIndex')-1]
 actor.set_editor_property('CrackedMesh',unreal.load_asset(DEST+'/'+door['cracked_mesh']))
 actor.set_editor_property('FragmentMeshes',[unreal.load_asset(DEST+'/'+p['mesh']) for p in door['pieces']]);actor.set_editor_property('FragmentOffsets',[unreal.Vector(*p['offset']) for p in door['pieces']]);actor.set_editor_property('DoorHeight',float(door['height']))
for name in ['BP_BaseEnemy','BP_ChargerEnemy']:
 bp=unreal.load_asset(E+name);unreal.get_default_object(bp.generated_class()).set_editor_property('ContactDamage',13.2);unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
bp=unreal.load_asset(R+'BP_DoorFragment');cdo=unreal.get_default_object(bp.generated_class());comp=cdo.static_mesh_component;comp.set_static_mesh(None);comp.set_mobility(unreal.ComponentMobility.MOVABLE);comp.set_collision_profile_name('PhysicsActor');comp.set_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN,unreal.CollisionResponseType.ECR_IGNORE);comp.set_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA,unreal.CollisionResponseType.ECR_IGNORE);comp.set_editor_property('can_ever_affect_navigation',False);unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('FRACTURED_DOORS_AND_13_2_DAMAGE_PREPARED')
