"""Editor-side: create the hostage's own character/controller/tree/task/service assets."""
import unreal
ROOT='/Game/ThirdPerson/Blueprints/Aliado'
tools=unreal.AssetToolsHelpers.get_asset_tools()
lib=unreal.BlueprintEditorLibrary
assert not unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/BP_Hostage')
bb=unreal.load_asset(ROOT+'/BB_Hostage') if unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/BB_Hostage') else tools.create_asset('BB_Hostage',ROOT,unreal.BlackboardData,unreal.BlackboardDataFactory())
keys=[]
for name,kind in [('PlayerActor','Object'),('DistanceToPlayer','Float'),
                 ('bEnemyNear','Bool'),('bMustFlee','Bool'),
                 ('bWaiting','Bool'),('bAccompanying','Bool'),
                 ('bRescued','Bool'),('FleeLocation','Vector')]:
    entry=unreal.BlackboardEntry()
    entry.set_editor_property('entry_name',name)
    entry.set_editor_property('key_type',unreal.new_object(unreal.load_class(None,'/Script/AIModule.BlackboardKeyType_'+kind),outer=bb))
    if kind=='Object':entry.get_editor_property('key_type').set_editor_property('BaseClass',unreal.Actor)
    keys.append(entry)
bb.set_editor_property('keys',keys)
unreal.EditorAssetLibrary.save_loaded_asset(bb)
tree=unreal.load_asset(ROOT+'/BT_Hostage') if unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/BT_Hostage') else tools.create_asset('BT_Hostage',ROOT,unreal.BehaviorTree,unreal.BehaviorTreeFactory())
unreal.EditorAssetLibrary.save_loaded_asset(tree)
for name,parent in [('BP_HostageController',unreal.AIController),('BP_Hostage',unreal.Character),
                    ('BTService_HostageSense',unreal.BTService_BlueprintBase),('BTTask_HostageArrive',unreal.BTTask_BlueprintBase)]:
    bp=lib.create_blueprint_asset_with_parent(ROOT+'/'+name,parent)
    lib.remove_unused_nodes(bp)
    if name=='BTService_HostageSense':
        for variable in ['ThreatActor','Candidate','SafeCandidate']:
            lib.add_member_variable(bp,variable,lib.get_object_reference_type(unreal.Actor))
        for variable in ['BestDistance','MinEnemyDistance','ThreatRadius','SafeEnemyDistance','SafePlayerDistance']:
            lib.add_member_variable(bp,variable,lib.get_basic_type_by_name('real'))
        for variable in ['ThreatRadius','SafeEnemyDistance','SafePlayerDistance']:
            lib.set_blueprint_variable_instance_editable(bp,variable,True)
    lib.compile_blueprint(bp)
    cdo=unreal.get_default_object(bp.generated_class())
    if name=='BP_Hostage':
        cdo.set_editor_property('ai_controller_class',unreal.load_class(None,ROOT+'/BP_HostageController.BP_HostageController_C'))
        cdo.set_editor_property('auto_possess_ai',unreal.AutoPossessAI.PLACED_IN_WORLD_OR_SPAWNED)
        cdo.set_editor_property('auto_receive_input',unreal.AutoReceiveInput.DISABLED)
        cdo.set_editor_property('use_controller_rotation_yaw',False)
        cdo.character_movement.set_editor_property('orient_rotation_to_movement',True)
        cdo.character_movement.set_editor_property('max_walk_speed',400.0)
        cdo.mesh.set_skeletal_mesh_asset(unreal.load_asset('/Game/Characters/Mannequins/Meshes/SKM_Manny'))
        cdo.mesh.set_anim_instance_class(unreal.load_class(None,ROOT+'/ABP_Aliado.ABP_Aliado_C'))
        cdo.mesh.set_editor_property('relative_location',unreal.Vector(0,0,-88))
        cdo.mesh.set_editor_property('relative_rotation',unreal.Rotator(pitch=0,yaw=-90,roll=0))
    elif name=='BTService_HostageSense':
        cdo.set_editor_property('ThreatRadius',800.0)
        cdo.set_editor_property('SafeEnemyDistance',1200.0)
        cdo.set_editor_property('SafePlayerDistance',1000.0)
        cdo.set_editor_property('interval',0.5)
        cdo.set_editor_property('random_deviation',0.0)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
unreal.log('HOSTAGE_ASSETS_CREATED')
