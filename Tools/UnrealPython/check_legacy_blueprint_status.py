import unreal
b=unreal.load_asset('/Game/ParagonKallari/Characters/Heroes/Kallari/KallariPlayerCharacter')
for name in ['Status','status','UbergraphPages','ubergraph_pages']:
 try:unreal.log('LEGACY_STATUS '+name+' '+str(b.get_editor_property(name)))
 except Exception as e:unreal.log('LEGACY_STATUS '+str(e))
for node in ['K2Node_CallFunction_79','K2Node_InputAction_3']:
 o=unreal.find_object(None,b.get_path_name()+':EventGraph.'+node)
 unreal.log('LEGACY_NODE '+node+' '+str(o))
