"""Read-only cold-load audit in a normal editor, without the authoring helper."""
import unreal,os,json
ues=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
assert not ues.get_game_world() and ues.get_editor_world().get_name()=='Nivel_Entrega'
assert not hasattr(unreal,'DeliveryBlueprintBuilder'),'Use the normal editor for this proof'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
cinemas=[a for a in actors if a.get_class().get_name()=='BP_CinematicDirector_C']
assert len(cinemas)==1 and not cinemas[0].get_editor_property('is_spatially_loaded')
rows=[]
for name,seconds,cuts in [('LS_Intro',18,3),('LS_Derrota',8,1),('LS_Victoria',14,3),('LS_Revelacion',12,3)]:
    seq=unreal.load_asset('/Game/ThirdPerson/Cinematics/'+name);assert seq
    assert seq.get_playback_end()==seconds*30
    cut=next(t for t in seq.get_tracks() if isinstance(t,unreal.MovieSceneCameraCutTrack));assert len(cut.get_sections())==cuts
    audio=next(t for t in seq.get_tracks() if isinstance(t,unreal.MovieSceneAudioTrack))
    assert audio.get_sections()[0].get_sound()
    rows.append(name)
director=next(a for a in actors if a.get_class().get_name()=='BP_DirectorEntrega_C')
zone=director.get_editor_property('Zona3');assert zone and not zone.get_editor_property('is_spatially_loaded')
assert zone.get_editor_property('bFinalStand') and zone.get_editor_property('bMixedEnemies') and zone.get_editor_property('WaveCount')==2
assert zone.get_editor_property('RequiredZone')==director.get_editor_property('Zona2')
for i in [1,2]:assert not director.get_editor_property('Zona'+str(i)).get_editor_property('bFinalStand')
for name in ['BP_BaseEnemy','BP_ChargerEnemy']:
    cdo=unreal.get_default_object(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/'+name+'.'+name+'_C'))
    assert abs(cdo.get_editor_property('ContactDamage')-13.2)<.001 and not cdo.is_actor_tick_enabled()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert not dirty,[p.get_path_name() for p in dirty]
result={'passed':True,'normal_editor_without_helper':True,'sequences':rows,'one_resident_cinematic_director':True,'enemy_damage_13_2_preserved':True,'no_pie':True,'dirty_packages':[]}
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/cinematics/cold-reload.json'),'w') as f:json.dump(result,f,indent=2)
unreal.log('CINEMA_COLD_RELOAD_PASSED '+json.dumps(result))
