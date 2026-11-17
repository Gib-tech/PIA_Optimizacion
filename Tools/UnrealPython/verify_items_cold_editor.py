"""Recarga normal sin helper y lectura del checkpoint del ejecutable de QA."""
import unreal,os,json,shutil
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not sub.get_game_world() and not hasattr(unreal,'DeliveryBlueprintBuilder')
assert sub.get_editor_world().get_name()=='Nivel_Entrega'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();robot=next(a for a in actors if a.get_class().get_name()=='BP_TecnicoTemporal_C')
capsule=robot.get_editor_property('ColisionRobot');assert capsule.get_collision_profile_name()=='BlockAllDynamic' and capsule.get_unscaled_capsule_radius()==37
table=next(a for a in actors if a.get_actor_label()=='Consola_Bruno');assert table.static_mesh_component.get_collision_profile_name()=='BlockAll'
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem);assert sm.get_convex_collision_count(table.static_mesh_component.static_mesh)==11
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());source=os.path.join(root,'Intermediate/inspect/items-native-user/Saved/SaveGames/TimeOut_Delivery_v1.sav');target=os.path.join(root,'Saved/SaveGames/QA_Items_Verificacion.sav');assert not os.path.exists(target)
try:
 shutil.copy2(source,target);data=unreal.GameplayStatics.load_game_from_slot('QA_Items_Verificacion',0);assert data
 saved={k:data.get_editor_property(k) for k in ['PlayerHealth','ExtrasRevision','Botiquines','Cargas','Creditos','MesaRecogido1','MesaRecogido2','MesaRecogido3']}
 assert saved=={'PlayerHealth':100.,'ExtrasRevision':3,'Botiquines':0,'Cargas':2,'Creditos':3,'MesaRecogido1':True,'MesaRecogido2':False,'MesaRecogido3':False},saved
finally:
 assert os.path.dirname(os.path.abspath(target))==os.path.abspath(os.path.join(root,'Saved/SaveGames'))
 if os.path.isfile(target):os.remove(target)
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not dirty,[p.get_name() for p in dirty]
result={'passed':True,'normal_editor_without_helper':True,'robot_blocks':True,'table_blocks_with_eleven_ucx':True,'native_save':saved,'temporary_slot_removed':True,'dirty_packages':[]}
with open(os.path.join(root,'docs/validation/items-colisiones/recarga-fria.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
unreal.log('ITEMS_COLD_EDITOR_AND_NATIVE_SAVE_PASSED')
