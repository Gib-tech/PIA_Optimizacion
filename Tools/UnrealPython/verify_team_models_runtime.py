"""Prepared visual/navigation fixture, without claiming a new natural playthrough."""
import unreal,os,json,traceback
def main():
 gs=unreal.GameplayStatics;w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
 pc=gs.get_player_controller(w,0);hero=gs.get_player_character(w,0);out=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/team-models');R='/Game/ThirdPerson/Blueprints/Entrega/'
 cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
 native=unreal.get_default_object(gs.static_class());tr=unreal.Transform();cam=native.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.CameraActor.static_class(),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));native.call_method('FinishSpawningActor',(cam,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));cam.get_component_by_class(unreal.CameraComponent).set_field_of_view(70)
 shots=[('skyline',(1100,-4400,700),(4000,-1900,1700)),('jardin',(3200,-3800,1700),(3200,-3800,0)),('auto',(3500,-3770,240),(3850,-3350,90)),('farol',(2450,-3750,200),(2200,-3260,230)),('escombros',(3500,-4300,220),(4000,-4150,55)),('arbol',(2000,-3900,150),(2550,-4175,340))]
 s={'stage':0,'index':0,'since':0,'handle':None,'busy':False,'paths':[],'photos':[],'prepared_fixture_not_natural_playthrough':True}
 def finish(error=None):
  unreal.unregister_slate_post_tick_callback(s['handle']);s['passed']=error is None
  if error:s['error']=error
  with open(os.path.join(out,'runtime.json'),'w') as f:json.dump({k:v for k,v in s.items() if k not in ['handle','busy']},f,indent=2)
  unreal.log('TEAM_MODELS_RUNTIME_COMPLETE '+str(s['passed'])+' '+str(error))
 def tick(dt):
  if s['busy']:return
  s['busy']=True
  try:
   now=gs.get_time_seconds(w)
   if s['stage']==0:
    if not cinema.get_editor_property('bInitialized'):s['busy']=False;return
    if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
    pc.get_hud().set_editor_property('show_hud',False);hero.get_editor_property('Health_Widget').set_visibility(unreal.SlateVisibility.HIDDEN);pc.set_view_target_with_blend(cam,0)
    s['stage']=1;s['since']=now
   elif s['stage']==1:
    if now-s['since']<2:s['busy']=False;return
    new=[a for a in gs.get_all_actors_of_class(w,unreal.StaticMeshActor) if a.get_actor_label().startswith('Equipo_')];assert len(new)==8,len(new)
    assert len({a.static_mesh_component.static_mesh.get_path_name() for a in new})==5
    for a in new:
     assert a.static_mesh_component.forced_lod_model==0
     assert a.static_mesh_component.get_collision_enabled()==unreal.CollisionEnabled.QUERY_AND_PHYSICS
    d=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DirectorEntrega.BP_DirectorEntrega_C'))
    assert d.get_editor_property('Zona3') and not d.get_editor_property('bOrderRevealed')
    h=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
    beacons=[d.get_editor_property('Baliza'+str(i)) for i in [1,2,3]]
    endpoints=[('rescate_arena',(0,-700,90),(0,-2700,90)),('deposito_refugio_norte',(-3200,-4800,90),(-2150,-4600,90)),('deposito_refugio_sur',(-3200,-4800,90),(-2150,-5500,90)),('guardia_spawn1',(0,-6700,90),(-350,-7700,90)),('guardia_spawn2',(0,-6700,90),(350,-7700,90)),('jardin_con_props',(2250,-3600,90),(3900,-3850,90))]
    for i,a in enumerate(beacons):
     for j,b in enumerate(beacons):
      if a!=b:
       av=a.get_editor_property('ApproachPoint').get_actor_location();bv=b.get_editor_property('ApproachPoint').get_actor_location();endpoints.append(('baliza_'+str(i)+str(j),(av.x,av.y,av.z),(bv.x,bv.y,bv.z)))
    for name,a,b in endpoints:
     path=unreal.NavigationSystemV1.find_path_to_location_synchronously(w,unreal.Vector(*a),unreal.Vector(*b),h,None)
     assert path and path.is_valid() and not path.is_partial(),name
     s['paths'].append({'route':name,'complete':True})
    s['five_new_designs_eight_instances']=True;s['stage']=2
   elif s['stage']==2:
    name,pos,target=shots[s['index']];cam.set_actor_location(unreal.Vector(*pos),False,True);cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(unreal.Vector(*pos),unreal.Vector(*target)),True);s['since']=now;s['stage']=3
   elif s['stage']==3:
    if now-s['since']<.6:s['busy']=False;return
    name=shots[s['index']][0];unreal.AutomationLibrary.take_high_res_screenshot(1280,720,os.path.join(out,'scene-'+name+'.png'));s['photos'].append(name);s['since']=now;s['stage']=4
   elif s['stage']==4:
    if now-s['since']<.3:s['busy']=False;return
    s['index']+=1
    if s['index']==len(shots):finish();return
    s['stage']=2
   s['busy']=False
  except Exception:finish(traceback.format_exc())
 s['handle']=unreal.register_slate_post_tick_callback(tick)
 unreal.log('TEAM_MODELS_RUNTIME_STARTED')
main()
