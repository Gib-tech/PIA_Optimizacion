"""Install cyclic dialogue signatures before final callers and save the WP map."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/';E='/Game/ThirdPerson/Blueprints/EnemigoIA/'
paths=['/Game/ThirdPerson/Cinematics/BP_CinematicDirector',E+'BP_BaseEnemy',R+'BP_CombatZone',R+'BP_DirectorEntrega',R+'BP_BeaconEntrega','/Game/ThirdPerson/Blueprints/Aliado/BTTask_ActivateBeacon',R+'BP_DeliverySaveManager',R+'BP_HUD_Entrega','/Game/ThirdPerson/Cinematics/BP_CinematicDirector']
for path in paths:
    bp=unreal.load_asset(path);unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
    assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs',bp.get_name()+'.t3d')),path
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
    unreal.log('FINAL_WORDS_INSTALLED '+path)
# Recompile dependent classes after the shared enemy/zone layouts change.
for path in paths+[E+'BP_ChargerEnemy','/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage',R+'BP_PlayerEntrega']:
    bp=unreal.load_asset(path);unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
    t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(root,'Intermediate/inspect/live',bp.get_name()+'.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;assert unreal.Exporter.run_asset_export_task(t)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=[p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() if p.get_path_name().startswith('/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/')]
if dirty:unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
unreal.log('FINAL_WORDS_INSTALL_COMPLETE')
