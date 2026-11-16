"""Preserve the team's GLB, normalize its origin and export a UE static mesh."""
import bpy, os, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Tools/ArtSource/Baliza';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=str(OUT/'Baliza.glb'))
parts=[o for o in bpy.context.scene.objects if o.type=='MESH']
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0]
if len(parts)>1:bpy.ops.object.join()
o=bpy.context.object
bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
points=[o.matrix_world@Vector(p) for p in o.bound_box]
lo=Vector([min(p[i] for p in points) for i in range(3)])
hi=Vector([max(p[i] for p in points) for i in range(3)])
# Fit to a 150 cm prop, leaving the supplied proportions and materials intact.
factor=150/(hi.z-lo.z)
for v in o.data.vertices:
 v.co=(v.co-Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z)))*factor
o.name='SM_Baliza';o.location=(0,0,0)
bpy.context.scene.unit_settings.system='METRIC'
bpy.context.scene.unit_settings.scale_length=.01
bpy.ops.export_scene.fbx(filepath=str(OUT/'SM_Baliza.fbx'),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False)
(OUT/'model_info.json').write_text(json.dumps({'source':'Baliza.glb','height_cm':150,'source_bounds':[list(lo),list(hi)],'materials':[m.name for m in o.data.materials]},indent=2))
