import unreal,json,os
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world();assert w
gs=unreal.GameplayStatics;p=gs.get_player_character(w,0);pc=p.get_controller();R='/Game/ThirdPerson/Blueprints/Entrega/'
c=gs.get_actor_of_class(w,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))
if c.get_editor_property('bActive'):c.call_method('FinishCinema')
extra=gs.get_actor_of_class(w,unreal.load_class(None,R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C'))
actors={a.get_actor_label():a for a in gs.get_all_actors_of_class(w,unreal.Actor)};rows=[]
for label in ['Tecnico_Bruno','Consola_Bruno','Muestra_Botiquin','Muestra_Celda','Muestra_Credito']:
 a=actors[label];row={'label':label,'location':str(a.get_actor_location()),'components':[]}
 for comp in a.get_components_by_class(unreal.PrimitiveComponent):
  row['components'].append({'name':comp.get_name(),'collision':str(comp.get_collision_enabled()),'profile':str(comp.get_collision_profile_name()),'bounds':str(unreal.SystemLibrary.get_component_bounds(comp))})
 rows.append(row)
mesh=actors['Consola_Bruno'].static_mesh_component.get_editor_property('static_mesh');ss=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
unreal.log('TABLE_CONVEX '+str(ss.get_convex_collision_count(mesh)))
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/items-revision/runtime-before.json'),'w',encoding='utf-8') as f:json.dump(rows,f,ensure_ascii=False,indent=2)
unreal.log('ITEMS_RUNTIME_INSPECTED')
