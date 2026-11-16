"""Prepare owned UI assets, audio preferences, and small additions to team widgets."""
import unreal, os
R='/Game/ThirdPerson/Blueprints/Entrega/'
lib=unreal.BlueprintEditorLibrary;tools=unreal.AssetToolsHelpers.get_asset_tools()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()

def shell(name,parent):
    bp=unreal.load_asset(R+name)
    if not bp:
        factory=unreal.BlueprintFactory();factory.set_editor_property('parent_class',parent)
        bp=tools.create_asset(name,R.rstrip('/'),unreal.Blueprint,factory)
    return bp

def add(bp,name,kind):
    try:unreal.get_default_object(bp.generated_class()).get_editor_property(name);return
    except Exception:pass
    if kind.startswith('/'):
        cls=unreal.load_class(None,kind);typ=lib.get_object_reference_type(cls)
    else:typ=lib.get_basic_type_by_name(kind)
    assert lib.add_member_variable(bp,name,typ),(name,kind)

settings=shell('BP_DeliveryOptions',unreal.SaveGame)
ui=shell('BP_DeliveryInterface',unreal.Actor)
for name,kind in {'Version':'int','MasterVolume':'real'}.items():add(settings,name,kind)
fields={
 'bInitialized':'bool','bPauseOpen':'bool','bOptionsOpen':'bool','MasterVolume':'real',
 'PauseWidget':'/Script/UMG.UserWidget','OptionsWidget':'/Script/UMG.UserWidget',
 'ReturnWidget':'/Script/UMG.UserWidget','ReturnFocus':'/Script/UMG.Widget',
 'OptionsData':R+'BP_DeliveryOptions.BP_DeliveryOptions_C',
}
for name,kind in fields.items():add(ui,name,kind)
hero=unreal.load_asset(R+'BP_PlayerEntrega')
add(hero,'LastFirstPerson','bool')
for bp in [settings,ui,hero]:
    lib.compile_blueprint(bp)
    if bp in [settings,ui]:unreal.get_default_object(bp.generated_class()).set_editor_property('MasterVolume',1.0)
    if bp==ui:
        cdo=unreal.get_default_object(bp.generated_class())
        cdo.set_editor_property('auto_receive_input',unreal.AutoReceiveInput.PLAYER0)
        cdo.set_editor_property('input_priority',10)
    unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)

mixpath='/Game/ThirdPerson/Audio/SM_TimeOutSettings'
if not unreal.load_asset(mixpath):
    factory=unreal.new_object(unreal.load_class(None,'/Script/AudioEditor.SoundMixFactory'))
    mix=tools.create_asset('SM_TimeOutSettings','/Game/ThirdPerson/Audio',unreal.SoundMix,factory)
    assert mix
    unreal.EditorAssetLibrary.save_loaded_asset(mix,only_if_is_dirty=False)
assert unreal.load_asset('/Engine/EngineSounds/Master')

options=unreal.load_asset('/Game/Menu/Menu_Opciones')
tree=unreal.find_object(None,options.get_path_name()+':WidgetTree')
canvas=unreal.find_object(None,tree.get_path_name()+'.CanvasPanel_43')
assert canvas
source_button=unreal.find_object(None,tree.get_path_name()+'.btn_shadow1_O')
style=source_button.get_editor_property('widget_style')
button_color=source_button.get_editor_property('background_color')
font=unreal.SlateFontInfo(font_object=unreal.load_asset('/Engine/EngineFonts/Roboto'),size=22)

def text(name,value,x,y,width=500,size=22):
    obj=unreal.find_object(None,tree.get_path_name()+'.'+name)
    if not obj:
        obj=unreal.new_object(unreal.TextBlock,outer=tree,name=name)
    assert unreal.DeliveryBlueprintBuilder.set_property_text(obj,'bIsVariable','True' if name=='SettingsStatus' else 'False')
    if not obj.get_parent():
        slot=canvas.add_child_to_canvas(obj);slot.set_position(unreal.Vector2D(x,y));slot.set_size(unreal.Vector2D(width,50));slot.set_z_order(5)
    obj.set_text(value);obj.set_font(unreal.SlateFontInfo(font_object=font.font_object,size=size))
    color=unreal.LinearColor(1,1,1,1) if name in ['SettingsStatus','SettingsKeys'] else unreal.LinearColor(1,.224,.748,1)
    obj.set_color_and_opacity(unreal.SlateColor(specified_color=color))
    return obj

def button(name,label,x,y,width=200):
    obj=unreal.find_object(None,tree.get_path_name()+'.'+name)
    if obj:
        obj.set_background_color(button_color)
        caption=obj.get_child_at(0)
        if isinstance(caption,unreal.TextBlock):caption.set_font(font)
        return obj
    obj=unreal.new_object(unreal.Button,outer=tree,name=name)
    assert unreal.DeliveryBlueprintBuilder.set_property_text(obj,'bIsVariable','True')
    obj.set_style(style)
    obj.set_background_color(button_color)
    slot=canvas.add_child_to_canvas(obj);slot.set_position(unreal.Vector2D(x,y));slot.set_size(unreal.Vector2D(width,55));slot.set_z_order(5)
    caption=unreal.new_object(unreal.TextBlock,outer=tree,name=name+'_Caption')
    caption.set_text(label);caption.set_font(font)
    caption.set_color_and_opacity(unreal.SlateColor(specified_color=unreal.LinearColor(0,.004,.1,1)))
    content_slot=obj.add_child(caption)
    content_slot.set_horizontal_alignment(unreal.HorizontalAlignment.H_ALIGN_CENTER)
    content_slot.set_vertical_alignment(unreal.VerticalAlignment.V_ALIGN_CENTER)
    return obj

text('VolumeLabel','Volumen',380,765,250,28)
for i,(label,x) in enumerate([('0 %',650),('25 %',880),('50 %',1110),('100 %',1340)]):button('btn_volume'+str(i),label,x,760)
old_display=unreal.find_object(None,tree.get_path_name()+'.DisplayLabel')
if old_display:
    unreal.DeliveryBlueprintBuilder.set_property_text(old_display,'bIsVariable','False')
    old_display.remove_from_parent()
text('ScreenModeLabel','Pantalla',380,850,250,28)
for i,(label,x) in enumerate([('Ventana',650),('Sin bordes',940),('Completa',1230)]):button('btn_display'+str(i),label,x,845,260)
text('SettingsStatus','Los cambios se aplican y guardan al elegir.',380,940,900,19)
text('SettingsKeys','ESC: volver    TAB / flechas: elegir    ENTER: confirmar',380,995,1150,18)
for i,label in enumerate(['1280x720','1600x900','1920x1080','2560x1440'],1):
    btn=unreal.find_object(None,tree.get_path_name()+'.btn_resolucion'+str(i)+'_O')
    child=btn.get_child_at(0)
    if isinstance(child,unreal.TextBlock):child.set_text(label)
for name,value in {'RTB_1':'1280x720','RTB2':'1600x900','RTB_3':'1920x1080','RTB_4':'2560x1440'}.items():
    obj=unreal.find_object(None,tree.get_path_name()+'.'+name)
    if obj:obj.set_text(value)
for prefix in ['AATB_','STB_','TTB_']:
    for i,value in enumerate(['Baja','Media','Alta','Epica'],1):
        obj=unreal.find_object(None,tree.get_path_name()+'.'+prefix+str(i))
        if obj:obj.set_text(value)
for i,value in enumerate(['Corta','Media','Larga'],1):
    obj=unreal.find_object(None,tree.get_path_name()+'.VDTB_'+str(i))
    if obj:obj.set_text(value)
layout=unreal.get_default_object(unreal.load_class(None,'/Script/UMG.WidgetLayoutLibrary'))
# The original independent captions sat above buttons and intercepted their clicks.
for obj in canvas.get_all_children():
    if isinstance(obj,unreal.TextBlock):obj.set_visibility(unreal.SlateVisibility.HIT_TEST_INVISIBLE)
back=unreal.find_object(None,tree.get_path_name()+'.btn_volver_opciones')
back_slot=layout.call_method('SlotAsCanvasSlot',(back,))
back_slot.set_anchors(unreal.Anchors(minimum=unreal.Vector2D(0,0),maximum=unreal.Vector2D(0,0)))
back_slot.set_position(unreal.Vector2D(1460,905));back_slot.set_size(unreal.Vector2D(240,95))
for name,label in [('viewdistance_TB','Distancia'),('shadows_TB','Sombras'),('Textues_TB','Texturas')]:
    obj=unreal.find_object(None,tree.get_path_name()+'.'+name)
    if obj:obj.set_text(label)
lib.compile_blueprint(options);unreal.EditorAssetLibrary.save_loaded_asset(options,only_if_is_dirty=False)

pause=unreal.load_asset('/Game/Menu/Menu_Pausa')
ptree=unreal.find_object(None,pause.get_path_name()+':WidgetTree')
pcanvas=unreal.find_object(None,ptree.get_path_name()+'.CanvasPanel_173');assert pcanvas
for name,label,y in [('PauseStatus','P / ESC: reanudar',865),('PauseSaveStatus','',930)]:
    obj=unreal.find_object(None,ptree.get_path_name()+'.'+name)
    if not obj:
        obj=unreal.new_object(unreal.TextBlock,outer=ptree,name=name)
        assert unreal.DeliveryBlueprintBuilder.set_property_text(obj,'bIsVariable','True')
        slot=pcanvas.add_child_to_canvas(obj);slot.set_position(unreal.Vector2D(360,y));slot.set_size(unreal.Vector2D(1250,60));slot.set_z_order(8)
    slot=layout.call_method('SlotAsCanvasSlot',(obj,))
    slot.set_position(unreal.Vector2D(730,y));slot.set_size(unreal.Vector2D(560,85))
    obj.set_auto_wrap_text(True)
    obj.set_text(label);obj.set_font(unreal.SlateFontInfo(font_object=font.font_object,size=18));obj.set_color_and_opacity(unreal.SlateColor(specified_color=unreal.LinearColor(1,1,1,1)))
# Keep a readable control legend beside the original pause artwork.
border=unreal.find_object(None,ptree.get_path_name()+'.ControlsHelpPanel')
if not border:
    border=unreal.new_object(unreal.Border,outer=ptree,name='ControlsHelpPanel')
    slot=pcanvas.add_child_to_canvas(border);slot.set_position(unreal.Vector2D(1410,260));slot.set_size(unreal.Vector2D(480,590));slot.set_z_order(10)
    caption=unreal.new_object(unreal.TextBlock,outer=ptree,name='ControlsHelpText');border.add_child(caption)
else:caption=border.get_child_at(0)
border.set_brush_color(unreal.LinearColor(0,.003,.025,.92));border.set_padding(unreal.Margin(22))
caption.set_text('CONTROLES\n\nWASD / flechas: moverse\nRaton: mirar\nEspacio: saltar\nClic izq.: ataque ligero\nClic der.: ataque pesado\nC: cambiar camara\nY: martillo / T: espada\nE: rescatar / seguir\nF5: guardar a salvo\nEnter: leer / cerrar\nP / ESC: pausa')
caption.set_font(unreal.SlateFontInfo(font_object=font.font_object,size=22))
caption.set_color_and_opacity(unreal.SlateColor(specified_color=unreal.LinearColor(1,1,1,1)))
border.set_visibility(unreal.SlateVisibility.HIT_TEST_INVISIBLE)
lib.compile_blueprint(pause);unreal.EditorAssetLibrary.save_loaded_asset(pause,only_if_is_dirty=False)

levels=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
for levelpath in ['/Game/LevelMenu/MainMenuLevel','/Game/ThirdPerson/Maps/Nivel_Entrega']:
    assert levels.load_level(levelpath)
    found=[a for a in actors.get_all_level_actors() if a.get_class()==ui.generated_class()]
    assert len(found)<=1
    if not found:
        a=actors.spawn_actor_from_class(ui.generated_class(),unreal.Vector(0,0,0));a.set_actor_label('Interfaz_Entrega')
    levels.save_current_level()
unreal.log('DELIVERY_CONTROLS_PREPARED')
