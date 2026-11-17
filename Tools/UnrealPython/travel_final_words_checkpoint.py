"""Prepared compatibility cases; never use these fixtures as a natural playthrough."""
import unreal,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
root=unreal.Paths.project_dir();mode=open(os.path.join(root,'Intermediate/inspect/final-words/checkpoint-mode.txt')).read().strip()
gs=unreal.GameplayStatics;data=gs.load_game_from_slot('TimeOut_Delivery_v1',0);assert data
sys=unreal.get_default_object(unreal.SystemLibrary)
def put(o,k,v):sys.call_method('Set'+('Bool' if isinstance(v,bool) else 'Int')+'PropertyByName',(o,k,v))
if mode.startswith('legacy'):
 put(data,'FinalStandRevision',0);put(data,'OrderRevealed',False)
 for k,v in [('Zone3Cleared',False),('Zone3Phase',0),('Zone3Wave',0),('Zone3Spawned',0)]:put(data,k,v)
 put(data,'Paso',1 if mode=='legacy-started' else 0)
 assert gs.save_game_to_slot(data,'TimeOut_Delivery_v1',0)
put(gs.get_game_instance(w),'bDeliveryContinue',True)
gs.set_game_paused(w,False)
gs.open_level(w,'/Game/ThirdPerson/Maps/Nivel_Entrega',True,'')
unreal.log('FINAL_WORDS_CHECKPOINT_TRAVEL '+mode)
