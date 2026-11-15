import unreal
ROOT='/Game/ThirdPerson/Blueprints/Aliado'
assert not unreal.EditorAssetLibrary.does_asset_exist(ROOT+'/ABP_Hostage'), 'Support already created; do not overwrite the working animation graph.'
bb=unreal.load_asset(ROOT+'/BB_Hostage')
keys=list(bb.get_editor_property('keys'))
if not any(str(k.get_editor_property('entry_name'))=='Estado' for k in keys):
    key=unreal.BlackboardEntry()
    key.set_editor_property('entry_name','Estado')
    key.set_editor_property('key_type',unreal.new_object(unreal.load_class(None,'/Script/AIModule.BlackboardKeyType_Int'),outer=bb))
    keys.append(key);bb.set_editor_property('keys',keys);unreal.EditorAssetLibrary.save_loaded_asset(bb)
anim=unreal.EditorAssetLibrary.duplicate_asset(ROOT+'/ABP_Aliado',ROOT+'/ABP_Hostage')
assert anim,'ABP_Hostage already exists'
unreal.BlueprintEditorLibrary.remove_unused_nodes(anim)
unreal.BlueprintEditorLibrary.compile_blueprint(anim)
unreal.EditorAssetLibrary.save_loaded_asset(anim)
cdo=unreal.get_default_object(unreal.load_class(None,ROOT+'/BP_Hostage.BP_Hostage_C'))
cdo.mesh.set_anim_instance_class(anim.generated_class())
unreal.EditorAssetLibrary.save_asset(ROOT+'/BP_Hostage')
unreal.log('HOSTAGE_SUPPORT_READY')
