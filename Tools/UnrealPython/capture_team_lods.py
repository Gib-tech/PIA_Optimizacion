"""Observe automatic LODs by camera distance; no forced LOD or gameplay claim."""
import unreal,os,json,math,traceback
def main():
 gs=unreal.GameplayStatics;w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
 pc=gs.get_player_controller(w,0);native=unreal.get_default_object(gs.static_class());tr=unreal.Transform();cam=native.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.CameraActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));native.call_method('FinishSpawningActor',(cam,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));cam.get_component_by_class(unreal.CameraComponent).set_field_of_view(60);pc.set_view_target_with_blend(cam,0)
 out=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/team-models/lods');os.makedirs(out,exist_ok=True)
 unique={}
 for a in gs.get_all_actors_of_class(w,unreal.StaticMeshActor):
  if a.get_actor_label().startswith('Equipo_') and a.static_mesh_component.static_mesh.get_name()!='SM_AutoDestruido':unique.setdefault(a.static_mesh_component.static_mesh.get_name(),a.static_mesh_component)
 assert len(unique)==4
 targets=[]
 for name,c in unique.items():
  assert c.forced_lod_model==0
  center,extent,radius=unreal.SystemLibrary.get_component_bounds(c)
  for i,factor in enumerate([4,12,24,80]):targets.append((name,i,center,radius*factor,radius))
 unreal.SystemLibrary.execute_console_command(w,'r.ForceLOD -1');unreal.SystemLibrary.execute_console_command(w,'viewmode lodcoloration');pc.get_hud().set_editor_property('show_hud',False)
 s={'index':0,'stage':0,'since':0,'handle':None,'busy':False,'rows':[],'no_forced_lods':True,'prepared_camera_fixture':True}
 def finish(error=None):
  unreal.unregister_slate_post_tick_callback(s['handle']);unreal.SystemLibrary.execute_console_command(w,'viewmode lit');s['passed']=error is None
  if error:s['error']=error
  with open(os.path.join(out,'observations.json'),'w') as f:json.dump({k:v for k,v in s.items() if k not in ['handle','busy']},f,indent=2)
  unreal.log('TEAM_LOD_CAPTURE_COMPLETE '+str(s['passed']))
 def tick(dt):
  if s['busy']:return
  s['busy']=True
  try:
   now=gs.get_time_seconds(w);name,index,center,distance,radius=targets[s['index']]
   if s['stage']==0:
    cam.set_actor_location(center+unreal.Vector(0,-distance*.5,distance*math.sqrt(.75)),False,True);cam.set_actor_rotation(unreal.Rotator(pitch=-60,yaw=90,roll=0),True);s.update(stage=1,since=now)
   elif s['stage']==1 and now-s['since']>.45:
    filename=name+'-'+str(index)+'.png';unreal.SystemLibrary.execute_console_command(w,'Shot filename="'+os.path.join(out,filename)+'"');s['rows'].append({'model':name,'requested_step':index,'distance_cm':distance,'radius_cm':radius,'fov':60,'file':filename});s.update(stage=2,since=now)
   elif s['stage']==2 and now-s['since']>.3:
    s['index']+=1;s['stage']=0
    if s['index']==len(targets):finish();return
   s['busy']=False
  except Exception:finish(traceback.format_exc())
 s['handle']=unreal.register_slate_post_tick_callback(tick)
 unreal.log('TEAM_LOD_CAPTURE_STARTED')
main()
