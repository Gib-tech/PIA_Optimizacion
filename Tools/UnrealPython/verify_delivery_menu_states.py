"""PIE: missing/incompatible/corrupt saves disable Continue; restore original bytes."""
import unreal, os, json, pathlib, traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
cls=unreal.load_class(None,'/Game/Menu/Menu_Inicio.Menu_Inicio_C')
library=unreal.get_default_object(unreal.load_class(None,'/Script/UMG.WidgetBlueprintLibrary'))
widgets=library.call_method('GetAllWidgetsOfClass',(w,cls,True))
assert len(widgets)==1
widget=widgets[0];button=widget.get_editor_property('btn_continuar_menu')
path=pathlib.Path(unreal.Paths.project_saved_dir())/'SaveGames/TimeOut_Delivery_v1.sav'
original=path.read_bytes()
result={'agent_tests_not_owner_acceptance':True}
def refresh():
    widget.call_method('Construct')
    return button.get_is_enabled()
try:
    assert refresh();result['valid_save_enables_continue']=True
    data=unreal.GameplayStatics.load_game_from_slot('TimeOut_Delivery_v1',0)
    unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetIntPropertyByName',(data,'Version',99))
    assert unreal.GameplayStatics.save_game_to_slot(data,'TimeOut_Delivery_v1',0)
    assert not refresh();result['incompatible_save_disables_continue']=True
    assert unreal.GameplayStatics.delete_game_in_slot('TimeOut_Delivery_v1',0)
    assert not refresh();result['missing_save_disables_continue']=True
    path.write_bytes(b'Invalid checkpoint test')
    assert not refresh();result['corrupt_save_disables_continue']=True
    result['passed']=True
except Exception:
    result['passed']=False;result['error']=traceback.format_exc()
finally:
    path.write_bytes(original)
    result['original_save_restored']=refresh()
    out=pathlib.Path(unreal.Paths.project_dir())/'Intermediate/inspect/delivery_menu_assertions.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    unreal.log('SAVE_MENU_REGRESSION '+json.dumps(result))
assert result.get('passed') and result['original_save_restored'],result
