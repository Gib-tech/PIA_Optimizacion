"""Extend the existing wall caps and cover two existing rooms, using the current kit."""
import bpy,json,bmesh
from pathlib import Path
root=Path(__file__).resolve().parents[2];out=root/'Tools/ArtSource/Atmosphere'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=.01
verts=[];faces=[]
for i in range(1,5):
    local=[]
    for line in (root/f'Intermediate/inspect/evaluation_wall_{i}.obj').read_text().splitlines():
        p=line.split()
        if p and p[0]=='v':local.append((float(p[1])*2,float(p[3])*2,float(p[2])*2))
        elif p and p[0]=='f':faces.append([local[int(v.split('/')[0])-1] for v in p[1:]])
def export(name,points,polygons):
    # Existing FBX recipes convert Blender +Y into UE -Y.
    mesh=bpy.data.meshes.new(name);mesh.from_pydata([(x,-y,z) for x,y,z in points],[],[tuple(reversed(f)) for f in polygons]);mesh.update()
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
    layer=mesh.uv_layers.new(name='UVMap')
    for face in mesh.polygons:
        axis=max(range(3),key=lambda i:abs(face.normal[i]))
        axes=[i for i in range(3) if i!=axis]
        for index in face.loop_indices:
            v=mesh.vertices[mesh.loops[index].vertex_index].co
            layer.data[index].uv=(v[axes[0]]/400,v[axes[1]]/400)
    o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bpy.ops.export_scene.fbx(filepath=str(out/(name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False)
def prism(poly,z0,z1,points,polygons):
    n=len(poly);base=len(points);points.extend([(x,y,z0) for x,y in poly]+[(x,y,z1) for x,y in poly])
    polygons.extend([tuple(base+i for i in reversed(range(n))),tuple(base+n+i for i in range(n))])
    for i in range(n):j=(i+1)%n;polygons.append((base+i,base+j,base+n+j,base+n+i))
rooms=[('Rescate',(-1250,-1510,1250,100),[(-1170,60),(1170,60),(715,-1470),(-715,-1470)]),('Deposito',(-5000,-5900,-2350,-4100),[(-4900,-4160),(-2500,-4160),(-2500,-5820),(-4900,-5820)])]
report=[]
for name,bounds,roof in rooms:
    pts=[];polys=[];count=0
    for face in faces:
        if len(face)<3 or min(p[2] for p in face)<370:continue
        if max(p[2] for p in face)-min(p[2] for p in face)>6:continue
        x=sum(p[0] for p in face)/len(face);y=sum(p[1] for p in face)/len(face)
        if not(bounds[0]<x<bounds[2] and bounds[1]<y<bounds[3]):continue
        # Copy the existing cap footprint. Adjacent top triangles remain nonblocking at floor height.
        prism([(p[0],p[1]) for p in face],395,420,pts,polys);count+=1
    export('SM_UpperWalls_'+name,pts,polys)
    pts=[];polys=[];prism(roof,420,442,pts,polys);export('SM_Roof_'+name,pts,polys)
    report.append({'room':name,'wall_cap_faces_extended':count,'ceiling_cm':420,'footprint':roof})
(out/'shelters.json').write_text(json.dumps(report,indent=2))
print('COMPOUND_SHELTERS',report)

# Split the old sector-wide meshes into individual buildings with local pivots.
# Preserve source UVs/materials; this improves WP bounds and occlusion granularity.
centers=[('Rescate',0,-700),('Arena',0,-3250),('Jardin',3150,-3650),('Deposito',-3700,-5000),('Servicio',2650,-5500),('PatioNorte',0,-5600),('Atrio',0,-7450),('AlaOeste',-3600,-9650),('AlaEste',3600,-9650),('Salida',0,-11000)]
groups={name:[] for name,x,y in centers}
for sector in range(1,5):
    pos=[];uv=[]
    for line in (root/f'Intermediate/inspect/evaluation_wall_{sector}.obj').read_text().splitlines():
        p=line.split()
        if p and p[0]=='v':pos.append((float(p[1])*2,float(p[3])*2,float(p[2])*2))
        elif p and p[0]=='vt':uv.append(tuple(map(float,p[1:3])))
        elif p and p[0]=='f':
            face=[];tex=[]
            for token in p[1:]:
                ids=token.split('/');face.append(pos[int(ids[0])-1]);tex.append(uv[int(ids[1])-1] if len(ids)>1 and ids[1] else (0,0))
            x=sum(v[0] for v in face)/len(face);y=sum(v[1] for v in face)/len(face)
            name,cx,cy=min(centers,key=lambda c:(c[1]-x)**2+(c[2]-y)**2)
            groups[name].append((face,tex,sector-1))
materials=[bpy.data.materials.new('Sector'+str(i)) for i in range(1,5)]
for name,cx,cy in centers:
    points=[];polys=[];tex=[];slots=[]
    for face,uv,slot in groups[name]:
        base=len(points);points.extend([(p[0]-cx,-(p[1]-cy),p[2]) for p in reversed(face)])
        polys.append(tuple(range(base,len(points))));tex.extend(reversed(uv));slots.append(slot)
    mesh=bpy.data.meshes.new('SM_Walls_'+name);mesh.from_pydata(points,[],polys);mesh.update()
    for material in materials:mesh.materials.append(material)
    layer=mesh.uv_layers.new(name='UVMap')
    for loop,coord in zip(layer.data,tex):loop.uv=coord
    for face,slot in zip(mesh.polygons,slots):face.material_index=slot
    o=bpy.data.objects.new(mesh.name,mesh);bpy.context.collection.objects.link(o)
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bpy.ops.export_scene.fbx(filepath=str(out/(mesh.name+'.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,apply_scale_options='FBX_SCALE_UNITS',axis_forward='-Y',axis_up='Z',bake_space_transform=True,add_leaf_bones=False)
(out/'building_layout.json').write_text(json.dumps([{'name':n,'center':[x,y,0],'faces':len(groups[n])} for n,x,y in centers],indent=2))
(root/'Intermediate/inspect/reimport_compound_walls.flag').touch()
