import unreal
unreal.log('SKY_MATERIAL_CLASSES '+str([x for x in dir(unreal) if x.startswith('MaterialExpression') and any(k in x for k in ['SkyAtmosphere','Custom','CameraPosition','WorldPosition'])]))
for n in ['MaterialExpressionCustom','CustomInput','CustomMaterialOutputType','MaterialExpressionSkyAtmosphereViewLuminance','MaterialExpressionSkyAtmosphereLightDiskLuminance']:
 c=getattr(unreal,n,None);unreal.log('SKY_API '+n+' '+str(c.__doc__ if c else None))
unreal.log('SPHERE_AVAILABLE '+str(unreal.EditorAssetLibrary.does_asset_exist('/Engine/EngineSky/SM_SkySphere')))
for path in ['/Game/Menu/Menu_Inicio','/Game/Menu/Menu_Pausa','/Game/Menu/Menu_Opciones']:
 bp=unreal.load_asset(path);t=unreal.AssetExportTask();t.object=bp;t.filename=unreal.Paths.project_dir()+'Intermediate/inspect/robot-sky/'+bp.get_name()+'.t3d';t.automated=True;t.prompt=False;t.replace_identical=True;unreal.Exporter.run_asset_export_task(t)
bp=unreal.load_asset('/Game/ThirdPerson/Cinematics/BP_CinematicDirector');t=unreal.AssetExportTask();t.object=bp;t.filename=unreal.Paths.project_dir()+'Intermediate/inspect/robot-sky/cinema-before.t3d';t.automated=True;t.prompt=False;t.replace_identical=True;assert unreal.Exporter.run_asset_export_task(t)
