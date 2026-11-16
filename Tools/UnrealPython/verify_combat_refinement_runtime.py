"""Read-only combat/escort configuration check during an ordinary PIE mission."""
import unreal,json,os
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert world
player=unreal.GameplayStatics.get_player_character(world,0)
host=unreal.GameplayStatics.get_actor_of_class(world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
assert host in player.capsule_component.copy_array_of_move_ignore_actors()
assert player in host.capsule_component.copy_array_of_move_ignore_actors()
rows=[]
for name in ['BP_BaseEnemy','BP_ChargerEnemy']:
 cdo=unreal.get_default_object(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/'+name+'.'+name+'_C'))
 assert not cdo.is_actor_tick_enabled()
 assert abs(cdo.get_editor_property('ContactDamage')-13.2)<.001
 assert abs(cdo.character_movement.rotation_rate.yaw-360)<.001
 assert cdo.get_editor_property('NextAttackAt')==0
 rows.append({'enemy':name,'actor_tick_enabled':False,'contact_damage':13.2,'rotation_rate':360,'stagger_cooldown':cdo.get_editor_property('StaggerCooldown')})
hud=player.get_controller().get_hud()
for i in [1,2,3]:assert hud.get_editor_property('CachedBeacon'+str(i))
result={'passed':True,'read_only_in_normal_mission':True,'allied_move_ignores_bidirectional':True,'beacons_cached':3,'enemies':rows}
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/combat_refinement_runtime.json'),'w') as f:json.dump(result,f,indent=2)
unreal.log('COMBAT_REFINEMENT_RUNTIME_PASSED')
