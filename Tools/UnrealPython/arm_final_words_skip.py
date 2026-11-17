"""Prepared cue, followed by a physical Space press in PIE; no gameplay completion claim."""
import unreal,os,json,traceback
def main():
 gs=unreal.GameplayStatics;w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
 pc=gs.get_player_controller(w,0);p=gs.get_player_character(w,0)
 c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
 assert not c.get_editor_property('bActive')
 path='/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C'
 lib=unreal.get_default_object(gs.static_class());tr=unreal.Transform(location=p.get_actor_location()+unreal.Vector(200,0,0))
 speaker=lib.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.load_class(None,path),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
 lib.call_method('FinishSpawningActor',(speaker,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
 sys=unreal.get_default_object(unreal.SystemLibrary)
 for k in ['bIsDead','bFinalWordsPending']:sys.call_method('SetBoolPropertyByName',(speaker,k,True))
 speaker.get_controller().get_component_by_class(unreal.BrainComponent).stop_logic('Prepared presentation cue')
 c.call_method('StartRevelation',(speaker,));assert c.get_editor_property('bActive')
 s={'handle':None}
 def watch(dt):
  if c.get_editor_property('bActive'):return
  unreal.unregister_slate_post_tick_callback(s['handle'])
  try:
   age=gs.get_time_seconds(w)-c.get_editor_property('StartedAt');assert age<11.5,'Expected physical skip before natural end'
   d=c.get_editor_property('Director');assert d.get_editor_property('bOrderRevealed') and not d.get_editor_property('bNarrativePaused')
   assert not gs.is_game_paused(w) and pc.get_view_target()==p
   assert not pc.is_move_input_ignored() and not pc.is_look_input_ignored()
   result={'passed':True,'physical_space_skip':True,'age':age,'order_revealed_and_input_restored':True,'prepared_state_not_natural_playthrough':True}
  except Exception:result={'passed':False,'error':traceback.format_exc()}
  with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/final-words/physical-skip.json'),'w') as f:json.dump(result,f,indent=2)
  unreal.log('FINAL_WORDS_PHYSICAL_SKIP_COMPLETE '+str(result))
 s['handle']=unreal.register_slate_post_tick_callback(watch)
 unreal.log('FINAL_WORDS_PHYSICAL_SKIP_ARMED')
main()
