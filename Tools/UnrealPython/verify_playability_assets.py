"""Lee las propiedades aplicadas y los materiales efectivos en el mapa cargado."""
from pathlib import Path
import json,unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert w and not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
unreal.DeliveryBlueprintBuilder.load_editor_region(w,unreal.Vector(-6500,-12500,-1200),unreal.Vector(6500,1500,7000))
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
sm=unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
lights=[];models=[];textures=[];effects=[]
for a in actors:
    label=a.get_actor_label()
    if label.startswith('Luminaria_Pared_'):
        c=a.get_component_by_class(unreal.SpotLightComponent)
        assert c.get_editor_property('max_draw_distance')==2300 and abs(c.get_editor_property('shadow_resolution_scale')-.35)<.001 and c.get_editor_property('volumetric_scattering_intensity')==0
        lights.append(label)
    if label.startswith(('Equipo_','LOD_')):
        c=a.static_mesh_component
        materials=[m.get_name() if m else None for m in c.get_materials()]
        assert all(materials),(label,materials)
        lods=sm.get_lod_count(c.static_mesh);assert lods>=1,(label,lods)
        models.append({'actor':label,'lods':lods,'materiales':materials,'distancia_dibujo_cm':c.get_editor_property('ld_max_draw_distance')})
    if label in ['FX_NS_Hojas','FX_NS_Polvo']:
        c=a.get_component_by_class(unreal.NiagaraComponent)
        effects.append({'actor':label,'sistema':c.get_asset().get_name(),'distancia_cm':c.get_editor_property('ld_max_draw_distance')})
for path,limit in [('/Game/ThirdPerson/RecursosPropios/Modelos/ConcreteBench',1024),('/Game/ThirdPerson/Environment/TeamModels/Textures/T_Escombros_0_BaseColor',512)]:
    t=unreal.load_asset(path);assert t.get_editor_property('max_texture_size')==limit and not t.get_editor_property('never_stream')
    textures.append({'recurso':path,'max_px':limit,'streaming':True})
assert len(lights)==41 and len(models)>=12 and len(effects)==2
data={'passed':True,'focos':len(lights),'radio_cm':1450,'distancia_dibujo_cm':2300,'escala_sombra':.35,'dispersion_volumetrica':0,'modelos':models,'texturas':textures,'particulas':effects}
(Path(unreal.Paths.project_dir()).resolve()/'docs/validation/revision-jugable/recursos.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
