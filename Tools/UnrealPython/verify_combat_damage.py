"""PIE integration assertions for both bound hit handlers and the shared health component."""
import unreal,json,os
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert world
player=unreal.GameplayStatics.get_player_pawn(world,0)
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
root='/Game/ThirdPerson/Blueprints/EnemigoIA/'
def spawn(name,dx):
    cls=unreal.load_class(None,root+name+'.'+name+'_C')
    transform=unreal.Transform(location=player.get_actor_location()+unreal.Vector(dx,0,10))
    statics=unreal.get_default_object(unreal.GameplayStatics.static_class())
    actor=statics.call_method('BeginDeferredActorSpawnFromClass',(world,cls,transform,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
    statics.call_method('FinishSpawningActor',(actor,transform,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
    actor.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Isolate damage assertions')
    return actor
orbiter=spawn('BP_BaseEnemy',-400);charger=spawn('BP_ChargerEnemy',400)
def hp(actor):
    component=next(c for c in actor.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_E_Health_C')
    return component.get_editor_property('E_Health')
hitbox=player.get_editor_property('WeaponHitbox')
parent='BndEvt__BP_ThirdPersonCharacter_WeaponHitbox_K2Node_ComponentBoundEvent_1_ComponentBeginOverlapSignature__DelegateSignature'
child='BndEvt__BP_PlayerEntrega_HeavyOverlap__DelegateSignature'
def hit(name,actor):player.call_method(name,(hitbox,actor,actor.capsule_component,0,False,unreal.HitResult()))
def flag(key,value):lib.call_method('SetBoolPropertyByName',(player,key,value))
flag('IsAttacking',True);flag('bLightAttackActive',True)
lib.call_method('SetIntPropertyByName',(player,'LightSwingIndex',0))
for actor in [orbiter,charger]:
    hit(parent,actor);hit(child,actor);assert hp(actor)==85.0,(actor.get_name(),hp(actor))
for index,remaining in [(1,70.0),(2,51.0)]:
    lib.call_method('SetIntPropertyByName',(player,'LightSwingIndex',index))
    for actor in [orbiter,charger]:
        hit(parent,actor);hit(child,actor);assert hp(actor)==remaining,(actor.get_name(),hp(actor))
flag('bLightAttackActive',False)
hit(child,charger);assert hp(charger)==26.0,hp(charger)
hit(child,charger);hit(parent,charger);assert hp(charger)==26.0,hp(charger)
hit(parent,orbiter);hit(child,orbiter);assert hp(orbiter)==51.0,hp(orbiter)
flag('IsAttacking',False);hit(child,charger);assert hp(charger)==26.0,hp(charger)
assert charger.get_controller().get_component_by_class(unreal.BlackboardComponent).get_value_as_bool('bReceivingDamage')
report={'passed':True,'light_combo_both':[15,15,19],'heavy_charger':25,'heavy_orbiter':0,'repeat_heavy_overlap':0,'inactive_heavy_overlap':0,'charger_mesh':charger.mesh.get_skeletal_mesh_asset().get_name(),'charger_anim':charger.mesh.get_anim_instance().get_class().get_name()}
assert report['charger_anim']=='ABP_EnemyEntrega_C',report
for actor in [orbiter,charger]:
    assert actor.mesh.get_skeletal_mesh_asset().get_name()=='SK_SciFiWarrior02'
    assert actor.mesh.get_editor_property('relative_scale3d').distance(unreal.Vector(1,1,1))<.001
    assert not actor.mesh.get_editor_property('override_materials')
    assert actor.get_editor_property('ContactDamage')==6
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
with open(os.path.join(project,'Intermediate/inspect/damage_assertions.json'),'w') as f:json.dump(report,f,indent=2)
orbiter.destroy_actor();charger.destroy_actor()
unreal.log('COMBAT_DAMAGE_ASSERTIONS_PASSED '+json.dumps(report))
