"""Editor recipe: convex prisms from exact coplanar render faces, retaining every door opening."""
import unreal,os,math
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,t):return tuple(x*t for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def unit(v):return mul(v,1/math.sqrt(dot(v,v)))
def hull(points):
    pts=sorted(set(points))
    def turn(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    chains=[]
    for seq in [pts,list(reversed(pts))]:
        chain=[]
        for p in seq:
            while len(chain)>1 and turn(chain[-2],chain[-1],p)<=.000001:chain.pop()
            chain.append(p)
        chains+=chain[:-1]
    return chains
def area(p):return abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p)))/2)
def prisms(path):
    vertices=[];triangles=[]
    for line in open(path,encoding='utf-8-sig'):
        if line.startswith('v '):
            x,z,y=map(float,line.split()[1:4]);vertices.append((x,y,z))
        elif line.startswith('f '):triangles.append([vertices[int(p.split('/')[0])-1] for p in line.split()[1:4]])
    groups={}
    for tri in triangles:
        n=cross(sub(tri[1],tri[0]),sub(tri[2],tri[0]))
        if dot(n,n)<1e-8:continue
        n=unit(n)
        if next(x for x in n if abs(x)>1e-5)<0:n=mul(n,-1)
        d=dot(n,tri[0]);key=tuple(round(x,4) for x in n)+(round(d,2),)
        if key not in groups:
            u=unit(cross((0,0,1) if abs(n[2])<.9 else (0,1,0),n));v=cross(n,u)
            groups[key]=(n,d,u,v,[])
        n,d,u,v,polys=groups[key]
        poly=hull([(round(dot(p,u),3),round(dot(p,v),3)) for p in tri])
        if len(poly)>2 and area(poly)>.001 and poly not in polys:polys.append(poly)
    output=[]
    for n,d,u,v,polys in groups.values():
        changed=True
        while changed:
            changed=False
            for i in range(len(polys)):
                for j in range(i+1,len(polys)):
                    if len(set(polys[i])&set(polys[j]))<2:continue
                    merged=hull(polys[i]+polys[j]);expected=area(polys[i])+area(polys[j])
                    if abs(area(merged)-expected)>max(.02,expected*.00001):continue
                    polys[i]=merged;polys.pop(j);changed=True;break
                if changed:break
        for poly in polys:
            face=[add(add(mul(u,x),mul(v,y)),mul(n,d)) for x,y in poly]
            output.append([add(p,mul(n,offset)) for offset in [-.6,.6] for p in face])
    return output
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='Nivel_Entrega'
assert not unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
for i in range(1,5):
    mesh=unreal.load_asset('/Game/ThirdPerson/Environment/EscenarioIan/Escenario_Sector'+str(i))
    path=os.path.join(project,'Intermediate/inspect','wall_source_'+str(i)+'.obj')
    task=unreal.AssetExportTask();task.object=mesh;task.filename=path;task.automated=True;task.prompt=False;task.replace_identical=True
    assert unreal.Exporter.run_asset_export_task(task)
    shapes=[]
    for j,points in enumerate(prisms(path)):
        def vec(p):return '(X=%.6f,Y=%.6f,Z=%.6f)'%p
        bounds=[tuple(fn(p[k] for p in points) for k in range(3)) for fn in [min,max]]
        text='(VertexData=('+','.join(vec(p) for p in points)+'),ElemBox=(Min='+vec(bounds[0])+',Max='+vec(bounds[1])+',IsValid=True),Name="WallFace'+str(j)+'")'
        shape=unreal.KConvexElem();assert shape.import_text(text);shapes.append(shape)
    body=unreal.new_object(unreal.BodySetup,outer=mesh)
    body.set_editor_property('collision_trace_flag',unreal.CollisionTraceFlag.CTF_USE_SIMPLE_AND_COMPLEX)
    body.set_editor_property('double_sided_geometry',True)
    agg=unreal.KAggregateGeom();agg.set_editor_property('convex_elems',shapes)
    body.set_editor_property('agg_geom',agg)
    mesh.modify();mesh.set_editor_property('body_setup',body)
    unreal.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
    for actor in unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors():
        if isinstance(actor,unreal.StaticMeshActor) and actor.static_mesh_component.static_mesh==mesh:
            actor.static_mesh_component.set_static_mesh(None);actor.static_mesh_component.set_static_mesh(mesh)
    unreal.log('PRECISE_WALL_PRISMS '+mesh.get_name()+' shapes='+str(len(shapes)))
unreal.SystemLibrary.execute_console_command(world,'RebuildNavigation')
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
