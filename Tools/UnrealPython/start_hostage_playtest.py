import unreal
root='/Game/ThirdPerson/Blueprints/Aliado/'
sub=unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
for name in ['BP_HostageController','BP_Hostage','BTTask_HostageArrive','BTService_HostageSense','BT_Hostage','ABP_Hostage']:
    sub.close_all_editors_for_asset(unreal.load_asset(root+name))
for name in ['BP_DirectorEntrega','BP_HUD_Entrega']:
    sub.close_all_editors_for_asset(unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/'+name))
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).editor_request_begin_play()
