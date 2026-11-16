"""Place team's real assets, five automatic four-LOD models, local lights and FX."""
import unreal,os,json
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/';ART='/Game/ThirdPerson/Environment/Evaluation'
tools=unreal.AssetToolsHelpers.get_asset_tools();lib=unreal.BlueprintEditorLibrary
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bp=unreal.load_asset(R+'BP_DestruibleEntrega')
if not bp:bp=tools.duplicate_asset('BP_DestruibleEntrega',R.rstrip('/'),unreal.load_asset('/Game/ThirdPerson/Bp_Modelos/BP_DestruiblePick'))
for name,kind in {'Health':'real','bBroken':'bool','ChaosBreakCount':'int','BreakFX':'/Script/Niagara.NiagaraSystem'}.items():
 try:unreal.get_default_object(bp.generated_class()).get_editor_property(name);continue
 except Exception:pass
 typ=lib.get_object_reference_type(unreal.load_class(None,kind)) if kind.startswith('/') else lib.get_basic_type_by_name(kind)
 assert lib.add_member_variable(bp,name,typ)
 lib.set_blueprint_variable_instance_editable(bp,name,True)
lib.compile_blueprint(bp);unreal.get_default_object(bp.generated_class()).set_editor_property('Health',50.0);unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
placed={a.get_actor_label():a for a in sub.get_all_level_actors()}

def actor(label,cls,pos):
 a=placed.get(label)
 if not a:a=sub.spawn_actor_from_class(cls,unreal.Vector(*pos));placed[label]=a
 a.set_actor_label(label);a.set_folder_path('Evaluacion/RecursosEquipo');return a

def fit(a,c,pos,height,bounds):
 # Normalize imported units/pivots without changing the source mesh.
 lo,hi=(bounds.min,bounds.max) if isinstance(bounds,unreal.Box) else bounds
 scale=height/max(hi.z-lo.z,1)
 a.set_actor_scale3d(unreal.Vector(scale,scale,scale))
 center=(lo+hi)*.5
 a.set_actor_location(unreal.Vector(pos[0]-center.x*scale,pos[1]-center.y*scale,pos[2]-lo.z*scale),False,True)
 c.set_collision_profile_name('BlockAllDynamic');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA,unreal.CollisionResponseType.ECR_IGNORE)

collections=[
 ('Caja','Box/GC_box',(1100,-1200,0),90),
 ('Basurero','Basura/GC_Trash',(-1100,-2000,0),100),
 ('Banca','Banca/GC_Banco',(-800,-3300,0),90),
 ('Barril','Barril/Barril_Barril/GC_Barril',(-3900,-5600,0),110),
 ('Auto','Carro/GC_Car2',(-4200,-7400,0),160),
 ('Fuente','Fuente/GC_fuente',(1400,-7600,0),160)]
for name,relative,pos,height in collections:
 a=actor('Destruible_'+name,bp.generated_class(),pos);gc=a.get_component_by_class(unreal.GeometryCollectionComponent)
 asset=unreal.load_asset('/Game/ThirdPerson/RecursosPropios/Modelos/'+relative);assert asset,relative
 gc.set_rest_collection(asset,True);gc.set_notify_breaks(True)
 gc.set_editor_property('generate_overlap_events',True)
 gc.set_editor_property('damage_threshold',[500000,50000,5000])
 fit(a,gc,pos,height,gc.get_local_bounds())
 a.set_editor_property('BreakFX',unreal.load_asset('/Game/ThirdPerson/RecursosPropios/Particulas/NS_Explocion' if name=='Barril' else '/Game/NS/Chispas_impacto/NS_ChispaImpacto'))
 a.get_editor_property('Colision').set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)

lods=[]
for name,pos,height in [('Banco',(900,-1900,0),90),('Car',(-4300,-4700,0),160),('Tree1',(-4400,-7900,0),450),('Light_Pole',(3900,-7800,0),400),('fuente',(0,-7300,0),160)]:
 source=unreal.load_asset('/Game/ThirdPerson/RecursosPropios/Modelos/'+name);assert source,name
 path=ART+'/SM_LOD_'+name;mesh=unreal.load_asset(path)
 if not mesh:mesh=tools.duplicate_asset('SM_LOD_'+name,ART,source)
 settings=unreal.StaticMeshReductionOptions();settings.auto_compute_lod_screen_size=False
 settings.reduction_settings=[unreal.StaticMeshReductionSettings(percent_triangles=p,screen_size=s) for p,s in [(1,1),(.55,.45),(.25,.20),(.08,.07)]]
 if sm.get_lod_count(mesh)!=4:sm.set_lods(mesh,settings)
 assert sm.get_lod_count(mesh)==4,name
 unreal.EditorAssetLibrary.save_loaded_asset(mesh)
 a=actor('LOD_'+name,unreal.StaticMeshActor,pos);c=a.static_mesh_component;c.set_static_mesh(mesh)
 bounds=mesh.get_bounds();fit(a,c,pos,height,(bounds.origin-bounds.box_extent,bounds.origin+bounds.box_extent))
 c.set_editor_properties({'ld_max_draw_distance':0.0,'never_distance_cull':True})
 lods.append({'asset':path,'source':source.get_path_name(),'position':pos,'lods':sm.get_lod_count(mesh),'screen_sizes':list(sm.get_lod_screen_sizes(mesh))})

for name,cls,pos,radius,power in [('Puntual_Rescate',unreal.PointLight,(900,-900,220),650,900),('Foco_Puerta1',unreal.SpotLight,(0,-3700,300),900,1800),('Rect_Patio',unreal.RectLight,(0,-8400,300),1000,1200)]:
 a=actor('Luz_'+name,cls,pos);c=a.light_component;c.set_mobility(unreal.ComponentMobility.MOVABLE)
 c.set_editor_property('attenuation_radius',radius);c.set_intensity(power);c.set_cast_shadows(False)
 c.set_editor_property('max_draw_distance',4500);c.set_editor_property('max_distance_fade_range',500)
 if isinstance(a,unreal.SpotLight):a.set_actor_rotation(unreal.Rotator(-70,0,0),True)
 if isinstance(a,unreal.RectLight):a.set_actor_rotation(unreal.Rotator(-90,0,0),True)

for name,pos,scale in [('NS_Hojas',(-4400,-7900,250),1),('NS_Polvo',(900,-2300,60),.5),('NS_Luces',(0,-9300,80),.5)]:
 a=actor('FX_'+name,unreal.NiagaraActor,pos);c=a.get_component_by_class(unreal.NiagaraComponent);c.set_asset(unreal.load_asset('/Game/ThirdPerson/RecursosPropios/Particulas/'+name));a.set_actor_scale3d(unreal.Vector(scale,scale,scale))
 c.set_editor_property('ld_max_draw_distance',4500)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
with open(os.path.join(root,'Intermediate/inspect/evaluation_props.json'),'w') as f:json.dump({'team_collections':collections,'four_lod_models':lods,'local_lights':3,'ambient_fx':3},f,indent=2)
unreal.log('EVALUATION_PROPS_PREPARED')
