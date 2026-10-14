# Editor-side. Exports every AI-related asset to T3D text in Intermediate/inspect/live/.
# Read-only: it does not save or modify assets. Exports reflect what is loaded in the
# editor, so check the DIRTY line: if a package is dirty, the export differs from disk.
import os
import unreal

project = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
out_dir = os.path.join(project, "Intermediate", "inspect", "live")
os.makedirs(out_dir, exist_ok=True)

paths = [
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BT_EnemyIA",
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BB_EnemyIA",
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_Attack",
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_Defend",
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_HitSun",
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BTTask_Roam",
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BTService_LocatePlayer",
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BP_BaseEnemy",
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BP_IAController",
    "/Game/ThirdPerson/Blueprints/EnemigoIA/BPI_Enemy",
    "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter",
    "/Game/ThirdPerson/Blueprints/AnimNotifies/Enemy_Health/BPC_E_Health",
]
# Add new AI assets here when they exist (hostage, combat zone, charger).
extra = os.path.join(project, "Intermediate", "inspect", "extra_paths.txt")
if os.path.exists(extra):
    paths += [l.strip() for l in open(extra, encoding="utf-8") if l.strip()]

for path in paths:
    asset = unreal.load_asset(path)
    if asset is None:
        unreal.log_warning("EXPORT missing %s" % path)
        continue
    name = path.rsplit("/", 1)[-1]
    task = unreal.AssetExportTask()
    task.object = asset
    task.filename = os.path.join(out_dir, name + ".t3d")
    task.automated = True
    task.prompt = False
    task.replace_identical = True
    ok = unreal.Exporter.run_asset_export_task(task)
    unreal.log("EXPORT %s ok=%s" % (name, ok))

dirty = [p.get_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
unreal.log("DIRTY " + (", ".join(dirty) if dirty else "(none)"))
unreal.log("OUT " + out_dir)
