import os
import unreal
root='/Game/ThirdPerson/Environment/EscenarioIan/'
out=os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()),'Intermediate/inspect/live')
for name in ['Sector1','Sector2','Sector3','Sector4','M_Suelo']:
    material=unreal.load_asset(root+name)
    node=unreal.MaterialEditingLibrary.get_material_property_input_node(material,unreal.MaterialProperty.MP_BASE_COLOR)
    texture=node.get_editor_property('texture') if isinstance(node,unreal.MaterialExpressionTextureSample) else None
    unreal.log('DELIVERY_MATERIAL '+name+' node='+str(node)+' texture='+str(texture))
    task=unreal.AssetExportTask();task.object=material;task.filename=os.path.join(out,name+'.t3d')
    task.automated=True;task.prompt=False;task.replace_identical=True;unreal.Exporter.run_asset_export_task(task)
menu=unreal.load_asset('/Game/Menu/Menu_Inicio')
button=unreal.find_object(None,menu.get_path_name()+':WidgetTree.btn_continuar_menu')
unreal.log('CONTINUE_ENABLED '+str(button.get_is_enabled()))
