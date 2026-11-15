"""Generate small original UI cues and a quiet, seamless science-fiction ambience."""
from pathlib import Path
import math,random,struct,wave
ROOT=Path(__file__).resolve().parent/'AudioSource'
ROOT.mkdir(exist_ok=True)
RATE=24000
def save(name,samples):
    with wave.open(str(ROOT/(name+'.wav')),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE)
        f.writeframes(b''.join(struct.pack('<h',round(max(-1,min(1,x))*32767)) for x in samples))
def notes(name,sequence,gain=.24):
    result=[]
    for hz,length in sequence:
        for i in range(round(length*RATE)):
            t=i/RATE;env=min(1,t/.006)*min(1,(length-t)/.035)
            result.append(gain*env*(math.sin(2*math.pi*hz*t)+.18*math.sin(4*math.pi*hz*t))/1.18)
    save(name,result)
notes('SW_Text',[(580,.026)],.14)
notes('SW_Open',[(294,.055),(440,.07)],.18)
notes('SW_Rescue',[(330,.10),(440,.10),(554,.18)])
notes('SW_Alert',[(220,.12),(0,.05),(294,.15)],.21)
notes('SW_Clear',[(440,.09),(554,.09),(659,.22)])
notes('SW_Victory',[(330,.12),(440,.12),(554,.12),(659,.35)])
notes('SW_Defeat',[(294,.18),(247,.18),(165,.32)],.22)
random.seed(18)
save('SW_PlayerHurt',[(random.uniform(-1,1)*.18*math.exp(-i/RATE*24)+.19*math.sin(2*math.pi*(130-i/RATE*180)*i/RATE))*min(1,i/80)*math.exp(-i/RATE*10) for i in range(round(.22*RATE))])
seconds=12
save('SW_Ambience',[.13*(.65*math.sin(2*math.pi*60*i/RATE)+.2*math.sin(2*math.pi*120*i/RATE)+.15*math.sin(2*math.pi*(97/12)*i/RATE))*(.8+.2*math.cos(2*math.pi*i/RATE/seconds)) for i in range(seconds*RATE)])
print('Generated',len(list(ROOT.glob('*.wav'))),'original WAV cues')
