"""Install arrival-first strikes and accepted-hit signals, preserving trees and balance."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert hasattr(unreal,'DeliveryBlueprintBuilder'),'Open editor with Tools/EditorBridge BPB3'
combat_root=unreal.Paths.project_dir();E='/Game/ThirdPerson/Blueprints/EnemigoIA/';A='/Game/ThirdPerson/Blueprints/Aliado/';R='/Game/ThirdPerson/Blueprints/Entrega/'
combat_lib=unreal.BlueprintEditorLibrary
combat_fields={E+'BP_BaseEnemy':{'bAttackResolved':'bool','LastFeedbackHealth':'real'},E+'BTTask_ChargerCharge':{'bAttackStarted':'bool'},A+'BP_Hostage':{'DamageNoticeSerial':'int'},R+'BP_HUD_Entrega':{'LastHostageHitSerial':'int','HostageHurtUntil':'real','HostageAlertCooldown':'real','EnemyHitUntil':'real','LastEnemyDamage':'real'}}
for path,fields in combat_fields.items():
 combat_bp=unreal.load_asset(path)
 for name,kind in fields.items():
  try:unreal.get_default_object(combat_bp.generated_class()).get_editor_property(name)
  except Exception:assert combat_lib.add_member_variable(combat_bp,name,combat_lib.get_basic_type_by_name(kind)),(path,name)
 combat_lib.compile_blueprint(combat_bp)
for folder,name in [(A,'BP_Hostage'),(R,'BP_HUD_Entrega'),(E,'BP_BaseEnemy'),(E,'BTTask_Attack'),(E,'BTTask_ChargerWindup'),(E,'BTTask_ChargerCharge')]:
 combat_bp=unreal.load_asset(folder+name);unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(combat_bp)
 assert unreal.DeliveryBlueprintBuilder.install_graph(combat_bp,os.path.join(combat_root,'Intermediate/inspect/delivery_graphs',name+'.t3d')),name
 unreal.EditorAssetLibrary.save_loaded_asset(combat_bp,only_if_is_dirty=False)
 combat_export=unreal.AssetExportTask();combat_export.object=combat_bp;combat_export.filename=os.path.join(combat_root,'Intermediate/inspect/live',name+'.t3d');combat_export.automated=True;combat_export.prompt=False;combat_export.replace_identical=True;assert unreal.Exporter.run_asset_export_task(combat_export)
 unreal.log('COMBAT_FEEDBACK_INSTALLED '+name)
combat_child=unreal.load_asset(E+'BP_ChargerEnemy');combat_lib.compile_blueprint(combat_child);unreal.EditorAssetLibrary.save_loaded_asset(combat_child,only_if_is_dirty=False)
assert abs(unreal.get_default_object(combat_child.generated_class()).get_editor_property('ContactDamage')-13.2)<.001
# Recompile dependency callers after the Hostage class layout changes.
for name in ['BP_DirectorEntrega','BP_DeliverySaveManager']:
 combat_bp=unreal.load_asset(R+name);combat_lib.compile_blueprint(combat_bp);unreal.EditorAssetLibrary.save_loaded_asset(combat_bp,only_if_is_dirty=False)
unreal.log('COMBAT_FEEDBACK_INSTALL_COMPLETE')
