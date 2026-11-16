"""Read-only export of the delivery loop and legacy persistence integration."""
import os
import unreal

project = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
out = os.path.join(project, 'Intermediate/inspect/save_audit')
os.makedirs(out, exist_ok=True)
paths = [
    '/Game/Menu/Menu_Inicio', '/Game/Menu/Menu_Pausa',
    '/Game/LevelMenu/BP_GameInstance', '/Game/LevelMenu/BP_SaveGame',
    '/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega',
    '/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega',
    '/Game/ThirdPerson/Blueprints/Entrega/BP_CombatZone',
    '/Game/ThirdPerson/Blueprints/Entrega/BP_BeaconEntrega',
    '/Game/ThirdPerson/Blueprints/Entrega/BP_DestructibleDoor',
    '/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage',
    '/Game/ThirdPerson/Blueprints/AnimNotifies/BPC_Health',
]
for path in paths:
    asset = unreal.load_asset(path)
    assert asset, path
    task = unreal.AssetExportTask()
    task.object = asset
    task.filename = os.path.join(out, asset.get_name() + '.t3d')
    task.automated = True
    task.prompt = False
    task.replace_identical = True
    assert unreal.Exporter.run_asset_export_task(task), path
    unreal.log('SAVE_AUDIT ' + path)
unreal.log('EDITOR_BUILDER_AVAILABLE ' + str(hasattr(unreal, 'DeliveryBlueprintBuilder')))
unreal.log('SAVE_AUDIT_OUT ' + out)
