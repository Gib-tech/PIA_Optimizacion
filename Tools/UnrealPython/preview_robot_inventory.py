"""Estado preparado para inspección visual; nunca se usa como partida natural."""
import unreal,os,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;pc=gs.get_player_controller(w,0);p=gs.get_player_character(w,0)
R='/Game/ThirdPerson/Blueprints/Entrega/'
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
lib=unreal.get_default_object(unreal.SystemLibrary)
def field(obj,k,v,kind):lib.call_method('Set'+kind+'PropertyByName',(obj,k,v))
for k,v in [('Botiquines',2),('Cargas',6),('Creditos',3)]:field(extra,k,v,'Int')
field(extra,'WorldSeconds',0.,'Double');field(extra,'InventoryOpen',True,'Bool')
p.set_actor_location(unreal.Vector(-140,-710,100),False,True);pc.set_control_rotation(unreal.Rotator(pitch=-8,yaw=-150));pc.set_view_target_with_blend(p,0)
unreal.log('PREVIEW_ROBOT '+json.dumps({'position':str(extra.get_editor_property('Tecnico').get_actor_location()),'mesh':[str(c.get_editor_property('static_mesh')) for c in extra.get_editor_property('Tecnico').get_components_by_class(unreal.StaticMeshComponent)]}))
unreal.SystemLibrary.execute_console_command(w,'stat none');unreal.SystemLibrary.execute_console_command(w,'t.MaxFPS 30')
