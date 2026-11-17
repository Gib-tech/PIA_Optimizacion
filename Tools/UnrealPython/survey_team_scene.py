"""Read-only map/asset survey before adding the team's scenery."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.project_dir();out=os.path.join(root,'Intermediate/inspect/team-models');os.makedirs(out,exist_ok=True)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors();rows=[]
for a in actors:
 label=a.get_actor_label()
 if label.startswith(('Compound_','Spawn_','Refugio','Zona_','Baliza','Puerta','Salida','LOD_','Destruible_')) or label in ['Landscape','Director_Entrega']:
  origin,extent=a.get_actor_bounds(False)
  rows.append({'label':label,'class':a.get_class().get_name(),'location':str(a.get_actor_location()),'center':str(origin),'extent':str(extent),'resident':not a.get_editor_property('is_spatially_loaded')})
trees=[]
for name in ['Tree1','Tree2','Tree3']:
 m=unreal.load_asset('/Game/ThirdPerson/RecursosPropios/Modelos/'+name)
 trees.append({'name':name,'bounds':str(m.get_bounds()),'source_files':list(m.get_editor_property('asset_import_data').extract_filenames()),'materials':[str(s.material_interface) for s in m.static_materials]})
with open(os.path.join(out,'scene-survey.json'),'w') as f:json.dump({'actors':rows,'trees':trees},f,indent=2)
unreal.log('TEAM_SCENE_SURVEY '+str(len(rows))+' actors '+str(trees))
