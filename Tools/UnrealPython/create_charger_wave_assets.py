"""Create Blueprint shells for the charger, encounter waves and isolated heavy-hit integration."""
import os
import unreal
ROOT='/Game/ThirdPerson/Blueprints/EnemigoIA'
DELIVERY='/Game/ThirdPerson/Blueprints/Entrega'
assert not unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/BP_ChargerEnemy'),'Initial creation recipe only; do not overwrite completed combat assets.'
lib=unreal.BlueprintEditorLibrary
tools=unreal.AssetToolsHelpers.get_asset_tools()
base=unreal.load_class(None,ROOT+'/BP_BaseEnemy.BP_BaseEnemy_C')
player=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C')
bb=unreal.load_asset(ROOT+'/BB_Charger') or tools.create_asset('BB_Charger',ROOT,unreal.BlackboardData,unreal.BlackboardDataFactory())
entries=[]
for name,kind in [('TargetActor','Object'),('DistanceToTarget','Float'),('ChargeGoal','Vector'),('bCharging','Bool'),('bRetreat','Bool'),('bReceivingDamage','Bool')]:
    entry=unreal.BlackboardEntry();entry.set_editor_property('entry_name',name)
    key=unreal.new_object(unreal.load_class(None,'/Script/AIModule.BlackboardKeyType_'+kind),outer=bb)
    if kind=='Object':key.set_editor_property('BaseClass',unreal.Actor)
    entry.set_editor_property('key_type',key);entries.append(entry)
bb.set_editor_property('keys',entries);unreal.EditorAssetLibrary.save_loaded_asset(bb,only_if_is_dirty=False)
tree=unreal.load_asset(ROOT+'/BT_Charger') or tools.create_asset('BT_Charger',ROOT,unreal.BehaviorTree,unreal.BehaviorTreeFactory())
unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetObjectPropertyByName',(tree,'BlackboardAsset',bb))
unreal.EditorAssetLibrary.save_loaded_asset(tree,only_if_is_dirty=False)
specs={
 'BP_ChargerEnemy':(ROOT,base,[]),
 'BP_ChargerController':(ROOT,unreal.AIController,[]),
 'BTService_ChargerSense':(ROOT,unreal.BTService_BlueprintBase,[]),
 'BTTask_ChargerWindup':(ROOT,unreal.BTTask_BlueprintBase,[('Elapsed','real')]),
 'BTTask_ChargerCharge':(ROOT,unreal.BTTask_BlueprintBase,[('Elapsed','real'),('bHit','bool')]),
 'BTTask_ChargerRetreat':(ROOT,unreal.BTTask_BlueprintBase,[('Elapsed','real'),('BestDistance','real'),('Candidate','actor'),('SafeCandidate','actor')]),
 'BTTask_ChargerRecover':(ROOT,unreal.BTTask_BlueprintBase,[]),
 'BP_PlayerEntrega':(DELIVERY,player,[('HeavyHitActors','array_actor'),('HeavyDamage','real')]),
 'BP_CombatZone':(DELIVERY,unreal.TriggerBox,[('EnemyClass','enemy_class'),('SpawnPoint1','actor'),('SpawnPoint2','actor'),('Blocker','actor'),('RefugePoint','actor'),('EncounterEnemies','array_actor'),('CurrentWave','int'),('WaveCount','int'),('Phase','int'),('LivingCount','int'),('SpawnedCount','int'),('NextWaveAt','real'),('bCleared','bool')])}
for name,(folder,parent,variables) in specs.items():
    if unreal.EditorAssetLibrary.does_asset_exist(folder+'/'+name):bp=unreal.load_asset(folder+'/'+name)
    else:
        factory=unreal.BlueprintFactory();factory.set_editor_property('parent_class',parent)
        bp=tools.create_asset(name,folder,unreal.Blueprint,factory)
    assert bp,name
    for variable,kind in variables:
        if kind in ('actor','array_actor'):typ=lib.get_object_reference_type(unreal.Actor)
        elif kind=='enemy_class':typ=lib.get_class_reference_type(base)
        else:typ=lib.get_basic_type_by_name(kind)
        if kind=='array_actor':typ=lib.get_array_type(typ)
        lib.add_member_variable(bp,variable,typ)
        if variable in ('EnemyClass','SpawnPoint1','SpawnPoint2','Blocker','RefugePoint','WaveCount','HeavyDamage'):
            lib.set_blueprint_variable_instance_editable(bp,variable,True)
    lib.compile_blueprint(bp)
    cdo=unreal.get_default_object(bp.generated_class())
    if name=='BP_CombatZone':
        cdo.set_editor_property('WaveCount',2)
        cdo.set_editor_property('EnemyClass',base)
        cdo.get_component_by_class(unreal.BoxComponent).set_box_extent(unreal.Vector(1200,1000,250),False)
        tick=cdo.get_editor_property('primary_actor_tick');tick.set_editor_property('tick_interval',0.2);cdo.set_editor_property('primary_actor_tick',tick)
    if name=='BP_PlayerEntrega':cdo.set_editor_property('HeavyDamage',25.0)
    if name=='BTService_ChargerSense':
        cdo.set_editor_property('interval',0.2);cdo.set_editor_property('random_deviation',0.0)
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
basebp=unreal.load_asset(ROOT+'/BP_BaseEnemy')
for variable,kind in [('bAttackInProgress','bool'),('AttackVictim','actor')]:
    typ=lib.get_object_reference_type(unreal.Actor) if kind=='actor' else lib.get_basic_type_by_name(kind)
    lib.add_member_variable(basebp,variable,typ)
lib.compile_blueprint(basebp)
# Own montages keep the team's source animation assets intact.
for name,source in [('AM_EnemyAttack_Entrega','ataque_enemigo'),('AM_EnemyHit_Entrega','enemigo_lastimado1'),('AM_EnemyDeath_Entrega','Enemy_Death')]:
    anim=unreal.load_asset(ROOT+'/'+source)
    factory=unreal.AnimMontageFactory();factory.set_editor_property('target_skeleton',anim.get_editor_property('skeleton'));factory.set_editor_property('source_animation',anim)
    montage=tools.create_asset(name,ROOT,unreal.AnimMontage,factory)
    if 'Death' in name:montage.set_editor_property('enable_auto_blend_out',False)
    unreal.EditorAssetLibrary.save_loaded_asset(montage,only_if_is_dirty=False)
anim=unreal.EditorAssetLibrary.duplicate_asset('/Game/SciFITrooper_Man_03/Blueprints/AnimBP/ABP_SciFiTrooperManV3',ROOT+'/ABP_EnemyEntrega')
assert anim
unreal.BlueprintEditorLibrary.compile_blueprint(anim)
unreal.EditorAssetLibrary.save_loaded_asset(anim,only_if_is_dirty=False)
cdo=unreal.get_default_object(basebp.generated_class())
cdo.mesh.set_skeletal_mesh_asset(unreal.load_asset('/Game/SciFiWarrior02/Meshes/SK_SciFiWarrior02'))
cdo.mesh.set_anim_instance_class(anim.generated_class())
cdo.mesh.set_editor_property('relative_location',unreal.Vector(0,0,-88))
cdo.mesh.set_editor_property('relative_rotation',unreal.Rotator(pitch=0,yaw=-90,roll=0))
cdo.set_editor_property('auto_possess_ai',unreal.AutoPossessAI.PLACED_IN_WORLD_OR_SPAWNED)
unreal.EditorAssetLibrary.save_loaded_asset(basebp,only_if_is_dirty=False)
unreal.log('CHARGER_WAVE_SHELLS_CREATED')
