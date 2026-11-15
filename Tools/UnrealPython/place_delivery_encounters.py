"""Place the two finite encounters in Nivel_Entrega; never changes teammate maps."""
import unreal
ROOT='/Game/ThirdPerson/Blueprints/Entrega/'
AI='/Game/ThirdPerson/Blueprints/EnemigoIA/'
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Nivel_Entrega'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
assert 'Zona_01_Orbitadores' not in placed,'Encounters already placed; edit the existing instances.'
def nav(pos):
    goal=unreal.NavigationSystemV1.project_point_to_navigation(world,unreal.Vector(*pos),None,None,unreal.Vector(400,400,300))
    assert goal,'Spawn point is outside navigation: '+str(pos)
    return goal+unreal.Vector(0,0,100)
specs=[('Zona_01_Orbitadores',(0,-2700,150),(1300,1000,250),[(800,-3000,100),(-500,-3200,100)],(0,-3800,140),'Refugio_Rehen_01','BP_BaseEnemy'),
       ('Zona_02_Embestidores',(-3200,-4800,150),(1000,900,250),[(-3500,-5000,100),(-2700,-4900,100)],(-3200,-5500,140),'Refugio_Rehen_04','BP_ChargerEnemy')]
goals=[[nav(p) for p in s[3]] for s in specs]
for a in list(placed.values()):
    if a.get_actor_label().startswith('Enemigo_Entrega_'):actors.destroy_actor(a)
for i,(label,center,extent,points,gatepos,refuge,enemy) in enumerate(specs):
    zone=actors.spawn_actor_from_class(unreal.load_class(None,ROOT+'BP_CombatZone.BP_CombatZone_C'),unreal.Vector(*center))
    zone.set_actor_label(label);zone.set_folder_path('Combate/Oleadas')
    zone.get_component_by_class(unreal.BoxComponent).set_box_extent(unreal.Vector(*extent),False)
    zone.set_editor_property('EnemyClass',unreal.load_class(None,AI+enemy+'.'+enemy+'_C'))
    zone.set_editor_property('WaveCount',2)
    for j,p in enumerate(goals[i]):
        marker=actors.spawn_actor_from_class(unreal.TargetPoint,p)
        marker.set_actor_label('Spawn_Zona_%02d_%02d'%(i+1,j+1));marker.set_folder_path('Combate/Spawns')
        zone.set_editor_property('SpawnPoint'+str(j+1),marker)
        unreal.log('ENCOUNTER_SPAWN '+str(p))
    blocker=actors.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(*gatepos))
    blocker.set_actor_label('Barrera_Zona_%02d'%(i+1));blocker.set_folder_path('Combate/Barreras')
    component=blocker.static_mesh_component
    component.set_mobility(unreal.ComponentMobility.MOVABLE)
    component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'))
    component.set_material(0,unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/M_Baliza_Pendiente'))
    component.set_collision_profile_name('BlockAllDynamic')
    blocker.set_actor_scale3d(unreal.Vector(5,0.3,2.8))
    blocker.set_actor_enable_collision(False);blocker.set_actor_hidden_in_game(True)
    zone.set_editor_property('Blocker',blocker);zone.set_editor_property('RefugePoint',placed[refuge])
    placed['Director_Entrega'].set_editor_property('Zona'+str(i+1),zone)
mode=unreal.load_asset(ROOT+'BP_GameMode_Entrega')
unreal.get_default_object(mode.generated_class()).set_editor_property('default_pawn_class',unreal.load_class(None,ROOT+'BP_PlayerEntrega.BP_PlayerEntrega_C'))
unreal.EditorAssetLibrary.save_loaded_asset(mode,only_if_is_dirty=False)
# Distinct orange upper armor for the charger; keep the shared skeleton and locomotion.
charger=unreal.load_asset(AI+'BP_ChargerEnemy')
cdo=unreal.get_default_object(charger.generated_class())
cdo.mesh.set_material(0,unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/M_Baliza_Pendiente'))
unreal.EditorAssetLibrary.save_loaded_asset(charger,only_if_is_dirty=False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('DELIVERY_ENCOUNTERS_PLACED')
