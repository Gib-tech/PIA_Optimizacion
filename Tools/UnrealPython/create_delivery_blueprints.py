"""Editor-side: isolated Blueprint shells for the mission and its HUD."""
import unreal
ROOT = '/Game/ThirdPerson/Blueprints/Entrega'
lib = unreal.BlueprintEditorLibrary
for name, parent in [('BP_DirectorEntrega',unreal.Actor),('BP_HUD_Entrega',unreal.HUD)]:
    assert not unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/'+name), name+' already exists'
    bp = lib.create_blueprint_asset_with_parent(ROOT+'/'+name,parent)
    lib.remove_unused_nodes(bp)
    if name == 'BP_DirectorEntrega':
        for variable in ('Baliza1','Baliza2','Baliza3','Salida'):
            assert lib.add_member_variable(bp,variable,lib.get_object_reference_type(unreal.StaticMeshActor))
            lib.set_blueprint_variable_instance_editable(bp,variable,True)
        assert lib.add_member_variable(bp,'Paso',lib.get_basic_type_by_name('int'))
        lib.compile_blueprint(bp)
        cdo = unreal.get_default_object(bp.generated_class())
        cdo.set_editor_property('auto_receive_input',unreal.AutoReceiveInput.PLAYER0)
        tick = cdo.get_editor_property('primary_actor_tick')
        tick.set_editor_property('tick_interval',0.2)
        cdo.set_editor_property('primary_actor_tick',tick)
    lib.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([unreal.load_asset(ROOT+'/BP_DirectorEntrega')])
unreal.log('DELIVERY_BLUEPRINT_SHELLS_CREATED')
