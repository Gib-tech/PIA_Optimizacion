import unreal
unreal.log('LEGACY_VR_CLASS '+str(getattr(unreal,'HeadMountedDisplayFunctionLibrary',None)))
unreal.log('LEGACY_VR_REFRESH '+str([n for n in dir(unreal.BlueprintEditorLibrary) if any(k in n for k in ['refresh','node','reconstruct'])]))
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega');unreal.log('SPANISH_DESCRIPTION_READBACK '+bp.get_editor_property('BlueprintDescription'))
