"""Read-only checkpoint runtime sample, for PIE and post-load verification."""
import unreal
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert w, 'PIE is not running'
path='/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager.BP_DeliverySaveManager_C'
m=unreal.GameplayStatics.get_actor_of_class(w,unreal.load_class(None,path))
assert m
unreal.log('SAVE_SAMPLE ticking=%s tick=%s' % (m.is_actor_tick_enabled(), m.get_editor_property('primary_actor_tick')))
for name in ['bInitialized','bHasCheckpoint','bSaveSucceeded','StatusText','SaveData']:
    unreal.log('SAVE_SAMPLE %s=%s' % (name,m.get_editor_property(name)))
p=unreal.GameplayStatics.get_player_character(w,0)
unreal.log('SAVE_SAMPLE player=%s location=%s' % (p,p.get_actor_location()))
h=m.get_editor_property('Hostage');d=m.get_editor_property('Director')
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
unreal.log('SAVE_SAMPLE hostage_location=%s velocity=%s paso=%s' % (h.get_actor_location(),h.get_velocity(),d.get_editor_property('Paso')))
unreal.log('SAVE_SAMPLE escort='+str({key:bb.get_value_as_bool(key) for key in ['bRescued','bAccompanying','bWaiting','bMustFlee','bEnemyNear','bActivateBeacon']}))
unreal.log('SAVE_SAMPLE beacons='+str([(d.get_editor_property('Baliza'+str(i)).get_actor_location(),d.get_editor_property('Baliza'+str(i)).get_editor_property('bActivated')) for i in (1,2,3)]))
