"""Preserve Ian's walls while removing only ground faces covered by Landscape."""
import bpy,os,json,math,bmesh
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tools/ArtSource/EvaluationWalls';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.fbx(filepath=str(ROOT/'Intermediate/DeliverySource/Escenario/Escenario.fbx'))
report=[]
for o in list(bpy.context.scene.objects):
 if o.type!='MESH':continue
 points=[o.matrix_world@Vector(v) for v in o.bound_box]
 report.append({'name':o.name,'bounds':[[min(p[i] for p in points) for i in range(3)],[max(p[i] for p in points) for i in range(3)]],'faces':len(o.data.polygons)})
(OUT/'source_bounds.json').write_text(json.dumps(report,indent=2))
print('EVALUATION_SCENE',json.dumps(report))
wall_report=[]
for number,o in enumerate(sorted([o for o in bpy.context.scene.objects if o.type=='MESH'],key=lambda o:o.name),1):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 world=o.matrix_world.copy()
 for v in o.data.vertices:v.co=world@v.co*100
 from mathutils import Matrix
 o.matrix_world=Matrix.Identity(4)
 bm=bmesh.new();bm.from_mesh(o.data)
 remove=[f for f in bm.faces if abs(f.normal.z)>.9 and f.calc_center_median().z<5]
 bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(o.data);bm.free();o.data.update()
 o.name='SM_IanWalls_%02d'%number
 bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
 bpy.ops.export_scene.fbx(filepath=str(OUT/(o.name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False)
 wall_report.append({'mesh':o.name,'removed_floor_faces':len(remove),'remaining_faces':len(o.data.polygons)})
(OUT/'wall_conversion.json').write_text(json.dumps(wall_report,indent=2))
