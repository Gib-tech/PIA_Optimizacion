"""Ambient Niagara culls simulation by distance/visibility and resumes on return."""
import unreal,os,json
ART='/Game/ThirdPerson/Environment/Atmosphere';tools=unreal.AssetToolsHelpers.get_asset_tools()
effect=unreal.load_asset(ART+'/NET_CompoundAmbient')
if not effect:effect=tools.create_asset('NET_CompoundAmbient',ART,unreal.NiagaraEffectType,None)
assert effect
settext=unreal.DeliveryBlueprintBuilder.set_property_text
assert settext(effect,'SystemScalabilitySettings','(Settings=((Platforms=(QualityLevelMask=-1),bCullByDistance=True,MaxDistance=2400,VisibilityCulling=(bCullWhenNotRendered=True,bCullByViewFrustum=True,bAllowPreCullingByViewFrustum=True,MaxTimeOutsideViewFrustum=1.0,MaxTimeWithoutRender=1.0))))')
assert settext(effect,'CullReaction','DeactivateImmediateResume')
assert settext(effect,'UpdateFrequency','Low')
unreal.EditorAssetLibrary.save_loaded_asset(effect)
report=[]
for a in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
    if a.get_actor_label() not in ('FX_NS_Hojas','FX_NS_Polvo','FX_Extraccion'):continue
    a.modify()
    c=a.get_component_by_class(unreal.NiagaraComponent);c.modify();source=c.get_asset();assert source
    name='NS_Compound_'+('Hojas' if 'Hojas' in a.get_actor_label() else 'Polvo' if 'Polvo' in a.get_actor_label() else 'Extraccion')
    system=unreal.load_asset(ART+'/'+name)
    if not system:system=tools.duplicate_asset(name,ART,source)
    assert settext(system,'EffectType',"/Script/Niagara.NiagaraEffectType'"+effect.get_path_name()+"'")
    # Finite bounds allow pre-culling before a simulation is started.
    assert settext(system,'bFixedBounds','True')
    assert settext(system,'FixedBounds','(Min=(X=-600,Y=-600,Z=-100),Max=(X=600,Y=600,Z=800),IsValid=True)')
    unreal.EditorAssetLibrary.save_loaded_asset(system)
    c.set_asset(system);c.set_editor_property('ld_max_draw_distance',2400)
    report.append({'actor':a.get_actor_label(),'system':system.get_path_name(),'source':source.get_path_name(),'max_distance':2400,'offscreen_seconds':1,'reaction':'DeactivateImmediateResume'})
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
dirty=[p for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages() if p.get_path_name().startswith('/Game/__ExternalActors__/ThirdPerson/Maps/Nivel_Entrega/')]
unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
with open(os.path.join(unreal.Paths.project_dir(),'Intermediate/inspect/compound_fx.json'),'w') as f:json.dump(report,f,indent=2)
unreal.log('COMPOUND_FX_SCALABILITY_READY')
