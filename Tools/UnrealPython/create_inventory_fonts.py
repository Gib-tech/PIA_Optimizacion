"""Atlas nítidos de uso exclusivo del inventario; no cambia tipografía de menús."""
import unreal
ART='/Game/ThirdPerson/Blueprints/Entrega/Inventario'
for name,height in [('F_InventarioTexto',24.),('F_InventarioNumero',48.)]:
 font=unreal.load_asset(ART+'/'+name)
 if font:
  chars=font.get_editor_property('characters')
  if len(chars)<127 or chars[65].get_editor_property('u_size')==0 or font.get_editor_property('import_options').get_editor_property('x_padding')<4:
   unreal.EditorAssetLibrary.delete_loaded_asset(font);font=None
 if not font:
  factory=unreal.TrueTypeFontFactory();options=factory.get_editor_property('import_options');data=options.get_editor_property('data')
  for key,value in [('font_name','Segoe UI'),('height',height),('enable_antialiasing',True),('include_ascii_range',True),('texture_page_width',1024),('texture_page_max_height',1024),('x_padding',4),('y_padding',4),('use_distance_field_alpha',False),('chars',''.join(chr(i) for i in range(32,256))+'→')]:data.set_editor_property(key,value)
  options.set_editor_property('data',data);lib=unreal.get_default_object(unreal.SystemLibrary)
  for key in ['bPropertiesConfigured','bFontSelected']:lib.call_method('SetBoolPropertyByName',(factory,key,True))
  font=unreal.AssetToolsHelpers.get_asset_tools().create_asset(name,ART,unreal.Font,factory);assert font
 unreal.EditorAssetLibrary.save_loaded_asset(font,only_if_is_dirty=False)
unreal.log('INVENTORY_FONTS_READY')
