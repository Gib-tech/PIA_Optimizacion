"""Isolated PIE regression of checkpoint data and safe-save guards, not FIN-01 acceptance."""
import unreal, json, os, traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert w
R='/Game/ThirdPerson/Blueprints/Entrega/'
m=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
assert m.get_editor_property('bHasCheckpoint')
p=m.get_editor_property('Hero');h=m.get_editor_property('Hostage');d=m.get_editor_property('Director')
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
z=[d.get_editor_property('Zona'+str(i)) for i in (1,2)]
b=[d.get_editor_property('Baliza'+str(i)) for i in (1,2,3)]
doors=[a.get_editor_property('Door') for a in b]
health=p.get_editor_property('BPC_Health')
system=unreal.get_default_object(unreal.SystemLibrary.static_class())
def put(obj,name,value):
    kind='Bool' if isinstance(value,bool) else 'Int' if isinstance(value,int) else 'Double'
    system.call_method('Set'+kind+'PropertyByName',(obj,name,value))
def prop(obj,name):return obj.get_editor_property(name)
def saved():return unreal.GameplayStatics.load_game_from_slot('TimeOut_Delivery_v1',0)
result={'agent_tests_not_owner_acceptance':True,'isolated_state_setup':True}
try:
    assert prop(saved(),'Version')==1
    result['initial_autosave']=True
    put(health,'Health',73.0);put(h,'Health',61.0)
    p.set_actor_location(unreal.Vector(100,-620,91.15),False,True)
    h.set_actor_location(unreal.Vector(220,-650,96),False,True)
    bb.set_value_as_bool('bRescued',True);bb.set_value_as_bool('bAccompanying',False);bb.set_value_as_bool('bWaiting',True)
    for name in ('bMustFlee','bEnemyNear'):bb.set_value_as_bool(name,False)
    put(z[0],'Phase',3);put(z[0],'bCleared',True);put(z[0],'CurrentWave',2);put(z[0],'SpawnedCount',4)
    put(d,'Paso',1);put(b[0],'bActivated',True)
    put(doors[0],'bUnlocked',True);put(doors[0],'Health',25.0);put(doors[0],'bCracked',True)
    p.call_method('GrantHammerUpgrade',(doors[0],))
    m.call_method('SaveCheckpoint')
    assert prop(m,'bSaveSucceeded')
    data=saved()
    assert prop(data,'PlayerHealth')==73 and prop(data,'HostageHealth')==61
    assert prop(data,'Paso')==1 and prop(data,'Zone1Cleared') and prop(data,'Zone1Wave')==2
    assert prop(data,'Door1Health')==25 and prop(data,'Door1Cracked')
    assert prop(data,'HammerEquipped') and prop(data,'Rescued') and prop(data,'Waiting')
    result['snapshot_health_progress_escort_weapon_cracks']=True
    for phase in (1,2):
        put(z[1],'Phase',phase);put(health,'Health',40.0)
        m.call_method('SaveCheckpoint')
        assert prop(saved(),'PlayerHealth')==73,'Combat or intermission overwrote checkpoint'
    put(z[1],'Phase',0)
    for actor,key in [(h,'bUsingBeacon'),(p,'IsAttacking')]:
        put(actor,key,True);m.call_method('SaveCheckpoint')
        assert prop(saved(),'PlayerHealth')==73
        put(actor,key,False)
    put(health,'Health',0.0);m.call_method('SaveCheckpoint');assert prop(saved(),'PlayerHealth')==73
    result['combat_intermission_channel_attack_death_guards']=True
    put(health,'Health',100.0);put(h,'Health',100.0);put(d,'Paso',0)
    put(z[0],'Phase',0);put(z[0],'bCleared',False);put(b[0],'bActivated',False)
    put(doors[0],'Health',50.0);put(doors[0],'bUnlocked',False);put(doors[0],'bCracked',False)
    bb.set_value_as_bool('bRescued',False);bb.set_value_as_bool('bAccompanying',True)
    m.call_method('RestoreCheckpoint')
    assert prop(health,'Health')==73 and prop(h,'Health')==61 and prop(d,'Paso')==1
    assert prop(z[0],'bCleared') and prop(z[0],'Phase')==3 and prop(z[0],'CurrentWave')==2
    assert prop(doors[0],'Health')==25 and prop(doors[0],'bUnlocked') and prop(doors[0],'bCracked')
    assert doors[0].static_mesh_component.static_mesh==prop(doors[0],'CrackedMesh')
    assert bb.get_value_as_bool('bRescued') and bb.get_value_as_bool('bWaiting') and not bb.get_value_as_bool('bAccompanying')
    assert (p.get_actor_location()-prop(data,'PlayerLocation')).length()<1
    assert (h.get_actor_location()-prop(data,'HostageLocation')).length()<1
    assert prop(p,'bIsHammerEquipped') and prop(p,'bDoorPending')
    result['restore_live_state_and_cracked_mesh']=True
    put(doors[0],'bDestroyed',True);put(doors[0],'Health',0.0);m.call_method('SaveCheckpoint')
    put(doors[0],'bDestroyed',False);doors[0].set_actor_hidden_in_game(False);doors[0].set_actor_enable_collision(True)
    m.call_method('RestoreCheckpoint')
    assert prop(doors[0],'bDestroyed') and not doors[0].get_actor_enable_collision()
    assert not prop(p,'bDoorPending')
    result['destroyed_door_stays_open']=True
    result['passed']=True
except Exception:
    result['passed']=False;result['error']=traceback.format_exc()
finally:
    target=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/delivery_save_assertions.json')
    with open(target,'w',encoding='utf-8') as handle:json.dump(result,handle,ensure_ascii=False,indent=2)
    unreal.log('SAVE_REGRESSION '+json.dumps(result,ensure_ascii=False))
assert result['passed'],result.get('error')
