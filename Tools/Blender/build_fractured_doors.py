"""Blender: matched cracked doors and true irregular fragments cut from the original geometry."""
from pathlib import Path
import bpy,bmesh,random,math,json
from mathutils import Vector

root=Path(__file__).resolve().parents[2];out=root/'Tools/ArtSource/Fracture';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'Tools/ArtSource/Progression/Progression.blend'))
interior=bpy.data.materials.new('FractureInterior');interior.diffuse_color=(.025,.018,.012,1)
interior.use_nodes=True;shader=interior.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=interior.diffuse_color;shader.inputs['Metallic'].default_value=.65;shader.inputs['Roughness'].default_value=.85

def clip(poly,n,c):
 result=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  da=a[0]*n[0]+a[1]*n[1]-c;db=b[0]*n[0]+b[1]*n[1]-c
  if da<=1e-7:result.append(a)
  if (da<0)!=(db<0):
   t=da/(da-db);result.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
 return result
def area(poly):return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))*.5)
def export(obj,name):
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 bpy.ops.export_scene.fbx(filepath=str(out/(name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False,use_mesh_modifiers=True)
manifest={'gap_cm':.7,'doors':[]}
for index,w,h,count in [(1,258,256,42),(2,344,333,56),(3,600,350,72)]:
 source=bpy.data.objects['SM_DoorPanel_%02d'%index];rng=random.Random(1818+index);seeds=[]
 while len(seeds)<count:
  if len(seeds)<count//4:
   angle=rng.random()*math.tau;r=rng.uniform(6,min(w,h)*.23);candidate=(math.cos(angle)*r,h*.48+math.sin(angle)*r)
  else:candidate=(rng.uniform(-w*.5,w*.5),rng.uniform(0,h))
  if all(math.dist(candidate,s)>10 for s in seeds):seeds.append(candidate)
 cells=[]
 for s in seeds:
  poly=[(-w*.5,0),(w*.5,0),(w*.5,h),(-w*.5,h)]
  for t in seeds:
   if t==s:continue
   n=(t[0]-s[0],t[1]-s[1]);c=(t[0]**2+t[1]**2-s[0]**2-s[1]**2)*.5;poly=clip(poly,n,c)
  cells.append(poly)
 assert abs(sum(area(p) for p in cells)-w*h)<.001
 entry={'index':index,'width':w,'height':h,'count':count,'coverage_area':sum(area(p) for p in cells),'pieces':[]};pieces=[]
 for i,poly in enumerate(cells):
  bm=bmesh.new();bm.from_mesh(source.data)
  for a,b in zip(poly,poly[1:]+poly[:1]):
   nx,nz=b[1]-a[1],a[0]-b[0];length=math.hypot(nx,nz);nx/=length;nz/=length
   plane=Vector((a[0]-nx*.35,0,a[1]-nz*.35))
   bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.0001,plane_co=plane,plane_no=Vector((nx,0,nz)),clear_outer=True,clear_inner=False)
   boundary=[e for e in bm.edges if e.is_boundary]
   if boundary:
    filled=bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
    for face in filled['faces']:face.material_index=len(source.data.materials)
  assert len(bm.faces)>3,(index,i)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
  cx=sum(p[0] for p in poly)/len(poly);cz=sum(p[1] for p in poly)/len(poly)
  for v in bm.verts:v.co-=Vector((cx,0,cz))
  name='SM_DoorShard_%02d_%02d'%(index,i);mesh=bpy.data.meshes.new(name);bm.to_mesh(mesh);bm.free()
  for material in source.data.materials:mesh.materials.append(material)
  mesh.materials.append(interior);mesh.update()
  obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj);obj.location=(0,0,0);export(obj,name)
  pieces.append((obj,cx,cz))
  entry['pieces'].append({'mesh':name,'offset':[cx,0,cz],'outline':[[x-cx,z-cz] for x,z in poly],'area':area(poly),'vertices':len(mesh.vertices),'faces':len(mesh.polygons)})
 # The first-hit mesh is literally the same shards, still held in place.
 bpy.ops.object.select_all(action='DESELECT')
 for obj,cx,cz in pieces:obj.location=(cx,0,cz);obj.select_set(True)
 bpy.context.view_layer.objects.active=pieces[0][0];bpy.ops.object.join();cracked=bpy.context.object
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');name='SM_DoorCracked_%02d'%index;cracked.name=name;export(cracked,name)
 entry['cracked_mesh']=name;manifest['doors'].append(entry)
 print('DOOR_FRACTURED',index,'shards',count,'coverage',entry['coverage_area'],flush=True)
(out/'fracture_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'FracturedDoors.blend'))
print('FRACTURED_DOORS_READY',flush=True)
