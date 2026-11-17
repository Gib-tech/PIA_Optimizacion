"""Prepare the Blueprint controller and cache field; preserve the existing map."""
import unreal,os,shutil
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
assert hasattr(unreal,'DeliveryBlueprintBuilder')
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
backup=os.path.join(root,'Intermediate/inspect/cinematics/backup');os.makedirs(backup,exist_ok=True)
for rel in ['Content/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.uasset','Content/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega.uasset','Content/ThirdPerson/Blueprints/Aliado/BP_Hostage.uasset']:
    dest=os.path.join(backup,os.path.basename(rel))
    if not os.path.exists(dest):shutil.copy2(os.path.join(root,rel),dest)
path='/Game/ThirdPerson/Cinematics/BP_CinematicDirector'
bp=unreal.load_asset(path)
if not bp:
    f=unreal.BlueprintFactory();f.set_editor_property('parent_class',unreal.Actor)
    bp=unreal.AssetToolsHelpers.get_asset_tools().create_asset('BP_CinematicDirector','/Game/ThirdPerson/Cinematics',unreal.Blueprint,f)
lib=unreal.BlueprintEditorLibrary
fields={'bShouldIntro':'bool','bInitialized':'bool','bActive':'bool','bOutcomeStarted':'bool','Kind':'int','StartedAt':'real','Duration':'real','EndsAt':'real',
        'Hero':'/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega.BP_PlayerEntrega_C',
        'Hostage':'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C',
        'Director':'/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega.BP_DirectorEntrega_C',
        'Interface':'/Game/ThirdPerson/Blueprints/Entrega/BP_DeliveryInterface.BP_DeliveryInterface_C',
        'GameHUD':'/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega.BP_HUD_Entrega_C',
        'SequencePlayer':'/Script/LevelSequence.LevelSequencePlayer','SequenceActor':'/Script/LevelSequence.LevelSequenceActor','SavedViewTarget':'/Script/Engine.Actor'}
def add(asset,name,kind):
    try:unreal.get_default_object(asset.generated_class()).get_editor_property(name);return
    except Exception:pass
    typ=lib.get_object_reference_type(unreal.load_class(None,kind)) if kind.startswith('/') else lib.get_basic_type_by_name(kind)
    assert lib.add_member_variable(asset,name,typ),(name,kind)
for name,kind in fields.items():add(bp,name,kind)
lib.compile_blueprint(bp)
cdo=unreal.get_default_object(bp.generated_class());cdo.set_editor_property('auto_receive_input',unreal.AutoReceiveInput.PLAYER0);cdo.set_editor_property('input_priority',100)
unreal.EditorAssetLibrary.save_loaded_asset(bp,only_if_is_dirty=False)
hud=unreal.load_asset('/Game/ThirdPerson/Blueprints/Entrega/BP_HUD_Entrega');add(hud,'CachedCinema',path+'.BP_CinematicDirector_C');lib.compile_blueprint(hud)
unreal.EditorAssetLibrary.save_loaded_asset(hud,only_if_is_dirty=False)
unreal.log('CINEMA_RUNTIME_SHELL_READY')
