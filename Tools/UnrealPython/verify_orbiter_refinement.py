"""Live orbiter tree regression: closes distance, circles, attacks and faces locomotion."""
import unreal,json,os,traceback,math
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);p.set_actor_location(unreal.Vector(0,-2000,100),False,True)
unreal.get_default_object(unreal.SystemLibrary.static_class()).call_method('SetBoolPropertyByName',(p,'bCanBeDamaged',False))
gs=unreal.get_default_object(unreal.GameplayStatics.static_class());tr=unreal.Transform(location=unreal.Vector(0,-2500,100));cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
e=gs.call_method('BeginDeferredActorSpawnFromClass',(w,cls,tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));gs.call_method('FinishSpawningActor',(e,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());s={'start':unreal.GameplayStatics.get_time_seconds(w),'last':-1,'samples':[],'handle':None}
def observe(dt,world=w,player=p,enemy=e,state=s,project=root):
 try:
  t=unreal.GameplayStatics.get_time_seconds(world)-state['start']
  if t-state['last']>.1:
   state['last']=t;v=enemy.get_velocity();speed=v.length();delta=enemy.get_actor_location()-player.get_actor_location();bb=enemy.get_controller().get_component_by_class(unreal.BlackboardComponent)
   state['samples'].append({'t':round(t,2),'distance':round(enemy.get_distance_to(player),1),'speed':round(speed,1),'facing_motion':round(enemy.get_actor_forward_vector().dot(v/speed),3) if speed>100 else None,'angle':round(math.degrees(math.atan2(delta.y,delta.x)),1),'attacking':enemy.get_editor_property('bAttackInProgress'),'orbit_goal':[bb.get_value_as_vector('OrbitLocation').x,bb.get_value_as_vector('OrbitLocation').y]})
  if t>=14:
   unreal.unregister_slate_post_tick_callback(state['handle']);enemy.destroy_actor();data=state['samples'];settled=[x for x in data if x['t']>3];moving=[x for x in settled if x['facing_motion'] is not None]
   result={'passed':min(x['distance'] for x in data)<240 and any(x['attacking'] for x in data) and len(moving)>10,'min_distance':min(x['distance'] for x in data),'settled_max_distance':max(x['distance'] for x in settled),'attacked':any(x['attacking'] for x in data),'forward_motion_fraction':round(sum(x['facing_motion']>0 for x in moving)/max(1,len(moving)),3),'samples':data}
   with open(os.path.join(project,'Intermediate/inspect/orbiter_refinement_assertions.json'),'w') as f:json.dump(result,f,indent=2)
   unreal.log('ORBITER_REFINEMENT_RESULT '+json.dumps({k:v for k,v in result.items() if k!='samples'}))
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle']);enemy.destroy_actor()
  with open(os.path.join(project,'Intermediate/inspect/orbiter_refinement_assertions.json'),'w') as f:json.dump({'passed':False,'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
