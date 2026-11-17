"""Instala sólo inventario, HUD y guardado. Conserva menús y cinemáticas."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());R='/Game/ThirdPerson/Blueprints/Entrega/'
for path in [R+'BP_PulsoTemporalVisual']+[R+'Inventario/'+n for n in ['T_Inv_BotiquinTemporal','T_Inv_CeldaTemporal','T_Inv_CreditoCronal','F_InventarioTexto','F_InventarioNumero']]:assert unreal.load_asset(path),path
for name in ['BP_SistemasComplementarios','BP_DeliverySaveManager','BP_HUD_Entrega']:
 bp=unreal.load_asset(R+name);unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(bp)
 assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs',name+'.t3d')),name
 unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level();unreal.log('ITEMS_REVISION_INSTALLED')
