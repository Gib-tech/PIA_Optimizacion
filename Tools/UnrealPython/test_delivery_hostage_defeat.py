"""Isolated hostile damage tests hostage defeat without changing the checkpoint."""
import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
h=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
enemy=unreal.get_default_object(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C'))
unreal.GameplayStatics.apply_damage(h,1000,None,enemy,None)
assert h.get_editor_property('bIsDead')
unreal.log('SAVE_HOSTAGE_DEFEAT_TRIGGERED_BY_HOSTILE_DAMAGE')
