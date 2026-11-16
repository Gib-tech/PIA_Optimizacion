"""Import our fitted door kit and create the editable progression Blueprint fields."""
import unreal,os,json
R='/Game/ThirdPerson/Blueprints/Entrega/'
A='/Game/ThirdPerson/Blueprints/Aliado/'
E='/Game/ThirdPerson/Blueprints/EnemigoIA/'
ART='/Game/ThirdPerson/Environment/Progression'
lib=unreal.BlueprintEditorLibrary; tools=unreal.AssetToolsHelpers.get_asset_tools()
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
tasks=[]
for name in ['SM_DoorPanel_01','SM_DoorPanel_02','SM_DoorPanel_03','SM_DoorFrame_01','SM_DoorFrame_02','SM_DoorFrame_03','SM_BulkheadModule','SM_DoorFragment']:
 if unreal.load_asset(ART+'/'+name):continue
 options=unreal.FbxImportUI();options.automated_import_should_detect_type=False;options.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH;options.import_materials=False;options.import_textures=False
 data=options.static_mesh_import_data;data.combine_meshes=True;data.auto_generate_collision=False;data.generate_lightmap_u_vs=True
 task=unreal.AssetImportTask();task.filename=os.path.join(project,'Tools/ArtSource/Progression',name+'.fbx');task.destination_path=ART;task.destination_name=name;task.automated=True;task.save=True;task.options=options;tasks.append(task)
tools.import_asset_tasks(tasks)
audio_tasks=[]
for name in ['Upgrade','DoorHit','DoorBreak']:
 if unreal.load_asset('/Game/ThirdPerson/Audio/SW_'+name):continue
 task=unreal.AssetImportTask();task.filename=os.path.join(project,'Tools/AudioSource/SW_'+name+'.wav');task.destination_path='/Game/ThirdPerson/Audio';task.destination_name='SW_'+name;task.automated=True;task.save=True;audio_tasks.append(task)
tools.import_asset_tasks(audio_tasks)
materials={}
for name,color,metal,rough,emissive in [('DoorSteel',(.075,.095,.115),.8,.55,0),('DoorRust',(.21,.105,.052),.55,.85,0),('DoorLight',(.8,.12,.015),.4,.4,2),('DoorPowered',(.08,.7,1),.4,.4,5)]:
 m=unreal.load_asset(ART+'/M_'+name)
 if not m:
  m=tools.create_asset('M_'+name,ART,unreal.Material,unreal.MaterialFactoryNew())
  c=unreal.MaterialEditingLibrary.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-400,0);c.constant=unreal.LinearColor(*color,1)
  unreal.MaterialEditingLibrary.connect_material_property(c,'',unreal.MaterialProperty.MP_BASE_COLOR)
  for val,prop in [(metal,unreal.MaterialProperty.MP_METALLIC),(rough,unreal.MaterialProperty.MP_ROUGHNESS)]:
   n=unreal.MaterialEditingLibrary.create_material_expression(m,unreal.MaterialExpressionConstant,-400,200);n.r=val;unreal.MaterialEditingLibrary.connect_material_property(n,'',prop)
  if emissive:
   c.constant=unreal.LinearColor(*(x*emissive for x in color),1);unreal.MaterialEditingLibrary.connect_material_property(c,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
  unreal.MaterialEditingLibrary.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m)
 materials[name]=m
materials['WallStone']=unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/Sector1')
sub=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for path in unreal.EditorAssetLibrary.list_assets(ART):
 mesh=unreal.load_asset(path)
 if not isinstance(mesh,unreal.StaticMesh):continue
 for i,slot in enumerate(mesh.static_materials):mesh.set_material(i,materials[str(slot.material_slot_name)])
 sub.remove_collisions(mesh)
 if 'Frame' not in mesh.get_name():sub.add_simple_collisions(mesh,unreal.ScriptingCollisionShapeType.BOX)
 unreal.EditorAssetLibrary.save_loaded_asset(mesh)
 b=mesh.get_bounds();unreal.log('ART_BOUNDS '+mesh.get_name()+' '+str(b.box_extent))

def shell(path,parent):
 bp=unreal.load_asset(path)
 if not bp:
  f=unreal.BlueprintFactory();f.set_editor_property('parent_class',parent);bp=tools.create_asset(path.rsplit('/',1)[1],path.rsplit('/',1)[0],unreal.Blueprint,f)
 return bp
door=shell(R+'BP_DestructibleDoor',unreal.StaticMeshActor)
beacon=shell(R+'BP_BeaconEntrega',unreal.StaticMeshActor)
fragment=shell(R+'BP_DoorFragment',unreal.StaticMeshActor)
task=shell(A+'BTTask_ActivateBeacon',unreal.BTTask_BlueprintBase)
specs={
 R+'BP_DestructibleDoor':{'BeaconIndex':'int','bUnlocked':'bool','bDestroyed':'bool','Health':'real'},
 R+'BP_BeaconEntrega':{'Index':'int','RequiredZone':R+'BP_CombatZone','Door':R+'BP_DestructibleDoor','ApproachPoint':'actor','bActivated':'bool','ActivationProgress':'real'},
 R+'BP_PlayerEntrega':{'bHammerUpgraded':'bool','bDoorPending':'bool','bHitboxOnHammer':'bool','bHeavyWindowManaged':'bool','HeavyWindowStart':'real','HeavyWindowEnd':'real','SwordHitboxRelativeTransform':'transform','UpgradeUntil':'real','RequiredDoor':R+'BP_DestructibleDoor'},
 A+'BP_Hostage':{'Health':'real','MaxHealth':'real','bIsDead':'bool','InvulnerableUntil':'real','bUsingBeacon':'bool','ActivationProgress':'real'},
 A+'BTTask_ActivateBeacon':{'Elapsed':'real','CachedPawn':A+'BP_Hostage','Beacon':R+'BP_BeaconEntrega'},
 E+'BP_BaseEnemy':{'CombatTarget':'actor','ChargeVictim':'actor'},
 E+'BTService_LocatePlayer':{'ChosenTarget':'actor'},E+'BTService_ChargerSense':{'ChosenTarget':'actor'},
}
for path,fields in specs.items():
 bp=unreal.load_asset(path);cdo=unreal.get_default_object(bp.generated_class())
 for name,kind in fields.items():
  try:cdo.get_editor_property(name);continue
  except Exception:pass
  typ=lib.get_object_reference_type(unreal.Actor if kind=='actor' else unreal.load_class(None,kind+'.'+kind.rsplit('/',1)[1]+'_C')) if kind=='actor' or kind.startswith('/') else (lib.get_struct_type(unreal.load_object(None,'/Script/CoreUObject.Transform')) if kind=='transform' else lib.get_basic_type_by_name(kind))
  assert lib.add_member_variable(bp,name,typ),(path,name)
  lib.set_blueprint_variable_instance_editable(bp,name,True)
 lib.compile_blueprint(bp);cdo=unreal.get_default_object(bp.generated_class())
 if path.endswith('BP_DestructibleDoor'):cdo.set_editor_property('Health',50.0)
 if path.endswith('BP_Hostage'):cdo.set_editor_property('Health',100.0);cdo.set_editor_property('MaxHealth',100.0)
 if path.endswith('BP_PlayerEntrega'):cdo.set_editor_property('HeavyWindowStart',.252330);cdo.set_editor_property('HeavyWindowEnd',1.183353)
 unreal.EditorAssetLibrary.save_loaded_asset(bp)
cdo=unreal.get_default_object(fragment.generated_class());comp=cdo.static_mesh_component;comp.set_static_mesh(unreal.load_asset(ART+'/SM_DoorFragment'));comp.set_mobility(unreal.ComponentMobility.MOVABLE);comp.set_collision_profile_name('PhysicsActor');comp.set_collision_response_to_channel(unreal.CollisionChannel.ECC_PAWN,unreal.CollisionResponseType.ECR_IGNORE);comp.set_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA,unreal.CollisionResponseType.ECR_IGNORE)
comp.set_editor_property('can_ever_affect_navigation',False)
unreal.EditorAssetLibrary.save_loaded_asset(fragment)
bb=unreal.load_asset(A+'BB_Hostage');entries=list(bb.get_editor_property('keys'));names=[str(e.get_editor_property('entry_name')) for e in entries]
for name,kind in [('bActivateBeacon','Bool'),('BeaconTarget','Object'),('ActiveBeacon','Object')]:
 if name in names:continue
 entry=unreal.BlackboardEntry();entry.set_editor_property('entry_name',name);key=unreal.new_object(unreal.load_class(None,'/Script/AIModule.BlackboardKeyType_'+kind),outer=bb)
 if kind=='Object':key.set_editor_property('BaseClass',unreal.Actor)
 entry.set_editor_property('key_type',key);entries.append(entry)
bb.set_editor_property('keys',entries);unreal.EditorAssetLibrary.save_loaded_asset(bb)
for name,source in [('NS_HammerUpgrade','RadialBurst'),('NS_DoorBreak','DirectionalBurst')]:
 if not unreal.load_asset(R+'FX/'+name):assert unreal.EditorAssetLibrary.duplicate_asset('/Niagara/DefaultAssets/Templates/Systems/'+source,R+'FX/'+name)
unreal.log('PROGRESSION_PREPARED')
