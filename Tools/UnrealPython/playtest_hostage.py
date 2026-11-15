"""Editor-side: sample escort state. Optional action JSON affects PIE only.

hostage_action.json: {"player_offset":[0,-1200,0]}, {"threat":true},
{"clear_threat":true}, {"approach":true}, {"stop_tree":true}.
"""
import json
import os
import unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert world
hostage=unreal.GameplayStatics.get_actor_of_class(world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
assert hostage
player=unreal.GameplayStatics.get_player_pawn(world,0)
controller=hostage.get_controller()
bb=controller.get_component_by_class(unreal.BlackboardComponent)
brain=controller.get_component_by_class(unreal.BehaviorTreeComponent)
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
flag=os.path.join(project,'Intermediate','inspect','hostage_action.json')
action={}
if os.path.isfile(flag):
    with open(flag,encoding='utf-8-sig') as f:action=json.load(f)
    os.remove(flag)
if 'player_offset' in action:
    player.set_actor_location(hostage.get_actor_location()+unreal.Vector(*action['player_offset']),False,True)
if action.get('approach'):
    player.set_actor_location(hostage.get_actor_location()+unreal.Vector(0,200,10),False,True)
if action.get('threat'):
    enemy=unreal.GameplayStatics.get_all_actors_of_class(world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C'))[0]
    enemy.set_actor_location(hostage.get_actor_location()+unreal.Vector(600,0,10),False,True)
    enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Isolate escort test')
if action.get('clear_threat'):
    for enemy in unreal.GameplayStatics.get_all_actors_of_class(world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')):
        enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Isolate escort test')
        enemy.set_actor_location(unreal.Vector(4800,-12000,100),False,True)
if action.get('stop_tree'):brain.stop_logic('Verify decision tree owns movement')
keys={key:bb.get_value_as_bool(key) for key in ['bWaiting','bMustFlee','bAccompanying','bEnemyNear','bRescued']}
keys['Estado']=bb.get_value_as_int('Estado')
keys['DistanceToPlayer']=bb.get_value_as_float('DistanceToPlayer')
p=hostage.get_actor_location();flee=bb.get_value_as_vector('FleeLocation')
unreal.log('HOSTAGE_SAMPLE '+json.dumps({'t':unreal.GameplayStatics.get_time_seconds(world),'location':[p.x,p.y,p.z],
 'speed':hostage.get_velocity().length(),'player_distance':hostage.get_horizontal_distance_to(player),
 'move':str(controller.get_move_status()),'bt_running':brain.is_running() if brain else False,'keys':keys,
 'flee':[flee.x,flee.y,flee.z],'animation':hostage.mesh.get_anim_instance().get_class().get_name() if hostage.mesh.get_anim_instance() else None,
 'animation_speed':hostage.mesh.get_anim_instance().get_editor_property('speed') if hostage.mesh.get_anim_instance() else None}))
