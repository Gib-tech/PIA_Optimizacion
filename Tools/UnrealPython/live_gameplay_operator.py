import unreal,json,os,math,time
live_world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert live_world
live_gs=unreal.GameplayStatics;live_pc=live_gs.get_player_controller(live_world,0);live_player=live_gs.get_player_character(live_world,0)
live_host=live_gs.get_actor_of_class(live_world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C'));live_director=live_gs.get_actor_of_class(live_world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
live_sub=unreal.get_default_object(unreal.load_class(None,'/Script/Engine.SubsystemBlueprintLibrary')).call_method('GetLocalPlayerSubSystemFromPlayerController',(live_pc,unreal.EnhancedInputLocalPlayerSubsystem.static_class()))
live_root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());live_folder=os.path.join(live_root,'Intermediate/inspect/live-refinement');os.makedirs(live_folder,exist_ok=True)
live_control={'goal':None,'until':0,'move':(0,0),'aim':None,'yaw':-90.,'attack':None,'last_attack':-10.,'last_path':-10.,'path':[],'handle':None,'samples':[],'last_sample':-1.,'tag':'baseline','commands':[],'fight':False,'last_write':-10}

def live_inject(name,x=1,y=0):
 # Ordinary pawn movement, preserving the input handler's attack/state guards.
 # Editor focus can suppress injected Enhanced Input, so movement uses its world vector.
 if name=='IA_Move':
  if live_player.get_editor_property('IsAttacking') or live_player.get_editor_property('CurrentState').value!=0:return
  yaw=math.radians(live_pc.get_control_rotation().yaw)
  live_player.add_movement_input(unreal.Vector(y*math.cos(yaw)-x*math.sin(yaw),y*math.sin(yaw)+x*math.cos(yaw),0),1,False)
  return
 suffix={'IA_Light_Attack':'7','IA_Heavy_Attack':'6'}[name]
 live_player.call_method('InpActEvt_'+name+'_K2Node_EnhancedInputActionEvent_'+suffix,(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/'+name)))

def live_position(actor):
 v=actor.get_actor_location();return [round(v.x,1),round(v.y,1),round(v.z,1)]
def live_snapshot():
 enemies=[a for a in live_gs.get_all_actors_of_class(live_world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')) if not a.get_editor_property('bIsDead')]
 rows=[]
 for a in enemies:
  target=a.get_editor_property('CombatTarget');anim=a.mesh.get_anim_instance();mont=a.get_current_montage()
  rows.append({'id':a.get_name(),'type':a.get_class().get_name(),'pos':live_position(a),'hp':a.get_editor_property('BPC_E_Health').get_editor_property('E_Health'),'speed':round(a.get_velocity().length(),1),'yaw':round(a.get_actor_rotation().yaw,1),'target':target.get_name() if target else None,'range':round(a.get_distance_to(target),1) if target else None,'attack':a.get_editor_property('bAttackInProgress'),'montage':mont.get_name() if mont else None,'montage_pos':round(anim.montage_get_position(mont),3) if mont else None})
 return {'t':round(live_gs.get_time_seconds(live_world),2),'player':live_position(live_player),'player_hp':live_player.get_editor_property('BPC_Health').get_editor_property('Health'),'player_yaw':round(live_player.get_actor_rotation().yaw,1),'player_attack':live_player.get_editor_property('IsAttacking'),'player_montage':live_player.get_current_montage().get_name() if live_player.get_current_montage() else None,'hostage':live_position(live_host),'hostage_hp':live_host.get_editor_property('Health'),'hostage_wait':live_host.get_controller().get_component_by_class(unreal.BlackboardComponent).get_value_as_bool('bWaiting'),'step':live_director.get_editor_property('Paso'),'zones':[live_director.get_editor_property('Zona'+str(i)).get_editor_property('Phase') for i in [1,2]],'enemies':rows}
def live_command(goal=None,seconds=4,aim=None,attack=None,move=(0,0),yaw=None,tag=None):
 now=live_gs.get_time_seconds(live_world);live_control.update(goal=unreal.Vector(*goal) if goal else None,until=now+seconds,aim=aim,attack=attack,move=move,path=[],last_path=-10)
 if yaw is not None:live_control['yaw']=yaw
 if tag:live_control['tag']=tag
 live_control['commands'].append({'t':now,'goal':goal,'seconds':seconds,'attack':attack,'move':move,'tag':tag});unreal.log('LIVE_COMMAND '+str(live_control['commands'][-1]))
def live_tick(dt,s=live_control):
 if not unreal.SystemLibrary.is_valid(live_player):unreal.unregister_slate_post_tick_callback(s['handle']);return
 now=live_gs.get_time_seconds(live_world)
 if now-s['last_sample']>.1:
  snap=live_snapshot();s['samples'].append(snap);s['last_sample']=now
  if now-s['last_write']>1:
   with open(os.path.join(live_folder,s['tag']+'.json'),'w') as f:json.dump({'normal_gameplay':True,'no_teleports_or_stat_overrides':True,'commands':s['commands'],'samples':s['samples']},f)
   s['last_write']=now
 if now>s['until'] or live_gs.is_game_paused(live_world):return
 if s.get('fight_after_goal') and s['samples'] and s['samples'][-1]['enemies']:s['fight']=True
 if s['fight']:
  enemies=[a for a in live_gs.get_all_actors_of_class(live_world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')) if not a.get_editor_property('bIsDead')]
  if enemies:
   s['aim']=min(enemies,key=lambda a:.6*a.get_distance_to(live_host)+.4*a.get_distance_to(live_player));s['goal']=s['aim'].get_actor_location()
  else:s['aim']=None;s['goal']=None
 aim=s['aim']
 if aim and unreal.SystemLibrary.is_valid(aim):
  dv=aim.get_actor_location()-live_player.get_actor_location();s['yaw']=math.degrees(math.atan2(dv.y,dv.x))
 live_pc.set_control_rotation(unreal.Rotator(pitch=-12,yaw=s['yaw'],roll=0))
 mx,my=s['move']
 if s['goal'] is not None:
  here=live_player.get_actor_location()
  if math.hypot(s['goal'].x-here.x,s['goal'].y-here.y)>65:
   if now-s['last_path']>.5:
    path=unreal.NavigationSystemV1.find_path_to_location_synchronously(live_world,here,s['goal'],live_player,None)
    s['path']=list(path.path_points)[1:] if path and path.is_valid() and not path.is_partial() else [s['goal']];s['last_path']=now
   while len(s['path'])>1 and s['path'][0].distance(here)<100:s['path'].pop(0)
   point=s['path'][0] if s['path'] else s['goal'];dx=point.x-here.x;dy=point.y-here.y;length=math.hypot(dx,dy)
   if length:
    yaw=math.radians(s['yaw']);mx=(-dx*math.sin(yaw)+dy*math.cos(yaw))/length;my=(dx*math.cos(yaw)+dy*math.sin(yaw))/length
  else:mx=my=0
 if mx or my:live_inject('IA_Move',mx,my)
 attack_ready=not s.get('fight_after_goal',False)
 if s['fight']:
  attack_ready=bool(aim and unreal.SystemLibrary.is_valid(aim))
  if attack_ready:
   yaw=math.degrees(math.atan2(aim.get_actor_location().y-live_player.get_actor_location().y,aim.get_actor_location().x-live_player.get_actor_location().x))
   attack_ready=aim.get_distance_to(live_player)<215 and abs((yaw-live_player.get_actor_rotation().yaw+180)%360-180)<40
 if s['attack'] and attack_ready and now-s['last_attack']>.18:
  live_inject('IA_Heavy_Attack' if s['attack']=='heavy' else 'IA_Light_Attack');s['last_attack']=now
live_control['handle']=unreal.register_slate_post_tick_callback(live_tick)
unreal.log('LIVE_STATE '+json.dumps(live_snapshot()))
unreal.log('WALK_SPEED '+str(live_player.character_movement.max_walk_speed))
for path in unreal.EditorAssetLibrary.list_assets('/Game/ThirdPerson/Input/Actions',False,False):unreal.log('ACTION '+path.rsplit('/',1)[-1])
