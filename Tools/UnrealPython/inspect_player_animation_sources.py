import unreal,os,re,json
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());out=os.path.join(root,'Intermediate/inspect/player_animations');os.makedirs(out,exist_ok=True)
registry=unreal.AssetRegistryHelpers.get_asset_registry();rows=[]
for a in registry.get_assets_by_path('/Game/ThirdPerson/Animations',recursive=True):
 if str(a.asset_class_path.asset_name)!='AnimMontage':continue
 asset=a.get_asset();t=unreal.AssetExportTask();t.object=asset;t.filename=os.path.join(out,asset.get_name()+'.t3d');t.automated=True;t.prompt=False;t.replace_identical=True
 assert unreal.Exporter.run_asset_export_task(t)
 raw=open(t.filename,'rb').read();source=raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig')
 refs=sorted(set(re.findall(r"AnimReference=\"/Script/Engine.AnimSequence'([^']+)'",source)))
 rows.append({'montage':asset.get_path_name(),'sequences':refs})
with open(os.path.join(out,'sources.json'),'w') as f:json.dump(rows,f,indent=2)
unreal.log('PLAYER_ANIMATION_SOURCES '+json.dumps(rows))
