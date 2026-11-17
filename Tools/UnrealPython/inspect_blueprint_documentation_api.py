import unreal
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega')
for name in ['BlueprintDescription','blueprint_description','BlueprintCategory','blueprint_category']:
 try:unreal.log('BP_DOC_FIELD '+name+' '+str(bp.get_editor_property(name)))
 except Exception as e:unreal.log('BP_DOC_FIELD '+name+' '+str(e))
unreal.log('BP_DOC_API '+str([n for n in dir(bp) if any(k in n.lower() for k in ['descrip','tooltip','metadata','comment'])]))
unreal.log('BP_DOC_LIBRARY '+str([n for n in dir(unreal.BlueprintEditorLibrary) if any(k in n.lower() for k in ['descrip','tooltip','metadata','comment'])]))
