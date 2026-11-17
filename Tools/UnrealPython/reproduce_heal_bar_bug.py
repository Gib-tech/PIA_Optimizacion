"""Reproducción anterior a la corrección: vida interna frente a barra visible."""
import unreal,os,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller();R='/Game/ThirdPerson/Blueprints/Entrega/'
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'));health=p.get_editor_property('BPC_Health');bar=p.get_editor_property('Health_Widget').get_editor_property('HealthBar')
unreal.get_default_object(unreal.SystemLibrary).call_method('SetIntPropertyByName',(extra,'Botiquines',2))
health.call_method('Increase_Health',(100.,));gs.apply_damage(p,40,pc,None,None)
before={'health':health.get_editor_property('Health'),'bar':bar.get_editor_property('percent'),'kits':extra.get_editor_property('Botiquines')}
extra.call_method('UsarBotiquin')
after={'health':health.get_editor_property('Health'),'bar':bar.get_editor_property('percent'),'kits':extra.get_editor_property('Botiquines')}
result={'damage_event':40,'before':before,'after':after,'ui_mismatch_reproduced':abs(after['bar']-after['health']/100)>.001}
folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/items-colisiones');os.makedirs(folder,exist_ok=True)
with open(os.path.join(folder,'reproduccion-curacion.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
unreal.log('HEAL_BAR_REPRO '+str(result))
