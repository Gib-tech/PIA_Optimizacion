"""Procedural two-channel branching fracture mask for the door material (R=wide, G=core)."""
from pathlib import Path
import random,math,struct
n=512;rng=random.Random(1815);wide=bytearray(n*n);core=bytearray(n*n)
def line(x1,y1,x2,y2,width):
 steps=max(1,round(math.hypot(x2-x1,y2-y1)*2))
 for s in range(steps+1):
  t=s/steps;x=x1+(x2-x1)*t;y=y1+(y2-y1)*t
  for yy in range(max(0,int(y-width-2)),min(n,int(y+width+3))):
   for xx in range(max(0,int(x-width-2)),min(n,int(x+width+3))):
    d=math.hypot(xx-x,yy-y);i=yy*n+xx
    wide[i]=max(wide[i],round(255*max(0,min(1,width+1.5-d))))
    core[i]=max(core[i],round(255*max(0,min(1,width-.2-d))))
for cx,cy in [(256,265),(140,350),(370,350),(80,80)]:
 for branch in range(7):
  angle=branch*math.tau/7+rng.uniform(-.2,.2);x,y=cx,cy
  for j in range(rng.randint(5,9)):
   angle+=rng.uniform(-.48,.48);distance=rng.uniform(15,34);nx=x+math.cos(angle)*distance;ny=y+math.sin(angle)*distance
   line(x,y,nx,ny,max(.7,2.4-j*.2))
   if j in [2,4]:
    a=angle+rng.choice([-1,1])*.9;line(nx,ny,nx+math.cos(a)*rng.uniform(18,45),ny+math.sin(a)*rng.uniform(18,45),.8)
   x,y=nx,ny
path=Path(__file__).resolve().parent/'ArtSource'/'UI'/'T_DoorCracks.tga';path.parent.mkdir(parents=True,exist_ok=True)
pixels=bytearray()
for r,g in zip(wide,core):pixels.extend((0,g,r,255))
path.write_bytes(struct.pack('<BBBHHBHHHHBB',0,0,2,0,0,0,0,0,n,n,32,0x28)+pixels)
print(path)
