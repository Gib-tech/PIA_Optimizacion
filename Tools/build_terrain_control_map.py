"""Rasterize the authored ground plan into data masks; no new surface art."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFilter
root=Path(__file__).resolve().parents[1]
folder=root/'Tools/ArtSource/Atmosphere'
layout=json.loads((folder/'terrain_layout.json').read_text())
loX,loY,hiX,hiY=layout['bounds'];size=1024
def uv(point):return ((point[0]-loX)/(hiX-loX)*(size-1),(point[1]-loY)/(hiY-loY)*(size-1))
masks=[Image.new('L',(size,size),0) for _ in range(4)]
draw=[ImageDraw.Draw(m) for m in masks]
for path in layout['walkways']:
    width=round(path['width']/(hiX-loX)*size)
    points=[uv(p) for p in path['points']]
    draw[0].line(points,fill=255,width=width,joint='curve')
    for x,y in points:draw[0].ellipse((x-width/2,y-width/2,x+width/2,y+width/2),fill=255)
for name in ['depot','parking']:draw[1].polygon([uv(p) for p in layout[name]],fill=255)
for poly in layout['paved_polygons']:draw[2].polygon([uv(p) for p in poly],fill=255)
for x,y,r in layout['beacon_pads']:
    draw[2].ellipse((*uv((x-r,y-r)),*uv((x+r,y+r))),fill=255)
for poly in layout['rock_gardens']:draw[3].polygon([uv(p) for p in poly],fill=255)
# ~15 cm edge softness for soil/paving contact, rather than broad airbrushed bands.
image=Image.merge('RGBA',[m.filter(ImageFilter.GaussianBlur(1.2)) for m in masks])
image.save(folder/'T_TerrainUseMask.png')
print('Authored terrain control map:',folder/'T_TerrainUseMask.png')
