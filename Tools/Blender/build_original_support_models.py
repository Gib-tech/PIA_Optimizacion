"""Cinco diseños originales de suministros y una cubeta de estanque, en cm."""
import bpy,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tools/ArtSource/Complementos';OUT.mkdir(parents=True,exist_ok=True)
palette={'Metal':(.07,.11,.14,1),'Goma':(.012,.018,.022,1),'Cian':(.04,.65,.9,1),'Blanco':(.8,.85,.86,1),'Rojo':(.6,.035,.018,1),'Bronce':(.5,.24,.055,1),'Concreto':(.24,.22,.17,1)}
rows=[]
def start():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
 for name,color in palette.items():
  m=bpy.data.materials.new('M_Apoyo_'+name);m.diffuse_color=color;m.use_nodes=True
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=.38;p.inputs['Metallic'].default_value=.65 if name in ['Metal','Bronce'] else .05
def finish(name):
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();obj=bpy.context.object;obj.name='SM_'+name
 bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
 bpy.ops.export_scene.fbx(filepath=str(OUT/(obj.name+'.fbx')),use_selection=True,object_types={'MESH'},add_leaf_bones=False,bake_anim=False,axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',bake_space_transform=True)
 rows.append({'name':obj.name,'materials':[m.name for m in obj.data.materials],'polygons':len(obj.data.polygons),'authoring':'Geometría original generada por build_original_support_models.py; no recurso Fab ni plantilla UE.'})
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/(name+'.blend')))
def cube(name,loc,size,mat,bevel=.7):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(bpy.data.materials['M_Apoyo_'+mat])
 if bevel:
  mod=o.modifiers.new('Cantos','BEVEL');mod.width=bevel;mod.segments=3;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 return o
def cylinder(name,loc,r,depth,mat,vertices=32):
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=name;o.data.materials.append(bpy.data.materials['M_Apoyo_'+mat]);m=o.modifiers.new('Bisel','BEVEL');m.width=.6;m.segments=2;bpy.ops.object.modifier_apply(modifier=m.name);return o
start();cube('Maletin',(0,0,12),(32,24,20),'Blanco',2)
cube('Junta',(0,0,12),(32.3,24.3,2),'Goma',.4);cube('Cruz_H',(0,-12.4,14),(17,.8,4),'Rojo',.3);cube('Cruz_V',(0,-12.4,14),(4,.8,14),'Rojo',.3)
cube('Asa',(0,0,25),(14,4,3),'Metal',1)
for x in [-10,10]:cube('Cierre',(x,-12.5,21),(3,2,4),'Metal',.4)
finish('BotiquinTemporal')
start();cylinder('Nucleo',(0,0,20),8,32,'Cian');cylinder('Base',(0,0,3),10,6,'Metal');cylinder('Cabeza',(0,0,37),10,6,'Metal')
for a in [0,math.pi/2,math.pi,3*math.pi/2]:cube('Nervadura',(9*math.cos(a),9*math.sin(a),20),(2,2,28),'Goma',.5)
finish('CeldaTemporal')
start();cylinder('Credito',(0,0,2),12,4,'Bronce',48);cylinder('Medallon',(0,0,4.2),9,1,'Metal',48)
for x in [-3,3]:cube('Marca',(x,0,5),(1.6,10,1),'Cian',.25)
finish('CreditoCronal')
start();cube('Caja',(0,0,27),(75,48,50),'Metal',2)
for x in [-33,33]:cube('Costilla',(x,0,27),(5,51,54),'Goma',.7)
cube('Cierre',(0,-25,28),(18,3,9),'Cian',1);cube('Tapa',(0,0,54),(76,50,5),'Goma',1)
for y in [-16,16]:cube('Refuerzo',(0,y,57),(69,4,3),'Blanco',.5)
finish('CajaSuministros')
start();cube('Pedestal',(0,0,7),(70,55,14),'Goma',2);cube('Cuerpo',(0,0,57),(54,38,92),'Metal',3)
panel=cube('Pantalla',(0,-21,92),(44,4,32),'Cian',2);panel.rotation_euler.x=math.radians(12)
cube('Teclado',(0,-27,62),(46,24,4),'Goma',1)
for x in range(-16,20,8):
 for y in [-32,-24]:cube('Tecla',(x,y,65),(5,5,2),'Blanco',.4)
for z in [27,37,47]:cube('Ranura',(0,-20,z),(34,2,3),'Goma',.4)
finish('ConsolaTecnico')
start();cylinder('Fondo',(0,0,-52),310,18,'Concreto',64)
# Cubeta circular abierta: paredes sólidas, sin una tapa encima del agua.
verts=[];faces=[];N=96
for z,r in [(-50,310),(15,310),(-50,285),(15,285)]:
 for j in range(N):a=math.tau*j/N;verts.append((r*math.cos(a),r*math.sin(a),z))
for j in range(N):
 k=(j+1)%N
 for a,b in [(0,1),(2,3),(1,3)]:faces.append((a*N+j,a*N+k,b*N+k,b*N+j))
mesh=bpy.data.meshes.new('Cubeta');mesh.from_pydata(verts,[],faces);obj=bpy.data.objects.new('Borde',mesh);bpy.context.collection.objects.link(obj);mesh.materials.append(bpy.data.materials['M_Apoyo_Concreto'])
finish('EstanqueRetencion')
(OUT/'manifest.json').write_text(json.dumps({'palette':palette,'models':rows},indent=2,ensure_ascii=False),encoding='utf-8')
print('ORIGINAL_SUPPORT_MODELS_READY',len(rows))
