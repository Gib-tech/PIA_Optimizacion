from pathlib import Path
import math, random, wave, array

out = Path(__file__).resolve().parent / 'AudioSource'
rate = 32000

def save(name, samples):
    frames = array.array('h',(round(max(-1, min(1, x)) * 32767) for x in samples))
    with wave.open(str(out / (name+'.wav')), 'wb') as wav:
        wav.setparams((1,2,rate,0,'NONE','not compressed'))
        wav.writeframes(frames.tobytes())

def alarm(t):
    # Dos llamadas ascendentes y una resolución más larga, con ataque suave.
    for start,duration,f in [(0,.14,590),(.21,.14,740),(.42,.27,930)]:
        u=t-start
        if 0<=u<duration:
            phase=math.tau*(f*u+115*u*u)
            env=min(1,u/.012,(duration-u)/.045)
            return env*(.42*math.sin(phase)+.09*math.sin(2*phase)+.07*math.sin(phase*.5))
    return 0

save('SW_HostageAlarm',(alarm(i/rate) for i in range(round(.70*rate))))
rng=random.Random(391)
samples=[]
low=0
for i in range(round(.37*rate)):
    t=i/rate
    low=.72*low+.28*rng.uniform(-1,1)
    droplets=sum(.09*math.exp(-65*(t-on))*math.sin(math.tau*(t-on)*(freq-680*(t-on)))
                 for on,freq in [(.015,820),(.066,570),(.11,1120),(.18,760)] if t>=on)
    samples.append(min(1,t/.009,(.37-t)/.035)*(.85*low*math.exp(-12*t)+droplets))
save('SW_PasoAgua',samples)
