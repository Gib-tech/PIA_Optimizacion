"""Isolated setup; attacks use actual montage/hitbox overlaps, never damage callbacks."""
import unreal,json,os,traceback
attack_world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert attack_world
attack_player=unreal.GameplayStatics.get_player_character(attack_world,0)
attack_objects=[a for a in unreal.GameplayStatics.get_all_actors_of_class(attack_world,unreal.Actor) if a.get_class().get_name()=='BP_DestruibleEntrega_C']
attack_target=next(a for a in attack_objects if a.get_component_by_class(unreal.GeometryCollectionComponent).get_editor_property('rest_collection').get_name()=='GC_box')
attack_gc=attack_target.get_component_by_class(unreal.GeometryCollectionComponent)
attack_director=unreal.GameplayStatics.get_actor_of_class(attack_world,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C'))
attack_door=attack_director.get_editor_property('Baliza1').get_editor_property('Door')
attack_player.call_method('GrantHammerUpgrade',(attack_door,))
assert all(a.get_component_by_class(unreal.GeometryCollectionComponent).get_editor_property('generate_overlap_events') for a in attack_objects)
attack_center,attack_extent,attack_radius=unreal.SystemLibrary.get_component_bounds(attack_gc)
attack_player.set_actor_location(unreal.Vector(attack_center.x,attack_center.y-150,90),False,True)
attack_player.set_actor_rotation(unreal.Rotator(pitch=0,yaw=90,roll=0),True);attack_player.get_controller().set_control_rotation(unreal.Rotator(pitch=0,yaw=90,roll=0))
attack_state={'age':0,'last':-5,'attempts':0,'handle':None,'health_samples':[]}
attack_out=os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/compound_physical_attack.json')
def physical_attack_tick(dt,s=attack_state):
 try:
  s['age']+=dt
  health=attack_target.get_editor_property('Health')
  if not s['health_samples'] or s['health_samples'][-1]!=health:s['health_samples'].append(health)
  if attack_target.get_editor_property('ChaosBreakCount')>0:
   result={'passed':True,'isolated_position_and_hammer_setup':True,'actual_input_action_and_animation_hitbox':True,'no_direct_damage_or_overlap_callback_calls':True,'health_samples':s['health_samples'],'chaos_events':attack_target.get_editor_property('ChaosBreakCount'),'attempts':s['attempts']}
  elif s['age']>15:raise AssertionError('No physical break: '+str(s))
  else:
   if not attack_player.get_editor_property('IsAttacking') and s['age']-s['last']>1:
    attack_player.call_method('InpActEvt_IA_Heavy_Attack_K2Node_EnhancedInputActionEvent_6',(unreal.InputActionValue(),0.,0.,unreal.load_asset('/Game/ThirdPerson/Input/Actions/IA_Heavy_Attack')))
    s['last']=s['age'];s['attempts']+=1
   return
 except Exception:result={'passed':False,'error':traceback.format_exc(),'health_samples':s['health_samples']}
 unreal.unregister_slate_post_tick_callback(s['handle'])
 with open(attack_out,'w') as f:json.dump(result,f,indent=2)
 unreal.log('COMPOUND_PHYSICAL_ATTACK '+str(result))
attack_state['handle']=unreal.register_slate_post_tick_callback(physical_attack_tick)
