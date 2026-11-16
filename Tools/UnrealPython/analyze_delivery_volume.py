"""Run outside the editor after verify_delivery_volume.py has exported both WAVs."""
from pathlib import Path
import wave,array,math,json
root=Path(__file__).resolve().parents[2];folder=root/'Intermediate/inspect/volume-audio'
values={}
for name in ['full','quarter']:
 with wave.open(str(folder/(name+'.wav')),'rb') as f:
  assert f.getsampwidth()==2
  samples=array.array('h',f.readframes(f.getnframes()))
  values[name]=math.sqrt(sum(x*x for x in samples)/len(samples))/32768
assert values['full']>0.00001,values
ratio=values['quarter']/values['full']
assert .15<ratio<.35,values
out={'passed':True,'method':'Master submix WAV recording with repeated SW_Text at volume 1 and 0.25','normalized_rms':values,'quarter_to_full_ratio':ratio}
(root/'Intermediate/inspect/delivery_volume_assertions.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out))
