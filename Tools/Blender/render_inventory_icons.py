"""Iconos del inventario renderizados desde los modelos originales del proyecto."""
import bpy, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'Tools/ArtSource/Inventario';OUT.mkdir(parents=True,exist_ok=True)
for name in ['BotiquinTemporal','CeldaTemporal','CreditoCronal']:
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/'Tools/ArtSource/Complementos'/(name+'.blend')))
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
 for o in objects:o.scale*=.01
 bpy.context.view_layer.update()
 points=[o.matrix_world@Vector(c) for o in objects for c in o.bound_box];lo=Vector(tuple(min(p[i] for p in points) for i in range(3)));hi=Vector(tuple(max(p[i] for p in points) for i in range(3)));center=(lo+hi)/2;radius=max(hi-lo)
 scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.eevee.use_gtao=True;scene.eevee.gtao_distance=.3;scene.eevee.use_soft_shadows=True;scene.render.film_transparent=True
 scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8'
 scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.view_settings.exposure=0;scene.view_settings.gamma=1
 if not scene.world:scene.world=bpy.data.worlds.new('Estudio')
 scene.world.color=(.2,.2,.2)
 bpy.ops.object.camera_add(location=center+Vector((1.3,-2,1.5))*radius);cam=bpy.context.object;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=radius*1.65;scene.camera=cam
 for title,offset,power,col,size in [('Principal',(-2,-3,4),240,(.85,.94,1),2),('Relleno',(2,-1,1),110,(.35,.8,1),1.6),('Borde',(1,3,3),280,(1,.65,.3),1.4)]:
  bpy.ops.object.light_add(type='AREA',location=center+Vector(offset)*radius);lamp=bpy.context.object;lamp.name=title;lamp.data.energy=power*radius*radius*6;lamp.data.color=col;lamp.data.shape='DISK';lamp.data.size=size*radius;lamp.rotation_euler=(center-lamp.location).to_track_quat('-Z','Y').to_euler()
 for m in bpy.data.materials:
  if m.use_nodes and 'Cian' in m.name:
   p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Emission'].default_value=(.02,.5,.8,1);p.inputs['Emission Strength'].default_value=.5
 scene.render.filepath=str(OUT/('T_Inv_'+name+'.png'));bpy.ops.render.render(write_still=True)
 print('INVENTORY_ICON_RENDERED',name)
