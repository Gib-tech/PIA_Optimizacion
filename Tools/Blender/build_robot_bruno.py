"""Robot BRUNO propio: chasis anclado, cabeza y aro móviles. Centímetros."""
import bpy,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tools/ArtSource/RobotBRUNO';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
palette={'Chasis':(.045,.085,.11,1),'Metal':(.32,.37,.4,1),'Goma':(.008,.012,.017,1),'Cobre':(.38,.19,.065,1),'Ceramica':(.54,.61,.62,1),'Energia':(.025,.7,1,1),'Ambar':(1,.35,.025,1)}
for name,color in palette.items():
 m=bpy.data.materials.new('M_BRUNO_'+name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Metallic'].default_value=.75 if name in ['Metal','Cobre','Chasis'] else .05;p.inputs['Roughness'].default_value=.34 if name!='Goma' else .75
 if name in ['Energia','Ambar']:p.inputs['Emission'].default_value=color;p.inputs['Emission Strength'].default_value=2
parts={};current='Chasis'
def finish_obj(o,name,mat,bevel=0):
 o.name=name;o.data.materials.append(bpy.data.materials['M_BRUNO_'+mat])
 if bevel:
  b=o.modifiers.new('Cantos_mecanizados','BEVEL');b.width=bevel;b.segments=3;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=b.name)
 if o.type=='MESH':
  for poly in o.data.polygons:poly.use_smooth=len(poly.vertices)<5
 parts.setdefault(current,[]).append(o);return o
def box(name,loc,size,mat,bevel=.6):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish_obj(o,name,mat,bevel)
def cyl(name,loc,r,depth,mat,axis='Z',vertices=32):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc);o=bpy.context.object
 if axis=='Y':o.rotation_euler.x=math.pi/2
 if axis=='X':o.rotation_euler.y=math.pi/2
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return finish_obj(o,name,mat,.35)
def bar(name,a,b,r,mat):
 from mathutils import Vector
 v=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=v.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();bpy.ops.object.transform_apply(location=False,rotation=True,scale=True);return finish_obj(o,name,mat,.2)
# Base atornillada: el robot depende de una conexión física al recinto.
cyl('Placa_de_anclaje',(0,0,3),34,6,'Chasis',vertices=64)
cyl('Corona_de_servicio',(0,0,8),28,4,'Metal',vertices=48)
for x in [-23,23]:
 for y in [-16,16]:cyl('Tornillo_de_fijacion',(x,y,7),2.8,2.2,'Cobre',vertices=6)
box('Pedestal',(0,4,23),(34,34,30),'Chasis',2)
for x in [-17,17]:bar('Piston_estabilizador',(x,10,12),(x,0,58),3.2,'Metal')
cyl('Rodamiento_cintura',(0,0,49),17,12,'Goma')
cyl('Cintura',(0,0,55),20,5,'Cobre')
box('Torso',(0,0,85),(48,30,51),'Chasis',5)
box('Placa_pectoral',(0,-17,91),(40,5,32),'Ceramica',2)
box('Panel_identidad',(0,-20,98),(31,2,12),'Goma',.7)
bpy.ops.object.text_add(location=(-12,-21.3,96),rotation=(math.pi/2,0,0));label=bpy.context.object;label.data.body='BRUNO';label.data.size=6.2;label.data.extrude=.12;label.data.align_x='LEFT';bpy.ops.object.convert(target='MESH');finish_obj(bpy.context.object,'Identidad_BRUNO','Energia')
for x in [-10,0,10]:box('Carga_LED',(x,-20.2,83),(5,1.8,4),'Energia',.4)
box('Salida_fabricacion',(0,-17,68),(28,5,9),'Goma',1)
box('Bandeja_suministros',(0,-24,62),(33,18,3),'Metal',1)
for z in [78,85,92,99]:box('Rejilla_trasera',(0,16,z),(27,2,2),'Goma',.3)
for side in [-1,1]:
 x=side*30;cyl('Hombrera',(x,0,107),10,13,'Ceramica',axis='X')
 bar('Brazo_superior',(side*32,0,102),(side*41,-4,82),5.8,'Chasis')
 cyl('Articulacion_codo',(side*41,-4,79),7,12,'Cobre',axis='X')
 bar('Antebrazo',(side*41,-4,78),(side*35,-17,65),6.5,'Metal')
 box('Mano_pinza',(side*34,-20,61),(13,13,10),'Chasis',2)
 for off in [-4,4]:bar('Dedo_pinza',(side*34+off,-24,60),(side*34+off,-28,53),1.7,'Metal')
 cyl('Indicador_hombro',(side*37,-6,110),2.3,2,'Ambar',axis='Y')
bar('Conducto_energia',(18,13,12),(18,13,64),2.8,'Goma')
cyl('Cuello',(0,0,117),9,13,'Metal')
current='Cabeza'
box('Cabeza',(0,0,11),(39,27,25),'Chasis',5)
box('Visor',(0,-13,13),(32,5,13),'Goma',3)
for x in [-9,9]:
 cyl('Lente_marco',(x,-16.2,13),4.4,2.8,'Metal',axis='Y');cyl('Lente_optica',(x,-18,13),3.1,1.5,'Energia',axis='Y')
for x in [-22,22]:cyl('Auricular',(x,0,12),7,5,'Cobre',axis='X')
bar('Antena',(16,5,23),(18,5,36),1.1,'Metal');cyl('Baliza_antena',(18,5,37),2.5,4,'Ambar')
for x in [-5,0,5]:box('Vocalizador',(x,-14,3),(2,2,3),'Metal',.3)
current='Aro'
bpy.ops.mesh.primitive_torus_add(major_radius=22,minor_radius=1.8,major_segments=48,minor_segments=10,location=(0,0,0));finish_obj(bpy.context.object,'Aro_conversion','Cobre')
for a in range(0,360,90):
 r=math.radians(a);cyl('Emisor_aro',(22*math.cos(r),22*math.sin(r),0),2.8,3,'Energia')
rows=[]
for part,objects in parts.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();obj=bpy.context.object;obj.name='SM_BRUNO_'+part
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(OUT/(obj.name+'.fbx')),use_selection=True,object_types={'MESH'},add_leaf_bones=False,bake_anim=False,axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',bake_space_transform=True)
 rows.append({'part':part,'name':obj.name,'vertices':len(obj.data.vertices),'polygons':len(obj.data.polygons),'materials':[m.name for m in obj.data.materials]})
bpy.data.objects['SM_BRUNO_Cabeza'].location.z=121
bpy.data.objects['SM_BRUNO_Aro'].location.z=58
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Robot_BRUNO.blend'))
(OUT/'manifest.json').write_text(json.dumps({'authoring':'Modelo original asistido, receta Blender; no recurso de terceros. Un único robot articulado en tres piezas.','units':'centímetros','palette':palette,'parts':rows},ensure_ascii=False,indent=2),encoding='utf-8')
print('ROBOT_BRUNO_SOURCE_READY',rows)
