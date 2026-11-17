"""Read the four supplied meshes before choosing scale, materials and budgets."""
import bpy,json,os,hashlib
from mathutils import Vector
root=os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))
out=os.path.join(root,'Intermediate/inspect/team-models');os.makedirs(out,exist_ok=True)
rows=[]
for filename in ['edificio.fbx','Faro.fbx','waste_construction_lumber.glb','destroyed_car_1_raw_scan.glb','realistic_tree.glb']:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 path=os.path.join(out,filename) if filename=='realistic_tree.glb' else os.path.join(os.path.expanduser('~/Downloads'),filename)
 if filename.endswith('.fbx'):bpy.ops.import_scene.fbx(filepath=path)
 else:bpy.ops.import_scene.gltf(filepath=path)
 objects=[o for o in bpy.context.scene.objects if o.type=='MESH'];points=[o.matrix_world@Vector(c) for o in objects for c in o.bound_box]
 lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
 meshes=[]
 for o in objects:
  o.data.calc_loop_triangles()
  meshes.append({'name':o.name,'triangles':len(o.data.loop_triangles),'vertices':len(o.data.vertices),'materials':[m.name if m else None for m in o.data.materials]})
 mats=[]
 for m in bpy.data.materials:
  nodes=[]
  if m.use_nodes:
   for n in m.node_tree.nodes:
    row={'type':n.type}
    if n.type=='TEX_IMAGE':row.update(image=n.image.name if n.image else None)
    if n.type=='BSDF_PRINCIPLED':row.update(base=list(n.inputs['Base Color'].default_value),roughness=n.inputs['Roughness'].default_value,metallic=n.inputs['Metallic'].default_value)
    nodes.append(row)
  mats.append({'name':m.name,'nodes':nodes})
 row={'source':filename,'sha256':hashlib.sha256(open(path,'rb').read()).hexdigest(),'bounds_min':lo,'bounds_max':hi,'size':[hi[i]-lo[i] for i in range(3)],'meshes':meshes,'materials':mats,'images':[{'name':im.name,'size':list(im.size),'packed':bool(im.packed_file),'filepath':im.filepath} for im in bpy.data.images]}
 rows.append(row);print('TEAM_MODEL_SURVEY',filename,sum(x['triangles'] for x in meshes),row['size'])
with open(os.path.join(out,'source-survey.json'),'w',encoding='utf-8') as f:json.dump(rows,f,indent=2,ensure_ascii=False)
