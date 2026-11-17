"""Bake source atlases onto new low-mesh UVs so decimation cannot scramble them."""
import bpy,json,math,bmesh
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tools/ArtSource/TeamModels';rows=json.loads((OUT/'manifest.json').read_text(encoding='utf-8'))
for row in rows:
 if row['name']!='Escombros':continue
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(Path.home()/'Downloads'/row['source']))
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0]
 if len(parts)>1:bpy.ops.object.join()
 high=bpy.context.object;high.name='Source_High';bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 for m in high.data.materials:
  if not m:continue
  nodes=m.node_tree.nodes;bs=next((n for n in nodes if n.type=='BSDF_PRINCIPLED'),None);em=next((n for n in nodes if n.type=='EMISSION'),None)
  pin=bs.inputs['Base Color'] if bs else em.inputs['Color'];incoming=pin.links[0].from_socket if pin.links else None;color=list(pin.default_value)
  out=next(n for n in nodes if n.type=='OUTPUT_MATERIAL');em=nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=color;em.inputs['Strength'].default_value=1
  if incoming:m.node_tree.links.new(incoming,em.inputs['Color'])
  m.node_tree.links.new(em.outputs[0],out.inputs['Surface'])
 low=high.copy();low.data=high.data.copy();bpy.context.collection.objects.link(low);low.name=row['mesh'];bpy.context.view_layer.objects.active=low
 bpy.ops.object.select_all(action='DESELECT');low.select_set(True)
 low.data.calc_loop_triangles();budget=45000 if row['name']=='Escombros' else 60000
 mod=low.modifiers.new('Budget','DECIMATE');mod.ratio=budget/len(low.data.loop_triangles);mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 bm=bmesh.new();bm.from_mesh(low.data);loose=[v for v in bm.verts if not v.link_faces]
 if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
 bm.to_mesh(low.data);bm.free()
 while low.data.uv_layers:low.data.uv_layers.remove(low.data.uv_layers[0])
 low.data.uv_layers.new(name='UV_Baked');bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.002,area_weight=.1);bpy.ops.object.mode_set(mode='OBJECT')
 image=bpy.data.images.new('Baked_Color',width=2048,height=2048,alpha=False);image.colorspace_settings.name='sRGB'
 mat=bpy.data.materials.new('M_'+row['name']+'_0');mat.use_nodes=True;node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=image;mat.node_tree.nodes.active=node
 low.data.materials.clear();low.data.materials.append(mat)
 for p in low.data.polygons:p.material_index=0
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=1;scene.cycles.device='CPU';scene.render.bake.use_selected_to_active=True;scene.render.bake.use_clear=True;scene.render.bake.margin=4;scene.render.bake.cage_extrusion=.12;scene.render.bake.max_ray_distance=.5
 bpy.ops.object.select_all(action='DESELECT');high.select_set(True);low.select_set(True);bpy.context.view_layer.objects.active=low
 bpy.ops.object.bake(type='EMIT')
 filename='T_'+row['name']+'_0_BaseColor.png';image.filepath_raw=str(OUT/filename);image.file_format='PNG';image.save()
 bs=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');mat.node_tree.links.new(node.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.82
 bpy.data.objects.remove(high,do_unlink=True)
 coords=[v.co for v in low.data.vertices];lo=Vector([min(p[i] for p in coords) for i in range(3)]);hi=Vector([max(p[i] for p in coords) for i in range(3)]);center=Vector(((hi.x+lo.x)/2,(hi.y+lo.y)/2,lo.z));factor=row['target_cm']/max((hi-lo).x,(hi-lo).y)
 for v in low.data.vertices:v.co=(v.co-center)*factor
 low.data.update();scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.01;bpy.ops.object.select_all(action='DESELECT');low.select_set(True)
 bpy.ops.export_scene.fbx(filepath=str(OUT/(row['mesh']+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False,path_mode='STRIP')
 row['materials']=[{'slot':mat.name,'original':'Baked from the supplied source atlases','base':[1,1,1],'roughness':.82,'metallic':.15 if row['name']=='AutoDestruido' else 0,'emission':[0,0,0],'base_texture':filename,'normal_texture':None,'masked':False,'two_sided':True}]
 row['texture_bake']={'type':'emission color selected-to-active','resolution':2048,'new_uv_atlas':True,'source_appearance_preserved':True}
 print('SCAN_BAKE_COMPLETE',row['name'])
(OUT/'manifest.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
