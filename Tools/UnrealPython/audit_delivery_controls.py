"""Read-only exports for pause, options, camera, and keyboard/mouse integration."""
import unreal, os
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
out=os.path.join(root,'Intermediate/inspect/control_audit');os.makedirs(out,exist_ok=True)
paths=[
 '/Game/Menu/Menu_Inicio','/Game/Menu/Menu_Pausa','/Game/Menu/Menu_Opciones',
 '/Game/Menu/Pausa_pantalla_OV','/Game/Menu/Opciones_pantalla_OV',
 '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter',
 '/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega',
 '/Game/ThirdPerson/Blueprints/Entrega/BP_DirectorEntrega',
 '/Game/ThirdPerson/Blueprints/Entrega/BP_DeliverySaveManager',
 '/Game/ThirdPerson/Input/IMC_Default','/Game/ThirdPerson/Input/Actions/IA_Camera',
]
for path in paths:
 asset=unreal.load_asset(path);assert asset,path
 t=unreal.AssetExportTask();t.object=asset;t.filename=os.path.join(out,asset.get_name()+'.t3d')
 t.automated=True;t.prompt=False;t.replace_identical=True
 assert unreal.Exporter.run_asset_export_task(t),path
 unreal.log('CONTROL_AUDIT '+path)
unreal.log('CONTROL_AUDIT_OUT '+out)
