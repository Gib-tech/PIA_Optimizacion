"""Avoid distance-field self-occlusion on Ian's combined room meshes."""
import unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Nivel_Entrega'
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
placed=actors.get_all_level_actors()
for actor in placed:
    if actor.get_actor_label().startswith('Ian_Sector_'):
        actor.modify()
        component=actor.static_mesh_component
        component.modify()
        component.set_editor_property('affect_distance_field_lighting',False)
        unreal.log('DELIVERY_DISTANCE_FIELD_OFF '+actor.get_actor_label())
    if isinstance(actor,unreal.SkyLight):
        actor.modify();actor.light_component.modify()
        actor.light_component.set_editor_property('cast_shadows',False)
volume=next((a for a in placed if a.get_actor_label()=='Iluminacion_Entrega'),None)
if not volume:
    volume=actors.spawn_actor_from_class(unreal.PostProcessVolume,unreal.Vector())
    volume.set_actor_label('Iluminacion_Entrega')
    volume.set_folder_path('Escenario/Iluminacion')
volume.modify()
volume.set_editor_property('unbound',True)
settings=volume.get_editor_property('settings')
settings.set_editor_property('override_dynamic_global_illumination_method',True)
settings.set_editor_property('dynamic_global_illumination_method',unreal.DynamicGlobalIlluminationMethod.NONE)
volume.set_editor_property('settings',settings)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('DELIVERY_LIGHTING: simple skylight GI for this level; sun shadows retained')
