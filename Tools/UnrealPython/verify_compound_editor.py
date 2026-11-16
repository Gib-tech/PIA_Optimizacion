import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
walls=[a for a in actors if a.get_actor_label().startswith('Compound_SM_Walls_')]
assert len(walls)==10
report={'buildings':[],'props':[]}
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
for a in walls:
 c=a.static_mesh_component;b=c.static_mesh.get_bounds();height=b.box_extent.z*2
 assert 390<height<410,(a.get_actor_label(),height)
 assert sm.get_nanite_settings(c.static_mesh).enabled
 report['buildings'].append({'label':a.get_actor_label(),'height':height,'nanite':True,'draw_distance':c.get_editor_property('ld_max_draw_distance')})
for a in actors:
 if a.get_actor_label().startswith(('LOD_','Destruible_')):
  c=a.get_component_by_class(unreal.GeometryCollectionComponent if a.get_actor_label().startswith('Destruible_') else unreal.StaticMeshComponent)
  center,extent,r=unreal.SystemLibrary.get_component_bounds(c)
  assert abs(center.z-extent.z)<3,(a.get_actor_label(),center.z-extent.z)
  assert c.get_editor_property('ld_max_draw_distance') ==0
  report['props'].append({'label':a.get_actor_label(),'center':[center.x,center.y,center.z],'base_z':center.z-extent.z,'draw_distance':c.get_editor_property('ld_max_draw_distance')})
 if isinstance(a,unreal.LandscapeProxy):assert a.get_editor_property('landscape_material').get_name()=='M_TerrenoRecorrido'
 if isinstance(a,unreal.SkyLight):assert not a.light_component.get_editor_property('real_time_capture')
report['passed']=True
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/compound_editor.json'),'w') as f:json.dump(report,f,indent=2)
unreal.log('COMPOUND_EDITOR_GEOMETRY_AND_CULLING_PASSED')
