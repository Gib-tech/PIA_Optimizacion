"""Retira exclusivamente la rama VR obsoleta del ejemplo de Kallari.

Este proyecto no usa VR ni la acción ResetVR. Se conservan los demás controles,
materiales y animaciones del pack y se documenta esta adaptación de UE5.6.
"""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bp=unreal.load_asset('/Game/ParagonKallari/Characters/Heroes/Kallari/KallariPlayerCharacter')
names=['K2Node_CallFunction_79','K2Node_InputAction_3']
present=[name for name in names if unreal.find_object(None,bp.get_path_name()+':EventGraph.'+name)]
removed=unreal.DeliveryBlueprintBuilder.remove_graph_nodes(bp,present) if present else 0
assert removed==len(present)
unreal.BlueprintEditorLibrary.compile_blueprint(bp);unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
with open(os.path.join(unreal.Paths.project_dir(),'docs/validation/compatibilidad-demo-kallari.json'),'w',encoding='utf-8') as f:json.dump({'asset':bp.get_path_name(),'removed_nodes':present,'reason':'Acción ResetVR sin configurar y función HeadMountedDisplay antigua ausente. Ejemplo sin uso en la misión; se retira sólo esa rama.'},f,indent=2,ensure_ascii=False)
unreal.log('LEGACY_VR_BRANCH_REMOVED '+str(removed))
