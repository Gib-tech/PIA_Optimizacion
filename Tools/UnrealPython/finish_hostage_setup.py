"""Editor-side: finalize key bindings and place the escort plus reachable refuge markers."""
import os
import unreal
ROOT='/Game/ThirdPerson/Blueprints/Aliado'
tree=unreal.load_asset(ROOT+'/BT_Hostage')
# UE's tree editor clears an object MoveTo key pasted before the correct BB was assigned.
move=unreal.find_object(None,tree.get_path_name()+':Instance_7')
assert move, 'Follow MoveTo instance not found'
key=move.get_editor_property('BlackboardKey')
key.set_editor_property('SelectedKeyName','PlayerActor')
move.set_editor_property('BlackboardKey',key)
unreal.EditorAssetLibrary.save_loaded_asset(tree)
for name in ['BP_HostageController','BP_Hostage','BTTask_HostageArrive','BTService_HostageSense','ABP_Hostage']:
    bp=unreal.load_asset(ROOT+'/'+name)
    unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Nivel_Entrega'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
hostage=placed.get('Rehen_Entrega') or actors.spawn_actor_from_class(unreal.load_class(None,ROOT+'/BP_Hostage.BP_Hostage_C'),unreal.Vector(300,-800,110),unreal.Rotator(pitch=0,yaw=90,roll=0))
hostage.set_actor_label('Rehen_Entrega');hostage.set_folder_path('Aliado')
refuges=[(0,-600),(-2500,-1000),(2500,-1000),(-4500,-3000),(4500,-3000),
         (-4500,-5500),(4500,-5500),(0,-6500),(-4500,-8000),(4500,-8000),
         (-3000,-10000),(3000,-10000),(0,-11500)]
for i,(x,y) in enumerate(refuges,1):
    label='Refugio_Rehen_%02d'%i
    if label in placed:continue
    p=unreal.NavigationSystemV1.project_point_to_navigation(world,unreal.Vector(x,y,20),None,None,unreal.Vector(200,200,200))
    assert p,'No walkable refuge at '+str((x,y))
    actor=actors.spawn_actor_from_class(unreal.TargetPoint,p)
    actor.set_actor_label(label);actor.set_folder_path('Aliado/Refugios')
    actor.set_editor_property('tags',[unreal.Name('RefugioRehen')])
# Rotator positional arguments are roll/pitch/yaw. Use keywords for all project placement.
for a in actors.get_all_level_actors():
    label=a.get_actor_label()
    if isinstance(a,unreal.PlayerStart):a.set_actor_rotation(unreal.Rotator(pitch=0,yaw=-90,roll=0),False)
    if label.startswith('Rotulo_Baliza_'):a.set_actor_rotation(unreal.Rotator(pitch=0,yaw=90,roll=0),False)
    if label=='Luz_Sol':a.set_actor_rotation(unreal.Rotator(pitch=-55,yaw=-35,roll=0),False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.EditorLevelLibrary.set_level_viewport_camera_info(unreal.Vector(0,-100,300),unreal.Rotator(pitch=-15,yaw=-90,roll=0))
unreal.log('HOSTAGE_PLACED refuges=%d' % len(refuges))
