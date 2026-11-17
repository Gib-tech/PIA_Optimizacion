"""Record fixture evidence separately from owner acceptance and natural gameplay."""
from pathlib import Path
import json,re

root=Path(__file__).resolve().parent.parent
qa=root/'Intermediate/inspect/final-words'
read=lambda path:json.loads(path.read_text(encoding='utf-8-sig'))
proof={name:read(qa/(name+'.json')) for name in ['integration','modern','legacy-started','legacy-unstarted','physical-skip','interruption','qa-restored']}
proof['beacon_channels']=read(root/'Intermediate/inspect/beacon_sequence_assertions.json')
proof['assets']=read(root/'Intermediate/inspect/cinematics/assets.json')
proof['cold_reload']=read(root/'Intermediate/inspect/cinematics/cold-reload.json')
assert all(row['passed'] for row in proof.values())
assert 'LS_Revelacion' in proof['cold_reload']['sequences']
assert proof['beacon_channels']['complete_channel_rejected_before_revelation']
assert len(proof['beacon_channels']['orders'])==6
assert len(proof['integration']['orders'])==6
build=(root/'Deliverables/build.log').read_text(encoding='utf-8-sig',errors='replace')
assert 'BUILD SUCCESSFUL' in build and 'AutomationTool exiting with ExitCode=0' in build
counts=re.findall(r'(\d+) error\(s\), (\d+) warning\(s\)',build)
assert counts and all(int(e)==0 for e,w in counts),counts
archive=root/'Deliverables/TimeOut_Avance_18Nov2026.zip';assert archive.is_file()
result={'date':'2026-11-16','passed':True,'agent_prepared_tests_not_owner_acceptance':True,'new_natural_full_playthrough':False,
 'implementation':'Blueprint-only runtime; editor helper only for authoring','proof':proof,
 'package':{'platform':'Win64 Development','build_success':True,'cook_errors':int(counts[-1][0]),'cook_warnings':int(counts[-1][1]),'zip':str(archive.relative_to(root)),'zip_bytes':archive.stat().st_size,'crc_verified_by':'Tools/Archive-Delivery.py'},
 'pending_owner_acceptance':['Visual direction and difficulty of final horde','Performance on presentation PC'],
 'screenshots':['Intermediate/inspect/final-words/revelation.png','Intermediate/inspect/final-words/notice-expired.png']}
if (qa/'native-smoke.json').is_file():result['native_smoke']=read(qa/'native-smoke.json')
target=root/'docs/validation/final-words-2026-11-16.json'
target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(target)
print('VALIDATED',len(proof),'evidence groups; ZIP',archive.stat().st_size)
