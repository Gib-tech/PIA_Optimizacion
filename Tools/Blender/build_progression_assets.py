"""Blender 3.6: fitted bunker doors, frames, bulkhead module and physical debris (centimeters)."""
import bpy,math,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Tools'/'ArtSource'/'Progression';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
materials={}
for name,color,metal in [('DoorSteel',(.14,.17,.19,1),.85),('DoorRust',(.25,.13,.07,1),.5),('DoorLight',(.9,.17,.03,1),.2),('WallStone',(.28,.32,.35,1),0)]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=color;bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=.78;materials[name]=m
parts=[];assets=[]
def cube(name,pos,dim,material,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(materials[material])
 if bevel:
  mod=o.modifiers.new('Worn edges','BEVEL');mod.width=bevel;mod.segments=1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 parts.append(o);return o
def bolt(x,y,z):
 bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=1.8,depth=3,location=(x,y,z),rotation=(math.pi/2,0,0));o=bpy.context.object;o.data.materials.append(materials['DoorSteel']);parts.append(o)
def finish(name):
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name=name;bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 bpy.ops.export_scene.fbx(filepath=str(OUT/(name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False,use_mesh_modifiers=True)
 assets.append(o);parts.clear()
for index,w,h in [(1,258,256),(2,344,333),(3,600,350)]:
 leaf=(w-2)/2
 for side in [-1,1]:
  x=side*(leaf/2+1);cube('Armored leaf',(x,0,h/2),(leaf,16,h),'DoorRust',1)
  for z in [10,h*.32,h*.67,h-10]:cube('Reinforcing rail',(x,-11,z),(leaf-7,6,8),'DoorSteel',.8)
  for edge in [-1,1]:
   ex=x+edge*(leaf/2-9);cube('Vertical binding',(ex,-11,h/2),(7,6,h-15),'DoorSteel',.6)
   for z in [13,h*.32,h*.67,h-13]:bolt(ex,-15,z)
  # A diagonal brace gives the broad leaf a recognizable forged structure.
  dx=leaf-30;dz=h-38;brace=cube('Diagonal brace',(x,-11,h/2),(math.hypot(dx,dz),5,6),'DoorSteel',.5);brace.rotation_euler[1]=-side*math.atan2(dz,dx)
 cube('Power lock',(0,-18,h*.48),(30,14,45),'DoorSteel',2)
 for x in [-8,0,8]:cube('Power veins',(x,-26,h*.48),(3,2,30),'DoorLight',.3)
 finish('SM_DoorPanel_%02d'%index)
 for side in [-1,1]:
  cube('Stone jamb',(side*(w/2+12),0,h/2),(24,76,h+10),'WallStone',2)
  cube('Steel jamb lining',(side*(w/2+1),-27,h/2),(6,16,h),'DoorSteel',1)
 cube('Stone lintel',(0,0,h+15),(w+48,76,30),'WallStone',2)
 cube('Lintel binding',(0,-30,h+4),(w+8,14,8),'DoorSteel',.7)
 finish('SM_DoorFrame_%02d'%index)
cube('Bulkhead stone',(0,0,210),(400,80,420),'WallStone',2)
cube('Top coping',(0,0,417),(402,86,12),'DoorSteel',1)
for x in [-194,194]:cube('Reinforced pier',(x,-43,210),(12,12,420),'DoorSteel',.8)
finish('SM_BulkheadModule')
cube('Door debris',(0,0,0),(100,16,100),'DoorRust',2)
cube('Torn reinforcing rail',(0,-11,10),(100,6,8),'DoorSteel',1)
finish('SM_DoorFragment')
for i,o in enumerate(assets):o.location.x=i*900
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Progression.blend'))
print('PROGRESSION_ART_READY',len(assets),'meshes',OUT)
