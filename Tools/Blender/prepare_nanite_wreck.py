"""Keep the raw scan's original UV surface for Nanite, without destructive reduction."""
import bpy,json,math,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tools/ArtSource/TeamModels';QA=ROOT/'Intermediate/inspect/team-models';rows=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
row=next((r for r in rows if r['name']=='AutoDestruido'),None)
if row is None:
 row={'name':'AutoDestruido','mesh':'SM_AutoDestruido','source':'destroyed_car_1_raw_scan.glb','target_cm':450,'fit':'width'};rows.append(row)
row['source_sha256']=hashlib.sha256((Path.home()/'Downloads'/row['source']).read_bytes()).hexdigest()
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path.home()/'Downloads'/row['source']))
parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
if len(parts)>1:bpy.ops.object.join()
o=bpy.context.object;world_matrix=o.matrix_world.copy();o.parent=None;o.matrix_world=world_matrix;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.name=row['mesh']
o.data.calc_loop_triangles();row['original_triangles']=len(o.data.loop_triangles)
positions=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',positions);positions=positions.reshape(-1,3)
ids=np.empty(len(o.data.loops),dtype=np.int32);o.data.loops.foreach_get('vertex_index',ids);used=np.unique(ids);xy=positions[used[::100],:2];values,vectors=np.linalg.eigh(np.cov(xy.T));v=vectors[:,-1];angle=math.atan2(v[1],v[0]);o.rotation_euler.z=-angle;bpy.ops.object.transform_apply(location=False,rotation=True,scale=False)
o.data.vertices.foreach_get('co',positions.reshape(-1));lo=positions[used].min(axis=0);hi=positions[used].max(axis=0);factor=450/max((hi-lo)[:2]);center=np.array([(lo[0]+hi[0])/2,(lo[1]+hi[1])/2,lo[2]]);positions=(positions-center)*factor;o.data.vertices.foreach_set('co',positions.astype(np.float32).reshape(-1));o.data.update()
image=next(n.image for m in o.data.materials if m and m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image)
image.filepath_raw=str(OUT/'T_AutoDestruido_0_BaseColor.png');image.file_format='PNG';image.save()
mat=o.data.materials[0];mat.name='M_AutoDestruido_0';row['materials']=[{'slot':mat.name,'original':'Original scan UV atlas','base':[1,1,1],'roughness':.85,'metallic':.15,'emission':[0,0,0],'base_texture':'T_AutoDestruido_0_BaseColor.png','normal_texture':None,'masked':False,'two_sided':True}]
lo=(lo-center)*factor;hi=(hi-center)*factor;bpy.ops.object.select_all(action='DESELECT');bpy.ops.mesh.primitive_cube_add(size=1,location=tuple((lo+hi)*.5));ucx=bpy.context.object;ucx.name='UCX_'+row['mesh']+'_00';ucx.dimensions=tuple(hi-lo);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.select_set(True)
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
fbx=QA/(row['mesh']+'.fbx');bpy.ops.export_scene.fbx(filepath=str(fbx),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False,path_mode='STRIP')
row.update(nanite=True,source_fbx='Intermediate/inspect/team-models/'+row['mesh']+'.fbx',exported_triangles=row['original_triangles'],bounds_cm={'min':lo.tolist(),'max':hi.tolist()},collision={'type':'simple_box','size_cm':(hi-lo).tolist()},texture_preservation='Original source geometry and UVs retained; Nanite streams detail')
row.pop('texture_bake',None);(OUT/'manifest.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8');print('NANITE_WRECK_EXPORTED',fbx.stat().st_size)
