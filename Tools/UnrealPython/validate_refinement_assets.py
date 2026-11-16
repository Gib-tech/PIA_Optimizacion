"""Compile the touched Blueprints, remove temporary task probes and export final evidence."""
import unreal,os,json,re
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
E='/Game/ThirdPerson/Blueprints/EnemigoIA/'
A='/Game/ThirdPerson/Blueprints/Aliado/'
R='/Game/ThirdPerson/Blueprints/Entrega/'
bp=unreal.load_asset(E+'BTTask_ChargerRetreat')
unreal.BlueprintEditorLibrary.remove_unused_variables(bp)
paths=[E+n for n in ['BP_BaseEnemy','BP_ChargerEnemy','BP_ChargerController','BTService_LocatePlayer','BTTask_Attack','BTTask_ChargerWindup','BTTask_ChargerCharge','BTTask_ChargerRetreat','BTTask_FaceCombatTarget']]+[A+n for n in ['BP_Hostage','BTService_HostageSense','BTTask_ActivateBeacon']]+[R+n for n in ['BP_PlayerEntrega','BP_BeaconEntrega','BP_CombatZone','BP_DirectorEntrega','BP_HUD_Entrega']]
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
results=[]
for path in paths:
 asset=unreal.load_asset(path);unreal.BlueprintEditorLibrary.compile_blueprint(asset)
 unreal.EditorAssetLibrary.save_loaded_asset(asset,only_if_is_dirty=False)
 t=unreal.AssetExportTask();t.object=asset;t.filename=os.path.join(project,'Intermediate/inspect/live',asset.get_name()+'.t3d');t.automated=True;t.prompt=False;t.replace_identical=True;unreal.Exporter.run_asset_export_task(t)
 raw=open(t.filename,'rb').read();text=raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8');match=re.search(r'^   Status=(\w+)',text,re.M);status=match.group(1) if match else 'Compiled; status transient in export'
 assert 'Status=BS_Error' not in text,path
 results.append({'asset':path,'status':status})
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
with open(os.path.join(project,'Intermediate/inspect/refinement_compile_assertions.json'),'w') as f:json.dump({'passed':True,'assets':results},f,indent=2)
unreal.log('REFINEMENT_COMPILE_ASSERTIONS_PASSED '+str(len(results)))
