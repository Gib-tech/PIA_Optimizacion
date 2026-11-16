"""Create checkpoint assets and fields without rebuilding existing gameplay."""
import unreal
from pathlib import Path

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name() == 'Nivel_Entrega', 'Open Nivel_Entrega before preparing checkpoint assets'
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()

# Remote execution has no guaranteed tools path.
import sys
sys.path.insert(0, str(Path(unreal.Paths.project_dir()) / 'Tools/UnrealPython'))
from delivery_save_schema import ROOT, FIELDS

lib = unreal.BlueprintEditorLibrary
tools = unreal.AssetToolsHelpers.get_asset_tools()

def shell(name, parent):
    bp = unreal.load_asset(ROOT + name)
    if bp:
        return bp
    factory = unreal.BlueprintFactory()
    factory.set_editor_property('parent_class', parent)
    return tools.create_asset(name, ROOT.rstrip('/'), unreal.Blueprint, factory)

save = shell('BP_DeliverySave', unreal.SaveGame)
manager = shell('BP_DeliverySaveManager', unreal.Actor)
gi = unreal.load_asset('/Game/LevelMenu/BP_GameInstance')

def add(bp, name, kind):
    cdo = unreal.get_default_object(bp.generated_class())
    try:
        cdo.get_editor_property(name)
        return
    except Exception:
        pass
    if kind in ('vector', 'rotator'):
        typ = lib.get_struct_type(unreal.load_object(None, '/Script/CoreUObject.' + kind.title()))
    elif kind.startswith('/'):
        typ = lib.get_object_reference_type(unreal.load_class(None, kind))
    else:
        typ = lib.get_basic_type_by_name(kind)
    assert lib.add_member_variable(bp, name, typ), (name, kind)

for name, kind in FIELDS.items():
    add(save, name, kind)
for name, kind in {
    'bInitialized':'bool', 'bSaveSucceeded':'bool', 'bHasCheckpoint':'bool',
    'StatusText':'string', 'SaveData':ROOT+'BP_DeliverySave.BP_DeliverySave_C',
    'bRestoring':'bool',
    'Beacon1':ROOT+'BP_BeaconEntrega.BP_BeaconEntrega_C',
    'Beacon2':ROOT+'BP_BeaconEntrega.BP_BeaconEntrega_C',
    'Beacon3':ROOT+'BP_BeaconEntrega.BP_BeaconEntrega_C',
    'Hero':ROOT+'BP_PlayerEntrega.BP_PlayerEntrega_C',
    'Hostage':'/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage.BP_Hostage_C',
    'Director':ROOT+'BP_DirectorEntrega.BP_DirectorEntrega_C',
    'Instance':'/Game/LevelMenu/BP_GameInstance.BP_GameInstance_C',
}.items():
    add(manager, name, kind)
add(gi, 'bDeliveryContinue', 'bool')
for bp in (save, manager, gi):
    lib.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp, only_if_is_dirty=False)

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
existing = [a for a in actors.get_all_level_actors() if a.get_class() == manager.generated_class()]
assert len(existing) <= 1
if not existing:
    actor = actors.spawn_actor_from_class(manager.generated_class(), unreal.Vector(0, 0, 0))
    actor.set_actor_label('Guardado_Entrega')
    actor.set_folder_path('Entrega')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('DELIVERY_SAVE_FIELDS_READY')
