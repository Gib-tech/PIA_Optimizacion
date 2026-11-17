import bpy,os,json,math
from mathutils import Vector
root=os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'));out=os.path.join(root,'Intermediate/inspect/team-models')
for filename in ['edificio.fbx','Faro.fbx','waste_construction_lumber.glb','destroyed_car_1_raw_scan.glb']:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 path=os.path.join(os.path.expanduser('~/Downloads'),filename)
 if filename.endswith('.fbx'):bpy.ops.import_scene.fbx(filepath=path)
 else:bpy.ops.import_scene.gltf(filepath=path)
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
 lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)]);center=(hi+lo)*.5;size=max(hi-lo)
 scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=24
 scene.world=bpy.data.worlds.new('Preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.17,.20,.25,1)
 scene.world.node_tree.nodes['Background'].inputs[1].default_value=.6
 bpy.ops.object.light_add(type='AREA',location=center+Vector((size*.5,-size*.7,size)));bpy.context.object.data.energy=size*size*800;bpy.context.object.data.size=size*1.5
 bpy.ops.object.camera_add(location=center+Vector((size*1.15,-size*1.4,size*.8)));cam=bpy.context.object;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=size*1.3;scene.camera=cam
 scene.render.resolution_x=500;scene.render.resolution_y=500;scene.render.resolution_percentage=100;scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast';scene.render.image_settings.file_format='PNG';scene.render.filepath=os.path.join(out,filename.split('.')[0]+'-source.png')
 bpy.ops.render.render(write_still=True)
