"""Read-only assertions after a real menu Continue or defeat retry world load."""
import unreal, json, pathlib
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
R='/Game/ThirdPerson/Blueprints/Entrega/'
m=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,R+'BP_DeliverySaveManager.BP_DeliverySaveManager_C'))
assert m.get_editor_property('bInitialized') and m.get_editor_property('bHasCheckpoint')
data=unreal.GameplayStatics.load_game_from_slot('TimeOut_Delivery_v1',0)
prop=lambda o,k:o.get_editor_property(k)
p=prop(m,'Hero');h=prop(m,'Hostage');d=prop(m,'Director')
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
assert prop(prop(p,'BPC_Health'),'Health')==prop(data,'PlayerHealth')
assert prop(h,'Health')==prop(data,'HostageHealth') and prop(d,'Paso')==prop(data,'Paso')
assert prop(p,'bIsHammerEquipped')==prop(data,'HammerEquipped')
assert bb.get_value_as_bool('bRescued')==prop(data,'Rescued')
assert (p.get_actor_location()-prop(data,'PlayerLocation')).length()<2
for i in (1,2):
    z=prop(d,'Zona'+str(i));assert prop(z,'bCleared')==prop(data,'Zone%dCleared'%i)
    assert prop(z,'Phase')==prop(data,'Zone%dPhase'%i) and prop(z,'CurrentWave')==prop(data,'Zone%dWave'%i)
    assert not prop(z,'EncounterEnemies'),'Checkpoint spawned duplicate enemies'
for i in (1,2,3):
    b=prop(d,'Baliza'+str(i));door=prop(b,'Door')
    assert prop(b,'bActivated')==prop(data,'Beacon%dActivated'%i)
    assert prop(door,'bDestroyed')==prop(data,'Door%dDestroyed'%i)
    assert prop(door,'Health')==prop(data,'Door%dHealth'%i)
    assert door.get_actor_enable_collision()!=prop(data,'Door%dDestroyed'%i)
result={'passed':True,'agent_tests_not_owner_acceptance':True,'restored_step':prop(d,'Paso'),'player_health':prop(data,'PlayerHealth'),'hostage_health':prop(data,'HostageHealth'),'fresh_world_restore':True,'no_duplicate_enemies':True,'doors_collision_restored':True}
target=pathlib.Path(unreal.Paths.project_dir())/'Intermediate/inspect/delivery_continue_assertions.json'
target.write_text(json.dumps(result,indent=2),encoding='utf-8')
unreal.log('SAVE_CONTINUE_REGRESSION '+json.dumps(result))
