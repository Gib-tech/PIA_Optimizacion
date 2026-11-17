"""Texturas repetibles de corteza y copa para el árbol LOD del acceso."""
from pathlib import Path
import math
import bpy
from mathutils import noise, Vector

out=Path(__file__).resolve().parents[1]/'ArtSource'/'ArbolAcceso'
out.mkdir(exist_ok=True)
size=512
def seamless(u,v,fx,fy,z):
    # Mezclar bordes opuestos permite repetir la muestra en la malla.
    def n(x,y):return noise.noise_vector(Vector((x*fx,y*fy,z)))[0]
    a=u*u*(3-2*u);b=v*v*(3-2*v)
    return (1-b)*((1-a)*n(u,v)+a*n(u-1,v))+b*((1-a)*n(u,v-1)+a*n(u-1,v-1))
for bark in (True, False):
    name='T_CortezaAcceso' if bark else 'T_FollajeAcceso'
    img=bpy.data.images.new(name,width=size,height=size,alpha=False)
    pixels=[]
    for y in range(size):
        for x in range(size):
            u,v=x/size,y/size
            if bark:
                bend=.018*seamless(u,v,5,3,8)
                ridge=abs(seamless(u+bend,v,30,4,1))
                detail=seamless(u,v,93,16,2)
                value=min(1,max(0,1.9*ridge+.18*detail))
                dark=(.18,.105,.062);light=(.54,.40,.27)
            else:
                value=min(1,max(0,.46+.55*seamless(u,v,9,12,4)+.39*seamless(u,v,40,45,7)))
                dark=(.09,.18,.095);light=(.43,.56,.23)
            pixels.extend([a+(b-a)*value for a,b in zip(dark,light)]+[1])
    img.pixels.foreach_set(pixels);img.filepath_raw=str(out/(name+'.png'));img.file_format='PNG';img.save()
