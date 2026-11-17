"""Read-only runtime survey of the proposed final encounter corridor."""
import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0)
for pos in [(-350,-7700,90),(350,-7700,90),(0,-6500,90)]:
    path=unreal.NavigationSystemV1.find_path_to_location_synchronously(w,unreal.Vector(0,-6700,90),unreal.Vector(*pos),p,None)
    unreal.log('FINAL_HORDE_ROUTE '+str(pos)+' '+str(bool(path and path.is_valid() and not path.is_partial())))
for name in ['AM_EnemyDeath_Entrega','AM_EnemyHit_Entrega']:
    a=unreal.load_asset('/Game/ThirdPerson/Blueprints/EnemigoIA/'+name)
    unreal.log('FINAL_HORDE_ANIMATION '+name+' '+str(a.get_play_length()))
