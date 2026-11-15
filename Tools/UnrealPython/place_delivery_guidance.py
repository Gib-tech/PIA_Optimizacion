"""World prompts and non-colliding entrance markings aligned to encounter bounds."""
import unreal
ROOT='/Game/ThirdPerson/Blueprints/Entrega/'
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors={a.get_actor_label():a for a in sub.get_all_level_actors()}
hostage=next(a for a in actors.values() if a.get_class().get_name()=='BP_Hostage_C')
def guide(name,label,pos,key,target):
    asset=unreal.load_asset(ROOT+name);unreal.BlueprintEditorLibrary.compile_blueprint(asset)
    cdo=unreal.get_default_object(asset.generated_class());text=cdo.get_component_by_class(unreal.TextRenderComponent)
    text.set_world_size(25);text.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER);text.set_vertical_alignment(unreal.VerticalTextAligment.EVRTA_TEXT_CENTER);text.set_cast_shadow(False)
    text.set_text_render_color(unreal.Color(90,220,255,255))
    tick=cdo.get_editor_property('primary_actor_tick');tick.set_editor_property('tick_interval',.1);cdo.set_editor_property('primary_actor_tick',tick)
    unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
    actor=actors.get(label) or sub.spawn_actor_from_class(asset.generated_class(),pos)
    actor.set_actor_label(label);actor.set_folder_path('Indicaciones');actor.set_editor_property(key,target)
    actor.get_component_by_class(unreal.TextRenderComponent).set_mobility(unreal.ComponentMobility.MOVABLE)
    actor.set_actor_enable_collision(False)
    return actor
guide('BP_RehenIndicador','Indicador_Rehen',hostage.get_actor_location()+unreal.Vector(0,0,180),'Rehen',hostage)
for i,zone in enumerate([a for a in actors.values() if a.get_class().get_name()=='BP_CombatZone_C'],1):
    pos=zone.get_actor_location();extent=zone.get_component_by_class(unreal.BoxComponent).get_unscaled_box_extent()
    guide('BP_ZonaIndicador','Indicador_Zona_%02d'%i,unreal.Vector(pos.x,pos.y+extent.y+130,180),'Zona',zone)
    for j,(dx,dy,sx,sy) in enumerate([(0,extent.y,extent.x*2/100,.1),(0,-extent.y,extent.x*2/100,.1),(extent.x,0,.1,extent.y*2/100),(-extent.x,0,.1,extent.y*2/100)]):
        label='Limite_Zona_%02d_%d'%(i,j)
        actor=actors.get(label) or sub.spawn_actor_from_class(unreal.StaticMeshActor,unreal.Vector(pos.x+dx,pos.y+dy,3))
        actor.set_actor_label(label);actor.set_folder_path('Indicaciones/Zonas')
        comp=actor.static_mesh_component;comp.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'));comp.set_material(0,unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/M_Baliza_Activa'))
        actor.set_actor_scale3d(unreal.Vector(sx,sy,.03));actor.set_actor_enable_collision(False)
        comp.set_editor_property('can_ever_affect_navigation',False);comp.set_cast_shadow(False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
for path in ['EnemigoIA/BP_BaseEnemy','EnemigoIA/BTTask_ChargerCharge','Entrega/BP_PlayerEntrega','Entrega/BP_RehenIndicador','Entrega/BP_ZonaIndicador']:
    unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).close_all_editors_for_asset(unreal.load_asset('/Game/ThirdPerson/Blueprints/'+path))
unreal.log('WORLD_GUIDANCE_PLACED')
