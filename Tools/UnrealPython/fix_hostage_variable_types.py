import unreal
ROOT='/Game/ThirdPerson/Blueprints/Aliado/'
lib=unreal.BlueprintEditorLibrary
for name in ['int','float','double','real']:
    unreal.log('PIN_TYPE %s=%s' % (name,lib.get_basic_type_by_name(name)))
bp=unreal.load_asset(ROOT+'BTService_HostageSense')
lib.remove_unused_variables(bp)
for variable in ['ThreatActor','Candidate','SafeCandidate']:
    lib.add_member_variable(bp,variable,lib.get_object_reference_type(unreal.Actor))
for variable in ['BestDistance','MinEnemyDistance','ThreatRadius','SafeEnemyDistance','SafePlayerDistance']:
    lib.add_member_variable(bp,variable,lib.get_basic_type_by_name('real'))
for variable in ['ThreatRadius','SafeEnemyDistance','SafePlayerDistance']:
    lib.set_blueprint_variable_instance_editable(bp,variable,True)
lib.compile_blueprint(bp)
cdo=unreal.get_default_object(bp.generated_class())
for key,value in [('ThreatRadius',800),('SafeEnemyDistance',1200),('SafePlayerDistance',1000)]:
    cdo.set_editor_property(key,value)
unreal.EditorAssetLibrary.save_loaded_asset(bp)
