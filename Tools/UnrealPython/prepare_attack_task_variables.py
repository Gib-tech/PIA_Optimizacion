import unreal
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_Attack')
lib=unreal.BlueprintEditorLibrary
for name,typ in [('Elapsed',lib.get_basic_type_by_name('real')),('bHit',lib.get_basic_type_by_name('bool')),('Enemy',lib.get_object_reference_type(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')))]:
    lib.add_member_variable(bp,name,typ)
lib.compile_blueprint(bp)
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
for name in ['BTTask_Attack','BTTask_HitSun','BTTask_ChargerWindup','BTTask_ChargerCharge','BTTask_ChargerRetreat','BTTask_ChargerRecover']:
    bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/EnemigoIA/'+name)
    lib.add_member_variable(bp,'CachedPawn',lib.get_object_reference_type(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')))
    lib.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
