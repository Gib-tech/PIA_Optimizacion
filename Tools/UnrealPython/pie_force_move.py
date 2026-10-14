# Editor-side, during PIE. Orders the first enemy to walk 600 units on +X, bypassing the
# Behavior Tree. If the enemy walks, the pawn, controller, and navmesh are fine and any
# "does not move" bug is inside the tree or its tasks.
import unreal

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
enemies = unreal.GameplayStatics.get_all_actors_of_class(
    world, unreal.load_class(None, "/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C"))
e = enemies[0]
ctrl = e.get_controller()
goal = e.get_actor_location() + unreal.Vector(600, 0, 0)
result = ctrl.move_to_location(goal, 50.0, True, True, True, False, None, True)
unreal.log("FORCE result=%s status=%s from=%s goal=%s" % (result, ctrl.get_move_status(), e.get_actor_location(), goal))
