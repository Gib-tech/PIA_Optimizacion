"""Instala sólo los cuatro grafos revisados. No reinstala menús ni cinemáticas."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
ART='/Game/ThirdPerson/Blueprints/Entrega/Inventario';tools=unreal.AssetToolsHelpers.get_asset_tools()
for name in ['BotiquinTemporal','CeldaTemporal','CreditoCronal']:
 task=unreal.AssetImportTask();task.filename=os.path.join(root,'Tools/ArtSource/Inventario/T_Inv_'+name+'.png');task.destination_path=ART;task.destination_name='T_Inv_'+name;task.automated=True;task.replace_existing=True;task.save=True;tools.import_asset_tasks([task])
 texture=unreal.load_asset(ART+'/T_Inv_'+name);texture.set_editor_property('lod_group',unreal.TextureGroup.TEXTUREGROUP_UI);texture.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_EDITOR_ICON);texture.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS);unreal.EditorAssetLibrary.save_loaded_asset(texture,only_if_is_dirty=False)
for name in ['BP_SistemasComplementarios','BP_TecnicoTemporal','BP_DeliverySaveManager','BP_HUD_Entrega']:
 bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/'+name)
 unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
 assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs',name+'.t3d')),name
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('ROBOT_INVENTORY_REVISION_INSTALLED')
