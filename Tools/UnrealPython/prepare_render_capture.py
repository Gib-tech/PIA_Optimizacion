import unreal,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
u=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C'))
if u.get_editor_property('bOptionsOpen'):u.call_method('CloseOptions')
if u.get_editor_property('bPauseOpen'):u.call_method('ClosePause')
unreal.SystemLibrary.execute_console_command(w,'stat none')
unreal.SystemLibrary.execute_console_command(w,'stat RHI')
folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/rendimiento-2026-11-17')
s={'handle':None,'at':unreal.GameplayStatics.get_real_time_seconds(w)}
def tick(dt,state=s):
 if unreal.GameplayStatics.get_real_time_seconds(w)-state['at']<3:return
 unreal.unregister_slate_post_tick_callback(state['handle'])
 unreal.SystemLibrary.execute_console_command(w,'Shot showui filename="'+os.path.join(folder,'rhi-ui.png').replace('\\','/')+'" -nosuffix')
s['handle']=unreal.register_slate_post_tick_callback(tick)
