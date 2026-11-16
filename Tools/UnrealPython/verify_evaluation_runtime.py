"""PIE audit of loaded content and six real Chaos destructions using weapon binding."""
import unreal,os,json,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;R='/Game/ThirdPerson/Blueprints/Entrega/'
actors=gs.get_all_actors_of_class(w,unreal.Actor)
p=gs.get_player_pawn(w,0)
level=next(a for a in actors if isinstance(a,unreal.LevelScriptActor))
assert unreal.DeliveryBlueprintBuilder.is_partitioned(w)
meshes={};effects=set();collections=[];land=[];lightclasses=set()
for a in actors:
 for c in a.get_components_by_class(unreal.StaticMeshComponent):
  if c.static_mesh:meshes[c.static_mesh.get_path_name()]=True
 for c in a.get_components_by_class(unreal.SkeletalMeshComponent):
  if c.skeletal_mesh:meshes[c.skeletal_mesh.get_path_name()]=True
 for c in a.get_components_by_class(unreal.GeometryCollectionComponent):
  asset=c.get_editor_property('rest_collection')
  if asset:meshes[asset.get_path_name()]=True
 for c in a.get_components_by_class(unreal.NiagaraComponent):
  if c.get_asset():effects.add(c.get_asset().get_path_name())
 if isinstance(a,unreal.LandscapeProxy):land.append(a.get_name())
 for c in a.get_components_by_class(unreal.LightComponent):lightclasses.add(c.get_class().get_name())
 if a.get_class().get_name()=='BP_DestruibleEntrega_C':collections.append(a)
assert len(collections)==6 and land and len(meshes)>=15,(len(collections),land,len(meshes))
assert level.get_editor_property('Inicializado')
assert level.get_editor_property('Inicializaciones')==1 and level.get_editor_property('Sincronizaciones')>0
assert level.call_method('ConsultarAliados') is True
assert level.call_method('ConsultarSecuencia') is False
assert gs.get_viewport_mouse_capture_mode(w)==unreal.MouseCaptureMode.CAPTURE_PERMANENTLY_INCLUDING_INITIAL_MOUSE_DOWN
system=unreal.get_default_object(unreal.SystemLibrary.static_class())
state={'handle':None,'start':gs.get_time_seconds(w),'objects':collections,'result':{'partitioned_runtime':True,'landscape_proxies':land,'distinct_loaded_models':list(meshes),'light_types':sorted(lightclasses),'level_functions_macros_and_custom_events_active':True,'mouse_capture_mode':'permanent including initial mouse down','destructibles':[]}}
for a in collections:
 c=a.get_component_by_class(unreal.GeometryCollectionComponent)
 assert len(c.get_initial_local_rest_transforms())>1,a.get_name()
 system.call_method('SetBoolPropertyByName',(p,'IsAttacking',False))
 gs.apply_damage(a,25,None,p,None);assert a.get_editor_property('Health')==50
 # Exercise the player's real overlap binding. New attack resets its hit cache.
 for hit in range(2):
  system.call_method('SetBoolPropertyByName',(p,'IsAttacking',False));p.call_method('ReceiveTick',(.016,))
  system.call_method('SetBoolPropertyByName',(p,'IsAttacking',True));system.call_method('SetBoolPropertyByName',(p,'bLightAttackActive',False))
  p.call_method('BndEvt__BP_PlayerEntrega_HeavyOverlap__DelegateSignature',(p.get_editor_property('WeaponHitbox'),a,c,0,False,unreal.HitResult()))
  assert a.get_editor_property('Health')==(25 if hit==0 else 0),a.get_name()
 assert a.get_editor_property('bBroken')
system.call_method('SetBoolPropertyByName',(p,'IsAttacking',False))

def observe(dt,s=state,world=w):
 try:
  now=gs.get_time_seconds(world)
  if now-s['start']<2:return
  if not all(a.get_editor_property('ChaosBreakCount')>0 for a in s['objects']):
   assert now-s['start']<6,'Chaos did not break: '+str([(a.get_name(),a.get_editor_property('ChaosBreakCount')) for a in s['objects']])
   return
  for a in s['objects']:
   c=a.get_component_by_class(unreal.GeometryCollectionComponent)
   s['result']['destructibles'].append({'actor':a.get_name(),'asset':c.get_editor_property('rest_collection').get_path_name(),'pieces':len(c.get_initial_local_rest_transforms()),'chaos_break_events':a.get_editor_property('ChaosBreakCount'),'weapon_overlap_two_heavy_hits':True})
  s['result']['passed']=True
 except Exception:s['result'].update(passed=False,error=traceback.format_exc())
 unreal.unregister_slate_post_tick_callback(s['handle'])
 with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/evaluation_runtime_assertions.json'),'w') as f:json.dump(s['result'],f,indent=2)
 unreal.log('EVALUATION_RUNTIME_RESULT '+str(s['result']['passed']))
state['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('EVALUATION_RUNTIME_TEST_STARTED')
