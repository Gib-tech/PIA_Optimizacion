import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
# ImportNodesFromText resuelve objetos ya cargados: mantener referencias duras.
for name in ['T_Inv_BotiquinTemporal','T_Inv_CeldaTemporal','T_Inv_CreditoCronal','F_InventarioTexto','F_InventarioNumero']:
 assert unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/Inventario/'+name)
bp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega')
assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/delivery_graphs/BP_HUD_Entrega.t3d'))
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.log('FINAL_HUD_INSTALLED')
