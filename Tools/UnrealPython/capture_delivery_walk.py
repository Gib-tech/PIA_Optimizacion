"""Record the real traversal outcome before leaving PIE."""
import unreal, os, json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
R='/Game/ThirdPerson/Blueprints/Entrega/'
d=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,R+'BP_DirectorEntrega.BP_DirectorEntrega_C'))
assert d.get_editor_property('Paso')==4
unreal.SystemLibrary.execute_console_command(w,'Shot showui')
unreal.log('DELIVERY_WALK_VICTORY_CONFIRMED')
