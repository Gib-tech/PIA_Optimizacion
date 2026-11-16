"""Isolate defeat using the real damage event; the saved checkpoint must survive."""
import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_character(w,0)
unreal.GameplayStatics.apply_damage(p,1000,None,None,None)
unreal.log('SAVE_DEFEAT_TRIGGERED_BY_REAL_DAMAGE')
