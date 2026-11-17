"""Comprueba fuentes en editor normal y lee un guardado nativo en slot temporal."""
import unreal,os,json,shutil
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not sub.get_game_world() and not hasattr(unreal,'DeliveryBlueprintBuilder')
assert sub.get_editor_world().get_name()=='Nivel_Entrega'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();robot=next(a for a in actors if a.get_class().get_name()=='BP_TecnicoTemporal_C');extra=next(a for a in actors if a.get_class().get_name()=='BP_SistemasComplementarios_C')
assert robot.skeletal_mesh_component.get_skeletal_mesh_asset() is None
meshes=robot.get_components_by_class(unreal.StaticMeshComponent);assert len(meshes)==3 and all(c.get_editor_property('static_mesh') for c in meshes)
assert extra.get_editor_property('SkyDome') and extra.get_editor_property('Moon') and extra.get_editor_property('Sky').light_component.real_time_capture
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());source=os.path.join(root,'Intermediate/inspect/robot-native-user/Saved/SaveGames/TimeOut_Delivery_v1.sav');target=os.path.join(root,'Saved/SaveGames/QA_BRUNO_Verificacion.sav')
assert not os.path.exists(target),'No reemplazar un slot que ya existe'
try:
 shutil.copy2(source,target);data=unreal.GameplayStatics.load_game_from_slot('QA_BRUNO_Verificacion',0);assert data
 saved={k:data.get_editor_property(k) for k in ['Version','ExtrasRevision','Botiquines','Cargas','Creditos','RobotEnergy','bFabricating','FabricationProgress','WorldSeconds','FirstPerson']}
 assert saved['Botiquines']==2 and saved['Cargas']==2 and saved['Creditos']==0 and saved['RobotEnergy']==0 and not saved['bFabricating'] and saved['FirstPerson'] and saved['WorldSeconds']>0,saved
finally:
 assert os.path.dirname(os.path.abspath(target))==os.path.abspath(os.path.join(root,'Saved/SaveGames'))
 if os.path.isfile(target):os.remove(target)
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert not dirty,[p.get_name() for p in dirty]
report={'passed':True,'normal_editor_without_helper':True,'no_pie':True,'robot_three_parts_no_human':True,'sky_references_realtime_capture':True,'native_save_read_by_unreal':saved,'temporary_slot_removed':True,'dirty_packages':[]}
with open(os.path.join(root,'docs/validation/robot-cielo-inventario/recarga-fria.json'),'w',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
unreal.log('ROBOT_COLD_EDITOR_AND_NATIVE_SAVE_PASSED')
