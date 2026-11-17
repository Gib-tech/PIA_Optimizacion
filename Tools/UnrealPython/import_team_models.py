"""Import five reviewed models, retain atlas UVs, four real LODs and simple UCX."""
import unreal,os,json
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());source=os.path.join(root,'Tools/ArtSource/TeamModels')
rows=json.load(open(os.path.join(source,'manifest.json'),encoding='utf-8'));ART='/Game/ThirdPerson/Environment/TeamModels'
tools=unreal.AssetToolsHelpers.get_asset_tools();edit=unreal.MaterialEditingLibrary;sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
unreal.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
def constant(m,value,prop,y):
 node=edit.create_material_expression(m,unreal.MaterialExpressionConstant,-250,y);node.r=value;edit.connect_material_property(node,'',prop)
def vector(m,value,prop,y):
 node=edit.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-250,y);node.constant=unreal.LinearColor(*value,1);edit.connect_material_property(node,'',prop)
def texture(filename,normal=False):
 path=ART+'/Textures/'+filename[:-4];tex=unreal.load_asset(path)
 task=unreal.AssetImportTask();task.filename=os.path.join(source,filename);task.destination_path=ART+'/Textures';task.automated=True;task.save=True;task.replace_existing=True;tools.import_asset_tasks([task]);tex=unreal.load_asset(path)
 assert tex,path
 tex.set_editor_property('srgb',not normal);tex.set_editor_property('never_stream',False);tex.set_editor_property('max_texture_size',2048 if ('ArbolFab' in filename and '_1_' in filename) or 'AutoDestruido' in filename or 'Escombros' in filename else 1024)
 tex.set_editor_property('mip_gen_settings',unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP)
 if normal:
  tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP);tex.set_editor_property('flip_green_channel',True)
 unreal.EditorAssetLibrary.save_loaded_asset(tex,only_if_is_dirty=False);return tex
def material(row):
 path=ART+'/Materials/'+row['slot'];m=unreal.load_asset(path)
 if m:edit.delete_all_material_expressions(m)
 else:m=tools.create_asset(row['slot'],ART+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
 m.set_editor_property('two_sided',row['two_sided']);masked=row['masked']
 if masked:m.set_editor_property('blend_mode',unreal.BlendMode.BLEND_MASKED);m.set_editor_property('opacity_mask_clip_value',.45)
 if row['base_texture']:
  node=edit.create_material_expression(m,unreal.MaterialExpressionTextureSample,-500,0);node.texture=texture(row['base_texture']);node.sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_COLOR
  edit.connect_material_property(node,'RGB',unreal.MaterialProperty.MP_BASE_COLOR)
  if masked:edit.connect_material_property(node,'A',unreal.MaterialProperty.MP_OPACITY_MASK)
 else:vector(m,row['base'],unreal.MaterialProperty.MP_BASE_COLOR,0)
 if row['normal_texture']:
  node=edit.create_material_expression(m,unreal.MaterialExpressionTextureSample,-500,300);node.texture=texture(row['normal_texture'],True);node.sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL;edit.connect_material_property(node,'RGB',unreal.MaterialProperty.MP_NORMAL)
 constant(m,row['metallic'],unreal.MaterialProperty.MP_METALLIC,160);constant(m,max(row['roughness'],.75) if 'ArbolFab' in row['slot'] else row['roughness'],unreal.MaterialProperty.MP_ROUGHNESS,240)
 if row['slot'].startswith('M_Farol_') and row['original']=='Material.002':vector(m,[1400,750,250],unreal.MaterialProperty.MP_EMISSIVE_COLOR,420)
 edit.recompile_material(m);unreal.EditorAssetLibrary.save_loaded_asset(m,only_if_is_dirty=False);return m
proof_file=os.path.join(root,'Intermediate/inspect/team-models/import-proof.json')
selection_file=os.path.join(root,'Intermediate/inspect/team-models/import-selection.txt')
selected=set(open(selection_file,encoding='utf-8-sig').read().split()) if os.path.exists(selection_file) else None
proof=json.load(open(proof_file))['meshes'] if selected and os.path.exists(proof_file) else []
for row in rows:
 if selected is not None and row['name'] not in selected:continue
 options=unreal.FbxImportUI();options.automated_import_should_detect_type=False;options.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH;options.import_materials=False;options.import_textures=False
 options.static_mesh_import_data.combine_meshes=True;options.static_mesh_import_data.auto_generate_collision=False
 if row.get('nanite'):
  options.static_mesh_import_data.build_nanite=True
  options.static_mesh_import_data.normal_import_method=unreal.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS
 existing=unreal.load_asset(ART+'/'+row['mesh'])
 if existing and row.get('nanite'):
  # Remove inherited conventional reductions before importing the dense scan.
  if sm.get_lod_count(existing)!=1:
   one=unreal.StaticMeshReductionOptions();one.auto_compute_lod_screen_size=False;one.reduction_settings=[unreal.StaticMeshReductionSettings(percent_triangles=1,screen_size=1)];sm.set_lods(existing,one)
  ns=sm.get_nanite_settings(existing)
  if not ns.enabled:ns.enabled=True;ns.fallback_percent_triangles=.02;sm.set_nanite_settings(existing,ns)
 if existing and (row.get('texture_bake') or row.get('nanite')) and [str(s.material_slot_name) for s in existing.static_materials]!=[r['slot'] for r in row['materials']]:existing.set_editor_property('static_materials',[])
 task=unreal.AssetImportTask();task.filename=os.path.join(root,row['source_fbx']) if row.get('source_fbx') else os.path.join(source,row['mesh']+'.fbx');task.destination_path=ART;task.destination_name=row['mesh'];task.automated=True;task.save=True;task.options=options;task.replace_existing=True;tools.import_asset_tasks([task])
 mesh=unreal.load_asset(ART+'/'+row['mesh']);assert mesh,row['name']
 mats={r['slot']:material(r) for r in row['materials']}
 for i,slot in enumerate(mesh.static_materials):
  name=str(slot.material_slot_name);assert name in mats,(row['name'],name,list(mats))
  if slot.material_interface!=mats[name]:mesh.set_material(i,mats[name])
 if row.get('nanite'):
  assert sm.get_nanite_settings(mesh).enabled and sm.get_lod_count(mesh)==1
 else:
  settings=sm.get_nanite_settings(mesh);settings.enabled=False;sm.set_nanite_settings(mesh,settings)
  lods=unreal.StaticMeshReductionOptions();lods.auto_compute_lod_screen_size=False
  fractions=[1,.7,.4,.16] if row['name']=='ArbolFab' else [1,.55,.25,.08]
  lods.reduction_settings=[unreal.StaticMeshReductionSettings(percent_triangles=p,screen_size=s) for p,s in zip(fractions,[1,.48,.22,.08])]
  sm.set_lods(mesh,lods);assert sm.get_lod_count(mesh)==4
 body=mesh.get_editor_property('body_setup');assert body
 if body.get_editor_property('collision_trace_flag')!=unreal.CollisionTraceFlag.CTF_USE_DEFAULT:body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_DEFAULT)
 assert sm.get_convex_collision_count(mesh)>0,row['name']
 unreal.EditorAssetLibrary.set_metadata_tag(mesh,'TimeOut.Source',row['source']);unreal.EditorAssetLibrary.set_metadata_tag(mesh,'TimeOut.Author','danpetro (Fab, CC-BY)' if row['name']=='ArbolFab' else 'matousekfoto (CC-BY-4.0)' if row['name']=='Escombros' else 'Renafox (CC-BY-4.0)' if row['name']=='AutoDestruido' else 'Por confirmar por el equipo')
 unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
 geometry=[{'vertices':p.x,'triangles':p.y} for p in unreal.DeliveryBlueprintBuilder.get_lod_geometry(mesh)]
 assert row.get('nanite') or len(geometry)==4 and len({p['triangles'] for p in geometry})==4,geometry
 proof=[p for p in proof if p['name']!=row['name']]
 proof.append({'name':row['name'],'path':mesh.get_path_name(),'bounds':str(mesh.get_bounds()),'lods':geometry,'screen_sizes':list(sm.get_lod_screen_sizes(mesh)),'convex_collisions':sm.get_convex_collision_count(mesh),'nanite':row.get('nanite',False)})
 unreal.log('TEAM_MODEL_IMPORTED '+json.dumps(proof[-1]))
with open(os.path.join(root,'Intermediate/inspect/team-models/import-proof.json'),'w') as f:json.dump({'passed':True,'meshes':proof},f,indent=2)
unreal.log('TEAM_MODELS_IMPORT_COMPLETE')
