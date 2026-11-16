"""Original soft retro vocal syllables, with formant-shaped harmonics and tiny pitch bends."""
from pathlib import Path
import math,random,struct,wave
root=Path(__file__).resolve().parent/'AudioSource';rate=24000
for index,(f0,formants) in enumerate([(154,(530,1100,2400)),(168,(670,1250,2450)),(143,(440,1050,2200))]):
 rng=random.Random(714+index);length=.068;audio=[];phase=0
 weights=[sum(gain*math.exp(-.5*((h*f0-center)/width)**2) for center,width,gain in zip(formants,(180,260,400),(1,.65,.25)))/h**.4 for h in range(1,23)]
 normal=sum(weights)
 for i in range(round(rate*length)):
  t=i/rate;phase+=2*math.pi*f0*(1+.055*math.sin(math.pi*t/length))/rate
  voiced=sum(g*math.sin(h*phase) for h,g in enumerate(weights,1))/normal
  env=min(1,t/.007)*min(1,(length-t)/.015)
  audio.append(.42*env*(voiced+.025*rng.uniform(-1,1)))
 path=root/('SW_HostageVoice_'+str(index+1)+'.wav')
 with wave.open(str(path),'wb') as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(b''.join(struct.pack('<h',round(v*32767)) for v in audio))
 print(path)
