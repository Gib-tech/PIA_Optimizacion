"""Name native screenshots and verify the rendered red/green/blue LOD stages."""
from pathlib import Path
import json
from PIL import Image
root=Path(__file__).resolve().parent.parent;folder=root/'Intermediate/inspect/team-models/lods';path=folder/'observations.json';result=json.loads(path.read_text())
assert result['passed'] and len(result['rows'])==16
for row in result['rows']:
 target=folder/row['file']
 matches=list(folder.glob(target.stem+'*.png'));assert matches,row
 source=max(matches,key=lambda p:p.stat().st_mtime)
 if source!=target:
  assert source.resolve().parent==folder.resolve() and target.resolve().parent==folder.resolve();source.replace(target)
 im=Image.open(target).convert('RGB');cx,cy=im.width//2,im.height//2;crop=im.crop((cx-24,cy-24,cx+25,cy+25));pixels=[crop.getpixel((x,y)) for y in range(crop.height) for x in range(crop.width)];stage=row['requested_step']
 if stage:
  counts=sum(p[stage-1]>55 and p[stage-1]>max(p[k] for k in range(3) if k!=stage-1)*1.7 for p in pixels)
  assert counts>=3,(row,counts)
  row['rendered_lod_color']=['white','red','green','blue'][stage];row['center_color_pixels']=counts
 else:row['rendered_lod_color']='white (visual inspection)'
result['rendered_color_checks_passed']=True;path.write_text(json.dumps(result,indent=2)+'\n');print('TEAM_LOD_RENDERED_COLORS_VALIDATED',len(result['rows']))
