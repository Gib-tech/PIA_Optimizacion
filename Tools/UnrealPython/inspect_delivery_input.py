import unreal
asset=unreal.load_asset('/Game/ThirdPerson/Input/IMC_Default')
for mapping in asset.get_editor_property('mappings'):
    unreal.log('INPUT '+mapping.action.get_name()+' '+str(mapping.key.export_text()))
