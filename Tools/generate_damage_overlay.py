"""Generate a seamless alpha mask for the HUD's brief damage pulse."""
from pathlib import Path
import struct

size=256
out=Path(__file__).resolve().parent/'ArtSource'/'UI'/'T_DamageCorners.tga'
out.parent.mkdir(parents=True,exist_ok=True)
pixels=bytearray()
for y in range(size):
    for x in range(size):
        u=abs(2*x/(size-1)-1);v=abs(2*y/(size-1)-1)
        alpha=max(0,(u*v-.12)/.88)**1.65
        pixels.extend((255,255,255,round(255*alpha)))
out.write_bytes(struct.pack('<BBBHHBHHHHBB',0,0,2,0,0,0,0,0,size,size,32,0x28)+pixels)
print(out)
