import unreal,os
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
bp=unreal.DeliveryBlueprintBuilder.get_level_blueprint(world);assert bp
for name,macro in [('AmbosAliadosVivos',True),('SecuenciaResuelta',True),('ConsultarAliados',False),('ConsultarSecuencia',False)]:
 assert unreal.DeliveryBlueprintBuilder.install_named_graph(bp,name,macro,os.path.join(root,'Intermediate/inspect/delivery_graphs',name+'.t3d')),name
assert unreal.DeliveryBlueprintBuilder.install_graph(bp,os.path.join(root,'Intermediate/inspect/delivery_graphs/Nivel_Entrega_Evaluation.t3d'))
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
t=unreal.AssetExportTask();t.object=bp;t.filename=os.path.join(root,'Intermediate/inspect/live/Nivel_Entrega_LevelBlueprint.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;assert unreal.Exporter.run_asset_export_task(t)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log('EVALUATION_LEVEL_BLUEPRINT_INSTALLED')
