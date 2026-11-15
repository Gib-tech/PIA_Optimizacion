"""Editor-side test driver. Actions only affect the running PIE world.

Optional Intermediate/inspect/delivery_action.json: {"teleport":"Baliza_02"},
{"damage":100}, or {"camera":true}. Run without the file to sample only.
Input itself is tested with real E/R/Enter keys in the game viewport.
"""
import json
import os
import unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert world, 'Start PIE first'
player=unreal.GameplayStatics.get_player_pawn(world,0)
all_actors=unreal.GameplayStatics.get_all_actors_of_class(world,unreal.Actor)
director=next(a for a in all_actors if a.get_class().get_name()=='BP_DirectorEntrega_C')
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
action_file=os.path.join(project,'Intermediate','inspect','delivery_action.json')
action={}
if os.path.isfile(action_file):
    with open(action_file,encoding='utf-8-sig') as f:action=json.load(f)
    os.remove(action_file)
if action.get('teleport'):
    target=next(a for a in all_actors if a.get_actor_label()==action['teleport'])
    p=target.get_actor_location()
    player.set_actor_location(unreal.Vector(p.x,p.y+180,100),False,True)
    player.get_controller().set_control_rotation(unreal.Rotator(pitch=-15,yaw=-90,roll=0))
    unreal.log('TEST_TELEPORT '+target.get_actor_label())
if action.get('camera'):
    player.get_controller().set_control_rotation(unreal.Rotator(pitch=-15,yaw=-90,roll=0))
if action.get('escort_exit'):
    hostage=unreal.GameplayStatics.get_actor_of_class(world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
    hostage.set_actor_location(director.get_editor_property('Salida').get_actor_location()+unreal.Vector(200,180,100),False,True)
if action.get('damage'):
    unreal.GameplayStatics.apply_damage(player,float(action['damage']),None,None,None)
health=next(c for c in player.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_Health_C')
unreal.log('DELIVERY_SAMPLE t=%.2f step=%s paused=%s player=%s health=%s control=%s' % (
    unreal.GameplayStatics.get_time_seconds(world),director.get_editor_property('Paso'),unreal.GameplayStatics.is_game_paused(world),
    player.get_actor_location(),health.get_editor_property('Health'),player.get_controller().get_control_rotation()))
for key in ['Baliza1','Baliza2','Baliza3','Salida']:
    actor=director.get_editor_property(key)
    unreal.log('DELIVERY_TARGET %s=%s distance=%.1f material=%s' % (key,actor.get_actor_label(),actor.get_horizontal_distance_to(player),actor.static_mesh_component.get_material(0).get_name()))
for c in player.get_components_by_class(unreal.SpringArmComponent):
    unreal.log('CAMERA %s rotation=%s length=%s' % (c.get_name(),c.get_relative_transform().rotation.rotator(),c.target_arm_length))
