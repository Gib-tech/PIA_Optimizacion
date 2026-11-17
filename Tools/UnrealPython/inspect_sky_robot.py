import unreal,os,json
sub=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);world=sub.get_editor_world();actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();result={'sky':[],'tech':[]}
for a in actors:
 if isinstance(a,(unreal.DirectionalLight,unreal.SkyLight,unreal.SkyAtmosphere,unreal.ExponentialHeightFog)) or any(k in a.get_actor_label().lower() for k in ['sky','cielo','atmos','nube','cloud']):
  row={'label':a.get_actor_label(),'class':a.get_class().get_name(),'path':a.get_path_name(),'rotation':str(a.get_actor_rotation()),'location':str(a.get_actor_location())}
  for c in a.get_components_by_class(unreal.ActorComponent):
   vals={}
   for key in ['intensity','atmosphere_sun_light','atmosphere_sun_light_index','real_time_capture','source_type','cubemap','lower_hemisphere_is_black','mobility','visible','aerial_perspective_view_distance_scale','start_distance']:
    try:vals[key]=str(c.get_editor_property(key))
    except Exception:pass
   if vals:row.setdefault('components',[]).append({'name':c.get_name(),**vals})
  result['sky'].append(row)
 if a.get_class().get_name() in ['BP_SistemasComplementarios_C','BP_TecnicoTemporal_C']:
  result['tech'].append({'label':a.get_actor_label(),'path':a.get_path_name(),'location':str(a.get_actor_location()),'rotation':str(a.get_actor_rotation())})
folder=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/robot-sky');os.makedirs(folder,exist_ok=True)
with open(os.path.join(folder,'before.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
unreal.log('SKY_ROBOT_INSPECTION '+json.dumps(result,ensure_ascii=False))
