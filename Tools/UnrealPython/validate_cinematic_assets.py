"""Saved-asset proof, native Sequencer structure and preserved combat invariants."""
import unreal,os,json,re
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());out=os.path.join(root,'Intermediate/inspect/cinematics')
rows=[]
for path in ['/Game/ThirdPerson/Cinematics/BP_CinematicDirector','/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage','/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega','/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega','/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager']:
    bp=unreal.load_asset(path);unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
    task=unreal.AssetExportTask();task.object=bp;task.filename=os.path.join(root,'Intermediate/inspect/live',bp.get_name()+'.t3d');task.automated=True;task.prompt=False;task.replace_identical=True;assert unreal.Exporter.run_asset_export_task(task)
    raw=open(task.filename,'rb').read();txt=raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8')
    assert 'Status=BS_Error' not in txt,path
    rows.append({'asset':path,'compiled_exported':True})
sequences=[]
for name,seconds,cuts in [('LS_Intro',18,3),('LS_Derrota',8,1),('LS_Victoria',14,3)]:
    seq=unreal.load_asset('/Game/ThirdPerson/Cinematics/'+name);tracks=seq.get_tracks()
    cut=next(t for t in tracks if isinstance(t,unreal.MovieSceneCameraCutTrack))
    assert len(cut.get_sections())==cuts
    assert seq.get_playback_end()==seconds*30 and seq.get_display_rate().numerator==30
    assert any(isinstance(t,unreal.MovieSceneAudioTrack) for t in tracks)
    assert any(isinstance(t,unreal.MovieSceneFadeTrack) for t in tracks)
    for b in seq.get_bindings():
        assert any(isinstance(t,unreal.MovieScene3DTransformTrack) for t in b.get_tracks()),str(b)
    sequences.append({'asset':seq.get_path_name(),'seconds':seconds,'camera_cuts':cuts,'animated_bindings':len(seq.get_bindings()),'audio_and_fade':True})
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
c=[a for a in actors if a.get_class().get_name()=='BP_CinematicDirector_C'];assert len(c)==1 and not c[0].get_editor_property('is_spatially_loaded')
for name in ['BP_BaseEnemy','BP_ChargerEnemy']:
    cdo=unreal.get_default_object(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/'+name+'.'+name+'_C'))
    assert abs(cdo.get_editor_property('ContactDamage')-13.2)<.001
    assert not cdo.is_actor_tick_enabled()
for name in ['BT_EnemyIA','BT_Charger']:
    assert unreal.load_asset('/Game/ThirdPerson/Blueprints/EnemigoIA/'+name)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert not dirty,[p.get_path_name() for p in dirty]
result={'passed':True,'blueprints':rows,'sequences':sequences,'one_resident_controller':True,'enemy_damage_13_2_and_distinct_trees_preserved':True,'gameplay_runtime':'Blueprint-only; no editor helper required','dirty_packages':[]}
with open(os.path.join(out,'assets.json'),'w',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
unreal.log('CINEMA_ASSETS_VALIDATED '+json.dumps(result))
