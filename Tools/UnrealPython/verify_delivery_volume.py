"""Record rendered master audio at full and quarter volume for WAV RMS comparison."""
import unreal,time,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs=unreal.GameplayStatics
ui=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C'))
audio=unreal.get_default_object(unreal.load_class(None,'/Script/AudioMixer.AudioMixerBlueprintLibrary'))
native_gs=unreal.get_default_object(unreal.GameplayStatics.static_class())
system=unreal.get_default_object(unreal.SystemLibrary.static_class())
path=os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()),'Intermediate/inspect/volume-audio');os.makedirs(path,exist_ok=True)
s={'stage':0,'at':time.monotonic(),'handle':None,'recording':False,'last_sound':0}
def observe(dt,state=s,world=w,interface=ui,mixer=audio,system=system,folder=path,play=native_gs):
 try:
  now=time.monotonic();age=now-state['at']
  if state['stage'] in [0,2]:
   if state['stage']==2 and age<1:return
   system.call_method('SetDoublePropertyByName',(interface,'MasterVolume',1. if state['stage']==0 else .25))
   interface.call_method('ApplyVolume');state.update(stage=state['stage']+1,at=now,recording=False)
  elif state['stage'] in [1,3]:
   if age<1.5:return
   if not state['recording']:
    mixer.call_method('StartRecordingOutput',(world,2.,None));state.update(recording=True,at=now,last_sound=0);return
   if now-state['last_sound']>.2:
    sound=unreal.load_asset('/Game/ThirdPerson/Audio/SW_Text')
    play.call_method('PlaySound2D',(world,sound,1.,1.,0.,None,None,True));state['last_sound']=now
   if age>=1.2:
    name='full' if state['stage']==1 else 'quarter'
    mixer.call_method('StopRecordingOutput',(world,unreal.AudioRecordingExportType.WAV_FILE,name,folder,None,None))
    if state['stage']==1:state.update(stage=2,at=now)
    else:
     unreal.unregister_slate_post_tick_callback(state['handle'])
     system.call_method('SetDoublePropertyByName',(interface,'MasterVolume',.25));interface.call_method('ApplyVolume')
     unreal.log('VOLUME_RECORDINGS_READY '+folder)
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle']);unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
