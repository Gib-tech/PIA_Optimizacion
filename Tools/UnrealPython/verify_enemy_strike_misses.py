"""Isolated dodge/cancel regression. Calls the same strike event at its real montage time."""
import unreal,json,os,traceback
miss_world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();miss_gs=unreal.GameplayStatics
miss_player=miss_gs.get_player_character(miss_world,0);miss_hpc=miss_player.get_component_by_class(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health.BPC_Health_C'))
miss_player.set_actor_location(unreal.Vector(0,-2000,100),False,True)
miss_native=unreal.get_default_object(miss_gs.static_class());miss_tr=unreal.Transform(location=unreal.Vector(0,-2160,100));miss_cls=unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C')
miss_enemy=miss_native.call_method('BeginDeferredActorSpawnFromClass',(miss_world,miss_cls,miss_tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT));miss_native.call_method('FinishSpawningActor',(miss_enemy,miss_tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
miss_enemy.get_controller().get_component_by_class(unreal.BehaviorTreeComponent).stop_logic('Dodge and cancel isolation')
miss_enemy.call_method('Attack',(miss_player,));assert miss_enemy.get_editor_property('bAttackInProgress')
miss_state={'stage':0,'at':miss_gs.get_time_seconds(miss_world),'hp':miss_hpc.get_editor_property('Health'),'handle':None}
def miss_tick(dt,s=miss_state):
 try:
  age=miss_gs.get_time_seconds(miss_world)-s['at']
  if s['stage']==0 and age>.15:
   miss_player.set_actor_location(unreal.Vector(0,-1700,100),False,True);s['stage']=1
  elif s['stage']==1 and age>.45:
   miss_enemy.call_method('ResolveAttack');assert miss_enemy.get_editor_property('bAttackResolved');assert miss_hpc.get_editor_property('Health')==s['hp'];s['stage']=2
  elif s['stage']==2 and age>.85:
   miss_player.set_actor_location(unreal.Vector(0,-2000,100),False,True);miss_enemy.call_method('ResolveAttack');assert miss_hpc.get_editor_property('Health')==s['hp']
   miss_enemy.call_method('EndAttack');miss_enemy.call_method('Attack',(miss_player,));s.update(stage=3,at=miss_gs.get_time_seconds(miss_world))
  elif s['stage']==3 and age>.15:
   miss_enemy.call_method('EndAttack');s['stage']=4
  elif s['stage']==4 and age>.45:
   miss_enemy.call_method('ResolveAttack');assert miss_hpc.get_editor_property('Health')==s['hp']
   unreal.unregister_slate_post_tick_callback(s['handle']);miss_enemy.destroy_actor()
   with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/enemy_strike_misses.json'),'w') as f:json.dump({'passed':True,'dodge_consumes_impact':True,'return_after_window_causes_no_damage':True,'cancelled_montage_causes_no_damage':True,'health_unchanged':s['hp']},f,indent=2)
   unreal.log('ENEMY_DODGE_AND_CANCEL_PASSED')
 except Exception:
  unreal.unregister_slate_post_tick_callback(s['handle']);miss_enemy.destroy_actor()
  with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/enemy_strike_misses.json'),'w') as f:json.dump({'passed':False,'error':traceback.format_exc()},f,indent=2)
  unreal.log_error(traceback.format_exc())
miss_state['handle']=unreal.register_slate_post_tick_callback(miss_tick)
