import unreal,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics
for path,fields in [('/Game/ThirdPerson/Blueprints/Entrega/BP_SistemasComplementarios',['bInitialized','Hero','Director','Tecnico','Sun','WorldSeconds']),('/Game/ThirdPerson/Cinematics/BP_CinematicDirector',['bInitialized','bActive','Hero','Hostage','Director','GameHUD']),('/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager',['bInitialized','Hero','Director','Extras'])]:
 a=gs.get_actor_of_class(w,unreal.load_class(None,path+'.'+path.rsplit('/',1)[-1]+'_C'))
 unreal.log('CURRENT_RUNTIME '+path+' '+json.dumps({f:str(a.get_editor_property(f)) for f in fields}))
unreal.log('PLAYER '+str(gs.get_player_character(w,0)))
unreal.log('CALLBACK_STATE '+str(globals().get('s')))
