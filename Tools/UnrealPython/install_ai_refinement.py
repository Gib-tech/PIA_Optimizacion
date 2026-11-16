"""Apply the reviewed refinement graphs, balance, tree transitions and HUD mask.

Requires the optional editor-only build bridge already used for this delivery.
No native helper is referenced by the game assets.
"""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert hasattr(unreal,'DeliveryBlueprintBuilder'),'Launch the editor with the local BPB2 plugin'
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
E='/Game/ThirdPerson/Blueprints/EnemigoIA/'
A='/Game/ThirdPerson/Blueprints/Aliado/'
R='/Game/ThirdPerson/Blueprints/Entrega/'
lib=unreal.BlueprintEditorLibrary
specs={R+'BP_PlayerEntrega':{'LastAttackMontage':lib.get_object_reference_type(unreal.AnimMontage),'LastAttackPosition':lib.get_basic_type_by_name('real')},R+'BP_HUD_Entrega':{'HurtPulseUntil':lib.get_basic_type_by_name('real')},E+'BTTask_ChargerRetreat':{'RetreatGoal':lib.get_struct_type(unreal.load_object(None,'/Script/CoreUObject.Vector'))}}
for path,fields in specs.items():
 bp=unreal.load_asset(path);cdo=unreal.get_default_object(bp.generated_class())
 for name,typ in fields.items():
  try:cdo.get_editor_property(name)
  except Exception:assert lib.add_member_variable(bp,name,typ),(path,name)
 lib.compile_blueprint(bp)

task=unreal.AssetImportTask();task.filename=os.path.join(project,'Tools/ArtSource/UI/T_DamageCorners.tga');task.destination_path=R+'FX';task.destination_name='T_DamageCorners';task.automated=True;task.replace_existing=True;task.save=True
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
texture=unreal.load_asset(R+'FX/T_DamageCorners');assert texture
texture.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_EDITOR_ICON)
texture.set_editor_property('lod_group',unreal.TextureGroup.TEXTUREGROUP_UI)
texture.set_editor_property('address_x',unreal.TextureAddress.TA_CLAMP);texture.set_editor_property('address_y',unreal.TextureAddress.TA_CLAMP)
unreal.EditorAssetLibrary.save_loaded_asset(texture,only_if_is_dirty=False)

names=[(E,n) for n in ['BP_ChargerController','BTService_LocatePlayer','BTTask_Attack','BTTask_ChargerWindup','BTTask_ChargerCharge','BTTask_ChargerRetreat']]+[(A,'BTService_HostageSense')]+[(R,n) for n in ['BP_PlayerEntrega','BP_BeaconEntrega','BP_CombatZone']]+[(A,n) for n in ['BP_Hostage','BTTask_ActivateBeacon']]+[(R,n) for n in ['BP_DirectorEntrega','BP_HUD_Entrega']]
for folder,name in names:
 bp=unreal.load_asset(folder+name)
 unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
 assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(project,'Intermediate/inspect/delivery_graphs',name+'.t3d')),name
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(project,'Intermediate/inspect/live',name+'.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;unreal.Exporter.run_asset_export_task(t)
 unreal.log('REFINEMENT_INSTALLED '+name)

for name in ['BP_BaseEnemy','BP_ChargerEnemy']:
 bp=unreal.load_asset(E+name);bp.modify();cdo=unreal.get_default_object(bp.generated_class())
 cdo.set_editor_property('use_controller_rotation_yaw',False)
 cdo.character_movement.set_editor_property('orient_rotation_to_movement',True)
 cdo.character_movement.set_editor_property('use_controller_desired_rotation',False)
 cdo.character_movement.set_editor_property('rotation_rate',unreal.Rotator(yaw=540))
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)

bp=unreal.load_asset(A+'BTService_HostageSense');cdo=unreal.get_default_object(bp.generated_class())
for name,value in [('SafePlayerDistance',600.),('SafeEnemyDistance',950.)]:cdo.set_editor_property(name,value)
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
tree=unreal.load_asset(E+'BT_Charger')
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(tree)
# During charge cooldown, a valid target must never fall through into random roam.
dec=unreal.find_object(None,tree.get_path_name()+':BTDecorator_Blackboard_8');dec.set_editor_property('FloatValue',0.)
for name in ['Instance_6','Instance_10']:
 wait=unreal.find_object(None,tree.get_path_name()+':'+name);v=wait.get_editor_property('WaitTime');v.set_editor_property('DefaultValue',.8);wait.set_editor_property('WaitTime',v)
unreal.EditorAssetLibrary.save_loaded_asset(tree,only_if_is_dirty=False)
t=unreal.AssetExportTask();t.object=tree;t.filename=os.path.join(project,'Intermediate/inspect/live/BT_Charger.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;unreal.Exporter.run_asset_export_task(t)
unreal.log('AI_REFINEMENT_INSTALLED')
