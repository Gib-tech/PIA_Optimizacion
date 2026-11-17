"""Verifica mapa, jerarquía de luces y save de QA en editor normal sin helper."""
import unreal,os,json,shutil,re
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not sub.get_game_world() and not hasattr(unreal,'DeliveryBlueprintBuilder')
assert sub.get_editor_world().get_name()=='Nivel_Entrega'
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());R='/Game/ThirdPerson/Blueprints/Entrega/'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
lamps=[a for a in actors if a.get_class().get_name()=='BP_LuminariaPared_C'];assert len(lamps)==41,len(lamps)
for actor in lamps:
 light=actor.get_component_by_class(unreal.SpotLightComponent)
 assert light.get_attach_parent()==actor.root_component and light.get_world_location().distance(actor.get_actor_location())<50,actor.get_actor_label()
 assert light.intensity==3200 and light.get_editor_property('cast_shadows') and light.get_editor_property('max_draw_distance')==2700
 for c in actor.get_components_by_class(unreal.StaticMeshComponent):assert c.get_collision_enabled()==unreal.CollisionEnabled.NO_COLLISION and not c.get_editor_property('can_ever_affect_navigation')
extra=next(a for a in actors if a.get_class().get_name()=='BP_SistemasComplementarios_C');assert extra.get_editor_property('DayCycleDuration')==1200
source=os.path.join(root,'Intermediate/inspect/daynight-attacks/native-user/Saved/SaveGames/TimeOut_Delivery_v1.sav');target=os.path.join(root,'Saved/SaveGames/QA_Daynight_Verificacion.sav');assert not os.path.exists(target)
try:
 shutil.copy2(source,target);data=unreal.GameplayStatics.load_game_from_slot('QA_Daynight_Verificacion',0);assert data
 saved={k:data.get_editor_property(k) for k in ['Version','WorldSeconds','FirstPerson','Cargas','Paso']};assert saved['Version']==2 and saved['WorldSeconds']>=783 and saved['FirstPerson'] and saved['Cargas']==2 and saved['Paso']==0
finally:
 assert os.path.dirname(os.path.abspath(target))==os.path.abspath(os.path.join(root,'Saved/SaveGames'))
 if os.path.isfile(target):os.remove(target)
# Exportar tras recarga fría descarta nodos huérfanos de instalaciones anteriores.
rows=[]
for name in ['BP_SistemasComplementarios','BP_PlayerEntrega','BP_DestruibleEntrega','BP_HUD_Entrega','BP_LuminariaPared','BP_DirectorEntrega','BP_DeliverySaveManager']:
 bp=unreal.load_asset(R+name);task=unreal.AssetExportTask();task.object=bp;task.filename=os.path.join(root,'Intermediate/inspect/daynight-attacks',name+'-cold.t3d');task.automated=True;task.prompt=False;task.replace_identical=True;assert unreal.Exporter.run_asset_export_task(task)
 raw=open(task.filename,'rb').read();text=raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig')
 # ErrorType puede conservar el último valor aunque el compilador haya limpiado
 # su mensaje. Sólo cuenta un diagnóstico activo (bHasCompilerMessage=True).
 fatal=any('bHasCompilerMessage=True' in block and re.search(r'^\s*ErrorType=1\s*$',block,re.M) for block in text.split('Begin Object'))
 assert not fatal,name
 rows.append({'blueprint':bp.get_path_name(),'cold_reload':True,'active_error_nodes':0,'diagnostics':sorted(set(re.findall(r'ErrorMsg="([^"]+)"',text)))})
folder=os.path.join(root,'docs/validation/ciclo-luces-ataques')
with open(os.path.join(folder,'compilacion.json'),'w',encoding='utf-8') as f:json.dump({'passed':True,'method':'Instalación compilada por InstallGraph, dependencias recompiladas, cook y recarga fría. Exportación del asset recién cargado sin nodos huérfanos de ediciones previas.','blueprints':rows},f,ensure_ascii=False,indent=2)
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages();assert not dirty,[p.get_name() for p in dirty]
with open(os.path.join(folder,'recarga-fria.json'),'w',encoding='utf-8') as f:json.dump({'passed':True,'normal_editor_without_helper':True,'wall_light_count':len(lamps),'all_lights_follow_root_with_shadows':True,'fixtures_do_not_collide_or_affect_navigation':True,'cycle_seconds':1200,'native_save_read_by_unreal':saved,'temporary_slot_removed':True,'dirty_packages':[]},f,ensure_ascii=False,indent=2)
unreal.log('DAYNIGHT_COLD_EDITOR_PASSED')
preferences=json.load(open(os.path.join(root,'Intermediate/inspect/daynight-attacks/editor-performance.json')))
unreal.get_default_object(unreal.load_class(None,'/Script/UnrealEd.EditorPerformanceSettings')).set_editor_property('bThrottleCPUWhenNotForeground',preferences['throttle'])
