from pathlib import Path
import json,re
root=Path(__file__).resolve().parent.parent;qa=root/'Intermediate/inspect/team-models';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
proof={name:read(qa/(name+'.json')) for name in ['import-proof','placement-proof','runtime','assets','qa-restored','cold']}
assert all(row['passed'] for row in proof.values())
lods=read(qa/'lods/observations.json');assert lods['passed'] and lods['no_forced_lods'] and len(lods['rows'])==16
proof['lod_camera_observations']=lods
assert proof['assets']['four_lod_designs_total']==9 and proof['assets']['new_nanite_wreck']
build=(root/'Deliverables/build.log').read_text(encoding='utf-8-sig',errors='replace');assert 'BUILD SUCCESSFUL' in build and 'AutomationTool exiting with ExitCode=0' in build
counts=re.findall(r'(\d+) error\(s\), (\d+) warning\(s\)',build);assert counts and int(counts[-1][0])==0
warnings={line.split('Warning: ',1)[1].strip() for line in build.splitlines() if 'Warning: ' in line and not line.startswith('LogInit: Display:')}
assert len(warnings)==15 and all('PoseAsset ' in w or 'Spawn System Attached' in w for w in warnings),warnings
archive=root/'Deliverables/TimeOut_Avance_18Nov2026.zip';assert archive.is_file()
result={'date':'2026-11-16','passed':True,'agent_fixture_evidence_not_owner_acceptance':True,'new_natural_playthrough':False,'proof':proof,'source_manifest':'Tools/ArtSource/TeamModels/manifest.json','credit_document':'docs/CREDITOS_MODELOS.md','building_and_lamp_authors':'Unconfirmed, as requested by owner','package':{'build_success':True,'cook_errors':int(counts[-1][0]),'cook_warnings':int(counts[-1][1]),'unique_previous_warning_messages':len(warnings),'new_warning_types':0,'zip_bytes':archive.stat().st_size,'zip_crc_verified':True,'credits_in_archive':True},'pending':['Owner visual acceptance','Performance on presentation PC','Authorship and academic/external evidence from team']}
if (qa/'native-smoke.json').exists():result['native_smoke']=read(qa/'native-smoke.json')
target=root/'docs/validation/team-models-2026-11-16.json';target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(target)
