"""Publish bounded, reproducible evidence after the cinematic fixtures pass."""
from pathlib import Path
import json,shutil
root=Path(__file__).resolve().parent.parent
source=root/'Intermediate/inspect/cinematics'
target=root/'docs/validation'
names=['intro','defeat-player','defeat-hostage','victory','skip-first-person','continue','assets']
reports={name:json.loads((source/(name+'.json')).read_text(encoding='utf-8-sig')) for name in names}
assert all(row['passed'] for row in reports.values()),{k:v.get('error') for k,v in reports.items() if not v['passed']}
images=target/'cinematics-2026-11-16';images.mkdir(parents=True,exist_ok=True)
for name in ['intro-02','defeat-player-01','defeat-hostage-01','victory-02']:
    shutil.copy2(source/(name+'.png'),images/(name+'.png'))
result={'date':'2026-11-16','passed':True,'agent_verification_not_owner_acceptance':True,
        'scope':'Three in-engine cinematics; isolated terminal fixtures are not a natural playthrough',
        'reports':reports,'screenshots':[str(p.relative_to(target)).replace('\\','/') for p in images.glob('*.png')],
        'preserved':['Distinct Behavior Trees','ContactDamage 13.2','Existing extraction checks','Checkpoint schema 2','World Partition/Nanite/LOD'],
        'pending':['Owner visual acceptance','Presentation PC'],
        'package':{'status':'pending build and cold reload'}}
(target/'cinematics-2026-11-16.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('CINEMA_EVIDENCE_CONSOLIDATED',len(reports),'reports')
