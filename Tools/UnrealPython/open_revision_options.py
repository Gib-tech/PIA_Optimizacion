import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
u=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C'))
u.call_method('OpenPause');q=u.get_editor_property('PauseWidget');q.call_method('BndEvt__Menu_Pausa_btn_opciones_pausa_Control_1_OnButtonClickedEvent__DelegateSignature')
