"""Leyenda española que cubre acciones reales con teclado y mando."""
import unreal
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bp=unreal.load_asset('/Game/Menu/Menu_Pausa');tree=unreal.find_object(None,bp.get_path_name()+':WidgetTree')
caption=unreal.find_object(None,tree.get_path_name()+'.ControlsHelpText');assert caption
caption.modify();caption.set_font(unreal.SlateFontInfo(font_object=unreal.load_asset('/Engine/EngineFonts/Roboto'),size=18))
caption.set_text('CONTROLES\n\nWASD / stick izq.: moverse\nRatón / stick der.: mirar\nEspacio / A: saltar\nClic izq. / X: ligero\nClic der. / Y: pesado\nC / pulsar stick der.: cámara\nT / cruceta izq.: espada\nY / cruceta der.: martillo\nE / RB: interactuar\nI / SELECT: inventario\nH / LB: botiquín\nClic central / RT: pulso\nF5 / botón Guardar: checkpoint\nEnter / cruceta arriba: leer\nP / ESC / START: pausa\nB: volver en menús')
unreal.BlueprintEditorLibrary.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
unreal.log('CONTROL_LEGEND_UPDATED')
