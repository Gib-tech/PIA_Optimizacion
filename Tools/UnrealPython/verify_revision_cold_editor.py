"""Lectura tras abrir el editor normal sin helper ni PIE."""
import unreal,os,json
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not sub.get_game_world() and not hasattr(unreal,'DeliveryBlueprintBuilder')
assert sub.get_editor_world().get_name()=='Nivel_Entrega'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
extra=next(a for a in actors if a.get_class().get_name()=='BP_SistemasComplementarios_C')
assert extra.get_editor_property('auto_receive_input')==unreal.AutoReceiveInput.PLAYER0 and extra.get_editor_property('input_priority')==5
host=next(a for a in actors if a.get_class().get_name()=='BP_Hostage_C')
assert 'SK_RehenSuperviviente' in host.mesh.get_skeletal_mesh_asset().get_path_name() and 'ABP_RehenSuperviviente' in host.mesh.anim_class.get_path_name()
for path in ['/Game/ThirdPerson/Characters/PrimeraPersona/SK_BrazosPrimeraPersona','/Game/ThirdPerson/Characters/PrimeraPersona/Animaciones/AFP_FA_1','/Game/ThirdPerson/Environment/Complementos/SM_CajaSuministros']:
 assert unreal.load_asset(path),path
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
result={'passed':True,'normal_editor_without_helper':True,'no_pie':True,'survivor_mesh_and_abp':True,'placed_input_player0_priority5':True,'fp_assets_load':True,'dirty_packages':[p.get_name() for p in dirty]}
assert not dirty,result
with open(os.path.join(unreal.Paths.project_dir(),'docs/validation/editor-recarga-fria.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
unreal.log('REVISION_COLD_EDITOR_PASSED')
