"""Importa brazos ligeros y agrega componentes visuales a BP_PlayerEntrega."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
path='/Game/ThirdPerson/Characters/PrimeraPersona/'
mesh=unreal.load_asset(path+'SK_BrazosPrimeraPersona')
if not mesh:
 unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
 options=unreal.FbxImportUI();options.set_editor_property('import_as_skeletal',True)
 options.set_editor_property('mesh_type_to_import',unreal.FBXImportType.FBXIT_SKELETAL_MESH)
 options.set_editor_property('automated_import_should_detect_type',False)
 options.set_editor_property('skeleton',unreal.load_asset('/Game/SciFITrooper_Man_03/SkeletalMesh/CH_SciFiTrooper_Man_03_Skeleton'))
 options.set_editor_property('import_animations',False);options.set_editor_property('import_materials',False);options.set_editor_property('import_textures',False)
 options.set_editor_property('create_physics_asset',False)
 task=unreal.AssetImportTask();task.filename=os.path.join(root,'Tools/ArtSource/FirstPerson/SK_BrazosPrimeraPersona.fbx')
 task.destination_path=path.rstrip('/');task.destination_name='SK_BrazosPrimeraPersona'
 task.automated=True;task.save=True;task.options=options;task.replace_existing=True
 unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);mesh=unreal.load_asset(path+'SK_BrazosPrimeraPersona');assert mesh
source=unreal.load_asset('/Game/SciFITrooper_Man_03/SkeletalMesh/SK_SciFITrooper_Man_03')
mesh.set_editor_property('materials',source.get_editor_property('materials'))
unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega')
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);fn=unreal.SubobjectDataBlueprintFunctionLibrary
handles=sub.k2_gather_subobject_data_for_blueprint(bp)
def component(name,cls,parent):
 for h in sub.k2_gather_subobject_data_for_blueprint(bp):
  obj=fn.get_object(fn.get_data(h))
  if obj.get_name()==name+'_GEN_VARIABLE':return h,obj
 h,error=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=parent,new_class=cls,blueprint_context=bp))
 assert not str(error),str(error)
 assert sub.rename_subobject(h,unreal.Text(name))
 return h,fn.get_object(fn.get_data(h))
arms_h,arms=component('BrazosFP',unreal.SkeletalMeshComponent,handles[0])
arms.set_skeletal_mesh_asset(mesh)
body=unreal.get_default_object(bp.generated_class()).mesh
for i,m in enumerate(body.get_materials()):arms.set_material(i,m)
_,sword=component('EspadaFP',unreal.StaticMeshComponent,arms_h)
sword.set_static_mesh(unreal.load_asset('/Game/Fab/long_sword/longsword'))
_,hammer=component('MartilloFP',unreal.SkeletalMeshComponent,arms_h)
hammer.set_skeletal_mesh_asset(unreal.load_asset('/Game/ThirdPerson/Bp_Modelos/Decahammer/SkeletalMeshes/Decahammer'))
_,fill=component('LuzFP',unreal.PointLightComponent,handles[0])
fill.set_editor_property('intensity',250);fill.set_editor_property('attenuation_radius',180);fill.set_cast_shadows(False)
fill.set_editor_property('lighting_channels',unreal.LightingChannels(channel0=False,channel1=True,channel2=False))
for c in [arms,sword,hammer]:
 c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);c.set_editor_property('generate_overlap_events',False)
 c.set_cast_shadow(False);c.set_editor_property('only_owner_see',True)
 c.set_editor_property('visible',False)
 c.set_editor_property('can_ever_affect_navigation',False)
 c.set_editor_property('receives_decals',False)
 c.set_editor_property('lighting_channels',unreal.LightingChannels(channel0=False,channel1=True,channel2=False))
arms.set_editor_property('visibility_based_anim_tick_option',unreal.VisibilityBasedAnimTickOption.ALWAYS_TICK_POSE_AND_REFRESH_BONES)
for name in ['FPBobTime','FPSwayYaw','FPSwayPitch','FPLastYaw','FPLastPitch','FPHeight','FPForward','FPIdleSwordPosition','FPIdleHammerPosition','FPRollSword']:
 try:unreal.get_default_object(bp.generated_class()).get_editor_property(name)
 except Exception:unreal.BlueprintEditorLibrary.add_member_variable(bp,name,unreal.BlueprintEditorLibrary.get_basic_type_by_name('real'))
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
defaults=unreal.get_default_object(bp.generated_class());defaults.set_editor_property('FPHeight',-17);defaults.set_editor_property('FPForward',55)
defaults.set_editor_property('FPIdleSwordPosition',0);defaults.set_editor_property('FPIdleHammerPosition',0);defaults.set_editor_property('FPRollSword',-70)
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.log('FIRST_PERSON_COMPONENTS_READY')
