"""Comprueba el sobreviviente con BT real: seguimiento, pose y pies, sin enemigos."""
import unreal,json,os,traceback,math
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0)
h=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'))
c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if c.get_editor_property('bActive'):c.call_method('FinishCinema')
p.set_actor_location(unreal.Vector(0,-800,100),False,True);h.set_actor_location(unreal.Vector(0,-1100,100),False,True)
initial_path=unreal.NavigationSystemV1.find_path_to_location_synchronously(w,h.get_actor_location(),p.get_actor_location(),h,None)
assert initial_path and initial_path.is_valid() and not initial_path.is_partial(),'La ubicación de prueba debe estar en una misma región navegable.'
brain=h.get_controller().get_component_by_class(unreal.BehaviorTreeComponent);brain.restart_logic()
bb=h.get_controller().get_component_by_class(unreal.BlackboardComponent)
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());out=os.path.join(root,'docs/validation/rehen-superviviente.json')
survivor_qa={'at':gs.get_time_seconds(w),'handle':None,'samples':[],'last':-1,'interacted':False}
def tick(dt,state=survivor_qa):
 try:
  now=gs.get_time_seconds(w);age=now-state['at']
  if not state['interacted'] and age>.3:h.call_method('Interactuar');state['interacted']=True
  if .5<age<3.5:
   p.add_movement_input(unreal.Vector(0,1,0),.4,False)
  if now-state['last']>.12:
   point=h.get_actor_location();foot=h.mesh.get_socket_transform('foot_l',unreal.RelativeTransformSpace.RTS_COMPONENT).translation
   state['samples'].append({'t':age,'speed':h.get_velocity().length(),'position':[point.x,point.y,point.z],'foot_local':[foot.x,foot.y,foot.z],'foot_world_z':h.mesh.get_socket_location('foot_l').z,'anim_valid':h.mesh.has_valid_animation_instance(),'following':bb.get_value_as_bool('bAccompanying')});state['last']=now
  if age<8:return
  moving=[r for r in state['samples'] if r['speed']>40]
  assert len(moving)>8,'El aliado no siguió con velocidad real'
  assert all(r['anim_valid'] for r in moving)
  assert max(r['position'][1] for r in moving)-min(r['position'][1] for r in moving)>150
  assert len({tuple(round(x,1) for x in r['foot_local']) for r in moving})>5,'Pose congelada mientras se desplaza'
  assert min(r['foot_world_z'] for r in moving)>-12,'Pies bajo el suelo'
  assert h.mesh.get_skeletal_mesh_asset().get_name()=='SK_RehenSuperviviente'
  report={'passed':True,'method':'PIE con posiciones iniciales preparadas y movimiento normal del jugador; Behavior Tree activo','mesh':h.mesh.get_skeletal_mesh_asset().get_path_name(),'anim_class':h.mesh.anim_class.get_path_name(),'samples':state['samples']}
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(out,'w',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
  unreal.log('SURVIVOR_LOCOMOTION_PASSED')
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(out,'w') as f:json.dump({'passed':False,'error':traceback.format_exc(),'samples':state['samples']},f,indent=2)
  unreal.log_error(traceback.format_exc())
survivor_qa['handle']=unreal.register_slate_post_tick_callback(tick)
