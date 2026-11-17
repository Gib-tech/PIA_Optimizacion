"""Deterministic original score stems, 48 kHz mono PCM. No third-party recordings."""
from pathlib import Path
import wave, json
import numpy as np

OUT=Path(__file__).resolve().parent/'ArtSource'/'Cinematics'
OUT.mkdir(parents=True,exist_ok=True)
RATE=48000
def score(name,duration,notes):
    t=np.arange(int(duration*RATE))/RATE
    # Airy D/A drone, deliberately quiet under the three-note beacon motif.
    data=.035*np.sin(2*np.pi*73.416*t)+.018*np.sin(2*np.pi*110*t)
    data*=np.minimum(t/1.5,1)*np.minimum((duration-t)/1.2,1)
    for at,freq,length,gain in notes:
        x=t-at;u=np.maximum(x,0)
        env=(1-np.exp(-u*18))*np.exp(-u*1.5/max(length,.2))*(x>=0)*(x<length)
        tone=np.sin(2*np.pi*freq*u)+.3*np.sin(2*np.pi*2*freq*u)+.12*np.sin(2*np.pi*3*freq*u)
        data+=gain*tone*env
    data*=np.clip(t/.08,0,1)*np.clip((duration-t)/.8,0,1)
    data=np.tanh(data)*.8
    pcm=(np.clip(data,-1,1)*32767).astype('<i2')
    with wave.open(str(OUT/(name+'.wav')),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(pcm.tobytes())
    return {'name':name,'duration':duration,'rms':float(np.sqrt(np.mean(data**2))),'peak':float(np.max(np.abs(data)))}
report=[
score('SW_CinemaIntro',18,[(.8,293.665,3,.13),(3,349.228,3,.11),(5.2,440,4,.12),(7,293.665,3,.10),(10,349.228,3,.10),(12,440,4,.13),(15,587.33,3,.09)]),
score('SW_CinemaDefeat',8,[(.1,440,2.6,.12),(2,349.228,2.5,.12),(4,293.665,3.5,.13),(5.2,146.832,2.6,.08)]),
score('SW_CinemaVictory',14,[(.4,293.665,3,.12),(2.2,349.228,3,.12),(4,440,4,.13),(6.2,587.33,5,.10),(8,293.665,5,.09),(8,349.228,5,.08),(8,440,5,.08),(10.5,880,3,.05)]),
score('SW_CinemaRevelation',12,[(.3,146.832,4,.12),(1.2,220,3,.07),(4.2,293.665,3,.11),(6.1,349.228,3,.10),(8,440,3,.10),(9.7,146.832,2.3,.09)])]
(OUT/'score_manifest.json').write_text(json.dumps({'authorship':'Original procedural synthesis for TIME OUT','sample_rate':RATE,'scores':report},indent=2),encoding='utf-8')
print(json.dumps(report))
