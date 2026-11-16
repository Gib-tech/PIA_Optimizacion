import unreal,os,json
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bp=unreal.DeliveryBlueprintBuilder.get_level_blueprint(world);assert bp,'Level Blueprint creation failed'
lib=unreal.BlueprintEditorLibrary
for name,kind in {'Jugador':'/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C','Rehen':'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C','Director':'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C','SenalExtraccion':'/Script/Engine.Actor','Inicializado':'bool','Inicializaciones':'int','Sincronizaciones':'int'}.items():
 try:unreal.get_default_object(bp.generated_class()).get_editor_property(name);continue
 except Exception:pass
 typ=lib.get_object_reference_type(unreal.load_class(None,kind)) if kind.startswith('/') else lib.get_basic_type_by_name(kind)
 assert lib.add_member_variable(bp,name,typ)
lib.compile_blueprint(bp)
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
signalbp=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_SenalExtraccion')
if not signalbp:
 factory=unreal.BlueprintFactory();factory.set_editor_property('parent_class',unreal.NiagaraActor)
 signalbp=unreal.AssetToolsHelpers.get_asset_tools().create_asset('BP_SenalExtraccion','/Game/ThirdPerson/Blueprints/Entrega',unreal.Blueprint,factory)
 unreal.get_default_object(signalbp.generated_class()).get_component_by_class(unreal.NiagaraComponent).set_asset(unreal.load_asset('/Game/ThirdPerson/RecursosPropios/Particulas/NS_Luces'))
 unreal.EditorAssetLibrary.save_loaded_asset(signalbp)
signal=next((a for a in actors.get_all_level_actors() if a.get_actor_label()=='FX_Extraccion'),None)
if not signal:
 signal=actors.spawn_actor_from_class(signalbp.generated_class(),unreal.Vector(0,-11400,100))
 signal.set_actor_label('FX_Extraccion');signal.set_folder_path('Mision/Extraccion')
 signal.get_component_by_class(unreal.NiagaraComponent).set_asset(unreal.load_asset('/Game/ThirdPerson/RecursosPropios/Particulas/NS_Luces'))
 signal.set_is_temporarily_hidden_in_editor(False)
signal.set_editor_property('is_spatially_loaded',False)
signal.set_actor_hidden_in_game(True)
# Resolve the signal by class at BeginPlay: no serialized actor pointer on a CDO.
tick=unreal.get_default_object(bp.generated_class()).get_editor_property('primary_actor_tick');tick.set_editor_property('tick_interval',.2)
unreal.get_default_object(bp.generated_class()).set_editor_property('primary_actor_tick',tick)
root=unreal.Paths.project_dir()
with open(os.path.join(root,'Intermediate/inspect/evaluation_level_blueprint.json'),'w') as f:json.dump({'blueprint':bp.get_path_name(),'class':bp.generated_class().get_path_name()},f,indent=2)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('EVALUATION_LEVEL_BLUEPRINT_PREPARED '+bp.get_path_name())
