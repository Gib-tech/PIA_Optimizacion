"""Real ApplyDamage health delta, HUD pulse/retrigger/fade and healing negative control."""
import unreal,json,os,traceback
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
p=unreal.GameplayStatics.get_player_pawn(w,0);hud=unreal.GameplayStatics.get_player_controller(w,0).get_hud()
lib=unreal.get_default_object(unreal.SystemLibrary.static_class())
lib.call_method('SetBoolPropertyByName',(p,'bCanBeDamaged',True))
health=next(c for c in p.get_components_by_class(unreal.ActorComponent) if c.get_class().get_name()=='BPC_Health_C')
lib.call_method('SetDoublePropertyByName',(health,'Health',100.))
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
s={'stage':'baseline','since':unreal.GameplayStatics.get_real_time_seconds(w),'handle':None,'results':{}}
def observe(dt,world=w,player=p,ui=hud,hp=health,state=s,project=root,lib=lib):
 try:
  now=unreal.GameplayStatics.get_real_time_seconds(world);age=now-state['since'];until=ui.get_editor_property('HurtPulseUntil')
  if state['stage']=='baseline' and age>.3:
   unreal.GameplayStatics.apply_damage(player,6,None,None,None)
   assert hp.get_editor_property('Health')==94
   state.update(stage='hit',since=now)
  elif state['stage']=='hit' and until>now:
   duration=until-now;assert .2<duration<=.39,duration
   state['results']['duration_seconds']=round(duration,3)
   state['first_until']=until
   unreal.SystemLibrary.execute_console_command(world,'HighResShot 1280x720 filename="'+os.path.join(project,'docs/validation/damage-pulse-preview.png').replace('\\','/')+'"')
   state.update(stage='retrigger',since=now)
  elif state['stage']=='retrigger' and age>.16:
   unreal.GameplayStatics.apply_damage(player,6,None,None,None);state.update(stage='second',since=now)
  elif state['stage']=='second' and until>state['first_until']:
   assert hp.get_editor_property('Health')==88
   state['results']['second_hit_retriggers']=True;state.update(stage='fade',since=now,last_until=until)
  elif state['stage']=='fade' and age>.48:
   assert until<now
   state['results']['fades_to_zero']=True
   lib.call_method('SetDoublePropertyByName',(hp,'Health',95.));state.update(stage='heal',since=now)
  elif state['stage']=='heal' and age>.2:
   assert until==state['last_until'],'Healing caused a red pulse'
   state['results'].update(healing_does_not_trigger=True,passed=True)
   unreal.unregister_slate_post_tick_callback(state['handle'])
   with open(os.path.join(project,'Intermediate/inspect/damage_pulse_assertions.json'),'w') as f:json.dump(state['results'],f,indent=2)
   unreal.log('DAMAGE_PULSE_ASSERTIONS_PASSED '+json.dumps(state['results']));return
  assert age<4,'Pulse timeout '+state['stage']
 except Exception:
  unreal.unregister_slate_post_tick_callback(state['handle'])
  with open(os.path.join(project,'Intermediate/inspect/damage_pulse_assertions.json'),'w') as f:json.dump({'passed':False,'stage':state['stage'],'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
s['handle']=unreal.register_slate_post_tick_callback(observe)
unreal.log('DAMAGE_PULSE_OBSERVER_STARTED')
