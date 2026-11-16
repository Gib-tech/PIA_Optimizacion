"""Set the menu's default presentation; Construct validates the mission checkpoint."""
import unreal
asset=unreal.load_asset('/Game/Menu/Menu_Inicio')
button=unreal.find_object(None,asset.get_path_name()+':WidgetTree.btn_continuar_menu')
assert button
asset.modify()
button.modify()
button.set_is_enabled(False)
button.set_tool_tip_text('Reanuda el ultimo punto de control guardado. Se habilita cuando existe una partida compatible.')
unreal.BlueprintEditorLibrary.compile_blueprint(asset)
unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
unreal.log('CONTINUE_ENABLED_AFTER_SAVE '+str(button.get_is_enabled()))
unreal.log('DELIVERY_MENU_PREPARED')
