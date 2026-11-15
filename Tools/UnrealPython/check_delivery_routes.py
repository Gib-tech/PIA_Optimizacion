import json
import os
import unreal
world=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
start=next(a for a in actors if isinstance(a,unreal.PlayerStart)).get_actor_location()
report=[]
for a in actors:
    if a.get_actor_label().startswith(('Baliza_','Salida_','Enemigo_')):
        p=a.get_actor_location()
        checks=[]
        for dx,dy in [(0,180),(180,0),(-180,0),(0,-180)]:
            goal=unreal.NavigationSystemV1.project_point_to_navigation(world,p+unreal.Vector(dx,dy,0),None,None,unreal.Vector(80,80,200))
            path=unreal.NavigationSystemV1.find_path_to_location_synchronously(world,start,goal) if goal else None
            if path and path.is_valid() and not path.is_partial():
                checks.append({'goal':[goal.x,goal.y,goal.z],'points':len(path.path_points)})
        entry={'label':a.get_actor_label(),'location':[p.x,p.y,p.z],'reachable':bool(checks),'approaches':checks}
        report.append(entry)
        unreal.log('ROUTE '+json.dumps(entry))
project=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
with open(os.path.join(project,'Intermediate','inspect','delivery_routes.json'),'w',encoding='utf-8') as f:json.dump(report,f,indent=2)
