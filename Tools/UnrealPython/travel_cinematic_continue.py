"""Exercise the same Continue flag and level travel used by the main menu."""
import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
assert not unreal.GameplayStatics.is_game_paused(w)
gi=unreal.GameplayStatics.get_game_instance(w)
unreal.get_default_object(unreal.SystemLibrary).call_method('SetBoolPropertyByName',(gi,'bDeliveryContinue',True))
unreal.GameplayStatics.open_level(w,'/Game/ThirdPerson/Maps/Nivel_Entrega',True,'')
unreal.log('CINEMA_CONTINUE_TRAVEL_REQUESTED')
