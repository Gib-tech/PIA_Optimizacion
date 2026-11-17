import struct,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent;out=root/'Intermediate/inspect/team-models';rows=[]
for filename in ['waste_construction_lumber.glb','destroyed_car_1_raw_scan.glb']:
 p=Path.home()/'Downloads'/filename
 with p.open('rb') as f:
  head=f.read(20);length=struct.unpack_from('<I',head,12)[0];data=json.loads(f.read(length))
 row={'file':filename,'asset':data.get('asset'),'extras':data.get('extras')};rows.append(row);print(json.dumps(row,ensure_ascii=False))
(out/'source-attribution.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
