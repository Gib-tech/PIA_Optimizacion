"""Crea inventario, suministros, técnico y ciclo horario del nivel entregable."""
import unreal,os
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
R='/Game/ThirdPerson/Blueprints/Entrega/'
lib=unreal.BlueprintEditorLibrary;assets=unreal.EditorAssetLibrary;tools=unreal.AssetToolsHelpers.get_asset_tools()
def shell(name,parent):
 bp=unreal.load_asset(R+name)
 if not bp:
  f=unreal.BlueprintFactory();f.set_editor_property('parent_class',parent);bp=tools.create_asset(name,R.rstrip('/'),unreal.Blueprint,f)
 return bp
def add(bp,name,kind):
 try:unreal.get_default_object(bp.generated_class()).get_editor_property(name);return
 except Exception:pass
 typ=lib.get_object_reference_type(unreal.load_class(None,kind)) if kind.startswith('/') else lib.get_basic_type_by_name(kind)
 assert lib.add_member_variable(bp,name,typ),name
systems=shell('BP_SistemasComplementarios',unreal.Actor)
tech=shell('BP_TecnicoTemporal',unreal.SkeletalMeshActor)
fields={'bInitialized':'bool','InventoryOpen':'bool','Botiquines':'int','Cargas':'int','Creditos':'int','WorldSeconds':'real',
 'LastPulseAt':'real','DialogUntil':'real','DialogSpeaker':'string','DialogText':'string','Notice':'string','NoticeUntil':'real',
 'Hero':R+'BP_PlayerEntrega.BP_PlayerEntrega_C','Director':R+'BP_DirectorEntrega.BP_DirectorEntrega_C','Tecnico':R+'BP_TecnicoTemporal.BP_TecnicoTemporal_C',
 'Sun':'/Script/Engine.DirectionalLight','Sky':'/Script/Engine.SkyLight'}
for i in range(1,5):fields.update({'Recogido'+str(i):'bool','Suministro'+str(i):'/Script/Engine.StaticMeshActor'})
for name,kind in fields.items():
 add(systems,name,kind)
 if name.startswith(('Suministro','Tecnico','Sun','Sky')):lib.set_blueprint_variable_instance_editable(systems,name,True)
for bp in [systems,tech]:lib.compile_blueprint(bp)
cdo=unreal.get_default_object(systems.generated_class());cdo.set_editor_property('auto_receive_input',unreal.AutoReceiveInput.PLAYER0);cdo.set_editor_property('input_priority',5)
cdo.set_editor_property('LastPulseAt',-10)
cdo=unreal.get_default_object(tech.generated_class());cdo.skeletal_mesh_component.set_skeletal_mesh_asset(unreal.load_asset('/Game/ThirdPerson/Characters/Rehen/SK_RehenSuperviviente'))
cdo.skeletal_mesh_component.set_anim_instance_class(unreal.load_class(None,'/Game/ThirdPerson/Blueprints/Aliado/ABP_RehenSuperviviente.ABP_RehenSuperviviente_C'))
cdo.skeletal_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
for bp in [systems,tech]:assets.save_loaded_asset(bp,only_if_is_dirty=False)
# El esquema 2 se amplía de forma aditiva; guardados anteriores usan valores 0.
save=unreal.load_asset(R+'BP_DeliverySave');manager=unreal.load_asset(R+'BP_DeliverySaveManager')
for name,kind in [('FirstPerson','bool'),('ExtrasRevision','int'),('Botiquines','int'),('Cargas','int'),('Creditos','int'),('WorldSeconds','real')]+[('Recogido'+str(i),'bool') for i in range(1,5)]:add(save,name,kind)
add(manager,'Extras',R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C')
for bp in [save,manager]:lib.compile_blueprint(bp);assets.save_loaded_asset(bp,only_if_is_dirty=False)
hud=unreal.load_asset(R+'BP_HUD_Entrega');add(hud,'CachedExtras',R+'BP_SistemasComplementarios.BP_SistemasComplementarios_C');lib.compile_blueprint(hud);assets.save_loaded_asset(hud,only_if_is_dirty=False)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem);level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
placed={a.get_actor_label():a for a in actors.get_all_level_actors()}
def spawn(label,cls,loc,rot=None):
 a=placed.get(label) or actors.spawn_actor_from_class(cls,unreal.Vector(*loc),rot or unreal.Rotator())
 a.set_actor_label(label);a.set_folder_path('Entrega/Complementos');a.modify();a.set_editor_property('is_spatially_loaded',False);return a
system=spawn('Sistemas_Complementarios',systems.generated_class(),(0,0,0))
system.set_editor_property('auto_receive_input',unreal.AutoReceiveInput.PLAYER0);system.set_editor_property('input_priority',5)
technician=spawn('Tecnico_Bruno',tech.generated_class(),(-400,-850,3),unreal.Rotator(yaw=70))
system.set_editor_property('Tecnico',technician)
for i,loc in enumerate([(-330,-1050,35),(-2300,-3750,35),(0,-6250,35),(900,-10000,35)],1):
 a=spawn('Suministro_Temporal_'+str(i),unreal.StaticMeshActor,loc)
 a.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'))
 a.set_actor_scale3d(unreal.Vector(.45,.35,.35));a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
 system.set_editor_property('Suministro'+str(i),a)
for a in actors.get_all_level_actors():
 if isinstance(a,unreal.DirectionalLight):system.set_editor_property('Sun',a)
 if isinstance(a,unreal.SkyLight):system.set_editor_property('Sky',a)
level.save_current_level()
dirty=unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
if dirty:unreal.EditorLoadingAndSavingUtils.save_packages(dirty,only_dirty=True)
unreal.log('RUBRIC_SYSTEMS_PREPARED')
