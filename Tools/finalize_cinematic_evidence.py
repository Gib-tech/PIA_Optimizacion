"""Attach final cook/archive/native/cold-load proof to the cinematic evidence."""
from pathlib import Path
from zipfile import ZipFile
import json,re
root=Path(__file__).resolve().parent.parent
folder=root/'Intermediate/inspect/cinematics'
target=root/'docs/validation/cinematics-2026-11-16.json'
report=json.loads(target.read_text(encoding='utf-8'))
build=(root/'Deliverables/build.log').read_text(encoding='utf-8-sig',errors='replace')
assert 'BUILD SUCCESSFUL' in build
summary=re.search(r'Success - (\d+) error\(s\), (\d+) warning\(s\)',build)
assert summary and int(summary[1])==0
native=(folder/'native-final.log').read_text(encoding='utf-8-sig',errors='replace')
cuts=[line for line in native.splitlines() if 'Starting new camera cut:' in line]
assert len(cuts)==3,cuts
assert not re.search(r'Accessed None|Infinite loop|Fatal error|LogBlueprint: Error|LogScript: Error',native,re.I)
assert 'LogExit: Exiting.' in native
assert (folder/'native-final-user/Saved/SaveGames/TimeOut_Delivery_v1.sav').is_file()
cold=json.loads((folder/'cold-reload.json').read_text(encoding='utf-8-sig'));assert cold['passed']
zip_path=root/'Deliverables/TimeOut_Avance_18Nov2026.zip'
with ZipFile(zip_path) as z:
    names=z.namelist()
    assert 'Windows/Terreno.exe' in names
    assert not any('Saved' in Path(name).parts or name.lower().endswith('.pdb') or 'BlueprintBuildBridge' in name for name in names)
report['package']={'status':'verified','configuration':'Win64 Development','build_exit_code':0,'cook_errors':int(summary[1]),'cook_warnings':int(summary[2]),'warnings':'Existing SpawnSystemAttached Scale pin and 14 Manny pose warnings',
                   'zip':'Deliverables/TimeOut_Avance_18Nov2026.zip','zip_bytes':zip_path.stat().st_size,'zip_crc_verified_by_archive_script':True,'zip_excludes_saved_pdb_editor_helper':True,
                   'native_smoke':{'fresh_isolated_user_dir':True,'intro_camera_cuts':len(cuts),'spanish_subtitles_observed':True,'normal_hud_and_checkpoint_observed_after_intro':True,'pause_after_intro_observed':True,'clean_exit':True,'accessed_none_or_script_errors':False,'limit':'Intro/menu/return smoke; endings verified in isolated PIE fixtures',
                                   'runtime_notice':'Original player startup reports Health widget already added; no cinematic script error'},'cold_reload':cold}
target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=[line for line in build.splitlines() if any(s in line for s in ['Success - ','BUILD SUCCESSFUL','AutomationTool exiting with ExitCode=','BuildCookRun time:'])]
lines+=['ZIP_BYTES '+str(zip_path.stat().st_size),'ZIP_CRC_PASS; no Saved/PDB/editor helper','Native intro 3 camera cuts, subtitles, HUD/checkpoint and pause observed; clean exit','Native endpoints not played through; prepared PIE endpoint fixtures passed','Normal cold reload: helper absent, one resident controller, 3 sequences, no PIE/dirty packages']
(root/'docs/validation/cinematics-build-2026-11-16.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('CINEMA_FINAL_EVIDENCE_READY',zip_path.stat().st_size)
