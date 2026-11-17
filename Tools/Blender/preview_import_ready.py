import bpy,json
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[2];source=root/'Tools/ArtSource/TeamModels';out=root/'Intermediate/inspect/team-models'
for row in json.loads((source/'manifest.json').read_text(encoding='utf-8')):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
 bpy.ops.import_scene.fbx(filepath=str(root/row['source_fbx'] if row.get('source_fbx') else source/(row['mesh']+'.fbx')))
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and not o.name.startswith('UCX_')]
 for o in bpy.context.scene.objects:
  if o.name.startswith('UCX_'):o.hide_render=True
 for m in bpy.data.materials:
  if not m.use_nodes:continue
  for n in m.node_tree.nodes:
   if n.type=='TEX_IMAGE' and n.image:
    name=Path(n.image.filepath.replace('\\','/')).name
    if (source/name).exists():n.image.filepath=str(source/name);n.image.reload()
 points=[o.matrix_world@Vector(v) for o in meshes for v in o.bound_box];lo=Vector([min(p[i] for p in points) for i in range(3)]);hi=Vector([max(p[i] for p in points) for i in range(3)]);center=(lo+hi)*.5;size=max(hi-lo)
 scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=24;scene.world=bpy.data.worlds.new('Preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.17,.20,.25,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.6
 bpy.ops.object.light_add(type='AREA',location=center+Vector((size*.5,-size*.7,size)));bpy.context.object.data.energy=size*size*800;bpy.context.object.data.size=size*1.5
 bpy.ops.object.camera_add(location=center+Vector((size*1.15,-size*1.4,size*.8)));cam=bpy.context.object;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=size*1.3;cam.data.clip_end=size*20;scene.camera=cam
 scene.render.resolution_x=600;scene.render.resolution_y=600;scene.render.resolution_percentage=100;scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.render.image_settings.file_format='PNG';scene.render.filepath=str(out/(row['name']+'-ready.png'));bpy.ops.render.render(write_still=True)
