import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs=unreal.GameplayStatics
for path,keys in [('/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C',['bActive','bInitialized','Kind','RevealEnemy']),('/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C',['bOrderRevealed','Paso','Zona3']),('/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone.BP_CombatZone_C',['bFinalStand','bRevelationStarted','CurrentWave','WaveCount','SpawnedCount']),('/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy.BP_BaseEnemy_C',['bIsDead','bFinalWordsPending','FinalPeersAlive'])]:
 for a in gs.get_all_actors_of_class(w,unreal.load_class(None,path)):
  unreal.log(str(a.get_name())+' '+str({k:str(a.get_editor_property(k)) for k in keys})+' owner='+str(a.get_owner()))
