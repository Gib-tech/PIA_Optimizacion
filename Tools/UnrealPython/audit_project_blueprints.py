"""Auditoría reproducible: exporta todos los Blueprints sin alterar sus grafos."""
import unreal, os, json, re, collections

root = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
out = os.path.join(root, 'Intermediate/inspect/project_audit')
os.makedirs(out, exist_ok=True)
registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets = registry.get_assets_by_path('/Game', recursive=True)
report = {'blueprints': [], 'animation_assets': [], 'skeletal_meshes': [], 'api': {}}
for entry in assets:
    kind = str(entry.asset_class_path.asset_name)
    path = str(entry.package_name)
    if kind in ['Blueprint', 'AnimBlueprint', 'WidgetBlueprint', 'ControlRigBlueprint']:
        bp = entry.get_asset()
        task = unreal.AssetExportTask()
        task.object = bp
        task.filename = os.path.join(out, path.removeprefix('/Game/').replace('/', '__') + '.t3d')
        task.automated = True; task.prompt = False; task.replace_identical = True
        exported = unreal.Exporter.run_asset_export_task(task)
        raw = open(task.filename, 'rb').read() if exported else b''
        source = raw.decode('utf-16' if raw.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig')
        parent = re.search(r'ParentClass=(.*)',source)
        report['blueprints'].append({'path': path, 'class': kind,
            'parent': parent.group(1).strip() if parent else None, 'export': task.filename,
            'exported': exported, 'nodes': len(re.findall(r'Begin Object Class=.*?(?:K2Node|AnimGraphNode)', source)),
            'events': sorted(set(re.findall(r'(?:CustomFunctionName|MemberName)="([^"]+)"', source))),
            'references': sorted(set(re.findall(r'/Game/[^\s\"\'\),]+', source)))})
    elif kind == 'SkeletalMesh' and any(p in path for p in ['Survival_Character', 'ThirdPerson', 'Mannequins']):
        mesh = entry.get_asset()
        report['skeletal_meshes'].append({'path':path,'skeleton':mesh.skeleton.get_path_name()})
    elif kind in ['BlendSpace', 'BlendSpace1D', 'AnimSequence', 'AnimMontage', 'IKRigDefinition', 'IKRetargeter']:
        report['animation_assets'].append({'path':path,'class':kind})
level_bp=unreal.DeliveryBlueprintBuilder.get_level_blueprint(unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world())
if level_bp:
    task=unreal.AssetExportTask();task.object=level_bp;task.filename=os.path.join(out,'Nivel_Entrega__LevelScript.t3d');task.automated=True;task.prompt=False;task.replace_identical=True
    exported=unreal.Exporter.run_asset_export_task(task)
    raw=open(task.filename,'rb').read() if exported else b''
    source=raw.decode('utf-16' if raw.startswith(b'\xff\xfe') else 'utf-8-sig')
    report['blueprints'].append({'path':level_bp.get_path_name(),'class':'LevelScriptBlueprint','parent':'/Script/Engine.LevelScriptActor','export':task.filename,'exported':exported,'nodes':len(re.findall(r'Begin Object Class=.*?(?:K2Node|AnimGraphNode)',source)),'events':sorted(set(re.findall(r'(?:CustomFunctionName|MemberName)="([^"]+)"',source))),'references':sorted(set(re.findall(r'/Game/[^\s\"\'\),]+',source)))})
for clsname in ['BlueprintEditorLibrary', 'SubobjectDataSubsystem', 'SkeletalMeshComponent', 'Skeleton', 'AnimationLibrary', 'AnimSequence', 'IKRigController']:
    cls = getattr(unreal, clsname, None)
    report['api'][clsname] = [n for n in dir(cls) if any(x in n.lower() for x in ['graph','skelet','bone','anim','subobject','comment','tooltip','retarget'])] if cls else []
for path in ['/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter','/Game/ThirdPerson/Blueprints/Entrega/BP_PlayerEntrega','/Game/ThirdPerson/Blueprints/Aliado/BP_Hostage']:
    bp = unreal.load_asset(path); cdo = unreal.get_default_object(bp.generated_class())
    components = []
    for c in cdo.get_components_by_class(unreal.SceneComponent):
        row = {'name':c.get_name(),'class':c.get_class().get_name(),'location':str(c.relative_location),'rotation':str(c.relative_rotation)}
        if isinstance(c, unreal.SkeletalMeshComponent):
            m=c.get_skeletal_mesh_asset()
            row.update(mesh=m.get_path_name() if m else None,anim=str(c.anim_class),skeleton=m.skeleton.get_path_name() if m else None)
        components.append(row)
    report.setdefault('characters',{})[path] = components
with open(os.path.join(out,'inventory.json'),'w',encoding='utf-8') as f: json.dump(report,f,ensure_ascii=False,indent=2)
unreal.log('PROJECT_AUDIT '+json.dumps({'blueprints':len(report['blueprints']),'exported':sum(b['exported'] for b in report['blueprints']),'meshes':report['skeletal_meshes'],'characters':report['characters'],'api':report['api']},ensure_ascii=False))
