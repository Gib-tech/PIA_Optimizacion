"""Install only presentation and the three terminal/HUD hooks, then save WP actors."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
paths=['/Game/ThirdPerson/Cinematics/BP_CinematicDirector','/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage','/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega','/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega']
for path in paths:
    bp=unreal.load_asset(path);unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
    assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs',bp.get_name()+'.t3d')),path
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
    unreal.log('CINEMA_INSTALLED '+path)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors=[a for a in sub.get_all_level_actors() if a.get_class().get_name()=='BP_CinematicDirector_C']
assert len(actors)<=1
a=actors[0] if actors else sub.spawn_actor_from_class(unreal.load_class(None,paths[0]+'.BP_CinematicDirector_C'),unreal.Vector(0,0,0))
a.modify();a.set_actor_label('Cinematicas_TIME_OUT');a.set_folder_path('Mision/Cinematicas');a.set_editor_property('is_spatially_loaded',False)
for path in paths+['/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager','/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega']:
    bp=unreal.load_asset(path);unreal.BlueprintEditorLibrary.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
    t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(root,'Intermediate/inspect/live',bp.get_name()+'.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;assert unreal.Exporter.run_asset_export_task(t)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=[p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() if p.get_path_name().startswith('/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/')]
if dirty:unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
unreal.log('CINEMA_RUNTIME_INSTALLED')
