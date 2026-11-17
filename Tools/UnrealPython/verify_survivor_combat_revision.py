"""Reutiliza la regresión de daño real y adapta el desenlace a cinemáticas."""
import unreal,os
root=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir());path=os.path.join(root,'Tools/UnrealPython/verify_hostage_combat.py')
source=open(path,encoding='utf-8').read()
old="   assert mission.get_editor_property('Paso')==6 and unreal.GameplayStatics.is_game_paused(world)"
new="   assert mission.get_editor_property('Paso')==6\n   cinema=unreal.GameplayStatics.get_actor_of_class(world,unreal.load_class(None,'/Game/ThirdPerson/Cinematics/BP_CinematicDirector.BP_CinematicDirector_C'))\n   if cinema.get_editor_property('bActive'):cinema.call_method('FinishCinema')\n   assert unreal.GameplayStatics.is_game_paused(world)\n   assert hostage.mesh.has_valid_animation_instance() and 'SK_RehenSuperviviente' in hostage.mesh.get_skeletal_mesh_asset().get_path_name()\n   state['results']['method']='PIE con posiciones preparadas y daño final letal explícito; ataques de orbitador y embestidor por sus árboles reales. No es partida natural.'\n   state['results']['survivor_valid_anim_on_death']=True"
assert source.count(old)==1;source=source.replace(old,new).replace('Intermediate/inspect/hostage_combat_assertions.json','docs/validation/rehen-combate-revision.json')
ns={'__name__':'survivor_combat_revision','__file__':path};exec(compile(source,path,'exec'),ns)
