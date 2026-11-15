"""Editor-side: refuse to quit with unsaved content, otherwise close for UAT."""
import unreal
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert not dirty, 'Unsaved packages: '+', '.join(p.get_name() for p in dirty)
unreal.log('DELIVERY_BUILD_READY: all packages saved; closing editor for UAT')
unreal.SystemLibrary.quit_editor()
