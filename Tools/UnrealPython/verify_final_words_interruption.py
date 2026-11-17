"""Prepared defeat during the new nonterminal scene; verify outcome priority."""
import unreal,os,json,traceback
def main():
 gs=unreal.GameplayStatics;w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
 p=gs.get_player_character(w,0);pc=gs.get_player_controller(w,0)
 c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
 d=c.get_editor_property('Director');assert not c.get_editor_property('bActive')
 lib=unreal.get_default_object(gs.static_class());tr=unreal.Transform(location=p.get_actor_location()+unreal.Vector(200,0,0))
 speaker=lib.call_method('BeginDeferredActorSpawnFromClass',(w,unreal.load_class(None,'/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C'),tr,unreal.SpawnActorCollisionHandlingMethod.ALWAYS_SPAWN,None,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
 lib.call_method('FinishSpawningActor',(speaker,tr,unreal.SpawnActorScaleMethod.MULTIPLY_WITH_ROOT))
 sys=unreal.get_default_object(unreal.SystemLibrary)
 for o,k,v in [(speaker,'bIsDead',True),(speaker,'bFinalWordsPending',True),(d,'bOrderRevealed',False),(p,'bCanBeDamaged',True)]:sys.call_method('SetBoolPropertyByName',(o,k,v))
 speaker.get_controller().get_component_by_class(unreal.BrainComponent).stop_logic('Prepared interruption cue')
 c.call_method('StartRevelation',(speaker,));assert c.get_editor_property('bActive')
 s={'stage':0,'handle':None,'start':gs.get_time_seconds(w),'prepared_state_not_natural_playthrough':True}
 def watch(dt):
  try:
   if s['stage']==0:
    if gs.get_time_seconds(w)-s['start']<.3:return
    gs.apply_damage(p,1000,None,None,None);s['stage']=1;return
   elif s['stage']==1:
    if c.get_editor_property('Kind')!=1:
     assert gs.get_time_seconds(w)-s['start']<3;return
    assert c.get_editor_property('bActive') and c.get_editor_property('bOutcomeStarted')
    assert not d.get_editor_property('bNarrativePaused') and not d.get_editor_property('bOrderRevealed')
    assert not speaker.get_editor_property('bFinalWordsPending');s['stage']=2
   elif s['stage']==2:
    if c.get_editor_property('bActive'):return
    assert gs.is_game_paused(w) and d.get_editor_property('Paso')==5
    assert not c.get_editor_property('SequencePlayer').is_playing()
    s['passed']=True;finish()
  except Exception:s['passed']=False;s['error']=traceback.format_exc();finish()
 def finish():
  unreal.unregister_slate_post_tick_callback(s['handle'])
  with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/final-words/interruption.json'),'w') as f:json.dump({k:v for k,v in s.items() if k!='handle'},f,indent=2)
  unreal.log('FINAL_WORDS_INTERRUPTION_COMPLETE '+str(s))
 s['handle']=unreal.register_slate_post_tick_callback(watch)
main()
