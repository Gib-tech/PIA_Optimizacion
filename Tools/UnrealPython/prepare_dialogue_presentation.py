"""Replace world text with the retro dialogue HUD; import original audio and set editable defaults."""
import unreal,os
ROOT='/Game/ThirdPerson/Blueprints/Entrega/'
bp=unreal.load_asset(ROOT+'BP_HUD_Entrega');lib=unreal.BlueprintEditorLibrary
types={'CachedDirector':lib.get_object_reference_type(unreal.load_class(None,ROOT+'BP_DirectorEntrega.BP_DirectorEntrega_C')),'CachedHostage':lib.get_object_reference_type(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C')),'AmbientAudio':lib.get_object_reference_type(unreal.AudioComponent)}
for name in ['CurrentDialog','LastDialog','DismissedDialog','VisibleCharacters']:types[name]=lib.get_basic_type_by_name('int')
for name in ['DialogStarted','LastBeepAt','LastHealth','CharactersPerSecond','HoldSeconds','UIAudioVolume']:types[name]=lib.get_basic_type_by_name('real')
for name in ['ForceReveal','DialogueVisible']:types[name]=lib.get_basic_type_by_name('bool')
for name in ['FullText','VisibleText','Speaker','ActionHint']:types[name]=lib.get_basic_type_by_name('string')
cdo=unreal.get_default_object(bp.generated_class())
for name,typ in types.items():
    try:cdo.get_editor_property(name)
    except Exception:assert lib.add_member_variable(bp,name,typ)
for name in ['CharactersPerSecond','HoldSeconds','UIAudioVolume']:lib.set_blueprint_variable_instance_editable(bp,name,True)
lib.compile_blueprint(bp);cdo=unreal.get_default_object(bp.generated_class())
for name,value in [('LastDialog',-1),('DismissedDialog',-1),('LastHealth',100.0),('CharactersPerSecond',42.0),('HoldSeconds',4.5),('UIAudioVolume',.32)]:cdo.set_editor_property(name,value)
cdo.set_editor_property('auto_receive_input',unreal.AutoReceiveInput.PLAYER0)
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
tasks=[]
for name in ['Text','Open','Rescue','Alert','Clear','Victory','Defeat','PlayerHurt','Ambience']:
    task=unreal.AssetImportTask();task.filename=os.path.join(project,'Tools/AudioSource/SW_'+name+'.wav');task.destination_path='/Game/ThirdPerson/Audio';task.destination_name='SW_'+name;task.automated=True;task.replace_existing=True;task.save=True;tasks.append(task)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
ambience=unreal.load_asset('/Game/ThirdPerson/Audio/SW_Ambience');ambience.set_editor_property('looping',True);unreal.EditorAssetLibrary.save_loaded_asset(ambience,only_if_is_dirty=False)
# Remove labels including the old beacon TextRenderActors; keep the physical beacons and exit.
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for actor in list(sub.get_all_level_actors()):
    if isinstance(actor,unreal.TextRenderActor) or actor.get_actor_label().startswith('Limite_Zona_'):sub.destroy_actor(actor)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('DIALOGUE_PRESENTATION_PREPARED: no floating text; 9 original sounds')
