"""Bake a monospaced atlas with Spanish glyphs for Canvas dialogue."""
import unreal
path='/Game/ThirdPerson/Blueprints/Entrega/F_DialogueMono'
if not unreal.EditorAssetLibrary.does_asset_exist(path):
    factory=unreal.TrueTypeFontFactory()
    options=factory.get_editor_property('import_options')
    data=options.get_editor_property('data')
    for name,value in [('font_name','Consolas'),('height',16.0),('enable_antialiasing',False),('include_ascii_range',True),('texture_page_width',512),('texture_page_max_height',512),('use_distance_field_alpha',False)]:data.set_editor_property(name,value)
    options.set_editor_property('data',data)
    lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
    for name in ['bPropertiesConfigured','bFontSelected']:lib.call_method('SetBoolPropertyByName',(factory,name,True))
    font=unreal.AssetToolsHelpers.get_asset_tools().create_asset('F_DialogueMono','/Game/ThirdPerson/Blueprints/Entrega',unreal.Font,factory)
    assert font
else:font=unreal.load_asset(path)
assert font.get_editor_property('font_cache_type')==unreal.FontCacheType.OFFLINE
# TrueTypeFontFactory creates non-streaming atlas textures with no mipmaps.
unreal.EditorAssetLibrary.save_loaded_asset(font,only_if_is_dirty=False)
chars=font.get_editor_property('characters')
unreal.log('DIALOGUE_FONT_BAKED '+str(len(chars))+' glyphs '+str([(c,chars[ord(c)].get_editor_property('u_size'),chars[ord(c)].get_editor_property('v_size')) for c in ['M','i','á','ñ']]))
