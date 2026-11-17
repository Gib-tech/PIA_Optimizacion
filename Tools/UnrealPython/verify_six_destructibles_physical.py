"""Seis tipos de Chaos con ataques animados; nunca llama daño/overlap directo."""
import unreal,os,json,time,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller();R='/Game/ThirdPerson/Blueprints/Entrega/'
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
objects=gs.get_all_actors_of_class(w,unreal.load_class(None,R+'BP_DestruibleEntrega.BP_DestruibleEntrega_C'));assert len(objects)==6,len(objects)
assert len({a.get_component_by_class(unreal.GeometryCollectionComponent).get_editor_property('rest_collection').get_path_name() for a in objects})==6
objects=sorted(objects,key=lambda a:a.get_editor_property('NombreDestruible'));director=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_DirectorEntrega.BP_DirectorEntrega_C'));p.call_method('GrantHammerUpgrade',(director.get_editor_property('Baliza1').get_editor_property('Door'),))
folder=os.path.join(unreal.Paths.project_dir(),'docs/validation/items-colisiones');os.makedirs(folder,exist_ok=True)
s={'i':0,'phase':0,'at':time.monotonic(),'last':0,'handle':None,'rows':[],'hp':[],'attempts':0}
def tick(dt,state=s):
 try:
  now=time.monotonic()
  if state['i']==len(objects):
   result={'passed':True,'required_distinct_types':6,'tested_distinct_collections':6,'method':'PIE. Posición ante cada objeto y mejora del martillo preparadas. Entradas Enhanced Input, montajes y solapamiento físico real. Sin ApplyDamage ni invocación de callbacks de overlap.','objects':state['rows']}
   unreal.unregister_slate_post_tick_callback(state['handle'])
   with open(os.path.join(folder,'seis-destruibles.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
   unreal.log('SIX_DESTRUCTIBLES_PHYSICAL_PASSED');return
  a=objects[state['i']]
  if state['phase']==0:
   gc=a.get_component_by_class(unreal.GeometryCollectionComponent);center,extent,_=unreal.SystemLibrary.get_component_bounds(a.get_editor_property('Colision'))
   p.set_actor_location(unreal.Vector(center.x,center.y-extent.y-95,95),False,True);p.set_actor_rotation(unreal.Rotator(yaw=90),False);pc.set_control_rotation(unreal.Rotator(yaw=90))
   state.update(phase=1,at=now,last=0,hp=[a.get_editor_property('Health')],attempts=0,row={'label':a.get_actor_label(),'name':a.get_editor_property('NombreDestruible'),'collection':gc.get_editor_property('rest_collection').get_path_name(),'proxy_center_cm':[center.x,center.y,center.z],'initial_piece_count':len(gc.get_initial_local_rest_transforms())});return
  hp=a.get_editor_property('Health')
  if state['hp'][-1]!=hp:state['hp'].append(hp)
  if a.get_editor_property('ChaosBreakCount')>0:
   assert a.get_editor_property('bBroken') and hp==0
   row=state['row'];row.update(health_samples=state['hp'],chaos_break_events=a.get_editor_property('ChaosBreakCount'),heavy_attack_attempts=state['attempts']);state['rows'].append(row);state['i']+=1;state['phase']=0;return
  assert now-state['at']<18,(a.get_actor_label(),state['hp'],state['attempts'])
  if now-state['at']>.6 and not p.get_editor_property('IsAttacking') and now-state['last']>1:
   p.call_method('InpActEvt_IA_Heavy_Attack_K2Node_EnhancedInputActionEvent_6',(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_Heavy_Attack')));state['last']=now;state['attempts']+=1
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(os.path.join(folder,'seis-destruibles.json'),'w',encoding='utf-8') as f:json.dump({'passed':False,'object_index':state['i'],'rows':state['rows'],'hp':state['hp'],'error':traceback.format_exc()},f,ensure_ascii=False,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(tick)
