"""Ciclo parametrizable y luminaria reutilizable, colocada por trazas sobre paredes reales."""
import unreal,os,json,math
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert hasattr(unreal,'DeliveryBlueprintBuilder')
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
R='/Game/ThirdPerson/Blueprints/Entrega/';ART='/Game/ThirdPerson/Environment/Atmosphere'
assets=unreal.EditorAssetLibrary;lib=unreal.BlueprintEditorLibrary;tools=unreal.AssetToolsHelpers.get_asset_tools()
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert unreal.DeliveryBlueprintBuilder.load_editor_region(world,unreal.Vector(-6500,-12500,-1000),unreal.Vector(6500,1000,3000))
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
bp=unreal.load_asset(R+'BP_SistemasComplementarios')
try:unreal.get_default_object(bp.generated_class()).get_editor_property('DayCycleDuration')
except Exception:assert lib.add_member_variable(bp,'DayCycleDuration',lib.get_basic_type_by_name('real'))
lib.set_blueprint_variable_instance_editable(bp,'DayCycleDuration',True)
lib.compile_blueprint(bp);unreal.get_default_object(bp.generated_class()).set_editor_property('DayCycleDuration',1200.)
for a in actors.get_all_level_actors():
 if a.get_class()==bp.generated_class():a.modify();a.set_editor_property('DayCycleDuration',1200.)
assets.save_loaded_asset(bp,only_if_is_dirty=False)

lamp=unreal.load_asset(R+'BP_LuminariaPared')
if not lamp:
 factory=unreal.BlueprintFactory();factory.set_editor_property('parent_class',unreal.Actor)
 lamp=tools.create_asset('BP_LuminariaPared',R.rstrip('/'),unreal.Blueprint,factory)
sub=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem);fn=unreal.SubobjectDataBlueprintFunctionLibrary
handles=sub.k2_gather_subobject_data_for_blueprint(lamp)
def component(name,cls,parent):
 for h in handles:
  obj=fn.get_object(fn.get_data(h))
  if obj.get_name()==name+'_GEN_VARIABLE':return h,obj
 h,error=sub.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=parent,new_class=cls,blueprint_context=lamp))
 assert not str(error),str(error);assert sub.rename_subobject(h,unreal.Text(name));handles.append(h)
 return h,fn.get_object(fn.get_data(h))
# El padre de componentes debe ser el SceneRoot, no el handle del Actor.
# Un SceneComponent sin padre se queda en el origen aunque se mueva el Actor.
rh,scene=component('AnclajePared',unreal.SceneComponent,handles[0]);scene.set_mobility(unreal.ComponentMobility.STATIC)
assert sub.make_new_scene_root(handles[0],rh,lamp)
metal=unreal.load_asset('/Game/ThirdPerson/Environment/Progression/M_DoorSteel');assert metal
warm=unreal.load_asset(ART+'/M_LampWarm');assert warm
for name,pos,scale,mat in [('Soporte',(0,0,0),(.08,.32,.46),metal),('Carcasa',(10,0,0),(.20,.28,.40),metal),('Difusor',(21,0,-2),(.025,.22,.30),warm)]:
 h,c=component(name,unreal.StaticMeshComponent,rh)
 c.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));c.set_material(0,mat)
 c.set_editor_property('relative_location',unreal.Vector(*pos));c.set_editor_property('relative_scale3d',unreal.Vector(*scale))
 c.set_collision_profile_name('NoCollision');c.set_cast_shadow(False);c.set_mobility(unreal.ComponentMobility.STATIC)
 c.set_editor_property('can_ever_affect_navigation',False);c.set_editor_property('ld_max_draw_distance',4000.)
lh,light=component('LuzRecorrido',unreal.SpotLightComponent,rh)
light.set_mobility(unreal.ComponentMobility.MOVABLE);light.set_editor_property('relative_location',unreal.Vector(30,0,-12));light.set_editor_property('relative_rotation',unreal.Rotator(pitch=-40))
light.set_editor_property('intensity_units',unreal.LightUnits.LUMENS);light.set_intensity(3200.)
light.set_light_color(unreal.LinearColor(1.,.78,.49,1));light.set_attenuation_radius(1450.)
light.set_inner_cone_angle(38.);light.set_outer_cone_angle(78.);light.set_cast_shadows(True)
light.set_editor_property('max_draw_distance',2700.);light.set_editor_property('max_distance_fade_range',500.)
light.set_editor_property('shadow_resolution_scale',.5)
assert unreal.DeliveryBlueprintBuilder.set_property_text(lamp,'BlueprintDescription','Luminaria de pared reutilizable: soporte, carcasa, difusor cálido y foco hacia el suelo. Sin Tick ni colisión. 3200 lm, radio 1450 cm, sombras y culling a 2700 cm. Colocación trazada sobre paredes; docs/CICLO_LUCES_Y_ATAQUES.md.')
lib.compile_blueprint(lamp);cdo=unreal.get_default_object(lamp.generated_class())
assert unreal.DeliveryBlueprintBuilder.set_property_text(cdo,'PrimaryActorTick','(bCanEverTick=False,bStartWithTickEnabled=False)')
assert unreal.DeliveryBlueprintBuilder.add_layout_comment(lamp,'DocumentacionLuminaria','LUMINARIA DE PARED · Sin Tick / sin colisión\nLuz cálida permanente de recorrido: 3200 lm; radio 14,5 m.\nFoco inclinado y sombras evitan iluminar a través de muros.\nDistancia máxima 27 m + desvanecimiento de 5 m.\nReceta: prepare_daynight_wall_lights.py\nContrato y QA: docs/CICLO_LUCES_Y_ATAQUES.md',unreal.Vector2D(-400,-400),unreal.Vector2D(750,350),unreal.LinearColor(.12,.20,.28,1))
assets.save_loaded_asset(lamp,only_if_is_dirty=False)

# Muestrear cada sector en su centro y dos puntos de paso. Cada candidato debe
# impactar una fachada vertical de Compound_SM_Walls_ a menos de 16 metros.
# El normal de impacto define la orientación y separa el anclaje de la pared.
buildings=json.load(open(os.path.join(root,'Tools/ArtSource/Atmosphere/building_layout.json')))
placed={a.get_actor_label():a for a in actors.get_all_level_actors()};points=[];rows=[]
for b in buildings:
 cx,cy,_=b['center'];chosen=[]
 for ox,oy in [(0,0),(-450,-250),(450,250)]:
  for deg in range(0,360,45):
   origin=unreal.Vector(cx+ox,cy+oy,275)
   end=origin+unreal.Vector(math.cos(math.radians(deg))*1600,math.sin(math.radians(deg))*1600,0)
   hit=unreal.SystemLibrary.line_trace_single(world,origin,end,unreal.TraceTypeQuery.TRACE_TYPE_QUERY1,True,[],unreal.DrawDebugTrace.NONE)
   if not hit:continue
   parts=unreal.get_default_object(unreal.GameplayStatics).call_method('BreakHitResult',(hit,))
   point,normal,wall=parts[5],parts[7],parts[9]
   if not wall or not wall.get_actor_label().startswith('Compound_SM_Walls_') or abs(normal.z)>.15 or parts[3]<120:continue
   if any(point.distance(other)<800 for other in points):continue
   points.append(point);chosen.append((point,normal,wall.get_actor_label()))
   if len(chosen)>=5:break
  if len(chosen)>=5:break
 for i,(point,normal,wall) in enumerate(chosen,1):
  label='Luminaria_Pared_'+b['name']+'_'+str(i)
  a=placed.get(label) or actors.spawn_actor_from_class(lamp.generated_class(),point)
  a.modify();a.set_actor_label(label);a.set_actor_location(point+normal*5,False,True)
  a.set_actor_rotation(unreal.Rotator(yaw=math.degrees(math.atan2(normal.y,normal.x))),False)
  a.set_folder_path('Escenario/Compound/LuminariasPared');a.set_editor_property('is_spatially_loaded',False)
  rows.append({'label':label,'wall':wall,'position_cm':[round(v,2) for v in [point.x+normal.x*5,point.y+normal.y*5,point.z]],'normal':[normal.x,normal.y,normal.z]})
assert len(rows)>=30, len(rows)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()+unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
if dirty:assert unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
folder=os.path.join(root,'docs/validation/ciclo-luces-ataques');os.makedirs(folder,exist_ok=True)
with open(os.path.join(folder,'luminarias.json'),'w',encoding='utf-8') as f:json.dump({'cycle_seconds':1200,'lamp_count':len(rows),'lumens':3200,'radius_cm':1450,'max_draw_distance_cm':2700,'cast_shadows':True,'actors':rows},f,ensure_ascii=False,indent=2)
unreal.log('DAYNIGHT_WALL_LIGHTS_PREPARED '+str(len(rows)))
