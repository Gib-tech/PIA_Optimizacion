"""Normalize supplied models, retain UVs/material regions, reduce scans and export."""
import bpy,os,json,math,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tools/ArtSource/TeamModels';OUT.mkdir(parents=True,exist_ok=True)
QA=ROOT/'Intermediate/inspect/team-models'
SPECS=[('Edificio','edificio.fbx','height',3300,None),('Farol','Faro.fbx','height',460,None),('Escombros','waste_construction_lumber.glb','width',350,45000),('ArbolFab','realistic_tree.glb','height',700,None)]
rows=[]
for name,filename,fit,target,budget in SPECS:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 path=QA/filename if name=='ArbolFab' else Path.home()/'Downloads'/filename
 if filename.endswith('.fbx'):bpy.ops.import_scene.fbx(filepath=str(path))
 else:bpy.ops.import_scene.gltf(filepath=str(path))
 parts=[o for o in bpy.context.scene.objects if o.type=='MESH'];bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0]
 if len(parts)>1:bpy.ops.object.join()
 o=bpy.context.object;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 pts=[Vector(v) for v in o.bound_box];lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)])
 factor=target/((hi-lo).z if fit=='height' else max((hi-lo).x,(hi-lo).y));origin=Vector(((hi.x+lo.x)/2,(hi.y+lo.y)/2,lo.z))
 for v in o.data.vertices:v.co=(v.co-origin)*factor
 o.name='SM_'+name;o.location=(0,0,0);o.data.calc_loop_triangles();before=len(o.data.loop_triangles)
 if budget and before>budget:
  mod=o.modifiers.new('Scan budget with UV preservation','DECIMATE');mod.ratio=budget/before;mod.use_collapse_triangulate=True
  bpy.ops.object.modifier_apply(modifier=mod.name)
 o.data.calc_loop_triangles();after=len(o.data.loop_triangles)
 mats=[]
 for i,m in enumerate(o.data.materials):
  if not m:continue
  original=m.name;m.name='M_'+name+'_'+str(i)
  bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
  if not bs:
   # Some scan surfaces use KHR_materials_unlit. Retain their atlas in a lit
   # rough material so they react consistently to the level's illumination.
   emission=next((n for n in m.node_tree.nodes if n.type=='EMISSION'),None)
   assert emission,original
   bs=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.9
   if emission.inputs['Color'].links:
    link=emission.inputs['Color'].links[0];m.node_tree.links.new(link.from_socket,bs.inputs['Base Color'])
   else:bs.inputs['Base Color'].default_value=emission.inputs['Color'].default_value
   output=next(n for n in m.node_tree.nodes if n.type=='OUTPUT_MATERIAL');m.node_tree.links.new(bs.outputs['BSDF'],output.inputs['Surface'])
  # Missing FBX textures are replaced deliberately, retaining the author's regions.
  if name in ['Edificio','Farol']:
   for n in list(m.node_tree.nodes):
    if n.type not in ['BSDF_PRINCIPLED','OUTPUT_MATERIAL']:m.node_tree.nodes.remove(n)
   if name=='Edificio':base,metal,rough,em=({'Material':((.24,.27,.28),.1,.82,0),'Material.001':((.027,.09,.13),.7,.22,0),'Material.002':((.065,.08,.10),.65,.4,0)})[original]
   else:base,metal,rough,em=((1,.60,.22),0,.3,3) if original=='Material.002' else ((.028,.034,.042),.78,.35,0)
   bs.inputs['Base Color'].default_value=(*base,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
   if em:bs.inputs['Emission'].default_value=(*(c*em for c in base),1)
  base_link=bs.inputs['Base Color'].links[0].from_node if bs.inputs['Base Color'].links else None
  normal_link=bs.inputs['Normal'].links[0].from_node if bs.inputs['Normal'].links else None
  def texture(node,kind):
   if not node:return None
   if node.type=='NORMAL_MAP':node=node.inputs['Color'].links[0].from_node
   if node.type!='TEX_IMAGE' or not node.image:return None
   im=node.image;limit=2048 if name=='ArbolFab' else 1024
   if max(im.size)>limit:im.scale(round(im.size[0]*limit/max(im.size)),round(im.size[1]*limit/max(im.size)))
   fname='T_'+name+'_'+str(i)+'_'+kind+'.png';im.filepath_raw=str(OUT/fname);im.file_format='PNG';im.save();return fname
  diffuse=texture(base_link,'BaseColor');normal=texture(normal_link,'Normal')
  masked=m.blend_method in ['CLIP','HASHED','BLEND'] and name=='ArbolFab'
  mats.append({'slot':m.name,'original':original,'base':list(bs.inputs['Base Color'].default_value)[:3],'roughness':float(bs.inputs['Roughness'].default_value),'metallic':float(bs.inputs['Metallic'].default_value),'emission':list(bs.inputs['Emission'].default_value)[:3],'base_texture':diffuse,'normal_texture':normal,'masked':masked,'two_sided':not m.use_backface_culling})
 glass=None
 if name=='Farol':
  ids=[i for i,m in enumerate(mats) if m['original']=='Material.002']
  vertices={v for p in o.data.polygons if p.material_index in ids for v in p.vertices}
  glass=list(sum((o.data.vertices[i].co for i in vertices),Vector())/len(vertices))
 bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
 bpy.ops.export_scene.fbx(filepath=str(OUT/(o.name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False,path_mode='STRIP')
 row={'name':name,'mesh':o.name,'source':filename,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'original_triangles':before,'exported_triangles':after,'target_cm':target,'fit':fit,'materials':mats,'glass_center':glass};rows.append(row)
 print('TEAM_MODEL_PREPARED',name,before,after)
 # Review the optimized asset with its supplied textures.
 scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=24
 scene.world=bpy.data.worlds.new('Preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.17,.20,.25,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.6
 pts=[Vector(v) for v in o.bound_box];lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)]);center=(lo+hi)*.5;size=max(hi-lo)
 bpy.ops.object.light_add(type='AREA',location=center+Vector((size*.5,-size*.7,size)));bpy.context.object.data.energy=size*size*800;bpy.context.object.data.size=size*1.5
 bpy.ops.object.camera_add(location=center+Vector((size*1.15,-size*1.4,size*.8)));cam=bpy.context.object;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=size*1.3;cam.data.clip_end=size*20;scene.camera=cam
 scene.render.resolution_x=600;scene.render.resolution_y=600;scene.render.resolution_percentage=100;scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.render.image_settings.file_format='PNG';scene.render.filepath=str(QA/(name+'-prepared.png'))
 bpy.ops.render.render(write_still=True)
(OUT/'manifest.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf-8')
