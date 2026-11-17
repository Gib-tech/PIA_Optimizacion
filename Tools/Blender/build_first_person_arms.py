"""Extrae brazos del personaje existente conservando rig, pesos y materiales.

No crea un personaje externo ni reemplaza la malla original. Ejecutar en Blender
después de inspect_presentation_assets.py.
"""
import bpy, bmesh, json
from pathlib import Path

root=Path(__file__).resolve().parents[2]
source=root/'Intermediate/inspect/project_audit/SK_SciFITrooper_Man_03.fbx'
out=root/'Tools/ArtSource/FirstPerson';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(source))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE')
report=[]
for obj in meshes:
    # Mantener sólo geometría influida por los brazos/manos; se retiran cabeza,
    # torso, piernas y accesorios que atravesarían la cámara al mirar abajo.
    arm_groups={g.index for g in obj.vertex_groups if any(n in g.name.lower() for n in
        ['lowerarm','hand_','thumb','index','middle','ring','pinky'])}
    keep={v.index for v in obj.data.vertices if sum(g.weight for g in v.groups if g.group in arm_groups)>.55}
    bm=bmesh.new();bm.from_mesh(obj.data);bm.verts.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.index not in keep],context='VERTS')
    bm.to_mesh(obj.data);bm.free();obj.data.update()
    report.append({'mesh':obj.name,'vertices':len(obj.data.vertices),'polygons':len(obj.data.polygons)})
    if not obj.data.polygons:bpy.data.objects.remove(obj,do_unlink=True)
rig.name='root'
# Los huesos virtuales exportados por Unreal no forman parte del rig deformante.
# Se retiran antes de FBX para evitar múltiples raíces al volver a importar.
bpy.context.view_layer.objects.active=rig
bpy.ops.object.mode_set(mode='EDIT')
for bone in list(rig.data.edit_bones):
    if bone.name.startswith('VB ') or bone.name.startswith('VB_'):
        rig.data.edit_bones.remove(bone)
roots=[b for b in rig.data.edit_bones if b.parent is None]
print('RIG_ROOTS',[b.name for b in roots])
# El objeto armature `root` se exporta como el hueso raíz original de Unreal.
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')
rig.select_set(True)
for obj in bpy.context.scene.objects:
    if obj.type=='MESH':obj.select_set(True)
bpy.context.view_layer.objects.active=rig
bpy.ops.export_scene.fbx(filepath=str(out/'SK_BrazosPrimeraPersona.fbx'),use_selection=True,
    object_types={'ARMATURE','MESH'},add_leaf_bones=False,bake_anim=False,
    axis_forward='-Y',axis_up='Z',use_armature_deform_only=False)
(out/'manifest.json').write_text(json.dumps({'source':str(source),'parts':report},indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'BrazosPrimeraPersona.blend'))
print('FIRST_PERSON_ARMS_READY',report)
