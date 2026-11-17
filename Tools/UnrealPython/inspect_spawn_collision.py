import unreal,json
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();gs=unreal.GameplayStatics
starts=gs.get_all_actors_of_class(w,unreal.PlayerStart);unreal.log('STARTS '+str(starts))
for a in gs.get_all_actors_of_class(w,unreal.Actor):
 if any(t in a.get_name() for t in ['Suministro','StaticMeshActor','PlayerStart']):
  for c in a.get_components_by_class(unreal.StaticMeshComponent):
   m=c.static_mesh
   if m and '/Complementos/' in m.get_path_name():unreal.log('SUPPORT_BOUNDS '+a.get_name()+' '+str(unreal.SystemLibrary.get_component_bounds(c))+' '+str(c.get_collision_enabled()))
