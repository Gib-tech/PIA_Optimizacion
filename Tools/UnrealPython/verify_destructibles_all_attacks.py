"""Matriz PIE: seis colecciones por ataque, con entrada, montaje y contacto reales."""
import unreal,os,json,time,traceback,math
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller();R='/Game/ThirdPerson/Blueprints/Entrega/'
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());folder=os.path.join(root,'docs/validation/ciclo-luces-ataques');os.makedirs(folder,exist_ok=True)
mode=json.load(open(os.path.join(root,'Intermediate/inspect/daynight-attacks/test-mode.json')))['mode']
assert mode in ['espada_ligero','espada_pesado','martillo_ligero','martillo_pesado','pulso']
cinema=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
syslib=unreal.get_default_object(unreal.SystemLibrary)
syslib.call_method('SetIntPropertyByName',(extra,'Cargas',30))
objects=sorted(gs.get_all_actors_of_class(w,unreal.load_class(None,R+'BP_DestruibleEntrega.BP_DestruibleEntrega_C')),key=lambda a:a.get_editor_property('NombreDestruible'))
assert len(objects)==6
unreal.SystemLibrary.execute_console_command(w,'t.MaxFPS 60')
state={'i':0,'phase':0,'at':time.monotonic(),'last':0,'handle':None,'rows':[],'hp':[],'attempts':0,'montages':set()}
def prop(key,value,kind='Bool',obj=p):syslib.call_method('Set'+kind+'PropertyByName',(obj,key,value))
# Equip flags use the same hitbox reattachment and real attack selection in Tick.
# Fixture only: the mission upgrade is deliberately false throughout this matrix.
prop('bHammerUpgraded',False);prop('bIsHammerEquipped',mode.startswith('martillo'));prop('bIsSwordEquipped',not mode.startswith('martillo'))
def save(result):
 with open(os.path.join(folder,'destruibles-'+mode+'.json'),'w',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
def tick(dt,s=state):
 try:
  now=time.monotonic()
  if s['i']==len(objects):
   unreal.unregister_slate_post_tick_callback(s['handle'])
   save({'passed':True,'attack':mode,'method':'PIE: posiciones y equipamiento preparados, sin mejora del martillo. Recolocación entre swings por root motion. Entrada Enhanced Input para melee y evento normal del pulso; montajes, ventanas, overlap y barrido del gameplay reales. Nunca ApplyDamage ni callbacks de contacto a mano.','objects':s['rows']});unreal.log('ALL_DESTRUCTIBLES_ATTACK_PASSED '+mode);return
  a=objects[s['i']]
  if s['phase']==0:
   center,extent,_=unreal.SystemLibrary.get_component_bounds(a.get_editor_property('Colision'))
   # Elegir una cara visible: el lado sur de la fuente queda tras un muro.
   # No acreditar un fallo de oclusión correcta como fallo del arma.
   candidates=[unreal.Vector(center.x,center.y-extent.y-120,95),unreal.Vector(center.x-extent.x-120,center.y,95),unreal.Vector(center.x,center.y+extent.y+120,95),unreal.Vector(center.x+extent.x+120,center.y,95)]
   for candidate in candidates:
    ray=unreal.SystemLibrary.line_trace_single(w,candidate+unreal.Vector(0,0,64),center,unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[p],unreal.DrawDebugTrace.NONE)
    if ray and unreal.get_default_object(gs).call_method('BreakHitResult',(ray,))[9]==a:break
   else:raise AssertionError('Ninguna cara accesible de '+a.get_actor_label())
   s['position']=candidate;s['yaw']=math.degrees(math.atan2(center.y-candidate.y,center.x-candidate.x))
   p.set_actor_location(s['position'],False,True);p.set_actor_rotation(unreal.Rotator(yaw=s['yaw']),False);pc.set_control_rotation(unreal.Rotator(yaw=s['yaw']));pc.set_view_target_with_blend(p,0)
   if mode=='pulso':
    prop('CamaraPrimera',True);p.get_editor_property('TPC').deactivate();p.get_editor_property('FPC').activate()
    eye=p.get_editor_property('FPC').get_world_location();pc.set_control_rotation(unreal.MathLibrary.find_look_at_rotation(eye,center))
   gc=a.get_component_by_class(unreal.GeometryCollectionComponent)
   s.update(phase=1,at=now,last=0,hp=[a.get_editor_property('Health')],attempts=0,montages=set(),row={'label':a.get_actor_label(),'collection':gc.get_editor_property('rest_collection').get_path_name(),'initial_health':a.get_editor_property('Health')});return
  if s['phase']==2:
   if not p.get_editor_property('IsAttacking') and not p.get_current_montage():s['i']+=1;s['phase']=0
   return
  hp=a.get_editor_property('Health')
  if hp!=s['hp'][-1]:s['hp'].append(hp)
  montage=p.get_current_montage()
  if montage:s['montages'].add(montage.get_name())
  if a.get_editor_property('ChaosBreakCount')>0:
   assert a.get_editor_property('bBroken') and hp==0
   row=s['row'];row.update(health_samples=s['hp'],chaos_break_events=a.get_editor_property('ChaosBreakCount'),attack_attempts=s['attempts'],montages=sorted(s['montages']),hammer_upgraded=p.get_editor_property('bHammerUpgraded'))
   if mode!='pulso':assert row['montages'],row
   s['rows'].append(row);s['phase']=2;return
  assert now-s['at']<35,(mode,a.get_actor_label(),s['hp'],s['attempts'],str(p.get_editor_property('CurrentState')),str(p.get_editor_property('WeaponHitbox').get_collision_enabled()))
  if now-s['at']>.8 and not p.get_editor_property('IsAttacking') and not p.get_current_montage() and now-s['last']>1.0:
   # Los montajes pesados desplazan al personaje. Recolocar entre golpes
   # mantiene la condición de alcance del fixture sin alterar el montaje.
   p.set_actor_location(s['position'],False,True);p.set_actor_rotation(unreal.Rotator(yaw=s['yaw']),False)
   if mode=='pulso':extra.call_method('DispararPulso')
   else:
    action='IA_Light_Attack' if mode.endswith('ligero') else 'IA_Heavy_Attack';suffix='7' if mode.endswith('ligero') else '6'
    p.call_method('InpActEvt_'+action+'_K2Node_EnhancedInputActionEvent_'+suffix,(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/'+action)))
   s['last']=now;s['attempts']+=1
 except Exception:
  unreal.unregister_slate_post_tick_callback(s['handle']);save({'passed':False,'attack':mode,'object_index':s['i'],'rows':s['rows'],'health':s['hp'],'error':traceback.format_exc()});unreal.log_error(traceback.format_exc())
state['handle']=unreal.register_slate_post_tick_callback(tick)
