"""Isolated renderer/scalability check. Camera moves are not a mission playthrough."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;pc=gs.get_player_controller(w,0);player=gs.get_player_pawn(w,0)
actors=gs.get_all_actors_of_class(w,unreal.Actor)
report={'isolated_camera_test':True,'partitioned':unreal.DeliveryBlueprintBuilder.is_partitioned(w),'lights':[],'samples':[]}
walls=[a for a in actors if a.get_name().startswith('StaticMeshActor') and a.get_component_by_class(unreal.StaticMeshComponent) and a.get_component_by_class(unreal.StaticMeshComponent).static_mesh and a.get_component_by_class(unreal.StaticMeshComponent).static_mesh.get_name().startswith('SM_Walls_')]
assert len(walls)==10,len(walls)
report['separate_buildings']=len(walls)
for a in [a for a in gs.get_all_actors_of_class(w,unreal.Light) if isinstance(a,(unreal.PointLight,unreal.SpotLight,unreal.RectLight))]:
 c=a.light_component;item={'type':c.get_class().get_name(),'forward_z':a.get_actor_forward_vector().z,'radius':c.get_editor_property('attenuation_radius'),'max_distance':c.get_editor_property('max_draw_distance'),'fade':c.get_editor_property('max_distance_fade_range'),'shadows':c.get_editor_property('cast_shadows')}
 assert item['max_distance']==2400 and item['fade']==350,item
 if isinstance(a,unreal.RectLight):assert item['forward_z']<-.99,item
 if isinstance(a,unreal.SpotLight):assert item['forward_z']<-.7,item
 report['lights'].append(item)
assert len(report['lights'])==3
components=[a.get_component_by_class(unreal.NiagaraComponent) for a in actors]
leaves=next(c for c in components if c and c.get_asset() and c.get_asset().get_name()=='NS_Compound_Hojas')
lib=unreal.get_default_object(gs.static_class());tr=unreal.Transform(location=unreal.Vector(1450,0,220),rotation=unreal.Rotator(pitch=4,yaw=-90,roll=0))
cam=lib.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.CameraActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));lib.call_method('FinishSpawningActor',(cam,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));pc.set_view_target_with_blend(cam,0)
state={'stage':0,'age':0,'handle':None}
out=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/compound_visibility.json')
with open(out,'w') as f:json.dump({'running':True},f)
def observe(dt,s=state):
 try:
  s['age']+=dt
  if s['age']<4:return
  culled=not leaves.is_active()
  report['samples'].append({'stage':['visible_near','far','visible_again','looking_away'][s['stage']],'component_inactive':culled})
  assert culled==(s['stage'] in (1,3)),report['samples']
  if s['stage']==3:
   report['passed']=True;pc.set_view_target_with_blend(player,0);unreal.unregister_slate_post_tick_callback(s['handle'])
   with open(out,'w') as f:json.dump(report,f,indent=2)
   unreal.log('COMPOUND_VISIBILITY_PASSED');return
  s['stage']+=1;s['age']=0
  cam.set_actor_location(unreal.Vector(0,-11200,500) if s['stage']==1 else unreal.Vector(1450,0,220),False,True)
  cam.set_actor_rotation(unreal.Rotator(pitch=4,yaw=90 if s['stage']==3 else -90,roll=0),True)
 except Exception:
  report.update(passed=False,error=traceback.format_exc());unreal.unregister_slate_post_tick_callback(s['handle'])
  with open(out,'w') as f:json.dump(report,f,indent=2)
  unreal.log_error(report['error'])
state['handle']=unreal.register_slate_post_tick_callback(observe)
