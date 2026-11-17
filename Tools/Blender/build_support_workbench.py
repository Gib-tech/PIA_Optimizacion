"""Mesa de apoyo original con superficie real y colisiones UCX por pieza."""
import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tools/ArtSource/Complementos'
palette=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))['palette']
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
for name,col in palette.items():
 m=bpy.data.materials.new('M_Apoyo_'+name);m.diffuse_color=col;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.4;p.inputs['Metallic'].default_value=.65 if name in ['Metal','Bronce'] else .05
parts=[];colliders=[]
def box(name,loc,dim,mat,collision=True,bevel=.7):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if collision:
  c=o.copy();c.data=o.data.copy();bpy.context.collection.objects.link(c);c.name='UCX_SM_ConsolaTecnico_'+str(len(colliders)).zfill(2);colliders.append(c)
 o.data.materials.append(bpy.data.materials['M_Apoyo_'+mat])
 if bevel:
  mod=o.modifiers.new('Cantos','BEVEL');mod.width=bevel;mod.segments=3;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 parts.append(o)
box('Superficie_metalica',(0,0,89),(140,78,7),'Metal',True,1.3) # cara superior Z=92,5 cm
box('Borde_frontal',(0,-38,87),(138,3,8),'Bronce')
for x in [-57,57]:
 for y in [-26,26]:box('Pata',(x,y,43),(7,7,86),'Goma')
box('Travesano',(0,25,22),(116,6,6),'Metal')
box('Base_monitor',(40,24,95),(28,18,5),'Goma')
box('Soporte_monitor',(40,27,104),(5,5,16),'Metal')
box('Monitor',(40,27,120),(33,5,25),'Goma')
box('Pantalla',(40,23.8,120),(29,1.6,21),'Cian',False,.4)
box('Teclado',(38,7,94),(29,14,3),'Goma')
for x in range(27,52,6):
 for y in [3,8,13]:box('Tecla',(x,y,96),(4,3,1),'Blanco',False,.2)
box('Panel_suministros',(-41,30,94.5),(38,4,4),'Cian',False)
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();main=bpy.context.object;main.name='SM_ConsolaTecnico';bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
for c in colliders:c.select_set(True)
bpy.ops.export_scene.fbx(filepath=str(OUT/'SM_ConsolaTecnico.fbx'),use_selection=True,object_types={'MESH'},add_leaf_bones=False,bake_anim=False,axis_forward='-Y',axis_up='Z',apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',bake_space_transform=True)
for c in colliders:c.hide_render=True;c.hide_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ConsolaTecnico.blend'))
p=OUT/'manifest.json';data=json.loads(p.read_text(encoding='utf-8'))
for row in data['models']:
 if row['name']=='SM_ConsolaTecnico':row.update(polygons=len(main.data.polygons),authoring='Mesa original asistida, build_support_workbench.py; reemplaza el kiosco anterior.',support_top_cm=92.5,ucx_hulls=len(colliders))
p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');print('WORKBENCH_READY',len(colliders),'UCX hulls')
