import unreal
sub=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
for name in ['BP_DirectorEntrega','BP_HUD_Entrega']:
    sub.close_all_editors_for_asset(unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/'+name))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
unreal.log('DELIVERY_PLAYTEST_STARTED')
