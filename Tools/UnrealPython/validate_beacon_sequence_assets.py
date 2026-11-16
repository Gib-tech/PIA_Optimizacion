"""Export the installed challenge and save all owned dependencies before cooking."""
import unreal,os,json
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
R='/Game/ThirdPerson/Blueprints/Entrega/'
paths=[R+n for n in ['BP_DirectorEntrega','BP_BeaconEntrega','BP_BeaconLabel','BP_DeliverySave','BP_DeliverySaveManager','BP_HUD_Entrega']]
paths+=['/Game/ThirdPerson/Blueprints/Aliado/BTTask_ActivateBeacon','/Game/Menu/Menu_Inicio','/Game/LevelMenu/BP_GameInstance']
for path in paths:
 bp=unreal.load_asset(path);unreal.BlueprintEditorLibrary.compile_blueprint(bp)
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
 t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(root,'Intermediate/inspect/live',bp.get_name()+'.t3d')
 t.automated=True;t.prompt=False;t.replace_identical=True;assert unreal.Exporter.run_asset_export_task(t)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
d=next(a for a in actors if a.get_class().get_name()=='BP_DirectorEntrega_C')
bs=[d.get_editor_property('Baliza'+str(i)) for i in (1,2,3)]
assert [b.get_editor_property('Index') for b in bs]==[1,2,3]
assert all(b.static_mesh_component.static_mesh.get_name()=='SM_Baliza' for b in bs)
assert len([a for a in actors if a.get_class().get_name()=='BP_BeaconLabel_C'])==3
assert len([a for a in actors if a.get_actor_label().startswith('Refugio_Baliza_')])==6
assert len([a for a in actors if a.get_class().get_name()=='BP_CombatZone_C'])==2
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
report={'passed':True,'compiled_exported_assets':paths,'stable_identities':[1,2,3],'team_model_instances':3,'labels':3,'local_refuges':6,'combat_zones':2,'dirty_packages':[],'cook_required_for_final_compilation_check':True}
with open(os.path.join(root,'Intermediate/inspect/beacon_assets_assertions.json'),'w') as f:json.dump(report,f,indent=2)
unreal.log('BEACON_ASSETS_VALIDATED')
