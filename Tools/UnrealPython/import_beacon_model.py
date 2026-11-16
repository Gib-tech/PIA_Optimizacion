"""Import the supplied beacon without replacing the team's material regions."""
import unreal,os
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
ART='/Game/ThirdPerson/Environment/Baliza'
tools=unreal.AssetToolsHelpers.get_asset_tools()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
if True:
 options=unreal.FbxImportUI();options.automated_import_should_detect_type=False
 options.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
 options.import_materials=False;options.import_textures=False
 options.static_mesh_import_data.combine_meshes=True
 options.static_mesh_import_data.auto_generate_collision=True
 task=unreal.AssetImportTask();task.filename=os.path.join(root,'Tools/ArtSource/Baliza/SM_Baliza.fbx')
 task.destination_path=ART;task.destination_name='SM_Baliza';task.automated=True;task.save=True;task.options=options;task.replace_existing=True
 tools.import_asset_tasks([task])

def material(name,color,emission=0,metal=.5,rough=.815):
 path=ART+'/'+name;m=unreal.load_asset(path)
 if m:return m
 m=tools.create_asset(name,ART,unreal.Material,unreal.MaterialFactoryNew())
 m.set_editor_property('two_sided',True)
 edit=unreal.MaterialEditingLibrary
 rgb=edit.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-450,0)
 rgb.set_editor_property('constant',unreal.LinearColor(*color,1))
 edit.connect_material_property(rgb,'',unreal.MaterialProperty.MP_BASE_COLOR)
 for prop,value,y in [(unreal.MaterialProperty.MP_METALLIC,metal,140),(unreal.MaterialProperty.MP_ROUGHNESS,rough,240)]:
  n=edit.create_material_expression(m,unreal.MaterialExpressionConstant,-200,y);n.set_editor_property('r',value);edit.connect_material_property(n,'',prop)
 if emission:
  glow=edit.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-450,350)
  glow.set_editor_property('constant',unreal.LinearColor(*(c*emission for c in color),1))
  edit.connect_material_property(glow,'',unreal.MaterialProperty.MP_EMISSIVE_COLOR)
 edit.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m)
 return m
body=material('M_Baliza_Cuerpo',(.03498,.03498,.03498))
detail=material('M_Baliza_Detalles',(.03332,.03621,.04323))
off=material('M_Baliza_Espera',(.12,.18,.09),.6,0,.5)
material('M_Baliza_Siguiente',(.04,.65,1),4,0,.5)
material('M_Baliza_Activada',(.02533,1,0),7.9984,0,.5)
mesh=unreal.load_asset(ART+'/SM_Baliza');assert mesh
for i,slot in enumerate(mesh.static_materials):
 name=str(slot.material_slot_name)
 mesh.set_material(i,off if name=='Brillo' else (detail if name in ['Material.002','Material_002'] else body))
 unreal.log('BEACON_SLOT '+str(i)+' '+name)
unreal.EditorAssetLibrary.save_loaded_asset(mesh)
unreal.log('BEACON_IMPORTED '+str(mesh.get_bounds()))
