import unreal,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs=unreal.GameplayStatics
rows=[]
for x,y in [(0,-560),(300,-800),(0,-1000),(0,-1350),(900,-1100),(0,-1800),(0,-2800),(0,-5000),(0,-8000)]:
 point=unreal.NavigationSystemV1.project_point_to_navigation(w,unreal.Vector(x,y,20),None,None,unreal.Vector(100,100,200))
 rows.append({'input':[x,y],'projected':str(point)})
unreal.log('NAV_POINTS '+json.dumps(rows))
for a in gs.get_all_actors_of_class(w,unreal.Actor):
 if isinstance(a,(unreal.NavMeshBoundsVolume,unreal.RecastNavMesh)):
  unreal.log('NAV_ACTOR '+a.get_name()+' '+str(a.get_actor_bounds(False)))
