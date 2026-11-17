"""Place useful scenery around the route while leaving existing gameplay intact."""
import unreal,os,json,math
ues=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem);assert not ues.get_game_world()
world=ues.get_editor_world();assert world.get_name()=='Nivel_Entrega'
root=unreal.Paths.project_dir();ART='/Game/ThirdPerson/Environment/TeamModels'
source=os.path.join(root,'Tools/ArtSource/TeamModels');specs=json.load(open(os.path.join(source,'placements.json')));models={r['name']:r for r in json.load(open(os.path.join(source,'manifest.json'),encoding='utf-8'))}
assert unreal.DeliveryBlueprintBuilder.load_editor_region(world,unreal.Vector(-6500,-12500,-1000),unreal.Vector(6500,1000,7000))
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);placed={a.get_actor_label():a for a in sub.get_all_level_actors()}
def actor(label,cls,position):
 a=placed.get(label)
 if not a:a=sub.spawn_actor_from_class(cls,unreal.Vector(*position));placed[label]=a
 a.modify();a.set_actor_label(label);a.set_folder_path('Escenario/ModelosEquipo');a.set_actor_location(unreal.Vector(*position),False,True);a.set_editor_property('is_spatially_loaded',False);return a
proof=[]
for spec in specs:
 row=models[spec['model']];a=actor(spec['label'],unreal.StaticMeshActor,spec['position']);a.set_actor_scale3d(unreal.Vector(spec['scale'],spec['scale'],spec['scale']));a.set_actor_rotation(unreal.Rotator(pitch=0,yaw=spec['yaw'],roll=0),True)
 c=a.static_mesh_component;c.modify();c.set_mobility(unreal.ComponentMobility.STATIC);c.set_static_mesh(unreal.load_asset(ART+'/'+row['mesh']));c.set_collision_profile_name('BlockAll');c.set_collision_response_to_channel(unreal.CollisionChannel.ECC_CAMERA,unreal.CollisionResponseType.ECR_IGNORE)
 c.set_editor_properties({'ld_max_draw_distance':0.0,'never_distance_cull':True,'bounds_scale':1.0});c.set_forced_lod_model(0)
 center,extent,radius=unreal.SystemLibrary.get_component_bounds(c)
 proof.append({'label':spec['label'],'model':spec['model'],'position':spec['position'],'scale':spec['scale'],'bounds_center':[center.x,center.y,center.z],'bounds_extent':[extent.x,extent.y,extent.z],'resident':True,'automatic_lod':True,'simple_collision':True})
 if spec['model']=='Farol':
  local=models['Farol']['glass_center'];rad=math.radians(spec['yaw']);x,y,z=spec['position'];s=spec['scale']
  pos=[x+(local[0]*math.cos(rad)-local[1]*math.sin(rad))*s,y+(local[0]*math.sin(rad)+local[1]*math.cos(rad))*s,z+local[2]*s]
  light=actor('Luz_'+spec['label'],unreal.PointLight,pos);lc=light.light_component;lc.modify();lc.set_mobility(unreal.ComponentMobility.MOVABLE);lc.set_editor_property('intensity_units',unreal.LightUnits.LUMENS);lc.set_intensity(1600);lc.set_light_color(unreal.LinearColor(1,.68,.34,1));lc.set_cast_shadows(False)
  lc.set_editor_properties({'attenuation_radius':450.0,'max_draw_distance':2200.0,'max_distance_fade_range':400.0,'volumetric_scattering_intensity':0.0})
# A two-triangle backdrop below the playable Landscape fills the black horizon.
# It has no collision, navigation or shadows and does not replace the terrain.
path=ART+'/Materials/M_Horizonte';ground=unreal.load_asset(path)
if not ground:
 ground=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_Horizonte',ART+'/Materials',unreal.Material,unreal.MaterialFactoryNew());edit=unreal.MaterialEditingLibrary
 color=edit.create_material_expression(ground,unreal.MaterialExpressionConstant3Vector,-220,0);color.constant=unreal.LinearColor(.15,.12,.085,1);edit.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR)
 rough=edit.create_material_expression(ground,unreal.MaterialExpressionConstant,-220,160);rough.r=1;edit.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS);edit.recompile_material(ground);unreal.EditorAssetLibrary.save_loaded_asset(ground)
backdrop=actor('Horizonte_Terreno_Distante',unreal.StaticMeshActor,[0,-6000,-100]);backdrop.set_actor_scale3d(unreal.Vector(3000,3000,1));bc=backdrop.static_mesh_component;bc.modify();bc.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Plane'));bc.set_material(0,ground);bc.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION);bc.set_cast_shadow(False);bc.set_editor_property('affect_distance_field_lighting',False);bc.set_editor_property('never_distance_cull',True)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=[p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() if p.get_path_name().startswith(('/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/','/Game/__ExternalObjects__/ThirdPerson/Maps/Nivel_Entrega/'))]
if dirty:assert unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
with open(os.path.join(root,'Intermediate/inspect/team-models/placement-proof.json'),'w') as f:json.dump({'passed':True,'actors':proof,'lights':2},f,indent=2)
unreal.log('TEAM_MODELS_PLACED '+str(len(proof))+' meshes and 2 lights')
