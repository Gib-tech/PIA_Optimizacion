"""Disable legacy Continue: the new mission does not yet persist escort/objective state."""
import unreal
asset=unreal.load_asset('/Game/Menu/Menu_Inicio')
button=unreal.find_object(None,asset.get_path_name()+':WidgetTree.btn_continuar_menu')
assert button
asset.modify()
button.modify()
button.set_is_enabled(False)
button.set_tool_tip_text('Continuar no esta disponible para esta mision. Usa Nuevo juego.')
unreal.BlueprintEditorLibrary.compile_blueprint(asset)
unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
unreal.log('CONTINUE_ENABLED_AFTER_SAVE '+str(button.get_is_enabled()))
unreal.log('DELIVERY_MENU_PREPARED')
