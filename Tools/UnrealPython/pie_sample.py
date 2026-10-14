# Editor-side, during PIE. Logs player and enemy positions, speed, path-following status,
# Behavior Tree running state, Blackboard values, and which Blueprint BT task is executing.
#
# Teleport: create the empty file Intermediate/inspect/teleport.flag before running this
# script. The player is then moved 450 units (+Y) from the first enemy, once.
#
# Change ENEMY_CLASS / BB_KEYS when sampling the hostage or the charger.
import os
import unreal

ENEMY_CLASS = "/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C"
BB_KEYS = {"float": ["DistanceToTarget", "DetectionRadius"], "object": ["TargetActor"],
           "bool": ["bReceivingDamage"], "vector": ["OrbitLocation"]}
BP_TASKS = ["BTTask_Roam_C", "BTTask_Attack_C", "BTTask_Defend_C", "BTTask_HitSun_C"]

project = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
flag = os.path.join(project, "Intermediate", "inspect", "teleport.flag")

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
if not world:
    unreal.log("SAMPLE no game world (PIE not running)")
else:
    player = unreal.GameplayStatics.get_player_pawn(world, 0)
    enemies = unreal.GameplayStatics.get_all_actors_of_class(world, unreal.load_class(None, ENEMY_CLASS))
    if os.path.exists(flag) and player and enemies:
        os.remove(flag)
        target = enemies[0].get_actor_location() + unreal.Vector(0, 450, 0)
        player.set_actor_location(target, False, True)
        unreal.log("SAMPLE teleported player to %s" % target)
    ploc = player.get_actor_location() if player else None
    unreal.log("SAMPLE t=%.2f player=%s" % (unreal.GameplayStatics.get_time_seconds(world), ploc))
    for e in enemies:
        loc = e.get_actor_location()
        ctrl = e.get_controller()
        line = "SAMPLE  %s loc=(%.0f,%.0f,%.0f) speed=%.0f" % (e.get_name()[-10:], loc.x, loc.y, loc.z,
                                                              e.get_velocity().length())
        if ploc:
            line += " distToPlayer=%.0f" % (loc - ploc).length()
        if ctrl:
            line += " move=%s" % ctrl.get_move_status()
            brain = ctrl.get_component_by_class(unreal.BehaviorTreeComponent)
            if brain:
                line += " bt_running=%s" % brain.is_running()
                executing = []
                for cls in BP_TASKS:
                    for i in range(4):
                        obj = unreal.find_object(None, "%s.%s_%d" % (brain.get_path_name(), cls, i))
                        if obj is not None and obj.is_task_executing():
                            executing.append(cls)
                line += " bp_task_executing=%s" % (executing or "none (native node or between tasks)")
            bb = ctrl.get_component_by_class(unreal.BlackboardComponent)
            if bb:
                vals = []
                for k in BB_KEYS["float"]:
                    vals.append("%s=%.0f" % (k, bb.get_value_as_float(k)))
                for k in BB_KEYS["object"]:
                    o = bb.get_value_as_object(k)
                    vals.append("%s=%s" % (k, o.get_name() if o else None))
                for k in BB_KEYS["bool"]:
                    vals.append("%s=%s" % (k, bb.get_value_as_bool(k)))
                for k in BB_KEYS["vector"]:
                    v = bb.get_value_as_vector(k)
                    vals.append("%s=(%.0f,%.0f)" % (k, v.x, v.y) if abs(v.x) < 1e30 else "%s=unset" % k)
                line += " | " + " ".join(vals)
        unreal.log(line)
