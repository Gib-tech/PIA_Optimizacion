"""Crea checkpoint nocturno de QA en el inicio, para Continuar en el ejecutable aislado."""
import unreal,os,json,shutil
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;R='/Game/ThirdPerson/Blueprints/Entrega/'
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'));manager=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
p=gs.get_player_character(w,0);p.set_actor_location(unreal.Vector(520,-1120,95),False,True);p.set_actor_rotation(unreal.Rotator(yaw=90),False);p.get_controller().set_control_rotation(unreal.Rotator(pitch=-20,yaw=90))
lib=unreal.get_default_object(unreal.SystemLibrary);lib.call_method('SetBoolPropertyByName',(p,'CamaraPrimera',True));p.get_editor_property('TPC').deactivate();p.get_editor_property('FPC').activate();lib.call_method('SetIntPropertyByName',(extra,'Cargas',3))
unreal.get_default_object(unreal.SystemLibrary).call_method('SetDoublePropertyByName',(extra,'WorldSeconds',783.))
manager.call_method('SaveCheckpoint');assert manager.get_editor_property('bSaveSucceeded')
data=gs.load_game_from_slot('TimeOut_Delivery_v1',0);assert data.get_editor_property('Paso')==0 and data.get_editor_property('WorldSeconds')==783.
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());target=os.path.join(root,'Intermediate/inspect/daynight-attacks/native-user/Saved/SaveGames');os.makedirs(target,exist_ok=True)
shutil.copy2(os.path.join(root,'Saved/SaveGames/TimeOut_Delivery_v1.sav'),os.path.join(target,'TimeOut_Delivery_v1.sav'))
with open(os.path.join(root,'docs/validation/ciclo-luces-ataques/fixture-paquete.json'),'w',encoding='utf-8') as f:json.dump({'prepared_for_qa':True,'world_seconds':783.,'checkpoint_step':0,'position_cm':[520,-1120,95],'first_person':True,'pulse_charges':3,'method':'Checkpoint seguro de PIE junto a caja del inicio. Hora, posición, cámara y cargas preparadas para teclas reales del ejecutable; no es partida natural. Datos del usuario respaldados por separado.'},f,ensure_ascii=False,indent=2)
unreal.log('DAYNIGHT_NATIVE_CHECKPOINT_READY')
