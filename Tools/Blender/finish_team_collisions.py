"""Give scenery simple static collision; orient the wreck along its long axis."""
import bpy,json,math,bmesh,sys
from pathlib import Path
from mathutils import Vector,Matrix
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tools/ArtSource/TeamModels';manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
selected=set(sys.argv[sys.argv.index('--')+1:]) if '--' in sys.argv else None
for row in manifest:
 if row.get('nanite'):continue
 if selected is not None and row['name'] not in selected:continue
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
 bpy.ops.import_scene.fbx(filepath=str(OUT/(row['mesh']+'.fbx')))
 o=next(o for o in bpy.context.scene.objects if o.type=='MESH' and not o.name.startswith('UCX_'))
 for old in list(bpy.context.scene.objects):
  if old.name.startswith('UCX_'):bpy.data.objects.remove(old,do_unlink=True)
 bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 bm=bmesh.new();bm.from_mesh(o.data);loose=[v for v in bm.verts if not v.link_faces]
 if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
 bm.to_mesh(o.data);bm.free()
 if row['name']=='AutoDestruido':
  data=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',data);xy=data.reshape(-1,3)[:,:2]
  vals,vecs=np.linalg.eigh(np.cov(xy.T));v=vecs[:,-1];angle=math.atan2(v[1],v[0]);mat=Matrix.Rotation(-angle,4,'Z')
  for p in o.data.vertices:p.co=mat@p.co
  row['long_axis_aligned']=True
 # Normalize again after FBX units and, for the car, the new orientation.
 coords=[v.co for v in o.data.vertices];lo=Vector([min(p[i] for p in coords) for i in range(3)]);hi=Vector([max(p[i] for p in coords) for i in range(3)])
 factor=row['target_cm']/((hi-lo).z if row['fit']=='height' else max((hi-lo).x,(hi-lo).y));origin=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z))
 for p in o.data.vertices:p.co=(p.co-origin)*factor
 o.data.update();coords=[v.co for v in o.data.vertices];lo=Vector([min(p[i] for p in coords) for i in range(3)]);hi=Vector([max(p[i] for p in coords) for i in range(3)])
 bpy.ops.object.select_all(action='DESELECT')
 if row['name'] in ['Farol','ArbolFab']:
  bottom=[v.co for v in o.data.vertices if v.co.z<15]
  cx=(min(v.x for v in bottom)+max(v.x for v in bottom))/2;cy=(min(v.y for v in bottom)+max(v.y for v in bottom))/2
  height=460 if row['name']=='Farol' else 300;radius=14 if row['name']=='Farol' else 22
  bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=radius,depth=height,location=(cx,cy,height/2));ucx=bpy.context.object
  row['collision']={'type':'trunk_or_pole_convex','radius_cm':radius,'height_cm':height}
 else:
  bpy.ops.mesh.primitive_cube_add(size=1,location=((lo+hi)*.5));ucx=bpy.context.object;ucx.dimensions=hi-lo;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  row['collision']={'type':'simple_box','size_cm':list(hi-lo)}
 ucx.name='UCX_'+row['mesh']+'_00';ucx.hide_render=True;o.select_set(True);ucx.select_set(True)
 bpy.ops.export_scene.fbx(filepath=str(OUT/(row['mesh']+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False,path_mode='STRIP')
 row['bounds_cm']={'min':list(lo),'max':list(hi)}
 if row['name']=='Farol':
  indices=[i for i,m in enumerate(row['materials']) if m['original']=='Material.002']
  verts={v for p in o.data.polygons if p.material_index in indices for v in p.vertices}
  row['glass_center']=list(sum((o.data.vertices[i].co for i in verts),Vector())/len(verts))
 print('TEAM_COLLISION_READY',row['name'],row['collision'])
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
