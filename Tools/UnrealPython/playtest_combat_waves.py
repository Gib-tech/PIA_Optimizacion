"""PIE-only diagnostic driver. Reads a one-shot combat_action.json, never saves PIE actors."""
import json,os,unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert world,'Start PIE first'
player=unreal.GameplayStatics.get_player_pawn(world,0)
base=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
zones=unreal.GameplayStatics.get_all_actors_of_class(world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C'))
hostage=unreal.GameplayStatics.get_actor_of_class(world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
bb=hostage.get_controller().get_component_by_class(unreal.BlackboardComponent)
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
flag=os.path.join(root,'Intermediate/inspect/combat_action.json')
action={}
if os.path.isfile(flag):
    with open(flag,encoding='utf-8-sig') as f:action=json.load(f)
    os.remove(flag)
if action.get('zone'):
    zone=sorted(zones,key=lambda a:a.get_actor_label())[action['zone']-1]
    center=zone.get_actor_location()
    player.set_actor_location(unreal.Vector(center.x,center.y+700,100),False,True)
    if action.get('escort'):
        hostage.set_actor_location(player.get_actor_location()+unreal.Vector(150,200,0),False,True)
        bb.set_value_as_bool('bMustFlee',False);bb.set_value_as_bool('bWaiting',False)
        bb.set_value_as_bool('bRescued',True);bb.set_value_as_bool('bAccompanying',True);bb.set_value_as_int('Estado',1)
if action.get('kill_wave'):
    for enemy in unreal.GameplayStatics.get_all_actors_of_class(world,base):
        if not enemy.get_editor_property('bIsDead'):
            health=next(c for c in enemy.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_E_Health_C')
            health.call_method('E_Decrease_Health',(100.0,))
if action.get('spawn'):
    cls=base if action['spawn']=='orbiter' else unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_ChargerEnemy.BP_ChargerEnemy_C')
    transform=unreal.Transform(location=player.get_actor_location()+unreal.Vector(600,0,30))
    statics=unreal.get_default_object(unreal.GameplayStatics.static_class())
    enemy=statics.call_method('BeginDeferredActorSpawnFromClass',(world,cls,transform,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
    statics.call_method('FinishSpawningActor',(enemy,transform,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
    unreal.log('TEST_SPAWN '+enemy.get_path_name())
if action.get('heal'):
    health=next(c for c in player.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_Health_C')
    unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetDoublePropertyByName',(health,'Health',100.0))
    unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetBoolPropertyByName',(player,'bCanBeDamaged',False))
report={'time':unreal.GameplayStatics.get_time_seconds(world),'player_class':player.get_class().get_name(),'player_pos':str(player.get_actor_location()),'escort':{k:bb.get_value_as_bool(k) for k in ['bAccompanying','bMustFlee','bWaiting']},'zones':[],'enemies':[]}
for zone in sorted(zones,key=lambda a:a.get_actor_label()):
    values={k:zone.get_editor_property(k) for k in ['Phase','CurrentWave','LivingCount','SpawnedCount','bCleared']}
    values.update(label=zone.get_actor_label(),gate=zone.get_editor_property('Blocker').get_actor_enable_collision(),array_count=len(zone.get_editor_property('EncounterEnemies')))
    report['zones'].append(values)
for enemy in unreal.GameplayStatics.get_all_actors_of_class(world,base):
    ctl=enemy.get_controller();board=ctl.get_component_by_class(unreal.BlackboardComponent) if ctl else None
    brain=ctl.get_component_by_class(unreal.BehaviorTreeComponent) if ctl else None
    health=next(c for c in enemy.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_E_Health_C')
    report['enemies'].append({'name':enemy.get_name(),'class':enemy.get_class().get_name(),'health':health.get_editor_property('E_Health'),'dead':enemy.get_editor_property('bIsDead'),'speed':enemy.get_velocity().length(),'pos':str(enemy.get_actor_location()),'distance':enemy.get_distance_to(player),'controller':ctl.get_class().get_name() if ctl else None,'tree':brain.is_running() if brain else False,'charging':board.get_value_as_bool('bCharging') if board and enemy.get_class().get_name()=='BP_ChargerEnemy_C' else None,'retreat':board.get_value_as_bool('bRetreat') if board and enemy.get_class().get_name()=='BP_ChargerEnemy_C' else None,'animation':enemy.mesh.get_anim_instance().get_class().get_name() if enemy.mesh.get_anim_instance() else None})
unreal.log('COMBAT_WAVE_SAMPLE '+json.dumps(report))
with open(os.path.join(root,'Intermediate/inspect/combat_samples.jsonl'),'a',encoding='utf8') as f:f.write(json.dumps(report)+'\n')
