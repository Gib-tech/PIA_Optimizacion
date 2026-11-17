"""Copias de secuencias para muestreo visual sin ejecutar notificaciones."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
rows=json.load(open(os.path.join(root,'Intermediate/inspect/player_animations/sources.json')))
out=[]
for row in rows:
 if len(row['sequences'])!=1 or 'Death_Montage' in row['montage']:continue
 name='AFP_'+row['montage'].rsplit('/',1)[-1].split('.')[0].removesuffix('_Montage')
 path='/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/'+name
 asset=unreal.load_asset(path) or unreal.EditorAssetLibrary.duplicate_asset(row['sequences'][0],path)
 unreal.AnimationLibrary.remove_all_animation_notify_tracks(asset)
 unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
 out.append({'montage':row['montage'],'sequence':asset.get_path_name()})
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega')
try:unreal.get_default_object(bp.generated_class()).get_editor_property('LastFPAnimation')
except Exception:unreal.BlueprintEditorLibrary.add_member_variable(bp,'LastFPAnimation',unreal.BlueprintEditorLibrary.get_object_reference_type(unreal.AnimSequence))
unreal.BlueprintEditorLibrary.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
with open(os.path.join(root,'Intermediate/inspect/player_animations/first_person.json'),'w') as f:json.dump(out,f,indent=2)
with open(os.path.join(root,'Tools/ArtSource/FirstPerson/animation_manifest.json'),'w') as f:json.dump(out,f,indent=2)
unreal.log('FIRST_PERSON_ANIMATION_COPIES '+str(len(out)))
