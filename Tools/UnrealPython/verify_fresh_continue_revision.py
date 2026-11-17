"""Lectura tras un viaje real de mundo con bandera de Continuar del menú."""
import unreal,os,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;R='/Game/ThirdPerson/Blueprints/Entrega/'
m=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'));assert m.get_editor_property('bInitialized') and m.get_editor_property('bHasCheckpoint')
data=gs.load_game_from_slot('TimeOut_Delivery_v1',0);p=m.get_editor_property('Hero');extra=m.get_editor_property('Extras');d=m.get_editor_property('Director')
checks=[]
for k in ['Botiquines','Cargas','Creditos','Recogido1','Recogido2','Recogido3','Recogido4']:assert extra.get_editor_property(k)==data.get_editor_property(k),k
assert p.get_editor_property('CamaraPrimera')==data.get_editor_property('FirstPerson')
assert p.get_editor_property('FPC').is_active()==data.get_editor_property('FirstPerson')
assert (p.get_actor_location()-data.get_editor_property('PlayerLocation')).length()<3
assert p.get_editor_property('BPC_Health').get_editor_property('Health')==data.get_editor_property('PlayerHealth')
for i in (1,2,3):
 z=d.get_editor_property('Zona'+str(i));assert z.get_editor_property('Phase')==data.get_editor_property('Zone'+str(i)+'Phase');assert not z.get_editor_property('EncounterEnemies')
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'));assert not cinema.get_editor_property('bActive') and not cinema.get_editor_property('bShouldIntro')
result={'passed':True,'method':'SaveCheckpoint, bandera real de Continuar y OpenLevel; lectura en mundo nuevo. Sin pulsación de mando físico.','inventory':{k:extra.get_editor_property(k) for k in ['Botiquines','Cargas','Creditos']},'first_person':p.get_editor_property('CamaraPrimera'),'position_restored':True,'three_zones_without_duplicate_enemies':True,'intro_omitted':True}
with open(os.path.join(unreal.Paths.project_dir(),'docs/validation/continuar-mundo-nuevo.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
unreal.log('FRESH_CONTINUE_REVISION_PASSED')
